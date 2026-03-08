from datetime import datetime, timedelta
from functools import wraps
from collections import deque
import logging
import os
import json

from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from dotenv import load_dotenv
from sqlalchemy.exc import OperationalError
from sqlalchemy import inspect, text
from werkzeug.utils import secure_filename

from config import DEV_FALLBACK_SECRET, config
from models import Categoria, ClientePublico, EnderecoEstoque, Estoque, Fornecedor, Funcionario, FuncaoRH, Movimentacao, Produto, PermissaoAcesso, Caixa, MovimentacaoCaixa, Pedido, ItemPedido, Garcom, EmpresaConfig, AuditoriaEvento, db
from routes.estoque_routes import register_estoque_routes
from routes.vendas_routes import register_vendas_routes
from routes.public_routes import obter_resumo_carrinho_site, register_public_routes
from security import csrf_input_tag, csrf_protect_request, ensure_csrf_token, is_json_request, json_response
from app import extensions
from app.cli import register_cli
from app.services.analytics import calcular_metricas_dashboard
from app.constants import (
    CARGOS_PERMANENTES,
    ENDPOINT_TO_PAGINA,
    PAGINAS_SISTEMA,
    PAGINAS_SISTEMA_MENU_ORDEM,
    ROLES_PERMITIDOS,
    TIPOS_MOVIMENTACAO_VALIDOS,
)
from app.utils.data import parse_date_range

# Informacoes do SystemLR
APP_NAME = 'SystemLR'
APP_VERSION = '1.0.0'
APP_DOMAIN = 'systemlr.com'

LOGIN_MAX_ATTEMPTS = 5
LOGIN_WINDOW_SECONDS = 300  # 5 minutes window
_failed_login_attempts = {}

TIPO_NEGOCIO_PRESETS = {
    EmpresaConfig.TIPO_NEGOCIO_CONVENIENCIA: {
        EmpresaConfig.CANAL_OPERACAO_FISICO: {'atendimento_mesas_ativo': True, 'separacao_entrega_ativa': False},
        EmpresaConfig.CANAL_OPERACAO_ECOMMERCE: {'atendimento_mesas_ativo': False, 'separacao_entrega_ativa': True},
        EmpresaConfig.CANAL_OPERACAO_HIBRIDO: {'atendimento_mesas_ativo': True, 'separacao_entrega_ativa': True},
    },
    EmpresaConfig.TIPO_NEGOCIO_SUPERMERCADO: {
        EmpresaConfig.CANAL_OPERACAO_FISICO: {'atendimento_mesas_ativo': False, 'separacao_entrega_ativa': False},
        EmpresaConfig.CANAL_OPERACAO_ECOMMERCE: {'atendimento_mesas_ativo': False, 'separacao_entrega_ativa': True},
        EmpresaConfig.CANAL_OPERACAO_HIBRIDO: {'atendimento_mesas_ativo': False, 'separacao_entrega_ativa': True},
    },
    EmpresaConfig.TIPO_NEGOCIO_FARMACIA: {
        EmpresaConfig.CANAL_OPERACAO_FISICO: {'atendimento_mesas_ativo': False, 'separacao_entrega_ativa': False},
        EmpresaConfig.CANAL_OPERACAO_ECOMMERCE: {'atendimento_mesas_ativo': False, 'separacao_entrega_ativa': True},
        EmpresaConfig.CANAL_OPERACAO_HIBRIDO: {'atendimento_mesas_ativo': False, 'separacao_entrega_ativa': True},
    },
    EmpresaConfig.TIPO_NEGOCIO_MODA: {
        EmpresaConfig.CANAL_OPERACAO_FISICO: {'atendimento_mesas_ativo': False, 'separacao_entrega_ativa': False},
        EmpresaConfig.CANAL_OPERACAO_ECOMMERCE: {'atendimento_mesas_ativo': False, 'separacao_entrega_ativa': True},
        EmpresaConfig.CANAL_OPERACAO_HIBRIDO: {'atendimento_mesas_ativo': False, 'separacao_entrega_ativa': True},
    },
    EmpresaConfig.TIPO_NEGOCIO_HOME_CENTER: {
        EmpresaConfig.CANAL_OPERACAO_FISICO: {'atendimento_mesas_ativo': False, 'separacao_entrega_ativa': False},
        EmpresaConfig.CANAL_OPERACAO_ECOMMERCE: {'atendimento_mesas_ativo': False, 'separacao_entrega_ativa': True},
        EmpresaConfig.CANAL_OPERACAO_HIBRIDO: {'atendimento_mesas_ativo': False, 'separacao_entrega_ativa': True},
    },
    EmpresaConfig.TIPO_NEGOCIO_OUTRO: {
        EmpresaConfig.CANAL_OPERACAO_FISICO: {'atendimento_mesas_ativo': False, 'separacao_entrega_ativa': False},
        EmpresaConfig.CANAL_OPERACAO_ECOMMERCE: {'atendimento_mesas_ativo': False, 'separacao_entrega_ativa': True},
        EmpresaConfig.CANAL_OPERACAO_HIBRIDO: {'atendimento_mesas_ativo': False, 'separacao_entrega_ativa': True},
    },
}

load_dotenv()
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
app = Flask(
    __name__,
    template_folder=os.path.join(PROJECT_ROOT, 'templates'),
    static_folder=os.path.join(PROJECT_ROOT, 'static'),
)
config_name = (os.environ.get('FLASK_CONFIG') or os.environ.get('APP_ENV') or 'development').strip().lower()
if config_name not in config:
    config_name = 'default'
app.config.from_object(config[config_name])
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.logger.setLevel(logging.INFO)
if not app.logger.handlers:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(name)s %(message)s',
    )

if app.config.get('ENV_NAME') == 'production' and app.config.get('SECRET_KEY') == DEV_FALLBACK_SECRET:
    raise RuntimeError('SECRET_KEY insegura em producao. Defina a variavel de ambiente SECRET_KEY.')

# Inicializar banco de dados
db.init_app(app)
extensions.init_extensions(app, db)
register_cli(app)


def _garantir_cargos_permanentes():
    try:
        nomes_existentes = {(f.nome or '').strip().lower() for f in FuncaoRH.query.all()}
        mudou = False
        for nome_cargo, descricao_cargo in CARGOS_PERMANENTES:
            if nome_cargo.lower() not in nomes_existentes:
                db.session.add(FuncaoRH(nome=nome_cargo, descricao=descricao_cargo, ativo=True))
                mudou = True
        if mudou:
            db.session.commit()
    except OperationalError:
        db.session.rollback()


with app.app_context():
    # A estrutura do schema deve ser aplicada via Flask-Migrate/Alembic.
    inspector = inspect(db.engine)
    colunas_funcoes = {col['name'] for col in inspector.get_columns('funcoes_rh')}
    if 'permissoes_padrao' not in colunas_funcoes:
        try:
            db.session.execute(text('ALTER TABLE funcoes_rh ADD COLUMN permissoes_padrao TEXT'))
            db.session.commit()
        except Exception:
            db.session.rollback()
    if inspector.has_table('empresa_config'):
        colunas_empresa = {col['name'] for col in inspector.get_columns('empresa_config')}
        colunas_novas_empresa = {
            'separacao_entrega_ativa': 'INTEGER DEFAULT 1',
            'emissao_etiqueta_entrega_ativa': 'INTEGER DEFAULT 1',
            'separacao_entrega_unir_vendas_off': 'INTEGER DEFAULT 0',
            'tipo_negocio': "VARCHAR(30) DEFAULT 'conveniencia'",
            'canal_operacao': "VARCHAR(30) DEFAULT 'hibrido'",
            'ecommerce_ativo': 'INTEGER DEFAULT 1',
            'ecom_cor_primaria': "VARCHAR(20) DEFAULT '#ff7848'",
            'ecom_cor_secundaria': "VARCHAR(20) DEFAULT '#ff5a2a'",
            'ecom_titulo_banner': 'VARCHAR(140)',
            'ecom_subtitulo_banner': 'VARCHAR(255)',
            'ecom_texto_promocao': 'VARCHAR(255)',
            'ecom_banner_path': 'VARCHAR(255)',
            'ecom_favicon_path': 'VARCHAR(255)',
            'ecom_produto_placeholder_path': 'VARCHAR(255)',
            'ecom_banners_json': 'TEXT',
            'ecom_campanhas_json': 'TEXT',
            'ecom_footer_bg': "VARCHAR(20) DEFAULT '#1f2b38'",
            'ecom_footer_texto': 'VARCHAR(255)',
            'ecom_footer_contato': 'VARCHAR(255)',
            'ecom_footer_creditos': 'VARCHAR(255)',
        }
        for coluna_nome, definicao in colunas_novas_empresa.items():
            if coluna_nome in colunas_empresa:
                continue
            try:
                db.session.execute(text(f'ALTER TABLE empresa_config ADD COLUMN {coluna_nome} {definicao}'))
                db.session.commit()
            except Exception:
                db.session.rollback()
    if inspector.has_table('pedidos'):
        colunas_pedidos = {col['name'] for col in inspector.get_columns('pedidos')}
        colunas_novas_pedidos = {
            'separacao_entrega_concluida': 'INTEGER DEFAULT 0',
            'separacao_entrega_em': 'DATETIME',
            'etiqueta_entrega_emitida_em': 'DATETIME',
        }
        for coluna_nome, definicao in colunas_novas_pedidos.items():
            if coluna_nome in colunas_pedidos:
                continue
            try:
                db.session.execute(text(f'ALTER TABLE pedidos ADD COLUMN {coluna_nome} {definicao}'))
                db.session.commit()
            except Exception:
                db.session.rollback()
    _garantir_cargos_permanentes()
    if not inspector.has_table('clientes_publicos'):
        ClientePublico.__table__.create(bind=db.engine, checkfirst=True)


# ============ DECORADORES DE AUTENTICACAO ============

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'funcionario_id' not in session:
            if is_json_request():
                return json_response(False, 'Você precisa fazer login.', status=401, code='auth_required')
            flash('Você precisa fazer login para acessar esta página.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


def require_role(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'funcionario_id' not in session:
                if is_json_request():
                    return json_response(False, 'Você precisa fazer login.', status=401, code='auth_required')
                flash('Você precisa fazer login.', 'warning')
                return redirect(url_for('login'))

            funcionario = Funcionario.query.get(session['funcionario_id'])
            if not funcionario or not funcionario.ativo:
                session.clear()
                if is_json_request():
                    return json_response(False, 'Funcionario inativo ou removido.', status=403, code='forbidden')
                flash('Funcionario inativo ou removido.', 'danger')
                return redirect(url_for('login'))

            if funcionario.role not in roles:
                if is_json_request():
                    return json_response(False, 'Sem permissao para executar esta operacao.', status=403, code='forbidden')
                flash('Você não tem permissão para acessar esta página.', 'danger')
                return redirect(url_for('dashboard'))

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def _client_ip():
    if request.access_route:
        return request.access_route[-1]
    return request.remote_addr or 'unknown'


def _purge_old_attempts(attempts: deque):
    now = datetime.utcnow()
    while attempts and (now - attempts[0]).total_seconds() > LOGIN_WINDOW_SECONDS:
        attempts.popleft()


def _is_login_rate_limited(ip_addr: str) -> bool:
    attempts = _failed_login_attempts.get(ip_addr)
    if not attempts:
        return False
    _purge_old_attempts(attempts)
    return len(attempts) >= LOGIN_MAX_ATTEMPTS


def _register_login_attempt(ip_addr: str, success: bool):
    attempts = _failed_login_attempts.setdefault(ip_addr, deque())
    _purge_old_attempts(attempts)
    if success:
        attempts.clear()
    else:
        attempts.append(datetime.utcnow())


def _limit(rule: str):
    """Decorador de rate-limit com fallback quando Flask-Limiter nao estiver disponivel."""
    def decorator(func):
        if extensions.limiter is None:
            return func
        return extensions.limiter.limit(rule)(func)
    return decorator


# ============ FUNCOES AUXILIARES ============

def get_funcionario_logado():
    if 'funcionario_id' in session:
        return Funcionario.query.get(session['funcionario_id'])
    return None


def _normalizar_texto(valor):
    return (valor or '').strip().lower()


def _role_para_cargo_padrao(role):
    mapa = {
        'admin': 'Administrador',
        'gerente': 'Gerente',
        'caixa': 'Caixa',
        'operador': 'Operador',
        'garcom': 'Garcom',
    }
    return mapa.get((role or '').strip().lower(), 'Operador')


def sincronizar_garcom_funcionario(funcionario):
    if not funcionario:
        return

    role_norm = _normalizar_texto(funcionario.role)
    cargo_norm = _normalizar_texto(funcionario.cargo)
    deve_ser_garcom = role_norm == 'garcom' or cargo_norm in {'garcom', 'garçom'}

    garcom = Garcom.query.filter_by(funcionario_id=funcionario.id).first()

    if deve_ser_garcom:
        if not garcom:
            garcom = Garcom(
                funcionario_id=funcionario.id,
                nome=funcionario.nome,
                ativo=funcionario.ativo,
            )
            db.session.add(garcom)
        else:
            garcom.nome = funcionario.nome
            garcom.ativo = funcionario.ativo
        return

    if garcom:
        garcom.nome = funcionario.nome
        # Ao trocar de funcao, o perfil de garcom deixa de participar da distribuicao automatica.
        garcom.ativo = False


def funcionario_tem_acesso(funcionario, endpoint):
    if not funcionario:
        return False
    if funcionario.role == 'admin':
        return True
    if not funcionario.controle_acesso_ativo:
        return True

    pagina = ENDPOINT_TO_PAGINA.get(endpoint)
    if not pagina:
        if request.path.startswith('/api/'):
            return False
        return True

    return PermissaoAcesso.query.filter_by(funcionario_id=funcionario.id, pagina=pagina).first() is not None


def aplicar_movimentacao_estoque(produto, tipo, quantidade):
    if tipo not in TIPOS_MOVIMENTACAO_VALIDOS:
        return 'Tipo de movimentação inválido'

    if quantidade <= 0:
        return 'Quantidade deve ser maior que 0'

    if tipo == Movimentacao.TIPO_ENTRADA:
        produto.quantidade_estoque += quantidade
        return None

    if produto.quantidade_estoque < quantidade:
        return 'Quantidade em estoque insuficiente'

    produto.quantidade_estoque -= quantidade
    return None


def _resumir_payload_requisicao():
    dados = {}
    try:
        if request.is_json:
            payload = request.get_json(silent=True) or {}
            if isinstance(payload, dict):
                dados = payload
        else:
            dados = request.form.to_dict(flat=True)
    except Exception:
        dados = {}

    chaves_sensiveis = {'senha', 'confirmacao_senha', 'password', 'token', 'csrf_token'}
    resumo = []
    for chave, valor in dados.items():
        chave_norm = (chave or '').strip().lower()
        if chave_norm in chaves_sensiveis:
            continue
        texto_valor = str(valor)
        if len(texto_valor) > 80:
            texto_valor = f'{texto_valor[:77]}...'
        resumo.append(f'{chave}={texto_valor}')
        if len(resumo) >= 10:
            break

    return '; '.join(resumo)


def registrar_evento_auditoria(*, funcionario=None, acao='acao', entidade=None, detalhes='', status_code=None):
    try:
        funcionario_id = None
        funcionario_nome = None
        funcionario_email = None
        funcionario_role = None
        if funcionario:
            funcionario_id = funcionario.id
            funcionario_nome = funcionario.nome
            funcionario_email = funcionario.email
            funcionario_role = funcionario.role

        evento = AuditoriaEvento(
            funcionario_id=funcionario_id,
            funcionario_nome=funcionario_nome,
            funcionario_email=funcionario_email,
            funcionario_role=funcionario_role,
            metodo=request.method,
            endpoint=request.endpoint,
            rota=request.path,
            acao=acao,
            entidade=entidade,
            detalhes=detalhes,
            status_code=status_code,
            ip=(request.headers.get('X-Forwarded-For') or request.remote_addr),
        )
        db.session.add(evento)
        db.session.commit()
    except Exception:
        db.session.rollback()


def _parse_date_range(data_inicial_str, data_final_str, default_days=7):
    return parse_date_range(data_inicial_str, data_final_str, default_days=default_days)


def _normalizar_tipo_negocio(valor):
    tipo_negocio = (valor or EmpresaConfig.TIPO_NEGOCIO_CONVENIENCIA).strip().lower()
    if tipo_negocio not in EmpresaConfig.TIPOS_NEGOCIO_VALIDOS:
        return EmpresaConfig.TIPO_NEGOCIO_CONVENIENCIA
    return tipo_negocio


def _normalizar_canal_operacao(valor):
    canal_operacao = (valor or EmpresaConfig.CANAL_OPERACAO_HIBRIDO).strip().lower()
    if canal_operacao not in EmpresaConfig.CANAIS_OPERACAO_VALIDOS:
        return EmpresaConfig.CANAL_OPERACAO_HIBRIDO
    return canal_operacao


def _normalizar_cor_hex(valor, fallback):
    valor = (valor or '').strip()
    if not valor:
        return fallback
    if len(valor) == 7 and valor.startswith('#'):
        validos = '0123456789abcdefABCDEF'
        if all(c in validos for c in valor[1:]):
            return valor.lower()
    return fallback


def _carregar_json_lista(valor_json):
    if not valor_json:
        return []
    try:
        dados = json.loads(valor_json)
        if isinstance(dados, list):
            return dados
    except Exception:
        pass
    return []


def _parse_datetime_local(valor):
    valor = (valor or '').strip()
    if not valor:
        return None
    try:
        return datetime.strptime(valor, '%Y-%m-%dT%H:%M')
    except ValueError:
        return None


def _parse_date_iso(valor):
    valor = (valor or '').strip()
    if not valor:
        return None
    try:
        return datetime.strptime(valor, '%Y-%m-%d').date()
    except ValueError:
        return None


def _periodo_datetime_ativo(inicio, fim, agora=None):
    agora = agora or datetime.utcnow()
    if inicio and agora < inicio:
        return False
    if fim and agora > fim:
        return False
    return True


def _periodo_data_ativo(inicio, fim, hoje=None):
    hoje = hoje or datetime.utcnow().date()
    if inicio and hoje < inicio:
        return False
    if fim and hoje > fim:
        return False
    return True


def _aplicar_preset_negocio(empresa):
    if not empresa:
        return
    preset_tipo = TIPO_NEGOCIO_PRESETS.get(empresa.tipo_negocio or EmpresaConfig.TIPO_NEGOCIO_CONVENIENCIA, {})
    preset = preset_tipo.get(empresa.canal_operacao or EmpresaConfig.CANAL_OPERACAO_HIBRIDO, {})
    for chave, valor in preset.items():
        setattr(empresa, chave, valor)


def _coletar_dashboard_analytics(inicio_periodo, fim_periodo):
    cache = extensions.cache
    cache_key = f'dashboard:{inicio_periodo.strftime("%Y%m%d")}:{fim_periodo.strftime("%Y%m%d")}'
    if cache is not None:
        dados = cache.get(cache_key)
        if dados is not None:
            return dados
    dados = calcular_metricas_dashboard(inicio_periodo, fim_periodo)
    if cache is not None:
        cache.set(cache_key, dados, timeout=60)
    return dados


# ============ ROTAS - AUTENTICACAO ============

@app.route('/login', methods=['GET', 'POST'])
@_limit('10 per 5 minute')
def login():
    if request.method == 'POST':
        ip_addr = _client_ip()
        if extensions.limiter is None and _is_login_rate_limited(ip_addr):
            flash('Muitas tentativas de login. Tente novamente em alguns minutos.', 'danger')
            registrar_evento_auditoria(
                funcionario=None,
                acao='login_rate_limited',
                entidade='autenticacao',
                detalhes=f'ip={ip_addr}',
                status_code=429
            )
            return redirect(url_for('login'))

        email = request.form.get('email', '').strip()
        senha = request.form.get('senha', '')

        if not email or not senha:
            flash('Email e senha são obrigatórios.', 'danger')
            return redirect(url_for('login'))

        funcionario = Funcionario.query.filter_by(email=email).first()

        if funcionario and funcionario.check_password(senha):
            if not funcionario.ativo:
                _register_login_attempt(ip_addr, success=False)
                registrar_evento_auditoria(
                    funcionario=funcionario,
                    acao='login_bloqueado_inativo',
                    entidade='autenticacao',
                    detalhes=f'email={email}',
                    status_code=403
                )
                flash('Usuário inativo. Contate um administrador.', 'danger')
                return redirect(url_for('login'))

            session['funcionario_id'] = funcionario.id
            session['funcionario_nome'] = funcionario.nome
            session['funcionario_role'] = funcionario.role
            db.session.commit()
            _register_login_attempt(ip_addr, success=True)
            registrar_evento_auditoria(
                funcionario=funcionario,
                acao='login_sucesso',
                entidade='autenticacao',
                detalhes=f'email={email}',
                status_code=200
            )

            flash(f'Bem-vindo, {funcionario.nome}!', 'success')
            return redirect(url_for('dashboard'))

        _register_login_attempt(ip_addr, success=False)
        registrar_evento_auditoria(
            funcionario=None,
            acao='login_falha',
            entidade='autenticacao',
            detalhes=f'email={email}',
            status_code=401
        )
        flash('Email ou senha incorretos.', 'danger')
        return redirect(url_for('login'))

    return render_template('sistema/login.html')


@app.route('/logout')
def logout():
    funcionario = get_funcionario_logado()
    registrar_evento_auditoria(
        funcionario=funcionario,
        acao='logout',
        entidade='autenticacao',
        detalhes=f'usuario={funcionario.nome if funcionario else "desconhecido"}',
        status_code=200
    )
    nome = session.get('funcionario_nome', 'Usuário')
    session.clear()
    flash(f'Ate logo, {nome}!', 'info')
    return redirect(url_for('login'))


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    total_funcionarios = Funcionario.query.count()

    if request.method == 'POST':
        if total_funcionarios > 0 and 'funcionario_id' not in session:
            flash('Acesso negado. Faca login como administrador.', 'danger')
            return redirect(url_for('login'))

        if total_funcionarios > 0:
            funcionario_logado = get_funcionario_logado()
            if not funcionario_logado or funcionario_logado.role != 'admin':
                flash('Apenas administradores podem registrar novos funcionarios.', 'danger')
                return redirect(url_for('dashboard'))

        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        senha = request.form.get('senha', '')
        confirmacao_senha = request.form.get('confirmacao_senha', '')
        role = _normalizar_texto(request.form.get('role', 'operador'))
        cargo = (request.form.get('cargo') or '').strip()

        if not nome or not email or not senha:
            flash('Nome, email e senha são obrigatórios.', 'danger')
            return redirect(url_for('registro'))

        if senha != confirmacao_senha:
            flash('As senhas não conferem.', 'danger')
            return redirect(url_for('registro'))

        if len(senha) < 6:
            flash('A senha deve ter no minimo 6 caracteres.', 'danger')
            return redirect(url_for('registro'))

        if Funcionario.query.filter_by(email=email).first():
            flash('Email ja cadastrado.', 'danger')
            return redirect(url_for('registro'))

        novo_funcionario = Funcionario(nome=nome, email=email)
        novo_funcionario.set_password(senha)

        if total_funcionarios == 0:
            novo_funcionario.role = 'admin'
            novo_funcionario.cargo = 'Administrador'
        elif role in ROLES_PERMITIDOS:
            novo_funcionario.role = role
            novo_funcionario.cargo = cargo or _role_para_cargo_padrao(role)
        else:
            flash('Perfil de acesso inválido.', 'danger')
            return redirect(url_for('registro'))

        db.session.add(novo_funcionario)
        db.session.flush()
        sincronizar_garcom_funcionario(novo_funcionario)
        db.session.commit()

        if total_funcionarios == 0:
            flash(f'Conta do administrador criada com sucesso! Bem-vindo, {nome}!', 'success')
            session['funcionario_id'] = novo_funcionario.id
            session['funcionario_nome'] = novo_funcionario.nome
            session['funcionario_role'] = novo_funcionario.role
            return redirect(url_for('dashboard'))

        flash(f'Funcionario {nome} registrado com sucesso!', 'success')
        return redirect(url_for('listar_funcionarios'))

    funcoes_rh = FuncaoRH.query.filter_by(ativo=True).order_by(FuncaoRH.nome.asc()).all()
    return render_template(
        'sistema/registro.html',
        primeira_vez=(total_funcionarios == 0),
        funcoes_rh=funcoes_rh
    )


# ============ ROTAS - SISTEMA ============

@app.route('/')
def index():
    empresa = EmpresaConfig.query.first()
    resumo_carrinho = obter_resumo_carrinho_site()
    produtos_disponiveis = Produto.query.filter(
        Produto.ativo.is_(True),
        Produto.status_disponibilidade.in_(Produto.STATUS_DISPONIBILIDADE_ONLINE_EQUIVALENTES)
    )

    produtos_destaque = produtos_disponiveis.order_by(
        Produto.atualizado_em.desc(),
        Produto.criado_em.desc()
    ).limit(12).all()

    if not produtos_destaque:
        produtos_destaque = Produto.query.filter_by(ativo=True).order_by(
            Produto.atualizado_em.desc(),
            Produto.criado_em.desc()
        ).limit(12).all()

    agora = datetime.utcnow()
    hoje = agora.date()
    banners_ativos = []
    for banner in _carregar_json_lista(empresa.ecom_banners_json if empresa else None):
        inicio = _parse_datetime_local(banner.get('inicio_em'))
        fim = _parse_datetime_local(banner.get('fim_em'))
        if not _periodo_datetime_ativo(inicio, fim, agora=agora):
            continue
        if not banner.get('ativo', True):
            continue
        image_path = (banner.get('image_path') or '').strip()
        if not image_path:
            continue
        banners_ativos.append({
            'titulo': (banner.get('titulo') or '').strip(),
            'subtitulo': (banner.get('subtitulo') or '').strip(),
            'image_path': image_path,
        })

    if not banners_ativos and empresa and empresa.ecom_banner_path:
        banners_ativos.append({
            'titulo': empresa.ecom_titulo_banner or 'Destaque da loja',
            'subtitulo': empresa.ecom_subtitulo_banner or '',
            'image_path': empresa.ecom_banner_path,
        })

    campanhas_ativas = []
    for campanha in _carregar_json_lista(empresa.ecom_campanhas_json if empresa else None):
        inicio = _parse_date_iso(campanha.get('inicio_em'))
        fim = _parse_date_iso(campanha.get('fim_em'))
        if not _periodo_data_ativo(inicio, fim, hoje=hoje):
            continue
        if not campanha.get('ativo', True):
            continue
        nome = (campanha.get('nome') or '').strip()
        texto = (campanha.get('texto') or '').strip()
        if not nome and not texto:
            continue
        campanhas_ativas.append({'nome': nome, 'texto': texto})

    campanha_principal = None
    if campanhas_ativas:
        campanha_principal = campanhas_ativas[0].get('texto') or campanhas_ativas[0].get('nome')
    if not campanha_principal and empresa:
        campanha_principal = empresa.ecom_texto_promocao

    return render_template(
        'public/home_varejo.html',
        app_name=APP_NAME,
        produtos_destaque=produtos_destaque,
        carrinho_site=resumo_carrinho,
        total_produtos_ativos=Produto.query.filter_by(ativo=True).count(),
        banners_ativos=banners_ativos,
        campanhas_ativas=campanhas_ativas,
        campanha_principal=campanha_principal,
    )


@app.route('/dashboard')
@login_required
def dashboard():
    inicio_periodo, fim_periodo, data_inicial_str, data_final_str = _parse_date_range(
        request.args.get('data_inicial'),
        request.args.get('data_final'),
        default_days=7
    )
    analytics = _coletar_dashboard_analytics(inicio_periodo, fim_periodo)

    return render_template(
        'dashboard/index.html',
        periodo_dias=analytics['periodo_dias'],
        data_inicial=data_inicial_str,
        data_final=data_final_str,
        pedidos_periodo_total=analytics['pedidos_periodo_total'],
        faturamento_periodo=analytics['faturamento_periodo'],
        faturamento_hoje=analytics['faturamento_hoje'],
        ticket_medio_periodo=analytics['ticket_medio_periodo'],
        pedidos_abertos=analytics['pedidos_abertos'],
        pedidos_cancelados_periodo=analytics['pedidos_cancelados_periodo'],
        vendas_periodo=analytics['vendas_periodo'],
        top_produtos_vendidos=analytics['top_produtos_vendidos'],
        pedidos_por_status=analytics['pedidos_por_status'],
        top_clientes=analytics['top_clientes'],
        desempenho_garcons=analytics['desempenho_garcons'],
        desempenho_caixas=analytics['desempenho_caixas'],
        metodos_pagamento=analytics['metodos_pagamento']
    )


@app.route('/api/dashboard/analytics')
@login_required
def dashboard_analytics_api():
    inicio_periodo, fim_periodo, data_inicial_str, data_final_str = _parse_date_range(
        request.args.get('data_inicial'),
        request.args.get('data_final'),
        default_days=7
    )
    analytics = _coletar_dashboard_analytics(inicio_periodo, fim_periodo)
    return jsonify({
        'success': True,
        'message': 'Analytics carregado com sucesso.',
        'data': {
            'data_inicial': data_inicial_str,
            'data_final': data_final_str,
            **analytics
        }
    })


@app.route('/api/docs')
@login_required
def api_docs():
    return render_template('api/docs.html')


@app.route('/empresa', methods=['GET', 'POST'])
@require_role('admin', 'gerente')
def editar_empresa():
    empresa = EmpresaConfig.query.first()

    if request.method == 'POST':
        novo_logo_path = None
        logo_anterior = (empresa.logo_path if empresa else None)
        try:
            if not empresa:
                empresa = EmpresaConfig()
                db.session.add(empresa)

            empresa.razao_social = request.form.get('razao_social', '').strip() or None
            empresa.nome_fantasia = request.form.get('nome_fantasia', '').strip() or None
            empresa.cnpj = request.form.get('cnpj', '').strip() or None
            empresa.inscricao_estadual = request.form.get('inscricao_estadual', '').strip() or None
            empresa.telefone = request.form.get('telefone', '').strip() or None
            empresa.email = request.form.get('email', '').strip() or None
            empresa.endereco = request.form.get('endereco', '').strip() or None
            empresa.cidade = request.form.get('cidade', '').strip() or None
            empresa.estado = request.form.get('estado', '').strip().upper() or None
            empresa.cep = request.form.get('cep', '').strip() or None
            empresa.mensagem_comprovante = request.form.get('mensagem_comprovante', '').strip() or None
            empresa.cardapio_titulo = request.form.get('cardapio_titulo', '').strip() or None
            empresa.cardapio_subtitulo = request.form.get('cardapio_subtitulo', '').strip() or None
            empresa.cardapio_mensagem = request.form.get('cardapio_mensagem', '').strip() or None
            empresa.cardapio_mostrar_imagem = (request.form.get('cardapio_mostrar_imagem') == 'on')
            empresa.cardapio_mostrar_descricao = (request.form.get('cardapio_mostrar_descricao') == 'on')
            empresa.tipo_negocio = _normalizar_tipo_negocio(request.form.get('tipo_negocio'))
            empresa.canal_operacao = _normalizar_canal_operacao(request.form.get('canal_operacao'))
            empresa.ecommerce_ativo = (request.form.get('ecommerce_ativo') == 'on')
            empresa.atendimento_mesas_ativo = (request.form.get('atendimento_mesas_ativo') == 'on')
            empresa.separacao_entrega_ativa = (request.form.get('separacao_entrega_ativa') == 'on')
            empresa.emissao_etiqueta_entrega_ativa = (request.form.get('emissao_etiqueta_entrega_ativa') == 'on')
            empresa.separacao_entrega_unir_vendas_off = (request.form.get('separacao_entrega_unir_vendas_off') == 'on')
            if request.form.get('aplicar_preset_operacao') == 'on':
                _aplicar_preset_negocio(empresa)

            remover_logo = (request.form.get('remover_logo') == 'on')
            arquivo_logo = request.files.get('logo')
            allowed_ext = {'.png', '.jpg', '.jpeg', '.webp', '.gif'}
            if arquivo_logo and arquivo_logo.filename:
                _, ext = os.path.splitext(arquivo_logo.filename.lower())
                if ext not in allowed_ext:
                    flash('Formato de logo inválido. Use PNG, JPG, JPEG, WEBP ou GIF.', 'error')
                    return redirect(url_for('editar_empresa'))
                nome_empresa_base = secure_filename((empresa.nome_fantasia or empresa.razao_social or 'empresa').strip())
                if not nome_empresa_base:
                    nome_empresa_base = 'empresa'
                relative_dir = os.path.join('uploads', 'empresa')
                absolute_dir = os.path.join(app.static_folder, relative_dir)
                os.makedirs(absolute_dir, exist_ok=True)
                image_name = f'{nome_empresa_base}_logo{ext}'
                novo_logo_path = os.path.join(relative_dir, image_name).replace('\\', '/')
                absolute_path = os.path.join(app.static_folder, novo_logo_path)
                arquivo_logo.save(absolute_path)
                empresa.logo_path = novo_logo_path
            elif remover_logo:
                empresa.logo_path = None

            qtd_maxima = request.form.get('cardapio_qtd_maxima', type=int)
            if qtd_maxima is None or qtd_maxima <= 0:
                qtd_maxima = 20
            empresa.cardapio_qtd_maxima = qtd_maxima
            if 'distribuicao_ativa' in request.form or 'modo_distribuicao_pedidos' in request.form:
                empresa.distribuicao_ativa = (request.form.get('distribuicao_ativa') == 'on')
                modo_distribuicao = (request.form.get('modo_distribuicao_pedidos') or 'round_robin').strip().lower()
                if modo_distribuicao not in {'round_robin', 'menos_pedidos', 'manual'}:
                    modo_distribuicao = 'round_robin'
                empresa.modo_distribuicao_pedidos = modo_distribuicao

            db.session.commit()
            if novo_logo_path and logo_anterior and logo_anterior != novo_logo_path:
                caminho_logo_anterior = os.path.join(app.static_folder, logo_anterior)
                if os.path.exists(caminho_logo_anterior):
                    os.remove(caminho_logo_anterior)
            if remover_logo and logo_anterior:
                caminho_logo_anterior = os.path.join(app.static_folder, logo_anterior)
                if os.path.exists(caminho_logo_anterior):
                    os.remove(caminho_logo_anterior)
            flash('Dados da empresa salvos com sucesso.', 'success')
            return redirect(url_for('editar_empresa'))
        except Exception as e:
            db.session.rollback()
            if novo_logo_path:
                caminho_novo_logo = os.path.join(app.static_folder, novo_logo_path)
                if os.path.exists(caminho_novo_logo):
                    os.remove(caminho_novo_logo)
            flash(f'Erro ao salvar dados da empresa: {str(e)}', 'error')

    tipos_negocio = [
        (EmpresaConfig.TIPO_NEGOCIO_CONVENIENCIA, 'Loja de conveniência'),
        (EmpresaConfig.TIPO_NEGOCIO_SUPERMERCADO, 'Supermercado/mercearia'),
        (EmpresaConfig.TIPO_NEGOCIO_FARMACIA, 'Farmacia/perfumaria'),
        (EmpresaConfig.TIPO_NEGOCIO_MODA, 'Moda/acessorios'),
        (EmpresaConfig.TIPO_NEGOCIO_HOME_CENTER, 'Casa/construcao'),
        (EmpresaConfig.TIPO_NEGOCIO_OUTRO, 'Outro varejo'),
    ]
    canais_operacao = [
        (EmpresaConfig.CANAL_OPERACAO_FISICO, 'Somente loja física'),
        (EmpresaConfig.CANAL_OPERACAO_ECOMMERCE, 'Somente e-commerce'),
        (EmpresaConfig.CANAL_OPERACAO_HIBRIDO, 'Hibrido (fisico + e-commerce)'),
    ]
    return render_template(
        'sistema/empresa.html',
        empresa=empresa,
        tipos_negocio=tipos_negocio,
        canais_operacao=canais_operacao
    )


@app.route('/ecommerce-config', methods=['GET', 'POST'])
@require_role('admin', 'gerente')
def configurar_ecommerce():
    empresa = EmpresaConfig.query.first()
    if not empresa:
        empresa = EmpresaConfig()
        db.session.add(empresa)
        db.session.commit()

    def _montar_slots_banners():
        slots = []
        origem = _carregar_json_lista(empresa.ecom_banners_json)
        for i in range(5):
            item = origem[i] if i < len(origem) and isinstance(origem[i], dict) else {}
            slots.append({
                'titulo': item.get('titulo') or '',
                'subtitulo': item.get('subtitulo') or '',
                'inicio_em': item.get('inicio_em') or '',
                'fim_em': item.get('fim_em') or '',
                'image_path': item.get('image_path') or '',
                'ativo': bool(item.get('ativo', False)),
            })
        return slots

    def _montar_slots_campanhas():
        slots = []
        origem = _carregar_json_lista(empresa.ecom_campanhas_json)
        for i in range(5):
            item = origem[i] if i < len(origem) and isinstance(origem[i], dict) else {}
            slots.append({
                'nome': item.get('nome') or '',
                'texto': item.get('texto') or '',
                'inicio_em': item.get('inicio_em') or '',
                'fim_em': item.get('fim_em') or '',
                'ativo': bool(item.get('ativo', False)),
            })
        return slots

    if request.method == 'POST':
        novo_banner_path = None
        novo_favicon_path = None
        novo_produto_placeholder_path = None
        banner_anterior = empresa.ecom_banner_path
        favicon_anterior = empresa.ecom_favicon_path
        produto_placeholder_anterior = empresa.ecom_produto_placeholder_path
        novos_arquivos = []
        arquivos_para_remover = []
        try:
            empresa.ecom_cor_primaria = _normalizar_cor_hex(
                request.form.get('ecom_cor_primaria'),
                empresa.ecom_cor_primaria or '#ff7848'
            )
            empresa.ecom_cor_secundaria = _normalizar_cor_hex(
                request.form.get('ecom_cor_secundaria'),
                empresa.ecom_cor_secundaria or '#ff5a2a'
            )
            empresa.ecom_titulo_banner = request.form.get('ecom_titulo_banner', '').strip() or None
            empresa.ecom_subtitulo_banner = request.form.get('ecom_subtitulo_banner', '').strip() or None
            empresa.ecom_texto_promocao = request.form.get('ecom_texto_promocao', '').strip() or None
            empresa.ecom_footer_bg = _normalizar_cor_hex(
                request.form.get('ecom_footer_bg'),
                empresa.ecom_footer_bg or '#1f2b38'
            )
            empresa.ecom_footer_texto = request.form.get('ecom_footer_texto', '').strip() or None
            empresa.ecom_footer_contato = request.form.get('ecom_footer_contato', '').strip() or None
            empresa.ecom_footer_creditos = request.form.get('ecom_footer_creditos', '').strip() or None

            remover_banner = (request.form.get('remover_ecom_banner') == 'on')
            remover_favicon = (request.form.get('remover_ecom_favicon') == 'on')
            remover_produto_placeholder = (request.form.get('remover_ecom_produto_placeholder') == 'on')
            arquivo_banner = request.files.get('ecom_banner')
            arquivo_favicon = request.files.get('ecom_favicon')
            arquivo_produto_placeholder = request.files.get('ecom_produto_placeholder')
            allowed_ext = {'.png', '.jpg', '.jpeg', '.webp', '.gif'}
            allowed_favicon_ext = {'.ico', '.png', '.svg', '.jpg', '.jpeg', '.webp'}
            nome_empresa_base = secure_filename((empresa.nome_fantasia or empresa.razao_social or 'empresa').strip())
            if not nome_empresa_base:
                nome_empresa_base = 'empresa'
            relative_dir = os.path.join('uploads', 'ecommerce')
            absolute_dir = os.path.join(app.static_folder, relative_dir)
            os.makedirs(absolute_dir, exist_ok=True)
            if arquivo_banner and arquivo_banner.filename:
                _, ext = os.path.splitext(arquivo_banner.filename.lower())
                if ext not in allowed_ext:
                    flash('Formato de banner inválido. Use PNG, JPG, JPEG, WEBP ou GIF.', 'error')
                    return redirect(url_for('configurar_ecommerce'))
                image_name = f'{nome_empresa_base}_banner{ext}'
                novo_banner_path = os.path.join(relative_dir, image_name).replace('\\', '/')
                absolute_path = os.path.join(app.static_folder, novo_banner_path)
                arquivo_banner.save(absolute_path)
                novos_arquivos.append(novo_banner_path)
                empresa.ecom_banner_path = novo_banner_path
            elif remover_banner:
                empresa.ecom_banner_path = None

            if arquivo_favicon and arquivo_favicon.filename:
                _, ext = os.path.splitext(arquivo_favicon.filename.lower())
                if ext not in allowed_favicon_ext:
                    flash('Formato de favicon inválido. Use ICO, PNG, SVG, JPG, JPEG ou WEBP.', 'error')
                    return redirect(url_for('configurar_ecommerce'))
                image_name = f'{nome_empresa_base}_favicon{ext}'
                novo_favicon_path = os.path.join(relative_dir, image_name).replace('\\', '/')
                absolute_path = os.path.join(app.static_folder, novo_favicon_path)
                arquivo_favicon.save(absolute_path)
                novos_arquivos.append(novo_favicon_path)
                empresa.ecom_favicon_path = novo_favicon_path
            elif remover_favicon:
                empresa.ecom_favicon_path = None

            if arquivo_produto_placeholder and arquivo_produto_placeholder.filename:
                _, ext = os.path.splitext(arquivo_produto_placeholder.filename.lower())
                if ext not in allowed_ext:
                    flash('Formato da imagem padrão inválido. Use PNG, JPG, JPEG, WEBP ou GIF.', 'error')
                    return redirect(url_for('configurar_ecommerce'))
                image_name = f'{nome_empresa_base}_produto_padrao{ext}'
                novo_produto_placeholder_path = os.path.join(relative_dir, image_name).replace('\\', '/')
                absolute_path = os.path.join(app.static_folder, novo_produto_placeholder_path)
                arquivo_produto_placeholder.save(absolute_path)
                novos_arquivos.append(novo_produto_placeholder_path)
                empresa.ecom_produto_placeholder_path = novo_produto_placeholder_path
            elif remover_produto_placeholder:
                empresa.ecom_produto_placeholder_path = None

            banners_slots = []
            for idx in range(5):
                titulo = (request.form.get(f'banner_titulo_{idx}') or '').strip()
                subtitulo = (request.form.get(f'banner_subtitulo_{idx}') or '').strip()
                inicio_em = (request.form.get(f'banner_inicio_{idx}') or '').strip()
                fim_em = (request.form.get(f'banner_fim_{idx}') or '').strip()
                image_path_atual = (request.form.get(f'banner_path_{idx}') or '').strip() or None
                ativo = (request.form.get(f'banner_ativo_{idx}') == 'on')
                remover_slot = (request.form.get(f'remover_banner_{idx}') == 'on')
                arquivo_slot = request.files.get(f'banner_imagem_{idx}')
                image_path_slot = image_path_atual

                if arquivo_slot and arquivo_slot.filename:
                    _, ext = os.path.splitext(arquivo_slot.filename.lower())
                    if ext not in allowed_ext:
                        flash(f'Formato de imagem inválido no banner {idx + 1}.', 'error')
                        return redirect(url_for('configurar_ecommerce'))
                    nome_slot = f'{nome_empresa_base}_carrossel_{idx}_{int(datetime.utcnow().timestamp())}{ext}'
                    novo_slot_path = os.path.join(relative_dir, nome_slot).replace('\\', '/')
                    caminho_slot = os.path.join(app.static_folder, novo_slot_path)
                    arquivo_slot.save(caminho_slot)
                    novos_arquivos.append(novo_slot_path)
                    image_path_slot = novo_slot_path
                    if image_path_atual and image_path_atual != novo_slot_path:
                        arquivos_para_remover.append(image_path_atual)
                elif remover_slot:
                    if image_path_atual:
                        arquivos_para_remover.append(image_path_atual)
                    image_path_slot = None

                inicio_dt = _parse_datetime_local(inicio_em)
                fim_dt = _parse_datetime_local(fim_em)
                if fim_dt and inicio_dt and fim_dt < inicio_dt:
                    flash(f'Banner {idx + 1}: o fim da vigência não pode ser menor que o início.', 'error')
                    return redirect(url_for('configurar_ecommerce'))

                if not any([titulo, subtitulo, image_path_slot, inicio_em, fim_em]):
                    continue

                banners_slots.append({
                    'titulo': titulo,
                    'subtitulo': subtitulo,
                    'inicio_em': inicio_em,
                    'fim_em': fim_em,
                    'image_path': image_path_slot,
                    'ativo': ativo,
                })

            campanhas_slots = []
            for idx in range(5):
                nome = (request.form.get(f'campanha_nome_{idx}') or '').strip()
                texto = (request.form.get(f'campanha_texto_{idx}') or '').strip()
                inicio_em = (request.form.get(f'campanha_inicio_{idx}') or '').strip()
                fim_em = (request.form.get(f'campanha_fim_{idx}') or '').strip()
                ativo = (request.form.get(f'campanha_ativa_{idx}') == 'on')

                if not any([nome, texto, inicio_em, fim_em]):
                    continue

                inicio_data = _parse_date_iso(inicio_em)
                fim_data = _parse_date_iso(fim_em)
                if fim_data and inicio_data and fim_data < inicio_data:
                    flash(f'Campanha {idx + 1}: o fim da vigência não pode ser menor que o início.', 'error')
                    return redirect(url_for('configurar_ecommerce'))

                campanhas_slots.append({
                    'nome': nome,
                    'texto': texto,
                    'inicio_em': inicio_em,
                    'fim_em': fim_em,
                    'ativo': ativo,
                })

            empresa.ecom_banners_json = json.dumps(banners_slots, ensure_ascii=False)
            empresa.ecom_campanhas_json = json.dumps(campanhas_slots, ensure_ascii=False)

            placeholder_alvos = [None, '', 'img/placeholders/produto-sem-foto.svg']
            if produto_placeholder_anterior:
                placeholder_alvos.append(produto_placeholder_anterior)
            placeholder_alvos = list({item for item in placeholder_alvos})

            if novo_produto_placeholder_path:
                Produto.query.filter(
                    db.or_(
                        Produto.imagem_path.is_(None),
                        Produto.imagem_path == '',
                        Produto.imagem_path.in_(placeholder_alvos),
                    )
                ).update(
                    {Produto.imagem_path: novo_produto_placeholder_path},
                    synchronize_session=False
                )
            elif remover_produto_placeholder and produto_placeholder_anterior:
                Produto.query.filter(
                    db.or_(
                        Produto.imagem_path.is_(None),
                        Produto.imagem_path == '',
                        Produto.imagem_path == produto_placeholder_anterior,
                    )
                ).update(
                    {Produto.imagem_path: 'img/placeholders/produto-sem-foto.svg'},
                    synchronize_session=False
                )

            db.session.commit()
            if novo_banner_path and banner_anterior and banner_anterior != novo_banner_path:
                caminho_banner_anterior = os.path.join(app.static_folder, banner_anterior)
                if os.path.exists(caminho_banner_anterior):
                    os.remove(caminho_banner_anterior)
            if remover_banner and banner_anterior:
                caminho_banner_anterior = os.path.join(app.static_folder, banner_anterior)
                if os.path.exists(caminho_banner_anterior):
                    os.remove(caminho_banner_anterior)
            if novo_favicon_path and favicon_anterior and favicon_anterior != novo_favicon_path:
                caminho_favicon_anterior = os.path.join(app.static_folder, favicon_anterior)
                if os.path.exists(caminho_favicon_anterior):
                    os.remove(caminho_favicon_anterior)
            if remover_favicon and favicon_anterior:
                caminho_favicon_anterior = os.path.join(app.static_folder, favicon_anterior)
                if os.path.exists(caminho_favicon_anterior):
                    os.remove(caminho_favicon_anterior)
            if novo_produto_placeholder_path and produto_placeholder_anterior and produto_placeholder_anterior != novo_produto_placeholder_path:
                caminho_placeholder_anterior = os.path.join(app.static_folder, produto_placeholder_anterior)
                if os.path.exists(caminho_placeholder_anterior):
                    os.remove(caminho_placeholder_anterior)
            if remover_produto_placeholder and produto_placeholder_anterior:
                caminho_placeholder_anterior = os.path.join(app.static_folder, produto_placeholder_anterior)
                if os.path.exists(caminho_placeholder_anterior):
                    os.remove(caminho_placeholder_anterior)
            for caminho_rel in arquivos_para_remover:
                caminho_abs = os.path.join(app.static_folder, caminho_rel)
                if os.path.exists(caminho_abs):
                    os.remove(caminho_abs)
            flash('Configurações de e-commerce salvas com sucesso.', 'success')
            return redirect(url_for('configurar_ecommerce'))
        except Exception as e:
            db.session.rollback()
            for caminho_rel in novos_arquivos:
                caminho_abs = os.path.join(app.static_folder, caminho_rel)
                if os.path.exists(caminho_abs):
                    os.remove(caminho_abs)
            flash(f'Erro ao salvar configurações de e-commerce: {str(e)}', 'error')

    return render_template(
        'sistema/ecommerce_config.html',
        empresa=empresa,
        banners_config=_montar_slots_banners(),
        campanhas_config=_montar_slots_campanhas(),
    )


@app.route('/empresa/config-cardapio/preview')
@require_role('admin', 'gerente')
def preview_cardapio_empresa():
    empresa = EmpresaConfig.query.first()
    if empresa and empresa.atendimento_mesas_ativo is False:
        flash('Atendimento por mesas e garcons esta desativado na empresa.', 'warning')
        return redirect(url_for('editar_empresa'))
    qtd_max = (empresa.cardapio_qtd_maxima if empresa and empresa.cardapio_qtd_maxima else 20)
    if qtd_max <= 0:
        qtd_max = 20

    categorias = Categoria.query.order_by(Categoria.nome.asc()).all()
    categorias_cardapio = []
    for categoria in categorias:
        produtos = Produto.query.filter_by(categoria_id=categoria.id, ativo=True).order_by(Produto.nome.asc()).all()
        if not produtos:
            continue
        categorias_cardapio.append({
            'categoria': categoria,
            'produtos': produtos
        })

    class MesaPreview:
        numero = 'Preview'

    return render_template(
        'public/cardapio.html',
        mesa=MesaPreview(),
        empresa=empresa,
        qtd_max=qtd_max,
        cliente_nome='Cliente Exemplo',
        cliente_celular='(00) 00000-0000',
        cliente_slug='preview',
        categorias_cardapio=categorias_cardapio,
        pedidos_cliente=[],
        preview_mode=True
    )


@app.route('/boas-vindas')
@login_required
def boas_vindas():
    return render_template(
        'sistema/boas_vindas.html',
        app_name=APP_NAME,
        app_version=APP_VERSION,
        app_domain=APP_DOMAIN,
        total_produtos=Produto.query.count(),
        total_categorias=Categoria.query.count()
    )


AJUDA_TOPICOS = {
    'primeiros-passos': {
        'slug': 'primeiros-passos',
        'titulo': 'Primeiros passos no sistema',
        'resumo': 'Configura o ambiente inicial para operar com seguranca e consistencia.',
        'passos': [
            'Acesse Meu RH > Funcionarios e valide os perfis de acesso.',
            'Cadastre os dados da empresa em Meu RH > Empresa.',
            'Defina o tipo de negocio e o canal de operacao.',
            'Crie ao menos uma categoria e alguns produtos para teste.',
            'Abra um caixa e valide o fluxo completo no PDV.',
        ],
    },
    'estoque-operacao': {
        'slug': 'estoque-operacao',
        'titulo': 'Operacao de estoque',
        'resumo': 'Passo a passo para cadastro, entrada, saida e acompanhamento de estoque.',
        'passos': [
            'Cadastre fornecedores com os dados principais.',
            'Crie categorias e depois cadastre os produtos.',
            'Informe preco de custo, preco de venda e estoque minimo.',
            'Registre entradas, saidas e recebimentos por fornecedor.',
            'Acompanhe relatorios para ruptura, giro e valor em estoque.',
        ],
    },
    'vendas-pdv': {
        'slug': 'vendas-pdv',
        'titulo': 'Vendas e PDV',
        'resumo': 'Fluxo recomendado para abertura de caixa, venda e fechamento do turno.',
        'passos': [
            'Abra o caixa com o valor inicial do turno.',
            'Lance os pedidos no PDV e confirme os itens.',
            'Selecione o metodo de pagamento e finalize a venda.',
            'Acompanhe os pedidos na tela de pedidos e status.',
            'Feche o caixa ao final do expediente e confira o historico.',
        ],
    },
    'rh-seguranca': {
        'slug': 'rh-seguranca',
        'titulo': 'RH e seguranca de acesso',
        'resumo': 'Define cargos, permissoes e auditoria para controle operacional.',
        'passos': [
            'Crie funcoes/perfis com permissoes por pagina.',
            'Associe cada colaborador ao cargo correto.',
            'Ative o controle de acesso quando terminar a configuracao.',
            'Revise os acessos por funcionario periodicamente.',
            'Use a auditoria para rastrear alteracoes e acoes sensiveis.',
        ],
    },
    'ecommerce-config': {
        'slug': 'ecommerce-config',
        'titulo': 'Configuracao do e-commerce',
        'resumo': 'Personaliza vitrine, banners, campanhas e elementos visuais da loja.',
        'passos': [
            'Acesse E-commerce > Tema, Banner e Promocoes.',
            'Defina cores da vitrine e mensagem principal.',
            'Configure multiplos banners com periodo de vigencia.',
            'Cadastre campanhas programadas com inicio e fim.',
            'Ajuste rodape, favicon e imagem padrao de produto.',
        ],
    },
}


@app.route('/ajuda')
@login_required
def central_ajuda():
    return render_template(
        'sistema/ajuda.html',
        topicos_ajuda=list(AJUDA_TOPICOS.values()),
    )


@app.route('/ajuda/<string:topico_slug>')
@login_required
def detalhe_ajuda(topico_slug):
    topico = AJUDA_TOPICOS.get(topico_slug)
    if not topico:
        flash('Topico de ajuda nao encontrado.', 'warning')
        return redirect(url_for('central_ajuda'))

    relacionados = [t for slug, t in AJUDA_TOPICOS.items() if slug != topico_slug]
    return render_template(
        'sistema/ajuda_detalhe.html',
        topico=topico,
        topicos_relacionados=relacionados,
    )


# ============ ROTAS - FUNCIONARIOS ============

@app.route('/funcionarios')
@require_role('admin', 'gerente')
def listar_funcionarios():
    funcionarios = Funcionario.query.all()
    return render_template('funcionarios/listar.html', funcionarios=funcionarios)


@app.route('/funcionarios/novo', methods=['GET', 'POST'])
@require_role('admin')
def criar_funcionario():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        senha = request.form.get('senha', '')
        confirmacao_senha = request.form.get('confirmacao_senha', '')
        role = _normalizar_texto(request.form.get('role', 'operador'))
        cargo = (request.form.get('cargo') or '').strip()

        if not nome or not email or not senha:
            flash('Nome, email e senha são obrigatórios.', 'danger')
            return redirect(url_for('criar_funcionario'))

        if senha != confirmacao_senha:
            flash('As senhas não conferem.', 'danger')
            return redirect(url_for('criar_funcionario'))

        if len(senha) < 6:
            flash('A senha deve ter no minimo 6 caracteres.', 'danger')
            return redirect(url_for('criar_funcionario'))

        if Funcionario.query.filter_by(email=email).first():
            flash('Email ja cadastrado.', 'danger')
            return redirect(url_for('criar_funcionario'))

        if role not in ROLES_PERMITIDOS:
            flash('Perfil de acesso inválido.', 'danger')
            return redirect(url_for('criar_funcionario'))

        novo_funcionario = Funcionario(
            nome=nome,
            email=email,
            role=role,
            cargo=cargo or _role_para_cargo_padrao(role),
        )
        novo_funcionario.set_password(senha)
        db.session.add(novo_funcionario)
        db.session.flush()
        sincronizar_garcom_funcionario(novo_funcionario)
        db.session.commit()

        flash(f'Funcionario {nome} criado com sucesso!', 'success')
        return redirect(url_for('listar_funcionarios'))

    funcoes_rh = FuncaoRH.query.filter_by(ativo=True).order_by(FuncaoRH.nome.asc()).all()
    return render_template('funcionarios/criar.html', funcoes_rh=funcoes_rh)


@app.route('/funcionarios/<int:funcionario_id>/editar', methods=['GET', 'POST'])
@require_role('admin', 'gerente')
def editar_funcionario(funcionario_id):
    funcionario = Funcionario.query.get_or_404(funcionario_id)

    funcionario_logado = get_funcionario_logado()
    if funcionario_logado.role == 'gerente' and funcionario.role in ['admin', 'gerente'] and funcionario.id != funcionario_logado.id:
        flash('Você não tem permissão para editar este funcionário.', 'danger')
        return redirect(url_for('listar_funcionarios'))

    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        role = _normalizar_texto(request.form.get('role', funcionario.role))
        cargo = (request.form.get('cargo') or '').strip()
        ativo = request.form.get('ativo') == 'on'
        nova_senha = request.form.get('nova_senha', '')

        if not nome or not email:
            flash('Nome e email são obrigatórios.', 'danger')
            return redirect(url_for('editar_funcionario', funcionario_id=funcionario_id))

        outro_func = Funcionario.query.filter_by(email=email).first()
        if outro_func and outro_func.id != funcionario.id:
            flash('Email ja cadastrado por outro funcionario.', 'danger')
            return redirect(url_for('editar_funcionario', funcionario_id=funcionario_id))

        funcionario.nome = nome
        funcionario.email = email
        funcionario.cargo = cargo or funcionario.cargo or _role_para_cargo_padrao(funcionario.role)
        funcionario.ativo = ativo

        if funcionario_logado.role == 'admin':
            if role not in ROLES_PERMITIDOS:
                flash('Perfil de acesso inválido.', 'danger')
                return redirect(url_for('editar_funcionario', funcionario_id=funcionario_id))
            funcionario.role = role

        if nova_senha:
            if len(nova_senha) < 6:
                flash('A nova senha deve ter no minimo 6 caracteres.', 'danger')
                return redirect(url_for('editar_funcionario', funcionario_id=funcionario_id))
            funcionario.set_password(nova_senha)

        sincronizar_garcom_funcionario(funcionario)
        db.session.commit()
        flash('Funcionario atualizado com sucesso!', 'success')
        return redirect(url_for('listar_funcionarios'))

    funcoes_rh = FuncaoRH.query.filter_by(ativo=True).order_by(FuncaoRH.nome.asc()).all()
    return render_template(
        'funcionarios/editar.html',
        funcionario=funcionario,
        funcoes_rh=funcoes_rh,
        funcoes_rh_nomes=[f.nome for f in funcoes_rh]
    )


@app.route('/funcionarios/<int:funcionario_id>/deletar', methods=['POST'])
@require_role('admin')
def deletar_funcionario(funcionario_id):
    if funcionario_id == session.get('funcionario_id'):
        flash('Você não pode deletar sua própria conta.', 'danger')
        return redirect(url_for('listar_funcionarios'))

    funcionario = Funcionario.query.get_or_404(funcionario_id)
    try:
        db.session.delete(funcionario)
        db.session.commit()
        flash(f'Funcionario {funcionario.nome} deletado com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao deletar funcionario: {str(e)}', 'danger')

    return redirect(url_for('listar_funcionarios'))


@app.route('/funcionarios/<int:funcionario_id>/acessos', methods=['GET', 'POST'])
@require_role('admin')
def editar_acessos_funcionario(funcionario_id):
    funcionario = Funcionario.query.get_or_404(funcionario_id)
    
    if request.method == 'POST':
        paginas_enviadas = set(request.form.getlist('paginas'))
        paginas_validas = set(PAGINAS_SISTEMA.keys())
        paginas_salvas = paginas_enviadas.intersection(paginas_validas)

        try:
            PermissaoAcesso.query.filter_by(funcionario_id=funcionario.id).delete()
            for pagina in paginas_salvas:
                db.session.add(PermissaoAcesso(funcionario_id=funcionario.id, pagina=pagina))
            funcionario.controle_acesso_ativo = True
            db.session.commit()
            flash(f'Acessos de {funcionario.nome} atualizados com sucesso.', 'success')
            return redirect(url_for('listar_funcionarios'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao salvar acessos: {str(e)}', 'danger')
    
    # Obter permissões atuais do funcionário
    permissoes_atuais = {p.pagina for p in PermissaoAcesso.query.filter_by(funcionario_id=funcionario.id).all()}
    paginas_ordenadas_menu = []
    for secao_nome, secao_paginas in PAGINAS_SISTEMA_MENU_ORDEM:
        itens_secao = [
            (pagina_key, PAGINAS_SISTEMA[pagina_key])
            for pagina_key in secao_paginas
            if pagina_key in PAGINAS_SISTEMA
        ]
        if itens_secao:
            paginas_ordenadas_menu.append((secao_nome, itens_secao))
    
    return render_template(
        'funcionarios/acessos.html',
        funcionario=funcionario,
        paginas_sistema=PAGINAS_SISTEMA,
        paginas_ordenadas_menu=paginas_ordenadas_menu,
        permissoes_atuais=permissoes_atuais
    )


@app.route('/rh/funcoes')
@require_role('admin', 'gerente')
def listar_funcoes_rh():
    funcoes = FuncaoRH.query.order_by(FuncaoRH.nome.asc()).all()
    return render_template('rh/funcoes.html', funcoes=funcoes)


@app.route('/rh/perfis')
@require_role('admin', 'gerente')
def listar_perfis_rh():
    funcoes = FuncaoRH.query.order_by(FuncaoRH.nome.asc()).all()
    funcoes_permissoes = []
    for f in funcoes:
        permissoes = []
        try:
            if f.permissoes_padrao:
                permissoes = json.loads(f.permissoes_padrao)
        except Exception:
            permissoes = []
        funcoes_permissoes.append((f, set(permissoes)))

    paginas_ordenadas_menu = []
    for secao_nome, secao_paginas in PAGINAS_SISTEMA_MENU_ORDEM:
        itens_secao = [
            (pagina_key, PAGINAS_SISTEMA[pagina_key])
            for pagina_key in secao_paginas
            if pagina_key in PAGINAS_SISTEMA
        ]
        if itens_secao:
            paginas_ordenadas_menu.append((secao_nome, itens_secao))

    return render_template(
        'rh/perfis.html',
        funcoes=funcoes,
        funcoes_permissoes=funcoes_permissoes,
        paginas_ordenadas_menu=paginas_ordenadas_menu,
        paginas_sistema=PAGINAS_SISTEMA,
    )


@app.route('/rh/indicadores')
@require_role('admin', 'gerente')
def indicadores_rh():
    total_funcionarios = Funcionario.query.count()
    funcionarios_ativos = Funcionario.query.filter_by(ativo=True).count()
    funcionarios_inativos = Funcionario.query.filter_by(ativo=False).count()
    acessos_controlados = Funcionario.query.filter_by(controle_acesso_ativo=True).count()

    funcoes_total = FuncaoRH.query.count()
    funcoes_ativas = FuncaoRH.query.filter_by(ativo=True).count()

    data_limite = datetime.utcnow() - timedelta(days=30)
    admissoes_30_dias = Funcionario.query.filter(Funcionario.criado_em >= data_limite).count()

    distribuicao_roles = db.session.query(
        Funcionario.role.label('role'),
        db.func.count(Funcionario.id).label('quantidade')
    ).group_by(Funcionario.role).order_by(db.desc('quantidade')).all()

    funcionarios_recentes = Funcionario.query.order_by(Funcionario.criado_em.desc()).limit(10).all()

    return render_template(
        'rh/indicadores.html',
        total_funcionarios=total_funcionarios,
        funcionarios_ativos=funcionarios_ativos,
        funcionarios_inativos=funcionarios_inativos,
        acessos_controlados=acessos_controlados,
        funcoes_total=funcoes_total,
        funcoes_ativas=funcoes_ativas,
        admissoes_30_dias=admissoes_30_dias,
        distribuicao_roles=distribuicao_roles,
        funcionarios_recentes=funcionarios_recentes
    )


@app.route('/api/rh/analytics')
@require_role('admin', 'gerente')
def analytics_rh_api():
    periodo = request.args.get('periodo', type=int) or 30
    if periodo not in {30, 90, 365}:
        periodo = 30

    data_limite = datetime.utcnow() - timedelta(days=periodo)
    admissoes_periodo = Funcionario.query.filter(Funcionario.criado_em >= data_limite).count()

    distribuicao_roles = db.session.query(
        Funcionario.role.label('role'),
        db.func.count(Funcionario.id).label('quantidade')
    ).group_by(Funcionario.role).order_by(db.desc('quantidade')).all()

    ativos_por_dia_raw = db.session.query(
        db.func.date(Funcionario.criado_em).label('dia'),
        db.func.count(Funcionario.id).label('quantidade')
    ).filter(
        Funcionario.criado_em >= data_limite
    ).group_by(db.func.date(Funcionario.criado_em)).order_by(db.func.date(Funcionario.criado_em).asc()).all()

    return jsonify({
        'success': True,
        'message': 'Analytics RH carregado com sucesso.',
        'data': {
            'periodo_dias': periodo,
            'admissoes_periodo': admissoes_periodo,
            'distribuicao_roles': [
                {'role': item.role, 'quantidade': int(item.quantidade or 0)}
                for item in distribuicao_roles
            ],
            'admissoes_diarias': [
                {'dia': str(item.dia), 'quantidade': int(item.quantidade or 0)}
                for item in ativos_por_dia_raw
            ]
        }
    })


@app.route('/auditoria')
@require_role('admin', 'gerente')
def auditoria_sistema():
    funcionario_id = request.args.get('funcionario_id', type=int)
    acao = (request.args.get('acao') or '').strip()
    entidade = (request.args.get('entidade') or '').strip()
    metodo = (request.args.get('metodo') or '').strip().upper()

    query = AuditoriaEvento.query
    if funcionario_id:
        query = query.filter(AuditoriaEvento.funcionario_id == funcionario_id)
    if acao:
        query = query.filter(AuditoriaEvento.acao.ilike(f'%{acao}%'))
    if entidade:
        query = query.filter(AuditoriaEvento.entidade.ilike(f'%{entidade}%'))
    if metodo in {'GET', 'POST', 'PUT', 'PATCH', 'DELETE'}:
        query = query.filter(AuditoriaEvento.metodo == metodo)

    eventos = query.order_by(AuditoriaEvento.criado_em.desc()).limit(400).all()
    funcionarios = Funcionario.query.order_by(Funcionario.nome.asc()).all()
    return render_template(
        'sistema/auditoria.html',
        eventos=eventos,
        funcionarios=funcionarios,
        filtros={
            'funcionario_id': funcionario_id,
            'acao': acao,
            'entidade': entidade,
            'metodo': metodo,
        }
    )


@app.route('/rh/funcoes/nova', methods=['POST'])
@require_role('admin', 'gerente')
def nova_funcao_rh():
    nome = (request.form.get('nome') or '').strip()
    descricao = (request.form.get('descricao') or '').strip() or None
    ativo = request.form.get('ativo') == 'on'
    paginas_enviadas = set(request.form.getlist('paginas'))
    paginas_validas = set(PAGINAS_SISTEMA.keys())
    permissoes_padrao = list(paginas_enviadas.intersection(paginas_validas))

    if not nome:
        flash('Nome da função é obrigatório.', 'danger')
        return redirect(url_for('listar_funcoes_rh'))

    existente = FuncaoRH.query.filter(db.func.lower(FuncaoRH.nome) == nome.lower()).first()
    if existente:
        flash('Já existe uma função com esse nome.', 'warning')
        return redirect(url_for('listar_funcoes_rh'))

    try:
        funcao = FuncaoRH(nome=nome, descricao=descricao, ativo=ativo, permissoes_padrao=json.dumps(permissoes_padrao))
        db.session.add(funcao)
        db.session.commit()
        flash(f'Funcao "{nome}" criada com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao criar função: {str(e)}', 'danger')

    return redirect(url_for('listar_funcoes_rh'))


@app.route('/rh/funcoes/<int:funcao_id>/editar', methods=['GET', 'POST'])
@require_role('admin', 'gerente')
def editar_funcao_rh(funcao_id):
    funcao = FuncaoRH.query.get_or_404(funcao_id)

    if request.method == 'POST':
        nome = (request.form.get('nome') or '').strip()
        descricao = (request.form.get('descricao') or '').strip() or None
        ativo = request.form.get('ativo') == 'on'
        paginas_enviadas = set(request.form.getlist('paginas'))
        paginas_validas = set(PAGINAS_SISTEMA.keys())
        permissoes_padrao = list(paginas_enviadas.intersection(paginas_validas))

        if not nome:
            flash('Nome da função é obrigatório.', 'danger')
            return redirect(url_for('editar_funcao_rh', funcao_id=funcao_id))

        existente = FuncaoRH.query.filter(
            db.func.lower(FuncaoRH.nome) == nome.lower(),
            FuncaoRH.id != funcao.id
        ).first()
        if existente:
            flash('Já existe outra função com esse nome.', 'warning')
            return redirect(url_for('editar_funcao_rh', funcao_id=funcao_id))

        try:
            funcao.nome = nome
            funcao.descricao = descricao
            funcao.ativo = ativo
            funcao.permissoes_padrao = json.dumps(permissoes_padrao)
            db.session.commit()
            flash('Função atualizada com sucesso!', 'success')
            return redirect(url_for('listar_funcoes_rh'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar função: {str(e)}', 'danger')

    return render_template('rh/editar_funcao.html', funcao=funcao)


@app.route('/rh/funcoes/<int:funcao_id>/deletar', methods=['POST'])
@require_role('admin', 'gerente')
def deletar_funcao_rh(funcao_id):
    funcao = FuncaoRH.query.get_or_404(funcao_id)
    try:
        db.session.delete(funcao)
        db.session.commit()
        flash('Funcao removida com sucesso.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao remover função: {str(e)}', 'danger')
    return redirect(url_for('listar_funcoes_rh'))


# ============ REGISTRO DE MODULOS DE DOMINIO ============
register_estoque_routes(app, login_required, require_role, aplicar_movimentacao_estoque)
register_vendas_routes(app, login_required, require_role)
register_public_routes(app)


@app.before_request
def validar_acesso_por_pagina():
    ensure_csrf_token()
    csrf_result = csrf_protect_request()
    if csrf_result is not None:
        return csrf_result

    endpoint = request.endpoint
    if not endpoint:
        return None
    if endpoint == 'static' or endpoint.startswith('static'):
        return None
    if endpoint in {'login', 'logout', 'registro', 'index', 'central_ajuda', 'detalhe_ajuda', 'public.cardapio_mesa', 'public.enviar_pedido_qr'}:
        return None
    if 'funcionario_id' not in session:
        return None

    funcionario = get_funcionario_logado()
    if not funcionario or not funcionario.ativo:
        session.clear()
        flash('Sua sessao expirou. Faca login novamente.', 'warning')
        return redirect(url_for('login'))

    if not funcionario_tem_acesso(funcionario, endpoint):
        if is_json_request():
            return json_response(False, 'Sem permissao para acessar este recurso.', status=403, code='forbidden')
        flash('Acesso negado para esta pagina.', 'danger')
        return redirect(url_for('boas_vindas'))
    return None


@app.after_request
def registrar_auditoria_pos_resposta(response):
    try:
        if request.method in {'POST', 'PUT', 'PATCH', 'DELETE'}:
            endpoint = request.endpoint or ''
            if not endpoint.startswith('static'):
                ignorar = {
                    'login',
                    'logout',
                }
                if endpoint not in ignorar:
                    funcionario = get_funcionario_logado()
                    detalhes = _resumir_payload_requisicao()
                    registrar_evento_auditoria(
                        funcionario=funcionario,
                        acao=f'{request.method.lower()}_{endpoint or "sem_endpoint"}',
                        entidade='operacao_sistema',
                        detalhes=detalhes,
                        status_code=response.status_code
                    )
    except Exception:
        pass
    return response


# ============ CONTEXT PROCESSORS ============

@app.context_processor
def inject_user():
    funcionario_logado = get_funcionario_logado()
    empresa_config = EmpresaConfig.query.first()
    atendimento_mesas_ativo = not empresa_config or empresa_config.atendimento_mesas_ativo is not False
    produto_imagem_padrao_path = (
        (empresa_config.ecom_produto_placeholder_path if empresa_config else None)
        or 'img/placeholders/produto-sem-foto.svg'
    )
    favicon_path = (empresa_config.ecom_favicon_path if empresa_config else None)
    csrf_token_value = ensure_csrf_token()
    return {
        'ano_atual': datetime.utcnow().year,
        'total_alertas': Produto.query.filter(
            Produto.quantidade_estoque < Produto.quantidade_minima,
            Produto.ativo == True
        ).count(),
        'funcionario_logado': funcionario_logado,
        'empresa_config': empresa_config,
        'atendimento_mesas_ativo': atendimento_mesas_ativo,
        'produto_imagem_padrao_path': produto_imagem_padrao_path,
        'favicon_path': favicon_path,
        'csrf_token': csrf_token_value,
        'csrf_input': csrf_input_tag()
    }


# ============ ERROR HANDLERS ============

@app.errorhandler(400)
def bad_request(error):
    mensagem = getattr(error, 'description', None) or 'Requisicao invalida.'
    if is_json_request():
        return json_response(False, mensagem, status=400, code='bad_request')
    return render_template('errors/500.html', error_message=mensagem), 400


@app.errorhandler(403)
def forbidden(error):
    mensagem = getattr(error, 'description', None) or 'Acesso negado.'
    if is_json_request():
        return json_response(False, mensagem, status=403, code='forbidden')
    return render_template('errors/500.html', error_message=mensagem), 403


@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500


def create_app():
    """Factory compatível com Flask CLI e scripts do projeto."""
    return app


__all__ = [
    'app',
    'create_app',
    'db',
    'sincronizar_garcom_funcionario',
]


