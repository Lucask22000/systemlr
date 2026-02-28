from datetime import datetime, timedelta
from functools import wraps
import os

from flask import Flask, flash, redirect, render_template, request, session, url_for
from sqlalchemy import inspect, text
from werkzeug.utils import secure_filename

from config import config
from models import Categoria, EnderecoEstoque, Funcionario, FuncaoRH, Movimentacao, Produto, PermissaoAcesso, Caixa, MovimentacaoCaixa, Pedido, ItemPedido, Garcom, EmpresaConfig, db
from routes.estoque_routes import register_estoque_routes
from routes.vendas_routes import register_vendas_routes
from routes.public_routes import register_public_routes

# Informacoes do SystemLR
APP_NAME = 'SystemLR'
APP_VERSION = '1.0.0'
APP_DOMAIN = 'systemlr.com'

app = Flask(__name__)
app.config.from_object(config['development'])
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'

# Inicializar banco de dados
db.init_app(app)

TIPOS_MOVIMENTACAO_VALIDOS = {Movimentacao.TIPO_ENTRADA, Movimentacao.TIPO_SAIDA}
ROLES_PERMITIDOS = {'admin', 'gerente', 'caixa', 'operador', 'garcom'}
CARGOS_PERMANENTES = (
    ('Garcom', 'Atendimento de mesas e acompanhamento de pedidos.'),
)
PAGINAS_SISTEMA = {
    'inicio': 'Inicio e Dashboard',
    'pdv': 'PDV',
    'produtos': 'Produtos',
    'categorias': 'Categorias',
    'fornecedores': 'Fornecedores',
    'enderecos_estoque': 'Enderecos de Estoque',
    'movimentacoes': 'Movimentacoes',
    'relatorios': 'Relatorios',
    'caixas': 'Caixas',
    'mesas': 'Mesas',
    'pedidos': 'Pedidos',
    'funcionarios': 'Funcionarios',
    'rh_funcoes': 'RH - Funcoes',
    'rh_indicadores': 'RH - Indicadores',
    'empresa': 'Empresa',
    'garcons': 'Garcons'
}
PAGINAS_SISTEMA_MENU_ORDEM = (
    ('Dashboard', ('inicio',)),
    ('Vendas', ('pdv', 'pedidos', 'mesas', 'caixas', 'garcons')),
    ('Estoque', ('produtos', 'categorias', 'fornecedores', 'enderecos_estoque', 'movimentacoes', 'relatorios')),
    ('Meu RH', ('rh_indicadores', 'funcionarios', 'rh_funcoes', 'empresa')),
)
PAGINA_ENDPOINTS = {
    'inicio': {'dashboard', 'boas_vindas'},
    'pdv': {'pdv'},
    'produtos': {'listar_produtos', 'novo_produto', 'editar_produto', 'visualizar_produto', 'deletar_produto'},
    'categorias': {'listar_categorias', 'nova_categoria', 'editar_categoria', 'deletar_categoria'},
    'fornecedores': {'listar_fornecedores', 'novo_fornecedor', 'editar_fornecedor', 'deletar_fornecedor'},
    'enderecos_estoque': {'listar_enderecos_estoque', 'novo_endereco_estoque', 'editar_endereco_estoque', 'deletar_endereco_estoque'},
    'movimentacoes': {'listar_movimentacoes', 'nova_movimentacao', 'movimentacao_rapida'},
    'relatorios': {'relatorios'},
    'caixas': {'listar_caixas', 'nova_caixa', 'editar_caixa', 'deletar_caixa', 'abrir_caixa', 'fechar_caixa', 'historico_caixa'},
    'mesas': {'listar_mesas', 'nova_mesa', 'editar_mesa', 'deletar_mesa'},
    'pedidos': {'listar_pedidos', 'novo_pedido', 'editar_pedido', 'deletar_pedido', 'visualizar_comprovante_pedido'},
    'funcionarios': {'listar_funcionarios', 'criar_funcionario', 'editar_funcionario', 'deletar_funcionario', 'editar_acessos_funcionario'},
    'rh_funcoes': {'listar_funcoes_rh', 'nova_funcao_rh', 'editar_funcao_rh', 'deletar_funcao_rh'},
    'rh_indicadores': {'indicadores_rh'},
    'empresa': {'editar_empresa'},
    'garcons': {'listar_garcons', 'novo_garcom', 'editar_garcom', 'deletar_garcom', 'configurar_distribuicao_garcons'}
}
ENDPOINT_TO_PAGINA = {
    endpoint: pagina
    for pagina, endpoints in PAGINA_ENDPOINTS.items()
    for endpoint in endpoints
}

# Criar tabelas e ajustes simples de schema
with app.app_context():
    db.create_all()
    inspector = inspect(db.engine)
    colunas_movimentacoes = {col['name'] for col in inspector.get_columns('movimentacoes')}
    if 'fornecedor_id' not in colunas_movimentacoes:
        db.session.execute(text('ALTER TABLE movimentacoes ADD COLUMN fornecedor_id INTEGER'))
        db.session.commit()
    if 'valor_compra' not in colunas_movimentacoes:
        db.session.execute(text('ALTER TABLE movimentacoes ADD COLUMN valor_compra FLOAT'))
        db.session.commit()
    if 'info_nota' not in colunas_movimentacoes:
        db.session.execute(text('ALTER TABLE movimentacoes ADD COLUMN info_nota VARCHAR(255)'))
        db.session.commit()
    # categorias image
    colunas_categorias = {col['name'] for col in inspector.get_columns('categorias')}
    if 'imagem_path' not in colunas_categorias:
        db.session.execute(text('ALTER TABLE categorias ADD COLUMN imagem_path VARCHAR(255)'))
        db.session.commit()
    colunas_funcionarios = {col['name'] for col in inspector.get_columns('funcionarios')}
    if 'controle_acesso_ativo' not in colunas_funcionarios:
        db.session.execute(text('ALTER TABLE funcionarios ADD COLUMN controle_acesso_ativo BOOLEAN DEFAULT 0'))
        db.session.commit()
    if 'cargo' not in colunas_funcionarios:
        db.session.execute(text('ALTER TABLE funcionarios ADD COLUMN cargo VARCHAR(100)'))
        db.session.commit()
    colunas_mesas = {col['name'] for col in inspector.get_columns('mesas')}
    if 'qr_token' not in colunas_mesas:
        db.session.execute(text('ALTER TABLE mesas ADD COLUMN qr_token VARCHAR(64)'))
        db.session.commit()
    colunas_pedidos = {col['name'] for col in inspector.get_columns('pedidos')}
    if 'origem' not in colunas_pedidos:
        db.session.execute(text("ALTER TABLE pedidos ADD COLUMN origem VARCHAR(20) DEFAULT 'interno'"))
        db.session.commit()
    if 'metodo_pagamento' not in colunas_pedidos:
        db.session.execute(text('ALTER TABLE pedidos ADD COLUMN metodo_pagamento VARCHAR(50)'))
        db.session.commit()
    if 'valor_pago' not in colunas_pedidos:
        db.session.execute(text('ALTER TABLE pedidos ADD COLUMN valor_pago FLOAT'))
        db.session.commit()
    if 'garcom_id' not in colunas_pedidos:
        db.session.execute(text('ALTER TABLE pedidos ADD COLUMN garcom_id INTEGER'))
        db.session.commit()
    if 'cliente_nome' not in colunas_pedidos:
        db.session.execute(text('ALTER TABLE pedidos ADD COLUMN cliente_nome VARCHAR(120)'))
        db.session.commit()
    if 'cliente_celular' not in colunas_pedidos:
        db.session.execute(text('ALTER TABLE pedidos ADD COLUMN cliente_celular VARCHAR(30)'))
        db.session.commit()
    colunas_garcons = {col['name'] for col in inspector.get_columns('garcons')}
    if 'funcionario_id' not in colunas_garcons:
        db.session.execute(text('ALTER TABLE garcons ADD COLUMN funcionario_id INTEGER'))
        db.session.commit()
    colunas_produtos = {col['name'] for col in inspector.get_columns('produtos')}
    if 'imagem_path' not in colunas_produtos:
        db.session.execute(text('ALTER TABLE produtos ADD COLUMN imagem_path VARCHAR(255)'))
        db.session.commit()
    if 'endereco_id' not in colunas_produtos:
        db.session.execute(text('ALTER TABLE produtos ADD COLUMN endereco_id INTEGER'))
        db.session.commit()
    tabelas_existentes = set(inspector.get_table_names())
    if 'empresa_config' in tabelas_existentes:
        colunas_empresa = {col['name'] for col in inspector.get_columns('empresa_config')}
        if 'logo_path' not in colunas_empresa:
            db.session.execute(text('ALTER TABLE empresa_config ADD COLUMN logo_path VARCHAR(255)'))
            db.session.commit()
        if 'cardapio_titulo' not in colunas_empresa:
            db.session.execute(text('ALTER TABLE empresa_config ADD COLUMN cardapio_titulo VARCHAR(120)'))
            db.session.commit()
        if 'cardapio_subtitulo' not in colunas_empresa:
            db.session.execute(text('ALTER TABLE empresa_config ADD COLUMN cardapio_subtitulo VARCHAR(255)'))
            db.session.commit()
        if 'cardapio_mensagem' not in colunas_empresa:
            db.session.execute(text('ALTER TABLE empresa_config ADD COLUMN cardapio_mensagem VARCHAR(255)'))
            db.session.commit()
        if 'cardapio_mostrar_imagem' not in colunas_empresa:
            db.session.execute(text('ALTER TABLE empresa_config ADD COLUMN cardapio_mostrar_imagem BOOLEAN DEFAULT 1'))
            db.session.commit()
        if 'cardapio_mostrar_descricao' not in colunas_empresa:
            db.session.execute(text('ALTER TABLE empresa_config ADD COLUMN cardapio_mostrar_descricao BOOLEAN DEFAULT 1'))
            db.session.commit()
        if 'cardapio_qtd_maxima' not in colunas_empresa:
            db.session.execute(text('ALTER TABLE empresa_config ADD COLUMN cardapio_qtd_maxima INTEGER DEFAULT 20'))
            db.session.commit()
        if 'distribuicao_ativa' not in colunas_empresa:
            db.session.execute(text('ALTER TABLE empresa_config ADD COLUMN distribuicao_ativa BOOLEAN DEFAULT 1'))
            db.session.commit()
        if 'modo_distribuicao_pedidos' not in colunas_empresa:
            db.session.execute(text("ALTER TABLE empresa_config ADD COLUMN modo_distribuicao_pedidos VARCHAR(30) DEFAULT 'round_robin'"))
            db.session.commit()
        if 'ultimo_garcom_id' not in colunas_empresa:
            db.session.execute(text('ALTER TABLE empresa_config ADD COLUMN ultimo_garcom_id INTEGER'))
            db.session.commit()

    # Garante cargo permanente para uso em cadastro de funcionarios.
    nomes_existentes = {(f.nome or '').strip().lower() for f in FuncaoRH.query.all()}
    for nome_cargo, descricao_cargo in CARGOS_PERMANENTES:
        if nome_cargo.lower() not in nomes_existentes:
            db.session.add(FuncaoRH(nome=nome_cargo, descricao=descricao_cargo, ativo=True))
    db.session.commit()


# ============ DECORADORES DE AUTENTICACAO ============

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'funcionario_id' not in session:
            flash('Voce precisa fazer login para acessar esta pagina.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


def require_role(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'funcionario_id' not in session:
                flash('Voce precisa fazer login.', 'warning')
                return redirect(url_for('login'))

            funcionario = Funcionario.query.get(session['funcionario_id'])
            if not funcionario or not funcionario.ativo:
                session.clear()
                flash('Funcionario inativo ou removido.', 'danger')
                return redirect(url_for('login'))

            if funcionario.role not in roles:
                flash('Voce nao tem permissao para acessar esta pagina.', 'danger')
                return redirect(url_for('dashboard'))

            return f(*args, **kwargs)

        return decorated_function

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
        garcom.ativo = funcionario.ativo


def funcionario_tem_acesso(funcionario, endpoint):
    if not funcionario:
        return False
    if funcionario.role == 'admin':
        return True
    pagina = ENDPOINT_TO_PAGINA.get(endpoint)
    if not pagina:
        return True
    if not funcionario.controle_acesso_ativo:
        return True

    return PermissaoAcesso.query.filter_by(funcionario_id=funcionario.id, pagina=pagina).first() is not None


def aplicar_movimentacao_estoque(produto, tipo, quantidade):
    if tipo not in TIPOS_MOVIMENTACAO_VALIDOS:
        return 'Tipo de movimentacao invalido'

    if quantidade <= 0:
        return 'Quantidade deve ser maior que 0'

    if tipo == Movimentacao.TIPO_ENTRADA:
        produto.quantidade_estoque += quantidade
        return None

    if produto.quantidade_estoque < quantidade:
        return 'Quantidade em estoque insuficiente'

    produto.quantidade_estoque -= quantidade
    return None


# ============ ROTAS - AUTENTICACAO ============

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        senha = request.form.get('senha', '')

        if not email or not senha:
            flash('Email e senha sao obrigatorios.', 'danger')
            return redirect(url_for('login'))

        funcionario = Funcionario.query.filter_by(email=email).first()

        if funcionario and funcionario.check_password(senha):
            if not funcionario.ativo:
                flash('Usuario inativo. Contate um administrador.', 'danger')
                return redirect(url_for('login'))

            session['funcionario_id'] = funcionario.id
            session['funcionario_nome'] = funcionario.nome
            session['funcionario_role'] = funcionario.role
            db.session.commit()

            flash(f'Bem-vindo, {funcionario.nome}!', 'success')
            return redirect(url_for('dashboard'))

        flash('Email ou senha incorretos.', 'danger')
        return redirect(url_for('login'))

    return render_template('sistema/login.html')


@app.route('/logout')
def logout():
    nome = session.get('funcionario_nome', 'Usuario')
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
            flash('Nome, email e senha sao obrigatorios.', 'danger')
            return redirect(url_for('registro'))

        if senha != confirmacao_senha:
            flash('As senhas nao conferem.', 'danger')
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
            flash('Perfil de acesso invalido.', 'danger')
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
    return redirect(url_for('boas_vindas'))


@app.route('/dashboard')
@login_required
def dashboard():
    agora = datetime.utcnow()
    inicio_hoje = agora.replace(hour=0, minute=0, second=0, microsecond=0)
    fim_hoje = inicio_hoje + timedelta(days=1)

    data_inicial_str = (request.args.get('data_inicial') or '').strip()
    data_final_str = (request.args.get('data_final') or '').strip()

    try:
        if data_inicial_str:
            inicio_periodo = datetime.strptime(data_inicial_str, '%Y-%m-%d')
        else:
            inicio_periodo = inicio_hoje - timedelta(days=6)
            data_inicial_str = inicio_periodo.strftime('%Y-%m-%d')
    except ValueError:
        inicio_periodo = inicio_hoje - timedelta(days=6)
        data_inicial_str = inicio_periodo.strftime('%Y-%m-%d')

    try:
        if data_final_str:
            fim_periodo = datetime.strptime(data_final_str, '%Y-%m-%d') + timedelta(days=1)
        else:
            fim_periodo = fim_hoje
            data_final_str = inicio_hoje.strftime('%Y-%m-%d')
    except ValueError:
        fim_periodo = fim_hoje
        data_final_str = inicio_hoje.strftime('%Y-%m-%d')

    if fim_periodo <= inicio_periodo:
        fim_periodo = inicio_periodo + timedelta(days=1)
        data_final_str = (fim_periodo - timedelta(days=1)).strftime('%Y-%m-%d')

    periodo_dias = (fim_periodo - inicio_periodo).days

    pedidos_periodo = Pedido.query.filter(
        Pedido.status == 'fechado',
        Pedido.fechado_em >= inicio_periodo,
        Pedido.fechado_em < fim_periodo
    ).all()
    pedidos_periodo_total = len(pedidos_periodo)
    faturamento_periodo = sum((pedido.total or 0) for pedido in pedidos_periodo)
    ticket_medio_periodo = (faturamento_periodo / pedidos_periodo_total) if pedidos_periodo_total else 0

    pedidos_abertos = Pedido.query.filter(Pedido.status.in_(['aberto', 'em_preparo'])).count()
    pedidos_cancelados_periodo = Pedido.query.filter(
        Pedido.status == 'cancelado',
        Pedido.criado_em >= inicio_periodo,
        Pedido.criado_em < fim_periodo
    ).count()
    faturamento_hoje = db.session.query(
        db.func.sum(Pedido.total)
    ).filter(
        Pedido.status == 'fechado',
        Pedido.fechado_em >= inicio_hoje,
        Pedido.fechado_em < fim_hoje
    ).scalar() or 0

    vendas_periodo_raw = db.session.query(
        db.func.date(Pedido.fechado_em).label('dia'),
        db.func.sum(Pedido.total).label('faturamento'),
        db.func.count(Pedido.id).label('pedidos')
    ).filter(
        Pedido.status == 'fechado',
        Pedido.fechado_em >= inicio_periodo,
        Pedido.fechado_em < fim_periodo
    ).group_by(db.func.date(Pedido.fechado_em)).all()
    vendas_periodo_map = {
        str(item.dia): {
            'faturamento': float(item.faturamento or 0),
            'pedidos': int(item.pedidos or 0)
        }
        for item in vendas_periodo_raw
    }

    vendas_periodo = []
    for i in range(periodo_dias):
        dia = inicio_periodo + timedelta(days=i)
        chave_dia = dia.strftime('%Y-%m-%d')
        valores_dia = vendas_periodo_map.get(chave_dia, {'faturamento': 0.0, 'pedidos': 0})
        vendas_periodo.append({
            'data_curta': dia.strftime('%d/%m'),
            'data_semana': dia.strftime('%a'),
            'faturamento': valores_dia['faturamento'],
            'pedidos': valores_dia['pedidos']
        })

    maior_faturamento_periodo = max((item['faturamento'] for item in vendas_periodo), default=0)
    for item in vendas_periodo:
        item['faturamento_pct'] = (item['faturamento'] / maior_faturamento_periodo * 100) if maior_faturamento_periodo else 0

    quantidade_vendida = db.func.sum(ItemPedido.quantidade).label('quantidade_vendida')
    receita_gerada = db.func.sum(ItemPedido.quantidade * ItemPedido.preco_unitario).label('receita_gerada')
    top_produtos_vendidos = db.session.query(
        Produto,
        quantidade_vendida,
        receita_gerada
    ).join(
        ItemPedido, ItemPedido.produto_id == Produto.id
    ).join(
        Pedido, Pedido.id == ItemPedido.pedido_id
    ).filter(
        Pedido.status == 'fechado',
        Pedido.fechado_em >= inicio_periodo,
        Pedido.fechado_em < fim_periodo
    ).group_by(Produto.id).order_by(
        db.desc(quantidade_vendida)
    ).limit(5).all()
    pedidos_por_status_raw = db.session.query(
        Pedido.status.label('status'),
        db.func.count(Pedido.id).label('quantidade')
    ).filter(
        Pedido.criado_em >= inicio_periodo,
        Pedido.criado_em < fim_periodo
    ).group_by(Pedido.status).all()
    status_labels = {
        'aberto': 'Aberto',
        'em_preparo': 'Em preparo',
        'entregue': 'Entregue',
        'fechado': 'Venda concluida',
        'cancelado': 'Cancelado'
    }
    pedidos_por_status = [
        {
            'status': item.status,
            'label': status_labels.get(item.status, item.status),
            'quantidade': int(item.quantidade or 0)
        }
        for item in pedidos_por_status_raw
    ]
    pedidos_por_status.sort(key=lambda item: item['quantidade'], reverse=True)

    top_clientes = db.session.query(
        Pedido.cliente_nome.label('cliente_nome'),
        db.func.count(Pedido.id).label('pedidos'),
        db.func.sum(Pedido.total).label('faturamento')
    ).filter(
        Pedido.status == 'fechado',
        Pedido.fechado_em >= inicio_periodo,
        Pedido.fechado_em < fim_periodo,
        Pedido.cliente_nome.isnot(None),
        Pedido.cliente_nome != ''
    ).group_by(Pedido.cliente_nome).order_by(
        db.desc('faturamento')
    ).limit(5).all()

    desempenho_garcons = db.session.query(
        Garcom.nome.label('nome'),
        db.func.count(Pedido.id).label('pedidos'),
        db.func.sum(Pedido.total).label('faturamento')
    ).join(
        Pedido, Pedido.garcom_id == Garcom.id
    ).filter(
        Pedido.status == 'fechado',
        Pedido.fechado_em >= inicio_periodo,
        Pedido.fechado_em < fim_periodo
    ).group_by(Garcom.id, Garcom.nome).order_by(
        db.desc('faturamento')
    ).limit(5).all()

    desempenho_caixas = db.session.query(
        Caixa.nome.label('nome'),
        db.func.count(Pedido.id).label('pedidos'),
        db.func.sum(Pedido.total).label('faturamento')
    ).join(
        Pedido, Pedido.caixa_id == Caixa.id
    ).filter(
        Pedido.status == 'fechado',
        Pedido.fechado_em >= inicio_periodo,
        Pedido.fechado_em < fim_periodo
    ).group_by(Caixa.id, Caixa.nome).order_by(
        db.desc('faturamento')
    ).limit(5).all()

    metodos_pagamento_map = {}
    for pedido in pedidos_periodo:
        metodo_raw = (pedido.metodo_pagamento or 'nao informado').lower()
        if 'dividido' in metodo_raw:
            metodo_key = 'dividido'
        elif 'crediario' in metodo_raw:
            metodo_key = 'crediario'
        elif 'dinheiro' in metodo_raw:
            metodo_key = 'dinheiro'
        elif 'cartao' in metodo_raw:
            metodo_key = 'cartao'
        elif 'pix' in metodo_raw:
            metodo_key = 'pix'
        else:
            metodo_key = metodo_raw
        metodos_pagamento_map[metodo_key] = metodos_pagamento_map.get(metodo_key, 0) + 1
    metodos_pagamento = sorted(
        [{'metodo': k, 'quantidade': v} for k, v in metodos_pagamento_map.items()],
        key=lambda item: item['quantidade'],
        reverse=True
    )

    return render_template(
        'dashboard/index.html',
        periodo_dias=periodo_dias,
        data_inicial=data_inicial_str,
        data_final=data_final_str,
        pedidos_periodo_total=pedidos_periodo_total,
        faturamento_periodo=faturamento_periodo,
        faturamento_hoje=faturamento_hoje,
        ticket_medio_periodo=ticket_medio_periodo,
        pedidos_abertos=pedidos_abertos,
        pedidos_cancelados_periodo=pedidos_cancelados_periodo,
        vendas_periodo=vendas_periodo,
        top_produtos_vendidos=top_produtos_vendidos,
        pedidos_por_status=pedidos_por_status,
        top_clientes=top_clientes,
        desempenho_garcons=desempenho_garcons,
        desempenho_caixas=desempenho_caixas,
        metodos_pagamento=metodos_pagamento
    )


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

            remover_logo = (request.form.get('remover_logo') == 'on')
            arquivo_logo = request.files.get('logo')
            allowed_ext = {'.png', '.jpg', '.jpeg', '.webp', '.gif'}
            if arquivo_logo and arquivo_logo.filename:
                _, ext = os.path.splitext(arquivo_logo.filename.lower())
                if ext not in allowed_ext:
                    flash('Formato de logo invalido. Use PNG, JPG, JPEG, WEBP ou GIF.', 'error')
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

    return render_template('sistema/empresa.html', empresa=empresa)


@app.route('/empresa/config-cardapio/preview')
@require_role('admin', 'gerente')
def preview_cardapio_empresa():
    empresa = EmpresaConfig.query.first()
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
            flash('Nome, email e senha sao obrigatorios.', 'danger')
            return redirect(url_for('criar_funcionario'))

        if senha != confirmacao_senha:
            flash('As senhas nao conferem.', 'danger')
            return redirect(url_for('criar_funcionario'))

        if len(senha) < 6:
            flash('A senha deve ter no minimo 6 caracteres.', 'danger')
            return redirect(url_for('criar_funcionario'))

        if Funcionario.query.filter_by(email=email).first():
            flash('Email ja cadastrado.', 'danger')
            return redirect(url_for('criar_funcionario'))

        if role not in ROLES_PERMITIDOS:
            flash('Perfil de acesso invalido.', 'danger')
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
        flash('Voce nao tem permissao para editar este funcionario.', 'danger')
        return redirect(url_for('listar_funcionarios'))

    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        role = _normalizar_texto(request.form.get('role', funcionario.role))
        cargo = (request.form.get('cargo') or '').strip()
        ativo = request.form.get('ativo') == 'on'
        nova_senha = request.form.get('nova_senha', '')

        if not nome or not email:
            flash('Nome e email sao obrigatorios.', 'danger')
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
                flash('Perfil de acesso invalido.', 'danger')
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
        flash('Voce nao pode deletar sua propria conta.', 'danger')
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


@app.route('/rh/funcoes/nova', methods=['POST'])
@require_role('admin', 'gerente')
def nova_funcao_rh():
    nome = (request.form.get('nome') or '').strip()
    descricao = (request.form.get('descricao') or '').strip() or None
    ativo = request.form.get('ativo') == 'on'

    if not nome:
        flash('Nome da funcao e obrigatorio.', 'danger')
        return redirect(url_for('listar_funcoes_rh'))

    existente = FuncaoRH.query.filter(db.func.lower(FuncaoRH.nome) == nome.lower()).first()
    if existente:
        flash('Ja existe uma funcao com esse nome.', 'warning')
        return redirect(url_for('listar_funcoes_rh'))

    try:
        funcao = FuncaoRH(nome=nome, descricao=descricao, ativo=ativo)
        db.session.add(funcao)
        db.session.commit()
        flash(f'Funcao "{nome}" criada com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao criar funcao: {str(e)}', 'danger')

    return redirect(url_for('listar_funcoes_rh'))


@app.route('/rh/funcoes/<int:funcao_id>/editar', methods=['GET', 'POST'])
@require_role('admin', 'gerente')
def editar_funcao_rh(funcao_id):
    funcao = FuncaoRH.query.get_or_404(funcao_id)

    if request.method == 'POST':
        nome = (request.form.get('nome') or '').strip()
        descricao = (request.form.get('descricao') or '').strip() or None
        ativo = request.form.get('ativo') == 'on'

        if not nome:
            flash('Nome da funcao e obrigatorio.', 'danger')
            return redirect(url_for('editar_funcao_rh', funcao_id=funcao_id))

        existente = FuncaoRH.query.filter(
            db.func.lower(FuncaoRH.nome) == nome.lower(),
            FuncaoRH.id != funcao.id
        ).first()
        if existente:
            flash('Ja existe outra funcao com esse nome.', 'warning')
            return redirect(url_for('editar_funcao_rh', funcao_id=funcao_id))

        try:
            funcao.nome = nome
            funcao.descricao = descricao
            funcao.ativo = ativo
            db.session.commit()
            flash('Funcao atualizada com sucesso!', 'success')
            return redirect(url_for('listar_funcoes_rh'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar funcao: {str(e)}', 'danger')

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
        flash(f'Erro ao remover funcao: {str(e)}', 'danger')
    return redirect(url_for('listar_funcoes_rh'))


# ============ REGISTRO DE MODULOS DE DOMINIO ============
register_estoque_routes(app, login_required, aplicar_movimentacao_estoque)
register_vendas_routes(app, login_required)
register_public_routes(app)


@app.before_request
def validar_acesso_por_pagina():
    endpoint = request.endpoint
    if not endpoint:
        return None
    if endpoint == 'static' or endpoint.startswith('static'):
        return None
    if endpoint in {'login', 'logout', 'registro', 'index', 'public.cardapio_mesa', 'public.enviar_pedido_qr'}:
        return None
    if 'funcionario_id' not in session:
        return None

    funcionario = get_funcionario_logado()
    if not funcionario or not funcionario.ativo:
        session.clear()
        flash('Sua sessao expirou. Faca login novamente.', 'warning')
        return redirect(url_for('login'))

    if not funcionario_tem_acesso(funcionario, endpoint):
        flash('Acesso negado para esta pagina.', 'danger')
        return redirect(url_for('boas_vindas'))
    return None


# ============ CONTEXT PROCESSORS ============

@app.context_processor
def inject_user():
    funcionario_logado = get_funcionario_logado()
    empresa_config = EmpresaConfig.query.first()
    return {
        'ano_atual': datetime.utcnow().year,
        'total_alertas': Produto.query.filter(
            Produto.quantidade_estoque < Produto.quantidade_minima,
            Produto.ativo == True
        ).count(),
        'funcionario_logado': funcionario_logado,
        'empresa_config': empresa_config
    }


# ============ ERROR HANDLERS ============

@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


