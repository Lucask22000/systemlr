from datetime import datetime, timedelta
import os
import json
import csv
import io
import re
from urllib.parse import urlparse

from flask import Response, flash, jsonify, redirect, render_template, request, send_from_directory, session, url_for
from sqlalchemy.exc import OperationalError
from sqlalchemy import inspect, text
from sqlalchemy.orm import selectinload
from werkzeug.utils import secure_filename

from models import Categoria, ClientePublico, EnderecoEstoque, Estoque, Fornecedor, Funcionario, FuncaoRH, PerfilAcesso, LancamentoFinanceiro, Movimentacao, Produto, PermissaoAcesso, Caixa, MovimentacaoCaixa, Pedido, ItemPedido, Garcom, EmpresaConfig, AuditoriaEvento, AssistenteLocalFeedback, EquipamentoMovimentacao, ManutencaoEquipamento, OrdemServico, ChamadoInterno, FundoSolicitacao, RecebimentoFornecedor, AlmoxarifadoAtribuicao, funcionario_estoques, db
from routes.estoque_routes import register_estoque_routes
from routes.vendas_routes import register_vendas_routes
from routes.public_routes import obter_resumo_carrinho_site, register_public_routes
from security import csrf_input_tag, csrf_protect_request, ensure_csrf_token, is_json_request, json_response
from app.api_routes import register_routes as register_api_routes
from app import extensions
from app.auth_routes import register_routes as register_auth_routes
from app.cli import register_cli
from app.decorators import _limit, login_required, require_role
from app.exceptions import AppError, BusinessRuleError, NotFound, PermissionDenied, ValidationError
from app.factory import create_app as create_base_app
from app.helpers import (
    _client_ip,
    _coletar_dashboard_analytics,
    _is_login_rate_limited,
    _normalizar_texto,
    _parse_date_range,
    _register_login_attempt,
    get_funcionario_logado,
)
from app.services.assistente_service import LocalAIAssistant
from app.services.estoque_service import aplicar_movimentacao_estoque
from app.services.rh_service import sincronizar_garcom_funcionario
from app.constants import (
    CARGOS_PERMANENTES,
    ENDPOINT_TO_PAGINA,
    NIVEIS_ORGANOGRAMA,
    PAGINA_ENDPOINTS,
    PAGINAS_SISTEMA,
    PAGINAS_SISTEMA_MENU_ORDEM,
    ROLES_PERMITIDOS,
    TIPOS_MOVIMENTACAO_VALIDOS,
)
from app.utils.payment_config import (
    api_integrations_text_to_json,
    api_integrations_to_text,
    payment_options_to_text,
    payment_text_to_json,
)
from app.utils.validators import (
    normalizar_matricula as shared_normalizar_matricula,
    validar_cpf as shared_validar_cpf,
    validar_data as shared_validar_data,
)

# Informacoes do SystemLR
APP_NAME = 'SystemLR'
APP_VERSION = '1.0.0'
APP_DOMAIN = 'systemlr.com'

PRIMEIRO_ACESSO_EMAIL = ((os.environ.get('SYSTEMLR_BOOTSTRAP_ADMIN_EMAIL') or 'admin@systemlr.com').strip().lower())
PRIMEIRO_ACESSO_SENHA = os.environ.get('SYSTEMLR_BOOTSTRAP_ADMIN_PASSWORD') or ''
PRIMEIRO_ACESSO_NOME = 'Administrador SystemLR'

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

app = create_base_app()
local_ai_assistant = None

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


def _carregar_paginas_json(valor_json):
    if not valor_json:
        return set()
    try:
        dados = json.loads(valor_json)
    except Exception:
        return set()
    if not isinstance(dados, list):
        return set()
    return {
        str(item)
        for item in dados
        if isinstance(item, str) and item in PAGINAS_SISTEMA
    }


def _serializar_paginas_json(paginas):
    return json.dumps(sorted(set(paginas)))


def _expandir_paginas_relacionadas(paginas, bloqueadas=None):
    paginas_normalizadas = set(paginas or [])
    bloqueadas = set(bloqueadas or [])
    if 'movimentacoes' in paginas_normalizadas and 'recebimentos' not in bloqueadas:
        paginas_normalizadas.add('recebimentos')
    if 'movimentacoes' in paginas_normalizadas and 'almoxarifado' not in bloqueadas:
        paginas_normalizadas.add('almoxarifado')
    if 'expedicao' in paginas_normalizadas and 'transferencias_estoque' not in bloqueadas:
        paginas_normalizadas.add('transferencias_estoque')
    return paginas_normalizadas


def _paginas_perfil_acesso(perfil_acesso):
    if not perfil_acesso:
        return set()
    return _expandir_paginas_relacionadas(_carregar_paginas_json(perfil_acesso.permissoes_padrao))


def _mapa_permissoes_personalizadas_funcionario(funcionario):
    if not funcionario:
        return {}
    return {
        permissao.pagina: bool(permissao.permitido)
        for permissao in PermissaoAcesso.query.filter_by(funcionario_id=funcionario.id).all()
        if permissao.pagina in PAGINAS_SISTEMA
    }


def _paginas_efetivas_funcionario(funcionario):
    if not funcionario:
        return set()

    if funcionario.role == 'admin' or not funcionario.controle_acesso_ativo:
        permitidas = set(PAGINAS_SISTEMA.keys())
    else:
        mapa_personalizado = _mapa_permissoes_personalizadas_funcionario(funcionario)
        bloqueadas = {
            pagina
            for pagina, permitido in mapa_personalizado.items()
            if not permitido
        }
        permitidas = _carregar_paginas_json(
            getattr(funcionario.perfil_acesso, 'permissoes_padrao', None)
        )
        permitidas.update(
            pagina
            for pagina, permitido in mapa_personalizado.items()
            if permitido
        )
        permitidas.difference_update(bloqueadas)
        permitidas = _expandir_paginas_relacionadas(permitidas, bloqueadas=bloqueadas)

    permitidas.add('ajuda')
    return permitidas


def _salvar_permissoes_funcionario(funcionario, paginas_selecionadas):
    paginas_validas = set(PAGINAS_SISTEMA.keys())
    paginas_salvas = set(paginas_selecionadas).intersection(paginas_validas)
    paginas_base = _paginas_perfil_acesso(funcionario.perfil_acesso)

    PermissaoAcesso.query.filter_by(funcionario_id=funcionario.id).delete()

    if funcionario.perfil_acesso_id:
        for pagina in sorted(paginas_validas):
            presente_na_base = pagina in paginas_base
            presente_no_resultado = pagina in paginas_salvas
            if presente_na_base == presente_no_resultado:
                continue
            db.session.add(
                PermissaoAcesso(
                    funcionario_id=funcionario.id,
                    pagina=pagina,
                    permitido=presente_no_resultado,
                )
            )
    else:
        for pagina in sorted(paginas_salvas):
            db.session.add(
                PermissaoAcesso(
                    funcionario_id=funcionario.id,
                    pagina=pagina,
                    permitido=True,
                )
            )

    funcionario.controle_acesso_ativo = True


def _migrar_funcoes_legadas_para_perfis():
    try:
        perfis_existentes = {
            (perfil.nome or '').strip().lower(): perfil
            for perfil in PerfilAcesso.query.all()
        }
        perfis_criados = {}
        mudou = False

        for funcao in FuncaoRH.query.all():
            paginas = _carregar_paginas_json(funcao.permissoes_padrao)
            if not paginas:
                continue

            nome_base = (funcao.nome or '').strip()
            if not nome_base:
                continue

            chave_nome = nome_base.lower()
            perfil = perfis_existentes.get(chave_nome)
            if not perfil:
                perfil = PerfilAcesso(
                    nome=nome_base,
                    descricao=funcao.descricao,
                    permissoes_padrao=_serializar_paginas_json(paginas),
                    ativo=funcao.ativo,
                )
                db.session.add(perfil)
                db.session.flush()
                perfis_existentes[chave_nome] = perfil
                mudou = True
            elif not perfil.permissoes_padrao:
                perfil.permissoes_padrao = _serializar_paginas_json(paginas)
                if not perfil.descricao and funcao.descricao:
                    perfil.descricao = funcao.descricao
                mudou = True

            perfis_criados[chave_nome] = perfil

        if perfis_criados:
            funcionarios_sem_perfil = Funcionario.query.filter(
                Funcionario.perfil_acesso_id.is_(None),
                Funcionario.cargo.isnot(None)
            ).all()
            for funcionario in funcionarios_sem_perfil:
                chave_cargo = (funcionario.cargo or '').strip().lower()
                perfil = perfis_criados.get(chave_cargo)
                if not perfil:
                    continue
                funcionario.perfil_acesso_id = perfil.id
                if funcionario.role != 'admin':
                    funcionario.controle_acesso_ativo = True
                mudou = True

        if mudou:
            db.session.commit()
    except OperationalError:
        db.session.rollback()
    except Exception:
        db.session.rollback()
        raise


def _bootstrap_admin_configurado():
    return bool(PRIMEIRO_ACESSO_EMAIL and PRIMEIRO_ACESSO_SENHA)


def _garantir_admin_primeiro_acesso():
    try:
        if Funcionario.query.count() > 0:
            return
        if not _bootstrap_admin_configurado():
            app.logger.warning(
                'Nenhum usuario encontrado e bootstrap admin nao configurado. '
                'Defina SYSTEMLR_BOOTSTRAP_ADMIN_PASSWORD para criar o primeiro acesso.'
            )
            return
        administrador = Funcionario(
            nome=PRIMEIRO_ACESSO_NOME,
            email=PRIMEIRO_ACESSO_EMAIL,
            role='admin',
            cargo='Administrador',
            departamento='Diretoria',
            time_nome='Gestao',
            nivel_organograma='Diretoria',
            ativo=True,
            controle_acesso_ativo=False,
            permitir_editar_imagem_perfil=True,
            senha_provisoria=True,
        )
        administrador.set_password(PRIMEIRO_ACESSO_SENHA)
        db.session.add(administrador)
        db.session.flush()
        administrador.numero_cadastro = _gerar_numero_cadastro_unico(administrador)
        administrador.matricula = _gerar_matricula_unica(administrador)
        db.session.commit()
    except OperationalError:
        db.session.rollback()
    except Exception:
        db.session.rollback()
        raise


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
    if not inspector.has_table('perfis_acesso'):
        PerfilAcesso.__table__.create(bind=db.engine, checkfirst=True)
    if inspector.has_table('funcionarios'):
        colunas_funcionarios = {col['name'] for col in inspector.get_columns('funcionarios')}
        if 'superior_id' not in colunas_funcionarios:
            try:
                db.session.execute(text('ALTER TABLE funcionarios ADD COLUMN superior_id INTEGER'))
                db.session.commit()
            except Exception:
                db.session.rollback()
        colunas_novas_funcionarios = {
            'numero_cadastro': 'INTEGER',
            'matricula': 'VARCHAR(30)',
            'cpf': 'VARCHAR(14)',
            'rg': 'VARCHAR(20)',
            'data_nascimento': 'DATE',
            'celular': 'VARCHAR(30)',
            'cep': 'VARCHAR(12)',
            'endereco': 'VARCHAR(180)',
            'bairro': 'VARCHAR(100)',
            'cidade': 'VARCHAR(100)',
            'estado': 'VARCHAR(2)',
            'imagem_perfil_path': 'VARCHAR(255)',
            'permitir_editar_imagem_perfil': 'INTEGER DEFAULT 0',
            'senha_provisoria': 'INTEGER DEFAULT 0',
            'departamento': 'VARCHAR(80)',
            'time_nome': 'VARCHAR(80)',
            'nivel_organograma': 'VARCHAR(40)',
            'pagina_inicial': "VARCHAR(30) DEFAULT 'dashboard'",
            'receber_alertas': 'INTEGER DEFAULT 1',
            'restricao_estoques_ativa': 'INTEGER DEFAULT 0',
            'estoque_principal_id': 'INTEGER',
            'perfil_acesso_id': 'INTEGER',
        }
        for coluna_nome, definicao in colunas_novas_funcionarios.items():
            if coluna_nome in colunas_funcionarios:
                continue
            try:
                db.session.execute(text(f'ALTER TABLE funcionarios ADD COLUMN {coluna_nome} {definicao}'))
                db.session.commit()
            except Exception:
                db.session.rollback()
    if inspector.has_table('permissoes_acesso'):
        colunas_permissoes_acesso = {col['name'] for col in inspector.get_columns('permissoes_acesso')}
        if 'permitido' not in colunas_permissoes_acesso:
            try:
                db.session.execute(text('ALTER TABLE permissoes_acesso ADD COLUMN permitido INTEGER DEFAULT 1'))
                db.session.commit()
            except Exception:
                db.session.rollback()
    if inspector.has_table('estoques'):
        colunas_estoques = {col['name'] for col in inspector.get_columns('estoques')}
        colunas_novas_estoques = {
            'codigo_filial': 'VARCHAR(20)',
        }
        for coluna_nome, definicao in colunas_novas_estoques.items():
            if coluna_nome in colunas_estoques:
                continue
            try:
                db.session.execute(text(f'ALTER TABLE estoques ADD COLUMN {coluna_nome} {definicao}'))
                db.session.commit()
            except Exception:
                db.session.rollback()
    if inspector.has_table('empresa_config'):
        colunas_empresa = {col['name'] for col in inspector.get_columns('empresa_config')}
        colunas_novas_empresa = {
            'codigo_empresa': 'VARCHAR(20)',
            'favicon_path': 'VARCHAR(255)',
            'app_icon_path': 'VARCHAR(255)',
            'separacao_entrega_ativa': 'INTEGER DEFAULT 1',
            'emissao_etiqueta_entrega_ativa': 'INTEGER DEFAULT 1',
            'separacao_entrega_unir_vendas_off': 'INTEGER DEFAULT 0',
            'roteirizacao_entrega_ativa': 'INTEGER DEFAULT 1',
            'emissao_nota_entrega_ativa': 'INTEGER DEFAULT 1',
            'entrega_local_saida_padrao': 'VARCHAR(160)',
            'entrega_veiculo_padrao': 'VARCHAR(80)',
            'entrega_motorista_padrao': 'VARCHAR(120)',
            'entrega_horario_fechamento_roteirizacao': 'VARCHAR(5)',
            'entrega_veiculos_json': 'TEXT',
            'entrega_terceirizadas_json': 'TEXT',
            'entrega_regras_roteirizacao_json': 'TEXT',
            'servicos_tecnicos_ativos': 'INTEGER DEFAULT 0',
            'servico_montagem_instalacao_ativo': 'INTEGER DEFAULT 0',
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
            'pagamentos_pdv_json': 'TEXT',
            'pagamentos_ecommerce_json': 'TEXT',
            'integracoes_pdv_json': 'TEXT',
            'integracoes_ecommerce_json': 'TEXT',
            'reposicao_loja_fisica_ativa': 'INTEGER DEFAULT 1',
            'emissao_etiqueta_loja_ativa': 'INTEGER DEFAULT 1',
            'emissao_etiqueta_endereco_ativa': 'INTEGER DEFAULT 1',
        }
        for coluna_nome, definicao in colunas_novas_empresa.items():
            if coluna_nome in colunas_empresa:
                continue
            try:
                db.session.execute(text(f'ALTER TABLE empresa_config ADD COLUMN {coluna_nome} {definicao}'))
                db.session.commit()
            except Exception:
                db.session.rollback()
    if not inspector.has_table('funcionario_estoques'):
        funcionario_estoques.create(bind=db.engine, checkfirst=True)
    if inspector.has_table('pedidos'):
        colunas_pedidos = {col['name'] for col in inspector.get_columns('pedidos')}
        colunas_novas_pedidos = {
            'separacao_entrega_concluida': 'INTEGER DEFAULT 0',
            'separacao_entrega_em': 'DATETIME',
            'etiqueta_entrega_emitida_em': 'DATETIME',
            'rota_entrega': 'VARCHAR(120)',
            'ordem_rota': 'INTEGER',
            'local_saida': 'VARCHAR(160)',
            'veiculo_tipo': 'VARCHAR(80)',
            'veiculo_placa': 'VARCHAR(20)',
            'motorista_nome': 'VARCHAR(120)',
            'empresa_terceirizada': 'VARCHAR(150)',
            'nota_fiscal_numero': 'VARCHAR(60)',
            'nota_fiscal_chave': 'VARCHAR(120)',
            'nota_fiscal_emitida_em': 'DATETIME',
            'saiu_para_entrega_em': 'DATETIME',
            'entrega_concluida_em': 'DATETIME',
        }
        for coluna_nome, definicao in colunas_novas_pedidos.items():
            if coluna_nome in colunas_pedidos:
                continue
            try:
                db.session.execute(text(f'ALTER TABLE pedidos ADD COLUMN {coluna_nome} {definicao}'))
                db.session.commit()
            except Exception:
                db.session.rollback()
    if inspector.has_table('produtos'):
        colunas_produtos = {col['name'] for col in inspector.get_columns('produtos')}
        colunas_novas_produtos = {
            'tipo_movimentacao': "VARCHAR(20) DEFAULT 'manual'",
            'fora_picking': 'INTEGER DEFAULT 0',
            'prioridade_reabastecimento': 'INTEGER',
            'ultima_baixa_picking_em': 'DATETIME',
            'servico_montagem_disponivel': 'INTEGER DEFAULT 0',
            'servico_instalacao_disponivel': 'INTEGER DEFAULT 0',
        }
        for coluna_nome, definicao in colunas_novas_produtos.items():
            if coluna_nome in colunas_produtos:
                continue
            try:
                db.session.execute(text(f'ALTER TABLE produtos ADD COLUMN {coluna_nome} {definicao}'))
                db.session.commit()
            except Exception:
                db.session.rollback()
    if inspector.has_table('recebimentos_fornecedor'):
        colunas_recebimentos = {col['name'] for col in inspector.get_columns('recebimentos_fornecedor')}
        if 'tipo_recebimento' not in colunas_recebimentos:
            try:
                db.session.execute(
                    text(
                        "ALTER TABLE recebimentos_fornecedor "
                        "ADD COLUMN tipo_recebimento VARCHAR(40) DEFAULT 'compra_revenda'"
                    )
                )
                db.session.commit()
            except Exception:
                db.session.rollback()
        if 'recebedor_funcionario_id' not in colunas_recebimentos:
            try:
                db.session.execute(
                    text(
                        "ALTER TABLE recebimentos_fornecedor "
                        "ADD COLUMN recebedor_funcionario_id INTEGER"
                    )
                )
                db.session.commit()
            except Exception:
                db.session.rollback()
    _garantir_cargos_permanentes()
    _migrar_funcoes_legadas_para_perfis()
    if not inspector.has_table('clientes_publicos'):
        ClientePublico.__table__.create(bind=db.engine, checkfirst=True)
    if not inspector.has_table('lancamentos_financeiros'):
        LancamentoFinanceiro.__table__.create(bind=db.engine, checkfirst=True)
    if not inspector.has_table('fundos_solicitacoes'):
        FundoSolicitacao.__table__.create(bind=db.engine, checkfirst=True)
    if not inspector.has_table('equipamentos_movimentacao'):
        EquipamentoMovimentacao.__table__.create(bind=db.engine, checkfirst=True)
    if not inspector.has_table('manutencoes_equipamento'):
        ManutencaoEquipamento.__table__.create(bind=db.engine, checkfirst=True)
    if not inspector.has_table('ordens_servico'):
        OrdemServico.__table__.create(bind=db.engine, checkfirst=True)
    else:
        colunas_ordens_servico = {col['name'] for col in inspector.get_columns('ordens_servico')}
        colunas_novas_ordens_servico = {
            'pedido_id': 'INTEGER',
            'iniciado_em': 'DATETIME',
            'retorno_tecnico': 'TEXT',
        }
        for coluna_nome, definicao in colunas_novas_ordens_servico.items():
            if coluna_nome in colunas_ordens_servico:
                continue
            try:
                db.session.execute(text(f'ALTER TABLE ordens_servico ADD COLUMN {coluna_nome} {definicao}'))
                db.session.commit()
            except Exception:
                db.session.rollback()
    if not inspector.has_table('chamados_internos'):
        ChamadoInterno.__table__.create(bind=db.engine, checkfirst=True)
    if not inspector.has_table('almoxarifado_atribuicoes'):
        AlmoxarifadoAtribuicao.__table__.create(bind=db.engine, checkfirst=True)
    if not inspector.has_table('assistente_local_feedback'):
        AssistenteLocalFeedback.__table__.create(bind=db.engine, checkfirst=True)
    try:
        db.session.query(Produto).filter(
            Produto.imagem_path == 'img/placeholders/produto-sem-foto.svg'
        ).update(
            {Produto.imagem_path: 'img/placeholders/imgindisponivel.png'},
            synchronize_session=False
        )
        db.session.commit()
    except Exception:
        db.session.rollback()
    _garantir_admin_primeiro_acesso()


def _destino_interno_seguro(destino):
    texto = (destino or '').strip()
    if not texto:
        return None
    parsed = urlparse(texto)
    if parsed.scheme or parsed.netloc:
        host_atual = urlparse(request.host_url).netloc
        if parsed.netloc != host_atual:
            return None
        caminho = parsed.path or '/'
        if not caminho.startswith('/'):
            caminho = f'/{caminho}'
        return f'{caminho}?{parsed.query}' if parsed.query else caminho
    if not texto.startswith('/') or texto.startswith('//'):
        return None
    return texto


def _redirect_interno_seguro(destino, fallback):
    return redirect(_destino_interno_seguro(destino) or fallback)


def _normalizar_matricula(valor):
    return shared_normalizar_matricula(valor)


def _normalizar_numero_cadastro(valor):
    try:
        numero = int(valor)
    except (TypeError, ValueError):
        return None
    return numero if numero > 0 else None


def _normalizar_cpf(valor):
    return shared_validar_cpf(valor)


def _normalizar_estado(valor):
    estado = (valor or '').strip().upper()
    return estado[:2] if estado else None


def _normalizar_codigo_identificacao(valor, fallback=None, maxlen=12):
    codigo = re.sub(r'[^A-Z0-9]+', '', (valor or '').strip().upper())
    if not codigo:
        codigo = (fallback or '').strip().upper()
    return codigo[:maxlen] if codigo else None


def _estoques_permitidos_ids_funcionario(funcionario):
    if not funcionario:
        return None
    ids = set()
    if getattr(funcionario, 'estoque_principal_id', None):
        ids.add(funcionario.estoque_principal_id)
    for estoque in getattr(funcionario, 'estoques_permitidos', []) or []:
        if getattr(estoque, 'id', None):
            ids.add(estoque.id)
    return ids


def _codigo_filial_matricula(funcionario):
    estoque_principal = getattr(funcionario, 'estoque_principal', None)
    if not estoque_principal and funcionario:
        ids = _estoques_permitidos_ids_funcionario(funcionario) or set()
        if ids:
            estoque_principal = Estoque.query.filter(Estoque.id.in_(ids)).order_by(Estoque.nome.asc()).first()
    codigo_base = getattr(estoque_principal, 'codigo_filial', None) if estoque_principal else None
    return _normalizar_codigo_identificacao(codigo_base, fallback='GERAL', maxlen=10) or 'GERAL'


def _gerar_numero_cadastro_unico(funcionario):
    funcionario_id = getattr(funcionario, 'id', funcionario)
    numero_atual = _normalizar_numero_cadastro(getattr(funcionario, 'numero_cadastro', None))
    if numero_atual and not Funcionario.query.filter(
        Funcionario.numero_cadastro == numero_atual,
        Funcionario.id != funcionario_id,
    ).first():
        return numero_atual

    numero_base = _normalizar_numero_cadastro(getattr(funcionario, 'id', None))
    if numero_base and not Funcionario.query.filter(
        Funcionario.numero_cadastro == numero_base,
        Funcionario.id != funcionario_id,
    ).first():
        return numero_base

    maior_numero = db.session.query(db.func.max(Funcionario.numero_cadastro)).scalar() or 0
    candidata = max(maior_numero + 1, numero_base or 1)
    while Funcionario.query.filter(
        Funcionario.numero_cadastro == candidata,
        Funcionario.id != funcionario_id,
    ).first():
        candidata += 1
    return candidata


def _gerar_matricula_padrao(funcionario):
    numero_cadastro = _normalizar_numero_cadastro(getattr(funcionario, 'numero_cadastro', None))
    if not numero_cadastro:
        numero_cadastro = _gerar_numero_cadastro_unico(funcionario)
    return f'{_codigo_filial_matricula(funcionario)}-{numero_cadastro:06d}'


def _gerar_matricula_unica(funcionario):
    funcionario_id = getattr(funcionario, 'id', funcionario)
    matricula_base = _gerar_matricula_padrao(funcionario)
    if not Funcionario.query.filter(
        db.func.lower(Funcionario.matricula) == matricula_base.lower(),
        Funcionario.id != funcionario_id,
    ).first():
        return matricula_base
    sufixo = 1
    while True:
        candidata = f'{matricula_base}-{sufixo:02d}'
        existe = Funcionario.query.filter(
            db.func.lower(Funcionario.matricula) == candidata.lower(),
            Funcionario.id != funcionario_id,
        ).first()
        if not existe:
            return candidata
        sufixo += 1


def _garantir_matriculas_funcionarios():
    houve_mudanca = False
    for funcionario in Funcionario.query.order_by(Funcionario.id.asc()).all():
        numero_cadastro_atual = _normalizar_numero_cadastro(getattr(funcionario, 'numero_cadastro', None))
        numero_cadastro_esperado = _gerar_numero_cadastro_unico(funcionario)
        if numero_cadastro_atual != numero_cadastro_esperado:
            funcionario.numero_cadastro = numero_cadastro_esperado
            houve_mudanca = True
        matricula_atual = _normalizar_matricula(funcionario.matricula)
        matricula_esperada = _gerar_matricula_unica(funcionario)
        if matricula_atual != matricula_esperada:
            funcionario.matricula = matricula_esperada
            houve_mudanca = True
    if houve_mudanca:
        db.session.commit()


with app.app_context():
    try:
        _garantir_matriculas_funcionarios()
    except Exception:
        db.session.rollback()


def _role_para_cargo_padrao(role):
    mapa = {
        'admin': 'Administrador',
        'gerente': 'Gerente',
        'caixa': 'Caixa',
        'operador': 'Operador',
        'garcom': 'Garcom',
    }
    return mapa.get((role or '').strip().lower(), 'Operador')


def _role_para_nivel_organograma(role):
    mapa = {
        'admin': 'Diretoria',
        'gerente': 'Gerencia',
        'caixa': 'Operacao',
        'operador': 'Operacao',
        'garcom': 'Operacao',
    }
    return mapa.get((role or '').strip().lower(), 'Operacao')


def _deve_exigir_superior_hierarquico(role, nivel_organograma):
    role_normalizado = (role or '').strip().lower()
    nivel_normalizado = (nivel_organograma or '').strip().lower()
    if role_normalizado == 'admin':
        return False
    if nivel_normalizado == 'diretoria':
        return False
    return True


def _normalizar_campo_organograma(valor):
    texto = (valor or '').strip()
    return texto or None


def _listar_cadastros_organograma():
    departamentos = sorted({
        (f.departamento or '').strip()
        for f in Funcionario.query.filter(Funcionario.departamento.isnot(None)).all()
        if (f.departamento or '').strip()
    }, key=str.lower)
    times = sorted({
        (f.time_nome or '').strip()
        for f in Funcionario.query.filter(Funcionario.time_nome.isnot(None)).all()
        if (f.time_nome or '').strip()
    }, key=str.lower)
    return departamentos, times


def _primeiro_funcionario_id():
    primeiro = Funcionario.query.order_by(Funcionario.id.asc()).first()
    return primeiro.id if primeiro else None


def _listar_estoques_para_vinculo_funcionario():
    return Estoque.query.order_by(Estoque.nome.asc()).all()


def _resolver_vinculos_estoque_funcionario(request_obj):
    restricao_estoques_ativa = (request_obj.form.get('restricao_estoques_ativa') == 'on')
    estoque_principal_id = request_obj.form.get('estoque_principal_id', type=int)
    estoques_ids = set()
    for valor in request_obj.form.getlist('estoques_permitidos_ids'):
        try:
            estoques_ids.add(int(valor))
        except (TypeError, ValueError):
            continue

    if estoque_principal_id:
        estoques_ids.add(estoque_principal_id)

    estoques_cadastrados = _listar_estoques_para_vinculo_funcionario()
    estoques_por_id = {estoque.id: estoque for estoque in estoques_cadastrados}

    if estoque_principal_id and estoque_principal_id not in estoques_por_id:
        return None, 'Estoque principal inválido.'

    ids_invalidos = [estoque_id for estoque_id in estoques_ids if estoque_id not in estoques_por_id]
    if ids_invalidos:
        return None, 'Há estoques/lojas inválidos no cadastro do colaborador.'

    if restricao_estoques_ativa and not estoques_ids:
        return None, 'Selecione ao menos um estoque/loja quando a restrição de acesso estiver ativa.'

    estoques_permitidos = [
        estoques_por_id[estoque_id]
        for estoque_id in sorted(estoques_ids, key=lambda item: (estoques_por_id[item].nome or '').lower())
    ]
    return {
        'restricao_estoques_ativa': restricao_estoques_ativa,
        'estoque_principal': estoques_por_id.get(estoque_principal_id),
        'estoques_permitidos': estoques_permitidos,
    }, None


def _estoques_contexto_base_ids_funcionario(funcionario):
    if not funcionario or funcionario.role == 'admin' or not getattr(funcionario, 'restricao_estoques_ativa', False):
        return None
    return _estoques_permitidos_ids_funcionario(funcionario) or set()


def _estoques_contexto_disponiveis(funcionario, apenas_ativos=True):
    query = Estoque.query
    ids = _estoques_contexto_base_ids_funcionario(funcionario)
    if ids is not None:
        if not ids:
            return []
        query = query.filter(Estoque.id.in_(ids))
    if apenas_ativos:
        query = query.filter(Estoque.ativo.is_(True))
    return query.order_by(Estoque.nome.asc()).all()


def _estoque_contexto_selecionado_id(funcionario):
    valor = session.get('estoque_contexto_id')
    if valor in (None, '', 'all'):
        return None
    try:
        estoque_id = int(valor)
    except (TypeError, ValueError):
        session.pop('estoque_contexto_id', None)
        return None

    disponiveis_ids = {estoque.id for estoque in _estoques_contexto_disponiveis(funcionario)}
    if estoque_id not in disponiveis_ids:
        session.pop('estoque_contexto_id', None)
        return None
    return estoque_id


def _paginas_permitidas_para_funcionario(funcionario):
    return _paginas_efetivas_funcionario(funcionario)


def _paginas_ordenadas_menu():
    paginas_ordenadas_menu = []
    for secao_nome, secao_paginas in PAGINAS_SISTEMA_MENU_ORDEM:
        itens_secao = [
            (pagina_key, PAGINAS_SISTEMA[pagina_key])
            for pagina_key in secao_paginas
            if pagina_key in PAGINAS_SISTEMA
        ]
        if itens_secao:
            paginas_ordenadas_menu.append((secao_nome, itens_secao))
    return paginas_ordenadas_menu


def _tabela_existe(nome_tabela):
    try:
        return inspect(db.engine).has_table(nome_tabela)
    except Exception:
        return False


def _extrair_permissoes_padrao_form():
    paginas_enviadas = set(request.form.getlist('paginas'))
    paginas_validas = set(PAGINAS_SISTEMA.keys())
    permissoes_padrao = set(paginas_enviadas.intersection(paginas_validas))

    setores_totais = set(request.form.getlist('setores_totais'))
    for secao_nome, itens in _paginas_ordenadas_menu():
        if secao_nome in setores_totais:
            permissoes_padrao.update(pagina_key for pagina_key, _ in itens)

    return sorted(permissoes_padrao)


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

    return pagina in _paginas_efetivas_funcionario(funcionario)


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


def _normalizar_horario_hhmm(valor):
    texto = (valor or '').strip()
    if not texto:
        return None
    if not re.fullmatch(r'\d{2}:\d{2}', texto):
        return None
    try:
        hora_txt, minuto_txt = texto.split(':', 1)
        hora = int(hora_txt)
        minuto = int(minuto_txt)
    except (TypeError, ValueError):
        return None
    if hora < 0 or hora > 23 or minuto < 0 or minuto > 59:
        return None
    return f'{hora:02d}:{minuto:02d}'


def _humanizar_rotulo_endpoint(valor):
    partes = [parte for parte in str(valor or '').split('_') if parte]
    if not partes:
        return 'Tela Atual'
    rotulo = ' '.join(partes).title()
    substituicoes = {
        'Pdv': 'PDV',
        'Rh': 'RH',
        'Cd': 'CD',
        'Ids': 'IDs',
        'Api': 'API',
        'Qr': 'QR',
    }
    for origem, destino in substituicoes.items():
        rotulo = rotulo.replace(origem, destino)
    return rotulo


def _titulo_tela_atual():
    endpoint = (request.endpoint or '').split('.')[-1]
    if not endpoint:
        return None, None

    pagina = ENDPOINT_TO_PAGINA.get(endpoint)
    secao_menu = None
    if pagina:
        for secao_nome, secao_paginas in PAGINAS_SISTEMA_MENU_ORDEM:
            if pagina in secao_paginas:
                secao_menu = secao_nome
                break

    titulos_especiais = {
        'dashboard': 'Meu Perfil',
        'boas_vindas': 'Home Operacional',
        'gestao_negocio': 'Central do Negócio',
        'financeiro': 'Visão Financeira',
        'financeiro_lancamentos': 'Lançamentos Financeiros',
        'financeiro_fundos': 'Gestão Monetária e Fundos',
        'pdv': 'PDV',
        'configurar_ecommerce': 'Tema e Loja Online',
        'configurar_ativacao_ecommerce': 'Ativação da Loja',
        'central_expedicao': 'Central de Expedição',
        'frota_expedicao': 'Frota Própria e Terceiros',
        'listar_separacao_entrega': 'Separação e Entrega',
        'listar_roteirizacao_entrega': 'Roteirização',
        'painel_expedicao': 'Painel em Tempo Real',
        'listar_transferencias_estoque': 'Histórico de Transferências',
        'transferir_armazenamento': 'Nova Transferência entre Lojas e CDs',
        'listar_movimentacoes': 'Entradas e Saídas Internas',
        'nova_movimentacao': 'Nova Entrada ou Saída Interna',
        'movimentacao_rapida': 'Movimentação Rápida Interna',
        'listar_almoxarifado': 'Central de Almoxarifado',
        'nova_atribuicao_almoxarifado': 'Nova Atribuição de Almoxarifado',
        'listar_recebimentos_fornecedor': 'Central de Recebimentos',
        'novo_recebimento_fornecedor': 'Novo Recebimento',
        'conferir_recebimento_fornecedor': 'Conferir Recebimento',
        'armazenar_recebimento_fornecedor': 'Armazenar Recebimento',
        'listar_funcoes_rh': 'Cargos',
        'listar_perfis_rh': 'Perfis de Acesso',
        'central_ajuda': 'Guia do Sistema',
        'detalhe_ajuda': 'Ajuda',
        'login': 'Login',
        'registro': 'Registro',
    }
    if endpoint in titulos_especiais:
        return secao_menu, titulos_especiais[endpoint]

    prefixos = (
        ('listar_', ''),
        ('novo_', 'Novo '),
        ('nova_', 'Nova '),
        ('criar_', 'Criar '),
        ('editar_', 'Editar '),
        ('deletar_', 'Excluir '),
        ('detalhes_', 'Detalhes de '),
        ('detalhe_', 'Detalhe de '),
        ('visualizar_', 'Visualizar '),
        ('configurar_', 'Configurar '),
        ('organograma_', 'Organograma '),
        ('indicadores_', 'Indicadores '),
        ('historico_', 'Histórico de '),
        ('abrir_', 'Abrir '),
        ('fechar_', 'Fechar '),
        ('imprimir_', 'Imprimir '),
        ('preview_', 'Preview '),
    )
    for prefixo, inicio in prefixos:
        if endpoint.startswith(prefixo):
            return secao_menu, f'{inicio}{_humanizar_rotulo_endpoint(endpoint[len(prefixo):])}'.strip()

    if pagina and pagina in PAGINAS_SISTEMA:
        return secao_menu, PAGINAS_SISTEMA[pagina]
    return secao_menu, _humanizar_rotulo_endpoint(endpoint)


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


def _normalizar_linhas_configuracao(valor_texto, tamanho_max=200):
    linhas = []
    for linha in (valor_texto or '').splitlines():
        item = linha.strip()
        if not item:
            continue
        if len(item) > tamanho_max:
            item = item[:tamanho_max]
        linhas.append(item)
    return linhas


def _parse_datetime_local(valor):
    valor = (valor or '').strip()
    if not valor:
        return None
    try:
        return datetime.strptime(valor, '%Y-%m-%dT%H:%M')
    except ValueError:
        return None


def _parse_date_iso(valor):
    return shared_validar_data(valor)


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


# ============ ROTAS - AUTENTICACAO ============

register_auth_routes(app, {
    'login_required': login_required,
    '_limit': _limit,
    '_client_ip': _client_ip,
    '_is_login_rate_limited': _is_login_rate_limited,
    '_register_login_attempt': _register_login_attempt,
    'get_funcionario_logado': get_funcionario_logado,
    '_normalizar_texto': _normalizar_texto,
    '_normalizar_matricula': _normalizar_matricula,
    '_normalizar_cpf': _normalizar_cpf,
    '_normalizar_estado': _normalizar_estado,
    '_normalizar_campo_organograma': _normalizar_campo_organograma,
    '_parse_date_iso': _parse_date_iso,
    '_role_para_cargo_padrao': _role_para_cargo_padrao,
    '_role_para_nivel_organograma': _role_para_nivel_organograma,
    '_gerar_numero_cadastro_unico': _gerar_numero_cadastro_unico,
    '_gerar_matricula_unica': _gerar_matricula_unica,
    '_listar_cadastros_organograma': _listar_cadastros_organograma,
    'sincronizar_garcom_funcionario': sincronizar_garcom_funcionario,
    'registrar_evento_auditoria': registrar_evento_auditoria,
    '_bootstrap_admin_configurado': _bootstrap_admin_configurado,
    'PRIMEIRO_ACESSO_EMAIL': PRIMEIRO_ACESSO_EMAIL,
    'ROLES_PERMITIDOS': ROLES_PERMITIDOS,
    'NIVEIS_ORGANOGRAMA': NIVEIS_ORGANOGRAMA,
    'extensions': extensions,
})


@app.route('/operacao/contexto-filial', methods=['POST'])
@login_required
def atualizar_contexto_filial():
    funcionario = get_funcionario_logado()
    valor = (request.form.get('estoque_contexto_id') or '').strip().lower()
    destino = request.form.get('next') or request.referrer

    if valor in ('', 'all', 'tudo'):
        session.pop('estoque_contexto_id', None)
        return _redirect_interno_seguro(destino, url_for('boas_vindas'))

    try:
        estoque_id = int(valor)
    except (TypeError, ValueError):
        session.pop('estoque_contexto_id', None)
        flash('Selecione uma filial/estoque valido.', 'warning')
        return _redirect_interno_seguro(destino, url_for('boas_vindas'))

    estoques_disponiveis = {estoque.id for estoque in _estoques_contexto_disponiveis(funcionario)}
    if estoque_id not in estoques_disponiveis:
        session.pop('estoque_contexto_id', None)
        flash('A filial/estoque selecionado nao esta disponivel para este colaborador.', 'warning')
        return _redirect_interno_seguro(destino, url_for('boas_vindas'))

    session['estoque_contexto_id'] = estoque_id
    return _redirect_interno_seguro(destino, url_for('boas_vindas'))


# ============ ROTAS - SISTEMA ============

@app.route('/')
def index():
    empresa = EmpresaConfig.query.first()
    if empresa and empresa.ecommerce_ativo is False:
        if session.get('funcionario_id'):
            return redirect(url_for('boas_vindas'))
        return redirect(url_for('login'))
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


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    funcionario = get_funcionario_logado()
    if not funcionario:
        flash('Sessao invalida. Faca login novamente.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        acao = (request.form.get('acao') or '').strip().lower()
        if acao == 'atualizar_perfil':
            remover_imagem_perfil = (request.form.get('remover_imagem_perfil') == 'on')
            arquivo_imagem = request.files.get('imagem_perfil')
            novo_imagem_perfil_path = None

            if (arquivo_imagem and arquivo_imagem.filename) or remover_imagem_perfil:
                if not funcionario.permitir_editar_imagem_perfil:
                    flash('Seu perfil nao possui permissao para alterar a imagem.', 'danger')
                    return redirect(url_for('dashboard'))

            imagem_anterior = funcionario.imagem_perfil_path
            allowed_ext = {'.png', '.jpg', '.jpeg', '.webp', '.gif'}
            if arquivo_imagem and arquivo_imagem.filename:
                _, ext = os.path.splitext(arquivo_imagem.filename.lower())
                if ext not in allowed_ext:
                    flash('Formato de imagem invalido. Use PNG, JPG, JPEG, WEBP ou GIF.', 'danger')
                    return redirect(url_for('dashboard'))
                nome_base = secure_filename((funcionario.nome or f'usuario_{funcionario.id}').strip()) or f'usuario_{funcionario.id}'
                relative_dir = os.path.join('uploads', 'usuarios')
                absolute_dir = os.path.join(app.static_folder, relative_dir)
                os.makedirs(absolute_dir, exist_ok=True)
                image_name = f'{nome_base}_{funcionario.id}_perfil{ext}'
                novo_imagem_perfil_path = os.path.join(relative_dir, image_name).replace('\\', '/')
                absolute_path = os.path.join(app.static_folder, novo_imagem_perfil_path)
                arquivo_imagem.save(absolute_path)
                funcionario.imagem_perfil_path = novo_imagem_perfil_path
            elif remover_imagem_perfil:
                funcionario.imagem_perfil_path = None

            funcionario.numero_cadastro = funcionario.numero_cadastro or _gerar_numero_cadastro_unico(funcionario)
            funcionario.matricula = funcionario.matricula or _gerar_matricula_unica(funcionario)
            db.session.commit()
            if novo_imagem_perfil_path and imagem_anterior and imagem_anterior != novo_imagem_perfil_path:
                caminho_anterior = os.path.join(app.static_folder, imagem_anterior)
                if os.path.exists(caminho_anterior):
                    os.remove(caminho_anterior)
            if remover_imagem_perfil and imagem_anterior:
                caminho_anterior = os.path.join(app.static_folder, imagem_anterior)
                if os.path.exists(caminho_anterior):
                    os.remove(caminho_anterior)
            flash('Perfil atualizado com sucesso.', 'success')
            return redirect(url_for('dashboard'))

        if acao == 'atualizar_senha':
            senha_atual = request.form.get('senha_atual', '')
            nova_senha = request.form.get('nova_senha', '')
            confirmacao_senha = request.form.get('confirmacao_senha', '')

            if not senha_atual or not nova_senha:
                flash('Informe senha atual e nova senha.', 'danger')
                return redirect(url_for('dashboard'))
            if not funcionario.check_password(senha_atual):
                flash('Senha atual invalida.', 'danger')
                return redirect(url_for('dashboard'))
            if len(nova_senha) < 6:
                flash('A nova senha deve ter no minimo 6 caracteres.', 'danger')
                return redirect(url_for('dashboard'))
            if nova_senha != confirmacao_senha:
                flash('Confirmacao de senha nao confere.', 'danger')
                return redirect(url_for('dashboard'))

            funcionario.set_password(nova_senha)
            funcionario.senha_provisoria = False
            db.session.commit()
            flash('Senha alterada com sucesso.', 'success')
            return redirect(url_for('dashboard'))

        if acao == 'atualizar_preferencias':
            receber_alertas = request.form.get('receber_alertas') == 'on'
            funcionario.receber_alertas = receber_alertas
            db.session.commit()
            flash('Preferencias salvas com sucesso.', 'success')
            return redirect(url_for('dashboard'))

        flash('Acao de configuracao invalida.', 'danger')
        return redirect(url_for('dashboard'))

    agora = datetime.utcnow()
    hora_atual = agora.hour
    if hora_atual < 12:
        saudacao = 'Bom dia'
    elif hora_atual < 18:
        saudacao = 'Boa tarde'
    else:
        saudacao = 'Boa noite'

    atividades_recentes = AuditoriaEvento.query.filter(
        AuditoriaEvento.funcionario_id == funcionario.id
    ).order_by(AuditoriaEvento.criado_em.desc()).limit(8).all()

    paginas_liberadas = len(_paginas_efetivas_funcionario(funcionario))

    alertas_usuario = []
    if funcionario.receber_alertas:
        if not (funcionario.matricula or '').strip():
            alertas_usuario.append('Defina sua matricula para rastreabilidade no RH.')
        if not (funcionario.cpf or '').strip():
            alertas_usuario.append('Cadastre seu CPF para completar os dados pessoais.')
        if not (funcionario.celular or '').strip():
            alertas_usuario.append('Cadastre seu celular para facilitar contato operacional.')
        if not (funcionario.endereco or '').strip():
            alertas_usuario.append('Complete seu endereco para manter o cadastro atualizado.')
        if not (funcionario.departamento or '').strip():
            alertas_usuario.append('Informe seu departamento para manter o organograma atualizado.')
        if not (funcionario.time_nome or '').strip():
            alertas_usuario.append('Informe seu time/squad para relatórios de RH e produtividade.')
    if not alertas_usuario:
        alertas_usuario.append('Nenhuma pendencia pessoal critica no momento.')

    secoes_acesso = []
    paginas_permitidas = _paginas_permitidas_para_funcionario(funcionario)
    for secao_nome, secao_paginas in PAGINAS_SISTEMA_MENU_ORDEM:
        paginas = [
            PAGINAS_SISTEMA.get(pagina_key, pagina_key)
            for pagina_key in secao_paginas
            if pagina_key in paginas_permitidas and pagina_key in PAGINAS_SISTEMA
        ]
        if paginas:
            secoes_acesso.append({'secao': secao_nome, 'paginas': paginas})

    return render_template(
        'dashboard/index.html',
        funcionario=funcionario,
        saudacao=saudacao,
        data_hora_atual=agora,
        paginas_liberadas=paginas_liberadas,
        total_alertas=len(alertas_usuario),
        alertas_usuario=alertas_usuario,
        atividades_recentes=atividades_recentes,
        secoes_acesso=secoes_acesso,
    )


@app.route('/gestao-negocio')
@require_role('admin', 'gerente')
def gestao_negocio():
    empresa = EmpresaConfig.query.first()
    total_funcionarios = Funcionario.query.count()
    funcionarios_ativos = Funcionario.query.filter_by(ativo=True).count()
    produtos_ativos = Produto.query.filter_by(ativo=True).count()
    categorias_total = Categoria.query.count()
    caixas_abertas = Caixa.query.filter_by(aberto=True).count()
    cargos_rh_ativos = FuncaoRH.query.filter_by(ativo=True).count()
    perfis_acesso_ativos = PerfilAcesso.query.filter_by(ativo=True).count()
    pedidos_abertos = Pedido.query.filter(Pedido.status.in_(['aberto', 'em_preparo', 'entregue'])).count()
    pendencias_armazenagem = RecebimentoFornecedor.query.filter_by(
        status=RecebimentoFornecedor.STATUS_AGUARDANDO_ARMAZENAGEM
    ).count()
    recebimento_armazenagem_mais_antigo = RecebimentoFornecedor.query.filter_by(
        status=RecebimentoFornecedor.STATUS_AGUARDANDO_ARMAZENAGEM
    ).order_by(
        RecebimentoFornecedor.conferido_em.asc(),
        RecebimentoFornecedor.criado_em.asc(),
    ).first()
    if recebimento_armazenagem_mais_antigo:
        referencia_pendencia_armazenagem = (
            recebimento_armazenagem_mais_antigo.conferido_em
            or recebimento_armazenagem_mais_antigo.criado_em
        )
        detalhe_pendencia_armazenagem = (
            f'{pendencias_armazenagem} recebimento(s) aguardando armazenagem. '
            f'Mais antigo desde {referencia_pendencia_armazenagem.strftime("%d/%m/%Y %H:%M")}.'
        )
    else:
        detalhe_pendencia_armazenagem = 'Nenhum recebimento aguardando armazenagem.'

    checklist_config = [
        {
            'titulo': 'Dados principais da empresa',
            'ok': bool(empresa and (empresa.nome_fantasia or '').strip()),
            'detalhe_ok': 'Cadastro principal preenchido.',
            'detalhe_pendente': 'Defina nome fantasia e dados da empresa.',
            'url': url_for('editar_empresa'),
            'acao': 'Configurar empresa',
        },
        {
            'titulo': 'Canal de operacao e entrega',
            'ok': bool(empresa and empresa.canal_operacao and empresa.separacao_entrega_ativa is not False),
            'detalhe_ok': 'Canal e fluxo de entrega ativos.',
            'detalhe_pendente': 'Revise canal de operacao e habilite separacao/entrega.',
            'url': url_for('editar_empresa') + '#config-entrega',
            'acao': 'Revisar operacao',
        },
        {
            'titulo': 'Ativacao do e-commerce',
            'ok': bool(empresa and empresa.ecommerce_ativo is not False),
            'detalhe_ok': 'Loja online liberada para operacao.',
            'detalhe_pendente': 'Habilite a loja online antes de divulgar o canal para clientes.',
            'url': url_for('configurar_ativacao_ecommerce'),
            'acao': 'Ativar loja online',
        },
        {
            'titulo': 'Tema e identidade visual da loja',
            'ok': bool(empresa and (getattr(empresa, 'ecom_titulo_banner', None) or '').strip()),
            'detalhe_ok': 'Tema, banners e comunicacao principal definidos.',
            'detalhe_pendente': 'Ajuste tema, banner, promocoes e identidade da vitrine.',
            'url': url_for('configurar_ecommerce'),
            'acao': 'Configurar visual da loja',
        },
        {
            'titulo': 'Cargos e perfis de acesso',
            'ok': cargos_rh_ativos > 0 and perfis_acesso_ativos > 0,
            'detalhe_ok': f'{cargos_rh_ativos} cargo(s) e {perfis_acesso_ativos} perfil(is) ativo(s).',
            'detalhe_pendente': 'Cadastre cargos da empresa e perfis de acesso padrao para a equipe.',
            'url': url_for('listar_funcoes_rh'),
            'acao': 'Configurar RH',
        },
        {
            'titulo': 'Equipe cadastrada',
            'ok': funcionarios_ativos > 0,
            'detalhe_ok': f'{funcionarios_ativos} colaborador(es) ativo(s).',
            'detalhe_pendente': 'Cadastre colaboradores e niveis da hierarquia.',
            'url': url_for('listar_funcionarios'),
            'acao': 'Gerir funcionarios',
        },
        {
            'titulo': 'Pendencias de armazenagem',
            'ok': pendencias_armazenagem == 0,
            'detalhe_ok': 'Fila de armazenagem em dia.',
            'detalhe_pendente': detalhe_pendencia_armazenagem,
            'url': url_for(
                'listar_recebimentos_fornecedor',
                status=RecebimentoFornecedor.STATUS_AGUARDANDO_ARMAZENAGEM,
            ),
            'acao': 'Abrir fila de armazenagem',
        },
    ]
    pendencias_criticas = [item for item in checklist_config if not item['ok']]

    atalhos_dono = [
        {'titulo': 'Configuracoes da Empresa', 'descricao': 'Dados, operacao, entrega e servicos.', 'url': url_for('editar_empresa')},
        {'titulo': 'Ativacao da Loja Online', 'descricao': 'Liga ou desliga a vitrine publica do e-commerce.', 'url': url_for('configurar_ativacao_ecommerce')},
        {'titulo': 'Tema e Loja Online', 'descricao': 'Cores, banners, promocoes, checkout e rodape.', 'url': url_for('configurar_ecommerce')},
        {'titulo': 'Cargos da Equipe', 'descricao': 'Estrutura organizacional usada nos cadastros e no organograma.', 'url': url_for('listar_funcoes_rh')},
        {'titulo': 'Perfis de Acesso', 'descricao': 'Conjuntos padrao de paginas para aplicar por colaborador.', 'url': url_for('listar_perfis_rh')},
        {'titulo': 'Central de Expedicao', 'descricao': 'Separacao, rotas, etiquetas e frota.', 'url': url_for('central_expedicao')},
        {'titulo': 'Lancamentos Financeiros', 'descricao': 'Controle monetario e exportacao contabil.', 'url': url_for('financeiro_lancamentos')},
        {'titulo': 'Guia do Sistema', 'descricao': 'Passo a passo para equipe e lideres.', 'url': url_for('central_ajuda')},
    ]

    return render_template(
        'sistema/gestao_negocio.html',
        empresa=empresa,
        total_funcionarios=total_funcionarios,
        funcionarios_ativos=funcionarios_ativos,
        produtos_ativos=produtos_ativos,
        categorias_total=categorias_total,
        caixas_abertas=caixas_abertas,
        pedidos_abertos=pedidos_abertos,
        pendencias_armazenagem=pendencias_armazenagem,
        detalhe_pendencia_armazenagem=detalhe_pendencia_armazenagem,
        checklist_config=checklist_config,
        pendencias_criticas=pendencias_criticas,
        atalhos_dono=atalhos_dono,
    )


@app.route('/financeiro')
@login_required
def financeiro():
    inicio_periodo, fim_periodo, data_inicial_str, data_final_str = _parse_date_range(
        request.args.get('data_inicial'),
        request.args.get('data_final'),
        default_days=7
    )
    analytics = _coletar_dashboard_analytics(inicio_periodo, fim_periodo)

    return render_template(
        'financeiro/index.html',
        periodo_dias=analytics['periodo_dias'],
        data_inicial=data_inicial_str,
        data_final=data_final_str,
        pedidos_periodo_total=analytics['pedidos_periodo_total'],
        faturamento_periodo=analytics['faturamento_periodo'],
        faturamento_periodo_anterior=analytics['faturamento_periodo_anterior'],
        crescimento_receita_pct=analytics['crescimento_receita_pct'],
        faturamento_hoje=analytics['faturamento_hoje'],
        receita_media_dia=analytics['receita_media_dia'],
        pedidos_media_dia=analytics['pedidos_media_dia'],
        ticket_medio_periodo=analytics['ticket_medio_periodo'],
        cmv_periodo=analytics['cmv_periodo'],
        lucro_bruto_periodo=analytics['lucro_bruto_periodo'],
        margem_bruta_pct=analytics['margem_bruta_pct'],
        despesas_operacionais_periodo=analytics['despesas_operacionais_periodo'],
        ajustes_financeiros_periodo=analytics['ajustes_financeiros_periodo'],
        resultado_operacional_periodo=analytics['resultado_operacional_periodo'],
        margem_operacional_pct=analytics['margem_operacional_pct'],
        pedidos_abertos=analytics['pedidos_abertos'],
        pedidos_cancelados_periodo=analytics['pedidos_cancelados_periodo'],
        valor_cancelado_periodo=analytics['valor_cancelado_periodo'],
        taxa_cancelamento_pct=analytics['taxa_cancelamento_pct'],
        metodo_mais_usado=analytics['metodo_mais_usado'],
        concentracao_top_pagamento_pct=analytics['concentracao_top_pagamento_pct'],
        vendas_periodo=analytics['vendas_periodo'],
        top_produtos_vendidos=analytics['top_produtos_vendidos'],
        pedidos_por_status=analytics['pedidos_por_status'],
        top_clientes=analytics['top_clientes'],
        desempenho_garcons=analytics['desempenho_garcons'],
        desempenho_caixas=analytics['desempenho_caixas'],
        metodos_pagamento=analytics['metodos_pagamento']
    )


@app.route('/financeiro/fundos', methods=['GET', 'POST'])
@require_role('admin', 'gerente', 'caixa')
def financeiro_fundos():
    funcionario = get_funcionario_logado()
    if request.method == 'POST':
        acao = (request.form.get('acao') or 'solicitar').strip().lower()
        fundo_id = request.form.get('fundo_id', type=int)

        if acao == 'solicitar':
            tipo = (request.form.get('tipo') or '').strip().lower()
            descricao = (request.form.get('descricao') or '').strip()
            categoria = (request.form.get('categoria') or '').strip() or None
            centro_custo = (request.form.get('centro_custo') or '').strip() or None
            referencia_documento = (request.form.get('referencia_documento') or '').strip() or None
            valor_texto = (request.form.get('valor') or '').strip().replace('.', '').replace(',', '.')
            try:
                valor = float(valor_texto)
            except Exception:
                valor = 0.0

            if tipo not in FundoSolicitacao.TIPOS_VALIDOS:
                flash('Tipo de fundo invalido.', 'danger')
                return redirect(url_for('financeiro_fundos'))
            if not descricao:
                flash('Descricao da solicitacao e obrigatoria.', 'danger')
                return redirect(url_for('financeiro_fundos'))
            if valor <= 0:
                flash('Valor deve ser maior que zero.', 'danger')
                return redirect(url_for('financeiro_fundos'))

            fundo = FundoSolicitacao(
                tipo=tipo,
                descricao=descricao,
                categoria=categoria,
                valor=valor,
                centro_custo=centro_custo,
                referencia_documento=referencia_documento,
                status=FundoSolicitacao.STATUS_SOLICITADA,
                solicitado_por_id=(funcionario.id if funcionario else None),
            )
            try:
                db.session.add(fundo)
                db.session.commit()
                flash(f'Solicitacao de fundo #{fundo.id} registrada.', 'success')
            except Exception as exc:
                db.session.rollback()
                flash(f'Erro ao registrar solicitacao: {str(exc)}', 'danger')
            return redirect(url_for('financeiro_fundos'))

        fundo = FundoSolicitacao.query.get_or_404(fundo_id)
        if acao == 'aprovar':
            if funcionario.role not in {'admin', 'gerente'}:
                flash('Somente admin/gerente pode aprovar solicitacoes.', 'danger')
                return redirect(url_for('financeiro_fundos'))
            if fundo.status != FundoSolicitacao.STATUS_SOLICITADA:
                flash('Apenas solicitacoes pendentes podem ser aprovadas.', 'warning')
                return redirect(url_for('financeiro_fundos'))
            fundo.status = FundoSolicitacao.STATUS_APROVADA
            fundo.aprovado_por_id = funcionario.id if funcionario else None
            fundo.aprovado_em = datetime.utcnow()
            db.session.commit()
            flash(f'Solicitacao #{fundo.id} aprovada.', 'success')
            return redirect(url_for('financeiro_fundos'))

        if acao == 'rejeitar':
            if funcionario.role not in {'admin', 'gerente'}:
                flash('Somente admin/gerente pode rejeitar solicitacoes.', 'danger')
                return redirect(url_for('financeiro_fundos'))
            if fundo.status != FundoSolicitacao.STATUS_SOLICITADA:
                flash('Apenas solicitacoes pendentes podem ser rejeitadas.', 'warning')
                return redirect(url_for('financeiro_fundos'))
            fundo.status = FundoSolicitacao.STATUS_REJEITADA
            fundo.aprovado_por_id = funcionario.id if funcionario else None
            fundo.aprovado_em = datetime.utcnow()
            fundo.motivo_rejeicao = (request.form.get('motivo_rejeicao') or '').strip() or None
            db.session.commit()
            flash(f'Solicitacao #{fundo.id} rejeitada.', 'warning')
            return redirect(url_for('financeiro_fundos'))

        if acao == 'liberar':
            if funcionario.role not in {'admin', 'gerente'}:
                flash('Somente admin/gerente pode liberar fundos.', 'danger')
                return redirect(url_for('financeiro_fundos'))
            if fundo.status not in {FundoSolicitacao.STATUS_APROVADA, FundoSolicitacao.STATUS_SOLICITADA}:
                flash('Somente solicitacao aprovada/presente pode ser liberada.', 'warning')
                return redirect(url_for('financeiro_fundos'))
            try:
                tipo_lanc = LancamentoFinanceiro.TIPO_RECEITA if fundo.tipo == FundoSolicitacao.TIPO_APORTE else LancamentoFinanceiro.TIPO_DESPESA
                lancamento = LancamentoFinanceiro(
                    tipo=tipo_lanc,
                    categoria=fundo.categoria or 'liberacao_fundos',
                    descricao=f'Liberacao de fundo #{fundo.id} - {fundo.descricao}',
                    valor=float(fundo.valor or 0.0),
                    data_competencia=datetime.utcnow().date(),
                    incluir_contabilidade=True,
                    referencia_documento=fundo.referencia_documento,
                    centro_custo=fundo.centro_custo,
                    criado_por_id=(funcionario.id if funcionario else None),
                )
                db.session.add(lancamento)
                db.session.flush()
                fundo.status = FundoSolicitacao.STATUS_LIBERADA
                if not fundo.aprovado_por_id:
                    fundo.aprovado_por_id = funcionario.id if funcionario else None
                    fundo.aprovado_em = datetime.utcnow()
                fundo.liberado_por_id = funcionario.id if funcionario else None
                fundo.liberado_em = datetime.utcnow()
                fundo.lancamento_financeiro_id = lancamento.id
                db.session.commit()
                flash(f'Fundo #{fundo.id} liberado e lancamento financeiro gerado.', 'success')
            except Exception as exc:
                db.session.rollback()
                flash(f'Erro ao liberar fundo: {str(exc)}', 'danger')
            return redirect(url_for('financeiro_fundos'))

    status_filtro = (request.args.get('status') or '').strip().lower()
    tipo_filtro = (request.args.get('tipo') or '').strip().lower()
    query = FundoSolicitacao.query.order_by(FundoSolicitacao.solicitado_em.desc())
    if status_filtro in FundoSolicitacao.STATUS_VALIDOS:
        query = query.filter(FundoSolicitacao.status == status_filtro)
    if tipo_filtro in FundoSolicitacao.TIPOS_VALIDOS:
        query = query.filter(FundoSolicitacao.tipo == tipo_filtro)
    fundos = query.limit(300).all()

    total_solicitado = sum(float(item.valor or 0.0) for item in fundos if item.status == FundoSolicitacao.STATUS_SOLICITADA)
    total_liberado = sum(float(item.valor or 0.0) for item in fundos if item.status == FundoSolicitacao.STATUS_LIBERADA)
    total_aprovado = sum(float(item.valor or 0.0) for item in fundos if item.status == FundoSolicitacao.STATUS_APROVADA)

    return render_template(
        'financeiro/fundos.html',
        fundos=fundos,
        status_validos=FundoSolicitacao.STATUS_VALIDOS,
        tipos_validos=FundoSolicitacao.TIPOS_VALIDOS,
        status_filtro=status_filtro,
        tipo_filtro=tipo_filtro,
        total_solicitado=total_solicitado,
        total_aprovado=total_aprovado,
        total_liberado=total_liberado,
    )


@app.route('/financeiro/lancamentos', methods=['GET', 'POST'])
@require_role('admin', 'gerente', 'caixa')
def financeiro_lancamentos():
    funcionario = get_funcionario_logado()
    if request.method == 'POST':
        tipo = (request.form.get('tipo') or '').strip().lower()
        descricao = (request.form.get('descricao') or '').strip()
        categoria = (request.form.get('categoria') or '').strip() or None
        referencia_documento = (request.form.get('referencia_documento') or '').strip() or None
        centro_custo = (request.form.get('centro_custo') or '').strip() or None
        data_competencia = _parse_date_iso(request.form.get('data_competencia')) or datetime.utcnow().date()
        incluir_contabilidade = (request.form.get('incluir_contabilidade') == 'on')

        if tipo not in LancamentoFinanceiro.TIPOS:
            flash('Tipo de lancamento invalido.', 'danger')
            return redirect(url_for('financeiro_lancamentos'))
        if not descricao:
            flash('Descricao e obrigatoria.', 'danger')
            return redirect(url_for('financeiro_lancamentos'))

        valor_texto = (request.form.get('valor') or '').strip().replace('.', '').replace(',', '.')
        valor = 0.0
        if valor_texto:
            try:
                valor = float(valor_texto)
            except ValueError:
                flash('Valor invalido.', 'danger')
                return redirect(url_for('financeiro_lancamentos'))

        produto = None
        produto_id = request.form.get('produto_id', type=int)
        quantidade = request.form.get('quantidade', type=float)
        if tipo == LancamentoFinanceiro.TIPO_CONSUMO_PROPRIO:
            if not produto_id:
                flash('Selecione um produto para consumo proprio.', 'danger')
                return redirect(url_for('financeiro_lancamentos'))
            produto = Produto.query.get(produto_id)
            if not produto:
                flash('Produto nao encontrado para consumo proprio.', 'danger')
                return redirect(url_for('financeiro_lancamentos'))
            if not quantidade or quantidade <= 0:
                flash('Informe quantidade valida para consumo proprio.', 'danger')
                return redirect(url_for('financeiro_lancamentos'))
            valor = round((produto.preco_custo or 0) * quantidade, 2)
        elif tipo in {LancamentoFinanceiro.TIPO_DESPESA, LancamentoFinanceiro.TIPO_RECEITA}:
            if valor <= 0:
                flash('Valor deve ser maior que zero.', 'danger')
                return redirect(url_for('financeiro_lancamentos'))
        elif tipo == LancamentoFinanceiro.TIPO_AJUSTE and valor == 0:
            flash('Ajuste deve ter valor diferente de zero.', 'danger')
            return redirect(url_for('financeiro_lancamentos'))

        novo = LancamentoFinanceiro(
            tipo=tipo,
            categoria=categoria,
            descricao=descricao,
            valor=valor,
            data_competencia=data_competencia,
            incluir_contabilidade=incluir_contabilidade,
            referencia_documento=referencia_documento,
            centro_custo=centro_custo,
            produto_id=(produto.id if produto else produto_id),
            quantidade=quantidade if quantidade and quantidade > 0 else None,
            criado_por_id=(funcionario.id if funcionario else None),
        )
        try:
            db.session.add(novo)
            db.session.commit()
            flash('Lancamento financeiro registrado com sucesso.', 'success')
        except Exception as exc:
            db.session.rollback()
            flash(f'Erro ao registrar lancamento: {str(exc)}', 'danger')
        return redirect(url_for('financeiro_lancamentos'))

    data_inicial_txt = (request.args.get('data_inicial') or '').strip()
    data_final_txt = (request.args.get('data_final') or '').strip()
    tipo_filtro = (request.args.get('tipo') or '').strip().lower()
    somente_contabilidade = (request.args.get('somente_contabilidade') == '1')

    data_inicial = _parse_date_iso(data_inicial_txt)
    data_final = _parse_date_iso(data_final_txt)

    query = LancamentoFinanceiro.query.order_by(
        LancamentoFinanceiro.data_competencia.desc(),
        LancamentoFinanceiro.criado_em.desc()
    )
    if data_inicial:
        query = query.filter(LancamentoFinanceiro.data_competencia >= data_inicial)
    if data_final:
        query = query.filter(LancamentoFinanceiro.data_competencia <= data_final)
    if tipo_filtro in LancamentoFinanceiro.TIPOS:
        query = query.filter(LancamentoFinanceiro.tipo == tipo_filtro)
    if somente_contabilidade:
        query = query.filter(LancamentoFinanceiro.incluir_contabilidade.is_(True))

    lancamentos = query.all()
    total_receitas = sum((item.valor or 0.0) for item in lancamentos if item.tipo == LancamentoFinanceiro.TIPO_RECEITA)
    total_despesas = sum(
        (item.valor or 0.0)
        for item in lancamentos
        if item.tipo in {LancamentoFinanceiro.TIPO_DESPESA, LancamentoFinanceiro.TIPO_CONSUMO_PROPRIO}
    )
    total_ajustes = sum((item.valor or 0.0) for item in lancamentos if item.tipo == LancamentoFinanceiro.TIPO_AJUSTE)
    saldo_periodo = total_receitas - total_despesas + total_ajustes

    produtos = Produto.query.filter_by(ativo=True).order_by(Produto.nome.asc()).all()
    return render_template(
        'financeiro/lancamentos.html',
        lancamentos=lancamentos,
        produtos=produtos,
        tipos_lancamento=LancamentoFinanceiro.TIPOS,
        data_inicial=data_inicial_txt,
        data_final=data_final_txt,
        tipo_filtro=tipo_filtro,
        somente_contabilidade=somente_contabilidade,
        total_receitas=total_receitas,
        total_despesas=total_despesas,
        total_ajustes=total_ajustes,
        saldo_periodo=saldo_periodo,
    )


@app.route('/financeiro/lancamentos/<int:lancamento_id>/marcar-enviado', methods=['POST'])
@require_role('admin', 'gerente')
def marcar_lancamento_enviado_contador(lancamento_id):
    lancamento = LancamentoFinanceiro.query.get_or_404(lancamento_id)
    try:
        lancamento.enviado_contador = True
        lancamento.enviado_em = datetime.utcnow()
        db.session.commit()
        flash('Lancamento marcado como enviado ao contador.', 'success')
    except Exception as exc:
        db.session.rollback()
        flash(f'Erro ao atualizar lancamento: {str(exc)}', 'danger')
    return redirect(url_for('financeiro_lancamentos'))


@app.route('/financeiro/lancamentos/exportar')
@require_role('admin', 'gerente', 'caixa')
def exportar_lancamentos_financeiros():
    data_inicial = _parse_date_iso(request.args.get('data_inicial'))
    data_final = _parse_date_iso(request.args.get('data_final'))
    tipo_filtro = (request.args.get('tipo') or '').strip().lower()
    somente_contabilidade = (request.args.get('somente_contabilidade', '1') == '1')

    query = LancamentoFinanceiro.query.order_by(
        LancamentoFinanceiro.data_competencia.asc(),
        LancamentoFinanceiro.id.asc()
    )
    if data_inicial:
        query = query.filter(LancamentoFinanceiro.data_competencia >= data_inicial)
    if data_final:
        query = query.filter(LancamentoFinanceiro.data_competencia <= data_final)
    if tipo_filtro in LancamentoFinanceiro.TIPOS:
        query = query.filter(LancamentoFinanceiro.tipo == tipo_filtro)
    if somente_contabilidade:
        query = query.filter(LancamentoFinanceiro.incluir_contabilidade.is_(True))

    output = io.StringIO()
    writer = csv.writer(output, delimiter=';')
    writer.writerow([
        'id',
        'data_competencia',
        'tipo',
        'categoria',
        'descricao',
        'valor',
        'produto_codigo',
        'produto_nome',
        'quantidade',
        'referencia_documento',
        'centro_custo',
        'incluir_contabilidade',
        'enviado_contador',
        'enviado_em',
        'criado_em',
    ])
    for item in query.all():
        writer.writerow([
            item.id,
            item.data_competencia.isoformat() if item.data_competencia else '',
            item.tipo,
            item.categoria or '',
            item.descricao or '',
            f'{(item.valor or 0.0):.2f}',
            item.produto.codigo if item.produto else '',
            item.produto.nome if item.produto else '',
            f'{item.quantidade:.3f}' if item.quantidade is not None else '',
            item.referencia_documento or '',
            item.centro_custo or '',
            'sim' if item.incluir_contabilidade else 'nao',
            'sim' if item.enviado_contador else 'nao',
            item.enviado_em.strftime('%Y-%m-%d %H:%M:%S') if item.enviado_em else '',
            item.criado_em.strftime('%Y-%m-%d %H:%M:%S') if item.criado_em else '',
        ])

    csv_content = output.getvalue()
    output.close()
    nome_arquivo = f'lancamentos_financeiros_{datetime.utcnow().strftime("%Y%m%d_%H%M%S")}.csv'
    return Response(
        csv_content,
        mimetype='text/csv; charset=utf-8',
        headers={'Content-Disposition': f'attachment; filename={nome_arquivo}'}
    )


@app.route('/financeiro/lancamentos/exportar-xlsx')
@require_role('admin', 'gerente', 'caixa')
def exportar_lancamentos_financeiros_xlsx():
    try:
        from openpyxl import Workbook
    except Exception:
        flash('Dependencia openpyxl nao instalada. Execute: pip install openpyxl', 'danger')
        return redirect(url_for('financeiro_lancamentos'))

    data_inicial = _parse_date_iso(request.args.get('data_inicial'))
    data_final = _parse_date_iso(request.args.get('data_final'))
    tipo_filtro = (request.args.get('tipo') or '').strip().lower()
    somente_contabilidade = (request.args.get('somente_contabilidade', '1') == '1')

    query = LancamentoFinanceiro.query.order_by(
        LancamentoFinanceiro.data_competencia.asc(),
        LancamentoFinanceiro.id.asc()
    )
    if data_inicial:
        query = query.filter(LancamentoFinanceiro.data_competencia >= data_inicial)
    if data_final:
        query = query.filter(LancamentoFinanceiro.data_competencia <= data_final)
    if tipo_filtro in LancamentoFinanceiro.TIPOS:
        query = query.filter(LancamentoFinanceiro.tipo == tipo_filtro)
    if somente_contabilidade:
        query = query.filter(LancamentoFinanceiro.incluir_contabilidade.is_(True))

    wb = Workbook()
    ws = wb.active
    ws.title = 'Lancamentos'
    ws.append([
        'id',
        'data_competencia',
        'tipo',
        'categoria',
        'descricao',
        'valor',
        'produto_codigo',
        'produto_nome',
        'quantidade',
        'referencia_documento',
        'centro_custo',
        'incluir_contabilidade',
        'enviado_contador',
        'enviado_em',
        'criado_em',
    ])
    for item in query.all():
        ws.append([
            item.id,
            item.data_competencia.isoformat() if item.data_competencia else '',
            item.tipo,
            item.categoria or '',
            item.descricao or '',
            float(item.valor or 0.0),
            item.produto.codigo if item.produto else '',
            item.produto.nome if item.produto else '',
            float(item.quantidade) if item.quantidade is not None else None,
            item.referencia_documento or '',
            item.centro_custo or '',
            'sim' if item.incluir_contabilidade else 'nao',
            'sim' if item.enviado_contador else 'nao',
            item.enviado_em.strftime('%Y-%m-%d %H:%M:%S') if item.enviado_em else '',
            item.criado_em.strftime('%Y-%m-%d %H:%M:%S') if item.criado_em else '',
        ])

    arquivo = io.BytesIO()
    wb.save(arquivo)
    arquivo.seek(0)
    nome_arquivo = f'lancamentos_financeiros_{datetime.utcnow().strftime("%Y%m%d_%H%M%S")}.xlsx'
    return Response(
        arquivo.getvalue(),
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': f'attachment; filename={nome_arquivo}'}
    )


@app.route('/empresa', methods=['GET', 'POST'])
@require_role('admin', 'gerente')
def editar_empresa():
    empresa = EmpresaConfig.query.first()

    if request.method == 'POST':
        novo_logo_path = None
        novo_favicon_empresa_path = None
        novo_app_icon_path = None
        logo_anterior = (empresa.logo_path if empresa else None)
        favicon_empresa_anterior = (empresa.favicon_path if empresa else None)
        app_icon_anterior = (empresa.app_icon_path if empresa else None)
        try:
            if not empresa:
                empresa = EmpresaConfig()
                db.session.add(empresa)

            empresa.razao_social = request.form.get('razao_social', '').strip() or None
            empresa.nome_fantasia = request.form.get('nome_fantasia', '').strip() or None
            empresa.codigo_empresa = _normalizar_codigo_identificacao(
                request.form.get('codigo_empresa'),
                maxlen=10,
            ) or None
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
            empresa.atendimento_mesas_ativo = (request.form.get('atendimento_mesas_ativo') == 'on')
            empresa.separacao_entrega_ativa = (request.form.get('separacao_entrega_ativa') == 'on')
            empresa.emissao_etiqueta_entrega_ativa = (request.form.get('emissao_etiqueta_entrega_ativa') == 'on')
            empresa.separacao_entrega_unir_vendas_off = (request.form.get('separacao_entrega_unir_vendas_off') == 'on')
            empresa.roteirizacao_entrega_ativa = (request.form.get('roteirizacao_entrega_ativa') == 'on')
            empresa.emissao_nota_entrega_ativa = (request.form.get('emissao_nota_entrega_ativa') == 'on')
            empresa.entrega_local_saida_padrao = request.form.get('entrega_local_saida_padrao', '').strip() or None
            empresa.entrega_veiculo_padrao = request.form.get('entrega_veiculo_padrao', '').strip() or None
            empresa.entrega_motorista_padrao = request.form.get('entrega_motorista_padrao', '').strip() or None
            horario_fechamento_roteirizacao_raw = request.form.get('entrega_horario_fechamento_roteirizacao', '')
            horario_fechamento_roteirizacao = _normalizar_horario_hhmm(horario_fechamento_roteirizacao_raw)
            if horario_fechamento_roteirizacao_raw.strip() and not horario_fechamento_roteirizacao:
                flash('Horario de fechamento para roteirizacao invalido. Use o formato HH:MM.', 'error')
                return redirect(url_for('editar_empresa') + '#config-entrega')
            empresa.entrega_horario_fechamento_roteirizacao = horario_fechamento_roteirizacao
            veiculos_linhas = _normalizar_linhas_configuracao(
                request.form.get('entrega_veiculos_cadastro', ''),
                tamanho_max=160
            )
            terceirizadas_linhas = _normalizar_linhas_configuracao(
                request.form.get('entrega_terceirizadas_cadastro', ''),
                tamanho_max=180
            )
            empresa.entrega_veiculos_json = json.dumps(veiculos_linhas, ensure_ascii=False) if veiculos_linhas else None
            empresa.entrega_terceirizadas_json = json.dumps(terceirizadas_linhas, ensure_ascii=False) if terceirizadas_linhas else None
            empresa.pagamentos_pdv_json = payment_text_to_json(
                request.form.get('pagamentos_pdv_config', ''),
                'pdv'
            )
            empresa.integracoes_pdv_json = api_integrations_text_to_json(
                request.form.get('integracoes_pdv_config', '')
            )
            empresa.reposicao_loja_fisica_ativa = (request.form.get('reposicao_loja_fisica_ativa') == 'on')
            empresa.emissao_etiqueta_loja_ativa = (request.form.get('emissao_etiqueta_loja_ativa') == 'on')
            empresa.emissao_etiqueta_endereco_ativa = (request.form.get('emissao_etiqueta_endereco_ativa') == 'on')
            empresa.servicos_tecnicos_ativos = (request.form.get('servicos_tecnicos_ativos') == 'on')
            empresa.servico_montagem_instalacao_ativo = (request.form.get('servico_montagem_instalacao_ativo') == 'on')
            if request.form.get('aplicar_preset_operacao') == 'on':
                _aplicar_preset_negocio(empresa)

            remover_logo = (request.form.get('remover_logo') == 'on')
            remover_favicon_empresa = (request.form.get('remover_favicon') == 'on')
            remover_app_icon = (request.form.get('remover_app_icon') == 'on')
            arquivo_logo = request.files.get('logo')
            arquivo_favicon_empresa = request.files.get('favicon')
            arquivo_app_icon = request.files.get('app_icon')
            allowed_ext = {'.png', '.jpg', '.jpeg', '.webp', '.gif'}
            allowed_favicon_ext = {'.ico', '.png', '.svg', '.jpg', '.jpeg', '.webp'}
            allowed_app_icon_ext = {'.png', '.jpg', '.jpeg', '.webp'}
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

            if arquivo_favicon_empresa and arquivo_favicon_empresa.filename:
                _, ext = os.path.splitext(arquivo_favicon_empresa.filename.lower())
                if ext not in allowed_favicon_ext:
                    flash('Formato de favicon inválido. Use ICO, PNG, SVG, JPG, JPEG ou WEBP.', 'error')
                    return redirect(url_for('editar_empresa'))
                nome_empresa_base = secure_filename((empresa.nome_fantasia or empresa.razao_social or 'empresa').strip())
                if not nome_empresa_base:
                    nome_empresa_base = 'empresa'
                relative_dir = os.path.join('uploads', 'empresa')
                absolute_dir = os.path.join(app.static_folder, relative_dir)
                os.makedirs(absolute_dir, exist_ok=True)
                image_name = f'{nome_empresa_base}_favicon{ext}'
                novo_favicon_empresa_path = os.path.join(relative_dir, image_name).replace('\\', '/')
                absolute_path = os.path.join(app.static_folder, novo_favicon_empresa_path)
                arquivo_favicon_empresa.save(absolute_path)
                empresa.favicon_path = novo_favicon_empresa_path
            elif remover_favicon_empresa:
                empresa.favicon_path = None

            if arquivo_app_icon and arquivo_app_icon.filename:
                _, ext = os.path.splitext(arquivo_app_icon.filename.lower())
                if ext not in allowed_app_icon_ext:
                    flash('Formato do ícone do app inválido. Use PNG, JPG, JPEG ou WEBP.', 'error')
                    return redirect(url_for('editar_empresa'))
                nome_empresa_base = secure_filename((empresa.nome_fantasia or empresa.razao_social or 'empresa').strip())
                if not nome_empresa_base:
                    nome_empresa_base = 'empresa'
                relative_dir = os.path.join('uploads', 'empresa')
                absolute_dir = os.path.join(app.static_folder, relative_dir)
                os.makedirs(absolute_dir, exist_ok=True)
                image_name = f'{nome_empresa_base}_app_icon{ext}'
                novo_app_icon_path = os.path.join(relative_dir, image_name).replace('\\', '/')
                absolute_path = os.path.join(app.static_folder, novo_app_icon_path)
                arquivo_app_icon.save(absolute_path)
                empresa.app_icon_path = novo_app_icon_path
            elif remover_app_icon:
                empresa.app_icon_path = None

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
            _garantir_matriculas_funcionarios()
            if novo_logo_path and logo_anterior and logo_anterior != novo_logo_path:
                caminho_logo_anterior = os.path.join(app.static_folder, logo_anterior)
                if os.path.exists(caminho_logo_anterior):
                    os.remove(caminho_logo_anterior)
            if remover_logo and logo_anterior:
                caminho_logo_anterior = os.path.join(app.static_folder, logo_anterior)
                if os.path.exists(caminho_logo_anterior):
                    os.remove(caminho_logo_anterior)
            if novo_favicon_empresa_path and favicon_empresa_anterior and favicon_empresa_anterior != novo_favicon_empresa_path:
                caminho_favicon_empresa_anterior = os.path.join(app.static_folder, favicon_empresa_anterior)
                if os.path.exists(caminho_favicon_empresa_anterior):
                    os.remove(caminho_favicon_empresa_anterior)
            if remover_favicon_empresa and favicon_empresa_anterior:
                caminho_favicon_empresa_anterior = os.path.join(app.static_folder, favicon_empresa_anterior)
                if os.path.exists(caminho_favicon_empresa_anterior):
                    os.remove(caminho_favicon_empresa_anterior)
            if novo_app_icon_path and app_icon_anterior and app_icon_anterior != novo_app_icon_path:
                caminho_app_icon_anterior = os.path.join(app.static_folder, app_icon_anterior)
                if os.path.exists(caminho_app_icon_anterior):
                    os.remove(caminho_app_icon_anterior)
            if remover_app_icon and app_icon_anterior:
                caminho_app_icon_anterior = os.path.join(app.static_folder, app_icon_anterior)
                if os.path.exists(caminho_app_icon_anterior):
                    os.remove(caminho_app_icon_anterior)
            flash('Dados da empresa salvos com sucesso.', 'success')
            return redirect(url_for('editar_empresa'))
        except Exception as e:
            db.session.rollback()
            if novo_logo_path:
                caminho_novo_logo = os.path.join(app.static_folder, novo_logo_path)
                if os.path.exists(caminho_novo_logo):
                    os.remove(caminho_novo_logo)
            if novo_favicon_empresa_path:
                caminho_novo_favicon = os.path.join(app.static_folder, novo_favicon_empresa_path)
                if os.path.exists(caminho_novo_favicon):
                    os.remove(caminho_novo_favicon)
            if novo_app_icon_path:
                caminho_novo_app_icon = os.path.join(app.static_folder, novo_app_icon_path)
                if os.path.exists(caminho_novo_app_icon):
                    os.remove(caminho_novo_app_icon)
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
    veiculos_texto = '\n'.join(_carregar_json_lista(empresa.entrega_veiculos_json if empresa else None))
    terceirizadas_texto = '\n'.join(_carregar_json_lista(empresa.entrega_terceirizadas_json if empresa else None))
    pagamentos_pdv_texto = payment_options_to_text(empresa.pagamentos_pdv_json if empresa else None, 'pdv')
    integracoes_pdv_texto = api_integrations_to_text(empresa.integracoes_pdv_json if empresa else None)
    return render_template(
        'sistema/empresa.html',
        empresa=empresa,
        tipos_negocio=tipos_negocio,
        canais_operacao=canais_operacao,
        veiculos_texto=veiculos_texto,
        terceirizadas_texto=terceirizadas_texto,
        pagamentos_pdv_texto=pagamentos_pdv_texto,
        integracoes_pdv_texto=integracoes_pdv_texto,
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
            empresa.pagamentos_ecommerce_json = payment_text_to_json(
                request.form.get('pagamentos_ecommerce_config', ''),
                'ecommerce'
            )
            empresa.integracoes_ecommerce_json = api_integrations_text_to_json(
                request.form.get('integracoes_ecommerce_config', '')
            )

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

            placeholder_alvos = [None, '', 'img/placeholders/imgindisponivel.png']
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
                    {Produto.imagem_path: 'img/placeholders/imgindisponivel.png'},
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
        pagamentos_ecommerce_texto=payment_options_to_text(empresa.pagamentos_ecommerce_json, 'ecommerce'),
        integracoes_ecommerce_texto=api_integrations_to_text(empresa.integracoes_ecommerce_json),
    )


@app.route('/ecommerce-ativacao', methods=['GET', 'POST'])
@require_role('admin', 'gerente')
def configurar_ativacao_ecommerce():
    empresa = EmpresaConfig.query.first()
    if not empresa:
        empresa = EmpresaConfig()
        db.session.add(empresa)
        db.session.commit()

    if request.method == 'POST':
        try:
            empresa.ecommerce_ativo = (request.form.get('ecommerce_ativo') == 'on')
            db.session.commit()
            flash('Ativacao do e-commerce salva com sucesso.', 'success')
            return redirect(url_for('configurar_ativacao_ecommerce'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao salvar ativacao do e-commerce: {str(e)}', 'error')

    return render_template('sistema/ecommerce_ativacao.html', empresa=empresa)


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


def _query_chamados_home(funcionario):
    if not _tabela_existe('chamados_internos'):
        return None
    query = ChamadoInterno.query.filter(
        ChamadoInterno.status.notin_([ChamadoInterno.STATUS_CONCLUIDO, ChamadoInterno.STATUS_CANCELADO])
    )
    if not _pode_gerir_chamados(funcionario):
        query = query.filter(
            db.or_(
                ChamadoInterno.solicitante_id == funcionario.id,
                ChamadoInterno.responsavel_id == funcionario.id,
            )
        )
    return query


def _query_ordens_home(funcionario):
    if not _tabela_existe('ordens_servico'):
        return None
    query = OrdemServico.query.filter(
        OrdemServico.status.in_([
            OrdemServico.STATUS_ABERTA,
            OrdemServico.STATUS_ENVIADA,
            OrdemServico.STATUS_EM_EXECUCAO,
        ])
    )
    if funcionario.role not in {'admin', 'gerente'}:
        query = query.filter(OrdemServico.funcionario_destino_id == funcionario.id)
    return query


def _montar_prioridades_home(funcionario, paginas_permitidas, empresa):
    prioridades = []
    origens_entrega = ['site']
    if empresa and empresa.separacao_entrega_unir_vendas_off:
        origens_entrega.append('interno')

    if 'pedidos' in paginas_permitidas:
        pedidos_abertos = Pedido.query.filter(
            Pedido.status.in_([Pedido.STATUS_ABERTO, Pedido.STATUS_EM_PREPARO, Pedido.STATUS_ENTREGUE])
        ).count()
        pedidos_preparo = Pedido.query.filter(
            Pedido.status.in_([Pedido.STATUS_ABERTO, Pedido.STATUS_EM_PREPARO])
        ).count()
        prioridades.append({
            'titulo': 'Pedidos na fila',
            'quantidade': pedidos_abertos,
            'descricao': 'Pedidos aguardando acao comercial ou operacional.',
            'acao': 'Abrir pedidos',
            'url': url_for('listar_pedidos'),
            'tom': 'primary',
            'detalhe': f'{pedidos_preparo} ainda em registro ou preparo.',
        })

    if 'expedicao' in paginas_permitidas and empresa and empresa.separacao_entrega_ativa is not False:
        pedidos_separacao = Pedido.query.filter(
            Pedido.status.in_([Pedido.STATUS_ABERTO, Pedido.STATUS_EM_PREPARO, Pedido.STATUS_ENTREGUE]),
            Pedido.origem.in_(origens_entrega),
            db.or_(
                Pedido.separacao_entrega_concluida.is_(False),
                Pedido.separacao_entrega_concluida.is_(None),
            ),
        ).count()
        pedidos_despacho = Pedido.query.filter(
            Pedido.status.in_([Pedido.STATUS_ABERTO, Pedido.STATUS_EM_PREPARO, Pedido.STATUS_ENTREGUE]),
            Pedido.origem.in_(origens_entrega),
            Pedido.separacao_entrega_concluida.is_(True),
            Pedido.entrega_concluida_em.is_(None),
        ).count()
        prioridades.append({
            'titulo': 'Separacao de entrega',
            'quantidade': pedidos_separacao,
            'descricao': 'Pedidos prontos comercialmente e aguardando separacao fisica.',
            'acao': 'Abrir separacao',
            'url': url_for('listar_separacao_entrega'),
            'tom': 'warning',
            'detalhe': f'{pedidos_despacho} ja separados aguardando roteirizacao ou despacho.',
        })

    if 'recebimentos' in paginas_permitidas:
        recebimentos_conferencia = RecebimentoFornecedor.query.filter_by(
            status=RecebimentoFornecedor.STATUS_CRIADO
        ).count()
        pendencias_armazenagem = RecebimentoFornecedor.query.filter_by(
            status=RecebimentoFornecedor.STATUS_AGUARDANDO_ARMAZENAGEM
        ).count()
        prioridades.append({
            'titulo': 'Recebimentos operacionais',
            'quantidade': recebimentos_conferencia,
            'descricao': 'Entradas aguardando conferencia inicial.',
            'acao': 'Abrir recebimentos',
            'url': url_for('listar_recebimentos_fornecedor'),
            'tom': 'info',
            'detalhe': f'{pendencias_armazenagem} pendencia(s) de armazenagem.',
        })

    if 'produtos' in paginas_permitidas:
        produtos_alerta = Produto.query.filter(
            Produto.quantidade_estoque < Produto.quantidade_minima,
            Produto.ativo.is_(True),
        ).count()
        prioridades.append({
            'titulo': 'Risco de ruptura',
            'quantidade': produtos_alerta,
            'descricao': 'Produtos abaixo do minimo configurado.',
            'acao': 'Revisar produtos',
            'url': url_for('listar_produtos', ruptura='sim'),
            'tom': 'danger',
            'detalhe': 'Use filtros e picking para priorizar reposicao.',
        })

    if 'financeiro' in paginas_permitidas:
        lancamentos_pendentes = LancamentoFinanceiro.query.filter(
            LancamentoFinanceiro.incluir_contabilidade.is_(True),
            db.or_(
                LancamentoFinanceiro.enviado_contador.is_(False),
                LancamentoFinanceiro.enviado_contador.is_(None),
            ),
        ).count()
        prioridades.append({
            'titulo': 'Financeiro e contador',
            'quantidade': lancamentos_pendentes,
            'descricao': 'Lancamentos ainda nao enviados para rotina contabil.',
            'acao': 'Abrir lancamentos',
            'url': url_for('financeiro_lancamentos'),
            'tom': 'secondary',
            'detalhe': 'Revise perdas, consumo interno e despesas operacionais.',
        })

    if 'caixas' in paginas_permitidas:
        caixas_abertos = Caixa.query.filter_by(aberto=True).count()
        prioridades.append({
            'titulo': 'Caixas abertos',
            'quantidade': caixas_abertos,
            'descricao': 'Caixas com operacao em andamento neste momento.',
            'acao': 'Abrir caixas',
            'url': url_for('listar_caixas'),
            'tom': 'success',
            'detalhe': 'Conferir aberturas, responsaveis e fechamento do turno.',
        })

    if 'chamados_internos' in paginas_permitidas:
        chamados_query = _query_chamados_home(funcionario)
        chamados_abertos = chamados_query.count() if chamados_query is not None else 0
        prioridades.append({
            'titulo': 'Chamados internos',
            'quantidade': chamados_abertos,
            'descricao': 'Pendencias de sistema, infraestrutura ou suporte.',
            'acao': 'Abrir chamados',
            'url': url_for('listar_chamados_internos'),
            'tom': 'dark',
            'detalhe': 'Priorize itens criticos e em triagem.',
        })

    if 'servicos_tecnicos' in paginas_permitidas:
        ordens_query = _query_ordens_home(funcionario)
        ordens_abertas = ordens_query.count() if ordens_query is not None else 0
        prioridades.append({
            'titulo': 'Ordens de servico',
            'quantidade': ordens_abertas,
            'descricao': 'Ordens tecnicas aguardando envio, execucao ou conclusao.',
            'acao': 'Abrir ordens',
            'url': url_for('listar_ordens_servico'),
            'tom': 'primary',
            'detalhe': 'Acompanhe agenda tecnica e retornos em aberto.',
        })

    prioridades.sort(key=lambda item: item['quantidade'], reverse=True)
    return prioridades


def _montar_atalhos_home(paginas_permitidas, empresa):
    candidatos = [
        ('pdv', 'PDV', 'Abrir venda no caixa ou pedido interno.', 'Abrir PDV', 'pdv'),
        ('pedidos', 'Pedidos', 'Ver filas de registro, preparo e fechamento.', 'Abrir pedidos', 'listar_pedidos'),
        ('recebimentos', 'Recebimentos', 'Conferir entradas e armazenagem.', 'Abrir recebimentos', 'listar_recebimentos_fornecedor'),
        ('produtos', 'Produtos', 'Consultar ruptura, picking e cadastro.', 'Abrir produtos', 'listar_produtos'),
        ('financeiro', 'Lancamentos', 'Registrar perdas, consumo e despesas.', 'Abrir lancamentos', 'financeiro_lancamentos'),
        ('caixas', 'Caixas', 'Abrir, fechar e revisar historico.', 'Abrir caixas', 'listar_caixas'),
        ('funcionarios', 'Funcionarios', 'Revisar equipe, acessos e estrutura.', 'Abrir funcionarios', 'listar_funcionarios'),
        ('rh_funcoes', 'Perfis e cargos', 'Ajustar cargos e perfis de acesso.', 'Abrir RH', 'listar_perfis_rh'),
        ('expedicao', 'Expedicao', 'Separar, roteirizar e despachar entregas.', 'Abrir expedicao', 'central_expedicao'),
        ('ajuda', 'Ajuda', 'Consultar fluxos, FAQ e treinamento.', 'Abrir ajuda', 'central_ajuda'),
    ]
    atalhos = []
    for pagina, titulo, descricao, acao, endpoint in candidatos:
        if pagina not in paginas_permitidas:
            continue
        if endpoint == 'central_expedicao' and empresa and empresa.separacao_entrega_ativa is False:
            continue
        atalhos.append({
            'titulo': titulo,
            'descricao': descricao,
            'acao': acao,
            'url': url_for(endpoint),
        })
    return atalhos[:8]


def _montar_fluxos_home(paginas_permitidas, empresa):
    passos = []
    if 'pedidos' in paginas_permitidas:
        passos.append({
            'titulo': 'Validar pedidos novos',
            'descricao': 'Comece por registro e preparo para manter a fila comercial organizada.',
            'url': url_for('listar_pedidos'),
            'acao': 'Ir para pedidos',
        })
    if 'expedicao' in paginas_permitidas and empresa and empresa.separacao_entrega_ativa is not False:
        passos.append({
            'titulo': 'Separar e despachar entregas',
            'descricao': 'Conclua separacao, roteirizacao e saida de pedidos de entrega.',
            'url': url_for('listar_separacao_entrega'),
            'acao': 'Ir para expedicao',
        })
    if 'recebimentos' in paginas_permitidas:
        passos.append({
            'titulo': 'Conferir entradas e armazenagem',
            'descricao': 'Receba, confira avarias e finalize o put-away antes da reposicao.',
            'url': url_for('listar_recebimentos_fornecedor'),
            'acao': 'Ir para recebimentos',
        })
    if 'financeiro' in paginas_permitidas:
        passos.append({
            'titulo': 'Atualizar perdas e despesas',
            'descricao': 'Lance consumo interno, despesas operacionais e pendencias contabeis.',
            'url': url_for('financeiro_lancamentos'),
            'acao': 'Ir para lancamentos',
        })
    if 'funcionarios' in paginas_permitidas:
        passos.append({
            'titulo': 'Revisar equipe e acessos',
            'descricao': 'Confirme perfil, cargo, responsavel direto e filiais liberadas para cada colaborador.',
            'url': url_for('listar_funcionarios'),
            'acao': 'Ir para funcionarios',
        })
    if 'ajuda' in paginas_permitidas:
        passos.append({
            'titulo': 'Treinar e alinhar operacao',
            'descricao': 'Use a ajuda para reforcar o fluxo correto antes de executar processos novos.',
            'url': url_for('central_ajuda'),
            'acao': 'Abrir ajuda',
        })
    return passos


@app.route('/boas-vindas')
@login_required
def boas_vindas():
    funcionario = get_funcionario_logado()
    if not funcionario:
        flash('Sessao invalida. Faca login novamente.', 'danger')
        return redirect(url_for('login'))

    empresa = EmpresaConfig.query.first()
    paginas_permitidas = _paginas_permitidas_para_funcionario(funcionario)
    saudacao_hora = datetime.now().hour
    if saudacao_hora < 12:
        saudacao = 'Bom dia'
    elif saudacao_hora < 18:
        saudacao = 'Boa tarde'
    else:
        saudacao = 'Boa noite'

    estoques_disponiveis = _estoques_contexto_disponiveis(funcionario)
    estoque_contexto_id = _estoque_contexto_selecionado_id(funcionario)
    estoque_contexto_atual = next((item for item in estoques_disponiveis if item.id == estoque_contexto_id), None)
    perfil_nome = funcionario.perfil_acesso.nome if getattr(funcionario, 'perfil_acesso', None) else 'Sem perfil padrao'
    prioridades = _montar_prioridades_home(funcionario, paginas_permitidas, empresa)
    atalhos = _montar_atalhos_home(paginas_permitidas, empresa)
    fluxos = _montar_fluxos_home(paginas_permitidas, empresa)

    return render_template(
        'sistema/boas_vindas.html',
        app_name=APP_NAME,
        app_version=APP_VERSION,
        app_domain=APP_DOMAIN,
        funcionario=funcionario,
        saudacao=saudacao,
        agora=datetime.now(),
        prioridades=prioridades,
        atalhos=atalhos,
        fluxos=fluxos,
        perfil_nome=perfil_nome,
        estoque_contexto_atual=estoque_contexto_atual,
        estoques_disponiveis=estoques_disponiveis,
        paginas_liberadas=len(paginas_permitidas),
    )


AJUDA_TOPICOS = {
    'primeiros-passos': {
        'slug': 'primeiros-passos',
        'titulo': 'Primeiros passos no sistema',
        'resumo': 'Configura o ambiente inicial para operar com seguranca e consistencia.',
        'objetivo': 'Preparar a empresa para operar do cadastro inicial ao primeiro teste controlado.',
        'paginas': [],
        'checklist': [
            'Validar quem sera responsavel por acessos, empresa e operacao.',
            'Confirmar dados da empresa, canal de operacao e recursos ativos.',
            'Separar alguns produtos e usuarios de teste antes de iniciar vendas reais.',
        ],
        'passos': [
            'Acesse Meu RH > Funcionarios e valide os perfis de acesso.',
            'Cadastre os dados da empresa em Meu RH > Empresa.',
            'Defina o tipo de negocio e o canal de operacao.',
            'Crie ao menos uma categoria e alguns produtos para teste.',
            'Abra um caixa e valide o fluxo completo no PDV.',
        ],
        'fluxograma': {
            'imagem': 'img/ajuda/fluxo-primeiros-passos.svg',
            'alt': 'Fluxograma dos primeiros passos para implantacao do sistema.',
            'legenda': 'Fluxo recomendado para iniciar a operacao sem pular configuracoes basicas.',
        },
        'alertas': [
            'Nao use vendas reais antes de testar caixa, pedidos e estoque com dados de exemplo.',
            'Ative o controle de acesso somente depois de revisar cargo e paginas permitidas.',
            'Se houver e-commerce ou expedicao, valide esses recursos antes de divulgar a operacao.',
        ],
        'duvidas': [
            {
                'pergunta': 'Por que alguns menus nao aparecem para mim?',
                'resposta': 'O sistema mostra apenas paginas liberadas para o seu perfil. Peça revisao de acesso em RH > Funcionarios > Acessos.',
            },
            {
                'pergunta': 'Qual modulo devo configurar primeiro?',
                'resposta': 'Comece por Empresa, depois Estoque basico (categoria/produto), em seguida PDV/Pedidos e por fim Expedicao, Financeiro e RH.',
            },
        ],
        'problemas': [
            {
                'situacao': 'Nao consigo salvar cadastro inicial.',
                'acao': 'Revise campos obrigatorios e se ha mensagens em vermelho no topo da pagina.',
            },
            {
                'situacao': 'Nao encontro um colaborador recem-criado.',
                'acao': 'Confirme se ele esta ativo e se o filtro da tela de Funcionarios nao esta limitado.',
            },
        ],
    },
    'duvidas-acesso': {
        'slug': 'duvidas-acesso',
        'titulo': 'Duvidas frequentes de acesso e navegacao',
        'resumo': 'Responde bloqueios comuns de menu, permissoes e acoes indisponiveis.',
        'objetivo': 'Ajudar o usuario a identificar se o bloqueio e de perfil, permissao, configuracao ou sessao.',
        'paginas': [],
        'checklist': [
            'Conferir se o usuario esta ativo e com senha correta.',
            'Verificar cargo, perfil e paginas liberadas em Funcionarios > Acessos.',
            'Fazer novo login depois de qualquer ajuste de permissao.',
        ],
        'passos': [
            'Valide se o colaborador esta ativo em Meu RH > Funcionarios.',
            'Confira o cargo/perfil do colaborador e a matricula utilizada no login.',
            'Se o controle de acesso estiver ativo, revise permissoes por pagina em Funcionarios > Acessos.',
            'Confirme se a funcionalidade esta habilitada em configuracoes da empresa.',
            'Peça novo login apos alteracoes de permissao para atualizar a sessao.',
        ],
        'fluxograma': {
            'imagem': 'img/ajuda/fluxo-acesso.svg',
            'alt': 'Fluxograma para diagnostico de bloqueios de acesso e navegacao.',
            'legenda': 'Use esta sequencia para identificar rapidamente o motivo de um menu ou acao nao aparecer.',
        },
        'alertas': [
            'Trocar apenas o cargo do colaborador pode nao ser suficiente se o controle de acesso por pagina estiver ativo.',
            'Permissoes novas normalmente exigem novo login para atualizar a sessao.',
            'Modulos desativados na empresa continuam ocultos mesmo para usuarios com cargo alto.',
        ],
        'duvidas': [
            {
                'pergunta': 'Por que o botao aparece para um usuario e para outro nao?',
                'resposta': 'As acoes obedecem permissao de pagina e perfil (admin/gerente/operacional).',
            },
            {
                'pergunta': 'Ajuda deve ficar visivel para todos os perfis?',
                'resposta': 'Sim. A ajuda fica disponivel para todos, mas o conteudo listado respeita o que cada perfil pode acessar.',
            },
        ],
        'problemas': [
            {
                'situacao': 'Recebo mensagem de acesso negado.',
                'acao': 'Solicite ao gestor revisao do perfil de acesso e dos ajustes individuais da pagina.',
            },
            {
                'situacao': 'Menu sumiu apos troca de cargo.',
                'acao': 'Revalide o perfil de acesso padrao e os ajustes individuais do colaborador, depois entre novamente no sistema.',
            },
        ],
    },
    'estoque-operacao': {
        'slug': 'estoque-operacao',
        'titulo': 'Operacao de estoque',
        'resumo': 'Passo a passo para cadastro, entrada, saida e acompanhamento de estoque.',
        'paginas': ['estoques', 'produtos', 'categorias', 'fornecedores', 'movimentacoes', 'relatorios'],
        'objetivo': 'Manter produtos, saldos e reposicao sob controle para evitar ruptura e divergencia fisica.',
        'checklist': [
            'Ter fornecedores, categorias e estoques cadastrados.',
            'Definir estoque minimo e preco nos produtos principais.',
            'Escolher o processo certo: recebimento, movimentacao, transferencia ou ajuste rapido.',
        ],
        'passos': [
            'Cadastre fornecedores com os dados principais.',
            'Crie categorias e depois cadastre os produtos.',
            'Informe preco de custo, preco de venda e estoque minimo.',
            'Registre entradas, saidas e recebimentos por fornecedor.',
            'Acompanhe relatorios para ruptura, giro e valor em estoque.',
        ],
        'fluxograma': {
            'imagem': 'img/ajuda/fluxo-estoque.svg',
            'alt': 'Fluxograma da operacao de estoque desde cadastro ate acompanhamento.',
            'legenda': 'Ciclo basico do estoque: cadastrar, movimentar, armazenar e acompanhar indicadores.',
        },
        'alertas': [
            'Nunca corrija saldo no produto sem registrar a movimentacao correspondente.',
            'Recebimentos e transferencias devem ser fechados no mesmo fluxo para nao gerar saldo solto.',
            'Produtos sem endereco ou estoque minimo ficam mais sujeitos a ruptura e retrabalho.',
        ],
        'duvidas': [
            {
                'pergunta': 'Quando usar movimentacao rapida?',
                'resposta': 'Use para ajustes operacionais de entrada/saida em lote e abastecimento rapido da operacao.',
            },
            {
                'pergunta': 'Como evitar ruptura em itens de alto giro?',
                'resposta': 'Defina estoque minimo coerente, acompanhe alertas de reposicao e use enderecos inteligentes.',
            },
        ],
        'problemas': [
            {
                'situacao': 'Produto sem endereco no coletor.',
                'acao': 'Acesse Enderecos Inteligentes e vincule o produto para reduzir retrabalho de separacao.',
            },
            {
                'situacao': 'Estoque ficou negativo ou incoerente.',
                'acao': 'Revise movimentacoes recentes, recebimentos e possiveis saidas duplicadas.',
            },
        ],
    },
    'vendas-pdv': {
        'slug': 'vendas-pdv',
        'titulo': 'Vendas e PDV',
        'resumo': 'Fluxo recomendado para abertura de caixa, venda e fechamento do turno.',
        'paginas': ['pdv', 'pedidos', 'caixas', 'mesas', 'garcons'],
        'objetivo': 'Padronizar a venda do caixa ao acompanhamento do pedido e do fechamento do turno.',
        'checklist': [
            'Confirmar que existe caixa aberto para a operacao.',
            'Verificar itens, precos e meios de pagamento liberados.',
            'Definir se a venda sera balcão, pedido, mesa ou comanda conforme o processo da empresa.',
        ],
        'passos': [
            'Abra o caixa com o valor inicial do turno.',
            'Lance os pedidos no PDV e confirme os itens.',
            'Selecione o metodo de pagamento e finalize a venda.',
            'Acompanhe os pedidos na tela de pedidos e status.',
            'Feche o caixa ao final do expediente e confira o historico.',
        ],
        'fluxograma': {
            'imagem': 'img/ajuda/fluxo-vendas.svg',
            'alt': 'Fluxograma do processo de vendas e PDV.',
            'legenda': 'Fluxo recomendado para venda no PDV com acompanhamento do pedido e fechamento do caixa.',
        },
        'alertas': [
            'Nao feche o caixa antes de conferir pedidos em aberto, pagamentos pendentes e diferencas.',
            'Pedidos finalizados devem ser tratados como historico operacional, nao como rascunho editavel.',
            'Se a venda estiver ligada a mesas ou garcons, valide a configuracao da empresa antes do turno.',
        ],
        'duvidas': [
            {
                'pergunta': 'Qual a diferenca entre Pedido e PDV?',
                'resposta': 'PDV e o ponto de registro/finalizacao da venda; Pedidos e a fila consolidada para acompanhamento operacional.',
            },
            {
                'pergunta': 'Posso editar pedido fechado?',
                'resposta': 'Normalmente nao. Pedidos fechados sao tratados como imutaveis para seguranca operacional e fiscal.',
            },
        ],
        'problemas': [
            {
                'situacao': 'Nao consigo fechar pedido.',
                'acao': 'Confirme metodo de pagamento, valor recebido e se o caixa informado esta aberto.',
            },
            {
                'situacao': 'Pedido nao aparece no monitor.',
                'acao': 'Verifique filtros de status/busca e atualize a tela para recarregar a listagem.',
            },
        ],
    },
    'expedicao-entregas': {
        'slug': 'expedicao-entregas',
        'titulo': 'Expedicao, transferencias e abastecimento',
        'resumo': 'Organiza separacao, rota, etiquetas, notas e fluxo de abastecimento entre estoques/lojas.',
        'paginas': ['expedicao', 'pedidos', 'movimentacoes', 'enderecos_estoque'],
        'objetivo': 'Garantir que pedidos saiam separados, roteirizados e despachados com rastreio operacional.',
        'checklist': [
            'Confirmar se a separacao de entrega esta ativa na empresa.',
            'Validar frota, etiquetas e regras de roteirizacao antes do despacho.',
            'Checar se o pedido esta separado e elegivel para entrar na fila de entrega.',
        ],
        'passos': [
            'Acesse Expedicao > Central de Expedicao para iniciar o fluxo diario.',
            'Faça separacao e embalagem dos pedidos na fila operacional.',
            'Preencha rota, ordem, local de saida e dados de motorista/veiculo.',
            'Emita etiqueta de entrega e registre nota fiscal quando aplicavel.',
            'Use transferencias e entrada em massa para abastecimento entre estoques/lojas.',
            'Acompanhe Painel em Tempo Real para status da operacao diaria.',
        ],
        'fluxograma': {
            'imagem': 'img/ajuda/fluxo-expedicao.svg',
            'alt': 'Fluxograma da operacao de expedicao e entrega.',
            'legenda': 'Ordem recomendada: separar, roteirizar, despachar, entregar e abastecer quando necessario.',
        },
        'alertas': [
            'Pedido sem separacao concluida nao deve seguir para roteirizacao.',
            'Nao misture ajuste de estoque com despacho sem registrar a movimentacao correspondente.',
            'Etiquetas e nota fiscal dependem de configuracoes da empresa e da elegibilidade do pedido.',
        ],
        'duvidas': [
            {
                'pergunta': 'Como cadastrar frota propria e terceiros?',
                'resposta': 'Use Expedicao > Frota Propria e Terceiros para salvar veiculos, Correios, freelancers e transportadoras.',
            },
            {
                'pergunta': 'Quando usar transferencia entre estoques?',
                'resposta': 'Quando houver necessidade de reposicao de loja/CD ou ajuste fisico de enderecamento.',
            },
        ],
        'problemas': [
            {
                'situacao': 'Pedido nao libera para roteirizacao.',
                'acao': 'Confirme se a separacao foi concluida e se o pedido nao esta cancelado/fechado.',
            },
            {
                'situacao': 'Etiqueta nao imprime.',
                'acao': 'Valide se emissao de etiqueta esta ativa nas configuracoes da empresa e se o pedido esta elegivel.',
            },
        ],
    },
    'financeiro-lancamentos': {
        'slug': 'financeiro-lancamentos',
        'titulo': 'Financeiro, lancamentos e fundos',
        'resumo': 'Padrao de registro monetario para conciliacao e exportacao contabil.',
        'paginas': ['financeiro'],
        'objetivo': 'Organizar entradas, saidas e fundos para facilitar conciliacao interna e envio contabil.',
        'checklist': [
            'Definir periodo de analise antes de lancar ou exportar dados.',
            'Conferir natureza, competencia e centro responsavel do registro.',
            'Separar o que e operacao diaria, fundo interno e item contabil.',
        ],
        'passos': [
            'Use Visao Financeira para acompanhar indicadores principais.',
            'Cadastre lancamentos com natureza, competencia e centro responsavel.',
            'Marque itens para contabilidade quando houver envio para contador.',
            'Registre solicitacoes e liberacoes de fundos conforme politica interna.',
            'Exporte arquivos para conferencia antes do fechamento mensal.',
        ],
        'fluxograma': {
            'imagem': 'img/ajuda/fluxo-financeiro.svg',
            'alt': 'Fluxograma do processo financeiro com lancamentos e conciliacao.',
            'legenda': 'Fluxo basico do financeiro: registrar, classificar, conciliar, aprovar fundos e exportar.',
        },
        'alertas': [
            'Lancamento sem competencia ou classificacao correta gera distorcao de relatorio.',
            'Antes de exportar, revise filtros de data e registros marcados para contabilidade.',
            'Consumo proprio, taxas e ajustes precisam ficar separados para manter rastreabilidade.',
        ],
        'duvidas': [
            {
                'pergunta': 'O que entra como lancamento contabil?',
                'resposta': 'Entradas e saidas monetarias que precisam compor conciliacao, declaracao e envio ao contador.',
            },
            {
                'pergunta': 'Posso separar consumo proprio da empresa?',
                'resposta': 'Sim. Classifique lancamentos de consumo proprio para manter rastreio e separacao fiscal.',
            },
        ],
        'problemas': [
            {
                'situacao': 'Valores nao batem com o periodo.',
                'acao': 'Revise filtros de data, status do caixa e se houve pedidos cancelados no intervalo.',
            },
            {
                'situacao': 'Exportacao incompleta.',
                'acao': 'Confirme se lancamentos obrigatorios foram marcados para contabilidade e salvos.',
            },
        ],
    },
    'rh-seguranca': {
        'slug': 'rh-seguranca',
        'titulo': 'RH e seguranca de acesso',
        'resumo': 'Define cargos, permissoes e auditoria para controle operacional.',
        'paginas': ['funcionarios', 'rh_funcoes', 'rh_indicadores', 'rh_organograma', 'auditoria'],
        'objetivo': 'Controlar quem acessa cada modulo, como a estrutura da equipe e montada e quem alterou dados sensiveis.',
        'checklist': [
            'Criar ou revisar cargos e perfis antes de cadastrar muitos usuarios.',
            'Definir superior, departamento, time e nivel organizacional quando aplicavel.',
            'Validar se o controle de acesso por pagina ja pode ser ativado.',
        ],
        'passos': [
            'Crie funcoes/perfis com permissoes por pagina.',
            'Associe cada colaborador ao cargo correto.',
            'Monte a arvore de hierarquia no RH > Organograma.',
            'Ative o controle de acesso quando terminar a configuracao.',
            'Revise os acessos por funcionario periodicamente.',
            'Use a auditoria para rastrear alteracoes e acoes sensiveis.',
        ],
        'fluxograma': {
            'imagem': 'img/ajuda/fluxo-rh.svg',
            'alt': 'Fluxograma do processo de RH e seguranca de acesso.',
            'legenda': 'Fluxo recomendado para criar cargos, vincular colaboradores, ativar acessos e auditar alteracoes.',
        },
        'alertas': [
            'Ativar controle de acesso cedo demais pode esconder telas essenciais da equipe.',
            'Usuario ativo sem superior, nivel ou cargo correto pode distorcer organograma e permissoes.',
            'A auditoria deve ser revisada em mudancas sensiveis de cadastro, financeiro e operacao.',
        ],
        'duvidas': [
            {
                'pergunta': 'Como liberar upload de foto de perfil para colaborador?',
                'resposta': 'No cadastro do funcionario, habilite a opcao de permitir edicao de imagem de perfil.',
            },
            {
                'pergunta': 'Matricula pode ser usada como login?',
                'resposta': 'Sim. A matricula pode ser usada como identificador de acesso junto com senha.',
            },
        ],
        'problemas': [
            {
                'situacao': 'Colaborador nao aparece no organograma.',
                'acao': 'Verifique superior, nivel, departamento/time e se o cadastro esta ativo.',
            },
            {
                'situacao': 'Permissoes nao foram aplicadas.',
                'acao': 'Confira cargo/perfil e, apos salvar, faça novo login para atualizar sessao.',
            },
        ],
    },
    'ecommerce-config': {
        'slug': 'ecommerce-config',
        'titulo': 'Configuracao do e-commerce',
        'resumo': 'Separa ativacao da loja online da configuracao visual, comercial e tecnica da vitrine.',
        'paginas': ['ecommerce_config'],
        'objetivo': 'Manter a loja online ativa quando necessario e ajustar a vitrine com identidade, campanhas e integracoes.',
        'checklist': [
            'Validar se a ativacao da loja online esta ligada antes de divulgar o link para clientes.',
            'Separar banners, logos e textos oficiais antes da configuracao.',
            'Definir periodo de vigencia para campanhas e promocoes.',
            'Verificar cores, rodape e imagem padrao de produto em mobile e desktop.',
        ],
        'passos': [
            'Acesse E-commerce > Ativacao da Loja e confirme se o canal publico esta liberado.',
            'Acesse E-commerce > Tema e Loja Online.',
            'Defina cores da vitrine e mensagem principal.',
            'Configure multiplos banners com periodo de vigencia.',
            'Cadastre campanhas programadas com inicio e fim.',
            'Ajuste rodape, favicon e imagem padrao de produto.',
        ],
        'fluxograma': {
            'imagem': 'img/ajuda/fluxo-ecommerce.svg',
            'alt': 'Fluxograma da configuracao do e-commerce.',
            'legenda': 'Sequencia sugerida para ajustar tema, vitrine, campanhas e revisao visual da loja.',
        },
        'alertas': [
            'Imagens fora do tamanho recomendado podem prejudicar a leitura da vitrine no celular.',
            'Campanhas sem vigencia clara podem continuar aparecendo fora do periodo esperado.',
            'Sempre revise a loja publica depois de alterar tema, favicon ou banner.',
        ],
        'duvidas': [
            {
                'pergunta': 'Como deixar a loja com visual padrao de marketplace?',
                'resposta': 'Ajuste paleta, banners e cards de produto no modulo de tema para manter consistencia mobile.',
            },
            {
                'pergunta': 'Posso agendar campanhas automaticamente?',
                'resposta': 'Sim. Configure inicio/fim de vigencia para promocoes e campanhas programadas.',
            },
        ],
        'problemas': [
            {
                'situacao': 'Banner nao aparece na loja.',
                'acao': 'Verifique vigencia, status ativo e dimensoes da imagem.',
            },
            {
                'situacao': 'Produto sem foto na vitrine.',
                'acao': 'Confirme imagem do produto ou fallback padrao configurado no e-commerce.',
            },
        ],
    },
    'servicos-tecnicos': {
        'slug': 'servicos-tecnicos',
        'titulo': 'Chamados internos e servicos tecnicos',
        'resumo': 'Explica como abrir, encaminhar e executar chamados e ordens de servico.',
        'paginas': ['servicos_tecnicos', 'chamados_internos'],
        'objetivo': 'Padronizar o registro da demanda interna ate a execucao tecnica e o retorno final.',
        'checklist': [
            'Definir se o caso deve nascer como chamado interno ou ordem tecnica.',
            'Informar produto, local, prioridade e descricao objetiva do problema.',
            'Validar se o servico de montagem/instalacao esta habilitado quando aplicavel.',
        ],
        'passos': [
            'Abra o chamado interno com contexto claro do problema ou necessidade.',
            'Classifique prioridade, local, responsavel e observacoes relevantes.',
            'Converta ou vincule a demanda a uma ordem de servico tecnica quando necessario.',
            'Acompanhe status, execucao em campo e retorno do tecnico.',
            'Feche a demanda somente apos validar a solucao ou o motivo do encerramento.',
        ],
        'fluxograma': {
            'imagem': 'img/ajuda/fluxo-servicos.svg',
            'alt': 'Fluxograma de chamados internos e ordens de servico.',
            'legenda': 'Fluxo recomendado para abertura, triagem, execucao e fechamento de servicos tecnicos.',
        },
        'alertas': [
            'Chamado sem descricao minima dificulta triagem e aumenta retrabalho.',
            'Nao feche a ordem antes de registrar o retorno tecnico e o resultado da visita.',
            'Servicos de montagem e instalacao dependem de empresa e produto habilitados.',
        ],
        'duvidas': [
            {
                'pergunta': 'Quando abrir chamado e quando abrir ordem de servico?',
                'resposta': 'O chamado registra a necessidade interna; a ordem organiza a execucao tecnica da atividade.',
            },
            {
                'pergunta': 'Posso acompanhar apenas minhas ordens?',
                'resposta': 'Sim. O modulo possui visao de ordens proprias e visao geral conforme o acesso liberado.',
            },
        ],
        'problemas': [
            {
                'situacao': 'Nao consigo criar ordem de instalacao.',
                'acao': 'Verifique se a empresa e o produto estao com servico de montagem/instalacao liberados.',
            },
            {
                'situacao': 'Chamado parado sem responsavel.',
                'acao': 'Revise prioridade, encaminhamento e se existe tecnico/perfil apto para receber a demanda.',
            },
        ],
    },
    'app-mobile': {
        'slug': 'app-mobile',
        'titulo': 'App mobile e tela inicial',
        'resumo': 'Mostra como instalar o sistema na tela inicial do celular e usar o acesso rapido.',
        'paginas': [],
        'objetivo': 'Facilitar o acesso diario no celular com comportamento de app, especialmente para operacao em campo.',
        'checklist': [
            'Abrir o sistema no celular usando navegador atualizado.',
            'Estar conectado ao sistema com a tela carregada normalmente.',
            'Verificar se o atalho ainda nao foi instalado no aparelho.',
        ],
        'passos': [
            'Ao entrar no sistema pelo celular, observe o aviso para adicionar o app a tela inicial.',
            'No Android, toque em Adicionar agora quando o navegador oferecer a instalacao.',
            'No iPhone, use Compartilhar > Adicionar a Tela de Inicio quando o aviso orientar esse passo.',
            'Abra o atalho criado para usar o sistema em tela cheia e com acesso mais rapido.',
            'Se o aviso sumir, abra novamente o sistema no navegador principal do aparelho e repita o processo.',
        ],
        'fluxograma': {
            'imagem': 'img/ajuda/fluxo-app-mobile.svg',
            'alt': 'Fluxograma para instalacao do sistema como app na tela inicial do celular.',
            'legenda': 'Fluxo simples para instalar o atalho do sistema no Android ou no iPhone.',
        },
        'alertas': [
            'O aviso de instalacao nao aparece para quem ja instalou ou dispensou recentemente.',
            'No iPhone a instalacao e manual pelo menu Compartilhar do Safari.',
            'Alguns navegadores de terceiros limitam o comportamento de app; prefira Chrome, Edge ou Safari.',
        ],
        'duvidas': [
            {
                'pergunta': 'Instalar na tela inicial muda meu acesso?',
                'resposta': 'Nao. O atalho apenas facilita abrir o sistema como app; seu perfil e permissao continuam os mesmos.',
            },
            {
                'pergunta': 'Posso remover e instalar de novo depois?',
                'resposta': 'Sim. O atalho pode ser removido do aparelho e reinstalado quando necessario.',
            },
        ],
        'problemas': [
            {
                'situacao': 'O botao de instalar nao apareceu no Android.',
                'acao': 'Atualize o navegador, recarregue a pagina e abra o sistema no navegador principal do aparelho.',
            },
            {
                'situacao': 'No iPhone nao apareceu botao de instalar.',
                'acao': 'Use o Safari e siga o caminho Compartilhar > Adicionar a Tela de Inicio.',
            },
        ],
    },
}

AJUDA_MENU_TOPICOS = {
    'Dashboard': ('primeiros-passos', 'duvidas-acesso', 'app-mobile'),
    'Gestao': (),
    'Financeiro': ('financeiro-lancamentos',),
    'Vendas': ('vendas-pdv',),
    'Estoque': ('estoque-operacao',),
    'Recebimento': ('estoque-operacao',),
    'Expedicao': ('expedicao-entregas',),
    'Meu RH': ('rh-seguranca',),
    'E-commerce': ('ecommerce-config',),
    'Servicos': ('servicos-tecnicos',),
    'Ajuda': (),
}

AJUDA_MENU_DESCRICOES = {
    'Dashboard': 'Orientacoes iniciais, acesso ao sistema e uso no celular.',
    'Gestao': 'Fluxos administrativos e configuracoes gerais do negocio.',
    'Financeiro': 'Lancamentos, fundos e conferencia financeira da operacao.',
    'Vendas': 'Atendimento, PDV, mesas, caixas e andamento dos pedidos.',
    'Estoque': 'Cadastros, enderecamento, ajustes internos e consultas operacionais.',
    'Recebimento': 'Entradas de fornecedores, conferencia e armazenagem por tipo de recebimento.',
    'Expedicao': 'Separacao, transferencias entre lojas/CDs e entrega de pedidos.',
    'Meu RH': 'Equipe, acessos, perfis, auditoria e estrutura organizacional.',
    'E-commerce': 'Ativacao da loja online, identidade visual, campanhas e integracoes.',
    'Servicos': 'Chamados internos, suporte tecnico e atendimentos de manutencao.',
}


def _rotulo_paginas_fluxo(paginas):
    rotulos = []
    for pagina in paginas:
        titulo = PAGINAS_SISTEMA.get(pagina)
        if titulo and titulo not in rotulos:
            rotulos.append(titulo)
    return rotulos


def _paginas_da_secao_menu(secao_nome):
    for nome, paginas in PAGINAS_SISTEMA_MENU_ORDEM:
        if nome == secao_nome:
            return paginas
    return ()


def _enriquecer_topico_ajuda(topico, secao_nome=None, secao_paginas=()):
    topico_formatado = dict(topico)
    paginas_topico = list(topico.get('paginas') or [])
    fluxo_paginas = []
    if secao_paginas:
        fluxo_paginas = [pagina for pagina in secao_paginas if pagina in paginas_topico]
    if not fluxo_paginas:
        fluxo_paginas = paginas_topico
    topico_formatado['menu_secao'] = secao_nome
    topico_formatado['fluxo_paginas'] = _rotulo_paginas_fluxo(fluxo_paginas)
    return topico_formatado


def _organizar_topicos_ajuda_por_menu(topicos):
    topicos_map = {item['slug']: item for item in topicos}
    grupos = []
    topicos_ordenados = []
    slugs_usados = set()

    for secao_nome, secao_paginas in PAGINAS_SISTEMA_MENU_ORDEM:
        slugs_secao = AJUDA_MENU_TOPICOS.get(secao_nome, ())
        topicos_secao = []
        for slug in slugs_secao:
            topico = topicos_map.get(slug)
            if not topico:
                continue
            topico_formatado = _enriquecer_topico_ajuda(topico, secao_nome, secao_paginas)
            topicos_secao.append(topico_formatado)
            topicos_ordenados.append(topico_formatado)
            slugs_usados.add(slug)
        if topicos_secao:
            grupos.append({
                'secao': secao_nome,
                'descricao': AJUDA_MENU_DESCRICOES.get(secao_nome),
                'topicos': topicos_secao,
            })

    topicos_restantes = []
    for topico in sorted(topicos_map.values(), key=lambda item: item.get('titulo') or ''):
        if topico['slug'] in slugs_usados:
            continue
        topico_formatado = _enriquecer_topico_ajuda(topico)
        topicos_restantes.append(topico_formatado)
        topicos_ordenados.append(topico_formatado)

    if topicos_restantes:
        grupos.append({
            'secao': 'Outros fluxos',
            'descricao': 'Guias complementares liberados para o seu perfil.',
            'topicos': topicos_restantes,
        })

    return grupos, topicos_ordenados


def _topicos_relacionados_ajuda(topico_atual, paginas_permitidas):
    grupo_atual = None
    for secao_nome, slugs_secao in AJUDA_MENU_TOPICOS.items():
        if topico_atual.get('slug') in slugs_secao:
            grupo_atual = secao_nome
            break

    relacionados_mesmo_grupo = []
    relacionados_outros = []

    for secao_nome, secao_paginas in PAGINAS_SISTEMA_MENU_ORDEM:
        slugs_secao = AJUDA_MENU_TOPICOS.get(secao_nome, ())
        for slug in slugs_secao:
            if slug == topico_atual.get('slug'):
                continue
            item = AJUDA_TOPICOS.get(slug)
            if not item:
                continue
            paginas_item = set(item.get('paginas') or [])
            if paginas_item and not paginas_item.intersection(paginas_permitidas):
                continue
            topico_formatado = _enriquecer_topico_ajuda(item, secao_nome, secao_paginas)
            if secao_nome == grupo_atual:
                relacionados_mesmo_grupo.append(topico_formatado)
            else:
                relacionados_outros.append(topico_formatado)

    for slug, item in sorted(AJUDA_TOPICOS.items(), key=lambda entry: (entry[1].get('titulo') or '')):
        if slug == topico_atual.get('slug'):
            continue
        if slug in {rel['slug'] for rel in relacionados_mesmo_grupo + relacionados_outros}:
            continue
        paginas_item = set(item.get('paginas') or [])
        if paginas_item and not paginas_item.intersection(paginas_permitidas):
            continue
        relacionados_outros.append(_enriquecer_topico_ajuda(item))

    return grupo_atual, relacionados_mesmo_grupo + relacionados_outros


ASSISTENTE_PAGINA_ENDPOINT_PRINCIPAL = {
    'inicio': 'boas_vindas',
    'gestao_negocio': 'gestao_negocio',
    'financeiro': 'financeiro_lancamentos',
    'pdv': 'pdv',
    'estoques': 'listar_estoques',
    'produtos': 'listar_produtos',
    'categorias': 'listar_categorias',
    'fornecedores': 'listar_fornecedores',
    'enderecos_estoque': 'listar_enderecos_estoque',
    'movimentacoes': 'listar_movimentacoes',
    'almoxarifado': 'listar_almoxarifado',
    'recebimentos': 'listar_recebimentos_fornecedor',
    'relatorios': 'relatorios',
    'equipamentos_estoque': 'listar_equipamentos_movimentacao',
    'enderecos_inteligentes': 'enderecos_inteligentes',
    'caixas': 'listar_caixas',
    'mesas': 'listar_mesas',
    'pedidos': 'listar_pedidos',
    'expedicao': 'central_expedicao',
    'transferencias_estoque': 'listar_transferencias_estoque',
    'funcionarios': 'listar_funcionarios',
    'rh_funcoes': 'listar_funcoes_rh',
    'rh_indicadores': 'indicadores_rh',
    'rh_organograma': 'organograma_rh',
    'auditoria': 'auditoria_sistema',
    'empresa': 'editar_empresa',
    'ecommerce_config': 'configurar_ecommerce',
    'servicos_tecnicos': 'listar_ordens_servico',
    'chamados_internos': 'listar_chamados_internos',
    'garcons': 'listar_garcons',
    'ajuda': 'central_ajuda',
}


def _endpoint_principal_assistente_pagina(pagina):
    endpoint = ASSISTENTE_PAGINA_ENDPOINT_PRINCIPAL.get(pagina)
    if endpoint:
        return endpoint
    endpoints = sorted(PAGINA_ENDPOINTS.get(pagina) or [])
    return endpoints[0] if endpoints else None


def _url_assistente(endpoint, **kwargs):
    if not endpoint:
        return None
    try:
        return url_for(endpoint, **kwargs)
    except Exception:
        return None


def _secao_menu_assistente_topico(topico):
    slug = topico.get('slug')
    for secao_nome, slugs in AJUDA_MENU_TOPICOS.items():
        if slug in slugs:
            return secao_nome
    for secao_nome, secao_paginas in PAGINAS_SISTEMA_MENU_ORDEM:
        if set(topico.get('paginas') or []).intersection(secao_paginas):
            return secao_nome
    return 'Ajuda'


def _resumo_topico_assistente(topico):
    partes = [
        topico.get('resumo'),
        topico.get('objetivo'),
    ]
    passos = [item for item in (topico.get('passos') or []) if item]
    if passos:
        partes.append('Fluxo: ' + ' '.join(passos[:3]))
    duvidas = [item.get('pergunta') for item in (topico.get('duvidas') or []) if item.get('pergunta')]
    if duvidas:
        partes.append('Duvidas comuns: ' + ' '.join(duvidas[:2]))
    alertas = [item for item in (topico.get('alertas') or []) if item]
    if alertas:
        partes.append('Atencao: ' + ' '.join(alertas[:2]))
    return ' '.join(item.strip() for item in partes if item).strip()


def _acoes_assistente_para_paginas(paginas):
    acoes = []
    for pagina in paginas or []:
        endpoint = _endpoint_principal_assistente_pagina(pagina)
        url = _url_assistente(endpoint)
        if not url:
            continue
        acoes.append({
            'label': f'Abrir {PAGINAS_SISTEMA.get(pagina, pagina)}',
            'url': url,
            'page': pagina,
            'reason': PAGINAS_SISTEMA.get(pagina, pagina),
            'kind': 'navigate',
        })
    return acoes


def _construir_documentos_assistente_local():
    documentos = []
    topicos_por_pagina = {}

    def _deduplicar_textos(itens):
        vistos = set()
        resultado = []
        for item in itens or []:
            texto = (item or '').strip()
            chave = texto.lower()
            if not texto or chave in vistos:
                continue
            vistos.add(chave)
            resultado.append(texto)
        return resultado

    def _deduplicar_problemas(itens):
        vistos = set()
        resultado = []
        for item in itens or []:
            situacao = (item.get('situacao') or '').strip()
            acao = (item.get('acao') or '').strip()
            chave = (situacao.lower(), acao.lower())
            if not situacao or not acao or chave in vistos:
                continue
            vistos.add(chave)
            resultado.append({
                'situation': situacao,
                'action': acao,
            })
        return resultado

    def _faq_pairs(topico):
        pares = []
        for duvida in topico.get('duvidas') or []:
            pergunta = (duvida.get('pergunta') or '').strip()
            resposta = (duvida.get('resposta') or '').strip()
            if pergunta and resposta:
                pares.append({
                    'question': pergunta,
                    'answer': resposta,
                })
        return pares

    for topico in AJUDA_TOPICOS.values():
        for pagina in topico.get('paginas') or []:
            topicos_por_pagina.setdefault(pagina, []).append(topico)

    for secao_nome, secao_paginas in PAGINAS_SISTEMA_MENU_ORDEM:
        for pagina in secao_paginas:
            titulo = PAGINAS_SISTEMA.get(pagina)
            if not titulo:
                continue
            topicos_relacionados = topicos_por_pagina.get(pagina, [])
            resumo_relacionado = ' '.join(
                item.get('resumo')
                for item in topicos_relacionados[:2]
                if item.get('resumo')
            ).strip()
            snippet = resumo_relacionado or f'Tela principal de {titulo} na secao {secao_nome}.'
            faq_pairs = []
            passos_relacionados = []
            checklist_relacionado = []
            alertas_relacionados = []
            problemas_relacionados = []
            palavras_chave = {
                pagina,
                titulo,
                secao_nome,
                'navegacao',
                'como usar',
                'onde fica',
            }
            for item in topicos_relacionados:
                if item.get('titulo'):
                    palavras_chave.add(item['titulo'])
                if item.get('slug'):
                    palavras_chave.add(item['slug'].replace('-', ' '))
                faq_pairs.extend(_faq_pairs(item))
                passos_relacionados.extend(item.get('passos') or [])
                checklist_relacionado.extend(item.get('checklist') or [])
                alertas_relacionados.extend(item.get('alertas') or [])
                problemas_relacionados.extend(item.get('problemas') or [])

            endpoint = _endpoint_principal_assistente_pagina(pagina)
            documentos.append({
                'id': f'page:{pagina}',
                'kind': 'page',
                'page': pagina,
                'pages': [pagina],
                'page_labels': [titulo],
                'section': secao_nome,
                'title': titulo,
                'summary': snippet,
                'snippet': snippet,
                'keywords': sorted(palavras_chave),
                'faq_pairs': faq_pairs,
                'steps': _deduplicar_textos(passos_relacionados),
                'checklist': _deduplicar_textos(checklist_relacionado),
                'alerts': _deduplicar_textos(alertas_relacionados),
                'problems': _deduplicar_problemas(problemas_relacionados),
                'url': _url_assistente(endpoint),
                'actions': _acoes_assistente_para_paginas([pagina]) + (
                    [{
                        'label': 'Abrir guia',
                        'url': _url_assistente('central_ajuda'),
                        'page': 'ajuda',
                        'reason': 'Ajuda e treinamento',
                        'kind': 'guide',
                    }] if _url_assistente('central_ajuda') else []
                ),
            })

    for topico in AJUDA_TOPICOS.values():
        secao_nome = _secao_menu_assistente_topico(topico)
        paginas = list(topico.get('paginas') or [])
        resumo = _resumo_topico_assistente(topico)
        faq_pairs = _faq_pairs(topico)
        problems = _deduplicar_problemas(topico.get('problemas') or [])
        palavras_chave = {
            topico.get('slug', '').replace('-', ' '),
            topico.get('titulo'),
            secao_nome,
            'fluxo',
            'passo a passo',
            'ajuda',
            'como fazer',
        }
        for pergunta in topico.get('duvidas') or []:
            if pergunta.get('pergunta'):
                palavras_chave.add(pergunta['pergunta'])

        documentos.append({
            'id': f"topic:{topico.get('slug')}",
            'kind': 'topic',
            'page': paginas[0] if paginas else 'ajuda',
            'pages': paginas or ['ajuda'],
            'page_labels': [PAGINAS_SISTEMA.get(item, item) for item in (paginas or ['ajuda'])],
            'section': secao_nome,
            'title': topico.get('titulo'),
            'summary': topico.get('resumo') or topico.get('objetivo'),
            'snippet': resumo,
            'keywords': sorted(item for item in palavras_chave if item),
            'faq_pairs': faq_pairs,
            'steps': _deduplicar_textos(topico.get('passos') or []),
            'checklist': _deduplicar_textos(topico.get('checklist') or []),
            'alerts': _deduplicar_textos(topico.get('alertas') or []),
            'problems': problems,
            'source_topic': topico.get('titulo'),
            'url': _url_assistente('detalhe_ajuda', topico_slug=topico.get('slug')),
            'actions': (
                [{
                    'label': 'Abrir guia detalhado',
                    'url': _url_assistente('detalhe_ajuda', topico_slug=topico.get('slug')),
                    'page': 'ajuda',
                    'reason': topico.get('titulo'),
                    'kind': 'guide',
                }] if _url_assistente('detalhe_ajuda', topico_slug=topico.get('slug')) else []
            ) + _acoes_assistente_para_paginas(paginas[:3]),
        })

        for indice, item in enumerate(faq_pairs, start=1):
            documentos.append({
                'id': f"faq:{topico.get('slug')}:{indice}",
                'kind': 'faq',
                'page': paginas[0] if paginas else 'ajuda',
                'pages': paginas or ['ajuda'],
                'page_labels': [PAGINAS_SISTEMA.get(pagina, pagina) for pagina in (paginas or ['ajuda'])],
                'section': secao_nome,
                'title': item.get('question'),
                'summary': item.get('answer'),
                'snippet': f"Duvida comum em {topico.get('titulo')}: {item.get('answer')}",
                'keywords': sorted({
                    topico.get('titulo'),
                    secao_nome,
                    topico.get('slug', '').replace('-', ' '),
                    item.get('question'),
                    'duvida comum',
                    'resposta',
                } - {None, ''}),
                'faq_pairs': [item],
                'steps': _deduplicar_textos(topico.get('passos') or []),
                'checklist': _deduplicar_textos(topico.get('checklist') or []),
                'alerts': _deduplicar_textos(topico.get('alertas') or []),
                'problems': problems,
                'source_topic': topico.get('titulo'),
                'url': _url_assistente('detalhe_ajuda', topico_slug=topico.get('slug')),
                'actions': (
                    [{
                        'label': 'Abrir guia detalhado',
                        'url': _url_assistente('detalhe_ajuda', topico_slug=topico.get('slug')),
                        'page': 'ajuda',
                        'reason': topico.get('titulo'),
                        'kind': 'guide',
                    }] if _url_assistente('detalhe_ajuda', topico_slug=topico.get('slug')) else []
                ) + _acoes_assistente_para_paginas(paginas[:3]),
            })

        for indice, item in enumerate(problems, start=1):
            documentos.append({
                'id': f"issue:{topico.get('slug')}:{indice}",
                'kind': 'issue',
                'page': paginas[0] if paginas else 'ajuda',
                'pages': paginas or ['ajuda'],
                'page_labels': [PAGINAS_SISTEMA.get(pagina, pagina) for pagina in (paginas or ['ajuda'])],
                'section': secao_nome,
                'title': item.get('situation'),
                'summary': item.get('action'),
                'snippet': f"Tratativa sugerida em {topico.get('titulo')}: {item.get('action')}",
                'keywords': sorted({
                    topico.get('titulo'),
                    secao_nome,
                    topico.get('slug', '').replace('-', ' '),
                    item.get('situation'),
                    'problema',
                    'nao consigo',
                    'erro',
                } - {None, ''}),
                'faq_pairs': faq_pairs,
                'steps': _deduplicar_textos(topico.get('passos') or []),
                'checklist': _deduplicar_textos(topico.get('checklist') or []),
                'alerts': _deduplicar_textos(topico.get('alertas') or []),
                'problems': [item],
                'source_topic': topico.get('titulo'),
                'url': _url_assistente('detalhe_ajuda', topico_slug=topico.get('slug')),
                'actions': (
                    [{
                        'label': 'Abrir guia detalhado',
                        'url': _url_assistente('detalhe_ajuda', topico_slug=topico.get('slug')),
                        'page': 'ajuda',
                        'reason': topico.get('titulo'),
                        'kind': 'guide',
                    }] if _url_assistente('detalhe_ajuda', topico_slug=topico.get('slug')) else []
                ) + _acoes_assistente_para_paginas(paginas[:3]),
            })

    documentos.append({
        'id': 'topic:home-operacional',
        'kind': 'topic',
        'page': 'inicio',
        'pages': ['inicio', 'pedidos', 'recebimentos', 'expedicao', 'financeiro'],
        'page_labels': [PAGINAS_SISTEMA.get(item, item) for item in ['inicio', 'pedidos', 'recebimentos', 'expedicao', 'financeiro']],
        'section': 'Dashboard',
        'title': 'Home Operacional',
        'summary': 'Painel inicial com prioridades do dia, atalhos e fluxo recomendado.',
        'snippet': 'Use a Home Operacional para ver o que esta pendente, entrar nas filas de trabalho e abrir os atalhos mais usados do seu perfil.',
        'keywords': ['home operacional', 'prioridades', 'pendencias', 'inicio', 'o que fazer hoje'],
        'faq_pairs': [],
        'steps': [],
        'checklist': [],
        'alerts': [],
        'problems': [],
        'url': _url_assistente('boas_vindas'),
        'actions': _acoes_assistente_para_paginas(['inicio', 'ajuda']),
    })

    return documentos


@app.route('/ajuda')
@login_required
def central_ajuda():
    funcionario = get_funcionario_logado()
    perfil_usuario = (funcionario.role if funcionario else 'operador')
    paginas_permitidas = _paginas_permitidas_para_funcionario(funcionario)
    topicos_ajuda = []
    for topico in AJUDA_TOPICOS.values():
        paginas_topico = set(topico.get('paginas') or [])
        if not paginas_topico or paginas_topico.intersection(paginas_permitidas):
            topicos_ajuda.append(topico)

    grupos_ajuda_menu, topicos_ordenados = _organizar_topicos_ajuda_por_menu(topicos_ajuda)

    faq_rapido = []
    for topico in topicos_ordenados:
        for duvida in (topico.get('duvidas') or []):
            faq_rapido.append({
                'topico_slug': topico.get('slug'),
                'topico_titulo': topico.get('titulo'),
                'pergunta': duvida.get('pergunta'),
            })
            if len(faq_rapido) >= 10:
                break
        if len(faq_rapido) >= 10:
            break

    resumo_ajuda = {
        'topicos': len(topicos_ordenados),
        'passos': sum(len(topico.get('passos') or []) for topico in topicos_ordenados),
        'fluxogramas': sum(1 for topico in topicos_ordenados if topico.get('fluxograma')),
    }

    return render_template(
        'sistema/ajuda.html',
        topicos_ajuda=topicos_ordenados,
        grupos_ajuda_menu=grupos_ajuda_menu,
        faq_rapido=faq_rapido,
        resumo_ajuda=resumo_ajuda,
        perfil_usuario=perfil_usuario,
        cargo_usuario=(funcionario.cargo if funcionario else None),
    )


@app.route('/ajuda/<string:topico_slug>')
@login_required
def detalhe_ajuda(topico_slug):
    topico = AJUDA_TOPICOS.get(topico_slug)
    if not topico:
        flash('Topico de ajuda nao encontrado.', 'warning')
        return redirect(url_for('central_ajuda'))

    funcionario = get_funcionario_logado()
    paginas_permitidas = _paginas_permitidas_para_funcionario(funcionario)
    paginas_topico = set(topico.get('paginas') or [])
    if paginas_topico and not paginas_topico.intersection(paginas_permitidas):
        flash('Este guia nao esta disponivel para o seu perfil de acesso.', 'warning')
        return redirect(url_for('central_ajuda'))

    grupo_menu_atual, relacionados = _topicos_relacionados_ajuda(topico, paginas_permitidas)
    return render_template(
        'sistema/ajuda_detalhe.html',
        topico=_enriquecer_topico_ajuda(topico, grupo_menu_atual, _paginas_da_secao_menu(grupo_menu_atual)),
        topicos_relacionados=relacionados,
        grupo_menu_atual=grupo_menu_atual,
    )


# ============ ROTAS - FUNCIONARIOS ============

@app.route('/funcionarios')
@require_role('admin', 'gerente')
def listar_funcionarios():
    page = max(request.args.get('page', 1, type=int), 1)
    per_page = min(max(request.args.get('per_page', 25, type=int), 10), 100)
    busca = (request.args.get('busca') or '').strip()
    role = (request.args.get('role') or '').strip().lower()
    status = (request.args.get('status') or '').strip().lower()
    departamento = (request.args.get('departamento') or '').strip()
    ordenar = (request.args.get('ordenar') or 'nome_asc').strip().lower()

    query = Funcionario.query.options(
        selectinload(Funcionario.superior),
        selectinload(Funcionario.perfil_acesso),
    )
    if busca:
        termo = f'%{busca}%'
        query = query.filter(
            db.or_(
                Funcionario.nome.ilike(termo),
                Funcionario.email.ilike(termo),
                Funcionario.matricula.ilike(termo),
                db.cast(Funcionario.numero_cadastro, db.String).ilike(termo),
                Funcionario.cargo.ilike(termo),
                Funcionario.departamento.ilike(termo),
                Funcionario.time_nome.ilike(termo),
                Funcionario.cpf.ilike(termo),
            )
        )
    if role in ROLES_PERMITIDOS:
        query = query.filter(Funcionario.role == role)
    if status == 'ativos':
        query = query.filter(Funcionario.ativo.is_(True))
    elif status == 'inativos':
        query = query.filter(Funcionario.ativo.is_(False))
    if departamento:
        query = query.filter(Funcionario.departamento == departamento)

    ordenacoes = {
        'nome_asc': (Funcionario.nome.asc(), Funcionario.id.asc()),
        'nome_desc': (Funcionario.nome.desc(), Funcionario.id.desc()),
        'recentes': (Funcionario.criado_em.desc(), Funcionario.id.desc()),
        'cargo': (Funcionario.cargo.asc(), Funcionario.nome.asc()),
        'departamento': (Funcionario.departamento.asc(), Funcionario.nome.asc()),
        'perfil': (Funcionario.role.asc(), Funcionario.nome.asc()),
    }
    if ordenar not in ordenacoes:
        ordenar = 'nome_asc'

    paginacao = query.order_by(*ordenacoes[ordenar]).paginate(page=page, per_page=per_page, error_out=False)
    funcionarios = paginacao.items
    departamentos_disponiveis = sorted({
        (item[0] or '').strip()
        for item in db.session.query(Funcionario.departamento).distinct().all()
        if (item[0] or '').strip()
    }, key=str.lower)
    resumo_funcionarios = {
        'total': Funcionario.query.count(),
        'ativos': Funcionario.query.filter(Funcionario.ativo.is_(True)).count(),
        'inativos': Funcionario.query.filter(Funcionario.ativo.is_(False)).count(),
        'filtrados': paginacao.total,
    }
    return render_template(
        'funcionarios/listar.html',
        funcionarios=funcionarios,
        paginacao=paginacao,
        resumo_funcionarios=resumo_funcionarios,
        departamentos_disponiveis=departamentos_disponiveis,
        filtros={
            'busca': busca,
            'role': role,
            'status': status,
            'departamento': departamento,
            'ordenar': ordenar,
            'per_page': per_page,
        },
        primeiro_funcionario_id=_primeiro_funcionario_id(),
    )


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
        perfil_acesso_id = request.form.get('perfil_acesso_id', type=int)
        cpf = _normalizar_cpf(request.form.get('cpf'))
        rg = _normalizar_campo_organograma(request.form.get('rg'))
        data_nascimento = _parse_date_iso(request.form.get('data_nascimento'))
        celular = _normalizar_campo_organograma(request.form.get('celular'))
        cep = _normalizar_campo_organograma(request.form.get('cep'))
        endereco = _normalizar_campo_organograma(request.form.get('endereco'))
        bairro = _normalizar_campo_organograma(request.form.get('bairro'))
        cidade = _normalizar_campo_organograma(request.form.get('cidade'))
        estado = _normalizar_estado(request.form.get('estado'))
        superior_id = request.form.get('superior_id', type=int)
        departamento = _normalizar_campo_organograma(request.form.get('departamento'))
        time_nome = _normalizar_campo_organograma(request.form.get('time_nome'))
        nivel_organograma = _normalizar_campo_organograma(request.form.get('nivel_organograma'))
        permitir_editar_imagem_perfil = (request.form.get('permitir_editar_imagem_perfil') == 'on')
        vinculos_estoque, erro_vinculos_estoque = _resolver_vinculos_estoque_funcionario(request)
        perfil_acesso = None

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


        if cpf == '__invalid__':
            flash('CPF invalido. Informe 11 digitos.', 'danger')
            return redirect(url_for('criar_funcionario'))
        if cpf and Funcionario.query.filter_by(cpf=cpf).first():
            flash('CPF ja cadastrado para outro funcionario.', 'danger')
            return redirect(url_for('criar_funcionario'))

        if role not in ROLES_PERMITIDOS:
            flash('Tipo de usuario invalido.', 'danger')
            return redirect(url_for('criar_funcionario'))

        if perfil_acesso_id:
            perfil_acesso = PerfilAcesso.query.get(perfil_acesso_id)
            if not perfil_acesso:
                flash('Perfil de acesso padrao invalido.', 'danger')
                return redirect(url_for('criar_funcionario'))

        if nivel_organograma and nivel_organograma not in NIVEIS_ORGANOGRAMA:
            flash('Nivel de organograma invalido.', 'danger')
            return redirect(url_for('criar_funcionario'))

        if erro_vinculos_estoque:
            flash(erro_vinculos_estoque, 'danger')
            return redirect(url_for('criar_funcionario'))

        nivel_hierarquico = nivel_organograma or _role_para_nivel_organograma(role)
        if not superior_id and _deve_exigir_superior_hierarquico(role, nivel_hierarquico):
            flash('Informe o responsavel direto do colaborador para manter o organograma organizado.', 'danger')
            return redirect(url_for('criar_funcionario'))

        superior = None
        if superior_id:
            superior = Funcionario.query.get(superior_id)
            if not superior:
                flash('Superior hierarquico invalido.', 'danger')
                return redirect(url_for('criar_funcionario'))

        novo_funcionario = Funcionario(
            nome=nome,
            email=email,
            matricula=None,
            cpf=(cpf if cpf != '__invalid__' else None),
            rg=rg,
            data_nascimento=data_nascimento,
            celular=celular,
            cep=cep,
            endereco=endereco,
            bairro=bairro,
            cidade=cidade,
            estado=estado,
            permitir_editar_imagem_perfil=permitir_editar_imagem_perfil,
            role=role,
            cargo=cargo or _role_para_cargo_padrao(role),
            perfil_acesso_id=(perfil_acesso.id if perfil_acesso else None),
            departamento=departamento,
            time_nome=time_nome,
            nivel_organograma=nivel_hierarquico,
            restricao_estoques_ativa=bool(vinculos_estoque and vinculos_estoque['restricao_estoques_ativa']),
            estoque_principal_id=(
                vinculos_estoque['estoque_principal'].id
                if vinculos_estoque and vinculos_estoque['estoque_principal']
                else None
            ),
            superior_id=(superior.id if superior else None),
            controle_acesso_ativo=bool(perfil_acesso),
        )
        novo_funcionario.set_password(senha)
        db.session.add(novo_funcionario)
        db.session.flush()
        novo_funcionario.estoques_permitidos = (
            vinculos_estoque['estoques_permitidos']
            if vinculos_estoque else []
        )
        novo_funcionario.numero_cadastro = _gerar_numero_cadastro_unico(novo_funcionario)
        novo_funcionario.matricula = _gerar_matricula_unica(novo_funcionario)
        sincronizar_garcom_funcionario(novo_funcionario)
        db.session.commit()

        flash(f'Funcionario {nome} criado com sucesso!', 'success')
        return redirect(url_for('listar_funcionarios'))

    funcoes_rh = FuncaoRH.query.filter_by(ativo=True).order_by(FuncaoRH.nome.asc()).all()
    perfis_acesso = PerfilAcesso.query.filter_by(ativo=True).order_by(PerfilAcesso.nome.asc()).all()
    superiores = Funcionario.query.filter_by(ativo=True).order_by(Funcionario.nome.asc()).all()
    departamentos_existentes, times_existentes = _listar_cadastros_organograma()
    return render_template(
        'funcionarios/criar.html',
        funcoes_rh=funcoes_rh,
        perfis_acesso=perfis_acesso,
        superiores=superiores,
        estoques_cadastrados=_listar_estoques_para_vinculo_funcionario(),
        estoques_permitidos_ids=[],
        niveis_organograma=NIVEIS_ORGANOGRAMA,
        departamentos_existentes=departamentos_existentes,
        times_existentes=times_existentes,
    )


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
        cpf = _normalizar_cpf(request.form.get('cpf'))
        rg = _normalizar_campo_organograma(request.form.get('rg'))
        data_nascimento = _parse_date_iso(request.form.get('data_nascimento'))
        celular = _normalizar_campo_organograma(request.form.get('celular'))
        cep = _normalizar_campo_organograma(request.form.get('cep'))
        endereco = _normalizar_campo_organograma(request.form.get('endereco'))
        bairro = _normalizar_campo_organograma(request.form.get('bairro'))
        cidade = _normalizar_campo_organograma(request.form.get('cidade'))
        estado = _normalizar_estado(request.form.get('estado'))
        role = _normalizar_texto(request.form.get('role', funcionario.role))
        cargo = (request.form.get('cargo') or '').strip()
        perfil_acesso_id = request.form.get('perfil_acesso_id', type=int)
        superior_id = request.form.get('superior_id', type=int)
        departamento = _normalizar_campo_organograma(request.form.get('departamento'))
        time_nome = _normalizar_campo_organograma(request.form.get('time_nome'))
        nivel_organograma = _normalizar_campo_organograma(request.form.get('nivel_organograma'))
        permitir_editar_imagem_perfil = (request.form.get('permitir_editar_imagem_perfil') == 'on')
        ativo = request.form.get('ativo') == 'on'
        nova_senha = request.form.get('nova_senha', '')
        vinculos_estoque, erro_vinculos_estoque = _resolver_vinculos_estoque_funcionario(request)
        perfil_acesso = None

        if not nome or not email:
            flash('Nome e email são obrigatórios.', 'danger')
            return redirect(url_for('editar_funcionario', funcionario_id=funcionario_id))

        outro_func = Funcionario.query.filter_by(email=email).first()
        if outro_func and outro_func.id != funcionario.id:
            flash('Email ja cadastrado por outro funcionario.', 'danger')
            return redirect(url_for('editar_funcionario', funcionario_id=funcionario_id))


        if cpf == '__invalid__':
            flash('CPF invalido. Informe 11 digitos.', 'danger')
            return redirect(url_for('editar_funcionario', funcionario_id=funcionario_id))
        if cpf:
            outro_cpf = Funcionario.query.filter(
                Funcionario.cpf == cpf,
                Funcionario.id != funcionario.id
            ).first()
            if outro_cpf:
                flash('CPF ja cadastrado para outro funcionario.', 'danger')
                return redirect(url_for('editar_funcionario', funcionario_id=funcionario_id))

        if erro_vinculos_estoque:
            flash(erro_vinculos_estoque, 'danger')
            return redirect(url_for('editar_funcionario', funcionario_id=funcionario_id))

        if perfil_acesso_id:
            perfil_acesso = PerfilAcesso.query.get(perfil_acesso_id)
            if not perfil_acesso:
                flash('Perfil de acesso padrao invalido.', 'danger')
                return redirect(url_for('editar_funcionario', funcionario_id=funcionario_id))

        funcionario.nome = nome
        funcionario.email = email
        funcionario.cpf = cpf if cpf != '__invalid__' else None
        funcionario.rg = rg
        funcionario.data_nascimento = data_nascimento
        funcionario.celular = celular
        funcionario.cep = cep
        funcionario.endereco = endereco
        funcionario.bairro = bairro
        funcionario.cidade = cidade
        funcionario.estado = estado
        funcionario.permitir_editar_imagem_perfil = permitir_editar_imagem_perfil
        funcionario.cargo = cargo or funcionario.cargo or _role_para_cargo_padrao(funcionario.role)
        funcionario.perfil_acesso_id = perfil_acesso.id if perfil_acesso else None
        funcionario.departamento = departamento
        funcionario.time_nome = time_nome
        funcionario.restricao_estoques_ativa = bool(vinculos_estoque and vinculos_estoque['restricao_estoques_ativa'])
        funcionario.estoque_principal_id = (
            vinculos_estoque['estoque_principal'].id
            if vinculos_estoque and vinculos_estoque['estoque_principal']
            else None
        )
        funcionario.estoques_permitidos = (
            vinculos_estoque['estoques_permitidos']
            if vinculos_estoque else []
        )
        funcionario.ativo = ativo
        funcionario.numero_cadastro = _gerar_numero_cadastro_unico(funcionario)
        funcionario.matricula = _gerar_matricula_unica(funcionario)

        if nivel_organograma and nivel_organograma not in NIVEIS_ORGANOGRAMA:
            flash('Nivel de organograma invalido.', 'danger')
            return redirect(url_for('editar_funcionario', funcionario_id=funcionario_id))

        nivel_hierarquico = nivel_organograma or _role_para_nivel_organograma(funcionario.role)
        if not superior_id and _deve_exigir_superior_hierarquico(role if funcionario_logado.role == 'admin' else funcionario.role, nivel_hierarquico):
            flash('Informe o responsavel direto do colaborador para manter o organograma organizado.', 'danger')
            return redirect(url_for('editar_funcionario', funcionario_id=funcionario_id))

        if superior_id == funcionario.id:
            flash('Um funcionario nao pode ser superior de si mesmo.', 'danger')
            return redirect(url_for('editar_funcionario', funcionario_id=funcionario_id))

        superior = None
        if superior_id:
            superior = Funcionario.query.get(superior_id)
            if not superior:
                flash('Superior hierarquico invalido.', 'danger')
                return redirect(url_for('editar_funcionario', funcionario_id=funcionario_id))
            cursor = superior
            visitados = set()
            while cursor:
                if cursor.id in visitados:
                    flash('Hierarquia invalida detectada. Revise o organograma da empresa.', 'danger')
                    return redirect(url_for('editar_funcionario', funcionario_id=funcionario_id))
                visitados.add(cursor.id)
                if cursor.id == funcionario.id:
                    flash('Hierarquia invalida: ciclo detectado na estrutura da empresa.', 'danger')
                    return redirect(url_for('editar_funcionario', funcionario_id=funcionario_id))
                cursor = cursor.superior
        funcionario.superior_id = superior.id if superior else None

        if funcionario_logado.role == 'admin':
            if role not in ROLES_PERMITIDOS:
                flash('Tipo de usuario invalido.', 'danger')
                return redirect(url_for('editar_funcionario', funcionario_id=funcionario_id))
            funcionario.role = role

        if funcionario.role != 'admin' and perfil_acesso:
            funcionario.controle_acesso_ativo = True

        funcionario.nivel_organograma = nivel_hierarquico

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
    perfis_acesso = PerfilAcesso.query.order_by(PerfilAcesso.nome.asc()).all()
    superiores = Funcionario.query.filter(
        Funcionario.id != funcionario.id,
        Funcionario.ativo.is_(True)
    ).order_by(Funcionario.nome.asc()).all()
    departamentos_existentes, times_existentes = _listar_cadastros_organograma()
    return render_template(
        'funcionarios/editar.html',
        funcionario=funcionario,
        funcoes_rh=funcoes_rh,
        funcoes_rh_nomes=[f.nome for f in funcoes_rh],
        perfis_acesso=perfis_acesso,
        superiores=superiores,
        estoques_cadastrados=_listar_estoques_para_vinculo_funcionario(),
        estoques_permitidos_ids=sorted(_estoques_permitidos_ids_funcionario(funcionario) or []),
        niveis_organograma=NIVEIS_ORGANOGRAMA,
        departamentos_existentes=departamentos_existentes,
        times_existentes=times_existentes,
    )


@app.route('/funcionarios/<int:funcionario_id>/deletar', methods=['POST'])
@require_role('admin')
def deletar_funcionario(funcionario_id):
    if funcionario_id == session.get('funcionario_id'):
        flash('Você não pode deletar sua própria conta.', 'danger')
        return redirect(url_for('listar_funcionarios'))

    funcionario = Funcionario.query.get_or_404(funcionario_id)
    try:
        Funcionario.query.filter_by(superior_id=funcionario.id).update(
            {Funcionario.superior_id: None},
            synchronize_session=False
        )
        db.session.delete(funcionario)
        db.session.commit()
        flash(f'Funcionario {funcionario.nome} deletado com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao deletar funcionario: {str(e)}', 'danger')

    return redirect(url_for('listar_funcionarios'))


@app.route('/funcionarios/<int:funcionario_id>/acessos', methods=['GET', 'POST'])
@require_role('admin', 'gerente')
def editar_acessos_funcionario(funcionario_id):
    funcionario = Funcionario.query.get_or_404(funcionario_id)
    funcionario_logado = get_funcionario_logado()
    primeiro_id = _primeiro_funcionario_id()
    estoques_cadastrados = _listar_estoques_para_vinculo_funcionario()
    restricao_estoques_ativa_form = bool(funcionario.restricao_estoques_ativa)
    estoque_principal_id_form = funcionario.estoque_principal_id
    estoques_permitidos_ids = sorted(_estoques_permitidos_ids_funcionario(funcionario) or [])

    if funcionario.id == primeiro_id:
        flash('O primeiro registro do sistema possui acesso protegido e nao pode ser alterado nesta tela.', 'warning')
        return redirect(url_for('listar_funcionarios'))

    if funcionario_logado and funcionario_logado.role == 'gerente':
        if funcionario.role in ['admin', 'gerente'] and funcionario.id != funcionario_logado.id:
            flash('Gerente nao pode alterar acessos de admin/gerente.', 'danger')
            return redirect(url_for('listar_funcionarios'))

    permissoes_atuais = _paginas_efetivas_funcionario(funcionario)
    if request.method == 'POST':
        paginas_enviadas = set(request.form.getlist('paginas'))
        permissoes_atuais = paginas_enviadas
        restricao_estoques_ativa_form = (request.form.get('restricao_estoques_ativa') == 'on')
        estoque_principal_id_form = request.form.get('estoque_principal_id', type=int)
        estoques_permitidos_ids = sorted({
            int(valor)
            for valor in request.form.getlist('estoques_permitidos_ids')
            if str(valor).isdigit()
        } | ({estoque_principal_id_form} if estoque_principal_id_form else set()))
        vinculos_estoque, erro_vinculo = _resolver_vinculos_estoque_funcionario(request)

        if erro_vinculo:
            flash(erro_vinculo, 'danger')
        else:
            try:
                funcionario.restricao_estoques_ativa = vinculos_estoque['restricao_estoques_ativa']
                funcionario.estoque_principal = vinculos_estoque['estoque_principal']
                funcionario.estoques_permitidos = vinculos_estoque['estoques_permitidos']
                funcionario.numero_cadastro = _gerar_numero_cadastro_unico(funcionario)
                funcionario.matricula = _gerar_matricula_unica(funcionario)
                _salvar_permissoes_funcionario(funcionario, paginas_enviadas)
                db.session.commit()
                flash(f'Acessos de {funcionario.nome} atualizados com sucesso.', 'success')
                return redirect(url_for('listar_funcionarios'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao salvar acessos: {str(e)}', 'danger')
    
    permissoes_personalizadas = _mapa_permissoes_personalizadas_funcionario(funcionario)
    permissoes_base = _paginas_perfil_acesso(funcionario.perfil_acesso)
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
        permissoes_atuais=permissoes_atuais,
        permissoes_base=permissoes_base,
        permissoes_personalizadas=permissoes_personalizadas,
        estoques_cadastrados=estoques_cadastrados,
        restricao_estoques_ativa_form=restricao_estoques_ativa_form,
        estoque_principal_id_form=estoque_principal_id_form,
        estoques_permitidos_ids=estoques_permitidos_ids,
    )


@app.route('/rh/funcoes')
@require_role('admin', 'gerente')
def listar_funcoes_rh():
    funcoes = FuncaoRH.query.order_by(FuncaoRH.nome.asc()).all()
    funcionarios_por_cargo = {
        (funcao.nome or '').strip().lower(): Funcionario.query.filter(
            db.func.lower(Funcionario.cargo) == (funcao.nome or '').strip().lower()
        ).count()
        for funcao in funcoes
    }
    cargos_em_uso = Funcionario.query.filter(
        Funcionario.cargo.isnot(None),
        Funcionario.cargo != ''
    ).count()
    return render_template(
        'rh/funcoes.html',
        funcoes=funcoes,
        resumo_cargos={
            'total': len(funcoes),
            'ativas': sum(1 for funcao in funcoes if funcao.ativo),
            'em_uso': cargos_em_uso,
        },
        funcionarios_por_cargo=funcionarios_por_cargo,
    )


@app.route('/rh/perfis')
@require_role('admin', 'gerente')
def listar_perfis_rh():
    perfis_acesso = PerfilAcesso.query.order_by(PerfilAcesso.nome.asc()).all()
    perfis_acesso_permissoes = []
    perfis_sem_paginas = 0
    for perfil in perfis_acesso:
        permissoes = _paginas_perfil_acesso(perfil)
        if not permissoes:
            perfis_sem_paginas += 1
        perfis_acesso_permissoes.append((perfil, permissoes))

    paginas_ordenadas_menu = _paginas_ordenadas_menu()
    funcionarios_por_perfil = {
        perfil.id: Funcionario.query.filter_by(perfil_acesso_id=perfil.id).count()
        for perfil in perfis_acesso
    }
    return render_template(
        'rh/perfis.html',
        perfis_acesso_permissoes=perfis_acesso_permissoes,
        resumo_perfis={
            'total': len(perfis_acesso),
            'ativos': sum(1 for perfil in perfis_acesso if perfil.ativo),
            'com_paginas': sum(1 for _, acessos in perfis_acesso_permissoes if acessos),
            'sem_paginas': perfis_sem_paginas,
        },
        funcionarios_por_perfil=funcionarios_por_perfil,
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
    perfis_acesso_total = PerfilAcesso.query.count()
    perfis_acesso_ativos = PerfilAcesso.query.filter_by(ativo=True).count()

    data_limite = datetime.utcnow() - timedelta(days=30)
    admissoes_30_dias = Funcionario.query.filter(Funcionario.criado_em >= data_limite).count()
    inicio_hoje = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

    distribuicao_roles = db.session.query(
        Funcionario.role.label('role'),
        db.func.count(Funcionario.id).label('quantidade')
    ).group_by(Funcionario.role).order_by(db.desc('quantidade')).all()

    distribuicao_perfis_acesso = [
        {
            'perfil': item.perfil,
            'quantidade': item.quantidade,
        }
        for item in db.session.query(
            PerfilAcesso.nome.label('perfil'),
            db.func.count(Funcionario.id).label('quantidade')
        ).outerjoin(
            Funcionario,
            Funcionario.perfil_acesso_id == PerfilAcesso.id
        ).group_by(PerfilAcesso.id, PerfilAcesso.nome).order_by(db.desc('quantidade'), PerfilAcesso.nome.asc()).all()
    ]
    sem_perfil_padrao = Funcionario.query.filter(Funcionario.perfil_acesso_id.is_(None)).count()
    if sem_perfil_padrao:
        distribuicao_perfis_acesso.append({
            'perfil': 'Sem perfil padrao',
            'quantidade': sem_perfil_padrao,
        })

    distribuicao_cargos = db.session.query(
        Funcionario.cargo.label('cargo'),
        db.func.count(Funcionario.id).label('quantidade'),
        db.func.sum(db.case((Funcionario.ativo.is_(True), 1), else_=0)).label('ativos')
    ).group_by(Funcionario.cargo).order_by(db.desc('quantidade')).all()

    pedidos_pendentes = Pedido.query.filter(
        Pedido.status.in_([Pedido.STATUS_ABERTO, Pedido.STATUS_EM_PREPARO, Pedido.STATUS_ENTREGUE])
    ).count()
    pedidos_hoje = Pedido.query.filter(Pedido.criado_em >= inicio_hoje).count()
    pedidos_30_dias = Pedido.query.filter(Pedido.criado_em >= data_limite).count()
    media_pedidos_dia_30 = (pedidos_30_dias / 30.0) if pedidos_30_dias else 0.0

    equipe_operacao_ativa = Funcionario.query.filter(
        Funcionario.ativo.is_(True),
        Funcionario.role.in_(['caixa', 'operador', 'garcom', 'gerente'])
    ).count()
    pendencias_por_colaborador = (
        pedidos_pendentes / equipe_operacao_ativa
        if equipe_operacao_ativa > 0 else float(pedidos_pendentes)
    )
    equipe_minima_recomendada = max(1, int((pedidos_pendentes + 7) // 8)) if pedidos_pendentes > 0 else 1
    deficit_equipe = max(0, equipe_minima_recomendada - equipe_operacao_ativa)

    funcoes_ativas_lista = FuncaoRH.query.filter_by(ativo=True).all()
    cargos_sem_cobertura = []
    for funcao in funcoes_ativas_lista:
        ativos_no_cargo = Funcionario.query.filter(
            Funcionario.ativo.is_(True),
            db.func.lower(Funcionario.cargo) == (funcao.nome or '').lower()
        ).count()
        if ativos_no_cargo == 0:
            cargos_sem_cobertura.append(funcao.nome)

    acoes_rh = []
    if deficit_equipe > 0:
        acoes_rh.append(f'Ajustar escala imediata: deficit atual de {deficit_equipe} colaborador(es).')
    if pendencias_por_colaborador > 8:
        acoes_rh.append('Revisar capacidade operacional: fila acima de 8 pendencias por colaborador.')
    if funcionarios_inativos > funcionarios_ativos and total_funcionarios > 0:
        acoes_rh.append('Revisar base de colaboradores inativos e normalizar quadro ativo.')
    if cargos_sem_cobertura:
        acoes_rh.append('Priorizar cobertura dos cargos sem pessoas ativas.')
    if perfis_acesso_ativos == 0:
        acoes_rh.append('Cadastrar perfis de acesso padrao para reduzir configuracoes manuais por colaborador.')
    if not acoes_rh:
        acoes_rh.append('Quadro dentro da capacidade atual. Manter monitoramento semanal.')

    funcionarios_recentes = Funcionario.query.options(
        selectinload(Funcionario.perfil_acesso)
    ).order_by(Funcionario.criado_em.desc()).limit(10).all()

    produtividade_map = {}
    pedidos_fechados_periodo = Pedido.query.filter(
        Pedido.status == Pedido.STATUS_FECHADO,
        Pedido.fechado_em.isnot(None),
        Pedido.fechado_em >= data_limite
    ).all()

    for pedido in pedidos_fechados_periodo:
        funcionario_produtividade = None
        if pedido.garcom and pedido.garcom.funcionario:
            funcionario_produtividade = pedido.garcom.funcionario
        elif pedido.caixa and pedido.caixa.funcionario:
            funcionario_produtividade = pedido.caixa.funcionario

        if not funcionario_produtividade:
            continue

        registro = produtividade_map.setdefault(
            funcionario_produtividade.id,
            {
                'nome': funcionario_produtividade.nome,
                'cargo': funcionario_produtividade.cargo or funcionario_produtividade.role.upper(),
                'role': funcionario_produtividade.role,
                'pedidos': 0,
                'itens': 0,
                'faturamento': 0.0,
            }
        )
        registro['pedidos'] += 1
        registro['faturamento'] += float(pedido.total or 0.0)
        registro['itens'] += sum((item.quantidade or 0) for item in (pedido.itens or []))

    produtividade_colaboradores = []
    for registro in produtividade_map.values():
        pedidos = float(registro['pedidos'] or 0)
        itens = float(registro['itens'] or 0)
        faturamento = float(registro['faturamento'] or 0.0)
        registro['ticket_medio'] = (faturamento / pedidos) if pedidos > 0 else 0.0
        registro['pedidos_dia'] = pedidos / 30.0
        registro['indice_produtividade'] = pedidos + (itens / 10.0)
        produtividade_colaboradores.append(registro)

    produtividade_colaboradores = sorted(
        produtividade_colaboradores,
        key=lambda item: (item['indice_produtividade'], item['faturamento']),
        reverse=True
    )
    top_produtividade = produtividade_colaboradores[0] if produtividade_colaboradores else None
    total_pedidos_produtividade = sum(item['pedidos'] for item in produtividade_colaboradores)
    media_pedidos_produtividade = (
        total_pedidos_produtividade / len(produtividade_colaboradores)
        if produtividade_colaboradores else 0.0
    )

    return render_template(
        'rh/indicadores.html',
        total_funcionarios=total_funcionarios,
        funcionarios_ativos=funcionarios_ativos,
        funcionarios_inativos=funcionarios_inativos,
        acessos_controlados=acessos_controlados,
        funcoes_total=funcoes_total,
        funcoes_ativas=funcoes_ativas,
        perfis_acesso_total=perfis_acesso_total,
        perfis_acesso_ativos=perfis_acesso_ativos,
        admissoes_30_dias=admissoes_30_dias,
        pedidos_pendentes=pedidos_pendentes,
        pedidos_hoje=pedidos_hoje,
        pedidos_30_dias=pedidos_30_dias,
        media_pedidos_dia_30=media_pedidos_dia_30,
        equipe_operacao_ativa=equipe_operacao_ativa,
        pendencias_por_colaborador=pendencias_por_colaborador,
        equipe_minima_recomendada=equipe_minima_recomendada,
        deficit_equipe=deficit_equipe,
        acoes_rh=acoes_rh,
        distribuicao_roles=distribuicao_roles,
        distribuicao_perfis_acesso=distribuicao_perfis_acesso,
        distribuicao_cargos=distribuicao_cargos,
        cargos_sem_cobertura=cargos_sem_cobertura,
        funcionarios_recentes=funcionarios_recentes,
        produtividade_colaboradores=produtividade_colaboradores,
        top_produtividade=top_produtividade,
        media_pedidos_produtividade=media_pedidos_produtividade,
    )


@app.route('/rh/organograma')
@login_required
def organograma_rh():
    funcionario_logado = get_funcionario_logado()
    todos_funcionarios = Funcionario.query.filter_by(ativo=True).order_by(Funcionario.nome.asc()).all()
    todos_map = {f.id: f for f in todos_funcionarios}
    filhos_map_total = {}
    for f in todos_funcionarios:
        if f.superior_id and f.superior_id in todos_map:
            filhos_map_total.setdefault(f.superior_id, []).append(f)

    def _ids_visiveis_para_funcionario(funcionario):
        if not funcionario:
            return set()
        role_norm = (funcionario.role or '').strip().lower()
        if role_norm in {'admin', 'gerente'}:
            return {f.id for f in todos_funcionarios}

        ids_visiveis = {funcionario.id}

        cursor = funcionario.superior
        visitados_superiores = set()
        while cursor and cursor.id not in visitados_superiores:
            visitados_superiores.add(cursor.id)
            ids_visiveis.add(cursor.id)
            cursor = cursor.superior

        fila = deque([funcionario.id])
        visitados_desc = set()
        while fila:
            atual_id = fila.popleft()
            if atual_id in visitados_desc:
                continue
            visitados_desc.add(atual_id)
            for filho in filhos_map_total.get(atual_id, []):
                ids_visiveis.add(filho.id)
                fila.append(filho.id)

        return ids_visiveis

    ids_visiveis = _ids_visiveis_para_funcionario(funcionario_logado)
    funcionarios_base = [f for f in todos_funcionarios if f.id in ids_visiveis] if ids_visiveis else todos_funcionarios

    departamentos_disponiveis = sorted({
        (f.departamento or '').strip()
        for f in funcionarios_base
        if (f.departamento or '').strip()
    }, key=str.lower)

    departamento_filtro = (request.args.get('departamento') or '').strip()
    if departamento_filtro:
        funcionarios = [
            f for f in funcionarios_base
            if (f.departamento or '').strip() == departamento_filtro
        ]
    else:
        funcionarios = funcionarios_base

    funcionarios_map = {f.id: f for f in funcionarios}

    role_ordem = {
        'admin': 0,
        'gerente': 1,
        'caixa': 2,
        'operador': 3,
        'garcom': 4,
    }

    def _sort_key(func):
        return (
            role_ordem.get((func.role or '').lower(), 99),
            (func.nivel_organograma or '').lower(),
            (func.cargo or '').lower(),
            (func.nome or '').lower(),
        )

    arvore = {}
    raizes = []
    for funcionario in funcionarios:
        if funcionario.superior_id and funcionario.superior_id in funcionarios_map:
            arvore.setdefault(funcionario.superior_id, []).append(funcionario)
        else:
            raizes.append(funcionario)

    for chave in list(arvore.keys()):
        arvore[chave] = sorted(arvore[chave], key=_sort_key)
    raizes = sorted(raizes, key=_sort_key)

    subordinados_totais = {}

    def _contar_subordinados(funcionario_id, visitados=None):
        if visitados is None:
            visitados = set()
        if funcionario_id in visitados:
            return 0
        visitados.add(funcionario_id)
        total = 0
        for filho in arvore.get(funcionario_id, []):
            total += 1 + _contar_subordinados(filho.id, visitados.copy())
        subordinados_totais[funcionario_id] = total
        return total

    for raiz in raizes:
        _contar_subordinados(raiz.id)
    for funcionario in funcionarios:
        subordinados_totais.setdefault(funcionario.id, len(arvore.get(funcionario.id, [])))

    camadas = {}
    fila = deque((raiz, 0) for raiz in raizes)
    visitados = set()
    while fila:
        funcionario, camada = fila.popleft()
        if funcionario.id in visitados:
            continue
        visitados.add(funcionario.id)
        camadas.setdefault(camada, []).append(funcionario)
        for filho in arvore.get(funcionario.id, []):
            fila.append((filho, camada + 1))

    for funcionario in funcionarios:
        if funcionario.id not in visitados:
            camadas.setdefault(0, []).append(funcionario)

    camadas_organograma = []
    for indice, colaboradores in sorted(camadas.items(), key=lambda item: item[0]):
        colaboradores = sorted(colaboradores, key=_sort_key)
        contagem_niveis = {}
        for colaborador in colaboradores:
            nivel = (colaborador.nivel_organograma or '').strip()
            if not nivel:
                continue
            contagem_niveis[nivel] = contagem_niveis.get(nivel, 0) + 1
        rotulo_camada = max(contagem_niveis, key=contagem_niveis.get) if contagem_niveis else f'Camada {indice + 1}'
        camadas_organograma.append({
            'indice': indice + 1,
            'rotulo': rotulo_camada,
            'colaboradores': colaboradores,
        })

    lideres = [f for f in funcionarios if f.id in arvore]
    sem_superior = [f for f in funcionarios if not f.superior_id or f.superior_id not in funcionarios_map]

    resumo_departamentos_map = {}
    for funcionario in funcionarios:
        departamento_nome = (funcionario.departamento or '').strip() or 'Sem departamento'
        registro = resumo_departamentos_map.setdefault(departamento_nome, {'nome': departamento_nome, 'total': 0, 'lideres': 0})
        registro['total'] += 1
        if funcionario.id in arvore:
            registro['lideres'] += 1

    resumo_departamentos = sorted(
        resumo_departamentos_map.values(),
        key=lambda item: (-item['total'], item['nome'].lower())
    )

    return render_template(
        'rh/organograma.html',
        raizes=raizes,
        arvore=arvore,
        camadas_organograma=camadas_organograma,
        subordinados_totais=subordinados_totais,
        departamentos_disponiveis=departamentos_disponiveis,
        departamento_filtro=departamento_filtro,
        profundidade_maxima=(max(camadas.keys()) + 1 if camadas else 0),
        resumo_departamentos=resumo_departamentos,
        total_colaboradores=len(funcionarios),
        total_lideres=len(lideres),
        total_sem_superior=len(sem_superior),
        modo_visao=('completo' if funcionario_logado and funcionario_logado.role in {'admin', 'gerente'} else 'restrito'),
        funcionario_logado=funcionario_logado,
    )


@app.route('/api/rh/analytics')
@require_role('admin', 'gerente')
def analytics_rh_api():
    periodo = request.args.get('periodo', type=int) or 30
    if periodo not in {30, 90, 365}:
        periodo = 30
    cache = extensions.cache
    cache_key = f'analytics:rh:{periodo}'
    if cache is not None:
        cached_payload = cache.get(cache_key)
        if cached_payload is not None:
            return jsonify(cached_payload)

    data_limite = datetime.utcnow() - timedelta(days=periodo)
    admissoes_periodo = Funcionario.query.filter(Funcionario.criado_em >= data_limite).count()

    distribuicao_roles = db.session.query(
        Funcionario.role.label('role'),
        db.func.count(Funcionario.id).label('quantidade')
    ).group_by(Funcionario.role).order_by(db.desc('quantidade')).all()
    distribuicao_cargos = db.session.query(
        Funcionario.cargo.label('cargo'),
        db.func.count(Funcionario.id).label('quantidade')
    ).group_by(Funcionario.cargo).order_by(db.desc('quantidade')).all()

    pedidos_pendentes = Pedido.query.filter(
        Pedido.status.in_([Pedido.STATUS_ABERTO, Pedido.STATUS_EM_PREPARO, Pedido.STATUS_ENTREGUE])
    ).count()
    equipe_operacao_ativa = Funcionario.query.filter(
        Funcionario.ativo.is_(True),
        Funcionario.role.in_(['caixa', 'operador', 'garcom', 'gerente'])
    ).count()
    pendencias_por_colaborador = (
        pedidos_pendentes / equipe_operacao_ativa
        if equipe_operacao_ativa > 0 else float(pedidos_pendentes)
    )

    ativos_por_dia_raw = db.session.query(
        db.func.date(Funcionario.criado_em).label('dia'),
        db.func.count(Funcionario.id).label('quantidade')
    ).filter(
        Funcionario.criado_em >= data_limite
    ).group_by(db.func.date(Funcionario.criado_em)).order_by(db.func.date(Funcionario.criado_em).asc()).all()

    payload = {
        'success': True,
        'message': 'Analytics RH carregado com sucesso.',
        'data': {
            'periodo_dias': periodo,
            'admissoes_periodo': admissoes_periodo,
            'distribuicao_roles': [
                {'role': item.role, 'quantidade': int(item.quantidade or 0)}
                for item in distribuicao_roles
            ],
            'distribuicao_cargos': [
                {'cargo': item.cargo or '-', 'quantidade': int(item.quantidade or 0)}
                for item in distribuicao_cargos
            ],
            'admissoes_diarias': [
                {'dia': str(item.dia), 'quantidade': int(item.quantidade or 0)}
                for item in ativos_por_dia_raw
            ],
            'pedidos_pendentes': pedidos_pendentes,
            'equipe_operacao_ativa': equipe_operacao_ativa,
            'pendencias_por_colaborador': round(pendencias_por_colaborador, 2),
        }
    }
    if cache is not None:
        cache.set(cache_key, payload, timeout=120)
    return jsonify(payload)


@app.route('/auditoria')
@require_role('admin', 'gerente')
def auditoria_sistema():
    funcionario_id = request.args.get('funcionario_id', type=int)
    acao = (request.args.get('acao') or '').strip()
    entidade = (request.args.get('entidade') or '').strip()
    metodo = (request.args.get('metodo') or '').strip().upper()
    page = max(request.args.get('page', 1, type=int), 1)
    per_page = min(max(request.args.get('per_page', 30, type=int), 10), 100)

    query = AuditoriaEvento.query
    if funcionario_id:
        query = query.filter(AuditoriaEvento.funcionario_id == funcionario_id)
    if acao:
        query = query.filter(AuditoriaEvento.acao.ilike(f'%{acao}%'))
    if entidade:
        query = query.filter(AuditoriaEvento.entidade.ilike(f'%{entidade}%'))
    if metodo in {'GET', 'POST', 'PUT', 'PATCH', 'DELETE'}:
        query = query.filter(AuditoriaEvento.metodo == metodo)

    paginacao = query.order_by(AuditoriaEvento.criado_em.desc()).paginate(page=page, per_page=per_page, error_out=False)
    eventos = paginacao.items
    funcionarios = Funcionario.query.order_by(Funcionario.nome.asc()).all()
    return render_template(
        'sistema/auditoria.html',
        eventos=eventos,
        paginacao=paginacao,
        funcionarios=funcionarios,
        filtros={
            'funcionario_id': funcionario_id,
            'acao': acao,
            'entidade': entidade,
            'metodo': metodo,
            'per_page': per_page,
        }
    )


@app.route('/rh/funcoes/nova', methods=['POST'])
@require_role('admin', 'gerente')
def nova_funcao_rh():
    nome = (request.form.get('nome') or '').strip()
    descricao = (request.form.get('descricao') or '').strip() or None
    ativo = request.form.get('ativo') == 'on'

    if not nome:
        flash('Nome do cargo e obrigatorio.', 'danger')
        return redirect(url_for('listar_funcoes_rh'))

    existente = FuncaoRH.query.filter(db.func.lower(FuncaoRH.nome) == nome.lower()).first()
    if existente:
        flash('Ja existe um cargo com esse nome.', 'warning')
        return redirect(url_for('listar_funcoes_rh'))

    try:
        funcao = FuncaoRH(nome=nome, descricao=descricao, ativo=ativo)
        db.session.add(funcao)
        db.session.commit()
        flash(f'Cargo "{nome}" criado com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao criar cargo: {str(e)}', 'danger')

    return redirect(url_for('listar_funcoes_rh'))


@app.route('/rh/funcoes/<int:funcao_id>/editar', methods=['GET', 'POST'])
@require_role('admin', 'gerente')
def editar_funcao_rh(funcao_id):
    funcao = FuncaoRH.query.get_or_404(funcao_id)
    nome_anterior = funcao.nome

    if request.method == 'POST':
        nome = (request.form.get('nome') or '').strip()
        descricao = (request.form.get('descricao') or '').strip() or None
        ativo = request.form.get('ativo') == 'on'

        if not nome:
            flash('Nome do cargo e obrigatorio.', 'danger')
            return redirect(url_for('editar_funcao_rh', funcao_id=funcao_id))

        existente = FuncaoRH.query.filter(
            db.func.lower(FuncaoRH.nome) == nome.lower(),
            FuncaoRH.id != funcao.id
        ).first()
        if existente:
            flash('Ja existe outro cargo com esse nome.', 'warning')
            return redirect(url_for('editar_funcao_rh', funcao_id=funcao_id))

        try:
            funcao.nome = nome
            funcao.descricao = descricao
            funcao.ativo = ativo
            if (nome_anterior or '').strip().lower() != nome.lower():
                Funcionario.query.filter(
                    db.func.lower(Funcionario.cargo) == (nome_anterior or '').strip().lower()
                ).update({Funcionario.cargo: nome}, synchronize_session=False)
            db.session.commit()
            flash('Cargo atualizado com sucesso!', 'success')
            return redirect(url_for('listar_funcoes_rh'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar cargo: {str(e)}', 'danger')

    return render_template(
        'rh/editar_funcao.html',
        funcao=funcao,
    )


@app.route('/rh/funcoes/<int:funcao_id>/deletar', methods=['POST'])
@require_role('admin', 'gerente')
def deletar_funcao_rh(funcao_id):
    funcao = FuncaoRH.query.get_or_404(funcao_id)
    vinculado = Funcionario.query.filter(
        db.func.lower(Funcionario.cargo) == (funcao.nome or '').strip().lower()
    ).first()
    if vinculado:
        flash('Este cargo ainda está vinculado a colaboradores. Realoque ou edite os cadastros antes de excluir.', 'warning')
        return redirect(url_for('listar_funcoes_rh'))
    try:
        db.session.delete(funcao)
        db.session.commit()
        flash('Cargo removido com sucesso.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao remover cargo: {str(e)}', 'danger')
    return redirect(url_for('listar_funcoes_rh'))


@app.route('/rh/perfis-acesso/novo', methods=['POST'])
@require_role('admin', 'gerente')
def novo_perfil_acesso_rh():
    nome = (request.form.get('nome') or '').strip()
    descricao = (request.form.get('descricao') or '').strip() or None
    ativo = request.form.get('ativo') == 'on'
    permissoes_padrao = _extrair_permissoes_padrao_form()

    if not nome:
        flash('Nome do perfil de acesso é obrigatório.', 'danger')
        return redirect(url_for('listar_perfis_rh'))

    existente = PerfilAcesso.query.filter(db.func.lower(PerfilAcesso.nome) == nome.lower()).first()
    if existente:
        flash('Já existe um perfil de acesso com esse nome.', 'warning')
        return redirect(url_for('listar_perfis_rh'))

    try:
        perfil = PerfilAcesso(
            nome=nome,
            descricao=descricao,
            ativo=ativo,
            permissoes_padrao=_serializar_paginas_json(permissoes_padrao),
        )
        db.session.add(perfil)
        db.session.commit()
        flash(f'Perfil de acesso "{nome}" criado com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao criar perfil de acesso: {str(e)}', 'danger')

    return redirect(url_for('listar_perfis_rh'))


@app.route('/rh/perfis-acesso/<int:perfil_id>/editar', methods=['GET', 'POST'])
@require_role('admin', 'gerente')
def editar_perfil_acesso_rh(perfil_id):
    perfil = PerfilAcesso.query.get_or_404(perfil_id)
    permissoes_atuais = _paginas_perfil_acesso(perfil)

    if request.method == 'POST':
        nome = (request.form.get('nome') or '').strip()
        descricao = (request.form.get('descricao') or '').strip() or None
        ativo = request.form.get('ativo') == 'on'
        permissoes_padrao = _extrair_permissoes_padrao_form()

        if not nome:
            flash('Nome do perfil de acesso é obrigatório.', 'danger')
            return redirect(url_for('editar_perfil_acesso_rh', perfil_id=perfil_id))

        existente = PerfilAcesso.query.filter(
            db.func.lower(PerfilAcesso.nome) == nome.lower(),
            PerfilAcesso.id != perfil.id
        ).first()
        if existente:
            flash('Já existe outro perfil de acesso com esse nome.', 'warning')
            return redirect(url_for('editar_perfil_acesso_rh', perfil_id=perfil_id))

        try:
            perfil.nome = nome
            perfil.descricao = descricao
            perfil.ativo = ativo
            perfil.permissoes_padrao = _serializar_paginas_json(permissoes_padrao)
            db.session.commit()
            flash('Perfil de acesso atualizado com sucesso!', 'success')
            return redirect(url_for('listar_perfis_rh'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar perfil de acesso: {str(e)}', 'danger')

    return render_template(
        'rh/editar_perfil_acesso.html',
        perfil=perfil,
        permissoes_atuais=permissoes_atuais,
        paginas_ordenadas_menu=_paginas_ordenadas_menu(),
        paginas_sistema=PAGINAS_SISTEMA,
    )


@app.route('/rh/perfis-acesso/<int:perfil_id>/deletar', methods=['POST'])
@require_role('admin', 'gerente')
def deletar_perfil_acesso_rh(perfil_id):
    perfil = PerfilAcesso.query.get_or_404(perfil_id)
    colaborador_vinculado = Funcionario.query.filter_by(perfil_acesso_id=perfil.id).first()
    if colaborador_vinculado:
        flash('Este perfil de acesso está vinculado a colaboradores. Remova os vínculos antes de excluir.', 'warning')
        return redirect(url_for('listar_perfis_rh'))
    try:
        db.session.delete(perfil)
        db.session.commit()
        flash('Perfil de acesso removido com sucesso.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao remover perfil de acesso: {str(e)}', 'danger')
    return redirect(url_for('listar_perfis_rh'))


# ============ ROTAS - SERVICOS TECNICOS ============

def _servicos_tecnicos_empresa_ativos():
    empresa = EmpresaConfig.query.first()
    return bool(empresa and empresa.servicos_tecnicos_ativos)


def _funcionarios_tecnicos_montadores():
    funcionarios = Funcionario.query.filter_by(ativo=True).order_by(Funcionario.nome.asc()).all()
    elegiveis = []
    for func in funcionarios:
        cargo_norm = (func.cargo or '').strip().lower()
        role_norm = (func.role or '').strip().lower()
        if role_norm in {'admin', 'gerente'}:
            continue
        if 'tecn' in cargo_norm or 'montador' in cargo_norm or 'instal' in cargo_norm:
            elegiveis.append(func)
    return elegiveis or funcionarios


def _pode_gerir_chamados(funcionario):
    role_norm = ((funcionario.role if funcionario else '') or '').strip().lower()
    return role_norm in {'admin', 'gerente'}


@app.route('/chamados')
@login_required
def listar_chamados_internos():
    funcionario = get_funcionario_logado()
    if not funcionario:
        flash('Sessao invalida. Faca login novamente.', 'danger')
        return redirect(url_for('login'))

    status = (request.args.get('status') or '').strip().lower()
    categoria = (request.args.get('categoria') or '').strip().lower()
    busca = (request.args.get('busca') or '').strip()

    query = ChamadoInterno.query

    if not _pode_gerir_chamados(funcionario):
        query = query.filter(
            db.or_(
                ChamadoInterno.solicitante_id == funcionario.id,
                ChamadoInterno.responsavel_id == funcionario.id,
            )
        )

    if status in ChamadoInterno.STATUS_VALIDOS:
        query = query.filter(ChamadoInterno.status == status)
    if categoria in ChamadoInterno.CATEGORIAS_VALIDAS:
        query = query.filter(ChamadoInterno.categoria == categoria)
    if busca:
        termo = f'%{busca}%'
        query = query.filter(
            db.or_(
                ChamadoInterno.titulo.ilike(termo),
                ChamadoInterno.descricao.ilike(termo),
                db.cast(ChamadoInterno.id, db.String).ilike(termo),
                ChamadoInterno.solicitante.has(Funcionario.nome.ilike(termo)),
                ChamadoInterno.responsavel.has(Funcionario.nome.ilike(termo)),
            )
        )

    chamados = query.order_by(
        db.case((ChamadoInterno.status.in_([ChamadoInterno.STATUS_ABERTO, ChamadoInterno.STATUS_TRIAGEM]), 0), else_=1),
        db.case((ChamadoInterno.prioridade == 'critica', 0), (ChamadoInterno.prioridade == 'alta', 1), (ChamadoInterno.prioridade == 'media', 2), else_=3),
        ChamadoInterno.aberto_em.desc(),
    ).all()

    return render_template(
        'servicos/chamados/listar.html',
        chamados=chamados,
        filtros={'status': status, 'categoria': categoria, 'busca': busca},
        categorias_validas=ChamadoInterno.CATEGORIAS_VALIDAS,
        status_validos=ChamadoInterno.STATUS_VALIDOS,
        prioridades_validas=ChamadoInterno.PRIORIDADES_VALIDAS,
        pode_gerir=_pode_gerir_chamados(funcionario),
    )


@app.route('/chamados/novo', methods=['GET', 'POST'])
@login_required
def criar_chamado_interno():
    funcionario = get_funcionario_logado()
    if not funcionario:
        flash('Sessao invalida. Faca login novamente.', 'danger')
        return redirect(url_for('login'))

    responsaveis = Funcionario.query.filter_by(ativo=True).order_by(Funcionario.nome.asc()).all() if _pode_gerir_chamados(funcionario) else []

    if request.method == 'POST':
        try:
            titulo = (request.form.get('titulo') or '').strip()
            categoria = (request.form.get('categoria') or ChamadoInterno.CATEGORIA_SISTEMA).strip().lower()
            prioridade = (request.form.get('prioridade') or 'media').strip().lower()
            descricao = (request.form.get('descricao') or '').strip()
            setor_origem = (request.form.get('setor_origem') or funcionario.departamento or '').strip() or None
            responsavel_id = request.form.get('responsavel_id', type=int) or None
            status = (request.form.get('status') or ChamadoInterno.STATUS_ABERTO).strip().lower()
            resolucao = (request.form.get('resolucao') or '').strip() or None

            if not titulo or not descricao:
                flash('Titulo e descricao do chamado sao obrigatorios.', 'danger')
                return redirect(url_for('criar_chamado_interno'))
            if categoria not in ChamadoInterno.CATEGORIAS_VALIDAS:
                categoria = ChamadoInterno.CATEGORIA_SISTEMA
            if prioridade not in ChamadoInterno.PRIORIDADES_VALIDAS:
                prioridade = 'media'
            if status not in ChamadoInterno.STATUS_VALIDOS or not _pode_gerir_chamados(funcionario):
                status = ChamadoInterno.STATUS_ABERTO

            responsavel = Funcionario.query.get(responsavel_id) if responsavel_id else None
            if responsavel_id and not responsavel:
                flash('Responsavel invalido.', 'danger')
                return redirect(url_for('criar_chamado_interno'))

            chamado = ChamadoInterno(
                titulo=titulo,
                categoria=categoria,
                prioridade=prioridade,
                status=status,
                descricao=descricao,
                setor_origem=setor_origem,
                solicitante_id=funcionario.id,
                responsavel_id=(responsavel.id if responsavel else None),
                resolucao=resolucao,
            )
            if chamado.status == ChamadoInterno.STATUS_CONCLUIDO:
                chamado.concluido_em = datetime.utcnow()
            db.session.add(chamado)
            db.session.commit()
            flash(f'Chamado #{chamado.id} aberto com sucesso.', 'success')
            return redirect(url_for('listar_chamados_internos'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao abrir chamado: {str(e)}', 'danger')

    return render_template(
        'servicos/chamados/form.html',
        chamado=None,
        categorias_validas=ChamadoInterno.CATEGORIAS_VALIDAS,
        status_validos=ChamadoInterno.STATUS_VALIDOS,
        prioridades_validas=ChamadoInterno.PRIORIDADES_VALIDAS,
        responsaveis=responsaveis,
        pode_gerir=_pode_gerir_chamados(funcionario),
        funcionario_logado=funcionario,
    )


@app.route('/chamados/<int:chamado_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_chamado_interno(chamado_id):
    funcionario = get_funcionario_logado()
    chamado = ChamadoInterno.query.get_or_404(chamado_id)
    pode_gerir = _pode_gerir_chamados(funcionario)

    if not pode_gerir and chamado.solicitante_id != funcionario.id and chamado.responsavel_id != funcionario.id:
        flash('Voce nao tem permissao para acessar este chamado.', 'danger')
        return redirect(url_for('listar_chamados_internos'))

    responsaveis = Funcionario.query.filter_by(ativo=True).order_by(Funcionario.nome.asc()).all() if pode_gerir else []

    if request.method == 'POST':
        try:
            chamado.titulo = (request.form.get('titulo') or chamado.titulo).strip() or chamado.titulo
            categoria = (request.form.get('categoria') or chamado.categoria).strip().lower()
            prioridade = (request.form.get('prioridade') or chamado.prioridade).strip().lower()
            descricao = (request.form.get('descricao') or chamado.descricao).strip() or chamado.descricao
            chamado.setor_origem = (request.form.get('setor_origem') or chamado.setor_origem or '').strip() or None

            if categoria in ChamadoInterno.CATEGORIAS_VALIDAS:
                chamado.categoria = categoria
            if prioridade in ChamadoInterno.PRIORIDADES_VALIDAS:
                chamado.prioridade = prioridade
            chamado.descricao = descricao

            if pode_gerir:
                status = (request.form.get('status') or chamado.status).strip().lower()
                if status in ChamadoInterno.STATUS_VALIDOS:
                    chamado.status = status
                chamado.responsavel_id = request.form.get('responsavel_id', type=int) or None
                chamado.resolucao = (request.form.get('resolucao') or '').strip() or None
                if chamado.status == ChamadoInterno.STATUS_CONCLUIDO:
                    chamado.concluido_em = chamado.concluido_em or datetime.utcnow()
                elif chamado.status != ChamadoInterno.STATUS_CONCLUIDO:
                    chamado.concluido_em = None

            db.session.commit()
            flash(f'Chamado #{chamado.id} atualizado com sucesso.', 'success')
            return redirect(url_for('listar_chamados_internos'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar chamado: {str(e)}', 'danger')

    return render_template(
        'servicos/chamados/form.html',
        chamado=chamado,
        categorias_validas=ChamadoInterno.CATEGORIAS_VALIDAS,
        status_validos=ChamadoInterno.STATUS_VALIDOS,
        prioridades_validas=ChamadoInterno.PRIORIDADES_VALIDAS,
        responsaveis=responsaveis,
        pode_gerir=pode_gerir,
        funcionario_logado=funcionario,
    )


@app.route('/chamados/<int:chamado_id>/status', methods=['POST'])
@login_required
def atualizar_status_chamado_interno(chamado_id):
    funcionario = get_funcionario_logado()
    chamado = ChamadoInterno.query.get_or_404(chamado_id)
    pode_gerir = _pode_gerir_chamados(funcionario)

    if not pode_gerir and chamado.responsavel_id != funcionario.id:
        flash('Voce nao tem permissao para alterar o status deste chamado.', 'danger')
        return redirect(url_for('listar_chamados_internos'))

    novo_status = (request.form.get('status') or '').strip().lower()
    if novo_status not in ChamadoInterno.STATUS_VALIDOS:
        flash('Status invalido.', 'warning')
        return redirect(url_for('listar_chamados_internos'))

    try:
        chamado.status = novo_status
        if not chamado.responsavel_id and funcionario:
            chamado.responsavel_id = funcionario.id
        if novo_status == ChamadoInterno.STATUS_CONCLUIDO:
            chamado.concluido_em = datetime.utcnow()
            chamado.resolucao = (request.form.get('resolucao') or chamado.resolucao or '').strip() or chamado.resolucao
        elif novo_status != ChamadoInterno.STATUS_CONCLUIDO:
            chamado.concluido_em = None
        db.session.commit()
        flash(f'Status do chamado #{chamado.id} atualizado para {novo_status}.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao atualizar status do chamado: {str(e)}', 'danger')
    return redirect(url_for('listar_chamados_internos'))


@app.route('/servicos')
@require_role('admin', 'gerente', 'operador', 'caixa')
def listar_ordens_servico():
    if not _servicos_tecnicos_empresa_ativos():
        flash('Modulo de servicos tecnicos desativado na empresa.', 'warning')
        return redirect(url_for('dashboard'))

    status = (request.args.get('status') or '').strip().lower()
    tipo = (request.args.get('tipo') or '').strip().lower()
    busca = (request.args.get('busca') or '').strip()

    query = OrdemServico.query
    if status in OrdemServico.STATUS_VALIDOS:
        query = query.filter(OrdemServico.status == status)
    if tipo in OrdemServico.TIPOS_VALIDOS:
        query = query.filter(OrdemServico.tipo == tipo)
    if busca:
        termo = f'%{busca}%'
        query = query.filter(
            db.or_(
                OrdemServico.titulo.ilike(termo),
                OrdemServico.descricao.ilike(termo),
                db.cast(OrdemServico.id, db.String).ilike(termo),
                db.cast(OrdemServico.pedido_id, db.String).ilike(termo),
                OrdemServico.funcionario_destino.has(Funcionario.nome.ilike(termo)),
                OrdemServico.produto.has(Produto.nome.ilike(termo)),
            )
        )

    ordens = query.order_by(
        db.case((OrdemServico.status == OrdemServico.STATUS_ABERTA, 0), else_=1),
        OrdemServico.criado_em.desc()
    ).all()

    return render_template(
        'servicos/ordens/listar.html',
        ordens=ordens,
        filtros={'status': status, 'tipo': tipo, 'busca': busca},
        tipos_validos=OrdemServico.TIPOS_VALIDOS,
        status_validos=OrdemServico.STATUS_VALIDOS,
    )


@app.route('/servicos/minhas-ordens')
@login_required
def minhas_ordens_servico():
    funcionario = get_funcionario_logado()
    if not funcionario:
        flash('Sessao invalida. Faca login novamente.', 'danger')
        return redirect(url_for('login'))

    ordens = OrdemServico.query.filter_by(funcionario_destino_id=funcionario.id).order_by(
        db.case((OrdemServico.status.in_([OrdemServico.STATUS_ENVIADA, OrdemServico.STATUS_EM_EXECUCAO]), 0), else_=1),
        OrdemServico.data_agendada.asc().nullsfirst(),
        OrdemServico.criado_em.desc(),
    ).all()

    return render_template(
        'servicos/ordens/minhas.html',
        ordens=ordens,
        funcionario=funcionario,
    )


@app.route('/servicos/nova', methods=['GET', 'POST'])
@require_role('admin', 'gerente', 'operador', 'caixa')
def criar_ordem_servico():
    if not _servicos_tecnicos_empresa_ativos():
        flash('Modulo de servicos tecnicos desativado na empresa.', 'warning')
        return redirect(url_for('dashboard'))

    empresa = EmpresaConfig.query.first()
    produtos = Produto.query.filter_by(ativo=True).order_by(Produto.nome.asc()).all()
    pedidos = Pedido.query.order_by(Pedido.criado_em.desc()).limit(300).all()
    funcionarios_destino = _funcionarios_tecnicos_montadores()
    funcionario_logado = get_funcionario_logado()

    if request.method == 'POST':
        try:
            titulo = (request.form.get('titulo') or '').strip()
            tipo = (request.form.get('tipo') or '').strip().lower()
            status = (request.form.get('status') or OrdemServico.STATUS_ABERTA).strip().lower()
            servico_tipo = (request.form.get('servico_tipo') or OrdemServico.SERVICO_NENHUM).strip().lower()
            prioridade = (request.form.get('prioridade') or '').strip() or None
            descricao = (request.form.get('descricao') or '').strip() or None
            observacoes = (request.form.get('observacoes') or '').strip() or None
            avaria_detalhes = (request.form.get('avaria_detalhes') or '').strip() or None
            inspecao_detalhes = (request.form.get('inspecao_detalhes') or '').strip() or None
            resultado_inspecao = (request.form.get('resultado_inspecao') or '').strip() or None
            produto_id = request.form.get('produto_id', type=int) or None
            pedido_id = request.form.get('pedido_id', type=int) or None
            funcionario_destino_id = request.form.get('funcionario_destino_id', type=int) or None
            data_agendada = _parse_date_iso(request.form.get('data_agendada'))

            if not titulo:
                flash('Titulo da ordem e obrigatorio.', 'danger')
                return redirect(url_for('criar_ordem_servico'))
            if tipo not in OrdemServico.TIPOS_VALIDOS:
                flash('Tipo de ordem invalido.', 'danger')
                return redirect(url_for('criar_ordem_servico'))
            if status not in OrdemServico.STATUS_VALIDOS:
                status = OrdemServico.STATUS_ABERTA
            if servico_tipo not in OrdemServico.SERVICOS_VALIDOS:
                servico_tipo = OrdemServico.SERVICO_NENHUM

            produto = Produto.query.get(produto_id) if produto_id else None
            if produto_id and not produto:
                flash('Produto informado nao existe.', 'danger')
                return redirect(url_for('criar_ordem_servico'))
            pedido = Pedido.query.get(pedido_id) if pedido_id else None
            if pedido_id and not pedido:
                flash('Venda/pedido informado nao existe.', 'danger')
                return redirect(url_for('criar_ordem_servico'))

            if servico_tipo in {OrdemServico.SERVICO_MONTAGEM, OrdemServico.SERVICO_INSTALACAO}:
                if not empresa or not empresa.servico_montagem_instalacao_ativo:
                    flash('Servico de montagem/instalacao nao liberado para a empresa.', 'danger')
                    return redirect(url_for('criar_ordem_servico'))
                if not produto:
                    flash('Selecione um produto para servico de montagem/instalacao.', 'danger')
                    return redirect(url_for('criar_ordem_servico'))
                if servico_tipo == OrdemServico.SERVICO_MONTAGEM and not produto.servico_montagem_disponivel:
                    flash('Produto sem liberacao para servico de montagem.', 'danger')
                    return redirect(url_for('criar_ordem_servico'))
                if servico_tipo == OrdemServico.SERVICO_INSTALACAO and not produto.servico_instalacao_disponivel:
                    flash('Produto sem liberacao para servico de instalacao.', 'danger')
                    return redirect(url_for('criar_ordem_servico'))

            destino = Funcionario.query.get(funcionario_destino_id) if funcionario_destino_id else None
            if funcionario_destino_id and not destino:
                flash('Funcionario de destino invalido.', 'danger')
                return redirect(url_for('criar_ordem_servico'))

            ordem = OrdemServico(
                titulo=titulo,
                tipo=tipo,
                status=status,
                servico_tipo=servico_tipo,
                prioridade=prioridade,
                descricao=descricao,
                observacoes=observacoes,
                avaria_detalhes=avaria_detalhes,
                inspecao_detalhes=inspecao_detalhes,
                resultado_inspecao=resultado_inspecao,
                produto_id=(produto.id if produto else None),
                pedido_id=(pedido.id if pedido else None),
                funcionario_destino_id=(destino.id if destino else None),
                criado_por_id=(funcionario_logado.id if funcionario_logado else None),
                data_agendada=data_agendada,
            )
            if ordem.status in {OrdemServico.STATUS_ENVIADA, OrdemServico.STATUS_EM_EXECUCAO, OrdemServico.STATUS_CONCLUIDA}:
                ordem.enviada_em = datetime.utcnow()
            if ordem.status == OrdemServico.STATUS_CONCLUIDA:
                ordem.concluida_em = datetime.utcnow()
            db.session.add(ordem)
            db.session.commit()
            flash(f'Ordem #{ordem.id} criada com sucesso.', 'success')
            return redirect(url_for('listar_ordens_servico'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao criar ordem: {str(e)}', 'danger')

    return render_template(
        'servicos/ordens/form.html',
        ordem=None,
        produtos=produtos,
        pedidos=pedidos,
        funcionarios_destino=funcionarios_destino,
        tipos_validos=OrdemServico.TIPOS_VALIDOS,
        status_validos=OrdemServico.STATUS_VALIDOS,
        servicos_validos=OrdemServico.SERVICOS_VALIDOS,
        empresa=empresa,
    )


@app.route('/servicos/<int:ordem_id>/editar', methods=['GET', 'POST'])
@require_role('admin', 'gerente', 'operador', 'caixa')
def editar_ordem_servico(ordem_id):
    if not _servicos_tecnicos_empresa_ativos():
        flash('Modulo de servicos tecnicos desativado na empresa.', 'warning')
        return redirect(url_for('dashboard'))

    ordem = OrdemServico.query.get_or_404(ordem_id)
    empresa = EmpresaConfig.query.first()
    produtos = Produto.query.filter_by(ativo=True).order_by(Produto.nome.asc()).all()
    pedidos = Pedido.query.order_by(Pedido.criado_em.desc()).limit(300).all()
    funcionarios_destino = _funcionarios_tecnicos_montadores()

    if request.method == 'POST':
        try:
            ordem.titulo = (request.form.get('titulo') or '').strip() or ordem.titulo
            tipo = (request.form.get('tipo') or ordem.tipo).strip().lower()
            status = (request.form.get('status') or ordem.status).strip().lower()
            servico_tipo = (request.form.get('servico_tipo') or ordem.servico_tipo).strip().lower()
            if tipo in OrdemServico.TIPOS_VALIDOS:
                ordem.tipo = tipo
            if status in OrdemServico.STATUS_VALIDOS:
                ordem.status = status
            if servico_tipo in OrdemServico.SERVICOS_VALIDOS:
                ordem.servico_tipo = servico_tipo
            ordem.prioridade = (request.form.get('prioridade') or '').strip() or None
            ordem.descricao = (request.form.get('descricao') or '').strip() or None
            ordem.observacoes = (request.form.get('observacoes') or '').strip() or None
            ordem.avaria_detalhes = (request.form.get('avaria_detalhes') or '').strip() or None
            ordem.inspecao_detalhes = (request.form.get('inspecao_detalhes') or '').strip() or None
            ordem.resultado_inspecao = (request.form.get('resultado_inspecao') or '').strip() or None
            ordem.data_agendada = _parse_date_iso(request.form.get('data_agendada'))
            ordem.produto_id = request.form.get('produto_id', type=int) or None
            ordem.pedido_id = request.form.get('pedido_id', type=int) or None
            ordem.funcionario_destino_id = request.form.get('funcionario_destino_id', type=int) or None

            produto = Produto.query.get(ordem.produto_id) if ordem.produto_id else None
            if ordem.pedido_id and not Pedido.query.get(ordem.pedido_id):
                flash('Venda/pedido informado nao existe.', 'danger')
                return redirect(url_for('editar_ordem_servico', ordem_id=ordem.id))
            if ordem.servico_tipo in {OrdemServico.SERVICO_MONTAGEM, OrdemServico.SERVICO_INSTALACAO}:
                if not empresa or not empresa.servico_montagem_instalacao_ativo:
                    flash('Servico de montagem/instalacao nao liberado para a empresa.', 'danger')
                    return redirect(url_for('editar_ordem_servico', ordem_id=ordem.id))
                if not produto:
                    flash('Selecione um produto para servico de montagem/instalacao.', 'danger')
                    return redirect(url_for('editar_ordem_servico', ordem_id=ordem.id))
                if ordem.servico_tipo == OrdemServico.SERVICO_MONTAGEM and not produto.servico_montagem_disponivel:
                    flash('Produto sem liberacao para servico de montagem.', 'danger')
                    return redirect(url_for('editar_ordem_servico', ordem_id=ordem.id))
                if ordem.servico_tipo == OrdemServico.SERVICO_INSTALACAO and not produto.servico_instalacao_disponivel:
                    flash('Produto sem liberacao para servico de instalacao.', 'danger')
                    return redirect(url_for('editar_ordem_servico', ordem_id=ordem.id))

            if ordem.status in {OrdemServico.STATUS_ENVIADA, OrdemServico.STATUS_EM_EXECUCAO, OrdemServico.STATUS_CONCLUIDA} and not ordem.enviada_em:
                ordem.enviada_em = datetime.utcnow()
            if ordem.status == OrdemServico.STATUS_CONCLUIDA:
                ordem.concluida_em = datetime.utcnow()
            elif ordem.status != OrdemServico.STATUS_CONCLUIDA:
                ordem.concluida_em = None

            db.session.commit()
            flash(f'Ordem #{ordem.id} atualizada com sucesso.', 'success')
            return redirect(url_for('listar_ordens_servico'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar ordem: {str(e)}', 'danger')

    return render_template(
        'servicos/ordens/form.html',
        ordem=ordem,
        produtos=produtos,
        pedidos=pedidos,
        funcionarios_destino=funcionarios_destino,
        tipos_validos=OrdemServico.TIPOS_VALIDOS,
        status_validos=OrdemServico.STATUS_VALIDOS,
        servicos_validos=OrdemServico.SERVICOS_VALIDOS,
        empresa=empresa,
    )


@app.route('/servicos/<int:ordem_id>/enviar', methods=['POST'])
@require_role('admin', 'gerente', 'operador', 'caixa')
def enviar_ordem_servico(ordem_id):
    if not _servicos_tecnicos_empresa_ativos():
        flash('Modulo de servicos tecnicos desativado na empresa.', 'warning')
        return redirect(url_for('dashboard'))

    ordem = OrdemServico.query.get_or_404(ordem_id)
    if not ordem.funcionario_destino_id:
        flash('Defina um funcionario de destino antes de enviar.', 'warning')
        return redirect(url_for('editar_ordem_servico', ordem_id=ordem.id))
    try:
        ordem.status = OrdemServico.STATUS_ENVIADA
        ordem.enviada_em = datetime.utcnow()
        db.session.commit()
        flash(f'Ordem #{ordem.id} enviada para o colaborador.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao enviar ordem: {str(e)}', 'danger')
    return redirect(url_for('listar_ordens_servico'))


@app.route('/servicos/<int:ordem_id>/tecnico', methods=['GET', 'POST'])
@login_required
def executar_ordem_servico_tecnico(ordem_id):
    funcionario = get_funcionario_logado()
    ordem = OrdemServico.query.get_or_404(ordem_id)

    if not funcionario:
        flash('Sessao invalida. Faca login novamente.', 'danger')
        return redirect(url_for('login'))

    pode_gerir = (funcionario.role or '').strip().lower() in {'admin', 'gerente'}
    if not pode_gerir and ordem.funcionario_destino_id != funcionario.id:
        flash('Voce nao tem permissao para executar esta ordem.', 'danger')
        return redirect(url_for('minhas_ordens_servico'))

    if request.method == 'POST':
        try:
            acao = (request.form.get('acao') or 'salvar').strip().lower()
            retorno_tecnico = (request.form.get('retorno_tecnico') or '').strip() or None
            observacoes_extra = (request.form.get('observacoes') or '').strip() or None
            resultado_inspecao = (request.form.get('resultado_inspecao') or '').strip() or None

            if acao == 'iniciar':
                ordem.status = OrdemServico.STATUS_EM_EXECUCAO
                ordem.iniciado_em = ordem.iniciado_em or datetime.utcnow()
                ordem.enviada_em = ordem.enviada_em or datetime.utcnow()
            elif acao == 'concluir':
                ordem.status = OrdemServico.STATUS_CONCLUIDA
                ordem.iniciado_em = ordem.iniciado_em or datetime.utcnow()
                ordem.concluida_em = datetime.utcnow()
            elif acao == 'aguardar':
                ordem.status = OrdemServico.STATUS_ENVIADA

            ordem.retorno_tecnico = retorno_tecnico
            ordem.observacoes = observacoes_extra
            ordem.resultado_inspecao = resultado_inspecao
            db.session.commit()
            flash(f'Ordem #{ordem.id} atualizada pelo tecnico.', 'success')
            return redirect(url_for('executar_ordem_servico_tecnico', ordem_id=ordem.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao registrar execucao da ordem: {str(e)}', 'danger')

    return render_template(
        'servicos/ordens/tecnico.html',
        ordem=ordem,
        funcionario=funcionario,
        pode_gerir=pode_gerir,
    )


# ============ REGISTRO DE MODULOS DE DOMINIO ============
register_estoque_routes(app, login_required, require_role, aplicar_movimentacao_estoque, _garantir_matriculas_funcionarios)
register_vendas_routes(app, login_required, require_role)
register_public_routes(app)


def _normalizar_historico_assistente(payload_historico):
    historico = []
    for item in payload_historico or []:
        if not isinstance(item, dict):
            continue
        role = (item.get('role') or '').strip().lower()
        text = (item.get('text') or '').strip()
        if role not in {'user', 'assistant'} or not text:
            continue
        historico.append({
            'role': role,
            'text': text[:1000],
        })
        if len(historico) >= 8:
            break
    return historico


def _normalizar_voto_assistente(valor):
    voto = (valor or '').strip().lower()
    if voto in AssistenteLocalFeedback.VOTOS_VALIDOS:
        return voto
    return ''


def _carregar_feedbacks_assistente_local(pagina_atual=None, limite=180):
    query = AssistenteLocalFeedback.query.order_by(AssistenteLocalFeedback.criado_em.desc())
    registros = query.limit(limite).all()
    feedbacks = []
    for item in registros:
        doc_ids = []
        try:
            dados = json.loads(item.matched_doc_ids_json or '[]')
            if isinstance(dados, list):
                doc_ids = [str(valor).strip() for valor in dados if str(valor).strip()]
        except Exception:
            doc_ids = []

        feedbacks.append({
            'vote': item.vote,
            'question': item.question or '',
            'reason': item.reason or '',
            'pagina_atual': item.pagina_atual or '',
            'doc_ids': doc_ids,
        })
    return feedbacks


local_ai_assistant = LocalAIAssistant(app, _construir_documentos_assistente_local)
if app.config.get('LOCAL_AI_ENABLED'):
    local_ai_assistant.start_background_prepare()

register_api_routes(app, {
    'login_required': login_required,
    '_limit': _limit,
    '_parse_date_range': _parse_date_range,
    '_coletar_dashboard_analytics': _coletar_dashboard_analytics,
    'get_funcionario_logado': get_funcionario_logado,
    'ENDPOINT_TO_PAGINA': ENDPOINT_TO_PAGINA,
    'local_ai_assistant_getter': lambda: local_ai_assistant,
    '_normalizar_historico_assistente': _normalizar_historico_assistente,
    '_normalizar_voto_assistente': _normalizar_voto_assistente,
    '_carregar_feedbacks_assistente_local': _carregar_feedbacks_assistente_local,
    '_paginas_permitidas_para_funcionario': _paginas_permitidas_para_funcionario,
    'json_dumps': json.dumps,
})


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

    if getattr(funcionario, 'senha_provisoria', False):
        endpoints_liberados = {
            'dashboard',
            'logout',
            'pwa_manifest',
            'pwa_service_worker',
        }
        if endpoint not in endpoints_liberados:
            flash('Altere a senha temporaria para continuar usando o sistema.', 'warning')
            return redirect(url_for('dashboard'))

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


@app.route('/manifest.webmanifest')
def pwa_manifest():
    empresa = EmpresaConfig.query.first()
    app_name = (empresa.nome_fantasia if empresa and empresa.nome_fantasia else APP_NAME)
    icon_path = (
        (getattr(empresa, 'app_icon_path', None) if empresa else None)
        or (getattr(empresa, 'logo_path', None) if empresa else None)
        or (getattr(empresa, 'favicon_path', None) if empresa else None)
        or (empresa.ecom_favicon_path if empresa else None)
        or 'uploads/empresa/Loja_do_Lucas_logo.png'
    )
    extensao_icone = os.path.splitext(icon_path)[1].lower()
    tipo_icone = {
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.webp': 'image/webp',
        '.ico': 'image/x-icon',
        '.svg': 'image/svg+xml',
    }.get(extensao_icone, 'image/png')
    manifest_data = {
        'name': app_name,
        'short_name': app_name[:12] if len(app_name) > 12 else app_name,
        'description': 'Sistema multiplataforma para operacao, vendas, estoque e expedicao.',
        'start_url': url_for('boas_vindas'),
        'scope': '/',
        'display': 'standalone',
        'background_color': '#f4f7fb',
        'theme_color': '#0f766e',
        'lang': 'pt-BR',
        'icons': [
            {
                'src': url_for('static', filename=icon_path),
                'sizes': '192x192',
                'type': tipo_icone,
                'purpose': 'any maskable',
            },
            {
                'src': url_for('static', filename=icon_path),
                'sizes': '512x512',
                'type': tipo_icone,
                'purpose': 'any maskable',
            },
        ],
    }
    return Response(
        json.dumps(manifest_data, ensure_ascii=False),
        mimetype='application/manifest+json',
    )


@app.route('/manifest-loja.webmanifest')
def store_pwa_manifest():
    empresa = EmpresaConfig.query.first()
    store_name = (empresa.nome_fantasia if empresa and empresa.nome_fantasia else APP_NAME)
    icon_path = (
        (getattr(empresa, 'app_icon_path', None) if empresa else None)
        or (getattr(empresa, 'logo_path', None) if empresa else None)
        or (empresa.ecom_favicon_path if empresa else None)
        or (getattr(empresa, 'favicon_path', None) if empresa else None)
        or 'uploads/empresa/Loja_do_Lucas_logo.png'
    )
    extensao_icone = os.path.splitext(icon_path)[1].lower()
    tipo_icone = {
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.webp': 'image/webp',
        '.ico': 'image/x-icon',
        '.svg': 'image/svg+xml',
    }.get(extensao_icone, 'image/png')
    theme_color = (
        (empresa.ecom_cor_primaria if empresa and empresa.ecom_cor_primaria else None)
        or '#ff7848'
    )
    manifest_data = {
        'id': url_for('index'),
        'name': f'{store_name} Loja',
        'short_name': store_name[:12] if len(store_name) > 12 else store_name,
        'description': 'Loja online com pedido rapido e atalho para abrir como app no celular.',
        'start_url': url_for('index'),
        'scope': '/',
        'display': 'standalone',
        'background_color': '#fffdfa',
        'theme_color': theme_color,
        'lang': 'pt-BR',
        'icons': [
            {
                'src': url_for('static', filename=icon_path),
                'sizes': '192x192',
                'type': tipo_icone,
                'purpose': 'any maskable',
            },
            {
                'src': url_for('static', filename=icon_path),
                'sizes': '512x512',
                'type': tipo_icone,
                'purpose': 'any maskable',
            },
        ],
    }
    return Response(
        json.dumps(manifest_data, ensure_ascii=False),
        mimetype='application/manifest+json',
    )


@app.route('/sw.js')
def pwa_service_worker():
    response = send_from_directory(app.static_folder, 'sw.js', mimetype='application/javascript')
    response.headers['Cache-Control'] = 'no-cache'
    return response


# ============ CONTEXT PROCESSORS ============

@app.context_processor
def inject_user():
    funcionario_logado = get_funcionario_logado()
    empresa_config = EmpresaConfig.query.first()
    atendimento_mesas_ativo = not empresa_config or empresa_config.atendimento_mesas_ativo is not False
    secao_atual_nome, tela_atual_nome = _titulo_tela_atual()
    endpoint_atual = request.endpoint or ''
    estoques_contexto_disponiveis = _estoques_contexto_disponiveis(funcionario_logado) if funcionario_logado else []
    estoque_contexto_id = _estoque_contexto_selecionado_id(funcionario_logado) if funcionario_logado else None
    produto_imagem_padrao_path = (
        (empresa_config.ecom_produto_placeholder_path if empresa_config else None)
        or 'img/placeholders/imgindisponivel.png'
    )
    favicon_path = (
        (empresa_config.favicon_path if empresa_config else None)
        or (empresa_config.ecom_favicon_path if empresa_config else None)
    )
    store_favicon_path = (
        (empresa_config.ecom_favicon_path if empresa_config else None)
        or favicon_path
    )
    app_icon_path = (
        (empresa_config.app_icon_path if empresa_config else None)
        or (empresa_config.logo_path if empresa_config else None)
        or favicon_path
        or 'uploads/empresa/Loja_do_Lucas_logo.png'
    )
    csrf_token_value = ensure_csrf_token()
    paginas_permitidas_usuario = _paginas_permitidas_para_funcionario(funcionario_logado) if funcionario_logado else set()
    assistente_status = (
        local_ai_assistant.status()
        if funcionario_logado and app.config.get('LOCAL_AI_ENABLED') and local_ai_assistant
        else {'enabled': False}
    )
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
        'store_favicon_path': store_favicon_path,
        'app_icon_path': app_icon_path,
        'paginas_permitidas_usuario': paginas_permitidas_usuario,
        'secao_atual_nome': secao_atual_nome,
        'tela_atual_nome': tela_atual_nome,
        'endpoint_atual': endpoint_atual,
        'estoques_contexto_disponiveis': estoques_contexto_disponiveis,
        'estoque_contexto_id': estoque_contexto_id,
        'assistente_local_status': assistente_status,
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


@app.errorhandler(AppError)
def handle_app_error(error):
    mensagem = str(error)
    status_code = getattr(error, 'status_code', 500)
    code = getattr(error, 'code', 'app_error')
    if is_json_request():
        return json_response(False, mensagem, status=status_code, code=code)
    flash(mensagem, 'danger' if status_code >= 400 else 'warning')
    destino = request.referrer
    if request.endpoint == 'login':
        destino = url_for('login')
    return redirect(destino or url_for('dashboard'))


@app.errorhandler(BusinessRuleError)
def handle_business_rule_error(error):
    return handle_app_error(error)


@app.errorhandler(ValidationError)
def handle_validation_error(error):
    return handle_app_error(error)


@app.errorhandler(PermissionDenied)
def handle_permission_denied(error):
    return handle_app_error(error)


@app.errorhandler(NotFound)
def handle_not_found_error(error):
    return handle_app_error(error)


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


