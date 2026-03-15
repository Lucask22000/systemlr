# Relatorio Completo do Backend (para IA)

- Gerado em: 2026-03-15 16:57:55

- Projeto base: `C:/Users/lucas/OneDrive/Desktop/conveniencia`

- Total de arquivos Python mapeados: **50**


## 1) Escopo
- Inclui: `app/`, `routes/`, `utils/` e arquivos Python principais na raiz.
- Exclui: assets frontend, migracoes, ambiente virtual e caches.


## 2) Estrutura de arquivos

- config.py
- fix_admin_access.py
- models.py
- realtime.py
- run.py
- security.py
- seed_data.py
- app/
  - app/__init__.py
  - app/api_routes.py
  - app/auth_routes.py
  - app/blueprints/__init__.py
  - app/blueprints/auth_bp.py
  - app/blueprints/estoque_bp.py
  - app/blueprints/rh_bp.py
  - app/blueprints/sistema_bp.py
  - app/blueprints/vendas_bp.py
  - app/cli.py
  - app/constants.py
  - app/dashboard_routes.py
  - app/decorators.py
  - app/empresa_routes.py
  - app/exceptions.py
  - app/extensions.py
  - app/factory.py
  - app/helpers.py
  - app/rh_routes.py
  - app/services/analytics.py
  - app/services/assistente_service.py
  - app/services/estoque.py
  - app/services/estoque_service.py
  - app/services/financeiro.py
  - app/services/financeiro_service.py
  - app/services/local_ai.py
  - app/services/pedido.py
  - app/services/pedido_service.py
  - app/services/rh.py
  - app/services/rh_service.py
  - app/services/utils.py
  - app/services/utils_service.py
  - app/services_routes.py
  - app/utils/data.py
  - app/utils/helpers.py
  - app/utils/payment_config.py
  - app/utils/validators.py
- routes/
  - routes/__init__.py
  - routes/estoque_routes.py
  - routes/public_routes.py
  - routes/vendas_routes.py
- utils/
  - utils/__init__.py
  - utils/endereco_codigo.py

## 3) Inventario de arquivos

| Arquivo | Linhas | Tamanho (KB) | Hash (sha256-16) |
|---|---:|---:|---|
| `app/__init__.py` | 6149 | 267.4 | `955feb70f03152d7` |
| `app/api_routes.py` | 144 | 6.5 | `2e56d487549b8395` |
| `app/auth_routes.py` | 267 | 13.1 | `280931eea8524d96` |
| `app/blueprints/__init__.py` | 7 | 0.2 | `005d430cecfb715d` |
| `app/blueprints/auth_bp.py` | 5 | 0.1 | `59c3816d462d5708` |
| `app/blueprints/estoque_bp.py` | 5 | 0.1 | `eaf3379106993a93` |
| `app/blueprints/rh_bp.py` | 5 | 0.1 | `b4f2db4f22ee79e0` |
| `app/blueprints/sistema_bp.py` | 5 | 0.1 | `18483a05cd11b629` |
| `app/blueprints/vendas_bp.py` | 5 | 0.1 | `ef9d3102be9f5399` |
| `app/cli.py` | 56 | 2.0 | `d2e251f0b7afced6` |
| `app/constants.py` | 199 | 7.1 | `c8c1120cde5cbf65` |
| `app/dashboard_routes.py` | 3 | 0.1 | `f1bc70fb6c0b7039` |
| `app/decorators.py` | 61 | 2.1 | `69669f232ba0bd43` |
| `app/empresa_routes.py` | 3 | 0.1 | `f1bc70fb6c0b7039` |
| `app/exceptions.py` | 31 | 0.6 | `a88b74fa482fa33b` |
| `app/extensions.py` | 72 | 2.1 | `3c4218b2ab8e9448` |
| `app/factory.py` | 76 | 3.0 | `4db67e55e8dd53d5` |
| `app/helpers.py` | 69 | 2.0 | `abb4f795ca8ba4af` |
| `app/rh_routes.py` | 3 | 0.1 | `f1bc70fb6c0b7039` |
| `app/services/analytics.py` | 313 | 12.2 | `825e0b4a921792f9` |
| `app/services/assistente_service.py` | 5 | 0.1 | `6fe31aabda8282e1` |
| `app/services/estoque.py` | 158 | 5.0 | `4c1834eaa83dc6e5` |
| `app/services/estoque_service.py` | 25 | 0.6 | `8b9e66e8ad786b39` |
| `app/services/financeiro.py` | 60 | 2.5 | `c15f6f98ae49208f` |
| `app/services/financeiro_service.py` | 23 | 0.5 | `2a9c27a9eddf234e` |
| `app/services/local_ai.py` | 917 | 34.2 | `fda4fcf6352b4bbf` |
| `app/services/pedido.py` | 76 | 2.9 | `9368e253db0e0c4f` |
| `app/services/pedido_service.py` | 25 | 0.6 | `87f5dd990df7f75c` |
| `app/services/rh.py` | 55 | 1.5 | `23d4f8058627636a` |
| `app/services/rh_service.py` | 17 | 0.4 | `64fd392456c2a6d7` |
| `app/services/utils.py` | 35 | 0.8 | `834db089c93fe9e9` |
| `app/services/utils_service.py` | 92 | 1.9 | `d704d43e3fe072cf` |
| `app/services_routes.py` | 3 | 0.1 | `f1bc70fb6c0b7039` |
| `app/utils/data.py` | 38 | 1.5 | `134a7ea208ac22eb` |
| `app/utils/helpers.py` | 18 | 0.4 | `611e5a7b506abf6c` |
| `app/utils/payment_config.py` | 199 | 7.3 | `0a6ed1e979bd5372` |
| `app/utils/validators.py` | 106 | 2.6 | `a18b0ba69427ee4d` |
| `config.py` | 57 | 1.4 | `855d0f2f355a7721` |
| `fix_admin_access.py` | 48 | 1.4 | `b0fe4cf4de27aa58` |
| `models.py` | 1149 | 51.3 | `b0a9f464f68ad7b9` |
| `realtime.py` | 30 | 0.7 | `004d2d4fd0c38805` |
| `routes/__init__.py` | 2 | 0.0 | `84b29b334b20301c` |
| `routes/estoque_routes.py` | 3529 | 173.1 | `65d4f14dddab3637` |
| `routes/public_routes.py` | 869 | 31.8 | `18718b91964bcf89` |
| `routes/vendas_routes.py` | 2550 | 106.0 | `b1e387b7544b9ffe` |
| `run.py` | 9 | 0.1 | `0f10c009722e4911` |
| `security.py` | 110 | 3.1 | `82be211f11ec6f6b` |
| `seed_data.py` | 231 | 10.0 | `360da908ebbf99a8` |
| `utils/__init__.py` | 2 | 0.0 | `870bc525a3cbeecd` |
| `utils/endereco_codigo.py` | 502 | 17.8 | `8e379c1cde723bed` |

**Total de linhas backend:** 18418


## 4) Codigo fonte consolidado
Observacao: arquivos muito grandes podem ser truncados para manter o relatorio utilizavel.


### Arquivo: `app/__init__.py`
- Linhas: 6149
- Tamanho: 267.4 KB
- Status: completo

```python
﻿from datetime import datetime, timedelta
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



```


### Arquivo: `app/api_routes.py`
- Linhas: 144
- Tamanho: 6.5 KB
- Status: completo

```python
from flask import Response, jsonify, render_template, request

from models import AssistenteLocalFeedback, db
from security import json_response


def register_routes(app, context):
    login_required = context['login_required']
    limit = context['_limit']
    parse_date_range = context['_parse_date_range']
    coletar_dashboard_analytics = context['_coletar_dashboard_analytics']
    get_funcionario_logado = context['get_funcionario_logado']
    endpoint_to_pagina = context['ENDPOINT_TO_PAGINA']
    local_ai_assistant = context['local_ai_assistant_getter']
    normalizar_historico = context['_normalizar_historico_assistente']
    normalizar_voto = context['_normalizar_voto_assistente']
    carregar_feedbacks = context['_carregar_feedbacks_assistente_local']
    paginas_permitidas = context['_paginas_permitidas_para_funcionario']

    @app.route('/api/dashboard/analytics')
    @login_required
    def dashboard_analytics_api():
        inicio_periodo, fim_periodo, data_inicial_str, data_final_str = parse_date_range(
            request.args.get('data_inicial'),
            request.args.get('data_final'),
            default_days=7
        )
        analytics = coletar_dashboard_analytics(inicio_periodo, fim_periodo)
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

    @app.route('/api/assistente-local/status')
    @login_required
    @limit('60 per minute')
    def assistente_local_status():
        assistant = local_ai_assistant()
        if not app.config.get('LOCAL_AI_ENABLED') or not assistant:
            return json_response(False, 'Assistente local desativado.', status=503, code='assistant_disabled')
        return json_response(True, 'Status do assistente local.', data=assistant.status())

    @app.route('/api/assistente-local/perguntar', methods=['POST'])
    @login_required
    @limit('30 per minute')
    def assistente_local_perguntar():
        assistant = local_ai_assistant()
        if not app.config.get('LOCAL_AI_ENABLED') or not assistant:
            return json_response(False, 'Assistente local desativado.', status=503, code='assistant_disabled')

        payload = request.get_json(silent=True) or {}
        pergunta = (payload.get('pergunta') or '').strip()
        if not pergunta:
            return json_response(False, 'Informe uma pergunta para o assistente local.', status=400, code='assistant_question_required')
        if len(pergunta) > 500:
            return json_response(False, 'Pergunta muito longa. Resuma em ate 500 caracteres.', status=400, code='assistant_question_too_long')

        endpoint_atual = str(payload.get('endpoint_atual') or '').strip()
        endpoint_resolvido = endpoint_atual.split('.')[-1] if endpoint_atual else ''
        pagina_atual = endpoint_to_pagina.get(endpoint_resolvido)
        historico = normalizar_historico(payload.get('historico') or [])
        funcionario = get_funcionario_logado()
        resposta = assistant.answer(
            pergunta,
            paginas_permitidas=paginas_permitidas(funcionario),
            pagina_atual=pagina_atual,
            tela_atual=(payload.get('tela_atual') or '').strip() or None,
            conversation_history=historico,
            feedback_items=carregar_feedbacks(pagina_atual=pagina_atual),
        )
        return json_response(True, 'Resposta do assistente local gerada com sucesso.', data=resposta)

    @app.route('/api/assistente-local/feedback', methods=['POST'])
    @login_required
    @limit('60 per minute')
    def assistente_local_feedback():
        assistant = local_ai_assistant()
        if not app.config.get('LOCAL_AI_ENABLED') or not assistant:
            return json_response(False, 'Assistente local desativado.', status=503, code='assistant_disabled')

        payload = request.get_json(silent=True) or {}
        response_id = (payload.get('response_id') or '').strip()
        vote = normalizar_voto(payload.get('vote'))
        if not response_id:
            return json_response(False, 'Informe a resposta avaliada.', status=400, code='assistant_feedback_response_required')
        if not vote:
            return json_response(False, 'Informe like ou dislike para registrar o feedback.', status=400, code='assistant_feedback_vote_required')

        endpoint_atual = str(payload.get('endpoint_atual') or '').strip()
        endpoint_resolvido = endpoint_atual.split('.')[-1] if endpoint_atual else ''
        pagina_atual = endpoint_to_pagina.get(endpoint_resolvido)
        funcionario = get_funcionario_logado()
        if not funcionario:
            return json_response(False, 'Voce precisa fazer login.', status=401, code='auth_required')

        matched_doc_ids = []
        for item in payload.get('matched_doc_ids') or []:
            texto = str(item).strip()
            if texto:
                matched_doc_ids.append(texto)
            if len(matched_doc_ids) >= 8:
                break

        registro = AssistenteLocalFeedback.query.filter_by(
            funcionario_id=funcionario.id,
            response_id=response_id,
        ).first()
        if not registro:
            registro = AssistenteLocalFeedback(
                funcionario_id=funcionario.id,
                response_id=response_id,
            )
            db.session.add(registro)

        registro.vote = vote
        registro.question = (payload.get('question_text') or '').strip()[:2000] or None
        registro.answer = (payload.get('answer_text') or '').strip()[:5000] or None
        registro.reason = (payload.get('reason') or '').strip()[:255] or None
        registro.endpoint_atual = endpoint_resolvido or None
        registro.pagina_atual = pagina_atual or None
        registro.tela_atual = (payload.get('tela_atual') or '').strip()[:120] or None
        registro.matched_doc_ids_json = context['json_dumps'](matched_doc_ids)

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            return json_response(False, 'Nao foi possivel salvar o feedback agora.', status=500, code='assistant_feedback_save_failed')

        return json_response(True, 'Feedback da assistente registrado com sucesso.', data={
            'vote': registro.vote,
            'response_id': registro.response_id,
        })

```


### Arquivo: `app/auth_routes.py`
- Linhas: 267
- Tamanho: 13.1 KB
- Status: completo

```python
from flask import flash, redirect, render_template, request, session, url_for

from models import FuncaoRH, Funcionario, PerfilAcesso, db


def register_routes(app, context):
    login_required = context['login_required']
    limit = context['_limit']
    client_ip = context['_client_ip']
    is_login_rate_limited = context['_is_login_rate_limited']
    register_login_attempt = context['_register_login_attempt']
    get_funcionario_logado = context['get_funcionario_logado']
    normalizar_texto = context['_normalizar_texto']
    normalizar_matricula = context['_normalizar_matricula']
    normalizar_cpf = context['_normalizar_cpf']
    normalizar_campo_organograma = context['_normalizar_campo_organograma']
    normalizar_estado = context['_normalizar_estado']
    parse_date_iso = context['_parse_date_iso']
    role_para_cargo_padrao = context['_role_para_cargo_padrao']
    role_para_nivel_organograma = context['_role_para_nivel_organograma']
    gerar_numero_cadastro_unico = context['_gerar_numero_cadastro_unico']
    gerar_matricula_unica = context['_gerar_matricula_unica']
    listar_cadastros_organograma = context['_listar_cadastros_organograma']
    sincronizar_garcom_funcionario = context['sincronizar_garcom_funcionario']
    registrar_evento_auditoria = context['registrar_evento_auditoria']
    bootstrap_admin_configurado = context['_bootstrap_admin_configurado']
    primeiro_acesso_email = context['PRIMEIRO_ACESSO_EMAIL']
    roles_permitidos = context['ROLES_PERMITIDOS']
    niveis_organograma = context['NIVEIS_ORGANOGRAMA']
    extensions = context['extensions']

    @app.route('/login', methods=['GET', 'POST'])
    @limit('10 per 5 minute')
    def login():
        if request.method == 'POST':
            ip_addr = client_ip()
            if extensions.limiter is None and is_login_rate_limited(ip_addr):
                flash('Muitas tentativas de login. Tente novamente em alguns minutos.', 'danger')
                registrar_evento_auditoria(
                    funcionario=None,
                    acao='login_rate_limited',
                    entidade='autenticacao',
                    detalhes=f'ip={ip_addr}',
                    status_code=429
                )
                return redirect(url_for('login'))

            identificador = (request.form.get('login') or request.form.get('email') or '').strip()
            senha = request.form.get('senha', '')

            if not identificador or not senha:
                flash('Matricula/email e senha sao obrigatorios.', 'danger')
                return redirect(url_for('login'))

            identificador_norm = identificador.lower()
            matricula_norm = normalizar_matricula(identificador)
            funcionario = Funcionario.query.filter(
                db.or_(
                    db.func.lower(Funcionario.email) == identificador_norm,
                    db.func.lower(Funcionario.matricula) == (matricula_norm.lower() if matricula_norm else identificador_norm),
                )
            ).first()

            if funcionario and funcionario.check_password(senha):
                if not funcionario.ativo:
                    register_login_attempt(ip_addr, success=False)
                    registrar_evento_auditoria(
                        funcionario=funcionario,
                        acao='login_bloqueado_inativo',
                        entidade='autenticacao',
                        detalhes=f'identificador={identificador}',
                        status_code=403
                    )
                    flash('Usuário inativo. Contate um administrador.', 'danger')
                    return redirect(url_for('login'))

                session['funcionario_id'] = funcionario.id
                session['funcionario_nome'] = funcionario.nome
                session['funcionario_role'] = funcionario.role
                db.session.commit()
                register_login_attempt(ip_addr, success=True)
                registrar_evento_auditoria(
                    funcionario=funcionario,
                    acao='login_sucesso',
                    entidade='autenticacao',
                    detalhes=f'identificador={identificador}',
                    status_code=200
                )

                if getattr(funcionario, 'senha_provisoria', False):
                    flash('Sua senha temporaria deve ser alterada antes de continuar.', 'warning')
                    return redirect(url_for('dashboard'))

                flash(f'Bem-vindo, {funcionario.nome}!', 'success')
                return redirect(url_for('boas_vindas'))

            register_login_attempt(ip_addr, success=False)
            registrar_evento_auditoria(
                funcionario=None,
                acao='login_falha',
                entidade='autenticacao',
                detalhes=f'identificador={identificador}',
                status_code=401
            )
            flash('Matricula/email ou senha incorretos.', 'danger')
            return redirect(url_for('login'))

        funcionario_admin_inicial = Funcionario.query.filter(
            db.func.lower(Funcionario.email) == primeiro_acesso_email.lower()
        ).order_by(Funcionario.id.asc()).first()
        mostrar_credenciais_iniciais = bool(
            bootstrap_admin_configurado()
            and getattr(funcionario_admin_inicial, 'senha_provisoria', False)
            and funcionario_admin_inicial
            and Funcionario.query.count() == 1
        )
        return render_template(
            'sistema/login.html',
            mostrar_credenciais_iniciais=mostrar_credenciais_iniciais,
            primeiro_acesso_email=primeiro_acesso_email,
        )

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
        return redirect(url_for('index'))

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
            role = normalizar_texto(request.form.get('role', 'operador'))
            cargo = (request.form.get('cargo') or '').strip()
            cpf = normalizar_cpf(request.form.get('cpf'))
            rg = normalizar_campo_organograma(request.form.get('rg'))
            data_nascimento = parse_date_iso(request.form.get('data_nascimento'))
            celular = normalizar_campo_organograma(request.form.get('celular'))
            cep = normalizar_campo_organograma(request.form.get('cep'))
            endereco = normalizar_campo_organograma(request.form.get('endereco'))
            bairro = normalizar_campo_organograma(request.form.get('bairro'))
            cidade = normalizar_campo_organograma(request.form.get('cidade'))
            estado = normalizar_estado(request.form.get('estado'))
            departamento = normalizar_campo_organograma(request.form.get('departamento'))
            time_nome = normalizar_campo_organograma(request.form.get('time_nome'))
            nivel_organograma = normalizar_campo_organograma(request.form.get('nivel_organograma'))
            permitir_editar_imagem_perfil = (request.form.get('permitir_editar_imagem_perfil') == 'on')
            perfil_acesso_id = request.form.get('perfil_acesso_id', type=int)
            perfil_acesso = None

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
            if cpf == '__invalid__':
                flash('CPF invalido. Informe 11 digitos.', 'danger')
                return redirect(url_for('registro'))
            if cpf and Funcionario.query.filter_by(cpf=cpf).first():
                flash('CPF ja cadastrado para outro funcionario.', 'danger')
                return redirect(url_for('registro'))
            if nivel_organograma and nivel_organograma not in niveis_organograma:
                flash('Nivel de organograma invalido.', 'danger')
                return redirect(url_for('registro'))

            if perfil_acesso_id:
                perfil_acesso = PerfilAcesso.query.get(perfil_acesso_id)
                if not perfil_acesso:
                    flash('Perfil de acesso invalido.', 'danger')
                    return redirect(url_for('registro'))

            novo_funcionario = Funcionario(nome=nome, email=email)
            novo_funcionario.set_password(senha)
            novo_funcionario.matricula = None
            novo_funcionario.cpf = cpf if cpf != '__invalid__' else None
            novo_funcionario.rg = rg
            novo_funcionario.data_nascimento = data_nascimento
            novo_funcionario.celular = celular
            novo_funcionario.cep = cep
            novo_funcionario.endereco = endereco
            novo_funcionario.bairro = bairro
            novo_funcionario.cidade = cidade
            novo_funcionario.estado = estado
            novo_funcionario.permitir_editar_imagem_perfil = permitir_editar_imagem_perfil

            if total_funcionarios == 0:
                novo_funcionario.role = 'admin'
                novo_funcionario.cargo = 'Administrador'
                novo_funcionario.departamento = departamento or 'Diretoria'
                novo_funcionario.time_nome = time_nome or 'Gestao'
                novo_funcionario.nivel_organograma = nivel_organograma or 'Diretoria'
                novo_funcionario.perfil_acesso_id = None
                novo_funcionario.controle_acesso_ativo = False
            elif role in roles_permitidos:
                novo_funcionario.role = role
                novo_funcionario.cargo = cargo or role_para_cargo_padrao(role)
                novo_funcionario.departamento = departamento
                novo_funcionario.time_nome = time_nome
                novo_funcionario.nivel_organograma = nivel_organograma or role_para_nivel_organograma(role)
                novo_funcionario.perfil_acesso_id = perfil_acesso.id if perfil_acesso else None
                novo_funcionario.controle_acesso_ativo = bool(perfil_acesso)
            else:
                flash('Tipo de usuario invalido.', 'danger')
                return redirect(url_for('registro'))

            db.session.add(novo_funcionario)
            db.session.flush()
            novo_funcionario.numero_cadastro = gerar_numero_cadastro_unico(novo_funcionario)
            if not novo_funcionario.matricula:
                novo_funcionario.matricula = gerar_matricula_unica(novo_funcionario)
            sincronizar_garcom_funcionario(novo_funcionario)
            db.session.commit()

            if total_funcionarios == 0:
                flash(f'Conta do administrador criada com sucesso! Bem-vindo, {nome}!', 'success')
                session['funcionario_id'] = novo_funcionario.id
                session['funcionario_nome'] = novo_funcionario.nome
                session['funcionario_role'] = novo_funcionario.role
                return redirect(url_for('boas_vindas'))

            flash(f'Funcionario {nome} registrado com sucesso!', 'success')
            return redirect(url_for('listar_funcionarios'))

        funcoes_rh = FuncaoRH.query.filter_by(ativo=True).order_by(FuncaoRH.nome.asc()).all()
        perfis_acesso = PerfilAcesso.query.filter_by(ativo=True).order_by(PerfilAcesso.nome.asc()).all()
        departamentos_existentes, times_existentes = listar_cadastros_organograma()
        return render_template(
            'sistema/registro.html',
            primeira_vez=(total_funcionarios == 0),
            funcoes_rh=funcoes_rh,
            perfis_acesso=perfis_acesso,
            niveis_organograma=niveis_organograma,
            departamentos_existentes=departamentos_existentes,
            times_existentes=times_existentes,
        )

```


### Arquivo: `app/blueprints/__init__.py`
- Linhas: 7
- Tamanho: 0.2 KB
- Status: completo

```python
"""Blueprints de dominio do SystemLR.

Nesta fase, o projeto preserva as rotas legadas existentes e disponibiliza
os blueprints para migração incremental sem quebra de compatibilidade.
"""


```


### Arquivo: `app/blueprints/auth_bp.py`
- Linhas: 5
- Tamanho: 0.1 KB
- Status: completo

```python
from flask import Blueprint


auth_bp = Blueprint('auth_bp', __name__)

```


### Arquivo: `app/blueprints/estoque_bp.py`
- Linhas: 5
- Tamanho: 0.1 KB
- Status: completo

```python
from flask import Blueprint


estoque_bp = Blueprint('estoque_bp', __name__)

```


### Arquivo: `app/blueprints/rh_bp.py`
- Linhas: 5
- Tamanho: 0.1 KB
- Status: completo

```python
from flask import Blueprint


rh_bp = Blueprint('rh_bp', __name__)

```


### Arquivo: `app/blueprints/sistema_bp.py`
- Linhas: 5
- Tamanho: 0.1 KB
- Status: completo

```python
from flask import Blueprint


sistema_bp = Blueprint('sistema_bp', __name__)

```


### Arquivo: `app/blueprints/vendas_bp.py`
- Linhas: 5
- Tamanho: 0.1 KB
- Status: completo

```python
from flask import Blueprint


vendas_bp = Blueprint('vendas_bp', __name__)

```


### Arquivo: `app/cli.py`
- Linhas: 56
- Tamanho: 2.0 KB
- Status: completo

```python
import os

import click
import qrcode

from models import Funcionario, Mesa, db


def register_cli(app):
    """Registra comandos Flask CLI para operacoes administrativas."""

    @app.cli.command('seed-data')
    def seed_data_command():
        """Popula o banco com dados de exemplo."""
        from seed_data import seed_database

        seed_database()
        click.echo('Seed finalizado.')

    @app.cli.command('fix-admin')
    @click.option('--email', default=lambda: os.environ.get('SYSTEMLR_ADMIN_EMAIL', 'admin@conveniencia.local'))
    @click.option('--senha', default=lambda: os.environ.get('SYSTEMLR_ADMIN_PASSWORD', '142536'))
    @click.option('--nome', default=lambda: os.environ.get('SYSTEMLR_ADMIN_NAME', 'Administrador'))
    def fix_admin_command(email, senha, nome):
        """Cria/atualiza usuario admin."""
        admin = Funcionario.query.filter_by(email=email).first()
        if admin:
            admin.nome = nome
            admin.role = 'admin'
            admin.ativo = True
            admin.set_password(senha)
        else:
            admin = Funcionario(nome=nome, email=email, role='admin', ativo=True)
            admin.set_password(senha)
            db.session.add(admin)
        db.session.commit()
        click.echo(f'Admin pronto: {email}')

    @app.cli.command('generate-qrcodes')
    @click.option('--base-url', default='http://localhost:5000', show_default=True)
    @click.option('--out-dir', default='qrcodes', show_default=True)
    def generate_qrcodes_command(base_url, out_dir):
        """Gera QR codes para mesas com token."""
        os.makedirs(out_dir, exist_ok=True)
        mesas = Mesa.query.all()
        total = 0
        for mesa in mesas:
            if not mesa.qr_token:
                continue
            url = f'{base_url.rstrip("/")}/m/{mesa.qr_token}'
            img = qrcode.make(url)
            filename = os.path.join(out_dir, f'mesa_{mesa.numero}.png')
            img.save(filename)
            total += 1
        click.echo(f'QR codes gerados: {total}')

```


### Arquivo: `app/constants.py`
- Linhas: 199
- Tamanho: 7.1 KB
- Status: completo

```python
"""Constantes de domínio do SystemLR."""

TIPOS_MOVIMENTACAO_VALIDOS = {'entrada', 'saida'}
ROLES_PERMITIDOS = {'admin', 'gerente', 'caixa', 'operador', 'garcom'}
NIVEIS_ORGANOGRAMA = (
    'Diretoria',
    'Gerencia',
    'Coordenacao',
    'Supervisao',
    'Especialista',
    'Operacao',
)

CARGOS_PERMANENTES = (
    ('Garcom', 'Atendimento de mesas e acompanhamento de pedidos.'),
)

PAGINAS_SISTEMA = {
    'inicio': 'Meu Perfil',
    'gestao_negocio': 'Gestao do Negocio',
    'financeiro': 'Financeiro',
    'pdv': 'PDV',
    'estoques': 'Estoques',
    'produtos': 'Produtos',
    'categorias': 'Categorias',
    'fornecedores': 'Fornecedores',
    'enderecos_estoque': 'Enderecos de Estoque',
    'movimentacoes': 'Entradas e Saidas Internas',
    'almoxarifado': 'Almoxarifado',
    'recebimentos': 'Recebimentos Operacionais',
    'relatorios': 'Relatorios',
    'equipamentos_estoque': 'Equipamentos de Movimentacao',
    'enderecos_inteligentes': 'Enderecos Inteligentes',
    'caixas': 'Caixas',
    'mesas': 'Mesas',
    'pedidos': 'Pedidos',
    'expedicao': 'Expedicao',
    'transferencias_estoque': 'Transferencias entre Lojas e CDs',
    'funcionarios': 'Funcionarios',
    'rh_funcoes': 'RH - Cargos e Perfis',
    'rh_indicadores': 'RH - Indicadores',
    'rh_organograma': 'RH - Organograma',
    'auditoria': 'Auditoria',
    'empresa': 'Empresa',
    'ecommerce_config': 'E-commerce - Ativacao e Configuracao',
    'servicos_tecnicos': 'Servicos Tecnicos',
    'chamados_internos': 'Chamados Internos',
    'garcons': 'Garcons',
    'ajuda': 'Ajuda e Treinamento',
}

PAGINAS_SISTEMA_MENU_ORDEM = (
    ('Dashboard', ('inicio',)),
    ('Gestao', ('gestao_negocio', 'empresa')),
    ('Financeiro', ('financeiro',)),
    ('Vendas', ('pdv', 'pedidos', 'mesas', 'caixas', 'garcons')),
    ('Estoque', ('estoques', 'produtos', 'categorias', 'enderecos_estoque', 'enderecos_inteligentes', 'equipamentos_estoque', 'movimentacoes', 'almoxarifado', 'relatorios')),
    ('Recebimento', ('fornecedores', 'recebimentos')),
    ('Expedicao', ('expedicao', 'transferencias_estoque')),
    ('Meu RH', ('rh_indicadores', 'rh_organograma', 'funcionarios', 'rh_funcoes', 'auditoria')),
    ('E-commerce', ('ecommerce_config',)),
    ('Servicos', ('servicos_tecnicos', 'chamados_internos')),
    ('Ajuda', ('ajuda',)),
)

PAGINA_ENDPOINTS = {
    'inicio': {'dashboard', 'boas_vindas'},
    'gestao_negocio': {'gestao_negocio'},
    'financeiro': {
        'financeiro',
        'dashboard_analytics_api',
        'financeiro_lancamentos',
        'financeiro_fundos',
        'marcar_lancamento_enviado_contador',
        'exportar_lancamentos_financeiros',
        'exportar_lancamentos_financeiros_xlsx',
    },
    'pdv': {
        'pdv',
        'criar_pedido_api',
        'finalizar_pedido_api',
        'get_pedido_aberto',
        'listar_pedidos_em_aberto_pdv',
        'listar_pedidos_caixa_em_aberto',
        'detalhes_pedido_api',
        'adicionar_itens_pedido_api',
        'sse_pedidos',
    },
    'estoques': {'listar_estoques', 'novo_estoque', 'editar_estoque', 'deletar_estoque'},
    'produtos': {'listar_produtos', 'novo_produto', 'editar_produto', 'visualizar_produto', 'deletar_produto', 'imprimir_etiquetas_loja'},
    'categorias': {'listar_categorias', 'nova_categoria', 'editar_categoria', 'deletar_categoria'},
    'fornecedores': {'listar_fornecedores', 'detalhes_fornecedor', 'novo_fornecedor', 'editar_fornecedor', 'deletar_fornecedor'},
    'enderecos_estoque': {
        'listar_enderecos_estoque',
        'novo_endereco_estoque',
        'editar_endereco_estoque',
        'deletar_endereco_estoque',
        'detalhes_endereco_estoque',
        'imprimir_etiqueta_endereco_estoque',
        'imprimir_etiquetas_enderecos_estoque',
    },
    'enderecos_inteligentes': {
        'enderecos_inteligentes',
        'enderecar_produto_inteligente',
        'marcar_produto_fora_picking',
        'baixar_produto_para_picking',
    },
    'equipamentos_estoque': {
        'listar_equipamentos_movimentacao',
        'novo_equipamento_movimentacao',
        'editar_equipamento_movimentacao',
    },
    'movimentacoes': {
        'listar_movimentacoes',
        'nova_movimentacao',
        'movimentacao_rapida',
    },
    'almoxarifado': {
        'listar_almoxarifado',
        'nova_atribuicao_almoxarifado',
    },
    'recebimentos': {
        'listar_recebimentos_fornecedor',
        'novo_recebimento_fornecedor',
        'conferir_recebimento_fornecedor',
        'armazenar_recebimento_fornecedor',
        'cancelar_recebimento_fornecedor',
    },
    'relatorios': {'relatorios', 'analytics_estoque_api'},
    'caixas': {'listar_caixas', 'nova_caixa', 'editar_caixa', 'deletar_caixa', 'abrir_caixa', 'fechar_caixa', 'historico_caixa'},
    'mesas': {'listar_mesas', 'nova_mesa', 'editar_mesa', 'deletar_mesa', 'visualizar_qrcode_mesa', 'download_qrcode_mesa', 'print_qrcode_mesa'},
    'pedidos': {
        'listar_pedidos',
        'listar_pedidos_pendentes',
        'novo_pedido',
        'editar_pedido',
        'deletar_pedido',
        'visualizar_comprovante_pedido',
        'detalhes_pedido',
        'alterar_status_pedido',
    },
    'expedicao': {
        'central_expedicao',
        'frota_expedicao',
        'coletor_estoque',
        'listar_separacao_entrega',
        'listar_roteirizacao_entrega',
        'painel_expedicao',
        'iniciar_processo_expedicao',
        'api_progresso_expedicao',
        'otimizar_rota_entrega',
        'atualizar_despacho_entrega',
        'atualizar_separacao_entrega_pedido',
        'imprimir_etiqueta_entrega_pedido',
    },
    'transferencias_estoque': {
        'listar_transferencias_estoque',
        'transferir_armazenamento',
    },
    'funcionarios': {'listar_funcionarios', 'criar_funcionario', 'editar_funcionario', 'deletar_funcionario', 'editar_acessos_funcionario'},
    'rh_funcoes': {
        'listar_funcoes_rh',
        'listar_perfis_rh',
        'nova_funcao_rh',
        'editar_funcao_rh',
        'deletar_funcao_rh',
        'novo_perfil_acesso_rh',
        'editar_perfil_acesso_rh',
        'deletar_perfil_acesso_rh',
    },
    'rh_indicadores': {'indicadores_rh', 'analytics_rh_api'},
    'rh_organograma': {'organograma_rh'},
    'auditoria': {'auditoria_sistema'},
    'empresa': {'editar_empresa', 'preview_cardapio_empresa'},
    'ecommerce_config': {'configurar_ecommerce', 'configurar_ativacao_ecommerce'},
    'servicos_tecnicos': {
        'listar_ordens_servico',
        'minhas_ordens_servico',
        'criar_ordem_servico',
        'editar_ordem_servico',
        'enviar_ordem_servico',
        'executar_ordem_servico_tecnico',
    },
    'chamados_internos': {
        'listar_chamados_internos',
        'criar_chamado_interno',
        'editar_chamado_interno',
        'atualizar_status_chamado_interno',
    },
    'garcons': {'listar_garcons', 'novo_garcom', 'editar_garcom', 'deletar_garcom', 'configurar_distribuicao_garcons'},
    'ajuda': {'central_ajuda', 'detalhe_ajuda', 'assistente_local_status', 'assistente_local_perguntar'},
}

ENDPOINT_TO_PAGINA = {
    endpoint: pagina
    for pagina, endpoints in PAGINA_ENDPOINTS.items()
    for endpoint in endpoints
}

```


### Arquivo: `app/dashboard_routes.py`
- Linhas: 3
- Tamanho: 0.1 KB
- Status: completo

```python
def register_routes(app, context=None):
    return app

```


### Arquivo: `app/decorators.py`
- Linhas: 61
- Tamanho: 2.1 KB
- Status: completo

```python
from functools import wraps

from flask import flash, redirect, session, url_for

from app import extensions
from models import Funcionario
from security import is_json_request, json_response


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


def _limit(rule):
    def decorator(func):
        if extensions.limiter is None:
            return func
        return extensions.limiter.limit(rule)(func)

    return decorator

```


### Arquivo: `app/empresa_routes.py`
- Linhas: 3
- Tamanho: 0.1 KB
- Status: completo

```python
def register_routes(app, context=None):
    return app

```


### Arquivo: `app/exceptions.py`
- Linhas: 31
- Tamanho: 0.6 KB
- Status: completo

```python
class AppError(Exception):
    status_code = 500
    code = 'app_error'

    def __init__(self, message, *, code=None, status_code=None):
        super().__init__(message)
        if code:
            self.code = code
        if status_code:
            self.status_code = status_code


class BusinessRuleError(AppError):
    status_code = 409
    code = 'business_rule'


class ValidationError(AppError):
    status_code = 400
    code = 'validation_error'


class PermissionDenied(AppError):
    status_code = 403
    code = 'forbidden'


class NotFound(AppError):
    status_code = 404
    code = 'not_found'

```


### Arquivo: `app/extensions.py`
- Linhas: 72
- Tamanho: 2.1 KB
- Status: completo

```python
"""Inicializacao centralizada de extensoes Flask."""

import os

from flask import request
from flask_migrate import Migrate

try:
    from flask_wtf.csrf import CSRFProtect
except Exception:  # pragma: no cover - fallback para ambientes sem dependencia instalada
    CSRFProtect = None

try:
    from flask_limiter import Limiter
except Exception:  # pragma: no cover - fallback para ambientes sem dependencia instalada
    Limiter = None

try:
    from flask_caching import Cache
except Exception:  # pragma: no cover - fallback para ambientes sem dependencia instalada
    Cache = None


migrate = Migrate()
csrf = CSRFProtect() if CSRFProtect else None
limiter = None
cache = Cache() if Cache else None


def _client_rate_limit_key():
    if request.access_route:
        return request.access_route[-1]
    return request.remote_addr or 'unknown'


def init_extensions(app, db):
    """Registra extensoes no app."""
    global limiter
    migrate.init_app(app, db)

    if csrf is not None:
        # Mantem a validacao manual legada durante transicao de arquitetura.
        app.config.setdefault('WTF_CSRF_CHECK_DEFAULT', False)
        csrf.init_app(app)

    if Limiter is not None:
        storage_uri = (
            os.environ.get('RATELIMIT_STORAGE_URI')
            or app.config.get('RATELIMIT_STORAGE_URI')
            or 'memory://'
        )
        limiter = Limiter(key_func=_client_rate_limit_key, storage_uri=storage_uri)
        limiter.init_app(app)
    else:
        limiter = None

    if cache is not None:
        cache_type = app.config.get('CACHE_TYPE') or os.environ.get('CACHE_TYPE') or 'SimpleCache'
        cache_default_timeout = int(
            app.config.get('CACHE_DEFAULT_TIMEOUT')
            or os.environ.get('CACHE_DEFAULT_TIMEOUT')
            or 60
        )
        cache_redis_url = app.config.get('CACHE_REDIS_URL') or os.environ.get('CACHE_REDIS_URL')
        cache_config = {
            'CACHE_TYPE': cache_type,
            'CACHE_DEFAULT_TIMEOUT': cache_default_timeout,
        }
        if cache_redis_url:
            cache_config['CACHE_REDIS_URL'] = cache_redis_url
        cache.init_app(app, config=cache_config)

```


### Arquivo: `app/factory.py`
- Linhas: 76
- Tamanho: 3.0 KB
- Status: completo

```python
import logging
import os

from dotenv import load_dotenv
from flask import Flask

from config import DEV_FALLBACK_SECRET, config
from models import db

from app.extensions import init_extensions


load_dotenv()
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


def create_app(config_name=None, *, register_routes=False, route_contexts=None):
    if config_name is None:
        config_name = (os.environ.get('FLASK_CONFIG') or os.environ.get('APP_ENV') or 'development').strip().lower()
    if config_name not in config:
        config_name = 'default'

    app = Flask(
        __name__,
        template_folder=os.path.join(PROJECT_ROOT, 'templates'),
        static_folder=os.path.join(PROJECT_ROOT, 'static'),
    )
    app.config.from_object(config[config_name])
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config.setdefault('LOGIN_MAX_ATTEMPTS', 5)
    app.config.setdefault('LOGIN_WINDOW_SECONDS', 300)
    app.config.setdefault('LOCAL_AI_ENABLED', os.environ.get('SYSTEMLR_LOCAL_AI_ENABLED', '1') not in {'0', 'false', 'False'})
    app.config.setdefault(
        'LOCAL_AI_AUTO_INSTALL',
        os.environ.get('SYSTEMLR_LOCAL_AI_AUTO_INSTALL', '1') not in {'0', 'false', 'False'}
        and app.config.get('ENV_NAME') != 'testing'
    )
    app.config.setdefault(
        'LOCAL_AI_MODEL_ID',
        os.environ.get('SYSTEMLR_LOCAL_AI_MODEL', 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
    )
    app.config.setdefault(
        'LOCAL_AI_MODEL_CANDIDATES',
        os.environ.get(
            'SYSTEMLR_LOCAL_AI_MODEL_CANDIDATES',
            'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2,intfloat/multilingual-e5-large,sentence-transformers/distiluse-base-multilingual-cased-v2',
        ),
    )
    app.config.setdefault('LOCAL_AI_MAX_HISTORY_MESSAGES', int(os.environ.get('SYSTEMLR_LOCAL_AI_MAX_HISTORY_MESSAGES', '5')))

    app.logger.setLevel(logging.INFO)
    if not app.logger.handlers:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s %(name)s %(message)s',
        )

    if app.config.get('ENV_NAME') == 'production' and app.config.get('SECRET_KEY') == DEV_FALLBACK_SECRET:
        raise RuntimeError('SECRET_KEY insegura em producao. Defina a variavel de ambiente SECRET_KEY.')

    init_extensions(app, db)

    if register_routes:
        route_contexts = route_contexts or {}
        from app import api_routes, auth_routes, dashboard_routes, empresa_routes, rh_routes, services_routes

        auth_routes.register_routes(app, route_contexts.get('auth'))
        dashboard_routes.register_routes(app, route_contexts.get('dashboard'))
        rh_routes.register_routes(app, route_contexts.get('rh'))
        empresa_routes.register_routes(app, route_contexts.get('empresa'))
        services_routes.register_routes(app, route_contexts.get('services'))
        api_routes.register_routes(app, route_contexts.get('api'))

    return app

```


### Arquivo: `app/helpers.py`
- Linhas: 69
- Tamanho: 2.0 KB
- Status: completo

```python
from collections import deque
from datetime import datetime

from flask import current_app, request, session

from app import extensions
from app.services.financeiro_service import calcular_metricas_dashboard, parse_date_range
from models import Funcionario


_failed_login_attempts = {}


def get_funcionario_logado():
    if 'funcionario_id' in session:
        return Funcionario.query.get(session['funcionario_id'])
    return None


def _normalizar_texto(valor):
    return (valor or '').strip().lower()


def _client_ip():
    if request.access_route:
        return request.access_route[-1]
    return request.remote_addr or 'unknown'


def _purge_old_attempts(attempts):
    now = datetime.utcnow()
    login_window_seconds = int(current_app.config.get('LOGIN_WINDOW_SECONDS', 300))
    while attempts and (now - attempts[0]).total_seconds() > login_window_seconds:
        attempts.popleft()


def _is_login_rate_limited(ip_addr):
    attempts = _failed_login_attempts.get(ip_addr)
    if not attempts:
        return False
    _purge_old_attempts(attempts)
    return len(attempts) >= int(current_app.config.get('LOGIN_MAX_ATTEMPTS', 5))


def _register_login_attempt(ip_addr, success):
    attempts = _failed_login_attempts.setdefault(ip_addr, deque())
    _purge_old_attempts(attempts)
    if success:
        attempts.clear()
    else:
        attempts.append(datetime.utcnow())


def _parse_date_range(data_inicial_str, data_final_str, default_days=7):
    return parse_date_range(data_inicial_str, data_final_str, default_days=default_days)


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

```


### Arquivo: `app/rh_routes.py`
- Linhas: 3
- Tamanho: 0.1 KB
- Status: completo

```python
def register_routes(app, context=None):
    return app

```


### Arquivo: `app/services/analytics.py`
- Linhas: 313
- Tamanho: 12.2 KB
- Status: completo

```python
from datetime import datetime, timedelta

from models import Caixa, Garcom, ItemPedido, LancamentoFinanceiro, Pedido, Produto, db


def calcular_metricas_dashboard(inicio_periodo, fim_periodo):
    """Calcula metricas agregadas do dashboard no intervalo informado."""
    inicio_hoje = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    fim_hoje = inicio_hoje + timedelta(days=1)
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
    pedidos_cancelados_lista = Pedido.query.filter(
        Pedido.status == 'cancelado',
        Pedido.criado_em >= inicio_periodo,
        Pedido.criado_em < fim_periodo
    ).all()
    pedidos_cancelados_periodo = Pedido.query.filter(
        Pedido.status == 'cancelado',
        Pedido.criado_em >= inicio_periodo,
        Pedido.criado_em < fim_periodo
    ).count()
    valor_cancelado_periodo = sum((pedido.total or 0) for pedido in pedidos_cancelados_lista)

    quantidade_vendida = db.func.sum(ItemPedido.quantidade).label('quantidade_vendida')
    receita_gerada = db.func.sum(ItemPedido.quantidade * ItemPedido.preco_unitario).label('receita_gerada')
    custo_gerado = db.func.sum(ItemPedido.quantidade * Produto.preco_custo).label('custo_gerado')

    custo_periodo_raw = db.session.query(
        custo_gerado
    ).join(
        Produto, Produto.id == ItemPedido.produto_id
    ).join(
        Pedido, Pedido.id == ItemPedido.pedido_id
    ).filter(
        Pedido.status == 'fechado',
        Pedido.fechado_em >= inicio_periodo,
        Pedido.fechado_em < fim_periodo
    ).scalar()
    cmv_periodo = float(custo_periodo_raw or 0.0)
    lucro_bruto_periodo = float(faturamento_periodo - cmv_periodo)
    margem_bruta_pct = (lucro_bruto_periodo / faturamento_periodo * 100.0) if faturamento_periodo > 0 else 0.0

    despesas_operacionais_periodo = db.session.query(
        db.func.sum(LancamentoFinanceiro.valor)
    ).filter(
        LancamentoFinanceiro.tipo.in_([
            LancamentoFinanceiro.TIPO_DESPESA,
            LancamentoFinanceiro.TIPO_CONSUMO_PROPRIO
        ]),
        LancamentoFinanceiro.data_competencia >= inicio_periodo.date(),
        LancamentoFinanceiro.data_competencia < fim_periodo.date()
    ).scalar() or 0.0

    ajustes_financeiros_periodo = db.session.query(
        db.func.sum(LancamentoFinanceiro.valor)
    ).filter(
        LancamentoFinanceiro.tipo == LancamentoFinanceiro.TIPO_AJUSTE,
        LancamentoFinanceiro.data_competencia >= inicio_periodo.date(),
        LancamentoFinanceiro.data_competencia < fim_periodo.date()
    ).scalar() or 0.0

    resultado_operacional_periodo = float(lucro_bruto_periodo - despesas_operacionais_periodo + ajustes_financeiros_periodo)
    margem_operacional_pct = (resultado_operacional_periodo / faturamento_periodo * 100.0) if faturamento_periodo > 0 else 0.0

    total_pedidos_considerados = pedidos_periodo_total + pedidos_cancelados_periodo
    taxa_cancelamento_pct = (
        (pedidos_cancelados_periodo / total_pedidos_considerados) * 100.0
        if total_pedidos_considerados > 0 else 0.0
    )

    receita_media_dia = (faturamento_periodo / periodo_dias) if periodo_dias > 0 else 0.0
    pedidos_media_dia = (pedidos_periodo_total / periodo_dias) if periodo_dias > 0 else 0.0

    periodo_anterior_inicio = inicio_periodo - timedelta(days=periodo_dias)
    periodo_anterior_fim = inicio_periodo
    faturamento_periodo_anterior = db.session.query(
        db.func.sum(Pedido.total)
    ).filter(
        Pedido.status == 'fechado',
        Pedido.fechado_em >= periodo_anterior_inicio,
        Pedido.fechado_em < periodo_anterior_fim
    ).scalar() or 0.0

    crescimento_receita_pct = (
        ((faturamento_periodo - faturamento_periodo_anterior) / faturamento_periodo_anterior) * 100.0
        if faturamento_periodo_anterior > 0 else 0.0
    )
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
            'data_iso': chave_dia,
            'data_curta': dia.strftime('%d/%m'),
            'data_semana': dia.strftime('%a'),
            'faturamento': valores_dia['faturamento'],
            'pedidos': valores_dia['pedidos']
        })

    maior_faturamento_periodo = max((item['faturamento'] for item in vendas_periodo), default=0)
    for item in vendas_periodo:
        item['faturamento_pct'] = (item['faturamento'] / maior_faturamento_periodo * 100) if maior_faturamento_periodo else 0

    top_produtos_vendidos_raw = db.session.query(
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
    top_produtos_vendidos = [
        {
            'produto_id': produto.id,
            'nome': produto.nome,
            'quantidade': int(qtd or 0),
            'receita': float(receita or 0),
        }
        for produto, qtd, receita in top_produtos_vendidos_raw
    ]

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

    top_clientes_raw = db.session.query(
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
    top_clientes = [
        {
            'cliente_nome': item.cliente_nome,
            'pedidos': int(item.pedidos or 0),
            'faturamento': float(item.faturamento or 0)
        }
        for item in top_clientes_raw
    ]

    desempenho_garcons_raw = db.session.query(
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
    desempenho_garcons = [
        {
            'nome': item.nome,
            'pedidos': int(item.pedidos or 0),
            'faturamento': float(item.faturamento or 0)
        }
        for item in desempenho_garcons_raw
    ]

    desempenho_caixas_raw = db.session.query(
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
    desempenho_caixas = [
        {
            'nome': item.nome,
            'pedidos': int(item.pedidos or 0),
            'faturamento': float(item.faturamento or 0)
        }
        for item in desempenho_caixas_raw
    ]

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
    metodo_mais_usado = metodos_pagamento[0]['metodo'] if metodos_pagamento else 'nao informado'
    concentracao_top_pagamento_pct = (
        (metodos_pagamento[0]['quantidade'] / pedidos_periodo_total) * 100.0
        if metodos_pagamento and pedidos_periodo_total > 0 else 0.0
    )

    return {
        'periodo_dias': periodo_dias,
        'pedidos_periodo_total': pedidos_periodo_total,
        'faturamento_periodo': float(faturamento_periodo),
        'faturamento_periodo_anterior': float(faturamento_periodo_anterior),
        'crescimento_receita_pct': float(crescimento_receita_pct),
        'faturamento_hoje': float(faturamento_hoje),
        'receita_media_dia': float(receita_media_dia),
        'pedidos_media_dia': float(pedidos_media_dia),
        'ticket_medio_periodo': float(ticket_medio_periodo),
        'cmv_periodo': float(cmv_periodo),
        'lucro_bruto_periodo': float(lucro_bruto_periodo),
        'margem_bruta_pct': float(margem_bruta_pct),
        'despesas_operacionais_periodo': float(despesas_operacionais_periodo),
        'ajustes_financeiros_periodo': float(ajustes_financeiros_periodo),
        'resultado_operacional_periodo': float(resultado_operacional_periodo),
        'margem_operacional_pct': float(margem_operacional_pct),
        'pedidos_abertos': int(pedidos_abertos),
        'pedidos_cancelados_periodo': int(pedidos_cancelados_periodo),
        'valor_cancelado_periodo': float(valor_cancelado_periodo),
        'taxa_cancelamento_pct': float(taxa_cancelamento_pct),
        'metodo_mais_usado': metodo_mais_usado,
        'concentracao_top_pagamento_pct': float(concentracao_top_pagamento_pct),
        'vendas_periodo': vendas_periodo,
        'top_produtos_vendidos': top_produtos_vendidos,
        'pedidos_por_status': pedidos_por_status,
        'top_clientes': top_clientes,
        'desempenho_garcons': desempenho_garcons,
        'desempenho_caixas': desempenho_caixas,
        'metodos_pagamento': metodos_pagamento
    }

```


### Arquivo: `app/services/assistente_service.py`
- Linhas: 5
- Tamanho: 0.1 KB
- Status: completo

```python
from app.services.local_ai import LocalAIAssistant


__all__ = ['LocalAIAssistant']

```


### Arquivo: `app/services/estoque.py`
- Linhas: 158
- Tamanho: 5.0 KB
- Status: completo

```python
import os
import re
import uuid

from flask import current_app
from PIL import Image

from app.exceptions import BusinessRuleError, ValidationError
from app.utils.helpers import sem_acentos
from app.utils.validators import normalizar_codigo_barras
from models import EmpresaConfig, Movimentacao, Produto


ALLOWED_IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp', '.gif'}
DEFAULT_PRODUCT_IMAGE = 'img/placeholders/imgindisponivel.png'


def aplicar_movimentacao_estoque(produto, tipo, quantidade, *, tipos_validos=None, movimentacao_model=Movimentacao):
    tipos_validos = set(tipos_validos or {
        movimentacao_model.TIPO_ENTRADA,
        movimentacao_model.TIPO_SAIDA,
        movimentacao_model.TIPO_TRANSFERENCIA,
    })
    if tipo not in tipos_validos:
        return 'Tipo de movimentação inválido'

    if quantidade <= 0:
        return 'Quantidade deve ser maior que 0'

    if tipo == movimentacao_model.TIPO_ENTRADA:
        produto.quantidade_estoque += quantidade
        return None

    if produto.quantidade_estoque < quantidade:
        return 'Quantidade em estoque insuficiente'

    produto.quantidade_estoque -= quantidade
    return None


def _normalizar_codigo_barras(valor):
    return normalizar_codigo_barras(valor)


def _is_allowed_image(filename):
    _, ext = os.path.splitext(filename.lower())
    return ext in ALLOWED_IMAGE_EXTENSIONS


def _is_valid_image_content(file_storage):
    if not file_storage:
        return False
    stream = getattr(file_storage, 'stream', None)
    if stream is None:
        return False
    try:
        stream.seek(0)
        img = Image.open(stream)
        img.verify()
        stream.seek(0)
        return True
    except Exception:
        try:
            stream.seek(0)
        except Exception:
            pass
        return False


def _optimize_image_file(absolute_path):
    try:
        img = Image.open(absolute_path)
        max_size = (800, 800)
        resample = getattr(Image, 'Resampling', Image).LANCZOS
        img.thumbnail(max_size, resample)
        save_kwargs = {'optimize': True}
        if img.format and img.format.lower() in ['jpeg', 'jpg']:
            save_kwargs['quality'] = 85
        img.save(absolute_path, **save_kwargs)
    except Exception:
        pass


def _delete_image_file(relative_path):
    if not relative_path:
        return
    caminho_rel = str(relative_path).replace('\\', '/')
    if caminho_rel == DEFAULT_PRODUCT_IMAGE:
        return
    caminho_padrao_config = None
    try:
        empresa_cfg = EmpresaConfig.query.first()
        caminho_padrao_config = (empresa_cfg.ecom_produto_placeholder_path or '').strip().replace('\\', '/') if empresa_cfg else ''
    except Exception:
        caminho_padrao_config = None
    if caminho_padrao_config and caminho_rel == caminho_padrao_config:
        return

    image_path = os.path.normpath(os.path.join(current_app.static_folder, relative_path))
    static_root = os.path.normpath(current_app.static_folder)
    if os.path.commonpath([image_path, static_root]) != static_root:
        return

    if os.path.exists(image_path):
        os.remove(image_path)


def _save_product_image(file_storage, product_name):
    if not file_storage or not file_storage.filename:
        return None, None
    if not _is_allowed_image(file_storage.filename):
        return None, 'Formato de imagem invalido. Use PNG, JPG, JPEG, WEBP ou GIF.'
    if not _is_valid_image_content(file_storage):
        return None, 'Arquivo enviado nao corresponde a uma imagem valida.'

    _, ext = os.path.splitext(file_storage.filename.lower())
    image_name = f'{uuid.uuid4().hex}{ext}'
    relative_dir = os.path.join('uploads', 'produtos')
    absolute_dir = os.path.join(current_app.static_folder, relative_dir)
    os.makedirs(absolute_dir, exist_ok=True)
    relative_path = os.path.join(relative_dir, image_name).replace('\\', '/')
    absolute_path = os.path.join(current_app.static_folder, relative_path)

    file_storage.save(absolute_path)
    _optimize_image_file(absolute_path)
    return relative_path, None


def categoria_parece_quimico(produto):
    categoria_nome = ''
    if getattr(produto, 'categoria', None):
        categoria_nome = produto.categoria.nome or ''
    texto = sem_acentos(categoria_nome).strip().lower()
    return bool(texto and re.search(r'quim', texto))


def aplicar_movimentacao_estoque(produto, tipo, quantidade, *, tipos_validos=None, movimentacao_model=Movimentacao):
    tipos_validos = set(tipos_validos or {
        movimentacao_model.TIPO_ENTRADA,
        movimentacao_model.TIPO_SAIDA,
        movimentacao_model.TIPO_TRANSFERENCIA,
    })
    if tipo not in tipos_validos:
        raise ValidationError('Tipo de movimentacao invalido.')

    if quantidade <= 0:
        raise ValidationError('Quantidade deve ser maior que 0.')

    if tipo == movimentacao_model.TIPO_ENTRADA:
        produto.quantidade_estoque += quantidade
        return None

    if produto.quantidade_estoque < quantidade:
        raise BusinessRuleError('Quantidade em estoque insuficiente.')

    produto.quantidade_estoque -= quantidade
    return None

```


### Arquivo: `app/services/estoque_service.py`
- Linhas: 25
- Tamanho: 0.6 KB
- Status: completo

```python
from app.services.estoque import (
    _delete_image_file,
    _normalizar_codigo_barras,
    _save_product_image,
    aplicar_movimentacao_estoque,
    categoria_parece_quimico,
)


normalizar_codigo_barras = _normalizar_codigo_barras
save_product_image = _save_product_image
delete_image_file = _delete_image_file


__all__ = [
    'aplicar_movimentacao_estoque',
    'categoria_parece_quimico',
    '_normalizar_codigo_barras',
    '_save_product_image',
    '_delete_image_file',
    'normalizar_codigo_barras',
    'save_product_image',
    'delete_image_file',
]

```


### Arquivo: `app/services/financeiro.py`
- Linhas: 60
- Tamanho: 2.5 KB
- Status: completo

```python
from app import extensions
from app.services.analytics import calcular_metricas_dashboard
from app.services.utils import _to_float
from app.utils.data import parse_date_range


def _parse_date_range(data_inicial_str, data_final_str, default_days=7):
    return parse_date_range(data_inicial_str, data_final_str, default_days=default_days)


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


def _build_payment_data(metodo_raw, valor_raw, total_pedido, payment_methods, split_raw=None, cliente_crediario=''):
    metodo = (metodo_raw or '').strip().lower()
    if metodo not in payment_methods:
        raise ValueError('Metodo de pagamento invalido.')
    total = float(total_pedido or 0.0)
    metodo_label_base = payment_methods.get(metodo, metodo.replace('_', ' ').title())

    if metodo == 'dividido':
        split_raw = split_raw or {}
        valor_dinheiro = _to_float(split_raw.get('dinheiro'), 0.0) or 0.0
        valor_cartao = _to_float(split_raw.get('cartao'), 0.0) or 0.0
        if valor_dinheiro < 0 or valor_cartao < 0:
            raise ValueError('Valores de pagamento nao podem ser negativos.')
        valor_pago = valor_dinheiro + valor_cartao
        if valor_pago <= 0:
            raise ValueError('Informe ao menos um valor para dinheiro ou cartao.')
        if valor_pago < total:
            raise ValueError('Valor informado insuficiente para finalizar o pedido.')
        metodo_texto = f'{metodo_label_base} (dinheiro: {valor_dinheiro:.2f} | cartao: {valor_cartao:.2f})'
        return metodo_texto, valor_pago

    valor_pago = _to_float(valor_raw, None)
    if valor_pago is None:
        valor_pago = 0.0 if metodo == 'crediario' else float(total_pedido or 0.0)
    if valor_pago < 0:
        raise ValueError('Valor pago nao pode ser negativo.')

    if metodo == 'crediario':
        cliente = (cliente_crediario or '').strip()
        metodo_texto = f'{metodo_label_base} ({cliente})' if cliente else metodo_label_base
    else:
        if metodo == 'dinheiro' and valor_pago < total:
            raise ValueError('Valor recebido insuficiente para finalizar o pedido.')
        metodo_texto = metodo_label_base

    return metodo_texto, valor_pago

```


### Arquivo: `app/services/financeiro_service.py`
- Linhas: 23
- Tamanho: 0.5 KB
- Status: completo

```python
from app.services.analytics import calcular_metricas_dashboard
from app.services.financeiro import (
    _build_payment_data,
    _coletar_dashboard_analytics,
    _parse_date_range,
)


build_payment_data = _build_payment_data
coletar_dashboard_analytics = _coletar_dashboard_analytics
parse_date_range = _parse_date_range


__all__ = [
    'calcular_metricas_dashboard',
    '_build_payment_data',
    '_coletar_dashboard_analytics',
    '_parse_date_range',
    'build_payment_data',
    'coletar_dashboard_analytics',
    'parse_date_range',
]

```


### Arquivo: `app/services/local_ai.py`
- Linhas: 917
- Tamanho: 34.2 KB
- Status: completo

```python
import importlib
import math
import os
import re
import subprocess
import sys
import threading
import unicodedata
import uuid
from pathlib import Path


LOCAL_AI_PACKAGES = (
    'torch==2.5.1',
    'sentence-transformers==3.3.1',
    'huggingface-hub==0.26.2',
    'safetensors==0.4.5',
)


class LocalAIAssistant:
    def __init__(self, app, knowledge_builder):
        self.app = app
        self.knowledge_builder = knowledge_builder
        self.model_id = app.config.get(
            'LOCAL_AI_MODEL_ID',
            'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2',
        )
        raw_candidates = app.config.get('LOCAL_AI_MODEL_CANDIDATES') or self.model_id
        self.model_candidates = [
            item.strip()
            for item in str(raw_candidates).split(',')
            if item and item.strip()
        ] or [self.model_id]
        self.enabled = bool(app.config.get('LOCAL_AI_ENABLED', True))
        self.auto_install = bool(app.config.get('LOCAL_AI_AUTO_INSTALL', True))
        self.max_history_messages = int(app.config.get('LOCAL_AI_MAX_HISTORY_MESSAGES', 5) or 5)
        self.instance_dir = Path(app.instance_path) / 'local_ai'
        self.model_dir = self.instance_dir / 'semantic-model'
        self._lock = threading.Lock()
        self._thread = None
        self._status = {
            'enabled': self.enabled,
            'ready': False,
            'state': 'idle',
            'mode': 'lexical',
            'message': 'Marcia pronta para inicializar.',
            'document_count': 0,
            'model_id': self.model_id,
            'last_error': None,
        }
        self._documents = []
        self._document_vectors = []
        self._encoder = None
        self._query_vector_cache = {}
        self._avg_doc_length = 0.0
        self._idf_map = {}

    def start_background_prepare(self):
        if not self.enabled:
            return
        if self.app.debug and os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
            return
        with self._lock:
            if self._thread and self._thread.is_alive():
                return
            self._thread = threading.Thread(
                target=self._prepare_runtime,
                name='systemlr-local-ai',
                daemon=True,
            )
            self._thread.start()

    def status(self):
        self._ensure_documents()
        if self._status.get('state') == 'idle':
            if self.auto_install:
                self._ensure_prepare_started()
            else:
                self._set_status(
                    ready=True,
                    state='ready',
                    mode='lexical',
                    message='Marcia esta em modo local basico. O modelo semantico automatico esta desabilitado.',
                    last_error=None,
                )
        payload = dict(self._status)
        payload['document_count'] = len(self._documents)
        return payload

    def answer(
        self,
        question,
        *,
        paginas_permitidas=None,
        pagina_atual=None,
        tela_atual=None,
        conversation_history=None,
        feedback_items=None,
    ):
        pergunta = (question or '').strip()
        if not pergunta:
            return {
                'answer': 'Envie uma pergunta para a Marcia orientar a navegacao e o proximo passo no sistema.',
                'actions': self._fallback_actions(paginas_permitidas or set(), pagina_atual),
                'sources': [],
                'status': self.status(),
                'response_id': uuid.uuid4().hex,
                'matched_doc_ids': [],
            }

        self._ensure_documents()
        self._ensure_prepare_started()
        paginas_permitidas = set(paginas_permitidas or [])

        saudacao = self._match_greeting_reply(pergunta)
        if saudacao:
            return {
                'response_id': uuid.uuid4().hex,
                'answer': saudacao,
                'actions': [],
                'sources': [],
                'status': self.status(),
                'matched_doc_ids': [],
            }

        documentos = [
            item
            for item in self._documents
            if self._documento_visivel(item, paginas_permitidas)
        ]
        if not documentos:
            return {
                'answer': 'Nao encontrei conteudo liberado para o seu perfil. Abra a Ajuda ou revise as permissoes do usuario.',
                'actions': [],
                'sources': [],
                'status': self.status(),
                'response_id': uuid.uuid4().hex,
                'matched_doc_ids': [],
            }

        question_context = self._build_question_context(pergunta, conversation_history)
        ranking = self._rank_documents(
            question_context['query_text'],
            documentos,
            pagina_atual=pagina_atual,
            feedback_items=feedback_items,
        )
        melhores = [item for item in ranking[:3] if item['score'] > 0]
        if not melhores:
            melhores = ranking[:2]

        resposta = self._compose_answer(
            pergunta,
            melhores,
            pagina_atual=pagina_atual,
            tela_atual=tela_atual,
        )
        acoes = self._build_actions(
            melhores,
            paginas_permitidas=paginas_permitidas,
            pagina_atual=pagina_atual,
        )

        fontes = []
        for item in melhores:
            doc = item['doc']
            fontes.append({
                'title': doc.get('title'),
                'url': doc.get('url'),
                'kind': doc.get('kind'),
                'section': doc.get('section'),
            })

        return {
            'response_id': uuid.uuid4().hex,
            'answer': resposta,
            'actions': acoes,
            'sources': fontes,
            'status': self.status(),
            'matched_doc_ids': [
                item['doc'].get('id')
                for item in melhores
                if item.get('doc') and item['doc'].get('id')
            ],
        }

    def _ensure_prepare_started(self):
        if not self.enabled:
            return
        if self._status.get('state') == 'idle':
            self.start_background_prepare()

    def _prepare_runtime(self):
        self._set_status(
            ready=False,
            state='preparing',
            mode='lexical',
            message='Preparando a Marcia para uso offline.',
            last_error=None,
        )
        try:
            self._ensure_documents(force=True)
            if not self.auto_install:
                self._set_status(
                    ready=True,
                    state='ready',
                    mode='lexical',
                    message='Marcia esta em modo local basico. O modelo semantico automatico esta desabilitado.',
                    last_error=None,
                )
                return

            if self._try_prepare_semantic_model():
                self._set_status(
                    ready=True,
                    state='ready',
                    mode='semantic',
                    message='Marcia esta pronta para uso offline.',
                    last_error=None,
                )
                return

            self._set_status(
                ready=True,
                state='ready',
                mode='lexical',
                message='Marcia esta em modo local basico enquanto o modelo semantico nao fica disponivel.',
                last_error=self._status.get('last_error'),
            )
        except Exception as exc:
            self.app.logger.exception('Falha ao preparar a IA local.')
            self._set_status(
                ready=True,
                state='ready',
                mode='lexical',
                message='Marcia esta em modo local basico por falha na preparacao offline.',
                last_error=str(exc),
            )

    def _try_prepare_semantic_model(self):
        modules = self._ensure_runtime_dependencies()
        if not modules:
            return False

        SentenceTransformer = modules['sentence_transformer']
        self.instance_dir.mkdir(parents=True, exist_ok=True)

        encoder = None
        errors = []
        try:
            if self.model_dir.exists():
                encoder = SentenceTransformer(str(self.model_dir), device='cpu')
        except Exception as exc:
            errors.append(str(exc))
            encoder = None

        if encoder is None:
            for candidate in self.model_candidates:
                try:
                    encoder = SentenceTransformer(candidate, device='cpu')
                    self.model_id = candidate
                    try:
                        encoder.save(str(self.model_dir))
                    except Exception:
                        pass
                    break
                except Exception as exc:
                    errors.append(f'{candidate}: {exc}')

        if encoder is None:
            self._status['last_error'] = '; '.join(errors[-3:]) if errors else 'modelo indisponivel'
            self.app.logger.warning('Nao foi possivel carregar o modelo semantico local: %s', self._status['last_error'])
            return False

        textos = [item['search_text'] for item in self._documents]
        try:
            vetores = encoder.encode(
                textos,
                normalize_embeddings=True,
                convert_to_numpy=True,
                show_progress_bar=False,
            )
        except Exception as exc:
            self._status['last_error'] = str(exc)
            self.app.logger.warning('Nao foi possivel vetorizar a base do assistente: %s', exc)
            return False

        self._encoder = encoder
        self._document_vectors = [self._vector_to_list(item) for item in vetores]
        self._query_vector_cache = {}
        self._status['model_id'] = self.model_id
        return True

    def _ensure_runtime_dependencies(self):
        try:
            sentence_transformers = importlib.import_module('sentence_transformers')
            return {'sentence_transformer': sentence_transformers.SentenceTransformer}
        except Exception:
            if not self.auto_install:
                return None

        try:
            subprocess.check_call(
                [
                    sys.executable,
                    '-m',
                    'pip',
                    'install',
                    '--disable-pip-version-check',
                    '--no-input',
                    *LOCAL_AI_PACKAGES,
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except Exception as exc:
            self._status['last_error'] = str(exc)
            self.app.logger.warning('Falha ao instalar dependencias da IA local: %s', exc)
            return None

        try:
            sentence_transformers = importlib.import_module('sentence_transformers')
            return {'sentence_transformer': sentence_transformers.SentenceTransformer}
        except Exception as exc:
            self._status['last_error'] = str(exc)
            self.app.logger.warning('Dependencias instaladas, mas o import da IA local falhou: %s', exc)
            return None

    def _ensure_documents(self, force=False):
        if self._documents and not force:
            return
        with self.app.app_context():
            with self.app.test_request_context('/'):
                documentos = self.knowledge_builder() or []
        preparados = []
        for item in documentos:
            doc = dict(item)
            doc['search_text'] = self._build_search_text(doc)
            doc['normalized_search_text'] = self._normalize_text(doc['search_text'])
            doc['normalized_title'] = self._normalize_text(doc.get('title') or '')
            doc['tokens'] = self._tokenize(doc['search_text'])
            doc['token_list'] = list(re.findall(r'[a-z0-9]{2,}', doc['normalized_search_text']))
            frequencias = {}
            for token in doc['token_list']:
                frequencias[token] = frequencias.get(token, 0) + 1
            doc['token_freq'] = frequencias
            doc['doc_length'] = len(doc['token_list'])
            doc['title_tokens'] = self._tokenize(doc.get('title') or '')
            doc['keyword_tokens'] = self._tokenize(' '.join(doc.get('keywords') or ()))
            preparados.append(doc)
        self._documents = preparados
        total_docs = len(preparados) or 1
        total_len = sum(doc.get('doc_length', 0) for doc in preparados)
        self._avg_doc_length = (total_len / total_docs) if total_docs else 0.0
        document_frequency = {}
        for doc in preparados:
            for token in set(doc.get('token_list') or ()):
                document_frequency[token] = document_frequency.get(token, 0) + 1
        self._idf_map = {
            token: math.log(1 + ((total_docs - freq + 0.5) / (freq + 0.5)))
            for token, freq in document_frequency.items()
        }
        self._status['document_count'] = len(preparados)
        self._query_vector_cache = {}

    def _rank_documents(self, question, documents, *, pagina_atual=None, feedback_items=None):
        query_text = question.strip()
        query_tokens = self._tokenize(query_text)
        query_text_normalized = self._normalize_text(query_text)
        semantic_mode = self._status.get('mode') == 'semantic' and self._encoder and self._document_vectors
        query_vector = self._get_query_vector(query_text) if semantic_mode else None

        ranking = []
        for doc in documents:
            lexical = self._lexical_score(
                query_tokens,
                doc,
                query_text_normalized=query_text_normalized,
            )
            bm25 = self._bm25_score(query_tokens, doc)
            semantic = 0.0
            if query_vector is not None:
                try:
                    idx = self._documents.index(doc)
                    semantic = self._cosine(query_vector, self._document_vectors[idx])
                except Exception:
                    semantic = 0.0
            feedback_score = self._feedback_score(
                query_tokens,
                doc,
                feedback_items,
                pagina_atual=pagina_atual,
            )

            page_boost = self._page_context_boost(doc, query_text, pagina_atual=pagina_atual)
            score = (lexical * 0.46) + (bm25 * 0.24) + feedback_score + page_boost
            if semantic > 0:
                score = max(
                    score,
                    (semantic * 0.42) + (lexical * 0.24) + (bm25 * 0.16) + max(feedback_score, 0.0) + page_boost,
                )

            ranking.append({
                'doc': doc,
                'score': score,
                'lexical_score': lexical,
                'bm25_score': bm25,
                'semantic_score': semantic,
                'feedback_score': feedback_score,
                'page_score': page_boost,
            })

        ranking.sort(key=lambda item: item['score'], reverse=True)
        return ranking

    def _compose_answer(self, question, ranking, *, pagina_atual=None, tela_atual=None):
        if not ranking:
            return 'Nao encontrei uma rota segura para esta pergunta. Abra a Ajuda ou use a Home Operacional para continuar.'

        intent = self._detect_intent(question)
        return self._generate_answer(
            question,
            ranking,
            intent,
            pagina_atual=pagina_atual,
            tela_atual=tela_atual,
        )

    def _build_actions(self, ranking, *, paginas_permitidas=None, pagina_atual=None):
        paginas_permitidas = set(paginas_permitidas or [])
        actions = []
        vistos = set()

        for item in ranking:
            doc = item['doc']
            for action in doc.get('actions') or ():
                page_key = action.get('page')
                if page_key and paginas_permitidas and page_key not in paginas_permitidas:
                    continue
                if not action.get('url'):
                    continue
                key = (action.get('label'), action.get('url'))
                if key in vistos:
                    continue
                vistos.add(key)
                actions.append({
                    'label': action.get('label'),
                    'url': action.get('url'),
                    'reason': action.get('reason') or doc.get('title'),
                    'kind': action.get('kind') or 'navigate',
                })
                if len(actions) >= 4:
                    return actions

            if doc.get('kind') == 'topic' and doc.get('url'):
                key = ('Abrir guia', doc.get('url'))
                if key not in vistos:
                    vistos.add(key)
                    actions.append({
                        'label': 'Abrir guia',
                        'url': doc.get('url'),
                        'reason': f'Passo a passo de {doc.get("title")}',
                        'kind': 'guide',
                    })
                    if len(actions) >= 4:
                        return actions

        if not actions:
            return self._fallback_actions(paginas_permitidas, pagina_atual)
        return actions

    def _fallback_actions(self, paginas_permitidas, pagina_atual):
        acoes = []
        if pagina_atual:
            for doc in self._documents:
                if doc.get('kind') == 'page' and pagina_atual in set(doc.get('pages') or []):
                    for action in doc.get('actions') or ():
                        if action.get('url'):
                            acoes.append({
                                'label': action.get('label'),
                                'url': action.get('url'),
                                'reason': action.get('reason') or doc.get('title'),
                                'kind': action.get('kind') or 'navigate',
                            })
                    break
        if acoes:
            return acoes[:3]
        return []

    def _documento_visivel(self, doc, paginas_permitidas):
        paginas_doc = set(doc.get('pages') or [])
        if not paginas_doc:
            return True
        return bool(paginas_doc.intersection(paginas_permitidas))

    def _build_search_text(self, doc):
        partes = [
            doc.get('title') or '',
            doc.get('summary') or '',
            doc.get('snippet') or '',
            ' '.join(doc.get('keywords') or ()),
            ' '.join(doc.get('pages') or ()),
            doc.get('section') or '',
        ]
        for item in doc.get('faq_pairs') or ():
            partes.append(item.get('question') or '')
            partes.append(item.get('answer') or '')
        partes.extend(doc.get('steps') or ())
        partes.extend(doc.get('checklist') or ())
        partes.extend(doc.get('alerts') or ())
        for item in doc.get('problems') or ():
            partes.append(item.get('situation') or '')
            partes.append(item.get('action') or '')
        if doc.get('source_topic'):
            partes.append(doc.get('source_topic'))
        return ' '.join(item for item in partes if item).strip()

    def _lexical_score(self, query_tokens, doc, *, query_text_normalized=''):
        if not query_tokens:
            return 0.0
        doc_tokens = set(doc.get('tokens') or ())
        if not doc_tokens:
            return 0.0
        comuns = query_tokens.intersection(doc_tokens)
        score = self._overlap_ratio(query_tokens, doc_tokens)

        search_text = doc.get('normalized_search_text', '')
        if query_text_normalized and query_text_normalized in search_text:
            score += 0.24

        title_text = doc.get('normalized_title', '')
        if query_text_normalized and query_text_normalized in title_text:
            score += 0.22

        title_tokens = set(doc.get('title_tokens') or ())
        if comuns.intersection(title_tokens):
            score += 0.12

        keywords = set(doc.get('keyword_tokens') or ())
        if comuns.intersection(keywords):
            score += 0.14

        kind_bonus = {
            'issue': 0.12,
            'faq': 0.1,
            'topic': 0.05,
            'page': 0.02,
        }
        score += kind_bonus.get(doc.get('kind'), 0.0)
        return score

    def _feedback_score(self, query_tokens, doc, feedback_items, *, pagina_atual=None):
        if not query_tokens or not feedback_items:
            return 0.0

        doc_id = doc.get('id')
        if not doc_id:
            return 0.0

        ajuste = 0.0
        for item in feedback_items:
            doc_ids = item.get('doc_ids') or ()
            if doc_id not in doc_ids:
                continue

            feedback_tokens = item.get('_tokens')
            if feedback_tokens is None:
                feedback_tokens = self._tokenize(item.get('question') or item.get('reason') or '')
                item['_tokens'] = feedback_tokens

            similaridade = self._overlap_ratio(query_tokens, feedback_tokens)
            if pagina_atual and item.get('pagina_atual') == pagina_atual:
                similaridade += 0.08
            if similaridade <= 0:
                continue

            peso = min(0.24, 0.02 + (similaridade * 0.24))
            if item.get('vote') == 'like':
                ajuste += peso
            else:
                ajuste -= peso * 0.85

        return max(min(ajuste, 0.28), -0.22)

    def _question_targets_current_screen(self, question):
        texto = self._normalize_text(question)
        marcadores = ('nesta tela', 'nessa tela', 'aqui', 'pagina atual', 'onde estou')
        return any(item in texto for item in marcadores)

    def _tokenize(self, text):
        texto_normalizado = self._normalize_text(text)
        return set(re.findall(r'[a-z0-9]{2,}', texto_normalizado))

    def _normalize_text(self, text):
        texto = unicodedata.normalize('NFKD', str(text or ''))
        texto = texto.encode('ascii', 'ignore').decode('ascii')
        return texto.lower().strip()

    def _build_question_context(self, question, conversation_history):
        historico = []
        for item in conversation_history or ():
            if not isinstance(item, dict):
                continue
            role = (item.get('role') or '').strip().lower()
            texto = (item.get('text') or '').strip()
            if role not in {'user', 'assistant'} or not texto:
                continue
            historico.append({'role': role, 'text': texto})
        historico = historico[-self.max_history_messages:]

        perguntas_anteriores = [item['text'] for item in historico if item['role'] == 'user']
        if perguntas_anteriores and self._normalize_text(perguntas_anteriores[-1]) == self._normalize_text(question):
            perguntas_anteriores = perguntas_anteriores[:-1]

        precisa_contexto = self._question_needs_history(question)
        contexto = perguntas_anteriores[-3:] if precisa_contexto else []
        partes = contexto + [question]
        return {
            'query_text': ' '.join(item for item in partes if item).strip(),
            'used_history': bool(contexto),
            'history_messages': historico,
        }

    def _question_needs_history(self, question):
        texto = self._normalize_text(question)
        tokens = self._tokenize(texto)
        marcadores = (
            'e depois',
            'depois disso',
            'e agora',
            'como assim',
            'isso',
            'essa',
            'esse',
            'nela',
            'nele',
            'nessa',
            'nesse',
            'aqui',
        )
        return len(tokens) <= 4 or any(item in texto for item in marcadores)

    def _normalize_short_message(self, text):
        texto = self._normalize_text(text)
        texto = re.sub(r'[^a-z0-9\s]', ' ', texto)
        return re.sub(r'\s+', ' ', texto).strip()

    def _match_greeting_reply(self, question):
        texto = self._normalize_short_message(question)
        if not texto:
            return ''

        respostas = {
            'bom dia': 'Bom dia! Em que posso ajudar?',
            'boa tarde': 'Boa tarde! Em que posso ajudar?',
            'boa noite': 'Boa noite! Como posso te ajudar?',
            'ola': 'Ola! Como posso te ajudar?',
            'oi': 'Oi! O que voce precisa?',
        }
        if texto in respostas:
            return respostas[texto]

        tokens = texto.split()
        if len(tokens) > 3:
            return ''
        if texto in {'oii', 'opa', 'e ai', 'iae'}:
            return 'Oi! Como posso te ajudar?'
        return ''

    def _detect_intent(self, question):
        texto = self._normalize_short_message(question)
        if re.search(r'\b(nao consigo|nao aparece|erro|falha|problema|travou|bloqueado|invalid|incorreto)\b', texto):
            return 'problem'
        if re.search(r'\b(e depois|depois disso|proximo passo|qual o proximo|e agora|como continuo)\b', texto):
            return 'follow_up'
        if re.search(r'\b(onde|onde fica|onde altero|onde configuro|localizar|em qual tela|fica em qual menu)\b', texto):
            return 'location'
        if re.search(r'\b(como|passo a passo|quais passos|o que fazer|registrar|configurar|criar|finalizar|lancar)\b', texto):
            return 'howto'
        if re.search(r'\b(posso|permissao|acesso|liberar|perfil)\b', texto):
            return 'permission'
        if re.search(r'\b(ajuda|explica|entender|duvida)\b', texto):
            return 'general_help'
        return 'general'

    def _generate_answer(self, question, ranking, intent, *, pagina_atual=None, tela_atual=None):
        principal = ranking[0]['doc']
        titulo = principal.get('title') or tela_atual or 'esta area'
        resposta_direta = self._resolve_direct_answer(question, ranking, intent)
        passos = self._select_steps(question, ranking, intent)
        alerta = self._select_alert(ranking, question)

        if pagina_atual and self._question_targets_current_screen(question) and tela_atual:
            abertura = f'Voce esta em {tela_atual}.'
        elif intent == 'location':
            abertura = f'Voce encontra isso em {titulo}.'
        elif intent == 'permission':
            abertura = f'Posso te orientar com base no que esta liberado para o seu perfil em {titulo}.'
        elif intent == 'problem':
            abertura = f'Vamos resolver isso em {titulo}.'
        elif intent in {'howto', 'follow_up'}:
            abertura = f'Para seguir com seguranca em {titulo}:'
        else:
            abertura = f'O melhor contexto para essa duvida agora e {titulo}.'

        linhas = [abertura]
        if resposta_direta:
            prefixo = {
                'problem': 'Tente o seguinte:',
                'location': 'Caminho sugerido:',
                'permission': 'Regra principal:',
            }.get(intent)
            if prefixo:
                linhas.append(f'{prefixo} {self._ensure_sentence(resposta_direta)}')
            else:
                linhas.append(self._ensure_sentence(resposta_direta))

        if passos:
            if intent in {'howto', 'follow_up'}:
                linhas.append('Passo a passo:')
            elif intent == 'problem':
                linhas.append('Checklist rapido:')
            else:
                linhas.append('Passos sugeridos:')
            for indice, passo in enumerate(passos, start=1):
                linhas.append(f'{indice}. {self._ensure_sentence(passo)}')

        if alerta:
            linhas.append(f'Atencao: {self._ensure_sentence(alerta)}')

        if len(linhas) == 1:
            linhas.append(self._ensure_sentence(principal.get('summary') or principal.get('snippet') or 'Veja as opcoes abaixo.'))

        return '\n'.join(item for item in linhas if item).strip()

    def _resolve_direct_answer(self, question, ranking, intent):
        principal = ranking[0]['doc']
        if principal.get('kind') in {'faq', 'issue'} and principal.get('summary'):
            return principal.get('summary')

        if intent == 'location':
            secao = principal.get('section')
            if secao and principal.get('title'):
                return f'Voce encontra isso em {secao} > {principal.get("title")}.'

        melhor_faq = self._best_faq_match(question, ranking)
        if melhor_faq:
            return melhor_faq.get('answer')

        if intent == 'problem':
            melhor_problema = self._best_problem_match(question, ranking)
            if melhor_problema:
                return melhor_problema.get('action')

        return principal.get('summary') or principal.get('snippet') or 'Use a opcao indicada para continuar com seguranca.'

    def _best_faq_match(self, question, ranking):
        query_tokens = self._tokenize(question)
        melhor = None
        melhor_score = 0.0
        for item in ranking[:3]:
            doc = item['doc']
            for faq in doc.get('faq_pairs') or ():
                score = self._text_match_score(query_tokens, faq.get('question'))
                if score > melhor_score:
                    melhor = faq
                    melhor_score = score
        return melhor if melhor_score >= 0.18 else None

    def _best_problem_match(self, question, ranking):
        query_tokens = self._tokenize(question)
        melhor = None
        melhor_score = 0.0
        for item in ranking[:3]:
            doc = item['doc']
            for problema in doc.get('problems') or ():
                score = self._text_match_score(query_tokens, problema.get('situation'))
                if score > melhor_score:
                    melhor = problema
                    melhor_score = score
        return melhor if melhor_score >= 0.18 else None

    def _select_steps(self, question, ranking, intent):
        query_tokens = self._tokenize(question)
        candidatos = []
        for doc_pos, item in enumerate(ranking[:3]):
            doc = item['doc']
            for step_pos, passo in enumerate(doc.get('steps') or ()):
                score = self._text_match_score(query_tokens, passo)
                if intent == 'follow_up' and step_pos > 0:
                    score += 0.08
                if doc.get('kind') in {'faq', 'issue'}:
                    score += 0.05
                score += max(0.0, 0.08 - (doc_pos * 0.02) - (step_pos * 0.01))
                candidatos.append((score, passo))

        if not candidatos:
            return []

        vistos = set()
        passos = []
        limite = 2 if intent in {'location', 'permission'} else 4
        for _, passo in sorted(candidatos, key=lambda item: item[0], reverse=True):
            chave = self._normalize_text(passo)
            if not chave or chave in vistos:
                continue
            vistos.add(chave)
            passos.append(passo)
            if len(passos) >= limite:
                break
        return passos

    def _select_alert(self, ranking, question):
        query_tokens = self._tokenize(question)
        melhor_alerta = ''
        melhor_score = 0.0
        for item in ranking[:2]:
            doc = item['doc']
            for alerta in doc.get('alerts') or ():
                score = self._text_match_score(query_tokens, alerta)
                if score > melhor_score:
                    melhor_score = score
                    melhor_alerta = alerta
        return melhor_alerta if melhor_score >= 0.14 else ''

    def _text_match_score(self, query_tokens, text):
        candidate_tokens = self._tokenize(text)
        if not candidate_tokens:
            return 0.0
        score = self._overlap_ratio(query_tokens, candidate_tokens)
        query_text = ' '.join(sorted(query_tokens))
        candidate_text = self._normalize_text(text)
        if query_text and query_text in candidate_text:
            score += 0.12
        return score

    def _page_context_boost(self, doc, question, *, pagina_atual=None):
        if not pagina_atual:
            return 0.0
        paginas = set(doc.get('pages') or ())
        if pagina_atual not in paginas:
            return 0.0
        return 0.32 if self._question_targets_current_screen(question) else 0.08

    def _bm25_score(self, query_tokens, doc, *, k1=1.5, b=0.75):
        if not query_tokens:
            return 0.0
        token_freq = doc.get('token_freq') or {}
        doc_length = float(doc.get('doc_length') or 0.0)
        avg_doc_length = self._avg_doc_length or 1.0
        total = 0.0
        for token in query_tokens:
            freq = float(token_freq.get(token) or 0.0)
            if freq <= 0:
                continue
            idf = self._idf_map.get(token, 0.0)
            denominador = freq + k1 * (1 - b + b * (doc_length / avg_doc_length))
            if denominador <= 0:
                continue
            total += idf * ((freq * (k1 + 1)) / denominador)
        return min(total, 1.4)

    def _get_query_vector(self, query_text):
        chave = self._normalize_text(query_text)
        if not chave or not self._encoder:
            return None
        if chave in self._query_vector_cache:
            return self._query_vector_cache[chave]
        try:
            vector = self._vector_to_list(
                self._encoder.encode(
                    [query_text],
                    normalize_embeddings=True,
                    convert_to_numpy=True,
                    show_progress_bar=False,
                )[0]
            )
        except Exception:
            return None
        self._query_vector_cache[chave] = vector
        if len(self._query_vector_cache) > 96:
            self._query_vector_cache.pop(next(iter(self._query_vector_cache)))
        return vector

    def _overlap_ratio(self, left_tokens, right_tokens):
        left = set(left_tokens or ())
        right = set(right_tokens or ())
        if not left or not right:
            return 0.0
        comuns = left.intersection(right)
        return len(comuns) / max(len(left), 1)

    def _ensure_sentence(self, text):
        texto = (text or '').strip()
        if not texto:
            return ''
        return texto if texto.endswith(('.', '!', '?')) else f'{texto}.'

    def _vector_to_list(self, vector):
        if hasattr(vector, 'tolist'):
            return vector.tolist()
        return list(vector)

    def _cosine(self, left, right):
        if not left or not right:
            return 0.0
        numerador = sum(float(a) * float(b) for a, b in zip(left, right))
        norma_left = math.sqrt(sum(float(a) * float(a) for a in left))
        norma_right = math.sqrt(sum(float(b) * float(b) for b in right))
        if not norma_left or not norma_right:
            return 0.0
        return numerador / (norma_left * norma_right)

    def _set_status(self, **kwargs):
        self._status.update(kwargs)

```


### Arquivo: `app/services/pedido.py`
- Linhas: 76
- Tamanho: 2.9 KB
- Status: completo

```python
from datetime import datetime

from app.exceptions import BusinessRuleError, NotFound, ValidationError
from models import Caixa, Movimentacao, MovimentacaoCaixa, Produto, db


def _normalizar_item_payload(item, *, produto_model=Produto):
    produto_id = item.get('produto_id')
    quantidade = item.get('quantidade', 1)
    try:
        produto_id = int(produto_id)
        quantidade = int(quantidade)
    except (TypeError, ValueError):
        raise ValidationError('Item invalido.')
    if quantidade <= 0:
        raise ValidationError('Quantidade deve ser maior que zero.')
    produto = produto_model.query.get(produto_id)
    if not produto or not produto.ativo:
        raise ValidationError('Produto invalido ou inativo.')
    return {'produto': produto, 'quantidade': quantidade}, None


def _recalcular_total_pedido(pedido):
    pedido.total = sum((item.quantidade or 0) * (item.preco_unitario or 0) for item in pedido.itens)
    return pedido.total


def _processar_fechamento_pedido(pedido):
    if not pedido.itens:
        raise ValidationError('Pedido sem itens nao pode ser fechado.')

    if not pedido.estoque_processado:
        for item in pedido.itens:
            produto = item.produto or Produto.query.get(item.produto_id)
            if not produto:
                raise NotFound(f'Produto do item {item.id} nao encontrado.')
            if produto.quantidade_estoque < item.quantidade:
                raise BusinessRuleError(f'Estoque insuficiente para "{produto.nome}".')

        for item in pedido.itens:
            produto = item.produto or Produto.query.get(item.produto_id)
            produto.quantidade_estoque -= item.quantidade
            db.session.add(Movimentacao(
                produto_id=produto.id,
                tipo=Movimentacao.TIPO_SAIDA,
                quantidade=item.quantidade,
                motivo='venda',
                observacoes=f'Pedido {pedido.id} fechado'
            ))
        pedido.estoque_processado = True

    if pedido.caixa_id and not pedido.financeiro_processado:
        caixa = pedido.caixa or Caixa.query.get(pedido.caixa_id)
        if not caixa:
            raise NotFound('Caixa do pedido nao encontrada.')
        if not caixa.aberto:
            raise BusinessRuleError('Caixa do pedido esta fechada. Nao e possivel concluir o financeiro.')

        valor_pedido = float(pedido.total or 0.0)
        caixa.saldo_atual = float(caixa.saldo_atual or 0.0) + valor_pedido
        db.session.add(MovimentacaoCaixa(
            caixa_id=caixa.id,
            tipo=MovimentacaoCaixa.TIPO_ENTRADA,
            valor=valor_pedido,
            descricao=f'Fechamento do pedido #{pedido.id}'
        ))
        pedido.financeiro_processado = True

    pedido.fechado_em = datetime.utcnow()
    if pedido.mesa:
        pedido.mesa.status = 'livre'


def _aplicar_transicao_status(pedido, novo_status):
    return pedido.transitar_para(novo_status, on_fechamento=_processar_fechamento_pedido)

```


### Arquivo: `app/services/pedido_service.py`
- Linhas: 25
- Tamanho: 0.6 KB
- Status: completo

```python
from app.services.pedido import (
    _aplicar_transicao_status,
    _normalizar_item_payload,
    _processar_fechamento_pedido,
    _recalcular_total_pedido,
)


normalizar_item_payload = _normalizar_item_payload
recalcular_total_pedido = _recalcular_total_pedido
processar_fechamento_pedido = _processar_fechamento_pedido
aplicar_transicao_status = _aplicar_transicao_status


__all__ = [
    '_normalizar_item_payload',
    '_recalcular_total_pedido',
    '_processar_fechamento_pedido',
    '_aplicar_transicao_status',
    'normalizar_item_payload',
    'recalcular_total_pedido',
    'processar_fechamento_pedido',
    'aplicar_transicao_status',
]

```


### Arquivo: `app/services/rh.py`
- Linhas: 55
- Tamanho: 1.5 KB
- Status: completo

```python
from flask import request

from app.helpers import _normalizar_texto
from app.constants import ENDPOINT_TO_PAGINA
from models import Garcom


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
            from models import db
            db.session.add(garcom)
        else:
            garcom.nome = funcionario.nome
            garcom.ativo = funcionario.ativo
        return

    if garcom:
        garcom.nome = funcionario.nome
        garcom.ativo = False


def funcionario_tem_acesso(funcionario, endpoint, paginas_resolvidas):
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

    return pagina in paginas_resolvidas


def _paginas_permitidas_para_funcionario(funcionario, resolver_paginas):
    return resolver_paginas(funcionario)

```


### Arquivo: `app/services/rh_service.py`
- Linhas: 17
- Tamanho: 0.4 KB
- Status: completo

```python
from app.services.rh import (
    _paginas_permitidas_para_funcionario,
    funcionario_tem_acesso,
    sincronizar_garcom_funcionario,
)


paginas_permitidas_para_funcionario = _paginas_permitidas_para_funcionario


__all__ = [
    'sincronizar_garcom_funcionario',
    'funcionario_tem_acesso',
    '_paginas_permitidas_para_funcionario',
    'paginas_permitidas_para_funcionario',
]

```


### Arquivo: `app/services/utils.py`
- Linhas: 35
- Tamanho: 0.8 KB
- Status: completo

```python
import re
import unicodedata


def _to_float(valor, default=None):
    if valor is None or valor == '':
        return default
    if isinstance(valor, str):
        valor = valor.replace(',', '.').strip()
    return float(valor)


def _to_int(valor, default=None):
    if valor is None or valor == '':
        return default
    return int(valor)


def _sem_acentos(texto):
    base = unicodedata.normalize('NFKD', str(texto or ''))
    return ''.join(char for char in base if not unicodedata.combining(char))


def _slugify(value):
    texto = _sem_acentos(value)
    texto = re.sub(r'[^a-zA-Z0-9]+', '-', texto).strip('-').lower()
    return texto


def _normalizar_contato(valor):
    texto = (valor or '').strip()
    if not texto:
        return None
    return re.sub(r'\s+', ' ', texto)

```


### Arquivo: `app/services/utils_service.py`
- Linhas: 92
- Tamanho: 1.9 KB
- Status: completo

```python
import re
from datetime import datetime

from app.services.utils import (
    _normalizar_contato,
    _sem_acentos,
    _slugify,
    _to_float,
    _to_int,
)


to_float = _to_float
to_int = _to_int
normalizar_contato = _normalizar_contato
sem_acentos = _sem_acentos
slugify = _slugify


def validar_float(valor, default=None):
    try:
        return _to_float(valor, default)
    except (TypeError, ValueError):
        return default


def validar_int(valor, default=None):
    try:
        return _to_int(valor, default)
    except (TypeError, ValueError):
        return default


def validar_data(valor, formato='%Y-%m-%d'):
    texto = str(valor or '').strip()
    if not texto:
        return None
    try:
        return datetime.strptime(texto, formato).date()
    except ValueError:
        return None


def validar_email(valor):
    texto = str(valor or '').strip().lower()
    if not texto:
        return None
    if re.fullmatch(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', texto):
        return texto
    return None


def validar_telefone(valor, *, minimo=10):
    digits = re.sub(r'[^0-9]+', '', str(valor or ''))
    if len(digits) < minimo:
        return None
    return digits


def validar_cpf(valor):
    digits = re.sub(r'[^0-9]+', '', str(valor or ''))
    if len(digits) != 11 or len(set(digits)) == 1:
        return None

    soma = sum(int(digits[i]) * (10 - i) for i in range(9))
    dv1 = (soma * 10 % 11) % 10
    soma = sum(int(digits[i]) * (11 - i) for i in range(10))
    dv2 = (soma * 10 % 11) % 10
    if digits[-2:] != f'{dv1}{dv2}':
        return None
    return digits


__all__ = [
    '_to_float',
    '_to_int',
    '_normalizar_contato',
    '_sem_acentos',
    '_slugify',
    'to_float',
    'to_int',
    'normalizar_contato',
    'sem_acentos',
    'slugify',
    'validar_float',
    'validar_int',
    'validar_data',
    'validar_email',
    'validar_telefone',
    'validar_cpf',
]

```


### Arquivo: `app/services_routes.py`
- Linhas: 3
- Tamanho: 0.1 KB
- Status: completo

```python
def register_routes(app, context=None):
    return app

```


### Arquivo: `app/utils/data.py`
- Linhas: 38
- Tamanho: 1.5 KB
- Status: completo

```python
from datetime import datetime, timedelta


def parse_date_range(data_inicial_str, data_final_str, default_days=7):
    """Normaliza intervalo de datas em formato YYYY-MM-DD para uso em filtros."""
    agora = datetime.utcnow()
    inicio_hoje = agora.replace(hour=0, minute=0, second=0, microsecond=0)
    fim_hoje = inicio_hoje + timedelta(days=1)

    data_inicial_str = (data_inicial_str or '').strip()
    data_final_str = (data_final_str or '').strip()

    try:
        if data_inicial_str:
            inicio_periodo = datetime.strptime(data_inicial_str, '%Y-%m-%d')
        else:
            inicio_periodo = inicio_hoje - timedelta(days=max(default_days - 1, 0))
            data_inicial_str = inicio_periodo.strftime('%Y-%m-%d')
    except ValueError:
        inicio_periodo = inicio_hoje - timedelta(days=max(default_days - 1, 0))
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

    return inicio_periodo, fim_periodo, data_inicial_str, data_final_str

```


### Arquivo: `app/utils/helpers.py`
- Linhas: 18
- Tamanho: 0.4 KB
- Status: completo

```python
import re
import unicodedata

from app.utils.data import parse_date_range


def sem_acentos(texto):
    base = unicodedata.normalize('NFKD', str(texto or ''))
    return ''.join(char for char in base if not unicodedata.combining(char))


def slugify(valor):
    texto = sem_acentos(valor)
    return re.sub(r'[^a-zA-Z0-9]+', '-', texto).strip('-').lower()


__all__ = ['sem_acentos', 'slugify', 'parse_date_range']

```


### Arquivo: `app/utils/payment_config.py`
- Linhas: 199
- Tamanho: 7.3 KB
- Status: completo

```python
import json
import re


DEFAULT_PDV_PAYMENT_OPTIONS = [
    {'id': 'dinheiro', 'label': 'Dinheiro', 'descricao': 'Recebimento em especie com troco.'},
    {'id': 'cartao', 'label': 'Cartao', 'descricao': 'Cartao de credito ou debito no caixa.'},
    {'id': 'pix', 'label': 'Pix', 'descricao': 'Transferencia instantanea por QR Code.'},
    {'id': 'crediario', 'label': 'Crediario', 'descricao': 'Venda no crediario da loja.'},
    {'id': 'dividido', 'label': 'Dividido', 'descricao': 'Divide o pagamento entre dinheiro e cartao.'},
]

DEFAULT_ECOMMERCE_PAYMENT_OPTIONS = [
    {'id': 'pix', 'label': 'Pix', 'descricao': 'Confirmacao imediata da compra.'},
    {'id': 'cartao_credito', 'label': 'Cartao de credito', 'descricao': 'Pagamento em credito na retirada ou entrega.'},
    {'id': 'cartao_debito', 'label': 'Cartao de debito', 'descricao': 'Pagamento em debito na retirada ou entrega.'},
    {'id': 'dinheiro', 'label': 'Dinheiro', 'descricao': 'Informe o valor para troco.'},
    {'id': 'vale_alimentacao', 'label': 'Vale-alimentacao', 'descricao': 'Aceite de beneficios e convenios alimentares.'},
]


def _slugify(value):
    texto = (value or '').strip().lower()
    texto = re.sub(r'[^a-z0-9]+', '_', texto)
    return texto.strip('_')


def _normalize_text(value):
    return re.sub(r'[^a-z0-9]+', '', (value or '').strip().lower())


def _load_json_list(raw_value):
    if not raw_value:
        return []
    try:
        data = json.loads(raw_value)
    except Exception:
        return []
    return data if isinstance(data, list) else []


def _payment_defaults(channel):
    if channel == 'pdv':
        return DEFAULT_PDV_PAYMENT_OPTIONS
    return DEFAULT_ECOMMERCE_PAYMENT_OPTIONS


def load_payment_options(raw_value, channel):
    defaults = _payment_defaults(channel)
    source = _load_json_list(raw_value)
    items = source if source else defaults

    options = []
    seen = set()
    for item in items:
        if isinstance(item, dict):
            payment_id = _slugify(item.get('id') or item.get('codigo') or item.get('label'))
            label = (item.get('label') or item.get('nome') or '').strip()
            description = (item.get('descricao') or item.get('description') or '').strip()
            active = item.get('ativo', True) is not False
        else:
            parts = [part.strip() for part in str(item or '').split('|')]
            payment_id = _slugify(parts[0] if parts else '')
            label = parts[1] if len(parts) > 1 else ''
            description = parts[2] if len(parts) > 2 else ''
            active = True
        if not payment_id or payment_id in seen or not active:
            continue
        seen.add(payment_id)
        if not label:
            label = payment_id.replace('_', ' ').title()
        options.append({
            'id': payment_id,
            'label': label,
            'descricao': description,
            'requires_cash_amount': payment_id == 'dinheiro',
            'supports_split': payment_id == 'dividido',
            'supports_credit_account': payment_id == 'crediario',
        })

    return options or [dict(item) for item in defaults]


def payment_options_to_text(raw_value, channel):
    options = load_payment_options(raw_value, channel)
    lines = []
    for item in options:
        lines.append(' | '.join([
            item.get('id') or '',
            item.get('label') or '',
            item.get('descricao') or '',
        ]).rstrip())
    return '\n'.join(lines)


def payment_text_to_json(text, channel):
    defaults_by_id = {item['id']: item for item in _payment_defaults(channel)}
    options = []
    seen = set()
    for line in (text or '').splitlines():
        parts = [part.strip() for part in line.split('|')]
        payment_id = _slugify(parts[0] if parts else '')
        if not payment_id or payment_id in seen:
            continue
        seen.add(payment_id)
        default = defaults_by_id.get(payment_id, {})
        label = parts[1] if len(parts) > 1 and parts[1] else default.get('label') or payment_id.replace('_', ' ').title()
        description = parts[2] if len(parts) > 2 and parts[2] else default.get('descricao') or ''
        options.append({
            'id': payment_id,
            'label': label,
            'descricao': description,
            'ativo': True,
        })
    return json.dumps(options, ensure_ascii=False) if options else None


def payment_methods_map(raw_value, channel):
    return {item['id']: item['label'] for item in load_payment_options(raw_value, channel)}


def default_payment_id(raw_value, channel):
    options = load_payment_options(raw_value, channel)
    return options[0]['id'] if options else None


def infer_payment_method_id(stored_value, options):
    raw_text = (stored_value or '').strip().lower()
    raw_key = _normalize_text(raw_text)
    if not raw_key:
        return ''
    for item in options:
        option_id = (item.get('id') or '').strip().lower()
        option_label = _normalize_text(item.get('label'))
        if option_id and option_id in raw_text:
            return option_id
        if option_label and option_label in raw_key:
            return option_id
    return ''


def load_api_integrations(raw_value):
    items = []
    for item in _load_json_list(raw_value):
        if not isinstance(item, dict):
            continue
        integration_id = _slugify(item.get('id') or item.get('nome') or item.get('provider'))
        if not integration_id:
            continue
        items.append({
            'id': integration_id,
            'nome': (item.get('nome') or '').strip(),
            'provider': (item.get('provider') or '').strip(),
            'ambiente': (item.get('ambiente') or '').strip(),
            'base_url': (item.get('base_url') or '').strip(),
            'chave_publica': (item.get('chave_publica') or '').strip(),
            'token_secreto': (item.get('token_secreto') or '').strip(),
            'webhook_url': (item.get('webhook_url') or '').strip(),
        })
    return items


def api_integrations_to_text(raw_value):
    lines = []
    for item in load_api_integrations(raw_value):
        lines.append(' | '.join([
            item.get('id') or '',
            item.get('nome') or '',
            item.get('provider') or '',
            item.get('ambiente') or '',
            item.get('base_url') or '',
            item.get('chave_publica') or '',
            item.get('token_secreto') or '',
            item.get('webhook_url') or '',
        ]).rstrip())
    return '\n'.join(lines)


def api_integrations_text_to_json(text):
    items = []
    seen = set()
    for line in (text or '').splitlines():
        parts = [part.strip() for part in line.split('|')]
        integration_id = _slugify(parts[0] if parts else '')
        if not integration_id or integration_id in seen:
            continue
        seen.add(integration_id)
        items.append({
            'id': integration_id,
            'nome': parts[1] if len(parts) > 1 else '',
            'provider': parts[2] if len(parts) > 2 else '',
            'ambiente': parts[3] if len(parts) > 3 else '',
            'base_url': parts[4] if len(parts) > 4 else '',
            'chave_publica': parts[5] if len(parts) > 5 else '',
            'token_secreto': parts[6] if len(parts) > 6 else '',
            'webhook_url': parts[7] if len(parts) > 7 else '',
        })
    return json.dumps(items, ensure_ascii=False) if items else None

```


### Arquivo: `app/utils/validators.py`
- Linhas: 106
- Tamanho: 2.6 KB
- Status: completo

```python
import re
from datetime import datetime


def validar_cpf(cpf):
    digitos = re.sub(r'\D', '', str(cpf or ''))
    if not digitos:
        return None
    if len(digitos) != 11:
        return '__invalid__'
    return f'{digitos[:3]}.{digitos[3:6]}.{digitos[6:9]}-{digitos[9:]}'


def validar_cnpj(cnpj):
    digitos = re.sub(r'\D', '', str(cnpj or ''))
    if not digitos:
        return None
    return digitos if len(digitos) == 14 else '__invalid__'


def validar_email(email):
    texto = str(email or '').strip().lower()
    if not texto:
        return None
    if re.fullmatch(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', texto):
        return texto
    return None


def validar_telefone(telefone):
    digitos = re.sub(r'[^0-9]+', '', str(telefone or ''))
    return digitos if len(digitos) >= 10 else None


def validar_cep(cep):
    digitos = re.sub(r'[^0-9]+', '', str(cep or ''))
    if not digitos:
        return None
    return digitos if len(digitos) == 8 else '__invalid__'


def validar_data(data_str):
    texto = str(data_str or '').strip()
    if not texto:
        return None
    try:
        return datetime.strptime(texto, '%Y-%m-%d').date()
    except ValueError:
        return None


def validar_float(valor):
    if valor is None or valor == '':
        return None
    try:
        return float(str(valor).replace(',', '.').strip())
    except (TypeError, ValueError):
        return None


def validar_int(valor):
    if valor is None or valor == '':
        return None
    try:
        return int(valor)
    except (TypeError, ValueError):
        return None


def normalizar_matricula(valor):
    matricula = re.sub(r'[^A-Z0-9]+', '', str(valor or '').strip().upper())
    return matricula or None


def _ean13_digito_verificador(base12):
    soma_impares = sum(int(base12[i]) for i in range(0, 12, 2))
    soma_pares = sum(int(base12[i]) for i in range(1, 12, 2))
    total = soma_impares + (soma_pares * 3)
    return str((10 - (total % 10)) % 10)


def normalizar_codigo_barras(codigo):
    digits = re.sub(r'\D', '', str(codigo or '').strip())
    if len(digits) == 12:
        digits = f'0{digits}'
    if len(digits) != 13:
        return None, 'Codigo de barras deve seguir EAN-13 (13 digitos numericos).'
    esperado = _ean13_digito_verificador(digits[:12])
    if digits[-1] != esperado:
        return None, 'Codigo de barras EAN-13 invalido (digito verificador incorreto).'
    return digits, None


__all__ = [
    'validar_cpf',
    'validar_cnpj',
    'validar_email',
    'validar_telefone',
    'validar_cep',
    'validar_data',
    'validar_float',
    'validar_int',
    'normalizar_matricula',
    'normalizar_codigo_barras',
]

```


### Arquivo: `config.py`
- Linhas: 57
- Tamanho: 1.4 KB
- Status: completo

```python
import os
from datetime import timedelta

DEV_FALLBACK_SECRET = 'dev-secret-key-change-in-production'


class Config:
    """Configuracao base da aplicacao."""

    SQLALCHEMY_DATABASE_URI = 'sqlite:///estoque.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', DEV_FALLBACK_SECRET)
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = False
    PREFERRED_URL_SCHEME = 'http'
    ENV_NAME = 'base'
    CACHE_TYPE = os.environ.get('CACHE_TYPE', 'SimpleCache')
    CACHE_DEFAULT_TIMEOUT = int(os.environ.get('CACHE_DEFAULT_TIMEOUT', '60'))
    CACHE_REDIS_URL = os.environ.get('CACHE_REDIS_URL')
    RATELIMIT_STORAGE_URI = os.environ.get('RATELIMIT_STORAGE_URI', 'memory://')


class DevelopmentConfig(Config):
    """Configuracao de desenvolvimento."""

    DEBUG = True
    TESTING = False
    ENV_NAME = 'development'


class ProductionConfig(Config):
    """Configuracao de producao."""

    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    PREFERRED_URL_SCHEME = 'https'
    ENV_NAME = 'production'


class TestingConfig(Config):
    """Configuracao de testes."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    ENV_NAME = 'testing'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
}

```


### Arquivo: `fix_admin_access.py`
- Linhas: 48
- Tamanho: 1.4 KB
- Status: completo

```python
"""
Script para corrigir/criar acesso do admin
Execute: python fix_admin_access.py
"""
import os

from app import app, db
from models import Funcionario

def fix_admin_access():
    """Cria ou atualiza o admin"""
    
    with app.app_context():
        email = os.environ.get("SYSTEMLR_ADMIN_EMAIL", "admin@conveniencia.local")
        senha = os.environ.get("SYSTEMLR_ADMIN_PASSWORD", "142536")
        nome = os.environ.get("SYSTEMLR_ADMIN_NAME", "Administrador")
        
        # Procurar por admin existente
        admin = Funcionario.query.filter_by(email=email).first()
        
        if admin:
            print(f"✏️  Atualizando admin existente: {admin.nome}")
            admin.set_password(senha)
            admin.role = "admin"
            admin.ativo = True
        else:
            print(f"✨ Criando novo admin...")
            admin = Funcionario(
                nome=nome,
                email=email,
                role="admin",
                ativo=True
            )
            admin.set_password(senha)
            db.session.add(admin)
        if admin and admin.nome != nome:
            admin.nome = nome
        
        db.session.commit()
        print(f"✅ Acesso de admin corrigido com sucesso!")
        print(f"   Email: {email}")
        print(f"   Senha: {senha}")
        print(f"   Role: admin")
        print(f"   Ativo: {admin.ativo}")

if __name__ == "__main__":
    fix_admin_access()

```


### Arquivo: `models.py`
- Linhas: 1149
- Tamanho: 51.3 KB
- Status: completo

```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Categoria(db.Model):
    __tablename__ = 'categorias'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    descricao = db.Column(db.Text)
    imagem_path = db.Column(db.String(255))
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    
    produtos = db.relationship('Produto', backref='categoria', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Categoria {self.nome}>'

class Produto(db.Model):
    __tablename__ = 'produtos'
    __table_args__ = (
        db.Index('ix_produtos_categoria_fornecedor', 'categoria_id', 'fornecedor_id'),
        db.Index('ix_produtos_endereco_ativo', 'endereco_id', 'ativo'),
    )

    STATUS_DISPONIVEL_ONLINE = 'online'
    STATUS_DISPONIVEL_OFF = 'off'
    STATUS_DISPONIBILIDADE_VALIDOS = [
        STATUS_DISPONIVEL_ONLINE,
        STATUS_DISPONIVEL_OFF,
    ]
    STATUS_DISPONIBILIDADE_ONLINE_EQUIVALENTES = [
        STATUS_DISPONIVEL_ONLINE,
        'disponivel_online',
        'disponivel_venda',
    ]
    STATUS_DISPONIBILIDADE_OFF_EQUIVALENTES = [
        STATUS_DISPONIVEL_OFF,
        'indisponivel',
        'somente_ressuprimento',
    ]
    
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False, index=True)
    nome = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text)
    imagem_path = db.Column(db.String(255))
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedores.id'), nullable=True)
    endereco_id = db.Column(db.Integer, db.ForeignKey('enderecos_estoque.id'), nullable=True)
    preco_custo = db.Column(db.Float, nullable=False)
    preco_venda = db.Column(db.Float, nullable=False)
    quantidade_estoque = db.Column(db.Integer, default=0)
    quantidade_minima = db.Column(db.Integer, default=5)
    status_disponibilidade = db.Column(db.String(30), default=STATUS_DISPONIVEL_ONLINE, nullable=False)
    tipo_movimentacao = db.Column(db.String(20), default='manual', nullable=False)
    fora_picking = db.Column(db.Boolean, default=False)
    prioridade_reabastecimento = db.Column(db.Integer, nullable=True)
    ultima_baixa_picking_em = db.Column(db.DateTime, nullable=True)
    servico_montagem_disponivel = db.Column(db.Boolean, default=False)
    servico_instalacao_disponivel = db.Column(db.Boolean, default=False)
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    movimentacoes = db.relationship('Movimentacao', backref='produto', lazy=True, cascade='all, delete-orphan')
    fornecedor = db.relationship('Fornecedor', backref=db.backref('produtos', lazy=True))
    
    def __repr__(self):
        return f'<Produto {self.nome}>'
    
    @property
    def lucro_unitario(self):
        return self.preco_venda - self.preco_custo
    
    @property
    def margem_lucro(self):
        if self.preco_venda == 0:
            return 0
        return ((self.preco_venda - self.preco_custo) / self.preco_venda) * 100
    
    @property
    def em_falta(self):
        return self.quantidade_estoque < self.quantidade_minima

    @classmethod
    def normalizar_status_disponibilidade(cls, status):
        status_normalizado = (status or cls.STATUS_DISPONIVEL_ONLINE).strip().lower()
        if status_normalizado in cls.STATUS_DISPONIBILIDADE_ONLINE_EQUIVALENTES:
            return cls.STATUS_DISPONIVEL_ONLINE
        if status_normalizado in cls.STATUS_DISPONIBILIDADE_OFF_EQUIVALENTES:
            return cls.STATUS_DISPONIVEL_OFF
        return cls.STATUS_DISPONIVEL_ONLINE

    @property
    def disponivel_para_venda(self):
        status = self.normalizar_status_disponibilidade(self.status_disponibilidade)
        return bool(self.ativo) and status == self.STATUS_DISPONIVEL_ONLINE

    @property
    def status_disponibilidade_label(self):
        status = self.normalizar_status_disponibilidade(self.status_disponibilidade)
        labels = {
            self.STATUS_DISPONIVEL_ONLINE: 'Online',
            self.STATUS_DISPONIVEL_OFF: 'Off',
        }
        return labels.get(status, 'Online')

class Movimentacao(db.Model):
    __tablename__ = 'movimentacoes'
    __table_args__ = (
        db.Index('ix_movimentacoes_tipo_criado_em', 'tipo', 'criado_em'),
        db.Index('ix_movimentacoes_produto_criado_em', 'produto_id', 'criado_em'),
    )
    
    TIPO_ENTRADA = 'entrada'
    TIPO_SAIDA = 'saida'
    TIPO_TRANSFERENCIA = 'transferencia'
    TIPOS = [TIPO_ENTRADA, TIPO_SAIDA, TIPO_TRANSFERENCIA]
    
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedores.id'), nullable=True)
    endereco_origem_id = db.Column(db.Integer, db.ForeignKey('enderecos_estoque.id'), nullable=True)
    endereco_destino_id = db.Column(db.Integer, db.ForeignKey('enderecos_estoque.id'), nullable=True)
    tipo = db.Column(db.String(20), nullable=False)  # entrada ou saida
    quantidade = db.Column(db.Integer, nullable=False)
    valor_compra = db.Column(db.Float, nullable=True)
    info_nota = db.Column(db.String(255))
    motivo = db.Column(db.String(200))  # venda, compra, devolução, perda, etc
    observacoes = db.Column(db.Text)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    endereco_origem = db.relationship(
        'EnderecoEstoque',
        foreign_keys=[endereco_origem_id],
        backref=db.backref('movimentacoes_como_origem', lazy=True),
        lazy='select',
    )
    endereco_destino = db.relationship(
        'EnderecoEstoque',
        foreign_keys=[endereco_destino_id],
        backref=db.backref('movimentacoes_como_destino', lazy=True),
        lazy='select',
    )
    
    def __repr__(self):
        return f'<Movimentacao {self.produto_id} - {self.tipo}>'


class EquipamentoMovimentacao(db.Model):
    __tablename__ = 'equipamentos_movimentacao'

    TIPO_EMPILHADEIRA = 'empilhadeira'
    TIPO_PALETEIRA = 'paleteira'
    TIPO_CARRINHO = 'carrinho'
    TIPOS_VALIDOS = [TIPO_EMPILHADEIRA, TIPO_PALETEIRA, TIPO_CARRINHO]

    STATUS_OPERACIONAL = 'operacional'
    STATUS_MANUTENCAO = 'manutencao'
    STATUS_INATIVO = 'inativo'
    STATUS_VALIDOS = [STATUS_OPERACIONAL, STATUS_MANUTENCAO, STATUS_INATIVO]

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(40), unique=True, nullable=False, index=True)
    nome = db.Column(db.String(120), nullable=False)
    tipo = db.Column(db.String(20), nullable=False, default=TIPO_EMPILHADEIRA)
    placa = db.Column(db.String(20), nullable=True)
    capacidade_kg = db.Column(db.Float, nullable=True)
    bateria_codigo = db.Column(db.String(40), nullable=True)
    bateria_nivel = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(20), nullable=False, default=STATUS_OPERACIONAL)
    proxima_manutencao_em = db.Column(db.Date, nullable=True)
    observacoes = db.Column(db.Text, nullable=True)
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    manutencoes = db.relationship(
        'ManutencaoEquipamento',
        backref='equipamento',
        lazy=True,
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'<EquipamentoMovimentacao {self.codigo} - {self.tipo}>'


class ManutencaoEquipamento(db.Model):
    __tablename__ = 'manutencoes_equipamento'

    id = db.Column(db.Integer, primary_key=True)
    equipamento_id = db.Column(db.Integer, db.ForeignKey('equipamentos_movimentacao.id'), nullable=False, index=True)
    tipo = db.Column(db.String(20), nullable=False, default='preventiva')
    descricao = db.Column(db.String(255), nullable=False)
    custo = db.Column(db.Float, nullable=True)
    realizado_em = db.Column(db.Date, nullable=True)
    proxima_em = db.Column(db.Date, nullable=True)
    responsavel = db.Column(db.String(120), nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<ManutencaoEquipamento eq={self.equipamento_id} tipo={self.tipo}>'


# ======= NOVOS MODELOS =======

class Fornecedor(db.Model):
    __tablename__ = 'fornecedores'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), unique=True, nullable=False)
    documento = db.Column(db.String(30), nullable=True)
    contato = db.Column(db.String(120))
    telefone = db.Column(db.String(30))
    email = db.Column(db.String(120))
    endereco_rua = db.Column(db.String(160), nullable=True)
    endereco_numero = db.Column(db.String(20), nullable=True)
    endereco_bairro = db.Column(db.String(100), nullable=True)
    endereco_cidade = db.Column(db.String(100), nullable=True)
    tipo_produtos_fornece = db.Column(db.String(255), nullable=True)
    observacoes_gerais = db.Column(db.Text, nullable=True)
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    movimentacoes = db.relationship('Movimentacao', backref='fornecedor', lazy=True)
    recebimentos = db.relationship('RecebimentoFornecedor', backref='fornecedor', lazy=True)

    def __repr__(self):
        return f'<Fornecedor {self.nome}>'


class Estoque(db.Model):
    __tablename__ = 'estoques'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), unique=True, nullable=False)
    codigo_filial = db.Column(db.String(20), nullable=True, index=True)
    descricao = db.Column(db.String(255))
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    endereco_origem_id = db.Column(db.Integer, db.ForeignKey('enderecos_estoque.id'), nullable=True)
    endereco_destino_id = db.Column(db.Integer, db.ForeignKey('enderecos_estoque.id'), nullable=True)

    endereco_origem = db.relationship(
        'EnderecoEstoque',
        foreign_keys=[endereco_origem_id],
        backref='estoques_como_origem',
        lazy='select'
    )
    endereco_destino = db.relationship(
        'EnderecoEstoque',
        foreign_keys=[endereco_destino_id],
        backref='estoques_como_destino',
        lazy='select'
    )

    enderecos = db.relationship(
        'EnderecoEstoque',
        foreign_keys='EnderecoEstoque.estoque_id',
        backref=db.backref('estoque', foreign_keys='EnderecoEstoque.estoque_id'),
        lazy=True
    )

    def __repr__(self):
        return f'<Estoque {self.nome}>'


funcionario_estoques = db.Table(
    'funcionario_estoques',
    db.Column('funcionario_id', db.Integer, db.ForeignKey('funcionarios.id'), primary_key=True),
    db.Column('estoque_id', db.Integer, db.ForeignKey('estoques.id'), primary_key=True),
)


class EnderecoEstoque(db.Model):
    __tablename__ = 'enderecos_estoque'
    __table_args__ = (
        db.Index('ix_enderecos_estoque_estoque_status', 'estoque_id', 'status'),
        db.UniqueConstraint(
            'codigo_armazem',
            'rua_corredor',
            'coluna_baia',
            'nivel_prateleira',
            'posicao_slot',
            name='uq_endereco_componentes'
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    estoque_id = db.Column(db.Integer, db.ForeignKey('estoques.id'), nullable=True)
    nome = db.Column(db.String(120), nullable=False, unique=True)
    codigo_localizacao = db.Column(db.String(60), unique=True, nullable=True)
    loja_cd = db.Column(db.String(20), nullable=True)
    setor_zona = db.Column(db.String(30), nullable=True)
    tipo_area = db.Column(db.String(40), nullable=True)
    status = db.Column(db.String(20), default='ativo', nullable=False)
    descricao = db.Column(db.String(255), nullable=True)
    tipo_estrutura = db.Column(db.String(20), nullable=True)
    codigo_armazem = db.Column(db.String(20), nullable=True)
    rua_corredor = db.Column(db.String(20), nullable=True)
    coluna_baia = db.Column(db.String(10), nullable=True)
    nivel_prateleira = db.Column(db.String(10), nullable=True)
    posicao_slot = db.Column(db.String(10), nullable=True)
    lado = db.Column(db.String(4), nullable=True)
    ponto_local = db.Column(db.String(255), nullable=True)
    permite_fracionado = db.Column(db.Boolean, default=False)
    permite_mistura_sku = db.Column(db.Boolean, default=False)
    permite_mistura_lote = db.Column(db.Boolean, default=False)
    controle_validade = db.Column(db.String(20), default='nenhum', nullable=True)
    temperatura = db.Column(db.String(20), nullable=True)
    restricoes = db.Column(db.String(255), nullable=True)
    capacidade_caixas = db.Column(db.Integer, nullable=True)
    capacidade_fardos = db.Column(db.Integer, nullable=True)
    capacidade_unidades = db.Column(db.Integer, nullable=True)
    capacidade_pallets = db.Column(db.Integer, nullable=True)
    peso_max_kg = db.Column(db.Float, nullable=True)
    volume_max_m3 = db.Column(db.Float, nullable=True)
    prioridade_picking = db.Column(db.Integer, nullable=True)
    observacoes = db.Column(db.Text, nullable=True)
    tipo_produto_reservado = db.Column(db.String(120), nullable=True)
    sku_produto = db.Column(db.String(100), nullable=True)
    data_alocacao = db.Column(db.DateTime, nullable=True)
    tipo_endereco = db.Column(db.String(30), nullable=True)
    rua = db.Column(db.String(160))
    numero = db.Column(db.String(20))
    bairro = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(2))
    cep = db.Column(db.String(12))
    complemento = db.Column(db.String(120))
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    produtos = db.relationship('Produto', backref='endereco', lazy=True)

    def __repr__(self):
        return f'<EnderecoEstoque {self.nome}>'

    def build_codigo_localizacao(self, pad=2):
        """Gera codigo composto padronizado a partir dos componentes."""
        rc = (self.rua_corredor or '').strip().upper()
        cb = (self.coluna_baia or '').strip().zfill(pad)
        nv = (self.nivel_prateleira or '').strip().zfill(pad)
        ps = (self.posicao_slot or '').strip().zfill(pad)
        return '-'.join([rc, cb, nv, ps]) if rc and cb and nv and ps else None

    @property
    def rack_estante(self):
        return self.coluna_baia

    @rack_estante.setter
    def rack_estante(self, valor):
        self.coluna_baia = valor


class RecebimentoFornecedor(db.Model):
    __tablename__ = 'recebimentos_fornecedor'
    __table_args__ = (
        db.Index('ix_recebimentos_status_criado_em', 'status', 'criado_em'),
        db.Index('ix_recebimentos_fornecedor_criado_em', 'fornecedor_id', 'criado_em'),
    )

    TIPO_COMPRA_REVENDA = 'compra_revenda'
    TIPO_USO_CONSUMO = 'uso_consumo_operacional'
    TIPO_BONIFICACAO = 'bonificacao'
    TIPO_CONSIGNADO = 'consignado'
    TIPO_RETORNO_INDUSTRIALIZACAO = 'retorno_industrializacao'
    TIPOS_VALIDOS = [
        TIPO_COMPRA_REVENDA,
        TIPO_USO_CONSUMO,
        TIPO_BONIFICACAO,
        TIPO_CONSIGNADO,
        TIPO_RETORNO_INDUSTRIALIZACAO,
    ]

    STATUS_CRIADO = 'criado'
    STATUS_AGUARDANDO_ARMAZENAGEM = 'aguardando_armazenagem'
    STATUS_CONCLUIDO = 'concluido'
    STATUS_CANCELADO = 'cancelado'
    STATUS_VALIDOS = [
        STATUS_CRIADO,
        STATUS_AGUARDANDO_ARMAZENAGEM,
        STATUS_CONCLUIDO,
        STATUS_CANCELADO,
    ]

    id = db.Column(db.Integer, primary_key=True)
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedores.id'), nullable=True)
    tipo_recebimento = db.Column(db.String(40), nullable=False, default=TIPO_COMPRA_REVENDA)
    fornecedor_documento = db.Column(db.String(30), nullable=True)
    data_entrega = db.Column(db.Date, nullable=True)
    info_nota = db.Column(db.String(255), nullable=True)
    subtotal = db.Column(db.Float, nullable=True, default=0.0)
    desconto = db.Column(db.Float, nullable=True, default=0.0)
    total_pagar = db.Column(db.Float, nullable=True, default=0.0)
    status = db.Column(db.String(30), default=STATUS_CRIADO, nullable=False)
    observacoes = db.Column(db.Text, nullable=True)
    recebedor_funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=True)
    recebedor_nome = db.Column(db.String(120), nullable=True)
    recebedor_assinatura = db.Column(db.String(255), nullable=True)
    entregador_nome = db.Column(db.String(120), nullable=True)
    entregador_assinatura = db.Column(db.String(255), nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    conferido_em = db.Column(db.DateTime, nullable=True)
    armazenado_em = db.Column(db.DateTime, nullable=True)

    itens = db.relationship('RecebimentoItem', backref='recebimento', lazy=True, cascade='all, delete-orphan')
    recebedor_funcionario = db.relationship('Funcionario', foreign_keys=[recebedor_funcionario_id], lazy='select')

    def __repr__(self):
        return f'<RecebimentoFornecedor {self.id} - {self.status}>'


class RecebimentoItem(db.Model):
    __tablename__ = 'recebimentos_itens'

    id = db.Column(db.Integer, primary_key=True)
    recebimento_id = db.Column(db.Integer, db.ForeignKey('recebimentos_fornecedor.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    qtd_recebida = db.Column(db.Integer, nullable=False, default=0)
    unidade = db.Column(db.String(10), nullable=True)
    descricao_item = db.Column(db.String(255), nullable=True)
    preco_unitario = db.Column(db.Float, nullable=True, default=0.0)
    total_item = db.Column(db.Float, nullable=True, default=0.0)
    qtd_avaria = db.Column(db.Integer, nullable=False, default=0)
    lote = db.Column(db.String(80), nullable=True)
    validade = db.Column(db.Date, nullable=True)
    endereco_destino_id = db.Column(db.Integer, db.ForeignKey('enderecos_estoque.id'), nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    produto = db.relationship('Produto')
    endereco_destino = db.relationship('EnderecoEstoque')

    @property
    def qtd_liquida(self):
        return max(int(self.qtd_recebida or 0) - int(self.qtd_avaria or 0), 0)

    def __repr__(self):
        return f'<RecebimentoItem rec={self.recebimento_id} prod={self.produto_id}>'

class Caixa(db.Model):
    __tablename__ = 'caixas'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=True)
    saldo_inicial = db.Column(db.Float, default=0.0)
    saldo_atual = db.Column(db.Float, default=0.0)
    saldo_fechamento = db.Column(db.Float, nullable=True)
    aberto = db.Column(db.Boolean, default=False)
    aberto_em = db.Column(db.DateTime, nullable=True)
    fechado_em = db.Column(db.DateTime, nullable=True)
    observacoes = db.Column(db.Text)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    pedidos = db.relationship('Pedido', backref='caixa', lazy=True)
    funcionario = db.relationship('Funcionario', backref='caixas_abertas')
    movimentacoes_caixa = db.relationship('MovimentacaoCaixa', backref='caixa', lazy=True, cascade='all, delete-orphan')

    @property
    def diferenca(self):
        """Calcul a diferença entre saldo de fechamento e saldo_atual"""
        if self.saldo_fechamento is None:
            return None
        return self.saldo_fechamento - self.saldo_atual

    def __repr__(self):
        return f'<Caixa {self.nome} - {'aberto' if self.aberto else 'fechado'}>'


class Mesa(db.Model):
    __tablename__ = 'mesas'

    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(20), unique=True, nullable=False)
    capacidade = db.Column(db.Integer, default=4)
    status = db.Column(db.String(20), default='livre')  # livre, ocupada
    qr_token = db.Column(db.String(64), unique=True, nullable=True)
    descricao = db.Column(db.Text)

    pedidos = db.relationship('Pedido', backref='mesa', lazy=True)

    def __repr__(self):
        return f'<Mesa {self.numero} - {self.status}>'


class Pedido(db.Model):
    __tablename__ = 'pedidos'
    __table_args__ = (
        db.Index('ix_pedidos_status_criado_em', 'status', 'criado_em'),
        db.Index('ix_pedidos_status_fechado_em', 'status', 'fechado_em'),
    )

    STATUS_ABERTO = 'aberto'
    STATUS_EM_PREPARO = 'em_preparo'
    STATUS_ENTREGUE = 'entregue'
    STATUS_FECHADO = 'fechado'
    STATUS_CANCELADO = 'cancelado'
    STATUS_IMUTAVEIS = {STATUS_FECHADO, STATUS_CANCELADO}
    TRANSICOES_PERMITIDAS = {
        STATUS_ABERTO: {STATUS_EM_PREPARO, STATUS_ENTREGUE, STATUS_FECHADO, STATUS_CANCELADO},
        STATUS_EM_PREPARO: {STATUS_ENTREGUE, STATUS_FECHADO, STATUS_CANCELADO},
        STATUS_ENTREGUE: {STATUS_FECHADO, STATUS_CANCELADO},
        STATUS_FECHADO: set(),
        STATUS_CANCELADO: set(),
    }

    id = db.Column(db.Integer, primary_key=True)
    mesa_id = db.Column(db.Integer, db.ForeignKey('mesas.id'), nullable=True)
    caixa_id = db.Column(db.Integer, db.ForeignKey('caixas.id'), nullable=True)
    garcom_id = db.Column(db.Integer, db.ForeignKey('garcons.id'), nullable=True)
    cliente_nome = db.Column(db.String(120))
    cliente_celular = db.Column(db.String(30))
    total = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default=STATUS_ABERTO, index=True)  # aberto, em_preparo, entregue, fechado, cancelado
    origem = db.Column(db.String(20), default='interno')  # interno, qr
    metodo_pagamento = db.Column(db.String(50))
    valor_pago = db.Column(db.Float, nullable=True)
    estoque_processado = db.Column(db.Boolean, default=False)
    financeiro_processado = db.Column(db.Boolean, default=False)
    separacao_entrega_concluida = db.Column(db.Boolean, default=False)
    separacao_entrega_em = db.Column(db.DateTime, nullable=True)
    etiqueta_entrega_emitida_em = db.Column(db.DateTime, nullable=True)
    rota_entrega = db.Column(db.String(120), nullable=True)
    ordem_rota = db.Column(db.Integer, nullable=True)
    local_saida = db.Column(db.String(160), nullable=True)
    veiculo_tipo = db.Column(db.String(80), nullable=True)
    veiculo_placa = db.Column(db.String(20), nullable=True)
    motorista_nome = db.Column(db.String(120), nullable=True)
    empresa_terceirizada = db.Column(db.String(150), nullable=True)
    nota_fiscal_numero = db.Column(db.String(60), nullable=True)
    nota_fiscal_chave = db.Column(db.String(120), nullable=True)
    nota_fiscal_emitida_em = db.Column(db.DateTime, nullable=True)
    saiu_para_entrega_em = db.Column(db.DateTime, nullable=True)
    entrega_concluida_em = db.Column(db.DateTime, nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    fechado_em = db.Column(db.DateTime)
    observacoes = db.Column(db.Text)

    itens = db.relationship('ItemPedido', backref='pedido', lazy=True, cascade='all, delete-orphan')

    @staticmethod
    def _normalizar_status(status, default=STATUS_ABERTO):
        status = (status or default).strip().lower()
        return status if status in Pedido.TRANSICOES_PERMITIDAS else default

    def transitar_para(self, novo_status, on_fechamento=None):
        """Valida e aplica transicao de status do pedido."""
        status_atual = self._normalizar_status(self.status, default=self.STATUS_ABERTO)
        novo_status = self._normalizar_status(novo_status, default=status_atual)

        if status_atual in self.STATUS_IMUTAVEIS and novo_status != status_atual:
            raise ValueError(f'Pedido {status_atual} e imutavel.')
        if novo_status != status_atual and novo_status not in self.TRANSICOES_PERMITIDAS.get(status_atual, set()):
            raise ValueError(f'Transicao invalida: {status_atual} -> {novo_status}.')

        if novo_status == self.STATUS_FECHADO and status_atual != self.STATUS_FECHADO:
            if on_fechamento:
                on_fechamento(self)
            else:
                self.fechado_em = datetime.utcnow()
        elif novo_status == self.STATUS_CANCELADO and status_atual != self.STATUS_CANCELADO:
            self.fechado_em = datetime.utcnow()
            if self.mesa:
                self.mesa.status = 'livre'
        elif self.mesa and novo_status in {self.STATUS_ABERTO, self.STATUS_EM_PREPARO, self.STATUS_ENTREGUE}:
            self.mesa.status = 'ocupada'

        self.status = novo_status
        return self.status

    def calcular_total(self):
        self.total = sum(item.quantidade * item.preco_unitario for item in self.itens)
        return self.total

    def marcar_separacao_entrega(self, concluida=True):
        concluida = bool(concluida)
        self.separacao_entrega_concluida = concluida
        self.separacao_entrega_em = datetime.utcnow() if concluida else None
        return self.separacao_entrega_concluida

    def marcar_etiqueta_entrega_emitida(self):
        self.etiqueta_entrega_emitida_em = datetime.utcnow()
        return self.etiqueta_entrega_emitida_em

    def __repr__(self):
        return f'<Pedido {self.id} - {self.status}>'


class ClientePublico(db.Model):
    __tablename__ = 'clientes_publicos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, index=True)
    celular = db.Column(db.String(30), nullable=False, index=True)
    cpf_cnpj = db.Column(db.String(20), nullable=True, index=True)
    cep = db.Column(db.String(12), nullable=True)
    endereco = db.Column(db.String(180), nullable=True)
    numero = db.Column(db.String(20), nullable=True)
    complemento = db.Column(db.String(120), nullable=True)
    bairro = db.Column(db.String(100), nullable=True)
    cidade = db.Column(db.String(100), nullable=True)
    estado = db.Column(db.String(2), nullable=True)
    referencia = db.Column(db.String(180), nullable=True)
    recebe_ofertas = db.Column(db.Boolean, default=False)
    observacoes = db.Column(db.Text, nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<ClientePublico {self.nome} ({self.email})>'


class ItemPedido(db.Model):
    __tablename__ = 'itens_pedido'

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Integer, default=1)
    preco_unitario = db.Column(db.Float, nullable=False)

    produto = db.relationship('Produto')

    def __repr__(self):
        return f'<ItemPedido {self.produto.nome} x{self.quantidade}>'


class Garcom(db.Model):
    __tablename__ = 'garcons'

    id = db.Column(db.Integer, primary_key=True)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=True)
    nome = db.Column(db.String(120), nullable=False)
    celular = db.Column(db.String(30))
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    pedidos = db.relationship('Pedido', backref='garcom', lazy=True)
    funcionario = db.relationship('Funcionario', backref=db.backref('garcom_perfil', uselist=False))

    def __repr__(self):
        return f'<Garcom {self.nome}>'


class Funcionario(db.Model):
    __tablename__ = 'funcionarios'
    __table_args__ = (
        db.Index('ix_funcionarios_matricula_ativo', 'matricula', 'ativo'),
        db.Index('ix_funcionarios_email_ativo', 'email', 'ativo'),
        db.Index('ix_funcionarios_cpf_ativo', 'cpf', 'ativo'),
    )

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    numero_cadastro = db.Column(db.Integer, unique=True, nullable=True, index=True)
    matricula = db.Column(db.String(30), unique=True, nullable=True, index=True)
    cpf = db.Column(db.String(14), nullable=True, index=True)
    rg = db.Column(db.String(20), nullable=True)
    data_nascimento = db.Column(db.Date, nullable=True)
    celular = db.Column(db.String(30), nullable=True)
    cep = db.Column(db.String(12), nullable=True)
    endereco = db.Column(db.String(180), nullable=True)
    bairro = db.Column(db.String(100), nullable=True)
    cidade = db.Column(db.String(100), nullable=True)
    estado = db.Column(db.String(2), nullable=True)
    senha_hash = db.Column(db.String(255), nullable=False)
    imagem_perfil_path = db.Column(db.String(255), nullable=True)
    permitir_editar_imagem_perfil = db.Column(db.Boolean, default=False)
    senha_provisoria = db.Column(db.Boolean, default=False)
    role = db.Column(db.String(20), default='operador')  # admin, gerente, caixa, operador
    cargo = db.Column(db.String(100), nullable=True)
    departamento = db.Column(db.String(80), nullable=True)
    time_nome = db.Column(db.String(80), nullable=True)
    nivel_organograma = db.Column(db.String(40), nullable=True)
    pagina_inicial = db.Column(db.String(30), default='dashboard')
    receber_alertas = db.Column(db.Boolean, default=True)
    restricao_estoques_ativa = db.Column(db.Boolean, default=False)
    estoque_principal_id = db.Column(db.Integer, db.ForeignKey('estoques.id'), nullable=True)
    perfil_acesso_id = db.Column(db.Integer, db.ForeignKey('perfis_acesso.id'), nullable=True)
    superior_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=True)
    ativo = db.Column(db.Boolean, default=True)
    controle_acesso_ativo = db.Column(db.Boolean, default=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    permissoes = db.relationship('PermissaoAcesso', backref='funcionario', lazy=True, cascade='all, delete-orphan')
    estoque_principal = db.relationship('Estoque', foreign_keys=[estoque_principal_id], lazy='select')
    perfil_acesso = db.relationship('PerfilAcesso', foreign_keys=[perfil_acesso_id], lazy='select')
    estoques_permitidos = db.relationship(
        'Estoque',
        secondary=funcionario_estoques,
        backref=db.backref('funcionarios_vinculados', lazy='select'),
        lazy='select',
    )
    superior = db.relationship('Funcionario', remote_side=[id], backref=db.backref('subordinados', lazy=True))

    def set_password(self, senha):
        """Hash e armazena a senha."""
        self.senha_hash = generate_password_hash(senha)

    def check_password(self, senha):
        """Verifica se a senha fornecida corresponde ao hash armazenado."""
        return check_password_hash(self.senha_hash, senha)

    def __repr__(self):
        return f'<Funcionario {self.nome} - {self.role}>'


class AlmoxarifadoAtribuicao(db.Model):
    __tablename__ = 'almoxarifado_atribuicoes'

    DESTINO_FUNCIONARIO = 'funcionario'
    DESTINO_SETOR = 'setor'
    DESTINOS_VALIDOS = [DESTINO_FUNCIONARIO, DESTINO_SETOR]

    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False, index=True)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=True, index=True)
    registrado_por_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=True)
    destino_tipo = db.Column(db.String(20), nullable=False, default=DESTINO_FUNCIONARIO)
    nome_destino = db.Column(db.String(120), nullable=False)
    setor_destino = db.Column(db.String(80), nullable=True)
    matricula_referencia = db.Column(db.String(30), nullable=True)
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    observacoes = db.Column(db.Text, nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    produto = db.relationship('Produto', foreign_keys=[produto_id], lazy='select')
    funcionario = db.relationship('Funcionario', foreign_keys=[funcionario_id], lazy='select')
    registrado_por = db.relationship('Funcionario', foreign_keys=[registrado_por_id], lazy='select')

    def __repr__(self):
        return f'<AlmoxarifadoAtribuicao {self.id} prod={self.produto_id} destino={self.destino_tipo}>'


class FuncaoRH(db.Model):
    __tablename__ = 'funcoes_rh'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    descricao = db.Column(db.String(255))
    permissoes_padrao = db.Column(db.Text)  # Campo legado migrado para PerfilAcesso
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<FuncaoRH {self.nome}>'


class PerfilAcesso(db.Model):
    __tablename__ = 'perfis_acesso'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    descricao = db.Column(db.String(255))
    permissoes_padrao = db.Column(db.Text)
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<PerfilAcesso {self.nome}>'


class PermissaoAcesso(db.Model):
    __tablename__ = 'permissoes_acesso'

    id = db.Column(db.Integer, primary_key=True)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=False)
    pagina = db.Column(db.String(80), nullable=False)
    permitido = db.Column(db.Boolean, default=True, nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('funcionario_id', 'pagina', name='uq_funcionario_pagina'),
    )

    def __repr__(self):
        return f'<PermissaoAcesso funcionario={self.funcionario_id} pagina={self.pagina} permitido={self.permitido}>'


class MovimentacaoCaixa(db.Model):
    __tablename__ = 'movimentacoes_caixa'

    TIPO_ENTRADA = 'entrada'
    TIPO_SAIDA = 'saida'
    TIPOS = [TIPO_ENTRADA, TIPO_SAIDA]

    id = db.Column(db.Integer, primary_key=True)
    caixa_id = db.Column(db.Integer, db.ForeignKey('caixas.id'), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # entrada ou saida
    valor = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<MovimentacaoCaixa caixa={self.caixa_id} {self.tipo} {self.valor}>'


class LancamentoFinanceiro(db.Model):
    __tablename__ = 'lancamentos_financeiros'
    __table_args__ = (
        db.Index('ix_lancamentos_tipo_data_competencia', 'tipo', 'data_competencia'),
    )

    TIPO_CONSUMO_PROPRIO = 'consumo_proprio'
    TIPO_DESPESA = 'despesa'
    TIPO_RECEITA = 'receita'
    TIPO_AJUSTE = 'ajuste'
    TIPOS = [TIPO_CONSUMO_PROPRIO, TIPO_DESPESA, TIPO_RECEITA, TIPO_AJUSTE]

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(30), nullable=False, index=True)
    categoria = db.Column(db.String(80), nullable=True)
    descricao = db.Column(db.String(255), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data_competencia = db.Column(db.Date, nullable=False, index=True)
    incluir_contabilidade = db.Column(db.Boolean, default=True, nullable=False)
    enviado_contador = db.Column(db.Boolean, default=False, nullable=False)
    enviado_em = db.Column(db.DateTime, nullable=True)
    referencia_documento = db.Column(db.String(120), nullable=True)
    centro_custo = db.Column(db.String(120), nullable=True)

    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=True)
    quantidade = db.Column(db.Float, nullable=True)

    criado_por_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    produto = db.relationship('Produto', backref=db.backref('lancamentos_financeiros', lazy=True))
    criado_por = db.relationship('Funcionario', backref=db.backref('lancamentos_financeiros', lazy=True))

    def __repr__(self):
        return f'<LancamentoFinanceiro {self.tipo} {self.valor}>'


class FundoSolicitacao(db.Model):
    __tablename__ = 'fundos_solicitacoes'

    TIPO_APORTE = 'aporte'
    TIPO_SAQUE = 'saque'
    TIPOS_VALIDOS = [TIPO_APORTE, TIPO_SAQUE]

    STATUS_SOLICITADA = 'solicitada'
    STATUS_APROVADA = 'aprovada'
    STATUS_REJEITADA = 'rejeitada'
    STATUS_LIBERADA = 'liberada'
    STATUS_CANCELADA = 'cancelada'
    STATUS_VALIDOS = [STATUS_SOLICITADA, STATUS_APROVADA, STATUS_REJEITADA, STATUS_LIBERADA, STATUS_CANCELADA]

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20), nullable=False, default=TIPO_APORTE)
    categoria = db.Column(db.String(80), nullable=True)
    descricao = db.Column(db.String(255), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    centro_custo = db.Column(db.String(120), nullable=True)
    referencia_documento = db.Column(db.String(120), nullable=True)
    status = db.Column(db.String(20), nullable=False, default=STATUS_SOLICITADA, index=True)
    motivo_rejeicao = db.Column(db.String(255), nullable=True)
    solicitado_por_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=True, index=True)
    aprovado_por_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=True)
    liberado_por_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=True)
    lancamento_financeiro_id = db.Column(db.Integer, db.ForeignKey('lancamentos_financeiros.id'), nullable=True)
    solicitado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    aprovado_em = db.Column(db.DateTime, nullable=True)
    liberado_em = db.Column(db.DateTime, nullable=True)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    solicitado_por = db.relationship('Funcionario', foreign_keys=[solicitado_por_id], backref=db.backref('fundos_solicitados', lazy=True))
    aprovado_por = db.relationship('Funcionario', foreign_keys=[aprovado_por_id], backref=db.backref('fundos_aprovados', lazy=True))
    liberado_por = db.relationship('Funcionario', foreign_keys=[liberado_por_id], backref=db.backref('fundos_liberados', lazy=True))
    lancamento_financeiro = db.relationship('LancamentoFinanceiro', backref=db.backref('fundo_origem', uselist=False))

    def __repr__(self):
        return f'<FundoSolicitacao {self.id} {self.tipo} {self.status}>'


class EmpresaConfig(db.Model):
    __tablename__ = 'empresa_config'

    TIPO_NEGOCIO_CONVENIENCIA = 'conveniencia'
    TIPO_NEGOCIO_SUPERMERCADO = 'supermercado'
    TIPO_NEGOCIO_FARMACIA = 'farmacia'
    TIPO_NEGOCIO_MODA = 'moda'
    TIPO_NEGOCIO_HOME_CENTER = 'home_center'
    TIPO_NEGOCIO_OUTRO = 'outro'
    TIPOS_NEGOCIO_VALIDOS = {
        TIPO_NEGOCIO_CONVENIENCIA,
        TIPO_NEGOCIO_SUPERMERCADO,
        TIPO_NEGOCIO_FARMACIA,
        TIPO_NEGOCIO_MODA,
        TIPO_NEGOCIO_HOME_CENTER,
        TIPO_NEGOCIO_OUTRO,
    }

    CANAL_OPERACAO_FISICO = 'fisico'
    CANAL_OPERACAO_ECOMMERCE = 'ecommerce'
    CANAL_OPERACAO_HIBRIDO = 'hibrido'
    CANAIS_OPERACAO_VALIDOS = {
        CANAL_OPERACAO_FISICO,
        CANAL_OPERACAO_ECOMMERCE,
        CANAL_OPERACAO_HIBRIDO,
    }

    id = db.Column(db.Integer, primary_key=True)
    razao_social = db.Column(db.String(150))
    nome_fantasia = db.Column(db.String(150))
    codigo_empresa = db.Column(db.String(20))
    cnpj = db.Column(db.String(20))
    inscricao_estadual = db.Column(db.String(30))
    telefone = db.Column(db.String(30))
    email = db.Column(db.String(120))
    endereco = db.Column(db.String(200))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(2))
    cep = db.Column(db.String(12))
    logo_path = db.Column(db.String(255))
    favicon_path = db.Column(db.String(255), nullable=True)
    app_icon_path = db.Column(db.String(255), nullable=True)
    mensagem_comprovante = db.Column(db.String(255))
    cardapio_titulo = db.Column(db.String(120))
    cardapio_subtitulo = db.Column(db.String(255))
    cardapio_mensagem = db.Column(db.String(255))
    cardapio_mostrar_imagem = db.Column(db.Boolean, default=True)
    cardapio_mostrar_descricao = db.Column(db.Boolean, default=True)
    cardapio_qtd_maxima = db.Column(db.Integer, default=20)
    tipo_negocio = db.Column(db.String(30), default=TIPO_NEGOCIO_CONVENIENCIA)
    canal_operacao = db.Column(db.String(30), default=CANAL_OPERACAO_HIBRIDO)
    ecommerce_ativo = db.Column(db.Boolean, default=True)
    ecom_cor_primaria = db.Column(db.String(20), default='#ff7848')
    ecom_cor_secundaria = db.Column(db.String(20), default='#ff5a2a')
    ecom_titulo_banner = db.Column(db.String(140), nullable=True)
    ecom_subtitulo_banner = db.Column(db.String(255), nullable=True)
    ecom_texto_promocao = db.Column(db.String(255), nullable=True)
    ecom_banner_path = db.Column(db.String(255), nullable=True)
    ecom_favicon_path = db.Column(db.String(255), nullable=True)
    ecom_produto_placeholder_path = db.Column(db.String(255), nullable=True)
    ecom_banners_json = db.Column(db.Text, nullable=True)
    ecom_campanhas_json = db.Column(db.Text, nullable=True)
    ecom_footer_bg = db.Column(db.String(20), default='#1f2b38')
    ecom_footer_texto = db.Column(db.String(255), nullable=True)
    ecom_footer_contato = db.Column(db.String(255), nullable=True)
    ecom_footer_creditos = db.Column(db.String(255), nullable=True)
    pagamentos_pdv_json = db.Column(db.Text, nullable=True)
    pagamentos_ecommerce_json = db.Column(db.Text, nullable=True)
    integracoes_pdv_json = db.Column(db.Text, nullable=True)
    integracoes_ecommerce_json = db.Column(db.Text, nullable=True)
    atendimento_mesas_ativo = db.Column(db.Boolean, default=True)
    reposicao_loja_fisica_ativa = db.Column(db.Boolean, default=True)
    emissao_etiqueta_loja_ativa = db.Column(db.Boolean, default=True)
    emissao_etiqueta_endereco_ativa = db.Column(db.Boolean, default=True)
    separacao_entrega_ativa = db.Column(db.Boolean, default=True)
    emissao_etiqueta_entrega_ativa = db.Column(db.Boolean, default=True)
    separacao_entrega_unir_vendas_off = db.Column(db.Boolean, default=False)
    roteirizacao_entrega_ativa = db.Column(db.Boolean, default=True)
    emissao_nota_entrega_ativa = db.Column(db.Boolean, default=True)
    entrega_local_saida_padrao = db.Column(db.String(160), nullable=True)
    entrega_veiculo_padrao = db.Column(db.String(80), nullable=True)
    entrega_motorista_padrao = db.Column(db.String(120), nullable=True)
    entrega_horario_fechamento_roteirizacao = db.Column(db.String(5), nullable=True)
    entrega_veiculos_json = db.Column(db.Text, nullable=True)
    entrega_terceirizadas_json = db.Column(db.Text, nullable=True)
    entrega_regras_roteirizacao_json = db.Column(db.Text, nullable=True)
    servicos_tecnicos_ativos = db.Column(db.Boolean, default=False)
    servico_montagem_instalacao_ativo = db.Column(db.Boolean, default=False)
    distribuicao_ativa = db.Column(db.Boolean, default=True)
    modo_distribuicao_pedidos = db.Column(db.String(30), default='round_robin')
    ultimo_garcom_id = db.Column(db.Integer, db.ForeignKey('garcons.id'), nullable=True)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<EmpresaConfig {self.nome_fantasia or self.razao_social or self.id}>'


class AuditoriaEvento(db.Model):
    __tablename__ = 'auditoria_eventos'

    id = db.Column(db.Integer, primary_key=True)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=True)
    funcionario_nome = db.Column(db.String(120))
    funcionario_email = db.Column(db.String(120))
    funcionario_role = db.Column(db.String(20))
    metodo = db.Column(db.String(10), nullable=False)
    endpoint = db.Column(db.String(120))
    rota = db.Column(db.String(255))
    acao = db.Column(db.String(120), nullable=False)
    entidade = db.Column(db.String(80))
    detalhes = db.Column(db.Text)
    status_code = db.Column(db.Integer)
    ip = db.Column(db.String(64))
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    funcionario = db.relationship('Funcionario', backref=db.backref('eventos_auditoria', lazy=True))

    def __repr__(self):
        return f'<AuditoriaEvento {self.metodo} {self.rota} ({self.status_code})>'


class AssistenteLocalFeedback(db.Model):
    __tablename__ = 'assistente_local_feedback'
    __table_args__ = (
        db.UniqueConstraint('funcionario_id', 'response_id', name='uq_assistente_feedback_funcionario_response'),
    )

    VOTO_LIKE = 'like'
    VOTO_DISLIKE = 'dislike'
    VOTOS_VALIDOS = [VOTO_LIKE, VOTO_DISLIKE]

    id = db.Column(db.Integer, primary_key=True)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=False, index=True)
    response_id = db.Column(db.String(64), nullable=False, index=True)
    vote = db.Column(db.String(10), nullable=False, index=True)
    question = db.Column(db.Text, nullable=True)
    answer = db.Column(db.Text, nullable=True)
    reason = db.Column(db.String(255), nullable=True)
    endpoint_atual = db.Column(db.String(120), nullable=True)
    pagina_atual = db.Column(db.String(80), nullable=True, index=True)
    tela_atual = db.Column(db.String(120), nullable=True)
    matched_doc_ids_json = db.Column(db.Text, nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    funcionario = db.relationship('Funcionario', backref=db.backref('feedbacks_assistente_local', lazy=True))

    def __repr__(self):
        return f'<AssistenteLocalFeedback funcionario={self.funcionario_id} vote={self.vote}>'


class OrdemServico(db.Model):
    __tablename__ = 'ordens_servico'

    TIPO_ORDEM_SERVICO = 'ordem_servico'
    TIPO_AVARIA = 'avaria'
    TIPO_INSPECAO = 'inspecao'
    TIPOS_VALIDOS = [TIPO_ORDEM_SERVICO, TIPO_AVARIA, TIPO_INSPECAO]

    SERVICO_MONTAGEM = 'montagem'
    SERVICO_INSTALACAO = 'instalacao'
    SERVICO_NENHUM = 'nenhum'
    SERVICOS_VALIDOS = [SERVICO_NENHUM, SERVICO_MONTAGEM, SERVICO_INSTALACAO]

    STATUS_ABERTA = 'aberta'
    STATUS_ENVIADA = 'enviada'
    STATUS_EM_EXECUCAO = 'em_execucao'
    STATUS_CONCLUIDA = 'concluida'
    STATUS_CANCELADA = 'cancelada'
    STATUS_VALIDOS = [STATUS_ABERTA, STATUS_ENVIADA, STATUS_EM_EXECUCAO, STATUS_CONCLUIDA, STATUS_CANCELADA]

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(160), nullable=False)
    tipo = db.Column(db.String(30), nullable=False, default=TIPO_ORDEM_SERVICO, index=True)
    servico_tipo = db.Column(db.String(20), nullable=False, default=SERVICO_NENHUM)
    prioridade = db.Column(db.String(20), nullable=True)
    status = db.Column(db.String(30), nullable=False, default=STATUS_ABERTA, index=True)
    descricao = db.Column(db.Text, nullable=True)
    observacoes = db.Column(db.Text, nullable=True)
    avaria_detalhes = db.Column(db.Text, nullable=True)
    inspecao_detalhes = db.Column(db.Text, nullable=True)
    resultado_inspecao = db.Column(db.String(120), nullable=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=True, index=True)
    funcionario_destino_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=True, index=True)
    criado_por_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=True)
    data_agendada = db.Column(db.Date, nullable=True)
    enviada_em = db.Column(db.DateTime, nullable=True)
    iniciado_em = db.Column(db.DateTime, nullable=True)
    concluida_em = db.Column(db.DateTime, nullable=True)
    retorno_tecnico = db.Column(db.Text, nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    produto = db.relationship('Produto', backref=db.backref('ordens_servico', lazy=True))
    pedido = db.relationship('Pedido', backref=db.backref('ordens_servico', lazy=True))
    funcionario_destino = db.relationship('Funcionario', foreign_keys=[funcionario_destino_id], backref=db.backref('ordens_recebidas', lazy=True))
    criado_por = db.relationship('Funcionario', foreign_keys=[criado_por_id], backref=db.backref('ordens_criadas', lazy=True))

    def __repr__(self):
        return f'<OrdemServico #{self.id} {self.tipo} {self.status}>'


class ChamadoInterno(db.Model):
    __tablename__ = 'chamados_internos'

    CATEGORIA_SISTEMA = 'sistema'
    CATEGORIA_ESTOQUE = 'estoque'
    CATEGORIA_FINANCEIRO = 'financeiro'
    CATEGORIA_VENDAS = 'vendas'
    CATEGORIA_RH = 'rh'
    CATEGORIA_EXPEDICAO = 'expedicao'
    CATEGORIA_INFRA = 'infraestrutura'
    CATEGORIAS_VALIDAS = [
        CATEGORIA_SISTEMA,
        CATEGORIA_ESTOQUE,
        CATEGORIA_FINANCEIRO,
        CATEGORIA_VENDAS,
        CATEGORIA_RH,
        CATEGORIA_EXPEDICAO,
        CATEGORIA_INFRA,
    ]

    PRIORIDADES_VALIDAS = ['baixa', 'media', 'alta', 'critica']
    STATUS_ABERTO = 'aberto'
    STATUS_TRIAGEM = 'triagem'
    STATUS_EM_ANDAMENTO = 'em_andamento'
    STATUS_AGUARDANDO = 'aguardando'
    STATUS_CONCLUIDO = 'concluido'
    STATUS_CANCELADO = 'cancelado'
    STATUS_VALIDOS = [
        STATUS_ABERTO,
        STATUS_TRIAGEM,
        STATUS_EM_ANDAMENTO,
        STATUS_AGUARDANDO,
        STATUS_CONCLUIDO,
        STATUS_CANCELADO,
    ]

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(160), nullable=False, index=True)
    categoria = db.Column(db.String(40), nullable=False, default=CATEGORIA_SISTEMA, index=True)
    prioridade = db.Column(db.String(20), nullable=False, default='media', index=True)
    status = db.Column(db.String(30), nullable=False, default=STATUS_ABERTO, index=True)
    setor_origem = db.Column(db.String(80), nullable=True)
    descricao = db.Column(db.Text, nullable=False)
    resolucao = db.Column(db.Text, nullable=True)
    solicitante_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=False, index=True)
    responsavel_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=True, index=True)
    aberto_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    concluido_em = db.Column(db.DateTime, nullable=True)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    solicitante = db.relationship('Funcionario', foreign_keys=[solicitante_id], backref=db.backref('chamados_abertos', lazy=True))
    responsavel = db.relationship('Funcionario', foreign_keys=[responsavel_id], backref=db.backref('chamados_responsaveis', lazy=True))

    def __repr__(self):
        return f'<ChamadoInterno #{self.id} {self.status}>'



```


### Arquivo: `realtime.py`
- Linhas: 30
- Tamanho: 0.7 KB
- Status: completo

```python
import json
import queue
import time

# Fila simples para despachar alertas de pedidos novos via SSE
alert_queue = queue.Queue()


def publish_alert(data: dict):
    """Publica um alerta na fila."""
    try:
        alert_queue.put_nowait(data)
    except queue.Full:
        # Em caso de fila cheia, descartamos para não travar o fluxo
        pass


def sse_stream():
    """Generator de eventos SSE."""
    while True:
        try:
            payload = alert_queue.get(timeout=30)
        except queue.Empty:
            # envia ping para manter conexão viva
            yield "event: ping\ndata: {}\n\n"
            continue

        yield f"event: pedido\ndata: {json.dumps(payload, default=str)}\n\n"
        time.sleep(0.01)

```


### Arquivo: `routes/__init__.py`
- Linhas: 2
- Tamanho: 0.0 KB
- Status: completo

```python
# Package de rotas por domínio.

```


### Arquivo: `routes/estoque_routes.py`
- Linhas: 3529
- Tamanho: 173.1 KB
- Status: completo

```python
﻿from datetime import datetime, timedelta
import os
import re
import unicodedata
import uuid

from sqlalchemy.orm import load_only, selectinload
from app import extensions

from flask import render_template, request, redirect, url_for, flash, jsonify, session

from app.exceptions import AppError, ValidationError
from app.utils.helpers import sem_acentos
from app.utils.validators import normalizar_codigo_barras
from models import (
    AlmoxarifadoAtribuicao,
    db,
    Categoria,
    EnderecoEstoque,
    Estoque,
    Produto,
    Movimentacao,
    Fornecedor,
    RecebimentoFornecedor,
    RecebimentoItem,
    EmpresaConfig,
    Funcionario,
    Pedido,
    ItemPedido,
    EquipamentoMovimentacao,
    ManutencaoEquipamento,
)
from utils.endereco_codigo import (
    CONTROLE_VALIDADE_VALIDOS,
    RESTRICOES_VALIDAS,
    SETORES_ZONA_VALIDOS,
    STATUS_ENDERECO_VALIDOS,
    TEMPERATURA_VALIDOS,
    TIPOS_AREA_VALIDOS,
    gerar_codigo_localizacao_supermercado,
    validar_endereco_supermercado_payload,
)

# pillow serÃ¡ usado para redimensionar/comprimir imagens
from PIL import Image

ALLOWED_IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp', '.gif'}
DEFAULT_PRODUCT_IMAGE = 'img/placeholders/imgindisponivel.png'


def register_estoque_routes(app, login_required, require_role, aplicar_movimentacao_estoque, sincronizar_matriculas_funcionarios=None):
    estoque_write_roles = ('admin', 'gerente', 'caixa', 'operador')
    endereco_context = {
        'setores_zona_validos': SETORES_ZONA_VALIDOS,
        'tipos_area_validos': TIPOS_AREA_VALIDOS,
        'status_endereco_validos': STATUS_ENDERECO_VALIDOS,
        'controle_validade_validos': CONTROLE_VALIDADE_VALIDOS,
        'temperatura_validos': TEMPERATURA_VALIDOS,
        'restricoes_validas': RESTRICOES_VALIDAS,
    }
    STATUS_DISPONIBILIDADE_LABELS = {
        Produto.STATUS_DISPONIVEL_ONLINE: 'Online',
        Produto.STATUS_DISPONIVEL_OFF: 'Off',
    }
    TIPOS_MOVIMENTACAO_PRODUTO = {
        'manual': 'Manual',
        'carrinho': 'Carrinho',
        'paleteira': 'Paleteira',
        'empilhadeira': 'Empilhadeira',
    }
    recebimento_status_labels = {
        RecebimentoFornecedor.STATUS_CRIADO: 'Criado',
        RecebimentoFornecedor.STATUS_AGUARDANDO_ARMAZENAGEM: 'Aguardando armazenagem',
        RecebimentoFornecedor.STATUS_CONCLUIDO: 'Concluido',
        RecebimentoFornecedor.STATUS_CANCELADO: 'Cancelado',
    }
    recebimento_tipo_labels = {
        RecebimentoFornecedor.TIPO_COMPRA_REVENDA: 'Compra para revenda',
        RecebimentoFornecedor.TIPO_USO_CONSUMO: 'Uso e consumo operacional',
        RecebimentoFornecedor.TIPO_BONIFICACAO: 'Bonificacao do fornecedor',
        RecebimentoFornecedor.TIPO_CONSIGNADO: 'Consignado',
        RecebimentoFornecedor.TIPO_RETORNO_INDUSTRIALIZACAO: 'Retorno de industrializacao',
    }
    recebimento_tipos_fornecedor_opcional = {
        RecebimentoFornecedor.TIPO_USO_CONSUMO,
    }
    almoxarifado_destino_labels = {
        AlmoxarifadoAtribuicao.DESTINO_FUNCIONARIO: 'Funcionario',
        AlmoxarifadoAtribuicao.DESTINO_SETOR: 'Setor',
    }
    motivos_movimentacao_interna = [
        'ajuste_inventario',
        'acerto_estoque',
        'consumo_operacional',
        'perda_validade',
        'avaria_quebra',
        'devolucao_cliente',
        'demonstracao_deguste',
        'uso_interno',
    ]
    motivos_transferencia = [
        'reposicao_loja',
        'abastecimento_filial',
        'transferencia_centro_distribuicao',
        'remanejamento_operacional',
    ]
    fornecedor_padrao_recebimento_nome = 'Origem interna / fornecedor nao informado'

    def _normalizar_status_disponibilidade(valor):
        return Produto.normalizar_status_disponibilidade(valor)

    def _normalizar_tipo_movimentacao(valor):
        tipo = (valor or 'manual').strip().lower()
        if tipo not in TIPOS_MOVIMENTACAO_PRODUTO:
            return 'manual'
        return tipo

    def _obter_empresa_config_estoque():
        empresa = EmpresaConfig.query.first()
        if not empresa:
            empresa = EmpresaConfig()
            db.session.add(empresa)
            db.session.commit()
        return empresa

    def _reposicao_loja_fisica_ativa(empresa=None):
        empresa = empresa or _obter_empresa_config_estoque()
        return empresa.reposicao_loja_fisica_ativa is not False

    def _emissao_etiqueta_loja_ativa(empresa=None):
        empresa = empresa or _obter_empresa_config_estoque()
        return empresa.emissao_etiqueta_loja_ativa is not False

    def _emissao_etiqueta_endereco_ativa(empresa=None):
        empresa = empresa or _obter_empresa_config_estoque()
        return empresa.emissao_etiqueta_endereco_ativa is not False

    def _normalizar_codigo_barras(valor):
        return normalizar_codigo_barras(valor)

    def _sem_acentos(texto):
        return sem_acentos(texto)

    def _categoria_parece_quimico(produto):
        categoria_nome = ''
        if getattr(produto, 'categoria', None):
            categoria_nome = produto.categoria.nome or ''
        texto = _sem_acentos(categoria_nome).strip().lower()
        return bool(texto and re.search(r'quim', texto))

    def _parse_data_filtro(valor):
        texto = (valor or '').strip()
        if not texto:
            return None
        try:
            return datetime.strptime(texto, '%Y-%m-%d')
        except ValueError:
            return None

    def _tipo_recebimento_exige_fornecedor(tipo_recebimento):
        tipo_normalizado = (tipo_recebimento or '').strip().lower()
        return (
            tipo_normalizado in RecebimentoFornecedor.TIPOS_VALIDOS
            and tipo_normalizado not in recebimento_tipos_fornecedor_opcional
        )

    def _obter_fornecedor_padrao_recebimento():
        fornecedor = Fornecedor.query.filter(
            db.func.lower(Fornecedor.nome) == fornecedor_padrao_recebimento_nome.lower()
        ).first()
        if fornecedor:
            return fornecedor
        fornecedor = Fornecedor(
            nome=fornecedor_padrao_recebimento_nome,
            contato='Cadastro automatico',
            observacoes_gerais='Usado quando o tipo de recebimento nao exige fornecedor informado.',
            tipo_produtos_fornece='Origem interna e consumo operacional',
            ativo=True,
        )
        db.session.add(fornecedor)
        db.session.flush()
        return fornecedor

    def _resolver_funcionario_por_matricula_ou_nome(texto_busca='', funcionario_id=None):
        if funcionario_id:
            funcionario = Funcionario.query.filter_by(id=funcionario_id, ativo=True).first()
            if funcionario:
                return funcionario

        texto = (texto_busca or '').strip()
        if not texto:
            return None

        matricula = texto.upper()
        funcionario = Funcionario.query.filter(
            Funcionario.ativo.is_(True),
            db.func.lower(Funcionario.matricula) == matricula.lower(),
        ).first()
        if funcionario:
            return funcionario

        return Funcionario.query.filter(
            Funcionario.ativo.is_(True),
            db.func.lower(Funcionario.nome) == texto.lower(),
        ).order_by(Funcionario.nome.asc()).first()

    def _listar_setores_almoxarifado():
        departamentos = {
            (nome or '').strip()
            for nome, in db.session.query(Funcionario.departamento).filter(Funcionario.departamento.isnot(None)).all()
            if (nome or '').strip()
        }
        times = {
            (nome or '').strip()
            for nome, in db.session.query(Funcionario.time_nome).filter(Funcionario.time_nome.isnot(None)).all()
            if (nome or '').strip()
        }
        return sorted(departamentos.union(times))

    def _aplicar_filtros_produtos(
        query,
        *,
        categoria_id=None,
        busca='',
        status_disponibilidade='',
        estoque_id=None,
        endereco_id=None,
        fornecedor_id=None,
        fora_picking='',
        status_ativo='',
        ruptura='',
    ):
        if categoria_id:
            query = query.filter(Produto.categoria_id == categoria_id)
        if busca:
            termo = f'%{busca}%'
            query = query.filter(
                db.or_(
                    Produto.nome.ilike(termo),
                    Produto.codigo.ilike(termo),
                    Produto.descricao.ilike(termo),
                )
            )
        ativo = (status_ativo or '').strip().lower()
        if ativo == 'ativos':
            query = query.filter(Produto.ativo.is_(True))
        elif ativo == 'inativos':
            query = query.filter(Produto.ativo.is_(False))
        status = (status_disponibilidade or '').strip().lower()
        if status in Produto.STATUS_DISPONIBILIDADE_ONLINE_EQUIVALENTES:
            query = query.filter(Produto.status_disponibilidade.in_(Produto.STATUS_DISPONIBILIDADE_ONLINE_EQUIVALENTES))
        elif status in Produto.STATUS_DISPONIBILIDADE_OFF_EQUIVALENTES:
            query = query.filter(Produto.status_disponibilidade.in_(Produto.STATUS_DISPONIBILIDADE_OFF_EQUIVALENTES))
        if endereco_id:
            query = query.filter(Produto.endereco_id == endereco_id)
        if fornecedor_id:
            query = query.filter(Produto.fornecedor_id == fornecedor_id)
        fora = (fora_picking or '').strip().lower()
        if fora == 'sim':
            query = query.filter(Produto.fora_picking.is_(True))
        elif fora == 'nao':
            query = query.filter(db.or_(Produto.fora_picking.is_(False), Produto.fora_picking.is_(None)))
        ruptura = (ruptura or '').strip().lower()
        if ruptura == 'sim':
            query = query.filter(Produto.quantidade_estoque < Produto.quantidade_minima)
        elif ruptura == 'nao':
            query = query.filter(Produto.quantidade_estoque >= Produto.quantidade_minima)
        if estoque_id:
            query = query.join(EnderecoEstoque, Produto.endereco_id == EnderecoEstoque.id).filter(
                EnderecoEstoque.estoque_id == estoque_id
            )
        return query

    def _funcionario_logado_estoque():
        funcionario_id = session.get('funcionario_id')
        if not funcionario_id:
            return None
        return Funcionario.query.get(funcionario_id)

    def _estoques_permitidos_ids_base(funcionario=None):
        funcionario = funcionario or _funcionario_logado_estoque()
        if not funcionario or funcionario.role == 'admin' or not getattr(funcionario, 'restricao_estoques_ativa', False):
            return None
        ids = set()
        if getattr(funcionario, 'estoque_principal_id', None):
            ids.add(funcionario.estoque_principal_id)
        for estoque in getattr(funcionario, 'estoques_permitidos', []) or []:
            if getattr(estoque, 'id', None):
                ids.add(estoque.id)
        return ids

    def _estoque_contexto_selecionado_id(funcionario=None):
        funcionario = funcionario or _funcionario_logado_estoque()
        valor = session.get('estoque_contexto_id')
        if valor in (None, '', 'all'):
            return None
        try:
            estoque_id = int(valor)
        except (TypeError, ValueError):
            session.pop('estoque_contexto_id', None)
            return None

        ids_base = _estoques_permitidos_ids_base(funcionario)
        query = Estoque.query.filter(Estoque.id == estoque_id, Estoque.ativo.is_(True))
        if ids_base is not None:
            if estoque_id not in ids_base:
                session.pop('estoque_contexto_id', None)
                return None
            query = query.filter(Estoque.id.in_(ids_base))
        if not query.with_entities(Estoque.id).first():
            session.pop('estoque_contexto_id', None)
            return None
        return estoque_id

    def _estoques_permitidos_ids(funcionario=None):
        funcionario = funcionario or _funcionario_logado_estoque()
        ids_base = _estoques_permitidos_ids_base(funcionario)
        estoque_contexto_id = _estoque_contexto_selecionado_id(funcionario)
        if estoque_contexto_id:
            return {estoque_contexto_id}
        return ids_base

    def _estoque_query_permitida(funcionario=None):
        query = Estoque.query
        ids = _estoques_permitidos_ids(funcionario)
        if ids is None:
            return query
        if not ids:
            return query.filter(Estoque.id == -1)
        return query.filter(Estoque.id.in_(ids))

    def _endereco_query_permitida(funcionario=None):
        query = EnderecoEstoque.query
        ids = _estoques_permitidos_ids(funcionario)
        if ids is None:
            return query
        if not ids:
            return query.filter(EnderecoEstoque.id == -1)
        return query.filter(EnderecoEstoque.estoque_id.in_(ids))

    def _produto_query_permitida(query, funcionario=None):
        ids = _estoques_permitidos_ids(funcionario)
        if ids is None:
            return query
        if not ids:
            return query.filter(Produto.endereco_id.is_(None))
        return query.filter(
            db.or_(
                Produto.endereco_id.is_(None),
                Produto.endereco.has(EnderecoEstoque.estoque_id.in_(ids)),
            )
        )

    def _movimentacao_query_permitida(query, funcionario=None):
        ids = _estoques_permitidos_ids(funcionario)
        if ids is None:
            return query
        if not ids:
            return query.filter(Movimentacao.id == -1)
        return query.filter(
            Movimentacao.produto.has(
                db.or_(
                    Produto.endereco_id.is_(None),
                    Produto.endereco.has(EnderecoEstoque.estoque_id.in_(ids)),
                )
            )
        )

    def _carregar_estoque_permitido(estoque_id, funcionario=None, *, apenas_ativo=False):
        if not estoque_id:
            return None
        query = _estoque_query_permitida(funcionario)
        if apenas_ativo:
            query = query.filter(Estoque.ativo.is_(True))
        return query.filter(Estoque.id == estoque_id).first()

    def _carregar_endereco_permitido(endereco_id, funcionario=None, *, apenas_ativo=False):
        if not endereco_id:
            return None
        query = _endereco_query_permitida(funcionario)
        if apenas_ativo:
            query = query.filter(EnderecoEstoque.ativo.is_(True))
        return query.filter(EnderecoEstoque.id == endereco_id).first()

    def _produto_em_estoque_permitido(produto, funcionario=None):
        ids = _estoques_permitidos_ids(funcionario)
        if ids is None or not produto:
            return True
        if not getattr(produto, 'endereco_id', None):
            return True
        endereco = getattr(produto, 'endereco', None) or EnderecoEstoque.query.get(produto.endereco_id)
        return bool(endereco and endereco.estoque_id in ids)
    def _is_allowed_image(filename):
        _, ext = os.path.splitext(filename.lower())
        return ext in ALLOWED_IMAGE_EXTENSIONS

    def _is_valid_image_content(file_storage):
        if not file_storage:
            return False
        stream = getattr(file_storage, 'stream', None)
        if stream is None:
            return False
        try:
            stream.seek(0)
            img = Image.open(stream)
            img.verify()
            stream.seek(0)
            return True
        except Exception:
            try:
                stream.seek(0)
            except Exception:
                pass
            return False

    def _optimize_image_file(absolute_path):
        try:
            img = Image.open(absolute_path)
            max_size = (800, 800)
            resample = getattr(Image, 'Resampling', Image).LANCZOS
            img.thumbnail(max_size, resample)
            save_kwargs = {'optimize': True}
            if img.format and img.format.lower() in ['jpeg', 'jpg']:
                save_kwargs['quality'] = 85
            img.save(absolute_path, **save_kwargs)
        except Exception:
            pass

    def _delete_image_file(relative_path):
        if not relative_path:
            return
        caminho_rel = str(relative_path).replace('\\', '/')
        if caminho_rel == DEFAULT_PRODUCT_IMAGE:
            return
        caminho_padrao_config = None
        try:
            empresa_cfg = EmpresaConfig.query.first()
            caminho_padrao_config = (empresa_cfg.ecom_produto_placeholder_path or '').strip().replace('\\', '/') if empresa_cfg else ''
        except Exception:
            caminho_padrao_config = None
        if caminho_padrao_config and caminho_rel == caminho_padrao_config:
            return

        image_path = os.path.normpath(os.path.join(app.static_folder, relative_path))
        static_root = os.path.normpath(app.static_folder)
        if os.path.commonpath([image_path, static_root]) != static_root:
            return

        if os.path.exists(image_path):
            os.remove(image_path)

    def _save_product_image(file_storage, product_name):
        if not file_storage or not file_storage.filename:
            return None, None
        if not _is_allowed_image(file_storage.filename):
            return None, 'Formato de imagem invalido. Use PNG, JPG, JPEG, WEBP ou GIF.'
        if not _is_valid_image_content(file_storage):
            return None, 'Arquivo enviado nao corresponde a uma imagem valida.'

        _, ext = os.path.splitext(file_storage.filename.lower())
        image_name = f'{uuid.uuid4().hex}{ext}'
        relative_dir = os.path.join('uploads', 'produtos')
        absolute_dir = os.path.join(app.static_folder, relative_dir)
        os.makedirs(absolute_dir, exist_ok=True)
        relative_path = os.path.join(relative_dir, image_name).replace('\\', '/')
        absolute_path = os.path.join(app.static_folder, relative_path)

        file_storage.save(absolute_path)
        _optimize_image_file(absolute_path)
        return relative_path, None

    def _imagem_padrao_produto():
        try:
            empresa_cfg = EmpresaConfig.query.first()
            caminho_cfg = (empresa_cfg.ecom_produto_placeholder_path or '').strip().replace('\\', '/') if empresa_cfg else ''
            if caminho_cfg:
                return caminho_cfg
        except Exception:
            pass
        return DEFAULT_PRODUCT_IMAGE

    def _normalizar_imagem_produto(path):
        texto = (path or '').strip().replace('\\', '/')
        return texto or _imagem_padrao_produto()

    def _preencher_imagem_padrao_produtos():
        try:
            atualizados = Produto.query.filter(
                db.or_(Produto.imagem_path.is_(None), Produto.imagem_path == '')
            ).update(
                {Produto.imagem_path: _imagem_padrao_produto()},
                synchronize_session=False
            )
            if atualizados:
                db.session.commit()
        except Exception:
            db.session.rollback()

    def _save_category_image(file_storage, category_name):
        if not file_storage or not file_storage.filename:
            return None, None
        if not _is_allowed_image(file_storage.filename):
            return None, 'Formato de imagem invalido. Use PNG, JPG, JPEG, WEBP ou GIF.'
        if not _is_valid_image_content(file_storage):
            return None, 'Arquivo enviado nao corresponde a uma imagem valida.'

        _, ext = os.path.splitext(file_storage.filename.lower())
        image_name = f'{uuid.uuid4().hex}{ext}'
        relative_dir = os.path.join('uploads', 'categorias')
        absolute_dir = os.path.join(app.static_folder, relative_dir)
        os.makedirs(absolute_dir, exist_ok=True)
        relative_path = os.path.join(relative_dir, image_name).replace('\\', '/')
        absolute_path = os.path.join(app.static_folder, relative_path)

        file_storage.save(absolute_path)
        _optimize_image_file(absolute_path)
        return relative_path, None

    with app.app_context():
        _preencher_imagem_padrao_produtos()

    @app.route('/produtos')
    @login_required
    def listar_produtos():
        funcionario_logado = _funcionario_logado_estoque()
        page = max(request.args.get('page', 1, type=int), 1)
        per_page = min(max(request.args.get('per_page', 25, type=int), 1), 100)
        categoria_id = request.args.get('categoria_id', type=int)
        busca = (request.args.get('busca') or '').strip()
        status_disponibilidade = (request.args.get('status_disponibilidade') or '').strip().lower()
        estoque_id = request.args.get('estoque_id', type=int)
        endereco_id = request.args.get('endereco_id', type=int)
        fornecedor_id = request.args.get('fornecedor_id', type=int)
        fora_picking = (request.args.get('fora_picking') or '').strip().lower()
        status_ativo = (request.args.get('status_ativo') or '').strip().lower()
        ruptura = (request.args.get('ruptura') or '').strip().lower()
        ordenar = (request.args.get('ordenar') or 'nome_asc').strip().lower()

        ordenacoes_produto = {
            'nome_asc': (Produto.nome.asc(), Produto.id.asc()),
            'nome_desc': (Produto.nome.desc(), Produto.id.desc()),
            'codigo_asc': (Produto.codigo.asc(), Produto.id.asc()),
            'estoque_menor': (Produto.quantidade_estoque.asc(), Produto.nome.asc()),
            'estoque_maior': (Produto.quantidade_estoque.desc(), Produto.nome.asc()),
            'recentes': (Produto.criado_em.desc(), Produto.id.desc()),
            'atualizados': (Produto.atualizado_em.desc(), Produto.id.desc()),
        }
        if ordenar not in ordenacoes_produto:
            ordenar = 'nome_asc'

        if estoque_id and not _carregar_estoque_permitido(estoque_id, funcionario_logado):
            flash('Você não possui acesso ao estoque selecionado.', 'warning')
            return redirect(url_for('listar_produtos'))
        if endereco_id and not _carregar_endereco_permitido(endereco_id, funcionario_logado):
            flash('Você não possui acesso ao endereço selecionado.', 'warning')
            return redirect(url_for('listar_produtos'))

        query = _aplicar_filtros_produtos(
            _produto_query_permitida(Produto.query, funcionario_logado),
            categoria_id=categoria_id,
            busca=busca,
            status_disponibilidade=status_disponibilidade,
            estoque_id=estoque_id,
            endereco_id=endereco_id,
            fornecedor_id=fornecedor_id,
            fora_picking=fora_picking,
            status_ativo=status_ativo,
            ruptura=ruptura,
        ).options(
            load_only(
                Produto.id,
                Produto.codigo,
                Produto.nome,
                Produto.imagem_path,
                Produto.categoria_id,
                Produto.fornecedor_id,
                Produto.endereco_id,
                Produto.preco_venda,
                Produto.quantidade_estoque,
                Produto.quantidade_minima,
                Produto.status_disponibilidade,
                Produto.tipo_movimentacao,
                Produto.fora_picking,
                Produto.ativo,
                Produto.criado_em,
                Produto.atualizado_em,
            ),
            selectinload(Produto.categoria).load_only(Categoria.id, Categoria.nome),
            selectinload(Produto.endereco).load_only(EnderecoEstoque.id, EnderecoEstoque.nome),
            selectinload(Produto.fornecedor).load_only(Fornecedor.id, Fornecedor.nome),
        )

        pagination = query.order_by(*ordenacoes_produto[ordenar]).paginate(page=page, per_page=per_page, error_out=False)
        produtos = pagination.items
        categorias = Categoria.query.order_by(Categoria.nome.asc()).all()
        estoques = _estoque_query_permitida(funcionario_logado).filter_by(ativo=True).order_by(Estoque.nome.asc()).all()
        if estoque_id:
            enderecos = _endereco_query_permitida(funcionario_logado).filter_by(
                ativo=True,
                estoque_id=estoque_id,
            ).order_by(EnderecoEstoque.nome.asc()).all()
        else:
            enderecos = []
        fornecedores = Fornecedor.query.filter(
            Fornecedor.ativo.is_(True),
            db.func.lower(Fornecedor.nome) != fornecedor_padrao_recebimento_nome.lower(),
        ).order_by(Fornecedor.nome.asc()).all()
        filtros_labels = []
        if busca:
            filtros_labels.append(f'Busca: {busca}')
        categoria_obj = next((cat for cat in categorias if cat.id == categoria_id), None)
        if categoria_obj:
            filtros_labels.append(f'Categoria: {categoria_obj.nome}')
        estoque_obj = next((estoque for estoque in estoques if estoque.id == estoque_id), None)
        if estoque_obj:
            filtros_labels.append(f'Estoque: {estoque_obj.nome}')
        endereco_obj = next((endereco for endereco in enderecos if endereco.id == endereco_id), None)
        if endereco_obj:
            filtros_labels.append(f'Endereco: {endereco_obj.nome}')
        fornecedor_obj = next((fornecedor for fornecedor in fornecedores if fornecedor.id == fornecedor_id), None)
        if fornecedor_obj:
            filtros_labels.append(f'Fornecedor: {fornecedor_obj.nome}')
        if status_disponibilidade:
            filtros_labels.append(f'Disponibilidade: {STATUS_DISPONIBILIDADE_LABELS.get(status_disponibilidade, status_disponibilidade)}')
        if status_ativo == 'ativos':
            filtros_labels.append('Somente ativos')
        elif status_ativo == 'inativos':
            filtros_labels.append('Somente inativos')
        if fora_picking == 'sim':
            filtros_labels.append('Fora de picking')
        elif fora_picking == 'nao':
            filtros_labels.append('Em picking')
        if ruptura == 'sim':
            filtros_labels.append('Somente ruptura')
        elif ruptura == 'nao':
            filtros_labels.append('Sem ruptura')

        total_resultados = pagination.total
        inicio_resultados = ((page - 1) * per_page) + 1 if total_resultados else 0
        fim_resultados = inicio_resultados + len(produtos) - 1 if total_resultados else 0
        return render_template(
            'estoque/produtos/produtos.html',
            produtos=produtos,
            pagination=pagination,
            per_page=per_page,
            per_page_options=(25, 50, 100),
            categorias=categorias,
            enderecos=enderecos,
            estoques=estoques,
            fornecedores=fornecedores,
            categoria_selecionada=categoria_id,
            busca=busca,
            filtros_labels=filtros_labels,
            ordenar=ordenar,
            ordenacoes_disponiveis={
                'nome_asc': 'Nome A-Z',
                'nome_desc': 'Nome Z-A',
                'codigo_asc': 'Codigo',
                'estoque_menor': 'Menor estoque',
                'estoque_maior': 'Maior estoque',
                'recentes': 'Mais recentes',
                'atualizados': 'Atualizados por ultimo',
            },
            resumo_lista={
                'total_resultados': total_resultados,
                'inicio_resultados': inicio_resultados,
                'fim_resultados': fim_resultados,
                'pagina_atual': pagination.page,
                'total_paginas': pagination.pages,
                'filtros_ativos': len(filtros_labels),
            },
            filtros={
                'status_disponibilidade': status_disponibilidade,
                'estoque_id': estoque_id,
                'endereco_id': endereco_id,
                'fornecedor_id': fornecedor_id,
                'fora_picking': fora_picking,
                'status_ativo': status_ativo,
                'ruptura': ruptura,
            },
            status_disponibilidade_labels=STATUS_DISPONIBILIDADE_LABELS,
            tipos_movimentacao_produto=TIPOS_MOVIMENTACAO_PRODUTO,
            query_params=request.args.to_dict()
        )

    @app.route('/produtos/etiquetas-loja')
    @login_required
    def imprimir_etiquetas_loja():
        empresa = _obter_empresa_config_estoque()
        if not _emissao_etiqueta_loja_ativa(empresa):
            flash('A emissao de etiquetas de loja esta desativada na configuracao da empresa.', 'warning')
            return redirect(url_for('listar_produtos'))

        funcionario_logado = _funcionario_logado_estoque()
        categoria_id = request.args.get('categoria_id', type=int)
        estoque_id = request.args.get('estoque_id', type=int)
        somente_em_venda = (request.args.get('somente_em_venda') or 'sim').strip().lower()
        busca = (request.args.get('busca') or '').strip()

        if estoque_id and not _carregar_estoque_permitido(estoque_id, funcionario_logado):
            flash('Voce nao possui acesso ao estoque selecionado para etiquetas de loja.', 'warning')
            return redirect(url_for('listar_produtos'))

        query = _produto_query_permitida(
            Produto.query.options(
                selectinload(Produto.categoria),
                selectinload(Produto.endereco),
            ),
            funcionario_logado,
        ).filter(Produto.ativo.is_(True))

        if categoria_id:
            query = query.filter(Produto.categoria_id == categoria_id)
        if estoque_id:
            query = query.filter(Produto.estoque_id == estoque_id)
        if somente_em_venda == 'sim':
            query = query.filter(Produto.quantidade_estoque > 0)
        if busca:
            termo = f'%{busca}%'
            query = query.filter(
                db.or_(
                    Produto.nome.ilike(termo),
                    Produto.codigo.ilike(termo),
                    Produto.descricao.ilike(termo),
                )
            )

        produtos = query.order_by(Produto.nome.asc()).limit(180).all()
        categorias = Categoria.query.order_by(Categoria.nome.asc()).all()
        estoques = _estoque_query_permitida(funcionario_logado).order_by(Estoque.nome.asc()).all()

        return render_template(
            'estoque/produtos/etiquetas_loja.html',
            empresa=empresa,
            produtos=produtos,
            categorias=categorias,
            estoques=estoques,
            filtros={
                'categoria_id': categoria_id,
                'estoque_id': estoque_id,
                'somente_em_venda': somente_em_venda,
                'busca': busca,
            },
        )

    @app.route('/produtos/enderecos/armazenar-todos', methods=['POST'])
    @require_role(*estoque_write_roles)
    def armazenar_todos_produtos_enderecos():
        funcionario_logado = _funcionario_logado_estoque()
        try:
            estoque_id = request.form.get('estoque_id', type=int)
            apenas_sem_endereco = (request.form.get('apenas_sem_endereco') == 'on')
            categoria_id = request.form.get('categoria_id', type=int)
            busca = (request.form.get('busca') or '').strip()
            status_disponibilidade = (request.form.get('status_disponibilidade') or '').strip().lower()
            filtro_estoque_id = request.form.get('filtro_estoque_id', type=int)
            filtro_endereco_id = request.form.get('filtro_endereco_id', type=int)

            if not estoque_id:
                flash('Selecione um estoque para distribuir os produtos.', 'error')
                return redirect(url_for(
                    'listar_produtos',
                    categoria_id=categoria_id or '',
                    busca=busca,
                    status_disponibilidade=status_disponibilidade,
                    estoque_id=filtro_estoque_id or '',
                    endereco_id=filtro_endereco_id or '',
                ))

            estoque = _carregar_estoque_permitido(estoque_id, funcionario_logado)
            if not estoque:
                flash('Estoque informado nao existe ou nao esta liberado para este colaborador.', 'error')
                return redirect(url_for(
                    'listar_produtos',
                    categoria_id=categoria_id or '',
                    busca=busca,
                    status_disponibilidade=status_disponibilidade,
                    estoque_id=filtro_estoque_id or '',
                    endereco_id=filtro_endereco_id or '',
                ))

            if filtro_estoque_id and not _carregar_estoque_permitido(filtro_estoque_id, funcionario_logado):
                flash('Filtro de estoque fora da sua alçada.', 'error')
                return redirect(url_for('listar_produtos'))
            if filtro_endereco_id and not _carregar_endereco_permitido(filtro_endereco_id, funcionario_logado):
                flash('Filtro de endereço fora da sua alçada.', 'error')
                return redirect(url_for('listar_produtos'))

            enderecos = _endereco_query_permitida(funcionario_logado).filter_by(
                estoque_id=estoque.id,
                ativo=True
            ).order_by(EnderecoEstoque.id.asc()).all()
            if not enderecos:
                flash('Este estoque nao possui enderecos ativos para armazenamento.', 'warning')
                return redirect(url_for(
                    'listar_produtos',
                    categoria_id=categoria_id or '',
                    busca=busca,
                    status_disponibilidade=status_disponibilidade,
                    estoque_id=filtro_estoque_id or '',
                    endereco_id=filtro_endereco_id or '',
                ))

            query = _aplicar_filtros_produtos(
                _produto_query_permitida(Produto.query.order_by(Produto.id.asc()), funcionario_logado),
                categoria_id=categoria_id,
                busca=busca,
                status_disponibilidade=status_disponibilidade,
                estoque_id=filtro_estoque_id,
                endereco_id=filtro_endereco_id,
            )
            if apenas_sem_endereco:
                query = query.filter(Produto.endereco_id.is_(None))

            produtos = query.all()
            if not produtos:
                flash('Nenhum produto encontrado para armazenar com os filtros selecionados.', 'warning')
                return redirect(url_for(
                    'listar_produtos',
                    categoria_id=categoria_id or '',
                    busca=busca,
                    status_disponibilidade=status_disponibilidade,
                    estoque_id=filtro_estoque_id or '',
                    endereco_id=filtro_endereco_id or '',
                ))

            total_enderecos = len(enderecos)
            for idx, produto in enumerate(produtos):
                destino = enderecos[idx % total_enderecos]
                produto.endereco_id = destino.id

            db.session.commit()
            msg_regra = 'sem endereco' if apenas_sem_endereco else 'filtrados'
            flash(
                f'{len(produtos)} produto(s) armazenado(s) em {total_enderecos} endereco(s) do estoque "{estoque.nome}" (criterio: {msg_regra}).',
                'success'
            )
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao armazenar produtos nos enderecos: {str(e)}', 'error')

        return redirect(url_for(
            'listar_produtos',
            categoria_id=request.form.get('categoria_id') or '',
            busca=(request.form.get('busca') or '').strip(),
            status_disponibilidade=(request.form.get('status_disponibilidade') or '').strip().lower(),
            estoque_id=request.form.get('filtro_estoque_id') or '',
            endereco_id=request.form.get('filtro_endereco_id') or '',
        ))

    @app.route('/produtos/novo', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def novo_produto():
        funcionario_logado = _funcionario_logado_estoque()
        if request.method == 'POST':
            nova_imagem_path = None
            try:
                categoria_id = request.form.get('categoria_id', type=int)
                fornecedor_id = request.form.get('fornecedor_id', type=int)
                categoria = Categoria.query.get(categoria_id)
                if not categoria:
                    flash('Categoria invalida', 'error')
                    return redirect(url_for('novo_produto'))
                fornecedor = Fornecedor.query.get(fornecedor_id) if fornecedor_id else None
                if not fornecedor:
                    flash('Fornecedor invalido. Selecione um fornecedor para o produto.', 'error')
                    return redirect(url_for('novo_produto'))

                endereco_id = request.form.get('endereco_id', type=int) or None
                if endereco_id and not _carregar_endereco_permitido(endereco_id, funcionario_logado, apenas_ativo=True):
                    flash('Endereco invalido ou fora dos estoques permitidos.', 'error')
                    return redirect(url_for('novo_produto'))

                codigo_barras, erro_codigo = _normalizar_codigo_barras(request.form.get('codigo'))
                if erro_codigo:
                    flash(erro_codigo, 'error')
                    return redirect(url_for('novo_produto'))

                nova_imagem_path, erro_imagem = _save_product_image(
                    request.files.get('imagem'),
                    request.form.get('nome')
                )
                if erro_imagem:
                    flash(erro_imagem, 'error')
                    return redirect(url_for('novo_produto'))

                produto = Produto(
                    codigo=codigo_barras,
                    nome=request.form.get('nome'),
                    descricao=request.form.get('descricao'),
                    imagem_path=_normalizar_imagem_produto(nova_imagem_path),
                    categoria_id=categoria_id,
                    fornecedor_id=fornecedor.id,
                    endereco_id=endereco_id,
                    preco_custo=float(request.form.get('preco_custo', 0)),
                    preco_venda=float(request.form.get('preco_venda', 0)),
                    quantidade_estoque=int(request.form.get('quantidade_estoque', 0)),
                    quantidade_minima=int(request.form.get('quantidade_minima', 5)),
                    status_disponibilidade=_normalizar_status_disponibilidade(request.form.get('status_disponibilidade')),
                    tipo_movimentacao=_normalizar_tipo_movimentacao(request.form.get('tipo_movimentacao')),
                    fora_picking=(request.form.get('fora_picking') == 'on'),
                    prioridade_reabastecimento=request.form.get('prioridade_reabastecimento', type=int),
                    servico_montagem_disponivel=(request.form.get('servico_montagem_disponivel') == 'on'),
                    servico_instalacao_disponivel=(request.form.get('servico_instalacao_disponivel') == 'on'),
                )
                db.session.add(produto)
                db.session.commit()
                flash(f'Produto "{produto.nome}" criado com sucesso!', 'success')
                return redirect(url_for('listar_produtos'))
            except Exception as e:
                db.session.rollback()
                if nova_imagem_path:
                    _delete_image_file(nova_imagem_path)
                flash(f'Erro ao criar produto: {str(e)}', 'error')

        categorias = Categoria.query.all()
        fornecedores = Fornecedor.query.filter(
            Fornecedor.ativo.is_(True),
            db.func.lower(Fornecedor.nome) != fornecedor_padrao_recebimento_nome.lower(),
        ).order_by(Fornecedor.nome.asc()).all()
        enderecos = _endereco_query_permitida(funcionario_logado).filter_by(ativo=True).order_by(EnderecoEstoque.nome.asc()).all()
        return render_template(
            'estoque/produtos/novo_produto.html',
            categorias=categorias,
            fornecedores=fornecedores,
            enderecos=enderecos,
            status_disponibilidade_labels=STATUS_DISPONIBILIDADE_LABELS,
            tipos_movimentacao_produto=TIPOS_MOVIMENTACAO_PRODUTO,
            codigos_existentes=[c[0] for c in db.session.query(Produto.codigo).all()]
        )

    @app.route('/produtos/<int:produto_id>/editar', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def editar_produto(produto_id):
        funcionario_logado = _funcionario_logado_estoque()
        produto = Produto.query.get_or_404(produto_id)
        if not _produto_em_estoque_permitido(produto, funcionario_logado):
            flash('Você não possui acesso ao estoque deste produto.', 'danger')
            return redirect(url_for('listar_produtos'))
        if request.method == 'POST':
            nova_imagem_path = None
            imagem_anterior = produto.imagem_path
            try:
                fornecedor_id = request.form.get('fornecedor_id', type=int)
                fornecedor = Fornecedor.query.get(fornecedor_id) if fornecedor_id else None
                if not fornecedor:
                    flash('Fornecedor invalido. Selecione um fornecedor para o produto.', 'error')
                    return redirect(url_for('editar_produto', produto_id=produto_id))
                endereco_id = request.form.get('endereco_id', type=int) or None
                if endereco_id and not _carregar_endereco_permitido(endereco_id, funcionario_logado, apenas_ativo=True):
                    flash('Endereco invalido ou fora dos estoques permitidos.', 'error')
                    return redirect(url_for('editar_produto', produto_id=produto_id))
                produto.nome = request.form.get('nome')
                produto.descricao = request.form.get('descricao')
                produto.categoria_id = int(request.form.get('categoria_id'))
                produto.fornecedor_id = fornecedor.id
                produto.endereco_id = endereco_id
                preco_custo_raw = request.form.get('preco_custo')
                if preco_custo_raw is not None and str(preco_custo_raw).strip() != '':
                    produto.preco_custo = float(preco_custo_raw)

                preco_venda_raw = request.form.get('preco_venda')
                if preco_venda_raw is not None and str(preco_venda_raw).strip() != '':
                    produto.preco_venda = float(preco_venda_raw)
                produto.quantidade_minima = int(request.form.get('quantidade_minima', 5))
                produto.status_disponibilidade = _normalizar_status_disponibilidade(request.form.get('status_disponibilidade'))
                produto.tipo_movimentacao = _normalizar_tipo_movimentacao(request.form.get('tipo_movimentacao'))
                produto.fora_picking = (request.form.get('fora_picking') == 'on')
                produto.prioridade_reabastecimento = request.form.get('prioridade_reabastecimento', type=int)
                produto.servico_montagem_disponivel = (request.form.get('servico_montagem_disponivel') == 'on')
                produto.servico_instalacao_disponivel = (request.form.get('servico_instalacao_disponivel') == 'on')

                remover_imagem = request.form.get('remover_imagem') == 'on'
                arquivo_imagem = request.files.get('imagem')

                if arquivo_imagem and arquivo_imagem.filename:
                    nova_imagem_path, erro_imagem = _save_product_image(arquivo_imagem, produto.nome)
                    if erro_imagem:
                        flash(erro_imagem, 'error')
                        return redirect(url_for('editar_produto', produto_id=produto_id))
                    produto.imagem_path = nova_imagem_path
                elif remover_imagem:
                    produto.imagem_path = _imagem_padrao_produto()

                produto.imagem_path = _normalizar_imagem_produto(produto.imagem_path)

                db.session.commit()

                if nova_imagem_path and imagem_anterior and imagem_anterior != nova_imagem_path:
                    _delete_image_file(imagem_anterior)
                if remover_imagem and imagem_anterior:
                    _delete_image_file(imagem_anterior)

                flash(f'Produto "{produto.nome}" atualizado com sucesso!', 'success')
                return redirect(url_for('listar_produtos'))
            except Exception as e:
                db.session.rollback()
                if nova_imagem_path:
                    _delete_image_file(nova_imagem_path)
                flash(f'Erro ao atualizar produto: {str(e)}', 'error')

        categorias = Categoria.query.all()
        fornecedores = Fornecedor.query.filter(
            Fornecedor.ativo.is_(True),
            db.func.lower(Fornecedor.nome) != fornecedor_padrao_recebimento_nome.lower(),
        ).order_by(Fornecedor.nome.asc()).all()
        enderecos = _endereco_query_permitida(funcionario_logado).filter_by(ativo=True).order_by(EnderecoEstoque.nome.asc()).all()
        return render_template(
            'estoque/produtos/editar_produto.html',
            produto=produto,
            categorias=categorias,
            fornecedores=fornecedores,
            enderecos=enderecos,
            status_disponibilidade_labels=STATUS_DISPONIBILIDADE_LABELS,
            tipos_movimentacao_produto=TIPOS_MOVIMENTACAO_PRODUTO,
            codigos_existentes=[c[0] for c in db.session.query(Produto.codigo).filter(Produto.id != produto.id).all()]
        )

    @app.route('/produtos/<int:produto_id>')
    @login_required
    def visualizar_produto(produto_id):
        funcionario_logado = _funcionario_logado_estoque()
        produto = Produto.query.get_or_404(produto_id)
        if not _produto_em_estoque_permitido(produto, funcionario_logado):
            flash('Você não possui acesso ao estoque deste produto.', 'danger')
            return redirect(url_for('listar_produtos'))
        movimentacoes = Movimentacao.query.filter_by(produto_id=produto_id).order_by(
            Movimentacao.criado_em.desc()
        ).all()
        return render_template('estoque/produtos/visualizar_produto.html', produto=produto, movimentacoes=movimentacoes)

    @app.route('/produtos/<int:produto_id>/deletar', methods=['POST'])
    @require_role(*estoque_write_roles)
    def deletar_produto(produto_id):
        funcionario_logado = _funcionario_logado_estoque()
        produto = Produto.query.get_or_404(produto_id)
        if not _produto_em_estoque_permitido(produto, funcionario_logado):
            flash('Você não possui acesso ao estoque deste produto.', 'danger')
            return redirect(url_for('listar_produtos'))
        imagem_produto = produto.imagem_path
        try:
            db.session.delete(produto)
            db.session.commit()
            if imagem_produto:
                _delete_image_file(imagem_produto)
            flash(f'Produto "{produto.nome}" deletado com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao deletar produto: {str(e)}', 'error')
        return redirect(url_for('listar_produtos'))

    @app.route('/produtos/<int:produto_id>/marcar-fora-picking', methods=['POST'])
    @require_role(*estoque_write_roles)
    def marcar_produto_fora_picking(produto_id):
        funcionario_logado = _funcionario_logado_estoque()
        produto = Produto.query.get_or_404(produto_id)
        if not _produto_em_estoque_permitido(produto, funcionario_logado):
            flash('Você não possui acesso ao estoque deste produto.', 'danger')
            return redirect(request.referrer or url_for('listar_produtos'))
        try:
            produto.fora_picking = True
            db.session.commit()
            flash(f'Produto "{produto.nome}" marcado como fora de picking.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao marcar fora de picking: {str(e)}', 'error')
        return redirect(request.referrer or url_for('listar_produtos'))

    @app.route('/produtos/<int:produto_id>/baixar-para-picking', methods=['POST'])
    @require_role(*estoque_write_roles)
    def baixar_produto_para_picking(produto_id):
        funcionario_logado = _funcionario_logado_estoque()
        produto = Produto.query.get_or_404(produto_id)
        if not _produto_em_estoque_permitido(produto, funcionario_logado):
            flash('Você não possui acesso ao estoque deste produto.', 'danger')
            return redirect(request.referrer or url_for('listar_produtos'))
        try:
            produto.fora_picking = False
            produto.ultima_baixa_picking_em = datetime.utcnow()
            db.session.commit()
            flash(f'Produto "{produto.nome}" baixado para fluxo de picking.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao baixar produto para picking: {str(e)}', 'error')
        return redirect(request.referrer or url_for('listar_produtos'))

    @app.route('/estoque/enderecos-inteligentes')
    @login_required
    def enderecos_inteligentes():
        empresa = _obter_empresa_config_estoque()
        funcionario_logado = _funcionario_logado_estoque()
        dias = request.args.get('dias', type=int) or 30
        if dias not in {7, 15, 30, 60, 90}:
            dias = 30
        data_limite = datetime.utcnow() - timedelta(days=dias)

        mais_vendidos = db.session.query(
            ItemPedido.produto_id,
            db.func.sum(ItemPedido.quantidade).label('qtd_vendida'),
        ).join(
            Pedido, Pedido.id == ItemPedido.pedido_id
        ).filter(
            Pedido.criado_em >= data_limite,
            Pedido.status != Pedido.STATUS_CANCELADO,
        ).group_by(
            ItemPedido.produto_id
        ).order_by(
            db.desc('qtd_vendida')
        ).limit(40).all()

        produtos_ids = [item.produto_id for item in mais_vendidos]
        produtos_map = {
            p.id: p for p in _produto_query_permitida(Produto.query, funcionario_logado).options(
                selectinload(Produto.endereco),
                selectinload(Produto.categoria),
            ).filter(Produto.id.in_(produtos_ids)).all()
        } if produtos_ids else {}

        ranking = []
        for item in mais_vendidos:
            produto = produtos_map.get(item.produto_id)
            if not produto:
                continue
            endereco = produto.endereco
            em_area_picking = bool(endereco and (endereco.tipo_area or '').lower() in {'picking', 'box_expedicao'})
            ranking.append({
                'produto': produto,
                'qtd_vendida': int(item.qtd_vendida or 0),
                'em_area_picking': em_area_picking,
            })

        enderecos_picking = _endereco_query_permitida(funcionario_logado).filter(
            EnderecoEstoque.ativo.is_(True),
            EnderecoEstoque.status == 'ativo',
            EnderecoEstoque.tipo_area.in_(['picking', 'box_expedicao', 'expedicao'])
        ).order_by(
            db.case((EnderecoEstoque.tipo_area == 'box_expedicao', 0), else_=1),
            EnderecoEstoque.prioridade_picking.asc().nullslast(),
            EnderecoEstoque.nome.asc()
        ).all()

        fora_picking = _produto_query_permitida(Produto.query, funcionario_logado).options(
            selectinload(Produto.endereco),
            selectinload(Produto.categoria),
        ).filter(
            Produto.ativo.is_(True),
            Produto.fora_picking.is_(True),
        ).order_by(
            db.case((Produto.prioridade_reabastecimento.is_(None), 1), else_=0),
            Produto.prioridade_reabastecimento.asc(),
            Produto.nome.asc()
        ).limit(120).all()

        return render_template(
            'estoque/enderecos/enderecos_inteligentes.html',
            empresa=empresa,
            dias=dias,
            ranking=ranking,
            enderecos_picking=enderecos_picking,
            fora_picking=fora_picking,
            reposicao_loja_ativa=_reposicao_loja_fisica_ativa(empresa),
            etiquetas_loja_ativas=_emissao_etiqueta_loja_ativa(empresa),
            etiquetas_endereco_ativas=_emissao_etiqueta_endereco_ativa(empresa),
            tipos_movimentacao_produto=TIPOS_MOVIMENTACAO_PRODUTO,
        )

    @app.route('/produtos/<int:produto_id>/enderecar-inteligente', methods=['POST'])
    @require_role(*estoque_write_roles)
    def enderecar_produto_inteligente(produto_id):
        funcionario_logado = _funcionario_logado_estoque()
        produto = Produto.query.get_or_404(produto_id)
        if not _produto_em_estoque_permitido(produto, funcionario_logado):
            flash('Você não possui acesso ao estoque deste produto.', 'danger')
            return redirect(request.referrer or url_for('enderecos_inteligentes'))
        try:
            endereco_id = request.form.get('endereco_id', type=int)
            endereco = _carregar_endereco_permitido(endereco_id, funcionario_logado, apenas_ativo=True) if endereco_id else None
            if not endereco:
                flash('Endereco inteligente invalido ou inativo.', 'error')
                return redirect(request.referrer or url_for('enderecos_inteligentes'))
            produto.endereco_id = endereco.id
            produto.fora_picking = False
            produto.ultima_baixa_picking_em = datetime.utcnow()
            db.session.commit()
            flash(f'Produto "{produto.nome}" direcionado para "{endereco.nome}" com sucesso.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao enderecar produto: {str(e)}', 'error')
        return redirect(request.referrer or url_for('enderecos_inteligentes'))

    @app.route('/estoque/equipamentos')
    @login_required
    def listar_equipamentos_movimentacao():
        status = (request.args.get('status') or '').strip().lower()
        tipo = (request.args.get('tipo') or '').strip().lower()
        busca = (request.args.get('busca') or '').strip()

        query = EquipamentoMovimentacao.query
        if status in EquipamentoMovimentacao.STATUS_VALIDOS:
            query = query.filter(EquipamentoMovimentacao.status == status)
        if tipo in EquipamentoMovimentacao.TIPOS_VALIDOS:
            query = query.filter(EquipamentoMovimentacao.tipo == tipo)
        if busca:
            termo = f'%{busca}%'
            query = query.filter(
                db.or_(
                    EquipamentoMovimentacao.codigo.ilike(termo),
                    EquipamentoMovimentacao.nome.ilike(termo),
                    EquipamentoMovimentacao.placa.ilike(termo),
                    EquipamentoMovimentacao.bateria_codigo.ilike(termo),
                )
            )

        equipamentos = query.order_by(
            db.case((EquipamentoMovimentacao.status == EquipamentoMovimentacao.STATUS_OPERACIONAL, 0), else_=1),
            EquipamentoMovimentacao.nome.asc(),
        ).all()
        return render_template(
            'estoque/equipamentos/equipamentos.html',
            equipamentos=equipamentos,
            filtros={'status': status, 'tipo': tipo, 'busca': busca},
            tipos_validos=EquipamentoMovimentacao.TIPOS_VALIDOS,
            status_validos=EquipamentoMovimentacao.STATUS_VALIDOS,
        )

    @app.route('/estoque/equipamentos/novo', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def novo_equipamento_movimentacao():
        if request.method == 'POST':
            try:
                codigo = (request.form.get('codigo') or '').strip().upper()
                nome = (request.form.get('nome') or '').strip()
                tipo = (request.form.get('tipo') or '').strip().lower()
                status = (request.form.get('status') or '').strip().lower()
                if not codigo or not nome:
                    flash('Codigo e nome do equipamento sao obrigatorios.', 'error')
                    return redirect(url_for('novo_equipamento_movimentacao'))
                if tipo not in EquipamentoMovimentacao.TIPOS_VALIDOS:
                    tipo = EquipamentoMovimentacao.TIPO_EMPILHADEIRA
                if status not in EquipamentoMovimentacao.STATUS_VALIDOS:
                    status = EquipamentoMovimentacao.STATUS_OPERACIONAL

                proxima_manutencao_em = None
                data_txt = (request.form.get('proxima_manutencao_em') or '').strip()
                if data_txt:
                    try:
                        proxima_manutencao_em = datetime.strptime(data_txt, '%Y-%m-%d').date()
                    except ValueError:
                        flash('Data de proxima manutencao invalida.', 'error')
                        return redirect(url_for('novo_equipamento_movimentacao'))

                equipamento = EquipamentoMovimentacao(
                    codigo=codigo,
                    nome=nome,
                    tipo=tipo,
                    placa=(request.form.get('placa') or '').strip().upper() or None,
                    capacidade_kg=request.form.get('capacidade_kg', type=float),
                    bateria_codigo=(request.form.get('bateria_codigo') or '').strip().upper() or None,
                    bateria_nivel=request.form.get('bateria_nivel', type=int),
                    status=status,
                    proxima_manutencao_em=proxima_manutencao_em,
                    observacoes=(request.form.get('observacoes') or '').strip() or None,
                    ativo=(request.form.get('ativo') == 'on'),
                )
                db.session.add(equipamento)
                db.session.commit()
                flash(f'Equipamento "{equipamento.nome}" cadastrado com sucesso.', 'success')
                return redirect(url_for('listar_equipamentos_movimentacao'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao cadastrar equipamento: {str(e)}', 'error')

        return render_template(
            'estoque/equipamentos/novo_equipamento.html',
            tipos_validos=EquipamentoMovimentacao.TIPOS_VALIDOS,
            status_validos=EquipamentoMovimentacao.STATUS_VALIDOS,
        )

    @app.route('/estoque/equipamentos/<int:equipamento_id>/editar', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def editar_equipamento_movimentacao(equipamento_id):
        equipamento = EquipamentoMovimentacao.query.get_or_404(equipamento_id)
        if request.method == 'POST':
            try:
                if request.form.get('acao') == 'nova_manutencao':
                    descricao = (request.form.get('descricao_manutencao') or '').strip()
                    if not descricao:
                        flash('Descricao da manutencao e obrigatoria.', 'error')
                        return redirect(url_for('editar_equipamento_movimentacao', equipamento_id=equipamento.id))
                    tipo_manut = (request.form.get('tipo_manutencao') or 'preventiva').strip().lower()
                    if tipo_manut not in {'preventiva', 'corretiva'}:
                        tipo_manut = 'preventiva'
                    realizado_em = None
                    realizado_txt = (request.form.get('realizado_em') or '').strip()
                    if realizado_txt:
                        realizado_em = datetime.strptime(realizado_txt, '%Y-%m-%d').date()
                    proxima_em = None
                    proxima_txt = (request.form.get('proxima_em') or '').strip()
                    if proxima_txt:
                        proxima_em = datetime.strptime(proxima_txt, '%Y-%m-%d').date()
                    manutencao = ManutencaoEquipamento(
                        equipamento_id=equipamento.id,
                        tipo=tipo_manut,
                        descricao=descricao,
                        custo=request.form.get('custo_manutencao', type=float),
                        realizado_em=realizado_em,
                        proxima_em=proxima_em,
                        responsavel=(request.form.get('responsavel_manutencao') or '').strip() or None,
                    )
                    db.session.add(manutencao)
                    if proxima_em:
                        equipamento.proxima_manutencao_em = proxima_em
                    equipamento.status = EquipamentoMovimentacao.STATUS_MANUTENCAO if tipo_manut == 'corretiva' else equipamento.status
                    db.session.commit()
                    flash('Manutencao registrada com sucesso.', 'success')
                    return redirect(url_for('editar_equipamento_movimentacao', equipamento_id=equipamento.id))

                equipamento.codigo = (request.form.get('codigo') or '').strip().upper()
                equipamento.nome = (request.form.get('nome') or '').strip()
                tipo = (request.form.get('tipo') or '').strip().lower()
                status = (request.form.get('status') or '').strip().lower()
                if tipo in EquipamentoMovimentacao.TIPOS_VALIDOS:
                    equipamento.tipo = tipo
                if status in EquipamentoMovimentacao.STATUS_VALIDOS:
                    equipamento.status = status
                equipamento.placa = (request.form.get('placa') or '').strip().upper() or None
                equipamento.capacidade_kg = request.form.get('capacidade_kg', type=float)
                equipamento.bateria_codigo = (request.form.get('bateria_codigo') or '').strip().upper() or None
                equipamento.bateria_nivel = request.form.get('bateria_nivel', type=int)
                equipamento.observacoes = (request.form.get('observacoes') or '').strip() or None
                equipamento.ativo = (request.form.get('ativo') == 'on')
                data_txt = (request.form.get('proxima_manutencao_em') or '').strip()
                equipamento.proxima_manutencao_em = datetime.strptime(data_txt, '%Y-%m-%d').date() if data_txt else None

                if not equipamento.codigo or not equipamento.nome:
                    flash('Codigo e nome do equipamento sao obrigatorios.', 'error')
                    return redirect(url_for('editar_equipamento_movimentacao', equipamento_id=equipamento.id))

                db.session.commit()
                flash('Equipamento atualizado com sucesso.', 'success')
                return redirect(url_for('listar_equipamentos_movimentacao'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao atualizar equipamento: {str(e)}', 'error')

        manutencoes = ManutencaoEquipamento.query.filter_by(
            equipamento_id=equipamento.id
        ).order_by(
            ManutencaoEquipamento.criado_em.desc()
        ).all()
        return render_template(
            'estoque/equipamentos/editar_equipamento.html',
            equipamento=equipamento,
            manutencoes=manutencoes,
            tipos_validos=EquipamentoMovimentacao.TIPOS_VALIDOS,
            status_validos=EquipamentoMovimentacao.STATUS_VALIDOS,
        )

    @app.route('/categorias')
    @login_required
    def listar_categorias():
        categorias = Categoria.query.all()
        return render_template('estoque/categorias/categorias.html', categorias=categorias)

    @app.route('/categorias/nova', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def nova_categoria():
        if request.method == 'POST':
            nova_imagem_path = None
            try:
                nome_categoria = request.form.get('nome')
                nova_imagem_path, erro_imagem = _save_category_image(
                    request.files.get('imagem'),
                    nome_categoria
                )
                if erro_imagem:
                    flash(erro_imagem, 'error')
                    return redirect(url_for('nova_categoria'))

                categoria = Categoria(
                    nome=nome_categoria,
                    descricao=request.form.get('descricao'),
                    imagem_path=nova_imagem_path
                )
                db.session.add(categoria)
                db.session.commit()
                flash(f'Categoria "{categoria.nome}" criada com sucesso!', 'success')
                return redirect(url_for('listar_categorias'))
            except Exception as e:
                db.session.rollback()
                if nova_imagem_path:
                    _delete_image_file(nova_imagem_path)
                flash(f'Erro ao criar categoria: {str(e)}', 'error')
        return render_template('estoque/categorias/nova_categoria.html')

    @app.route('/categorias/<int:categoria_id>/editar', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def editar_categoria(categoria_id):
        categoria = Categoria.query.get_or_404(categoria_id)
        if request.method == 'POST':
            nova_imagem_path = None
            imagem_anterior = categoria.imagem_path
            try:
                categoria.nome = request.form.get('nome')
                categoria.descricao = request.form.get('descricao')
                remover_imagem = request.form.get('remover_imagem') == 'on'
                arquivo_imagem = request.files.get('imagem')

                if arquivo_imagem and arquivo_imagem.filename:
                    nova_imagem_path, erro_imagem = _save_category_image(arquivo_imagem, categoria.nome)
                    if erro_imagem:
                        flash(erro_imagem, 'error')
                        return redirect(url_for('editar_categoria', categoria_id=categoria_id))
                    categoria.imagem_path = nova_imagem_path
                elif remover_imagem:
                    categoria.imagem_path = None

                db.session.commit()

                if nova_imagem_path and imagem_anterior and imagem_anterior != nova_imagem_path:
                    _delete_image_file(imagem_anterior)
                if remover_imagem and imagem_anterior:
                    _delete_image_file(imagem_anterior)

                flash(f'Categoria "{categoria.nome}" atualizada com sucesso!', 'success')
                return redirect(url_for('listar_categorias'))
            except Exception as e:
                db.session.rollback()
                if nova_imagem_path:
                    _delete_image_file(nova_imagem_path)
                flash(f'Erro ao atualizar categoria: {str(e)}', 'error')
        return render_template('estoque/categorias/editar_categoria.html', categoria=categoria)

    @app.route('/categorias/<int:categoria_id>/deletar', methods=['POST'])
    @require_role(*estoque_write_roles)
    def deletar_categoria(categoria_id):
        categoria = Categoria.query.get_or_404(categoria_id)
        imagem_categoria = categoria.imagem_path
        try:
            db.session.delete(categoria)
            db.session.commit()
            if imagem_categoria:
                _delete_image_file(imagem_categoria)
            flash(f'Categoria "{categoria.nome}" deletada com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao deletar categoria: {str(e)}', 'error')
        return redirect(url_for('listar_categorias'))

    @app.route('/fornecedores')
    @login_required
    def listar_fornecedores():
        page = max(request.args.get('page', 1, type=int), 1)
        per_page = min(max(request.args.get('per_page', 25, type=int), 1), 100)
        busca = (request.args.get('busca') or '').strip()
        status = (request.args.get('status') or '').strip().lower()

        query = Fornecedor.query
        if busca:
            termo = f'%{busca}%'
            query = query.filter(
                db.or_(
                    Fornecedor.nome.ilike(termo),
                    Fornecedor.documento.ilike(termo),
                    Fornecedor.contato.ilike(termo),
                    Fornecedor.telefone.ilike(termo),
                    Fornecedor.email.ilike(termo),
                    Fornecedor.endereco_cidade.ilike(termo),
                    Fornecedor.tipo_produtos_fornece.ilike(termo),
                )
            )
        if status == 'ativo':
            query = query.filter(Fornecedor.ativo.is_(True))
        elif status == 'inativo':
            query = query.filter(Fornecedor.ativo.is_(False))

        pagination = query.order_by(Fornecedor.nome.asc()).paginate(page=page, per_page=per_page, error_out=False)
        return render_template(
            'estoque/fornecedores/fornecedores.html',
            fornecedores=pagination.items,
            pagination=pagination,
            per_page=per_page,
            filtros={'busca': busca, 'status': status},
            query_params=request.args.to_dict(),
        )

    @app.route('/fornecedores/<int:fornecedor_id>')
    @login_required
    def detalhes_fornecedor(fornecedor_id):
        fornecedor = Fornecedor.query.get_or_404(fornecedor_id)
        recebimentos = RecebimentoFornecedor.query.filter_by(
            fornecedor_id=fornecedor.id
        ).order_by(
            RecebimentoFornecedor.criado_em.desc()
        ).limit(20).all()
        movimentacoes = Movimentacao.query.filter_by(
            fornecedor_id=fornecedor.id
        ).order_by(
            Movimentacao.criado_em.desc()
        ).limit(20).all()
        return render_template(
            'estoque/fornecedores/detalhes_fornecedor.html',
            fornecedor=fornecedor,
            recebimentos=recebimentos,
            movimentacoes=movimentacoes,
        )

    @app.route('/fornecedores/novo', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def novo_fornecedor():
        if request.method == 'POST':
            try:
                fornecedor = Fornecedor(
                    nome=request.form.get('nome', '').strip(),
                    documento=request.form.get('documento', '').strip() or None,
                    contato=request.form.get('contato', '').strip() or None,
                    telefone=request.form.get('telefone', '').strip() or None,
                    email=request.form.get('email', '').strip() or None,
                    endereco_rua=request.form.get('endereco_rua', '').strip() or None,
                    endereco_numero=request.form.get('endereco_numero', '').strip() or None,
                    endereco_bairro=request.form.get('endereco_bairro', '').strip() or None,
                    endereco_cidade=request.form.get('endereco_cidade', '').strip() or None,
                    tipo_produtos_fornece=request.form.get('tipo_produtos_fornece', '').strip() or None,
                    observacoes_gerais=request.form.get('observacoes_gerais', '').strip() or None,
                    ativo=(request.form.get('ativo') == 'on')
                )
                if not fornecedor.nome:
                    flash('Nome do fornecedor e obrigatorio.', 'error')
                    return redirect(url_for('novo_fornecedor'))
                db.session.add(fornecedor)
                db.session.commit()
                flash(f'Fornecedor "{fornecedor.nome}" cadastrado com sucesso!', 'success')
                return redirect(url_for('listar_fornecedores'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao cadastrar fornecedor: {str(e)}', 'error')
        return render_template('estoque/fornecedores/novo_fornecedor.html')

    @app.route('/fornecedores/<int:fornecedor_id>/editar', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def editar_fornecedor(fornecedor_id):
        fornecedor = Fornecedor.query.get_or_404(fornecedor_id)
        if request.method == 'POST':
            try:
                nome = request.form.get('nome', '').strip()
                if not nome:
                    flash('Nome do fornecedor e obrigatorio.', 'error')
                    return redirect(url_for('editar_fornecedor', fornecedor_id=fornecedor_id))
                fornecedor.nome = nome
                fornecedor.documento = request.form.get('documento', '').strip() or None
                fornecedor.contato = request.form.get('contato', '').strip() or None
                fornecedor.telefone = request.form.get('telefone', '').strip() or None
                fornecedor.email = request.form.get('email', '').strip() or None
                fornecedor.endereco_rua = request.form.get('endereco_rua', '').strip() or None
                fornecedor.endereco_numero = request.form.get('endereco_numero', '').strip() or None
                fornecedor.endereco_bairro = request.form.get('endereco_bairro', '').strip() or None
                fornecedor.endereco_cidade = request.form.get('endereco_cidade', '').strip() or None
                fornecedor.tipo_produtos_fornece = request.form.get('tipo_produtos_fornece', '').strip() or None
                fornecedor.observacoes_gerais = request.form.get('observacoes_gerais', '').strip() or None
                fornecedor.ativo = (request.form.get('ativo') == 'on')
                db.session.commit()
                flash(f'Fornecedor "{fornecedor.nome}" atualizado com sucesso!', 'success')
                return redirect(url_for('listar_fornecedores'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao atualizar fornecedor: {str(e)}', 'error')
        return render_template('estoque/fornecedores/editar_fornecedor.html', fornecedor=fornecedor)

    @app.route('/fornecedores/<int:fornecedor_id>/deletar', methods=['POST'])
    @require_role(*estoque_write_roles)
    def deletar_fornecedor(fornecedor_id):
        fornecedor = Fornecedor.query.get_or_404(fornecedor_id)
        try:
            db.session.delete(fornecedor)
            db.session.commit()
            flash(f'Fornecedor "{fornecedor.nome}" removido com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao remover fornecedor: {str(e)}', 'error')
        return redirect(url_for('listar_fornecedores'))

    @app.route('/estoque/recebimentos')
    @login_required
    def listar_recebimentos_fornecedor():
        page = max(request.args.get('page', 1, type=int), 1)
        per_page = min(max(request.args.get('per_page', 20, type=int), 1), 100)
        status = (request.args.get('status') or '').strip().lower()
        tipo_recebimento = (request.args.get('tipo_recebimento') or '').strip().lower()
        fornecedor_id = request.args.get('fornecedor_id', type=int)
        busca = (request.args.get('busca') or '').strip()
        data_inicio_txt = (request.args.get('data_inicio') or '').strip()
        data_fim_txt = (request.args.get('data_fim') or '').strip()
        data_inicio = _parse_data_filtro(data_inicio_txt)
        data_fim = _parse_data_filtro(data_fim_txt)

        query = RecebimentoFornecedor.query
        if status in RecebimentoFornecedor.STATUS_VALIDOS:
            query = query.filter(RecebimentoFornecedor.status == status)
        if tipo_recebimento in RecebimentoFornecedor.TIPOS_VALIDOS:
            query = query.filter(RecebimentoFornecedor.tipo_recebimento == tipo_recebimento)
        if fornecedor_id:
            query = query.filter(RecebimentoFornecedor.fornecedor_id == fornecedor_id)
        if data_inicio:
            query = query.filter(RecebimentoFornecedor.criado_em >= data_inicio)
        if data_fim:
            query = query.filter(RecebimentoFornecedor.criado_em < (data_fim + timedelta(days=1)))
        if busca:
            termo = f'%{busca}%'
            query = query.outerjoin(Fornecedor, Fornecedor.id == RecebimentoFornecedor.fornecedor_id).outerjoin(
                Funcionario, Funcionario.id == RecebimentoFornecedor.recebedor_funcionario_id
            ).outerjoin(
                RecebimentoItem, RecebimentoItem.recebimento_id == RecebimentoFornecedor.id
            ).outerjoin(
                Produto, Produto.id == RecebimentoItem.produto_id
            ).filter(
                db.or_(
                    Fornecedor.nome.ilike(termo),
                    Funcionario.nome.ilike(termo),
                    Funcionario.matricula.ilike(termo),
                    RecebimentoFornecedor.info_nota.ilike(termo),
                    RecebimentoFornecedor.observacoes.ilike(termo),
                    RecebimentoFornecedor.recebedor_nome.ilike(termo),
                    Produto.nome.ilike(termo),
                    Produto.codigo.ilike(termo),
                    db.cast(RecebimentoFornecedor.id, db.String).ilike(termo),
                )
            ).distinct()

        recebimentos = query.options(
            load_only(
                RecebimentoFornecedor.id,
                RecebimentoFornecedor.fornecedor_id,
                RecebimentoFornecedor.tipo_recebimento,
                RecebimentoFornecedor.info_nota,
                RecebimentoFornecedor.subtotal,
                RecebimentoFornecedor.total_pagar,
                RecebimentoFornecedor.status,
                RecebimentoFornecedor.recebedor_funcionario_id,
                RecebimentoFornecedor.recebedor_nome,
                RecebimentoFornecedor.criado_em,
                RecebimentoFornecedor.conferido_em,
            ),
            selectinload(RecebimentoFornecedor.fornecedor),
            selectinload(RecebimentoFornecedor.recebedor_funcionario),
            selectinload(RecebimentoFornecedor.itens).selectinload(RecebimentoItem.produto),
        ).order_by(RecebimentoFornecedor.criado_em.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False,
        )
        pendencias_armazenagem = RecebimentoFornecedor.query.filter_by(
            status=RecebimentoFornecedor.STATUS_AGUARDANDO_ARMAZENAGEM
        ).count()
        recebimento_armazenagem_mais_antigo = RecebimentoFornecedor.query.filter_by(
            status=RecebimentoFornecedor.STATUS_AGUARDANDO_ARMAZENAGEM
        ).order_by(
            RecebimentoFornecedor.conferido_em.asc(),
            RecebimentoFornecedor.criado_em.asc(),
        ).first()
        fornecedores = Fornecedor.query.filter(
            Fornecedor.ativo.is_(True),
            db.func.lower(Fornecedor.nome) != fornecedor_padrao_recebimento_nome.lower(),
        ).order_by(Fornecedor.nome.asc()).all()
        return render_template(
            'estoque/recebimentos/recebimentos.html',
            recebimentos=recebimentos.items,
            pagination=recebimentos,
            per_page=per_page,
            fornecedores=fornecedores,
            pendencias_armazenagem=pendencias_armazenagem,
            recebimento_armazenagem_mais_antigo=recebimento_armazenagem_mais_antigo,
            status_labels=recebimento_status_labels,
            tipo_labels=recebimento_tipo_labels,
            filtros={
                'status': status,
                'tipo_recebimento': tipo_recebimento,
                'fornecedor_id': fornecedor_id,
                'busca': busca,
                'data_inicio': data_inicio_txt,
                'data_fim': data_fim_txt,
            },
            query_params=request.args.to_dict(),
        )

    @app.route('/estoque/recebimentos/novo', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def novo_recebimento_fornecedor():
        funcionario_logado = _funcionario_logado_estoque()
        fornecedores = Fornecedor.query.filter(
            Fornecedor.ativo.is_(True),
            db.func.lower(Fornecedor.nome) != fornecedor_padrao_recebimento_nome.lower(),
        ).order_by(Fornecedor.nome.asc()).all()
        produtos = _produto_query_permitida(Produto.query.filter_by(ativo=True), funcionario_logado).order_by(Produto.nome.asc()).all()
        funcionarios_recebimento = Funcionario.query.filter_by(ativo=True).options(
            load_only(
                Funcionario.id,
                Funcionario.nome,
                Funcionario.matricula,
                Funcionario.numero_cadastro,
                Funcionario.departamento,
            )
        ).order_by(Funcionario.nome.asc()).all()

        if request.method == 'POST':
            try:
                fornecedor_id = request.form.get('fornecedor_id', type=int)
                tipo_recebimento = (request.form.get('tipo_recebimento') or '').strip().lower()
                fornecedor = Fornecedor.query.get(fornecedor_id) if fornecedor_id else None
                if tipo_recebimento not in RecebimentoFornecedor.TIPOS_VALIDOS:
                    flash('Selecione um tipo de recebimento valido.', 'error')
                    return redirect(url_for('novo_recebimento_fornecedor'))
                if fornecedor_id and not fornecedor:
                    flash('Selecione um fornecedor valido.', 'error')
                    return redirect(url_for('novo_recebimento_fornecedor'))
                if _tipo_recebimento_exige_fornecedor(tipo_recebimento) and not fornecedor:
                    flash('Este tipo de recebimento exige fornecedor informado.', 'error')
                    return redirect(url_for('novo_recebimento_fornecedor'))
                if not fornecedor:
                    fornecedor = _obter_fornecedor_padrao_recebimento()

                recebedor_funcionario = _resolver_funcionario_por_matricula_ou_nome(
                    texto_busca=(request.form.get('recebedor_busca') or request.form.get('recebedor_nome') or '').strip(),
                    funcionario_id=request.form.get('recebedor_funcionario_id', type=int),
                )
                recebedor_nome = (
                    recebedor_funcionario.nome
                    if recebedor_funcionario
                    else (request.form.get('recebedor_nome') or request.form.get('recebedor_busca') or '').strip() or None
                )

                produto_ids = request.form.getlist('produto_id[]') or request.form.getlist('produto_id')
                quantidades = request.form.getlist('qtd_recebida[]') or request.form.getlist('qtd_recebida')
                unidades = request.form.getlist('unidade[]') or request.form.getlist('unidade')
                descricoes_itens = request.form.getlist('descricao_item[]') or request.form.getlist('descricao_item')
                precos_unitarios = request.form.getlist('preco_unitario[]') or request.form.getlist('preco_unitario')
                if not produto_ids:
                    flash('Informe ao menos um item no recebimento.', 'error')
                    return redirect(url_for('novo_recebimento_fornecedor'))

                data_entrega = None
                data_entrega_txt = (request.form.get('data_entrega') or '').strip()
                if data_entrega_txt:
                    try:
                        data_entrega = datetime.strptime(data_entrega_txt, '%Y-%m-%d').date()
                    except ValueError:
                        flash('Data de entrega invalida.', 'error')
                        return redirect(url_for('novo_recebimento_fornecedor'))

                subtotal = 0.0
                desconto_raw = (request.form.get('desconto') or '').strip()
                if desconto_raw:
                    try:
                        desconto = float(desconto_raw.replace(',', '.'))
                    except ValueError:
                        flash('Desconto invalido.', 'error')
                        return redirect(url_for('novo_recebimento_fornecedor'))
                else:
                    desconto = 0.0
                if desconto < 0:
                    flash('Desconto nao pode ser negativo.', 'error')
                    return redirect(url_for('novo_recebimento_fornecedor'))

                itens_processados = []
                for idx, raw_produto_id in enumerate(produto_ids):
                    texto_produto_id = str(raw_produto_id or '').strip()
                    if not texto_produto_id:
                        continue
                    try:
                        produto_id = int(texto_produto_id)
                    except ValueError:
                        flash('Produto invalido em um dos itens.', 'error')
                        return redirect(url_for('novo_recebimento_fornecedor'))

                    produto = Produto.query.get(produto_id)
                    if not produto or not produto.ativo:
                        flash('Um dos produtos informados nao existe ou esta inativo.', 'error')
                        return redirect(url_for('novo_recebimento_fornecedor'))
                    if not _produto_em_estoque_permitido(produto, funcionario_logado):
                        flash(f'Voce nao possui acesso ao estoque do produto "{produto.nome}".', 'error')
                        return redirect(url_for('novo_recebimento_fornecedor'))

                    raw_qtd = quantidades[idx] if idx < len(quantidades) else '0'
                    try:
                        qtd_recebida = int(str(raw_qtd or '0').strip() or '0')
                    except ValueError:
                        flash(f'Quantidade invalida para o produto "{produto.nome}".', 'error')
                        return redirect(url_for('novo_recebimento_fornecedor'))
                    if qtd_recebida < 0:
                        flash(f'Quantidade recebida nao pode ser negativa para o produto "{produto.nome}".', 'error')
                        return redirect(url_for('novo_recebimento_fornecedor'))

                    unidade = (unidades[idx] if idx < len(unidades) else '').strip().upper() or 'UN'
                    descricao_item = (descricoes_itens[idx] if idx < len(descricoes_itens) else '').strip() or produto.nome
                    raw_preco = (precos_unitarios[idx] if idx < len(precos_unitarios) else '').strip()
                    if raw_preco:
                        try:
                            preco_unitario = float(raw_preco.replace(',', '.'))
                        except ValueError:
                            flash(f'Preco unitario invalido para o produto "{produto.nome}".', 'error')
                            return redirect(url_for('novo_recebimento_fornecedor'))
                    else:
                        preco_unitario = float(produto.preco_custo or 0.0)
                    if preco_unitario < 0:
                        flash(f'Preco unitario nao pode ser negativo para o produto "{produto.nome}".', 'error')
                        return redirect(url_for('novo_recebimento_fornecedor'))

                    total_item = float(qtd_recebida) * float(preco_unitario)
                    subtotal += total_item
                    itens_processados.append({
                        'produto_id': produto_id,
                        'qtd_recebida': qtd_recebida,
                        'unidade': unidade,
                        'descricao_item': descricao_item,
                        'preco_unitario': preco_unitario,
                        'total_item': total_item,
                    })

                if not itens_processados:
                    flash('Informe ao menos um item valido no recebimento.', 'error')
                    return redirect(url_for('novo_recebimento_fornecedor'))

                total_pagar = max(subtotal - desconto, 0.0)

                recebimento = RecebimentoFornecedor(
                    fornecedor_id=fornecedor.id,
                    tipo_recebimento=tipo_recebimento,
                    fornecedor_documento=(request.form.get('fornecedor_documento') or '').strip() or None,
                    data_entrega=data_entrega,
                    info_nota=(request.form.get('info_nota') or '').strip() or None,
                    subtotal=subtotal,
                    desconto=desconto,
                    total_pagar=total_pagar,
                    observacoes=(request.form.get('observacoes') or '').strip() or None,
                    recebedor_funcionario_id=(recebedor_funcionario.id if recebedor_funcionario else None),
                    recebedor_nome=recebedor_nome,
                    recebedor_assinatura=(request.form.get('recebedor_assinatura') or '').strip() or None,
                    entregador_nome=(request.form.get('entregador_nome') or '').strip() or None,
                    entregador_assinatura=(request.form.get('entregador_assinatura') or '').strip() or None,
                    status=RecebimentoFornecedor.STATUS_CRIADO,
                )
                ir_para_armazenagem = (request.form.get('ir_para_armazenagem') == 'on')
                if ir_para_armazenagem:
                    recebimento.status = RecebimentoFornecedor.STATUS_AGUARDANDO_ARMAZENAGEM
                    recebimento.conferido_em = datetime.utcnow()
                db.session.add(recebimento)
                db.session.flush()

                for item in itens_processados:
                    db.session.add(
                        RecebimentoItem(
                            recebimento_id=recebimento.id,
                            produto_id=item['produto_id'],
                            qtd_recebida=item['qtd_recebida'],
                            unidade=item['unidade'],
                            descricao_item=item['descricao_item'],
                            preco_unitario=item['preco_unitario'],
                            total_item=item['total_item'],
                            qtd_avaria=0,
                        )
                    )

                db.session.commit()
                if ir_para_armazenagem:
                    flash('Recebimento criado. Direcionando para armazenagem em enderecos ativos.', 'success')
                    return redirect(url_for('armazenar_recebimento_fornecedor', recebimento_id=recebimento.id))
                flash('Recebimento criado com sucesso. Agora confira os itens.', 'success')
                return redirect(url_for('conferir_recebimento_fornecedor', recebimento_id=recebimento.id))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao criar recebimento: {str(e)}', 'error')

        return render_template(
            'estoque/recebimentos/novo_recebimento.html',
            fornecedores=fornecedores,
            produtos=produtos,
            funcionarios_recebimento=funcionarios_recebimento,
            tipo_labels=recebimento_tipo_labels,
            tipo_recebimento_padrao=RecebimentoFornecedor.TIPO_COMPRA_REVENDA,
            tipos_fornecedor_opcional=sorted(recebimento_tipos_fornecedor_opcional),
        )

    @app.route('/estoque/recebimentos/<int:recebimento_id>/conferir', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def conferir_recebimento_fornecedor(recebimento_id):
        recebimento = RecebimentoFornecedor.query.options(
            selectinload(RecebimentoFornecedor.fornecedor),
            selectinload(RecebimentoFornecedor.recebedor_funcionario),
            selectinload(RecebimentoFornecedor.itens).selectinload(RecebimentoItem.produto),
        ).get_or_404(recebimento_id)

        if recebimento.status in {RecebimentoFornecedor.STATUS_CANCELADO, RecebimentoFornecedor.STATUS_CONCLUIDO}:
            flash('Nao e possivel conferir um recebimento cancelado ou concluido.', 'warning')
            return redirect(url_for('listar_recebimentos_fornecedor'))

        if request.method == 'POST':
            try:
                for item in recebimento.itens:
                    prefix = f'item_{item.id}_'
                    raw_qtd_recebida = request.form.get(f'{prefix}qtd_recebida', '0')
                    raw_qtd_avaria = request.form.get(f'{prefix}qtd_avaria', '0')
                    lote = (request.form.get(f'{prefix}lote') or '').strip() or None
                    validade_texto = (request.form.get(f'{prefix}validade') or '').strip()

                    try:
                        qtd_recebida = int(str(raw_qtd_recebida or '0').strip() or '0')
                    except ValueError:
                        raise ValueError(f'Quantidade recebida invalida para o produto "{item.produto.nome}".')
                    try:
                        qtd_avaria = int(str(raw_qtd_avaria or '0').strip() or '0')
                    except ValueError:
                        raise ValueError(f'Quantidade avariada invalida para o produto "{item.produto.nome}".')

                    if qtd_recebida < 0:
                        raise ValueError(f'Quantidade recebida nao pode ser negativa para o produto "{item.produto.nome}".')
                    if qtd_avaria < 0:
                        raise ValueError(f'Quantidade avariada nao pode ser negativa para o produto "{item.produto.nome}".')
                    if qtd_avaria > qtd_recebida:
                        raise ValueError(f'Avaria nao pode ser maior que recebimento no produto "{item.produto.nome}".')

                    validade = None
                    if validade_texto:
                        try:
                            validade = datetime.strptime(validade_texto, '%Y-%m-%d').date()
                        except ValueError:
                            raise ValueError(f'Data de validade invalida para o produto "{item.produto.nome}".')

                    item.qtd_recebida = qtd_recebida
                    item.qtd_avaria = qtd_avaria
                    item.lote = lote
                    item.validade = validade

                recebimento.status = RecebimentoFornecedor.STATUS_AGUARDANDO_ARMAZENAGEM
                recebimento.conferido_em = datetime.utcnow()
                db.session.commit()
                flash('Conferencia salva. Proximo passo: armazenagem (put-away).', 'success')
                return redirect(url_for('armazenar_recebimento_fornecedor', recebimento_id=recebimento.id))
            except ValueError as e:
                db.session.rollback()
                flash(str(e), 'error')
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao conferir recebimento: {str(e)}', 'error')

        return render_template(
            'estoque/recebimentos/conferir_recebimento.html',
            recebimento=recebimento,
            status_labels=recebimento_status_labels,
            tipo_labels=recebimento_tipo_labels,
        )

    @app.route('/estoque/recebimentos/<int:recebimento_id>/armazenar', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def armazenar_recebimento_fornecedor(recebimento_id):
        funcionario_logado = _funcionario_logado_estoque()
        recebimento = RecebimentoFornecedor.query.options(
            selectinload(RecebimentoFornecedor.fornecedor),
            selectinload(RecebimentoFornecedor.recebedor_funcionario),
            selectinload(RecebimentoFornecedor.itens).selectinload(RecebimentoItem.produto).selectinload(Produto.categoria),
        ).get_or_404(recebimento_id)

        if recebimento.status == RecebimentoFornecedor.STATUS_CANCELADO:
            flash('Recebimento cancelado. Armazenagem nao permitida.', 'warning')
            return redirect(url_for('listar_recebimentos_fornecedor'))
        if recebimento.status == RecebimentoFornecedor.STATUS_CONCLUIDO:
            flash('Recebimento ja concluido.', 'info')
            return redirect(url_for('listar_recebimentos_fornecedor'))
        if recebimento.status == RecebimentoFornecedor.STATUS_CRIADO:
            flash('Conclua a conferencia antes da armazenagem.', 'warning')
            return redirect(url_for('conferir_recebimento_fornecedor', recebimento_id=recebimento.id))

        enderecos_ativos = _endereco_query_permitida(funcionario_logado).filter(EnderecoEstoque.status == 'ativo').order_by(EnderecoEstoque.nome.asc()).all()
        enderecos_por_id = {endereco.id: endereco for endereco in enderecos_ativos}

        if request.method == 'POST':
            try:
                if not enderecos_ativos:
                    flash('Nao existem enderecos ativos para armazenagem.', 'error')
                    return redirect(url_for('armazenar_recebimento_fornecedor', recebimento_id=recebimento.id))

                erros = []
                destinos_por_item = {}
                for item in recebimento.itens:
                    endereco_destino_id = request.form.get(f'endereco_destino_{item.id}', type=int)
                    if not endereco_destino_id:
                        erros.append(f'Informe o endereco destino para "{item.produto.nome}".')
                        continue
                    endereco_destino = enderecos_por_id.get(endereco_destino_id)
                    if not endereco_destino:
                        erros.append(f'Endereco destino invalido/inativo para "{item.produto.nome}".')
                        continue
                    if item.qtd_liquida > 0 and (endereco_destino.controle_validade or 'nenhum') == 'fefo' and not item.validade:
                        erros.append(f'Endereco "{endereco_destino.nome}" exige FEFO. Informe validade para "{item.produto.nome}".')
                    restricoes = {parte.strip().lower() for parte in (endereco_destino.restricoes or '').split(',') if parte.strip()}
                    if 'alimentos' in restricoes and _categoria_parece_quimico(item.produto):
                        erros.append(
                            f'Produto "{item.produto.nome}" (categoria quimica) nao pode ser armazenado no endereco de alimentos "{endereco_destino.nome}".'
                        )
                    destinos_por_item[item.id] = endereco_destino

                if erros:
                    for erro in erros:
                        flash(erro, 'error')
                    return redirect(url_for('armazenar_recebimento_fornecedor', recebimento_id=recebimento.id))

                for item in recebimento.itens:
                    endereco_destino = destinos_por_item[item.id]
                    item.endereco_destino_id = endereco_destino.id
                    quantidade_entrada = item.qtd_liquida
                    if quantidade_entrada <= 0:
                        continue

                    aplicar_movimentacao_estoque(item.produto, Movimentacao.TIPO_ENTRADA, quantidade_entrada)

                    item.produto.endereco_id = endereco_destino.id
                    tipo_recebimento_label = recebimento_tipo_labels.get(
                        recebimento.tipo_recebimento,
                        recebimento.tipo_recebimento or 'Recebimento'
                    )
                    tipo_recebimento_slug = (
                        recebimento.tipo_recebimento
                        if recebimento.tipo_recebimento in RecebimentoFornecedor.TIPOS_VALIDOS
                        else 'compra_revenda'
                    )
                    observacoes_mov = f'Recebimento #{recebimento.id} | Tipo: {tipo_recebimento_label}'
                    if item.lote:
                        observacoes_mov += f' | Lote: {item.lote}'
                    if item.validade:
                        observacoes_mov += f' | Validade: {item.validade.strftime("%d/%m/%Y")}'
                    if item.qtd_avaria:
                        observacoes_mov += f' | Avaria: {item.qtd_avaria}'

                    movimentacao = Movimentacao(
                        produto_id=item.produto_id,
                        fornecedor_id=recebimento.fornecedor_id,
                        endereco_destino_id=endereco_destino.id,
                        tipo=Movimentacao.TIPO_ENTRADA,
                        quantidade=quantidade_entrada,
                        info_nota=recebimento.info_nota,
                        motivo=f'recebimento_{tipo_recebimento_slug}',
                        observacoes=observacoes_mov,
                    )
                    db.session.add(movimentacao)

                recebimento.status = RecebimentoFornecedor.STATUS_CONCLUIDO
                recebimento.armazenado_em = datetime.utcnow()
                db.session.commit()
                flash('Armazenagem concluida. Estoque atualizado com sucesso.', 'success')
                return redirect(url_for('listar_recebimentos_fornecedor'))
            except AppError as e:
                db.session.rollback()
                flash(str(e), 'error')
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao concluir armazenagem: {str(e)}', 'error')

        return render_template(
            'estoque/recebimentos/armazenar_recebimento.html',
            recebimento=recebimento,
            enderecos_ativos=enderecos_ativos,
            status_labels=recebimento_status_labels,
            tipo_labels=recebimento_tipo_labels,
        )

    @app.route('/estoque/recebimentos/<int:recebimento_id>/cancelar', methods=['POST'])
    @require_role(*estoque_write_roles)
    def cancelar_recebimento_fornecedor(recebimento_id):
        recebimento = RecebimentoFornecedor.query.get_or_404(recebimento_id)
        try:
            if recebimento.status == RecebimentoFornecedor.STATUS_CONCLUIDO:
                flash('Recebimento concluido nao pode ser cancelado.', 'error')
                return redirect(url_for('listar_recebimentos_fornecedor'))
            if recebimento.status == RecebimentoFornecedor.STATUS_CANCELADO:
                flash('Recebimento ja esta cancelado.', 'info')
                return redirect(url_for('listar_recebimentos_fornecedor'))
            recebimento.status = RecebimentoFornecedor.STATUS_CANCELADO
            db.session.commit()
            flash('Recebimento cancelado com sucesso.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao cancelar recebimento: {str(e)}', 'error')
        return redirect(url_for('listar_recebimentos_fornecedor'))

    @app.route('/estoque/almoxarifado')
    @login_required
    def listar_almoxarifado():
        funcionario_logado = _funcionario_logado_estoque()
        page = max(request.args.get('page', 1, type=int), 1)
        per_page = min(max(request.args.get('per_page', 20, type=int), 1), 100)
        busca = (request.args.get('busca') or '').strip()
        destino_tipo = (request.args.get('destino_tipo') or '').strip().lower()
        funcionario_id = request.args.get('funcionario_id', type=int)
        setor = (request.args.get('setor') or '').strip()

        query = AlmoxarifadoAtribuicao.query.join(Produto, Produto.id == AlmoxarifadoAtribuicao.produto_id)
        ids_estoques = _estoques_permitidos_ids(funcionario_logado)
        if ids_estoques is not None:
            if not ids_estoques:
                query = query.filter(Produto.endereco_id.is_(None))
            else:
                query = query.filter(
                    db.or_(
                        Produto.endereco_id.is_(None),
                        Produto.endereco.has(EnderecoEstoque.estoque_id.in_(ids_estoques)),
                    )
                )
        if destino_tipo in AlmoxarifadoAtribuicao.DESTINOS_VALIDOS:
            query = query.filter(AlmoxarifadoAtribuicao.destino_tipo == destino_tipo)
        if funcionario_id:
            query = query.filter(AlmoxarifadoAtribuicao.funcionario_id == funcionario_id)
        if setor:
            query = query.filter(AlmoxarifadoAtribuicao.setor_destino == setor)
        if busca:
            termo = f'%{busca}%'
            query = query.outerjoin(Funcionario, Funcionario.id == AlmoxarifadoAtribuicao.funcionario_id).filter(
                db.or_(
                    Produto.nome.ilike(termo),
                    Produto.codigo.ilike(termo),
                    AlmoxarifadoAtribuicao.nome_destino.ilike(termo),
                    AlmoxarifadoAtribuicao.matricula_referencia.ilike(termo),
                    AlmoxarifadoAtribuicao.setor_destino.ilike(termo),
                    Funcionario.nome.ilike(termo),
                )
            ).distinct()

        atribuicoes = query.options(
            selectinload(AlmoxarifadoAtribuicao.produto),
            selectinload(AlmoxarifadoAtribuicao.funcionario),
            selectinload(AlmoxarifadoAtribuicao.registrado_por),
        ).order_by(AlmoxarifadoAtribuicao.criado_em.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False,
        )
        funcionarios_ativos = Funcionario.query.filter_by(ativo=True).options(
            load_only(Funcionario.id, Funcionario.nome, Funcionario.matricula)
        ).order_by(Funcionario.nome.asc()).all()

        return render_template(
            'estoque/almoxarifado/almoxarifado.html',
            atribuicoes=atribuicoes.items,
            pagination=atribuicoes,
            per_page=per_page,
            funcionarios_ativos=funcionarios_ativos,
            setores_disponiveis=_listar_setores_almoxarifado(),
            destino_labels=almoxarifado_destino_labels,
            filtros={
                'busca': busca,
                'destino_tipo': destino_tipo,
                'funcionario_id': funcionario_id,
                'setor': setor,
            },
            query_params=request.args.to_dict(),
        )

    @app.route('/estoque/almoxarifado/nova', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def nova_atribuicao_almoxarifado():
        funcionario_logado = _funcionario_logado_estoque()
        produtos = _produto_query_permitida(Produto.query.filter_by(ativo=True), funcionario_logado).order_by(Produto.nome.asc()).all()
        funcionarios_ativos = Funcionario.query.filter_by(ativo=True).options(
            load_only(
                Funcionario.id,
                Funcionario.nome,
                Funcionario.matricula,
                Funcionario.numero_cadastro,
                Funcionario.departamento,
            )
        ).order_by(Funcionario.nome.asc()).all()
        setores_disponiveis = _listar_setores_almoxarifado()

        if request.method == 'POST':
            try:
                produto_id = request.form.get('produto_id', type=int)
                quantidade = request.form.get('quantidade', type=int)
                destino_tipo = (request.form.get('destino_tipo') or '').strip().lower()
                setor_destino = (request.form.get('setor_destino') or '').strip() or None
                observacoes = (request.form.get('observacoes') or '').strip() or None
                funcionario_destino = None

                produto = Produto.query.get(produto_id) if produto_id else None
                if not produto or not produto.ativo:
                    flash('Selecione um produto valido para o almoxarifado.', 'error')
                    return redirect(url_for('nova_atribuicao_almoxarifado'))
                if not _produto_em_estoque_permitido(produto, funcionario_logado):
                    flash('Voce nao possui acesso ao estoque desse produto.', 'error')
                    return redirect(url_for('nova_atribuicao_almoxarifado'))
                if not quantidade or quantidade <= 0:
                    flash('Informe uma quantidade maior que zero.', 'error')
                    return redirect(url_for('nova_atribuicao_almoxarifado'))
                if destino_tipo not in AlmoxarifadoAtribuicao.DESTINOS_VALIDOS:
                    flash('Selecione um destino valido para a atribuicao.', 'error')
                    return redirect(url_for('nova_atribuicao_almoxarifado'))

                if destino_tipo == AlmoxarifadoAtribuicao.DESTINO_FUNCIONARIO:
                    funcionario_destino = _resolver_funcionario_por_matricula_ou_nome(
                        texto_busca=(request.form.get('funcionario_busca') or '').strip(),
                        funcionario_id=request.form.get('funcionario_destino_id', type=int),
                    )
                    if not funcionario_destino:
                        flash('Selecione um funcionario valido por matricula ou nome.', 'error')
                        return redirect(url_for('nova_atribuicao_almoxarifado'))
                else:
                    if not setor_destino:
                        flash('Informe o setor que recebera o produto.', 'error')
                        return redirect(url_for('nova_atribuicao_almoxarifado'))

                aplicar_movimentacao_estoque(produto, Movimentacao.TIPO_SAIDA, quantidade)

                nome_destino = funcionario_destino.nome if funcionario_destino else setor_destino
                matricula_referencia = funcionario_destino.matricula if funcionario_destino else None
                descricao_movimentacao = f'Almoxarifado | Destino: {nome_destino}'
                if matricula_referencia:
                    descricao_movimentacao += f' | Matricula: {matricula_referencia}'
                if observacoes:
                    descricao_movimentacao += f' | Obs: {observacoes}'

                db.session.add(
                    AlmoxarifadoAtribuicao(
                        produto_id=produto.id,
                        funcionario_id=(funcionario_destino.id if funcionario_destino else None),
                        registrado_por_id=(funcionario_logado.id if funcionario_logado else None),
                        destino_tipo=destino_tipo,
                        nome_destino=nome_destino,
                        setor_destino=setor_destino,
                        matricula_referencia=matricula_referencia,
                        quantidade=quantidade,
                        observacoes=observacoes,
                    )
                )
                db.session.add(
                    Movimentacao(
                        produto_id=produto.id,
                        endereco_origem_id=produto.endereco_id,
                        tipo=Movimentacao.TIPO_SAIDA,
                        quantidade=quantidade,
                        motivo=f'almoxarifado_{destino_tipo}',
                        observacoes=descricao_movimentacao,
                    )
                )
                db.session.commit()
                flash('Atribuicao registrada no almoxarifado com baixa de estoque.', 'success')
                return redirect(url_for('listar_almoxarifado'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao registrar atribuicao do almoxarifado: {str(e)}', 'error')

        return render_template(
            'estoque/almoxarifado/nova_atribuicao.html',
            produtos=produtos,
            funcionarios_ativos=funcionarios_ativos,
            setores_disponiveis=setores_disponiveis,
            destino_labels=almoxarifado_destino_labels,
        )

    @app.route('/enderecos-estoque')
    @login_required
    def listar_enderecos_estoque():
        funcionario_logado = _funcionario_logado_estoque()
        page = max(request.args.get('page', 1, type=int), 1)
        per_page = min(max(request.args.get('per_page', 25, type=int), 1), 100)
        estoque_id = request.args.get('estoque_id', type=int)
        setor_zona = (request.args.get('setor_zona') or '').strip().lower()
        busca = (request.args.get('busca') or '').strip()
        status = (request.args.get('status') or '').strip().lower()

        if estoque_id and not _carregar_estoque_permitido(estoque_id, funcionario_logado):
            flash('Você não possui acesso ao estoque selecionado.', 'warning')
            return redirect(url_for('listar_enderecos_estoque'))

        query = _endereco_query_permitida(funcionario_logado)
        if estoque_id:
            query = query.filter(EnderecoEstoque.estoque_id == estoque_id)
        if setor_zona in SETORES_ZONA_VALIDOS:
            query = query.filter(EnderecoEstoque.setor_zona == setor_zona)
        if busca:
            termo = f'%{busca}%'
            query = query.filter(
                db.or_(
                    EnderecoEstoque.nome.ilike(termo),
                    EnderecoEstoque.codigo_localizacao.ilike(termo),
                    EnderecoEstoque.loja_cd.ilike(termo),
                    EnderecoEstoque.setor_zona.ilike(termo),
                    EnderecoEstoque.tipo_produto_reservado.ilike(termo),
                    EnderecoEstoque.rua.ilike(termo),
                    EnderecoEstoque.bairro.ilike(termo),
                    EnderecoEstoque.cidade.ilike(termo),
                )
            )
        if status in STATUS_ENDERECO_VALIDOS:
            query = query.filter(EnderecoEstoque.status == status)
        elif status == 'ativo':
            query = query.filter(EnderecoEstoque.ativo.is_(True))
        elif status == 'inativo':
            query = query.filter(EnderecoEstoque.ativo.is_(False))

        pagination = query.options(
            load_only(
                EnderecoEstoque.id,
                EnderecoEstoque.estoque_id,
                EnderecoEstoque.nome,
                EnderecoEstoque.codigo_localizacao,
                EnderecoEstoque.loja_cd,
                EnderecoEstoque.setor_zona,
                EnderecoEstoque.tipo_area,
                EnderecoEstoque.status,
                EnderecoEstoque.ativo,
            ),
            selectinload(EnderecoEstoque.estoque).load_only(Estoque.id, Estoque.nome),
        ).order_by(EnderecoEstoque.nome.asc()).paginate(page=page, per_page=per_page, error_out=False)
        enderecos = pagination.items
        estoques = _estoque_query_permitida(funcionario_logado).order_by(Estoque.nome.asc()).all()
        enderecos_stats = {}
        ids_endereco = [endereco.id for endereco in enderecos]
        if ids_endereco:
            stats_raw = db.session.query(
                Produto.endereco_id.label('endereco_id'),
                db.func.count(Produto.id).label('produtos'),
                db.func.sum(Produto.quantidade_estoque).label('unidades'),
                db.func.sum(Produto.quantidade_estoque * Produto.preco_custo).label('valor_total'),
            ).filter(
                Produto.endereco_id.in_(ids_endereco)
            ).group_by(
                Produto.endereco_id
            ).all()
            enderecos_stats = {
                int(item.endereco_id): {
                    'produtos': int(item.produtos or 0),
                    'unidades': int(item.unidades or 0),
                    'valor_total': float(item.valor_total or 0.0),
                }
                for item in stats_raw
            }
        return render_template(
            'estoque/enderecos/enderecos.html',
            enderecos=enderecos,
            estoques=estoques,
            enderecos_stats=enderecos_stats,
            pagination=pagination,
            per_page=per_page,
            filtros={
                'estoque_id': estoque_id,
                'setor_zona': setor_zona,
                'busca': busca,
                'status': status,
            },
            **endereco_context,
        )

    @app.route('/enderecos-estoque/<int:endereco_id>/detalhes')
    @login_required
    def detalhes_endereco_estoque(endereco_id):
        funcionario_logado = _funcionario_logado_estoque()
        endereco = _carregar_endereco_permitido(endereco_id, funcionario_logado)
        if not endereco:
            flash('Você não possui acesso a este endereço.', 'danger')
            return redirect(url_for('listar_enderecos_estoque'))
        produtos = _produto_query_permitida(Produto.query.filter_by(endereco_id=endereco.id), funcionario_logado).order_by(Produto.nome.asc()).all()
        total_unidades = sum(int(produto.quantidade_estoque or 0) for produto in produtos)
        valor_total = sum(float(produto.quantidade_estoque or 0) * float(produto.preco_custo or 0) for produto in produtos)
        return render_template(
            'estoque/enderecos/detalhes_endereco.html',
            endereco=endereco,
            produtos=produtos,
            total_unidades=total_unidades,
            valor_total=valor_total,
        )

    @app.route('/enderecos-estoque/<int:endereco_id>/etiqueta')
    @login_required
    def imprimir_etiqueta_endereco_estoque(endereco_id):
        empresa = _obter_empresa_config_estoque()
        if not _emissao_etiqueta_endereco_ativa(empresa):
            flash('A emissao de etiquetas de enderecos de estoque esta desativada na configuracao da empresa.', 'warning')
            return redirect(url_for('listar_enderecos_estoque'))
        funcionario_logado = _funcionario_logado_estoque()
        endereco = _carregar_endereco_permitido(endereco_id, funcionario_logado)
        if not endereco:
            flash('Você não possui acesso a este endereço.', 'danger')
            return redirect(url_for('listar_enderecos_estoque'))
        return render_template(
            'estoque/enderecos/etiquetas_enderecos.html',
            empresa=empresa,
            enderecos=[endereco],
            titulo='Etiqueta de Endereco',
        )

    @app.route('/enderecos-estoque/etiquetas')
    @login_required
    def imprimir_etiquetas_enderecos_estoque():
        empresa = _obter_empresa_config_estoque()
        if not _emissao_etiqueta_endereco_ativa(empresa):
            flash('A emissao de etiquetas de enderecos de estoque esta desativada na configuracao da empresa.', 'warning')
            return redirect(url_for('listar_enderecos_estoque'))
        funcionario_logado = _funcionario_logado_estoque()
        estoque_id = request.args.get('estoque_id', type=int)
        if estoque_id and not _carregar_estoque_permitido(estoque_id, funcionario_logado):
            flash('Você não possui acesso ao estoque selecionado.', 'warning')
            return redirect(url_for('listar_enderecos_estoque'))
        query = _endereco_query_permitida(funcionario_logado)
        if estoque_id:
            query = query.filter(EnderecoEstoque.estoque_id == estoque_id)
        enderecos = query.filter(EnderecoEstoque.ativo.is_(True)).order_by(EnderecoEstoque.nome.asc()).all()
        if not enderecos:
            flash('Nenhum endereco ativo encontrado para imprimir etiquetas.', 'warning')
            return redirect(url_for('listar_enderecos_estoque', estoque_id=estoque_id or ''))
        return render_template(
            'estoque/enderecos/etiquetas_enderecos.html',
            empresa=empresa,
            enderecos=enderecos,
            titulo='Etiquetas de Enderecos',
        )

    @app.route('/estoques')
    @login_required
    def listar_estoques():
        funcionario_logado = _funcionario_logado_estoque()
        page = max(request.args.get('page', 1, type=int), 1)
        per_page = min(max(request.args.get('per_page', 20, type=int), 1), 100)
        busca = (request.args.get('busca') or '').strip()
        status = (request.args.get('status') or '').strip().lower()

        query = _estoque_query_permitida(funcionario_logado)
        if busca:
            termo = f'%{busca}%'
            query = query.filter(
                db.or_(
                    Estoque.nome.ilike(termo),
                    Estoque.codigo_filial.ilike(termo),
                    Estoque.descricao.ilike(termo),
                )
            )
        if status == 'ativo':
            query = query.filter(Estoque.ativo.is_(True))
        elif status == 'inativo':
            query = query.filter(Estoque.ativo.is_(False))

        pagination = query.order_by(Estoque.nome.asc()).paginate(page=page, per_page=per_page, error_out=False)
        estoques = pagination.items
        return render_template(
            'estoque/estoques/estoques.html',
            estoques=estoques,
            pagination=pagination,
            per_page=per_page,
            filtros={
                'busca': busca,
                'status': status,
            }
        )

    @app.route('/estoques/novo', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def novo_estoque():
        if request.method == 'POST':
            try:
                nome = (request.form.get('nome') or '').strip()
                codigo_filial = re.sub(r'[^A-Z0-9]+', '', (request.form.get('codigo_filial') or '').strip().upper()) or None
                descricao = (request.form.get('descricao') or '').strip() or None
                ativo = (request.form.get('ativo') == 'on')

                if not nome:
                    flash('Nome do estoque e obrigatorio.', 'error')
                    return redirect(url_for('novo_estoque'))
                if codigo_filial and Estoque.query.filter(db.func.lower(Estoque.codigo_filial) == codigo_filial.lower()).first():
                    flash('Codigo de filial ja utilizado por outro estoque.', 'error')
                    return redirect(url_for('novo_estoque'))

                estoque = Estoque(nome=nome, codigo_filial=codigo_filial, descricao=descricao, ativo=ativo)
                db.session.add(estoque)
                db.session.commit()
                if sincronizar_matriculas_funcionarios:
                    sincronizar_matriculas_funcionarios()
                flash(f'Estoque "{estoque.nome}" criado com sucesso!', 'success')
                return redirect(url_for('listar_estoques'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao criar estoque: {str(e)}', 'error')
        return render_template('estoque/estoques/novo_estoque.html')

    @app.route('/estoques/<int:estoque_id>/editar', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def editar_estoque(estoque_id):
        funcionario_logado = _funcionario_logado_estoque()
        estoque = _carregar_estoque_permitido(estoque_id, funcionario_logado)
        if not estoque:
            flash('Você não possui acesso a este estoque.', 'danger')
            return redirect(url_for('listar_estoques'))
        if request.method == 'POST':
            try:
                nome = (request.form.get('nome') or '').strip()
                codigo_filial = re.sub(r'[^A-Z0-9]+', '', (request.form.get('codigo_filial') or '').strip().upper()) or None
                descricao = (request.form.get('descricao') or '').strip() or None
                ativo = (request.form.get('ativo') == 'on')
                if not nome:
                    flash('Nome do estoque e obrigatorio.', 'error')
                    return redirect(url_for('editar_estoque', estoque_id=estoque.id))
                duplicado = Estoque.query.filter(
                    db.func.lower(Estoque.codigo_filial) == (codigo_filial.lower() if codigo_filial else ''),
                    Estoque.id != estoque.id,
                ).first() if codigo_filial else None
                if duplicado:
                    flash('Codigo de filial ja utilizado por outro estoque.', 'error')
                    return redirect(url_for('editar_estoque', estoque_id=estoque.id))

                estoque.nome = nome
                estoque.codigo_filial = codigo_filial
                estoque.descricao = descricao
                estoque.ativo = ativo
                db.session.commit()
                if sincronizar_matriculas_funcionarios:
                    sincronizar_matriculas_funcionarios()
                flash('Estoque atualizado com sucesso!', 'success')
                return redirect(url_for('listar_estoques'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao atualizar estoque: {str(e)}', 'error')
        return render_template('estoque/estoques/editar_estoque.html', estoque=estoque)

    @app.route('/estoques/<int:estoque_id>/deletar', methods=['POST'])
    @require_role(*estoque_write_roles)
    def deletar_estoque(estoque_id):
        funcionario_logado = _funcionario_logado_estoque()
        estoque = _carregar_estoque_permitido(estoque_id, funcionario_logado)
        if not estoque:
            flash('Você não possui acesso a este estoque.', 'danger')
            return redirect(url_for('listar_estoques'))
        try:
            if EnderecoEstoque.query.filter_by(estoque_id=estoque.id).count() > 0:
                flash('Nao e possivel excluir estoque com enderecos vinculados.', 'error')
                return redirect(url_for('listar_estoques'))
            if Funcionario.query.filter(
                db.or_(
                    Funcionario.estoque_principal_id == estoque.id,
                    Funcionario.estoques_permitidos.any(Estoque.id == estoque.id),
                )
            ).count() > 0:
                flash('Nao e possivel excluir estoque vinculado a colaboradores.', 'error')
                return redirect(url_for('listar_estoques'))
            db.session.delete(estoque)
            db.session.commit()
            flash('Estoque removido com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao remover estoque: {str(e)}', 'error')
        return redirect(url_for('listar_estoques'))

    @app.route('/enderecos-estoque/novo', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def novo_endereco_estoque():
        funcionario_logado = _funcionario_logado_estoque()
        estoques_ativos = _estoque_query_permitida(funcionario_logado).filter_by(ativo=True).order_by(Estoque.nome.asc()).all()
        categorias = Categoria.query.order_by(Categoria.nome.asc()).all()
        if request.method == 'POST':
            try:
                estoque_id = request.form.get('estoque_id', type=int) or None
                categoria_reservada_id = request.form.get('tipo_produto_reservado_categoria_id', type=int)
                nome = (request.form.get('nome') or '').strip()
                cadastrar_lote_rack = (request.form.get('cadastrar_lote_rack') == 'on')
                payload_validacao = request.form.copy()
                tipo_estrutura_form = (request.form.get('tipo_estrutura') or '').strip().lower()
                if cadastrar_lote_rack and tipo_estrutura_form == 'rack':
                    # Permite lote mesmo quando nivel/vao unitarios nao forem informados.
                    nivel_inicial_tmp = request.form.get('lote_nivel_inicial', type=int)
                    vao_inicial_tmp = request.form.get('lote_vao_inicial', type=int)
                    if not payload_validacao.get('nivel_prateleira') and nivel_inicial_tmp is not None:
                        payload_validacao['nivel_prateleira'] = str(nivel_inicial_tmp)
                    if not payload_validacao.get('posicao_slot') and vao_inicial_tmp is not None:
                        payload_validacao['posicao_slot'] = str(vao_inicial_tmp)

                comp = validar_endereco_supermercado_payload(payload_validacao)
                codigo_localizacao = comp['codigo_localizacao']
                if not nome:
                    flash('Nome do endereco e obrigatorio.', 'error')
                    return redirect(url_for('novo_endereco_estoque'))
                if not estoque_id:
                    flash('Selecione um estoque para o endereco.', 'error')
                    return redirect(url_for('novo_endereco_estoque'))
                estoque = _carregar_estoque_permitido(estoque_id, funcionario_logado, apenas_ativo=True)
                if not estoque:
                    flash('Estoque informado e invalido ou nao esta liberado para este colaborador.', 'error')
                    return redirect(url_for('novo_endereco_estoque'))
                categoria_reservada = None
                if categoria_reservada_id:
                    categoria_reservada = Categoria.query.get(categoria_reservada_id)
                    if not categoria_reservada:
                        flash('Categoria de produto reservado invalida.', 'error')
                        return redirect(url_for('novo_endereco_estoque'))
                tipo_produto_reservado_valor = (
                    categoria_reservada.nome
                    if categoria_reservada
                    else (comp.get('tipo_produto_reservado') or None)
                )

                # Cadastro em lote de endereco apenas para estrutura rack
                if cadastrar_lote_rack and comp['tipo_estrutura'] == 'rack':
                    nivel_inicial = request.form.get('lote_nivel_inicial', type=int)
                    nivel_final = request.form.get('lote_nivel_final', type=int)
                    vao_inicial = request.form.get('lote_vao_inicial', type=int)
                    vao_final = request.form.get('lote_vao_final', type=int)
                    if None in (nivel_inicial, nivel_final, vao_inicial, vao_final):
                        flash('Preencha nivel inicial/final e vao inicial/final para cadastro em lote.', 'error')
                        return redirect(url_for('novo_endereco_estoque'))
                    if nivel_inicial < 0 or vao_inicial < 1:
                        flash('Intervalo invalido. Nivel deve iniciar em 0+ e vao em 1+.', 'error')
                        return redirect(url_for('novo_endereco_estoque'))
                    if nivel_final < nivel_inicial or vao_final < vao_inicial:
                        flash('Intervalo invalido. Valores finais devem ser maiores ou iguais aos iniciais.', 'error')
                        return redirect(url_for('novo_endereco_estoque'))

                    combinacoes = []
                    for nivel in range(nivel_inicial, nivel_final + 1):
                        for vao in range(vao_inicial, vao_final + 1):
                            combinacoes.append((nivel, vao))
                    if not combinacoes:
                        flash('Nenhuma combinacao valida para gerar enderecos.', 'error')
                        return redirect(url_for('novo_endereco_estoque'))
                    if len(combinacoes) > 400:
                        flash('Limite excedido. Gere no maximo 400 enderecos por lote.', 'error')
                        return redirect(url_for('novo_endereco_estoque'))

                    codigos_gerados = []
                    nomes_gerados = []
                    for nivel, vao in combinacoes:
                        codigos_gerados.append(
                            gerar_codigo_localizacao_supermercado(
                                loja_cd=comp['loja_cd'],
                                setor_zona=comp['setor_zona'],
                                tipo_estrutura='rack',
                                rua_corredor=comp['rua_corredor'],
                                rack_estante=comp['coluna_baia'],
                                nivel_prateleira=str(nivel),
                                posicao_slot=str(vao),
                                lado=comp['lado'],
                            )
                        )
                        nomes_gerados.append(f'{nome} N{nivel:02d} V{vao:02d}')

                    duplicado_codigo = EnderecoEstoque.query.filter(
                        EnderecoEstoque.codigo_localizacao.in_(codigos_gerados)
                    ).first()
                    if duplicado_codigo:
                        flash(
                            f'Ja existe endereco com codigo "{duplicado_codigo.codigo_localizacao}". '
                            'Ajuste o intervalo informado.',
                            'error'
                        )
                        return redirect(url_for('novo_endereco_estoque'))

                    duplicado_nome = EnderecoEstoque.query.filter(
                        EnderecoEstoque.nome.in_(nomes_gerados)
                    ).first()
                    if duplicado_nome:
                        flash(
                            f'Ja existe endereco com nome "{duplicado_nome.nome}". '
                            'Use outro nome base para o lote.',
                            'error'
                        )
                        return redirect(url_for('novo_endereco_estoque'))

                    novos_enderecos = []
                    for idx, (nivel, vao) in enumerate(combinacoes):
                        novos_enderecos.append(
                            EnderecoEstoque(
                                estoque_id=estoque.id,
                                nome=nomes_gerados[idx],
                                codigo_localizacao=codigos_gerados[idx],
                                loja_cd=comp['loja_cd'],
                                setor_zona=comp['setor_zona'],
                                tipo_area=comp['tipo_area'],
                                status=comp['status'],
                                descricao=comp['descricao'],
                                observacoes=comp['observacoes'],
                                tipo_estrutura='rack',
                                codigo_armazem=comp['codigo_armazem'],
                                rua_corredor=comp['rua_corredor'],
                                coluna_baia=comp['coluna_baia'],
                                nivel_prateleira=f'{nivel:02d}',
                                posicao_slot=f'{vao:02d}',
                                lado=comp['lado'],
                                ponto_local=None,
                                permite_fracionado=comp['permite_fracionado'],
                                permite_mistura_sku=comp['permite_mistura_sku'],
                                permite_mistura_lote=comp['permite_mistura_lote'],
                                controle_validade=comp['controle_validade'],
                                temperatura=comp['temperatura'],
                                restricoes=comp['restricoes'],
                                capacidade_caixas=comp['capacidade_caixas'],
                                capacidade_fardos=comp['capacidade_fardos'],
                                capacidade_unidades=comp['capacidade_unidades'],
                                capacidade_pallets=comp['capacidade_pallets'],
                                peso_max_kg=comp['peso_max_kg'],
                                volume_max_m3=comp['volume_max_m3'],
                                prioridade_picking=comp['prioridade_picking'],
                                tipo_produto_reservado=tipo_produto_reservado_valor,
                                sku_produto=comp['sku_produto'],
                                data_alocacao=datetime.utcnow(),
                                tipo_endereco=comp['tipo_endereco'],
                                rua=(request.form.get('rua') or '').strip() or None,
                                numero=(request.form.get('numero') or '').strip() or None,
                                bairro=(request.form.get('bairro') or '').strip() or None,
                                cidade=(request.form.get('cidade') or '').strip() or None,
                                estado=((request.form.get('estado') or '').strip().upper() or None),
                                cep=(request.form.get('cep') or '').strip() or None,
                                complemento=(request.form.get('complemento') or '').strip() or None,
                                ativo=(comp['status'] != 'bloqueado')
                            )
                        )
                    db.session.add_all(novos_enderecos)
                    db.session.commit()
                    flash(f'{len(novos_enderecos)} enderecos cadastrados com sucesso para o rack/estante.', 'success')
                    return redirect(url_for('listar_enderecos_estoque'))

                if codigo_localizacao and EnderecoEstoque.query.filter_by(codigo_localizacao=codigo_localizacao).first():
                    flash(f'Codigo de localizacao "{codigo_localizacao}" ja cadastrado.', 'error')
                    return redirect(url_for('novo_endereco_estoque'))
                if comp['tipo_estrutura'] == 'rack':
                    duplicado = EnderecoEstoque.query.filter_by(
                        codigo_armazem=comp['codigo_armazem'],
                        rua_corredor=comp['rua_corredor'],
                        coluna_baia=comp['coluna_baia'],
                        nivel_prateleira=comp['nivel_prateleira'],
                        posicao_slot=comp['posicao_slot'],
                    ).first()
                    if duplicado:
                        flash('Ja existe um endereco com os mesmos componentes (armazem/corredor/baia/nivel/slot).', 'error')
                        return redirect(url_for('novo_endereco_estoque'))

                endereco = EnderecoEstoque(
                    estoque_id=estoque.id,
                    nome=nome,
                    codigo_localizacao=codigo_localizacao,
                    loja_cd=comp['loja_cd'],
                    setor_zona=comp['setor_zona'],
                    tipo_area=comp['tipo_area'],
                    status=comp['status'],
                    descricao=comp['descricao'],
                    observacoes=comp['observacoes'],
                    tipo_estrutura=comp['tipo_estrutura'],
                    codigo_armazem=comp['codigo_armazem'],
                    rua_corredor=comp['rua_corredor'],
                    coluna_baia=comp['coluna_baia'],
                    nivel_prateleira=comp['nivel_prateleira'],
                    posicao_slot=comp['posicao_slot'],
                    lado=comp['lado'],
                    ponto_local=comp['ponto_local'],
                    permite_fracionado=comp['permite_fracionado'],
                    permite_mistura_sku=comp['permite_mistura_sku'],
                    permite_mistura_lote=comp['permite_mistura_lote'],
                    controle_validade=comp['controle_validade'],
                    temperatura=comp['temperatura'],
                    restricoes=comp['restricoes'],
                    capacidade_caixas=comp['capacidade_caixas'],
                    capacidade_fardos=comp['capacidade_fardos'],
                    capacidade_unidades=comp['capacidade_unidades'],
                    capacidade_pallets=comp['capacidade_pallets'],
                    peso_max_kg=comp['peso_max_kg'],
                    volume_max_m3=comp['volume_max_m3'],
                    prioridade_picking=comp['prioridade_picking'],
                    tipo_produto_reservado=tipo_produto_reservado_valor,
                    sku_produto=comp['sku_produto'],
                    data_alocacao=datetime.utcnow(),
                    tipo_endereco=comp['tipo_endereco'],
                    rua=(request.form.get('rua') or '').strip() or None,
                    numero=(request.form.get('numero') or '').strip() or None,
                    bairro=(request.form.get('bairro') or '').strip() or None,
                    cidade=(request.form.get('cidade') or '').strip() or None,
                    estado=((request.form.get('estado') or '').strip().upper() or None),
                    cep=(request.form.get('cep') or '').strip() or None,
                    complemento=(request.form.get('complemento') or '').strip() or None,
                    ativo=(comp['status'] != 'bloqueado')
                )
                db.session.add(endereco)
                db.session.commit()
                flash(f'Endereco "{endereco.nome}" cadastrado com sucesso!', 'success')
                return redirect(url_for('listar_enderecos_estoque'))
            except ValueError as e:
                db.session.rollback()
                flash(str(e), 'error')
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao cadastrar endereco: {str(e)}', 'error')
        return render_template(
            'estoque/enderecos/novo_endereco.html',
            estoques=estoques_ativos,
            categorias=categorias,
            **endereco_context
        )

    @app.route('/enderecos-estoque/<int:endereco_id>/editar', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def editar_endereco_estoque(endereco_id):
        funcionario_logado = _funcionario_logado_estoque()
        endereco = _carregar_endereco_permitido(endereco_id, funcionario_logado)
        if not endereco:
            flash('Você não possui acesso a este endereço.', 'danger')
            return redirect(url_for('listar_enderecos_estoque'))
        estoques_ativos = _estoque_query_permitida(funcionario_logado).filter_by(ativo=True).order_by(Estoque.nome.asc()).all()
        categorias = Categoria.query.order_by(Categoria.nome.asc()).all()
        if request.method == 'POST':
            try:
                estoque_id = request.form.get('estoque_id', type=int) or None
                categoria_reservada_id = request.form.get('tipo_produto_reservado_categoria_id', type=int)
                nome = (request.form.get('nome') or '').strip()
                comp = validar_endereco_supermercado_payload(request.form)
                codigo_localizacao = comp['codigo_localizacao']
                if not nome:
                    flash('Nome do endereco e obrigatorio.', 'error')
                    return redirect(url_for('editar_endereco_estoque', endereco_id=endereco_id))
                if not estoque_id:
                    flash('Selecione um estoque para o endereco.', 'error')
                    return redirect(url_for('editar_endereco_estoque', endereco_id=endereco_id))
                estoque = _carregar_estoque_permitido(estoque_id, funcionario_logado, apenas_ativo=True)
                if not estoque:
                    flash('Estoque informado e invalido ou nao esta liberado para este colaborador.', 'error')
                    return redirect(url_for('editar_endereco_estoque', endereco_id=endereco_id))
                if not categoria_reservada_id:
                    flash('Selecione uma categoria para o tipo de produto reservado.', 'error')
                    return redirect(url_for('editar_endereco_estoque', endereco_id=endereco_id))
                categoria_reservada = Categoria.query.get(categoria_reservada_id)
                if not categoria_reservada:
                    flash('Categoria de produto reservado invalida.', 'error')
                    return redirect(url_for('editar_endereco_estoque', endereco_id=endereco_id))
                if codigo_localizacao:
                    endereco_existente = EnderecoEstoque.query.filter_by(codigo_localizacao=codigo_localizacao).first()
                    if endereco_existente and endereco_existente.id != endereco.id:
                        flash(f'Codigo de localizacao "{codigo_localizacao}" ja cadastrado.', 'error')
                        return redirect(url_for('editar_endereco_estoque', endereco_id=endereco_id))
                if comp['tipo_estrutura'] == 'rack':
                    duplicado = EnderecoEstoque.query.filter_by(
                        codigo_armazem=comp['codigo_armazem'],
                        rua_corredor=comp['rua_corredor'],
                        coluna_baia=comp['coluna_baia'],
                        nivel_prateleira=comp['nivel_prateleira'],
                        posicao_slot=comp['posicao_slot'],
                    ).first()
                    if duplicado and duplicado.id != endereco.id:
                        flash('Ja existe um endereco com os mesmos componentes (armazem/corredor/baia/nivel/slot).', 'error')
                        return redirect(url_for('editar_endereco_estoque', endereco_id=endereco_id))

                endereco.estoque_id = estoque.id
                endereco.nome = nome
                endereco.codigo_localizacao = codigo_localizacao
                endereco.loja_cd = comp['loja_cd']
                endereco.setor_zona = comp['setor_zona']
                endereco.tipo_area = comp['tipo_area']
                endereco.status = comp['status']
                endereco.descricao = comp['descricao']
                endereco.observacoes = comp['observacoes']
                endereco.tipo_estrutura = comp['tipo_estrutura']
                endereco.codigo_armazem = comp['codigo_armazem']
                endereco.rua_corredor = comp['rua_corredor']
                endereco.coluna_baia = comp['coluna_baia']
                endereco.nivel_prateleira = comp['nivel_prateleira']
                endereco.posicao_slot = comp['posicao_slot']
                endereco.lado = comp['lado']
                endereco.ponto_local = comp['ponto_local']
                endereco.permite_fracionado = comp['permite_fracionado']
                endereco.permite_mistura_sku = comp['permite_mistura_sku']
                endereco.permite_mistura_lote = comp['permite_mistura_lote']
                endereco.controle_validade = comp['controle_validade']
                endereco.temperatura = comp['temperatura']
                endereco.restricoes = comp['restricoes']
                endereco.capacidade_caixas = comp['capacidade_caixas']
                endereco.capacidade_fardos = comp['capacidade_fardos']
                endereco.capacidade_unidades = comp['capacidade_unidades']
                endereco.capacidade_pallets = comp['capacidade_pallets']
                endereco.peso_max_kg = comp['peso_max_kg']
                endereco.volume_max_m3 = comp['volume_max_m3']
                endereco.prioridade_picking = comp['prioridade_picking']
                endereco.tipo_produto_reservado = categoria_reservada.nome
                endereco.sku_produto = comp['sku_produto']
                endereco.tipo_endereco = comp['tipo_endereco']
                endereco.rua = (request.form.get('rua') or '').strip() or None
                endereco.numero = (request.form.get('numero') or '').strip() or None
                endereco.bairro = (request.form.get('bairro') or '').strip() or None
                endereco.cidade = (request.form.get('cidade') or '').strip() or None
                endereco.estado = ((request.form.get('estado') or '').strip().upper() or None)
                endereco.cep = (request.form.get('cep') or '').strip() or None
                endereco.complemento = (request.form.get('complemento') or '').strip() or None
                endereco.ativo = (comp['status'] != 'bloqueado')
                db.session.commit()
                flash('Endereco atualizado com sucesso!', 'success')
                return redirect(url_for('listar_enderecos_estoque'))
            except ValueError as e:
                db.session.rollback()
                flash(str(e), 'error')
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao atualizar endereco: {str(e)}', 'error')
        return render_template(
            'estoque/enderecos/editar_endereco.html',
            endereco=endereco,
            estoques=estoques_ativos,
            categorias=categorias,
            **endereco_context
        )

    @app.route('/enderecos-estoque/<int:endereco_id>/deletar', methods=['POST'])
    @require_role(*estoque_write_roles)
    def deletar_endereco_estoque(endereco_id):
        funcionario_logado = _funcionario_logado_estoque()
        endereco = _carregar_endereco_permitido(endereco_id, funcionario_logado)
        if not endereco:
            flash('Você não possui acesso a este endereço.', 'danger')
            return redirect(url_for('listar_enderecos_estoque'))
        try:
            Produto.query.filter_by(endereco_id=endereco.id).update({'endereco_id': None})
            db.session.delete(endereco)
            db.session.commit()
            flash('Endereco removido com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao remover endereco: {str(e)}', 'error')
        return redirect(url_for('listar_enderecos_estoque'))

    @app.route('/movimentacoes/rapido/<int:produto_id>', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def movimentacao_rapida(produto_id):
        funcionario_logado = _funcionario_logado_estoque()
        produto = Produto.query.get_or_404(produto_id)
        if not _produto_em_estoque_permitido(produto, funcionario_logado):
            flash('Você não possui acesso ao estoque deste produto.', 'danger')
            return redirect(url_for('listar_movimentacoes'))
        if request.method == 'POST':
            try:
                tipo = request.form.get('tipo')
                quantidade = int(request.form.get('quantidade'))
                fornecedor_id = request.form.get('fornecedor_id', type=int)
                recebimento_fornecedor = (request.form.get('recebimento_fornecedor') == 'on')

                if tipo not in {Movimentacao.TIPO_ENTRADA, Movimentacao.TIPO_SAIDA}:
                    flash('Tipo de movimentacao invalido.', 'error')
                    return redirect(url_for('movimentacao_rapida', produto_id=produto_id))

                aplicar_movimentacao_estoque(produto, tipo, quantidade)

                fornecedor = None
                if tipo == Movimentacao.TIPO_ENTRADA and fornecedor_id:
                    fornecedor = Fornecedor.query.get(fornecedor_id)
                    if not fornecedor:
                        flash('Fornecedor invalido.', 'error')
                        return redirect(url_for('movimentacao_rapida', produto_id=produto_id))
                if tipo == Movimentacao.TIPO_ENTRADA and recebimento_fornecedor and not fornecedor:
                    flash('No recebimento de fornecedor, selecione o fornecedor.', 'error')
                    return redirect(url_for('movimentacao_rapida', produto_id=produto_id))

                motivo = request.form.get('motivo')
                if tipo == Movimentacao.TIPO_ENTRADA and recebimento_fornecedor and not motivo:
                    motivo = 'recebimento_fornecedor'

                movimentacao = Movimentacao(
                    produto_id=produto_id,
                    fornecedor_id=(fornecedor.id if fornecedor else None),
                    tipo=tipo,
                    quantidade=quantidade,
                    valor_compra=request.form.get('valor_compra', type=float),
                    info_nota=request.form.get('info_nota'),
                    motivo=motivo,
                    observacoes=request.form.get('observacoes'),
                    endereco_origem_id=(produto.endereco_id if tipo == Movimentacao.TIPO_SAIDA else None),
                    endereco_destino_id=(produto.endereco_id if tipo == Movimentacao.TIPO_ENTRADA else None),
                )
                db.session.add(movimentacao)
                db.session.commit()
                flash('Movimentacao registrada com sucesso!', 'success')
                return redirect(url_for('listar_movimentacoes'))
            except AppError as e:
                db.session.rollback()
                flash(str(e), 'error')
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao registrar movimentacao: {str(e)}', 'error')

        return render_template(
            'estoque/movimentacoes/movimentacao_rapida.html',
            produto=produto,
            motivos_sugeridos=motivos_movimentacao_interna,
        )

    @app.route('/movimentacoes')
    @login_required
    def listar_movimentacoes():
        funcionario_logado = _funcionario_logado_estoque()
        page = max(request.args.get('page', 1, type=int), 1)
        per_page = min(max(request.args.get('per_page', 25, type=int), 1), 100)
        produto_id = request.args.get('produto_id', type=int)
        status = (request.args.get('status') or request.args.get('tipo') or '').strip().lower()
        busca = (request.args.get('busca') or '').strip()
        data_inicio_txt = (request.args.get('data_inicio') or '').strip()
        data_fim_txt = (request.args.get('data_fim') or '').strip()
        data_inicio = _parse_data_filtro(data_inicio_txt)
        data_fim = _parse_data_filtro(data_fim_txt)

        query = _movimentacao_query_permitida(Movimentacao.query, funcionario_logado).filter(
            Movimentacao.tipo.in_([Movimentacao.TIPO_ENTRADA, Movimentacao.TIPO_SAIDA])
        )
        if produto_id:
            query = query.filter_by(produto_id=produto_id)
        if status and status in [Movimentacao.TIPO_ENTRADA, Movimentacao.TIPO_SAIDA]:
            query = query.filter_by(tipo=status)
        if data_inicio:
            query = query.filter(Movimentacao.criado_em >= data_inicio)
        if data_fim:
            query = query.filter(Movimentacao.criado_em < (data_fim + timedelta(days=1)))
        if busca:
            termo = f'%{busca}%'
            query = query.join(Produto, Produto.id == Movimentacao.produto_id).outerjoin(
                Fornecedor, Fornecedor.id == Movimentacao.fornecedor_id
            ).filter(
                db.or_(
                    Produto.nome.ilike(termo),
                    Produto.codigo.ilike(termo),
                    Movimentacao.motivo.ilike(termo),
                    Movimentacao.info_nota.ilike(termo),
                    Movimentacao.observacoes.ilike(termo),
                    Fornecedor.nome.ilike(termo),
                )
            )

        movimentacoes = query.options(
            load_only(
                Movimentacao.id,
                Movimentacao.produto_id,
                Movimentacao.fornecedor_id,
                Movimentacao.tipo,
                Movimentacao.quantidade,
                Movimentacao.valor_compra,
                Movimentacao.info_nota,
                Movimentacao.motivo,
                Movimentacao.observacoes,
                Movimentacao.criado_em,
            ),
            selectinload(Movimentacao.produto).load_only(
                Produto.id,
                Produto.nome,
                Produto.codigo,
                Produto.endereco_id,
            ),
            selectinload(Movimentacao.fornecedor).load_only(
                Fornecedor.id,
                Fornecedor.nome,
            )
        ).order_by(Movimentacao.criado_em.desc()).paginate(page=page, per_page=per_page, error_out=False)
        produtos = _produto_query_permitida(Produto.query, funcionario_logado).all()
        return render_template(
            'estoque/movimentacoes/movimentacoes.html',
            movimentacoes=movimentacoes.items,
            pagination=movimentacoes,
            per_page=per_page,
            produtos=produtos,
            produto_selecionado=produto_id,
            status_selecionado=status,
            busca=busca,
            data_inicio=data_inicio_txt,
            data_fim=data_fim_txt,
            query_params=request.args.to_dict()
        )

    @app.route('/movimentacoes/nova', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def nova_movimentacao():
        funcionario_logado = _funcionario_logado_estoque()
        if request.method == 'POST':
            try:
                produto_id = int(request.form.get('produto_id'))
                tipo = request.form.get('tipo')
                quantidade = int(request.form.get('quantidade'))
                fornecedor_id = request.form.get('fornecedor_id', type=int)
                recebimento_fornecedor = (request.form.get('recebimento_fornecedor') == 'on')

                if tipo not in {Movimentacao.TIPO_ENTRADA, Movimentacao.TIPO_SAIDA}:
                    flash('Tipo de movimentacao invalido.', 'error')
                    return redirect(url_for('nova_movimentacao'))

                produto = Produto.query.get(produto_id)
                if not produto:
                    flash('Produto nao encontrado', 'error')
                    return redirect(url_for('nova_movimentacao'))
                if not _produto_em_estoque_permitido(produto, funcionario_logado):
                    flash('Você não possui acesso ao estoque deste produto.', 'danger')
                    return redirect(url_for('nova_movimentacao'))

                aplicar_movimentacao_estoque(produto, tipo, quantidade)

                fornecedor = None
                if tipo == Movimentacao.TIPO_ENTRADA and fornecedor_id:
                    fornecedor = Fornecedor.query.get(fornecedor_id)
                    if not fornecedor:
                        flash('Fornecedor invalido.', 'error')
                        return redirect(url_for('nova_movimentacao'))
                if tipo == Movimentacao.TIPO_ENTRADA and recebimento_fornecedor and not fornecedor:
                    flash('No recebimento de fornecedor, selecione o fornecedor.', 'error')
                    return redirect(url_for('nova_movimentacao'))

                motivo = request.form.get('motivo')
                if tipo == Movimentacao.TIPO_ENTRADA and recebimento_fornecedor and not motivo:
                    motivo = 'recebimento_fornecedor'

                movimentacao = Movimentacao(
                    produto_id=produto_id,
                    fornecedor_id=(fornecedor.id if fornecedor else None),
                    tipo=tipo,
                    quantidade=quantidade,
                    valor_compra=request.form.get('valor_compra', type=float),
                    info_nota=request.form.get('info_nota'),
                    motivo=motivo,
                    observacoes=request.form.get('observacoes'),
                    endereco_origem_id=(produto.endereco_id if tipo == Movimentacao.TIPO_SAIDA else None),
                    endereco_destino_id=(produto.endereco_id if tipo == Movimentacao.TIPO_ENTRADA else None),
                )
                db.session.add(movimentacao)
                db.session.commit()
                flash('Movimentacao registrada com sucesso!', 'success')
                return redirect(url_for('listar_movimentacoes'))
            except AppError as e:
                db.session.rollback()
                flash(str(e), 'error')
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao registrar movimentacao: {str(e)}', 'error')

        produtos = _produto_query_permitida(Produto.query.filter_by(ativo=True), funcionario_logado).all()
        return render_template(
            'estoque/movimentacoes/nova_movimentacao.html',
            produtos=produtos,
            motivos_sugeridos=motivos_movimentacao_interna,
        )

    @app.route('/movimentacoes/transferencias')
    @login_required
    def listar_transferencias_estoque():
        funcionario_logado = _funcionario_logado_estoque()
        page = max(request.args.get('page', 1, type=int), 1)
        per_page = min(max(request.args.get('per_page', 25, type=int), 1), 100)
        produto_id = request.args.get('produto_id', type=int)
        busca = (request.args.get('busca') or '').strip()
        data_inicio_txt = (request.args.get('data_inicio') or '').strip()
        data_fim_txt = (request.args.get('data_fim') or '').strip()
        data_inicio = _parse_data_filtro(data_inicio_txt)
        data_fim = _parse_data_filtro(data_fim_txt)

        query = _movimentacao_query_permitida(Movimentacao.query, funcionario_logado).filter(
            Movimentacao.tipo == Movimentacao.TIPO_TRANSFERENCIA
        )
        if produto_id:
            query = query.filter(Movimentacao.produto_id == produto_id)
        if data_inicio:
            query = query.filter(Movimentacao.criado_em >= data_inicio)
        if data_fim:
            query = query.filter(Movimentacao.criado_em < (data_fim + timedelta(days=1)))
        if busca:
            termo = f'%{busca}%'
            query = query.join(Produto, Produto.id == Movimentacao.produto_id).filter(
                db.or_(
                    Produto.nome.ilike(termo),
                    Produto.codigo.ilike(termo),
                    Movimentacao.motivo.ilike(termo),
                    Movimentacao.observacoes.ilike(termo),
                )
            )

        transferencias = query.options(
            selectinload(Movimentacao.produto),
            selectinload(Movimentacao.endereco_origem).selectinload(EnderecoEstoque.estoque),
            selectinload(Movimentacao.endereco_destino).selectinload(EnderecoEstoque.estoque),
        ).order_by(Movimentacao.criado_em.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False,
        )
        produtos = _produto_query_permitida(Produto.query, funcionario_logado).order_by(Produto.nome.asc()).all()
        return render_template(
            'estoque/movimentacoes/transferencias.html',
            transferencias=transferencias.items,
            pagination=transferencias,
            per_page=per_page,
            produtos=produtos,
            produto_selecionado=produto_id,
            busca=busca,
            data_inicio=data_inicio_txt,
            data_fim=data_fim_txt,
            query_params=request.args.to_dict(),
        )

    @app.route('/movimentacoes/transferencia', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def transferir_armazenamento():
        funcionario_logado = _funcionario_logado_estoque()
        if request.method == 'POST':
            try:
                produto_id = request.form.get('produto_id', type=int)
                endereco_destino_id = request.form.get('endereco_destino_id', type=int)
                motivo = (request.form.get('motivo') or '').strip() or 'transferencia_armazenamento'
                observacoes = (request.form.get('observacoes') or '').strip() or None

                produto = Produto.query.get(produto_id)
                if not produto:
                    flash('Produto nao encontrado.', 'error')
                    return redirect(url_for('transferir_armazenamento'))
                if not _produto_em_estoque_permitido(produto, funcionario_logado):
                    flash('Você não possui acesso ao estoque deste produto.', 'danger')
                    return redirect(url_for('transferir_armazenamento'))
                if not produto.endereco_id:
                    flash('Produto sem endereco de origem para transferencia.', 'error')
                    return redirect(url_for('transferir_armazenamento'))

                endereco_origem = _carregar_endereco_permitido(produto.endereco_id, funcionario_logado)
                endereco_destino = _carregar_endereco_permitido(endereco_destino_id, funcionario_logado, apenas_ativo=True)
                if not endereco_destino:
                    flash('Endereco de destino invalido.', 'error')
                    return redirect(url_for('transferir_armazenamento'))
                if not endereco_origem:
                    flash('Origem da transferencia nao localizada.', 'error')
                    return redirect(url_for('transferir_armazenamento'))
                if endereco_origem and endereco_origem.id == endereco_destino.id:
                    flash('Origem e destino nao podem ser iguais.', 'error')
                    return redirect(url_for('transferir_armazenamento'))
                if (
                    endereco_origem.estoque_id
                    and endereco_destino.estoque_id
                    and endereco_origem.estoque_id == endereco_destino.estoque_id
                ):
                    flash(
                        'Esta tela e exclusiva para transferencias entre lojas/CDs. '
                        'Para ajustes internos use Entradas e Saidas Internas ou Enderecos Inteligentes.',
                        'warning'
                    )
                    return redirect(url_for('transferir_armazenamento'))

                produto.endereco_id = endereco_destino.id
                movimentacao = Movimentacao(
                    produto_id=produto.id,
                    tipo=Movimentacao.TIPO_TRANSFERENCIA,
                    quantidade=max(int(produto.quantidade_estoque or 0), 0),
                    motivo=motivo,
                    observacoes=observacoes,
                    endereco_origem_id=(endereco_origem.id if endereco_origem else None),
                    endereco_destino_id=endereco_destino.id,
                )
                db.session.add(movimentacao)
                db.session.commit()
                flash(
                    f'Transferencia concluida: produto "{produto.nome}" movido para "{endereco_destino.nome}".',
                    'success'
                )
                return redirect(url_for('listar_transferencias_estoque'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao transferir armazenamento: {str(e)}', 'error')

        produtos = _produto_query_permitida(
            Produto.query.options(
                selectinload(Produto.endereco).selectinload(EnderecoEstoque.estoque),
                selectinload(Produto.categoria),
            ).filter(
                Produto.ativo.is_(True),
                Produto.endereco_id.isnot(None)
            ),
            funcionario_logado,
        ).order_by(Produto.nome.asc()).all()
        enderecos = _endereco_query_permitida(funcionario_logado).options(
            selectinload(EnderecoEstoque.estoque),
        ).filter_by(ativo=True).order_by(EnderecoEstoque.nome.asc()).all()
        return render_template(
            'estoque/movimentacoes/transferencia_armazenamento.html',
            produtos=produtos,
            enderecos=enderecos,
            motivos_sugeridos=motivos_transferencia,
        )

    @app.route('/api/estoque/analytics')
    @login_required
    def analytics_estoque_api():
        funcionario_logado = _funcionario_logado_estoque()
        periodo = request.args.get('periodo', type=int) or 30
        if periodo not in {7, 30, 90}:
            periodo = 30
        cache = extensions.cache
        funcionario_id = getattr(funcionario_logado, 'id', 'anon')
        cache_key = f'analytics:estoque:{funcionario_id}:{periodo}'
        if cache is not None:
            cached_payload = cache.get(cache_key)
            if cached_payload is not None:
                return jsonify(cached_payload)

        data_limite = datetime.utcnow() - timedelta(days=periodo)
        movimentos_raw = _movimentacao_query_permitida(db.session.query(
            db.func.date(Movimentacao.criado_em).label('dia'),
            Movimentacao.tipo.label('tipo'),
            db.func.sum(Movimentacao.quantidade).label('quantidade')
        ), funcionario_logado).filter(
            Movimentacao.criado_em >= data_limite
        ).group_by(
            db.func.date(Movimentacao.criado_em),
            Movimentacao.tipo
        ).order_by(db.func.date(Movimentacao.criado_em).asc()).all()

        entradas_por_dia = {}
        saidas_por_dia = {}
        for item in movimentos_raw:
            dia = str(item.dia)
            qtd = int(item.quantidade or 0)
            if item.tipo == Movimentacao.TIPO_ENTRADA:
                entradas_por_dia[dia] = entradas_por_dia.get(dia, 0) + qtd
            elif item.tipo == Movimentacao.TIPO_SAIDA:
                saidas_por_dia[dia] = saidas_por_dia.get(dia, 0) + qtd

        dias = []
        for i in range(periodo):
            dia = (datetime.utcnow() - timedelta(days=(periodo - i - 1))).date()
            key = str(dia)
            dias.append({
                'dia': key,
                'entradas': entradas_por_dia.get(key, 0),
                'saidas': saidas_por_dia.get(key, 0),
            })

        valor_categoria_raw = _produto_query_permitida(db.session.query(
            Categoria.nome.label('categoria_nome'),
            db.func.sum(Produto.quantidade_estoque * Produto.preco_custo).label('valor_total')
        ).join(Produto, Produto.categoria_id == Categoria.id), funcionario_logado).filter(
            Produto.ativo == True
        ).group_by(Categoria.id, Categoria.nome).order_by(db.desc('valor_total')).all()

        payload = {
            'success': True,
            'message': 'Analytics de estoque carregado com sucesso.',
            'data': {
                'periodo_dias': periodo,
                'movimentacao_diaria': dias,
                'valor_por_categoria': [
                    {
                        'categoria': item.categoria_nome,
                        'valor_total': float(item.valor_total or 0)
                    }
                    for item in valor_categoria_raw
                ],
                'produtos_em_falta': _produto_query_permitida(Produto.query, funcionario_logado).filter(
                    Produto.quantidade_estoque < Produto.quantidade_minima,
                    Produto.ativo == True
                ).count(),
                'produtos_sem_estoque': _produto_query_permitida(Produto.query, funcionario_logado).filter(
                    Produto.ativo == True,
                    Produto.quantidade_estoque <= 0
                ).count()
            }
        }
        if cache is not None:
            cache.set(cache_key, payload, timeout=120)
        return jsonify(payload)

    @app.route('/relatorios')
    @login_required
    def relatorios():
        empresa = _obter_empresa_config_estoque()
        funcionario_logado = _funcionario_logado_estoque()
        total_produtos = _produto_query_permitida(Produto.query, funcionario_logado).count()
        produtos_ativos = _produto_query_permitida(Produto.query, funcionario_logado).filter_by(ativo=True).count()
        produtos_inativos = _produto_query_permitida(Produto.query, funcionario_logado).filter_by(ativo=False).count()
        total_unidades = _produto_query_permitida(
            db.session.query(db.func.sum(Produto.quantidade_estoque)),
            funcionario_logado,
        ).scalar() or 0

        produtos_em_falta = _produto_query_permitida(Produto.query, funcionario_logado).filter(
            Produto.quantidade_estoque < Produto.quantidade_minima,
            Produto.ativo == True
        ).all()
        produtos_sem_estoque = _produto_query_permitida(Produto.query, funcionario_logado).filter(
            Produto.ativo == True,
            Produto.quantidade_estoque <= 0
        ).count()

        valor_total = _produto_query_permitida(db.session.query(
            db.func.sum(Produto.quantidade_estoque * Produto.preco_custo)
        ), funcionario_logado).scalar() or 0
        custo_medio_estoque = (valor_total / total_unidades) if total_unidades else 0

        produtos_maior_valor = _produto_query_permitida(db.session.query(
            Produto,
            (Produto.quantidade_estoque * Produto.preco_custo).label('valor_total')
        ), funcionario_logado).order_by(db.desc('valor_total')).limit(10).all()

        data_limite = datetime.utcnow() - timedelta(days=30)
        movimentacoes_mes = _movimentacao_query_permitida(Movimentacao.query, funcionario_logado).filter(Movimentacao.criado_em >= data_limite).count()
        entradas_mes = _movimentacao_query_permitida(Movimentacao.query, funcionario_logado).filter(
            Movimentacao.criado_em >= data_limite,
            Movimentacao.tipo == Movimentacao.TIPO_ENTRADA
        ).count()
        saidas_mes = _movimentacao_query_permitida(Movimentacao.query, funcionario_logado).filter(
            Movimentacao.criado_em >= data_limite,
            Movimentacao.tipo == Movimentacao.TIPO_SAIDA
        ).count()
        saldo_movimentacao_mes = int(entradas_mes or 0) - int(saidas_mes or 0)

        data_sem_giro = datetime.utcnow() - timedelta(days=60)
        produtos_sem_giro = _produto_query_permitida(Produto.query, funcionario_logado).filter(
            Produto.ativo == True,
            ~Produto.movimentacoes.any(Movimentacao.criado_em >= data_sem_giro)
        ).order_by(Produto.nome.asc()).limit(10).all()

        valor_por_categoria = _produto_query_permitida(db.session.query(
            Categoria.nome.label('categoria_nome'),
            db.func.sum(Produto.quantidade_estoque * Produto.preco_custo).label('valor_total'),
            db.func.sum(Produto.quantidade_estoque).label('qtd_total'),
            db.func.count(Produto.id).label('produtos')
        ).join(Produto, Produto.categoria_id == Categoria.id), funcionario_logado).filter(
            Produto.ativo == True
        ).group_by(Categoria.id, Categoria.nome).order_by(
            db.desc('valor_total')
        ).all()

        valor_por_endereco = _endereco_query_permitida(funcionario_logado).with_entities(
            EnderecoEstoque.nome.label('endereco_nome'),
            db.func.count(Produto.id).label('produtos'),
            db.func.sum(Produto.quantidade_estoque).label('qtd_total'),
            db.func.sum(Produto.quantidade_estoque * Produto.preco_custo).label('valor_total')
        ).join(Produto, Produto.endereco_id == EnderecoEstoque.id).filter(
            Produto.ativo == True
        ).group_by(EnderecoEstoque.id, EnderecoEstoque.nome).order_by(
            db.desc('valor_total')
        ).all()

        total_enderecos_ativos = _endereco_query_permitida(funcionario_logado).filter_by(ativo=True).count()
        enderecos_ocupados = _endereco_query_permitida(funcionario_logado).with_entities(EnderecoEstoque.id).join(
            Produto, Produto.endereco_id == EnderecoEstoque.id
        ).filter(
            EnderecoEstoque.ativo == True,
            Produto.ativo == True
        ).distinct().count()
        taxa_ocupacao_enderecos = (
            (enderecos_ocupados / total_enderecos_ativos) * 100.0
            if total_enderecos_ativos > 0 else 0.0
        )

        produtos_ativos_total = max(int(produtos_ativos or 0), 1)
        taxa_reposicao_necessaria = (len(produtos_em_falta) / produtos_ativos_total) * 100.0

        produtos_sem_endereco = _produto_query_permitida(Produto.query, funcionario_logado).filter(
            Produto.ativo == True,
            Produto.endereco_id.is_(None)
        ).count()
        produtos_fora_picking = _produto_query_permitida(Produto.query, funcionario_logado).filter(
            Produto.ativo == True,
            Produto.fora_picking.is_(True)
        ).count()
        produtos_risco_ruptura = _produto_query_permitida(Produto.query, funcionario_logado).filter(
            Produto.ativo == True,
            Produto.quantidade_minima > 0,
            Produto.quantidade_estoque <= 0
        ).count()

        risco_operacional_score = 0
        risco_operacional_score += min(int(taxa_reposicao_necessaria // 5), 8)
        risco_operacional_score += min(int((produtos_sem_endereco / produtos_ativos_total) * 10), 5)
        risco_operacional_score += min(int((produtos_fora_picking / produtos_ativos_total) * 10), 4)
        risco_operacional_score += min(int((produtos_risco_ruptura / produtos_ativos_total) * 12), 8)
        risco_operacional_score = min(risco_operacional_score, 25)

        dicas_estoque_inteligente = []
        if taxa_ocupacao_enderecos > 90:
            dicas_estoque_inteligente.append(
                'Ocupacao alta de enderecos. Priorize consolidacao de SKUs e abertura de novos slots de picking.'
            )
        elif taxa_ocupacao_enderecos < 55 and total_enderecos_ativos > 0:
            dicas_estoque_inteligente.append(
                'Ocupacao baixa de enderecos. Reorganize para reduzir deslocamento operacional e concentrar picking.'
            )

        if taxa_reposicao_necessaria >= 18:
            dicas_estoque_inteligente.append(
                'Reposicao elevada. Programe janelas fixas de reabastecimento e revise minimo por curva ABC.'
            )

        if produtos_sem_endereco > 0:
            dicas_estoque_inteligente.append(
                f'{produtos_sem_endereco} produto(s) sem endereco. Enderece para evitar ruptura e retrabalho no coletor.'
            )

        if produtos_fora_picking > 0:
            dicas_estoque_inteligente.append(
                f'{produtos_fora_picking} produto(s) fora de picking. Use "enderecos inteligentes" para baixar ao fluxo.'
            )

        if produtos_sem_giro:
            dicas_estoque_inteligente.append(
                'Existem produtos sem giro em 60 dias. Reavalie ponto de estocagem, promocao ou descontinuidade.'
            )

        if saldo_movimentacao_mes < 0:
            dicas_estoque_inteligente.append(
                'Saidas maiores que entradas no periodo. Reforce compras e agenda de recebimento para itens criticos.'
            )

        if not dicas_estoque_inteligente:
            dicas_estoque_inteligente.append(
                'Operacao equilibrada. Mantenha rotina de reposicao preventiva e revisao semanal por endereco.'
            )

        return render_template(
            'estoque/relatorios/relatorios.html',
            empresa=empresa,
            total_produtos=total_produtos,
            produtos_ativos=produtos_ativos,
            produtos_inativos=produtos_inativos,
            total_unidades=total_unidades,
            produtos_em_falta=produtos_em_falta,
            produtos_sem_estoque=produtos_sem_estoque,
            valor_total_estoque=f'{valor_total:.2f}',
            custo_medio_estoque=f'{custo_medio_estoque:.2f}',
            produtos_maior_valor=produtos_maior_valor,
            movimentacoes_mes=movimentacoes_mes,
            entradas_mes=entradas_mes,
            saidas_mes=saidas_mes,
            saldo_movimentacao_mes=saldo_movimentacao_mes,
            produtos_sem_giro=produtos_sem_giro,
            valor_por_categoria=valor_por_categoria,
            valor_por_endereco=valor_por_endereco,
            total_enderecos_ativos=total_enderecos_ativos,
            enderecos_ocupados=enderecos_ocupados,
            taxa_ocupacao_enderecos=taxa_ocupacao_enderecos,
            taxa_reposicao_necessaria=taxa_reposicao_necessaria,
            produtos_sem_endereco=produtos_sem_endereco,
            produtos_fora_picking=produtos_fora_picking,
            produtos_risco_ruptura=produtos_risco_ruptura,
            risco_operacional_score=risco_operacional_score,
            dicas_estoque_inteligente=dicas_estoque_inteligente,
        )


```


### Arquivo: `routes/public_routes.py`
- Linhas: 869
- Tamanho: 31.8 KB
- Status: completo

```python
import json
import re
import unicodedata
from urllib.parse import urlparse

from flask import Blueprint, abort, current_app, flash, redirect, render_template, request, session, url_for
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from sqlalchemy import or_

from app.services.utils_service import _normalizar_contato, _to_float
from app.utils.helpers import slugify
from app.utils.validators import validar_cep, validar_email, validar_telefone
from models import Categoria, ClientePublico, EmpresaConfig, Garcom, ItemPedido, Mesa, Pedido, Produto, db
from realtime import publish_alert
from app.utils.payment_config import default_payment_id, load_payment_options, payment_methods_map


CLIENTE_SESSION_KEY = 'qr_clientes'
SITE_CART_SESSION_KEY = 'site_carrinho'
SITE_CUSTOMER_SESSION_KEY = 'site_cliente_cadastro'
PEDIDO_CONFIRMACAO_SALT = 'pedido-site-confirmacao'


def _obter_empresa_config():
    empresa = EmpresaConfig.query.first()
    if not empresa:
        empresa = EmpresaConfig()
        db.session.add(empresa)
        db.session.commit()
    return empresa


def _serializer_confirmacao_pedido():
    return URLSafeTimedSerializer(current_app.config['SECRET_KEY'], salt=PEDIDO_CONFIRMACAO_SALT)


def _gerar_token_confirmacao_pedido(pedido_id):
    return _serializer_confirmacao_pedido().dumps({'pedido_id': int(pedido_id), 'origem': 'site'})


def _token_confirmacao_pedido_valido(pedido_id, token):
    if not token:
        return False
    try:
        payload = _serializer_confirmacao_pedido().loads(token, max_age=60 * 60 * 24 * 15)
    except (BadSignature, SignatureExpired):
        return False
    return payload.get('origem') == 'site' and int(payload.get('pedido_id') or 0) == int(pedido_id)


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


def _slugify(texto):
    return slugify(texto) or 'cliente'


def _atendimento_mesas_ativo():
    empresa = _obter_empresa_config()
    return empresa.atendimento_mesas_ativo is not False


def _ecommerce_site_ativo(empresa=None):
    empresa = empresa or _obter_empresa_config()
    return empresa.ecommerce_ativo is not False


def _redirecionar_loja_inativa():
    if session.get('funcionario_id'):
        return redirect(url_for('boas_vindas'))
    return redirect(url_for('login'))


def _status_legivel(status):
    labels = {
        'aberto': 'Aberto',
        'em_preparo': 'Em preparo',
        'entregue': 'Entregue',
        'fechado': 'Venda concluida',
        'cancelado': 'Cancelado'
    }
    return labels.get(status, status)


def _atribuir_garcom_automatico(empresa):
    if not empresa or empresa.atendimento_mesas_ativo is False or not empresa.distribuicao_ativa:
        return None

    garcons_ativos = Garcom.query.filter_by(ativo=True).order_by(Garcom.nome.asc()).all()
    if not garcons_ativos:
        return None

    modo = (empresa.modo_distribuicao_pedidos or 'round_robin').lower()
    if modo == 'manual':
        return None

    if modo == 'menos_pedidos':
        candidatos = []
        for garcom in garcons_ativos:
            em_andamento = Pedido.query.filter(
                Pedido.garcom_id == garcom.id,
                Pedido.status.in_(['aberto', 'em_preparo'])
            ).count()
            candidatos.append((em_andamento, garcom.id))
        candidatos.sort(key=lambda item: (item[0], item[1]))
        return candidatos[0][1] if candidatos else None

    ids = [g.id for g in garcons_ativos]
    if empresa.ultimo_garcom_id in ids:
        idx = ids.index(empresa.ultimo_garcom_id)
        proximo_idx = (idx + 1) % len(ids)
    else:
        proximo_idx = 0

    escolhido_id = ids[proximo_idx]
    empresa.ultimo_garcom_id = escolhido_id
    db.session.flush()
    return escolhido_id


def _obter_cliente_qr(token):
    clientes = session.get(CLIENTE_SESSION_KEY, {})
    return clientes.get(token)


def _remover_cliente_qr(token):
    clientes = dict(session.get(CLIENTE_SESSION_KEY, {}))
    if token in clientes:
        clientes.pop(token, None)
        session[CLIENTE_SESSION_KEY] = clientes
        session.modified = True


def _salvar_cliente_qr(token, mesa_id, nome, celular):
    clientes = dict(session.get(CLIENTE_SESSION_KEY, {}))
    clientes[token] = {
        'mesa_id': mesa_id,
        'nome': nome,
        'celular': celular,
        'slug': _slugify(nome)
    }
    session[CLIENTE_SESSION_KEY] = clientes
    session.modified = True


def _obter_cliente_por_mesa_slug(mesa, cliente_slug):
    clientes = session.get(CLIENTE_SESSION_KEY, {})
    mesa_id = mesa.id
    slug_informado = (cliente_slug or '').strip().lower()

    for token, dados in clientes.items():
        if not isinstance(dados, dict):
            continue
        if dados.get('mesa_id') != mesa_id:
            continue
        slug_salvo = (dados.get('slug') or _slugify(dados.get('nome') or '')).lower()
        if slug_salvo == slug_informado:
            dados = dict(dados)
            dados['token'] = token
            dados['slug'] = slug_salvo
            return dados
    return None


def _categorias_com_produtos():
    categorias = Categoria.query.order_by(Categoria.nome.asc()).all()
    resultado = []
    for categoria in categorias:
        produtos = Produto.query.filter_by(categoria_id=categoria.id, ativo=True).order_by(Produto.nome.asc()).all()
        if not produtos:
            continue
        resultado.append({
            'categoria': categoria,
            'produtos': produtos
        })
    return resultado


def _listar_pedidos_cliente(mesa_id, cliente):
    if not cliente:
        return []

    pedidos = Pedido.query.filter_by(
        mesa_id=mesa_id,
        origem='qr',
        cliente_nome=cliente.get('nome'),
        cliente_celular=cliente.get('celular')
    ).order_by(Pedido.criado_em.desc()).all()

    for pedido in pedidos:
        pedido.status_label = _status_legivel(pedido.status)
    return pedidos


def _normalizar_quantidade(valor, minimo=1, maximo=99, default=1):
    try:
        quantidade = int(valor)
    except (TypeError, ValueError):
        quantidade = int(default)
    if quantidade < minimo:
        return minimo
    if quantidade > maximo:
        return maximo
    return quantidade


def _obter_carrinho_site():
    carrinho_bruto = session.get(SITE_CART_SESSION_KEY, {})
    if not isinstance(carrinho_bruto, dict):
        carrinho_bruto = {}

    carrinho = {}
    for produto_id, quantidade in carrinho_bruto.items():
        try:
            produto_int = int(produto_id)
            quantidade_int = int(quantidade)
        except (TypeError, ValueError):
            continue
        if quantidade_int <= 0:
            continue
        carrinho[str(produto_int)] = min(quantidade_int, 99)

    if carrinho != carrinho_bruto:
        session[SITE_CART_SESSION_KEY] = carrinho
        session.modified = True

    return carrinho


def _salvar_carrinho_site(carrinho):
    normalizado = {}
    for produto_id, quantidade in (carrinho or {}).items():
        try:
            produto_int = int(produto_id)
            quantidade_int = int(quantidade)
        except (TypeError, ValueError):
            continue
        if quantidade_int <= 0:
            continue
        normalizado[str(produto_int)] = min(quantidade_int, 99)

    session[SITE_CART_SESSION_KEY] = normalizado
    session.modified = True


def _dados_cliente_padrao():
    return {
        'nome': '',
        'email': '',
        'celular': '',
        'cpf_cnpj': '',
        'cep': '',
        'endereco': '',
        'numero': '',
        'complemento': '',
        'bairro': '',
        'cidade': '',
        'estado': '',
        'referencia': '',
        'observacoes': '',
        'recebe_ofertas': False,
    }


def _obter_cliente_site_sessao():
    dados = session.get(SITE_CUSTOMER_SESSION_KEY, {})
    defaults = _dados_cliente_padrao()
    if not isinstance(dados, dict):
        return defaults

    resultado = dict(defaults)
    for chave in defaults:
        if chave not in dados:
            continue
        if chave == 'recebe_ofertas':
            resultado[chave] = bool(dados.get(chave))
        else:
            resultado[chave] = (dados.get(chave) or '').strip()
    return resultado


def _salvar_cliente_site_sessao(dados):
    defaults = _dados_cliente_padrao()
    payload = {}
    for chave in defaults:
        if chave == 'recebe_ofertas':
            payload[chave] = bool(dados.get(chave))
        else:
            payload[chave] = (dados.get(chave) or '').strip()
    session[SITE_CUSTOMER_SESSION_KEY] = payload
    session.modified = True


def _coletar_dados_cliente_form(form_data):
    dados = {
        'nome': (form_data.get('nome') or '').strip(),
        'email': (form_data.get('email') or '').strip().lower(),
        'celular': (form_data.get('celular') or '').strip(),
        'cpf_cnpj': (form_data.get('cpf_cnpj') or '').strip(),
        'cep': (form_data.get('cep') or '').strip(),
        'endereco': (form_data.get('endereco') or '').strip(),
        'numero': (form_data.get('numero') or '').strip(),
        'complemento': (form_data.get('complemento') or '').strip(),
        'bairro': (form_data.get('bairro') or '').strip(),
        'cidade': (form_data.get('cidade') or '').strip(),
        'estado': (form_data.get('estado') or '').strip().upper(),
        'referencia': (form_data.get('referencia') or '').strip(),
        'observacoes': (form_data.get('observacoes') or '').strip(),
        'recebe_ofertas': (form_data.get('recebe_ofertas') == 'on'),
    }

    erros = []
    if not dados['nome']:
        erros.append('Informe o nome completo.')
    if not validar_email(dados['email']):
        erros.append('Informe um e-mail valido.')
    if not validar_telefone(dados['celular']):
        erros.append('Informe um celular valido com DDD.')
    cep = validar_cep(dados['cep'])
    if not cep:
        erros.append('Informe o CEP.')
    elif cep == '__invalid__':
        erros.append('Informe um CEP valido.')
    if not dados['endereco']:
        erros.append('Informe o endereco.')
    if not dados['numero']:
        erros.append('Informe o numero do endereco.')
    if not dados['bairro']:
        erros.append('Informe o bairro.')
    if not dados['cidade']:
        erros.append('Informe a cidade.')
    if len(dados['estado']) != 2:
        erros.append('Informe o estado com 2 letras.')

    return dados, erros


def _upsert_cliente_publico(dados):
    filtros = []
    email = validar_email(dados.get('email'))
    celular = validar_telefone(dados.get('celular')) or _normalizar_contato(dados.get('celular'))
    cpf_cnpj = _normalizar_contato(dados.get('cpf_cnpj'))

    if email:
        filtros.append(db.func.lower(ClientePublico.email) == email)
    if celular:
        filtros.append(ClientePublico.celular == celular)
    if cpf_cnpj:
        filtros.append(ClientePublico.cpf_cnpj == cpf_cnpj)

    cliente = None
    if filtros:
        cliente = ClientePublico.query.filter(or_(*filtros)).order_by(ClientePublico.atualizado_em.desc()).first()

    if not cliente:
        cliente = ClientePublico()
        db.session.add(cliente)

    cliente.nome = dados.get('nome')
    cliente.email = email
    cliente.celular = celular or (dados.get('celular') or '').strip()
    cliente.cpf_cnpj = cpf_cnpj or None
    cliente.cep = dados.get('cep') or None
    cliente.endereco = dados.get('endereco') or None
    cliente.numero = dados.get('numero') or None
    cliente.complemento = dados.get('complemento') or None
    cliente.bairro = dados.get('bairro') or None
    cliente.cidade = dados.get('cidade') or None
    cliente.estado = dados.get('estado') or None
    cliente.referencia = dados.get('referencia') or None
    cliente.observacoes = dados.get('observacoes') or None
    cliente.recebe_ofertas = bool(dados.get('recebe_ofertas'))
    return cliente


def obter_resumo_carrinho_site():
    carrinho = _obter_carrinho_site()
    if not carrinho:
        return {'itens': [], 'subtotal': 0.0, 'quantidade_itens': 0}

    produto_ids = [int(produto_id) for produto_id in carrinho.keys()]
    produtos = Produto.query.filter(Produto.id.in_(produto_ids)).all()
    produtos_por_id = {produto.id: produto for produto in produtos}

    itens = []
    subtotal = 0.0
    mudou = False
    for produto_id, quantidade in list(carrinho.items()):
        produto = produtos_por_id.get(int(produto_id))
        if not produto or not produto.ativo or not produto.disponivel_para_venda:
            carrinho.pop(produto_id, None)
            mudou = True
            continue

        quantidade_int = _normalizar_quantidade(quantidade, minimo=1, maximo=99, default=1)
        if quantidade_int != quantidade:
            carrinho[produto_id] = quantidade_int
            mudou = True

        total_item = float(produto.preco_venda or 0.0) * quantidade_int
        subtotal += total_item
        itens.append({
            'produto': produto,
            'quantidade': quantidade_int,
            'total_item': total_item,
        })

    if mudou:
        _salvar_carrinho_site(carrinho)

    return {
        'itens': itens,
        'subtotal': round(subtotal, 2),
        'quantidade_itens': sum(item['quantidade'] for item in itens),
    }


def _coletar_pagamento_checkout(form_data, total_pedido, metodos_validos):
    metodo = (form_data.get('metodo_pagamento') or '').strip().lower()
    if metodo not in metodos_validos:
        raise ValueError('Selecione um metodo de pagamento valido.')

    total = float(total_pedido or 0.0)
    valor_pago = total
    troco = 0.0
    detalhes = {}
    if metodo == 'dinheiro':
        valor_recebido = _to_float(form_data.get('valor_recebido'), 0.0)
        if valor_recebido < total:
            raise ValueError('Valor recebido em dinheiro e menor que o total do pedido.')
        valor_pago = valor_recebido
        troco = max(valor_recebido - total, 0.0)
        detalhes['valor_recebido'] = round(valor_recebido, 2)

    return {
        'metodo': metodo,
        'metodo_label': metodos_validos[metodo],
        'valor_pago': round(valor_pago, 2),
        'troco': round(troco, 2),
        'detalhes': detalhes,
    }


def register_public_routes(app):
    bp = Blueprint('public', __name__)

    @bp.route('/cliente/cadastro', methods=['GET', 'POST'])
    def cadastro_cliente_site():
        empresa = _obter_empresa_config()
        if not _ecommerce_site_ativo(empresa):
            return _redirecionar_loja_inativa()
        resumo_carrinho = obter_resumo_carrinho_site()
        cliente_dados = _obter_cliente_site_sessao()
        proximo_seguro = _destino_interno_seguro(request.args.get('proximo'))

        if request.method == 'POST':
            cliente_dados, erros = _coletar_dados_cliente_form(request.form)
            if erros:
                for erro in erros:
                    flash(erro, 'warning')
            else:
                try:
                    _upsert_cliente_publico(cliente_dados)
                    db.session.commit()
                    _salvar_cliente_site_sessao(cliente_dados)
                    flash('Cadastro do cliente salvo com sucesso.', 'success')
                    proximo = (request.form.get('proximo') or '').strip()
                    if proximo:
                        return _redirect_interno_seguro(proximo, url_for('public.checkout_site'))
                    return redirect(url_for('public.checkout_site'))
                except Exception as e:
                    db.session.rollback()
                    flash(f'Nao foi possivel salvar o cadastro: {str(e)}', 'danger')

        return render_template(
            'public/cadastro_cliente.html',
            empresa=empresa,
            resumo_carrinho=resumo_carrinho,
            cliente_dados=cliente_dados,
            proximo_seguro=proximo_seguro,
        )

    @bp.route('/carrinho', methods=['GET'])
    def carrinho_site():
        empresa = _obter_empresa_config()
        if not _ecommerce_site_ativo(empresa):
            return _redirecionar_loja_inativa()
        resumo_carrinho = obter_resumo_carrinho_site()
        ids_no_carrinho = {item['produto'].id for item in resumo_carrinho['itens']}
        query_destaque = Produto.query.filter(
            Produto.ativo.is_(True),
            Produto.status_disponibilidade.in_(Produto.STATUS_DISPONIBILIDADE_ONLINE_EQUIVALENTES)
        )
        if ids_no_carrinho:
            query_destaque = query_destaque.filter(~Produto.id.in_(list(ids_no_carrinho)))
        produtos_destaque = query_destaque.order_by(Produto.atualizado_em.desc()).limit(6).all()

        return render_template(
            'public/carrinho.html',
            empresa=empresa,
            resumo_carrinho=resumo_carrinho,
            produtos_destaque=produtos_destaque,
        )

    @bp.route('/carrinho/adicionar', methods=['POST'])
    def adicionar_item_carrinho_site():
        if not _ecommerce_site_ativo():
            return _redirecionar_loja_inativa()
        destino = _destino_interno_seguro(request.form.get('next')) or _destino_interno_seguro(request.referrer) or url_for('index')
        produto_id = request.form.get('produto_id', type=int)
        quantidade = _normalizar_quantidade(request.form.get('quantidade'), minimo=1, maximo=99, default=1)

        produto = Produto.query.get(produto_id) if produto_id else None
        if not produto or not produto.ativo or not produto.disponivel_para_venda:
            flash('Produto indisponivel para venda no momento.', 'warning')
            return redirect(destino)

        carrinho = _obter_carrinho_site()
        qtd_atual = int(carrinho.get(str(produto.id), 0))
        carrinho[str(produto.id)] = min(qtd_atual + quantidade, 99)
        _salvar_carrinho_site(carrinho)
        flash(f'"{produto.nome}" adicionado ao carrinho.', 'success')
        return redirect(destino)

    @bp.route('/carrinho/atualizar', methods=['POST'])
    def atualizar_carrinho_site():
        if not _ecommerce_site_ativo():
            return _redirecionar_loja_inativa()
        carrinho = _obter_carrinho_site()
        if not carrinho:
            flash('Seu carrinho esta vazio.', 'warning')
            return redirect(url_for('public.carrinho_site'))

        for produto_id in list(carrinho.keys()):
            campo = f'quantidade_{produto_id}'
            if campo not in request.form:
                continue
            quantidade_raw = request.form.get(campo)
            try:
                quantidade = int(quantidade_raw)
            except (TypeError, ValueError):
                quantidade = 1

            if quantidade <= 0:
                carrinho.pop(produto_id, None)
            else:
                carrinho[produto_id] = _normalizar_quantidade(quantidade, minimo=1, maximo=99, default=1)

        _salvar_carrinho_site(carrinho)
        flash('Carrinho atualizado.', 'success')
        return redirect(url_for('public.carrinho_site'))

    @bp.route('/carrinho/remover', methods=['POST'])
    def remover_item_carrinho_site():
        if not _ecommerce_site_ativo():
            return _redirecionar_loja_inativa()
        produto_id = request.form.get('produto_id', type=int)
        carrinho = _obter_carrinho_site()
        if produto_id and str(produto_id) in carrinho:
            carrinho.pop(str(produto_id), None)
            _salvar_carrinho_site(carrinho)
            flash('Item removido do carrinho.', 'success')
        else:
            flash('Item nao encontrado no carrinho.', 'warning')
        return redirect(url_for('public.carrinho_site'))

    @bp.route('/checkout', methods=['GET', 'POST'])
    def checkout_site():
        empresa = _obter_empresa_config()
        if not _ecommerce_site_ativo(empresa):
            return _redirecionar_loja_inativa()
        resumo_carrinho = obter_resumo_carrinho_site()
        if not resumo_carrinho['itens']:
            flash('Adicione itens ao carrinho antes de finalizar.', 'warning')
            return redirect(url_for('public.carrinho_site'))

        payment_options = load_payment_options(empresa.pagamentos_ecommerce_json, 'ecommerce')
        payment_methods = payment_methods_map(empresa.pagamentos_ecommerce_json, 'ecommerce')
        default_payment = default_payment_id(empresa.pagamentos_ecommerce_json, 'ecommerce') or 'pix'
        cliente_dados = _obter_cliente_site_sessao()
        pagamento_selecionado = (request.form.get('metodo_pagamento') or default_payment).strip().lower() if request.method == 'POST' else default_payment
        valor_recebido = (request.form.get('valor_recebido') or '').strip() if request.method == 'POST' else ''

        if request.method == 'POST':
            cliente_dados, erros = _coletar_dados_cliente_form(request.form)
            if erros:
                for erro in erros:
                    flash(erro, 'warning')
            else:
                try:
                    pagamento = _coletar_pagamento_checkout(request.form, resumo_carrinho['subtotal'], payment_methods)
                    cliente_db = _upsert_cliente_publico(cliente_dados)
                    db.session.flush()

                    pedido = Pedido(
                        cliente_nome=cliente_dados.get('nome'),
                        cliente_celular=cliente_dados.get('celular'),
                        status='aberto',
                        origem='site',
                        total=float(resumo_carrinho['subtotal'] or 0.0),
                        metodo_pagamento=pagamento['metodo_label'],
                        valor_pago=pagamento['valor_pago'],
                        estoque_processado=False,
                        financeiro_processado=False,
                    )
                    db.session.add(pedido)
                    db.session.flush()

                    for item in resumo_carrinho['itens']:
                        produto = item['produto']
                        db.session.add(ItemPedido(
                            pedido_id=pedido.id,
                            produto_id=produto.id,
                            quantidade=item['quantidade'],
                            preco_unitario=produto.preco_venda
                        ))

                    pedido.observacoes = json.dumps({
                        'cliente_publico_id': cliente_db.id,
                        'cliente_cadastro': cliente_dados,
                        'pagamento': {
                            'metodo': pagamento['metodo'],
                            'metodo_label': pagamento['metodo_label'],
                            'troco': pagamento['troco'],
                            'detalhes': pagamento['detalhes'],
                        },
                        'origem_checkout': 'home_varejo',
                    }, ensure_ascii=False)

                    db.session.commit()
                    try:
                        publish_alert({
                            'pedido_id': pedido.id,
                            'origem': 'site',
                            'cliente_nome': pedido.cliente_nome,
                            'itens': [
                                {'produto': item['produto'].nome, 'quantidade': item['quantidade']}
                                for item in resumo_carrinho['itens']
                            ],
                            'criado_em': pedido.criado_em.isoformat() if pedido.criado_em else None
                        })
                    except Exception:
                        pass

                    _salvar_cliente_site_sessao(cliente_dados)
                    _salvar_carrinho_site({})
                    token_confirmacao = _gerar_token_confirmacao_pedido(pedido.id)

                    flash(f'Pedido #{pedido.id} recebido com sucesso.', 'success')
                    return redirect(url_for('public.pedido_confirmado_site', pedido_id=pedido.id, token=token_confirmacao))
                except ValueError as e:
                    db.session.rollback()
                    flash(str(e), 'warning')
                except Exception as e:
                    db.session.rollback()
                    flash(f'Nao foi possivel concluir seu pedido: {str(e)}', 'danger')

        return render_template(
            'public/checkout.html',
            empresa=empresa,
            resumo_carrinho=resumo_carrinho,
            cliente_dados=cliente_dados,
            payment_options=payment_options,
            pagamento_selecionado=pagamento_selecionado,
            valor_recebido=valor_recebido,
        )

    @bp.route('/pedido/<int:pedido_id>/confirmado', methods=['GET'])
    def pedido_confirmado_site(pedido_id):
        empresa = _obter_empresa_config()
        if not _ecommerce_site_ativo(empresa):
            return _redirecionar_loja_inativa()
        token = (request.args.get('token') or '').strip()
        if not _token_confirmacao_pedido_valido(pedido_id, token):
            abort(404)
        pedido = Pedido.query.filter_by(id=pedido_id, origem='site').first_or_404()
        detalhes = {}
        if pedido.observacoes:
            try:
                detalhes = json.loads(pedido.observacoes)
            except Exception:
                detalhes = {}

        return render_template(
            'public/pedido_confirmado.html',
            empresa=empresa,
            pedido=pedido,
            detalhes=detalhes,
            resumo_carrinho=obter_resumo_carrinho_site(),
        )

    @bp.route('/m/<token>', methods=['GET'])
    def cardapio_mesa(token):
        if not _atendimento_mesas_ativo():
            abort(404)
        mesa = Mesa.query.filter_by(qr_token=token).first_or_404()
        empresa = _obter_empresa_config()
        cliente = _obter_cliente_qr(token)

        if not cliente:
            return render_template('public/abrir_comanda.html', mesa=mesa, empresa=empresa)

        # Compatibilidade com sessoes antigas (sem mesa_id/slug) e dados incompletos.
        cliente_nome = (cliente.get('nome') or '').strip() if isinstance(cliente, dict) else ''
        cliente_celular = (cliente.get('celular') or '').strip() if isinstance(cliente, dict) else ''
        if not cliente_nome or not cliente_celular:
            _remover_cliente_qr(token)
            return render_template('public/abrir_comanda.html', mesa=mesa, empresa=empresa)

        if not isinstance(cliente, dict) or cliente.get('mesa_id') != mesa.id or not cliente.get('slug'):
            _salvar_cliente_qr(token, mesa.id, cliente_nome, cliente_celular)
            cliente = _obter_cliente_qr(token)

        return redirect(
            url_for(
                'public.comanda_cliente',
                mesa_numero=mesa.numero,
                cliente_slug=cliente.get('slug') or _slugify(cliente.get('nome') or '')
            )
        )

    @bp.route('/m/<token>/abrir-comanda', methods=['POST'])
    def abrir_comanda_qr(token):
        if not _atendimento_mesas_ativo():
            abort(404)
        mesa = Mesa.query.filter_by(qr_token=token).first_or_404()
        nome = (request.form.get('cliente_nome') or '').strip()
        celular = (request.form.get('cliente_celular') or '').strip()

        if not nome or not celular:
            flash('Informe seu nome e celular para abrir a comanda.', 'warning')
            empresa = _obter_empresa_config()
            return render_template('public/abrir_comanda.html', mesa=mesa, empresa=empresa)

        _salvar_cliente_qr(token, mesa.id, nome, celular)
        return redirect(url_for('public.comanda_cliente', mesa_numero=mesa.numero, cliente_slug=_slugify(nome)))

    @bp.route('/comanda/<mesa_numero>/<cliente_slug>', methods=['GET'])
    def comanda_cliente(mesa_numero, cliente_slug):
        if not _atendimento_mesas_ativo():
            abort(404)
        mesa = Mesa.query.filter_by(numero=mesa_numero).first_or_404()
        empresa = _obter_empresa_config()
        cliente = _obter_cliente_por_mesa_slug(mesa, cliente_slug)

        if not cliente:
            flash('Abra a comanda informando nome e celular.', 'warning')
            return redirect(url_for('public.cardapio_mesa', token=mesa.qr_token))

        slug_canonico = cliente.get('slug') or _slugify(cliente.get('nome') or '')
        if slug_canonico != (cliente_slug or '').lower():
            return redirect(url_for('public.comanda_cliente', mesa_numero=mesa.numero, cliente_slug=slug_canonico))

        qtd_max = (empresa.cardapio_qtd_maxima if empresa and empresa.cardapio_qtd_maxima else 20)
        if qtd_max <= 0:
            qtd_max = 20

        return render_template(
            'public/cardapio.html',
            mesa=mesa,
            empresa=empresa,
            qtd_max=qtd_max,
            cliente_nome=cliente.get('nome'),
            cliente_celular=cliente.get('celular'),
            cliente_slug=slug_canonico,
            categorias_cardapio=_categorias_com_produtos(),
            pedidos_cliente=_listar_pedidos_cliente(mesa.id, cliente)
        )

    @bp.route('/comanda/<mesa_numero>/<cliente_slug>/pedido', methods=['POST'])
    def enviar_pedido_qr(mesa_numero, cliente_slug):
        if not _atendimento_mesas_ativo():
            abort(404)
        mesa = Mesa.query.filter_by(numero=mesa_numero).first_or_404()
        empresa = _obter_empresa_config()
        cliente = _obter_cliente_por_mesa_slug(mesa, cliente_slug)

        if not cliente:
            flash('Abra a comanda informando nome e celular.', 'warning')
            return redirect(url_for('public.cardapio_mesa', token=mesa.qr_token))

        qtd_max = (empresa.cardapio_qtd_maxima if empresa and empresa.cardapio_qtd_maxima else 20)
        if qtd_max <= 0:
            qtd_max = 20

        itens = []
        for key, value in request.form.items():
            if not key.startswith('produto_'):
                continue
            try:
                produto_id = int(key.split('_')[1])
                quantidade = int(value)
            except Exception:
                continue
            if quantidade <= 0:
                continue
            if quantidade > qtd_max:
                quantidade = qtd_max
            itens.append((produto_id, quantidade))

        if not itens:
            flash('Nenhum item selecionado.', 'warning')
            return redirect(url_for('public.comanda_cliente', mesa_numero=mesa.numero, cliente_slug=cliente.get('slug')))

        pedido = Pedido(
            mesa_id=mesa.id,
            status='aberto',
            origem='qr',
            cliente_nome=cliente.get('nome'),
            cliente_celular=cliente.get('celular'),
            estoque_processado=False,
            financeiro_processado=False
        )
        db.session.add(pedido)

        pedido.garcom_id = _atribuir_garcom_automatico(empresa)

        total = 0
        itens_alerta = []
        for produto_id, quantidade in itens:
            prod = Produto.query.get(produto_id)
            if not prod:
                continue
            item = ItemPedido(
                pedido=pedido,
                produto_id=prod.id,
                quantidade=quantidade,
                preco_unitario=prod.preco_venda
            )
            total += quantidade * prod.preco_venda
            itens_alerta.append({'produto': prod.nome, 'quantidade': quantidade})
            db.session.add(item)
        pedido.total = total
        mesa.status = 'ocupada'
        db.session.commit()

        publish_alert({
            'mesa': mesa.numero,
            'pedido_id': pedido.id,
            'cliente_nome': pedido.cliente_nome,
            'garcom': (pedido.garcom.nome if pedido.garcom else None),
            'itens': itens_alerta,
            'criado_em': pedido.criado_em.isoformat()
        })

        flash(f'Pedido #{pedido.id} enviado com sucesso.', 'success')
        return redirect(url_for('public.comanda_cliente', mesa_numero=mesa.numero, cliente_slug=cliente.get('slug')))

    app.register_blueprint(bp)

```


### Arquivo: `routes/vendas_routes.py`
- Linhas: 2550
- Tamanho: 106.0 KB
- Status: completo

```python
from datetime import datetime
from datetime import time
from datetime import timedelta
import json
import secrets
import qrcode
from io import BytesIO
from flask import render_template, request, redirect, url_for, flash, session, Response, jsonify
from sqlalchemy.orm import selectinload

from models import db, Caixa, Mesa, Pedido, Produto, ItemPedido, Movimentacao, MovimentacaoCaixa, Funcionario, Garcom, EmpresaConfig, PermissaoAcesso
from realtime import publish_alert, sse_stream
from security import json_response
from app.constants import ENDPOINT_TO_PAGINA
from app.exceptions import AppError, BusinessRuleError, ValidationError
from app.services.financeiro_service import _build_payment_data
from app.services.pedido_service import (
    _aplicar_transicao_status as service_aplicar_transicao_status,
    _normalizar_item_payload,
    _processar_fechamento_pedido as service_processar_fechamento_pedido,
    _recalcular_total_pedido,
)
from app.services.utils_service import _to_float, _to_int
from app.utils.payment_config import default_payment_id, infer_payment_method_id, load_payment_options, payment_methods_map

ORDER_ALLOWED_TRANSITIONS = Pedido.TRANSICOES_PERMITIDAS
ORDER_IMMUTABLE_STATUSES = Pedido.STATUS_IMUTAVEIS
DELIVERY_SEPARATION_STATUSES = {Pedido.STATUS_ABERTO, Pedido.STATUS_EM_PREPARO, Pedido.STATUS_ENTREGUE}


def _obter_empresa_config():
    empresa = EmpresaConfig.query.first()
    if not empresa:
        empresa = EmpresaConfig()
        db.session.add(empresa)
        db.session.commit()
    return empresa


def _atendimento_mesas_ativo():
    empresa = _obter_empresa_config()
    return empresa.atendimento_mesas_ativo is not False


def _separacao_entrega_ativa(empresa=None):
    empresa = empresa or _obter_empresa_config()
    return empresa.separacao_entrega_ativa is not False


def _emissao_etiqueta_entrega_ativa(empresa=None):
    empresa = empresa or _obter_empresa_config()
    return _separacao_entrega_ativa(empresa) and empresa.emissao_etiqueta_entrega_ativa is not False


def _parse_horario_hhmm(valor):
    texto = (valor or '').strip()
    if not texto:
        return None
    try:
        hora_txt, minuto_txt = texto.split(':', 1)
        hora = int(hora_txt)
        minuto = int(minuto_txt)
    except (AttributeError, TypeError, ValueError):
        return None
    if hora < 0 or hora > 23 or minuto < 0 or minuto > 59:
        return None
    return time(hour=hora, minute=minuto)


def _origens_separacao_entrega(empresa=None):
    empresa = empresa or _obter_empresa_config()
    origens = ['site']
    if empresa.separacao_entrega_unir_vendas_off:
        origens.append('interno')
    return origens


def _pedido_pronto_para_roteirizacao(pedido):
    if not pedido:
        return False
    if not pedido.separacao_entrega_concluida:
        return False
    if pedido.status in {Pedido.STATUS_CANCELADO, Pedido.STATUS_FECHADO}:
        return False
    return True


def _referencia_pedido_roteirizacao(pedido):
    return (
        pedido.separacao_entrega_em
        or pedido.fechado_em
        or pedido.criado_em
    )


def _config_corte_roteirizacao(empresa, agora=None):
    agora = agora or datetime.utcnow()
    horario_txt = (
        empresa.entrega_horario_fechamento_roteirizacao
        if empresa and empresa.entrega_horario_fechamento_roteirizacao
        else ''
    )
    horario = _parse_horario_hhmm(horario_txt)
    if not horario:
        return {
            'ativo': False,
            'horario': None,
            'janela_aberta': True,
            'corte_do_dia': None,
            'proximo_ciclo_em': None,
        }

    corte_do_dia = agora.replace(
        hour=horario.hour,
        minute=horario.minute,
        second=0,
        microsecond=0,
    )
    janela_aberta = agora <= corte_do_dia
    proximo_ciclo_em = corte_do_dia if janela_aberta else (corte_do_dia + timedelta(days=1))
    return {
        'ativo': True,
        'horario': horario_txt,
        'janela_aberta': janela_aberta,
        'corte_do_dia': corte_do_dia,
        'proximo_ciclo_em': proximo_ciclo_em,
    }


def _separar_pedidos_por_corte_roteirizacao(pedidos, empresa, agora=None):
    corte = _config_corte_roteirizacao(empresa, agora=agora)
    pedidos_base = list(pedidos or [])
    if not corte['ativo']:
        return pedidos_base, [], corte

    liberados = []
    proximo_ciclo = []
    limite = corte['corte_do_dia']
    for pedido in pedidos_base:
        referencia = _referencia_pedido_roteirizacao(pedido)
        if referencia and referencia > limite:
            proximo_ciclo.append(pedido)
        else:
            liberados.append(pedido)
    return liberados, proximo_ciclo, corte


def _carregar_lista_config(valor_json):
    if not valor_json:
        return []
    try:
        dados = json.loads(valor_json)
    except Exception:
        return []
    if not isinstance(dados, list):
        return []
    itens = []
    for item in dados:
        if isinstance(item, dict):
            texto = (
                item.get('nome')
                or item.get('empresa')
                or item.get('descricao')
                or ''
            )
        else:
            texto = str(item or '').strip()
        if texto:
            itens.append(texto)
    return itens


def _normalizar_linhas_configuracao(texto):
    linhas = []
    vistos = set()
    for linha in (texto or '').splitlines():
        valor = linha.strip()
        if not valor:
            continue
        chave = valor.lower()
        if chave in vistos:
            continue
        vistos.add(chave)
        linhas.append(valor)
    return linhas


def _parse_veiculo_cadastrado(valor):
    texto = (valor or '').strip()
    if not texto:
        return None, None
    if '|' in texto:
        nome, placa = texto.split('|', 1)
        nome = nome.strip() or None
        placa = placa.strip().upper() or None
        return nome, placa
    return texto, None


def _carregar_veiculos_config(valor_json):
    if not valor_json:
        return []
    try:
        dados = json.loads(valor_json)
    except Exception:
        return []
    if not isinstance(dados, list):
        return []

    veiculos = []
    for item in dados:
        if isinstance(item, dict):
            nome = (item.get('nome') or '').strip()
            if not nome:
                continue
            veiculos.append({
                'nome': nome,
                'placa': (item.get('placa') or '').strip().upper() or None,
                'categoria': (item.get('categoria') or '').strip().lower() or 'geral',
                'tipo_entrega': (item.get('tipo_entrega') or '').strip().lower() or 'todos',
                'capacidade_pedidos': max(int(item.get('capacidade_pedidos') or 0), 0),
                'capacidade_kg': float(item.get('capacidade_kg') or 0) if item.get('capacidade_kg') not in (None, '') else None,
                'empresa': (item.get('empresa') or '').strip() or None,
                'ativo': item.get('ativo', True) is not False,
            })
            continue

        partes = [p.strip() for p in str(item or '').split('|')]
        nome = partes[0] if partes else ''
        if not nome:
            continue
        capacidade_pedidos = 0
        try:
            capacidade_pedidos = int(partes[4]) if len(partes) > 4 and partes[4] else 0
        except Exception:
            capacidade_pedidos = 0
        capacidade_kg = None
        try:
            capacidade_kg = float(partes[5]) if len(partes) > 5 and partes[5] else None
        except Exception:
            capacidade_kg = None
        veiculos.append({
            'nome': nome,
            'placa': partes[1].upper() if len(partes) > 1 and partes[1] else None,
            'categoria': (partes[2].lower() if len(partes) > 2 and partes[2] else 'geral'),
            'tipo_entrega': (partes[3].lower() if len(partes) > 3 and partes[3] else 'todos'),
            'capacidade_pedidos': capacidade_pedidos,
            'capacidade_kg': capacidade_kg,
            'empresa': partes[6] if len(partes) > 6 and partes[6] else None,
            'ativo': True,
        })
    return veiculos


def _serializar_veiculos_config_texto(veiculos):
    linhas = []
    for item in veiculos:
        linhas.append(' | '.join([
            item.get('nome') or '',
            item.get('placa') or '',
            item.get('categoria') or 'geral',
            item.get('tipo_entrega') or 'todos',
            str(item.get('capacidade_pedidos') or ''),
            str(item.get('capacidade_kg') or ''),
            item.get('empresa') or '',
        ]).strip())
    return '\n'.join(linhas)


def _normalizar_veiculos_texto(texto):
    veiculos = []
    vistos = set()
    for linha in (texto or '').splitlines():
        partes = [p.strip() for p in linha.split('|')]
        nome = partes[0] if partes else ''
        if not nome:
            continue
        chave = nome.lower(), (partes[1].upper() if len(partes) > 1 and partes[1] else '')
        if chave in vistos:
            continue
        vistos.add(chave)
        capacidade_pedidos = 0
        try:
            capacidade_pedidos = int(partes[4]) if len(partes) > 4 and partes[4] else 0
        except Exception:
            capacidade_pedidos = 0
        capacidade_kg = None
        try:
            capacidade_kg = float(partes[5]) if len(partes) > 5 and partes[5] else None
        except Exception:
            capacidade_kg = None
        veiculos.append({
            'nome': nome,
            'placa': partes[1].upper() if len(partes) > 1 and partes[1] else None,
            'categoria': (partes[2].lower() if len(partes) > 2 and partes[2] else 'geral'),
            'tipo_entrega': (partes[3].lower() if len(partes) > 3 and partes[3] else 'todos'),
            'capacidade_pedidos': capacidade_pedidos,
            'capacidade_kg': capacidade_kg,
            'empresa': partes[6] if len(partes) > 6 and partes[6] else None,
            'ativo': True,
        })
    return veiculos


def _carregar_regras_roteirizacao(empresa):
    regras = {
        'prefixo_rota': 'Rota',
        'tipo_entrega': 'todos',
        'modo_distribuicao': 'capacidade',
        'considerar_capacidade': True,
        'max_paradas_por_rota': 0,
        'somente_sem_rota': True,
    }
    if not empresa or not empresa.entrega_regras_roteirizacao_json:
        return regras
    try:
        dados = json.loads(empresa.entrega_regras_roteirizacao_json)
    except Exception:
        return regras
    if not isinstance(dados, dict):
        return regras
    regras.update({
        'prefixo_rota': (dados.get('prefixo_rota') or regras['prefixo_rota']).strip() or 'Rota',
        'tipo_entrega': (dados.get('tipo_entrega') or regras['tipo_entrega']).strip().lower() or 'todos',
        'modo_distribuicao': (dados.get('modo_distribuicao') or regras['modo_distribuicao']).strip().lower() or 'capacidade',
        'considerar_capacidade': bool(dados.get('considerar_capacidade', True)),
        'max_paradas_por_rota': max(int(dados.get('max_paradas_por_rota') or 0), 0),
        'somente_sem_rota': bool(dados.get('somente_sem_rota', True)),
    })
    return regras


def _regras_roteirizacao_do_form(request_obj, empresa):
    atuais = _carregar_regras_roteirizacao(empresa)
    return {
        'prefixo_rota': (request_obj.form.get('prefixo_rota') or atuais['prefixo_rota']).strip() or 'Rota',
        'tipo_entrega': (request_obj.form.get('tipo_entrega') or atuais['tipo_entrega']).strip().lower() or 'todos',
        'modo_distribuicao': (request_obj.form.get('modo_distribuicao') or atuais['modo_distribuicao']).strip().lower() or 'capacidade',
        'considerar_capacidade': request_obj.form.get('considerar_capacidade') == 'on',
        'max_paradas_por_rota': max(int(request_obj.form.get('max_paradas_por_rota') or 0), 0),
        'somente_sem_rota': request_obj.form.get('somente_sem_rota') == 'on',
    }


def _distribuir_pedidos_automaticamente(pedidos, veiculos, regras, empresa):
    if not pedidos:
        return 0

    pedidos_ordenados = sorted(pedidos, key=lambda p: (p.criado_em or datetime.utcnow(), p.id))
    tipo_entrega = regras.get('tipo_entrega') or 'todos'
    if tipo_entrega != 'todos':
        pedidos_ordenados = [p for p in pedidos_ordenados if (p.origem or '').strip().lower() == tipo_entrega]

    if regras.get('somente_sem_rota', True):
        pedidos_ordenados = [p for p in pedidos_ordenados if not (p.rota_entrega or '').strip()]

    if not pedidos_ordenados:
        return 0

    veiculos_ativos = [v for v in veiculos if v.get('ativo', True)]
    if tipo_entrega != 'todos':
        veiculos_ativos = [
            v for v in veiculos_ativos
            if (v.get('tipo_entrega') or 'todos') in {'todos', tipo_entrega}
        ]

    if not veiculos_ativos:
        veiculos_ativos = [{
            'nome': empresa.entrega_veiculo_padrao or 'Expedicao',
            'placa': None,
            'categoria': 'geral',
            'tipo_entrega': tipo_entrega,
            'capacidade_pedidos': 0,
            'capacidade_kg': None,
            'empresa': None,
            'ativo': True,
        }]

    modo = regras.get('modo_distribuicao') or 'capacidade'
    if modo == 'capacidade':
        veiculos_base = sorted(veiculos_ativos, key=lambda v: (-(v.get('capacidade_pedidos') or 0), v.get('nome') or ''))
    else:
        veiculos_base = list(veiculos_ativos)

    prefixo = regras.get('prefixo_rota') or 'Rota'
    max_paradas_regra = int(regras.get('max_paradas_por_rota') or 0)
    considerar_capacidade = bool(regras.get('considerar_capacidade'))
    alocados = 0
    cursor_pedido = 0
    rodada = 1

    while cursor_pedido < len(pedidos_ordenados):
        if modo == 'round_robin':
            iteracao_veiculos = veiculos_ativos
        else:
            iteracao_veiculos = veiculos_base

        for indice_veiculo, veiculo in enumerate(iteracao_veiculos, start=1):
            if cursor_pedido >= len(pedidos_ordenados):
                break
            limite = max_paradas_regra if max_paradas_regra > 0 else 0
            if considerar_capacidade and (veiculo.get('capacidade_pedidos') or 0) > 0:
                capacidade_veiculo = int(veiculo.get('capacidade_pedidos') or 0)
                limite = min(limite, capacidade_veiculo) if limite > 0 else capacidade_veiculo
            if limite <= 0:
                limite = len(pedidos_ordenados)

            rota_nome = f"{prefixo} {rodada}.{indice_veiculo} - {veiculo.get('nome') or 'Expedicao'}"
            ordem = 1
            while cursor_pedido < len(pedidos_ordenados) and ordem <= limite:
                pedido = pedidos_ordenados[cursor_pedido]
                pedido.rota_entrega = rota_nome
                pedido.ordem_rota = ordem
                pedido.local_saida = pedido.local_saida or empresa.entrega_local_saida_padrao
                pedido.veiculo_tipo = veiculo.get('nome') or empresa.entrega_veiculo_padrao
                pedido.veiculo_placa = veiculo.get('placa') or pedido.veiculo_placa
                pedido.motorista_nome = pedido.motorista_nome or empresa.entrega_motorista_padrao
                pedido.empresa_terceirizada = veiculo.get('empresa') or pedido.empresa_terceirizada
                ordem += 1
                cursor_pedido += 1
                alocados += 1
                if modo == 'round_robin':
                    break
        rodada += 1

    return alocados


def _resolver_etapa_expedicao(pedido):
    if not pedido.separacao_entrega_concluida:
        return 'separacao'
    if not pedido.etiqueta_entrega_emitida_em:
        return 'embalagem'
    if not pedido.saiu_para_entrega_em:
        return 'expedicao'
    if not pedido.entrega_concluida_em:
        return 'em_rota'
    return 'entregue'


def _pedido_na_fila_entrega(pedido, empresa=None):
    empresa = empresa or _obter_empresa_config()
    return (
        _separacao_entrega_ativa(empresa)
        and (pedido.origem or '').strip().lower() in _origens_separacao_entrega(empresa)
    )


def _visao_operacional_pedido(pedido, empresa=None):
    empresa = empresa or _obter_empresa_config()
    fila_entrega = _pedido_na_fila_entrega(pedido, empresa)
    possui_rota = bool((pedido.rota_entrega or '').strip())

    if pedido.status == Pedido.STATUS_CANCELADO:
        return {
            'chave': 'cancelado',
            'titulo': 'Cancelado',
            'descricao': 'Pedido fora da fila operacional ativa.',
            'proxima_acao': 'Sem acao operacional. Revise somente estorno, estoque ou registro interno se necessario.',
            'apos_concluir': 'Pedido permanece fora da fila de trabalho.',
        }

    if pedido.status == Pedido.STATUS_FECHADO:
        return {
            'chave': 'concluido',
            'titulo': 'Concluido',
            'descricao': 'Venda encerrada e fora da fila operacional.',
            'proxima_acao': 'Nenhuma acao pendente no pedido.',
            'apos_concluir': 'Fluxo finalizado.',
        }

    if fila_entrega and pedido.saiu_para_entrega_em and not pedido.entrega_concluida_em:
        return {
            'chave': 'em_rota',
            'titulo': 'Em rota',
            'descricao': 'Pedido ja saiu para entrega e aguarda confirmacao final.',
            'proxima_acao': 'Acompanhe o motorista, confirme a entrega e registre ocorrencias se houver.',
            'apos_concluir': 'Marque como entregue e encaminhe para fechamento da venda.',
        }

    if fila_entrega and pedido.entrega_concluida_em:
        return {
            'chave': 'fechamento',
            'titulo': 'Fechamento',
            'descricao': 'Entrega concluida, aguardando encerramento comercial e financeiro.',
            'proxima_acao': 'Conferir comprovantes, baixa financeira e fechar o pedido.',
            'apos_concluir': 'Pedido sai da fila operacional.',
        }

    if fila_entrega and pedido.separacao_entrega_concluida:
        if not possui_rota:
            proxima_acao = 'Defina rota, ordem de parada, local de saida e responsavel pelo transporte.'
        elif not pedido.etiqueta_entrega_emitida_em:
            proxima_acao = 'Emita a etiqueta, confira volumes e deixe o pedido pronto para despacho.'
        else:
            proxima_acao = 'Registre a saida para entrega e encaminhe o pedido ao motorista ou terceirizada.'

        return {
            'chave': 'roteirizacao',
            'titulo': 'Roteirizacao e despacho',
            'descricao': 'Pedido separado e aguardando roteirizacao final ou despacho.',
            'proxima_acao': proxima_acao,
            'apos_concluir': 'Pedido entra em acompanhamento de rota ate a confirmacao da entrega.',
        }

    if fila_entrega and pedido.status == Pedido.STATUS_ENTREGUE:
        return {
            'chave': 'separacao',
            'titulo': 'Separacao',
            'descricao': 'Pedido pronto comercialmente e aguardando separacao fisica.',
            'proxima_acao': 'Separar os itens, revisar quantidades, embalar e marcar o pedido como separado.',
            'apos_concluir': 'Envie para roteirizacao, etiqueta e despacho.',
        }

    if pedido.status == Pedido.STATUS_EM_PREPARO:
        return {
            'chave': 'preparo',
            'titulo': 'Preparo',
            'descricao': 'Pedido em producao, montagem ou conferencia operacional.',
            'proxima_acao': 'Produza, monte ou confira os itens conforme observacoes e disponibilidade.',
            'apos_concluir': (
                'Atualize para entregue e siga para separacao.'
                if fila_entrega
                else 'Entregue ao cliente e siga para fechamento da venda.'
            ),
        }

    if pedido.status == Pedido.STATUS_ABERTO:
        return {
            'chave': 'registro',
            'titulo': 'Registro e conferencia',
            'descricao': 'Pedido recem-lancado e aguardando validacao inicial.',
            'proxima_acao': 'Conferir itens, origem, pagamento e encaminhar para a equipe responsavel.',
            'apos_concluir': 'Mova o pedido para preparo.',
        }

    return {
        'chave': 'fechamento',
        'titulo': 'Fechamento',
        'descricao': 'Pedido aguarda revisao final para sair da fila.',
        'proxima_acao': 'Conferir documentacao, pagamento e concluir o encerramento.',
        'apos_concluir': 'Pedido sai da fila operacional.',
    }


def _acoes_rapidas_pedido(pedido, empresa=None, funcionario=None, paginas_permitidas=None):
    empresa = empresa or _obter_empresa_config()
    fila_entrega = _pedido_na_fila_entrega(pedido, empresa)
    pode_alterar_status = _usuario_tem_acesso_endpoint('alterar_status_pedido', funcionario=funcionario, paginas_permitidas=paginas_permitidas)
    pode_separar = _usuario_tem_acesso_endpoint('atualizar_separacao_entrega_pedido', funcionario=funcionario, paginas_permitidas=paginas_permitidas)
    pode_despachar = _usuario_tem_acesso_endpoint('atualizar_despacho_entrega', funcionario=funcionario, paginas_permitidas=paginas_permitidas)
    pode_ver_separacao = _usuario_tem_acesso_endpoint('listar_separacao_entrega', funcionario=funcionario, paginas_permitidas=paginas_permitidas)
    pode_ver_roteirizacao = _usuario_tem_acesso_endpoint('listar_roteirizacao_entrega', funcionario=funcionario, paginas_permitidas=paginas_permitidas)

    acoes = []

    def adicionar_formulario(tipo, label, valor, classe):
        acoes.append({
            'tipo': tipo,
            'label': label,
            'valor': valor,
            'classe': classe,
        })

    def adicionar_link(label, url, classe='btn-outline-primary'):
        acoes.append({
            'tipo': 'link',
            'label': label,
            'url': url,
            'classe': classe,
        })

    if pedido.status == Pedido.STATUS_ABERTO and pode_alterar_status:
        adicionar_formulario('status', 'Enviar p/ preparo', Pedido.STATUS_EM_PREPARO, 'btn-primary')
    elif pedido.status == Pedido.STATUS_EM_PREPARO and pode_alterar_status:
        adicionar_formulario('status', 'Marcar pronto', Pedido.STATUS_ENTREGUE, 'btn-warning')

    if fila_entrega and pedido.status == Pedido.STATUS_ENTREGUE and not pedido.separacao_entrega_concluida:
        if pode_separar:
            adicionar_formulario('separacao', 'Separado', 'concluir', 'btn-success')
        if pode_ver_separacao:
            adicionar_link('Fila de separacao', url_for('listar_separacao_entrega', busca=str(pedido.id)), 'btn-outline-secondary')
    elif fila_entrega and _pedido_pronto_para_roteirizacao(pedido):
        if not (pedido.rota_entrega or '').strip() or not pedido.etiqueta_entrega_emitida_em:
            if pode_ver_roteirizacao:
                rota_kwargs = {'rota': pedido.rota_entrega} if (pedido.rota_entrega or '').strip() else {}
                adicionar_link('Roteirizar', url_for('listar_roteirizacao_entrega', **rota_kwargs), 'btn-outline-secondary')
        elif not pedido.saiu_para_entrega_em and pode_despachar:
            adicionar_formulario('despacho', 'Saiu p/ entrega', 'sair', 'btn-info')
        elif pedido.saiu_para_entrega_em and not pedido.entrega_concluida_em and pode_despachar:
            adicionar_formulario('despacho', 'Confirmar entrega', 'entregar', 'btn-success')
        elif pedido.entrega_concluida_em and pedido.status == Pedido.STATUS_ENTREGUE and pode_alterar_status:
            adicionar_formulario('status', 'Fechar venda', Pedido.STATUS_FECHADO, 'btn-primary')
    elif pedido.status == Pedido.STATUS_ENTREGUE and pode_alterar_status:
        adicionar_formulario('status', 'Fechar venda', Pedido.STATUS_FECHADO, 'btn-primary')

    adicionar_link('Ver completo', url_for('detalhes_pedido', pedido_id=pedido.id))
    return acoes


def _resumir_filas_operacionais_pedidos(pedidos, empresa=None):
    empresa = empresa or _obter_empresa_config()
    contagens = {
        'registro': 0,
        'preparo': 0,
        'separacao': 0,
        'roteirizacao': 0,
        'em_rota': 0,
        'fechamento': 0,
    }

    for pedido in pedidos:
        fluxo = _visao_operacional_pedido(pedido, empresa)
        if fluxo['chave'] in contagens:
            contagens[fluxo['chave']] += 1

    cards = [
        {
            'chave': 'registro',
            'titulo': 'Registro e conferencia',
            'quantidade': contagens['registro'],
            'descricao': 'Pedidos novos aguardando validacao inicial.',
            'proxima_acao': 'Conferir itens, pagamento, canal e observacoes do pedido.',
            'apos_concluir': 'Enviar para preparo.',
            'url': url_for('listar_pedidos', status='aberto'),
        },
        {
            'chave': 'preparo',
            'titulo': 'Preparo',
            'quantidade': contagens['preparo'],
            'descricao': 'Pedidos em producao, montagem ou conferencia.',
            'proxima_acao': 'Separar internamente a producao e revisar faltas antes de liberar.',
            'apos_concluir': (
                'Atualizar para entregue e seguir para separacao.'
                if _separacao_entrega_ativa(empresa)
                else 'Entregar ao cliente e seguir para fechamento.'
            ),
            'url': url_for('listar_pedidos', status='em_preparo'),
        },
    ]

    if _separacao_entrega_ativa(empresa):
        cards.extend([
            {
                'chave': 'separacao',
                'titulo': 'Separacao',
                'quantidade': contagens['separacao'],
                'descricao': 'Pedidos prontos comercialmente, aguardando separacao fisica.',
                'proxima_acao': 'Separar itens, embalar e validar volumes.',
                'apos_concluir': 'Encaminhar para roteirizacao e despacho.',
                'url': url_for('listar_separacao_entrega', pendente='1'),
            },
            {
                'chave': 'roteirizacao',
                'titulo': 'Roteirizacao e despacho',
                'quantidade': contagens['roteirizacao'],
                'descricao': 'Pedidos separados aguardando rota, etiqueta ou saida.',
                'proxima_acao': 'Definir rota, motorista, etiqueta e expedicao.',
                'apos_concluir': 'Registrar saida para entrega.',
                'url': url_for('listar_roteirizacao_entrega', status_entrega='aguardando'),
            },
            {
                'chave': 'em_rota',
                'titulo': 'Em rota',
                'quantidade': contagens['em_rota'],
                'descricao': 'Pedidos ja despachados e em acompanhamento de entrega.',
                'proxima_acao': 'Monitorar entrega e tratar ocorrencias.',
                'apos_concluir': 'Confirmar entrega e seguir para fechamento.',
                'url': url_for('listar_roteirizacao_entrega', status_entrega='em_rota'),
            },
        ])

    cards.append({
        'chave': 'fechamento',
        'titulo': 'Fechamento',
        'quantidade': contagens['fechamento'],
        'descricao': 'Pedidos aguardando encerramento final da venda.',
        'proxima_acao': 'Conferir comprovantes, pagamento e documentacao.',
        'apos_concluir': 'Retirar o pedido da fila operacional.',
        'url': url_for('listar_pedidos', status='entregue'),
    })

    return cards


def _publicar_evento_expedicao(pedido, acao):
    try:
        publish_alert({
            'tipo': 'expedicao',
            'acao': acao,
            'pedido_id': pedido.id,
            'rota': pedido.rota_entrega,
            'etapa': _resolver_etapa_expedicao(pedido),
            'atualizado_em': datetime.utcnow().isoformat(),
        })
    except Exception:
        pass


def _coletar_progresso_expedicao_diario(empresa):
    agora = datetime.utcnow()
    inicio_dia = datetime(agora.year, agora.month, agora.day)
    fim_dia = inicio_dia + timedelta(days=1)

    pedidos = Pedido.query.filter(
        Pedido.status.in_(DELIVERY_SEPARATION_STATUSES),
        Pedido.origem.in_(_origens_separacao_entrega(empresa)),
        Pedido.criado_em >= inicio_dia,
        Pedido.criado_em < fim_dia,
    ).all()

    totais = {
        'separacao': 0,
        'embalagem': 0,
        'expedicao': 0,
        'em_rota': 0,
        'entregue': 0,
    }
    for pedido in pedidos:
        etapa = _resolver_etapa_expedicao(pedido)
        totais[etapa] = totais.get(etapa, 0) + 1

    total_dia = len(pedidos)
    etapas = [
        ('separacao', 'Separacao'),
        ('embalagem', 'Embalagem'),
        ('expedicao', 'Expedicao'),
        ('em_rota', 'Em rota'),
        ('entregue', 'Entregue'),
    ]
    progresso = []
    for chave, label in etapas:
        quantidade = int(totais.get(chave, 0))
        percentual = round((quantidade * 100.0 / total_dia), 1) if total_dia else 0.0
        progresso.append({
            'chave': chave,
            'label': label,
            'quantidade': quantidade,
            'percentual': percentual,
        })

    return {
        'total_dia': total_dia,
        'inicio_dia': inicio_dia.isoformat(),
        'fim_dia': fim_dia.isoformat(),
        'progresso': progresso,
    }


def _bloquear_se_atendimento_mesas_desativado():
    if _atendimento_mesas_ativo():
        return None
    flash('Modulo de mesas e garcons esta desativado para esta empresa.', 'warning')
    return redirect(url_for('pdv'))


def _usuario_tem_acesso_endpoint(endpoint, funcionario=None, paginas_permitidas=None):
    if funcionario is None:
        funcionario_id = session.get('funcionario_id')
        if not funcionario_id:
            return False
        funcionario = Funcionario.query.get(funcionario_id)
    if not funcionario or not funcionario.ativo:
        return False
    if funcionario.role == 'admin':
        return True
    if not funcionario.controle_acesso_ativo:
        return True
    pagina = ENDPOINT_TO_PAGINA.get(endpoint)
    if not pagina:
        return True
    if paginas_permitidas is not None:
        return pagina in paginas_permitidas
    return pagina in _paginas_efetivas_funcionario(funcionario)


def _paginas_perfil_acesso_funcionario(funcionario):
    perfil = getattr(funcionario, 'perfil_acesso', None)
    if not perfil or not perfil.permissoes_padrao:
        return set()
    try:
        dados = json.loads(perfil.permissoes_padrao)
    except Exception:
        return set()
    if not isinstance(dados, list):
        return set()
    return {
        pagina
        for pagina in dados
        if isinstance(pagina, str)
    }


def _paginas_efetivas_funcionario(funcionario):
    if not funcionario or not funcionario.ativo:
        return set()
    if funcionario.role == 'admin' or not funcionario.controle_acesso_ativo:
        return set(ENDPOINT_TO_PAGINA.values())

    permitidas = set(_paginas_perfil_acesso_funcionario(funcionario))
    for permissao in PermissaoAcesso.query.filter_by(funcionario_id=funcionario.id).all():
        if permissao.permitido:
            permitidas.add(permissao.pagina)
        else:
            permitidas.discard(permissao.pagina)
    return permitidas


def _garcom_logado_id():
    funcionario_id = session.get('funcionario_id')
    if not funcionario_id:
        return None
    garcom = Garcom.query.filter_by(funcionario_id=funcionario_id, ativo=True).first()
    return garcom.id if garcom else None


def _parse_status(value, default='aberto'):
    status = (value or default).strip().lower()
    return status if status in ORDER_ALLOWED_TRANSITIONS else default


def _http_status_for_order_error(message):
    text = (message or '').lower()
    conflict_terms = (
        'imutavel',
        'transicao',
        'insuficiente',
        'caixa do pedido esta fechada',
        'somente pedidos',
        'ja esta',
        'nao pode ser fechado',
    )
    for term in conflict_terms:
        if term in text:
            return 409, 'business_rule'
    return 400, 'validation_error'


def _processar_fechamento_pedido(pedido):
    """Aplica regras de negócio para encerrar um pedido.

    - Garante que há itens
    - Calcula total e registra timestamps de fechamento
    - Marca pedido como processado para estoque/financeiro quando aplicável
    """
    if not pedido.itens:
        raise ValueError('Pedido sem itens nao pode ser fechado.')

    if not pedido.estoque_processado:
        for item in pedido.itens:
            produto = item.produto or Produto.query.get(item.produto_id)
            if not produto:
                raise ValueError(f'Produto do item {item.id} nao encontrado.')
            if produto.quantidade_estoque < item.quantidade:
                raise ValueError(f'Estoque insuficiente para "{produto.nome}".')

        for item in pedido.itens:
            produto = item.produto or Produto.query.get(item.produto_id)
            produto.quantidade_estoque -= item.quantidade
            db.session.add(Movimentacao(
                produto_id=produto.id,
                tipo=Movimentacao.TIPO_SAIDA,
                quantidade=item.quantidade,
                motivo='venda',
                observacoes=f'Pedido {pedido.id} fechado'
            ))
        pedido.estoque_processado = True

    if pedido.caixa_id and not pedido.financeiro_processado:
        caixa = pedido.caixa or Caixa.query.get(pedido.caixa_id)
        if not caixa:
            raise ValueError('Caixa do pedido nao encontrada.')
        if not caixa.aberto:
            raise ValueError('Caixa do pedido esta fechada. Nao e possivel concluir o financeiro.')

        valor_pedido = float(pedido.total or 0.0)
        caixa.saldo_atual = float(caixa.saldo_atual or 0.0) + valor_pedido
        db.session.add(MovimentacaoCaixa(
            caixa_id=caixa.id,
            tipo=MovimentacaoCaixa.TIPO_ENTRADA,
            valor=valor_pedido,
            descricao=f'Fechamento do pedido #{pedido.id}'
        ))
        pedido.financeiro_processado = True

    pedido.fechado_em = datetime.utcnow()
    if pedido.mesa:
        pedido.mesa.status = 'livre'


def _aplicar_transicao_status(pedido, novo_status):
    return pedido.transitar_para(novo_status, on_fechamento=_processar_fechamento_pedido)


def _processar_fechamento_pedido(pedido):
    return service_processar_fechamento_pedido(pedido)


def _aplicar_transicao_status(pedido, novo_status):
    return service_aplicar_transicao_status(pedido, novo_status)


def register_vendas_routes(app, login_required, require_role):
    vendas_operacao_roles = ('admin', 'gerente', 'caixa', 'operador', 'garcom')
    vendas_gestao_roles = ('admin', 'gerente')
    caixa_operacao_roles = ('admin', 'gerente', 'caixa')
    separacao_entrega_roles = ('admin', 'gerente', 'caixa', 'operador')

    @app.route('/expedicao')
    @require_role(*separacao_entrega_roles)
    def central_expedicao():
        empresa = _obter_empresa_config()
        if not _separacao_entrega_ativa(empresa):
            flash('Separacao para entrega esta desativada na configuracao da empresa.', 'warning')
            return redirect(url_for('listar_pedidos'))

        progresso = _coletar_progresso_expedicao_diario(empresa)
        return render_template(
            'expedicao/central.html',
            empresa=empresa,
            progresso=progresso,
            veiculos_cadastrados=_carregar_lista_config(empresa.entrega_veiculos_json),
            terceirizadas_cadastradas=_carregar_lista_config(empresa.entrega_terceirizadas_json),
            etiquetas_ativas=_emissao_etiqueta_entrega_ativa(empresa),
            emissao_nota_ativa=empresa.emissao_nota_entrega_ativa is not False,
        )

    @app.route('/expedicao/frota', methods=['GET', 'POST'])
    @require_role(*vendas_gestao_roles)
    def frota_expedicao():
        empresa = _obter_empresa_config()
        if request.method == 'POST':
            try:
                empresa.entrega_local_saida_padrao = (request.form.get('entrega_local_saida_padrao') or '').strip() or None
                empresa.entrega_motorista_padrao = (request.form.get('entrega_motorista_padrao') or '').strip() or None
                empresa.entrega_veiculo_padrao = (request.form.get('entrega_veiculo_padrao') or '').strip() or None
                horario_fechamento_roteirizacao = _parse_horario_hhmm(request.form.get('entrega_horario_fechamento_roteirizacao'))
                horario_fechamento_roteirizacao_txt = (request.form.get('entrega_horario_fechamento_roteirizacao') or '').strip()
                if horario_fechamento_roteirizacao_txt and not horario_fechamento_roteirizacao:
                    flash('Horario de fechamento da roteirizacao invalido. Use HH:MM.', 'error')
                    return redirect(url_for('frota_expedicao'))
                empresa.entrega_horario_fechamento_roteirizacao = (
                    horario_fechamento_roteirizacao.strftime('%H:%M')
                    if horario_fechamento_roteirizacao
                    else None
                )

                veiculos_linhas = _normalizar_veiculos_texto(request.form.get('entrega_veiculos_cadastro', ''))
                terceirizadas_linhas = _normalizar_linhas_configuracao(request.form.get('entrega_terceirizadas_cadastro', ''))

                empresa.entrega_veiculos_json = json.dumps(veiculos_linhas, ensure_ascii=False) if veiculos_linhas else None
                empresa.entrega_terceirizadas_json = json.dumps(terceirizadas_linhas, ensure_ascii=False) if terceirizadas_linhas else None
                db.session.commit()
                flash('Cadastro de frota e terceiros atualizado com sucesso.', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao atualizar cadastro de frota: {str(e)}', 'error')
            return redirect(url_for('frota_expedicao'))

        veiculos_texto = _serializar_veiculos_config_texto(_carregar_veiculos_config(empresa.entrega_veiculos_json))
        terceirizadas_texto = '\n'.join(_carregar_lista_config(empresa.entrega_terceirizadas_json))
        return render_template(
            'expedicao/frota.html',
            empresa=empresa,
            veiculos_texto=veiculos_texto,
            terceirizadas_texto=terceirizadas_texto,
        )

    @app.route('/garcons')
    @require_role(*vendas_gestao_roles)
    def listar_garcons():
        bloqueio = _bloquear_se_atendimento_mesas_desativado()
        if bloqueio:
            return bloqueio
        garcons = Garcom.query.order_by(Garcom.nome.asc()).all()
        pedidos_em_andamento = Pedido.query.filter(Pedido.status.in_(['aberto', 'em_preparo', 'entregue'])).order_by(Pedido.criado_em.desc()).all()
        empresa = _obter_empresa_config()
        return render_template(
            'vendas/garcons/garcons.html',
            garcons=garcons,
            pedidos_em_andamento=pedidos_em_andamento,
            empresa=empresa
        )

    @app.route('/garcons/novo', methods=['GET', 'POST'])
    @require_role(*vendas_gestao_roles)
    def novo_garcom():
        bloqueio = _bloquear_se_atendimento_mesas_desativado()
        if bloqueio:
            return bloqueio
        if request.method == 'POST':
            try:
                nome = (request.form.get('nome') or '').strip()
                celular = (request.form.get('celular') or '').strip()
                ativo = (request.form.get('ativo') == 'on')
                if not nome:
                    flash('Nome do garcom e obrigatorio.', 'error')
                    return redirect(url_for('novo_garcom'))

                garcom = Garcom(nome=nome, celular=celular or None, ativo=ativo)
                db.session.add(garcom)
                db.session.commit()
                flash('Garcom cadastrado com sucesso.', 'success')
                return redirect(url_for('listar_garcons'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao cadastrar garcom: {str(e)}', 'error')
        return render_template('vendas/garcons/novo_garcom.html')

    @app.route('/garcons/<int:garcom_id>/editar', methods=['GET', 'POST'])
    @require_role(*vendas_gestao_roles)
    def editar_garcom(garcom_id):
        bloqueio = _bloquear_se_atendimento_mesas_desativado()
        if bloqueio:
            return bloqueio
        garcom = Garcom.query.get_or_404(garcom_id)
        if request.method == 'POST':
            try:
                nome = (request.form.get('nome') or '').strip()
                if not nome:
                    flash('Nome do garcom e obrigatorio.', 'error')
                    return redirect(url_for('editar_garcom', garcom_id=garcom_id))
                garcom.nome = nome
                garcom.celular = (request.form.get('celular') or '').strip() or None
                garcom.ativo = (request.form.get('ativo') == 'on')
                db.session.commit()
                flash('Garcom atualizado com sucesso.', 'success')
                return redirect(url_for('listar_garcons'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao atualizar garcom: {str(e)}', 'error')
        return render_template('vendas/garcons/editar_garcom.html', garcom=garcom)

    @app.route('/garcons/<int:garcom_id>/deletar', methods=['POST'])
    @require_role(*vendas_gestao_roles)
    def deletar_garcom(garcom_id):
        bloqueio = _bloquear_se_atendimento_mesas_desativado()
        if bloqueio:
            return bloqueio
        garcom = Garcom.query.get_or_404(garcom_id)
        try:
            Pedido.query.filter_by(garcom_id=garcom.id).update({'garcom_id': None})
            db.session.delete(garcom)
            db.session.commit()
            flash('Garcom removido com sucesso.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao remover garcom: {str(e)}', 'error')
        return redirect(url_for('listar_garcons'))

    @app.route('/garcons/config', methods=['GET', 'POST'])
    @require_role(*vendas_gestao_roles)
    def configurar_distribuicao_garcons():
        bloqueio = _bloquear_se_atendimento_mesas_desativado()
        if bloqueio:
            return bloqueio
        empresa = _obter_empresa_config()
        if request.method == 'POST':
            try:
                empresa.distribuicao_ativa = (request.form.get('distribuicao_ativa') == 'on')
                modo = (request.form.get('modo_distribuicao_pedidos') or 'round_robin').strip().lower()
                if modo not in {'round_robin', 'menos_pedidos', 'manual'}:
                    modo = 'round_robin'
                empresa.modo_distribuicao_pedidos = modo
                db.session.commit()
                flash('Configuracao de distribuicao salva com sucesso.', 'success')
                return redirect(url_for('configurar_distribuicao_garcons'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao salvar configuracao: {str(e)}', 'error')
        return render_template('vendas/garcons/config_distribuicao.html', empresa=empresa)

    @app.route('/caixas')
    @require_role(*caixa_operacao_roles)
    def listar_caixas():
        caixas = Caixa.query.all()
        return render_template('vendas/caixas/caixas.html', caixas=caixas)

    @app.route('/caixas/nova', methods=['GET', 'POST'])
    @require_role(*vendas_gestao_roles)
    def nova_caixa():
        if request.method == 'POST':
            try:
                nome = request.form.get('nome')
                saldo = float(request.form.get('saldo_inicial') or 0)
                caixa = Caixa(nome=nome, saldo_inicial=saldo, saldo_atual=saldo)
                db.session.add(caixa)
                db.session.commit()
                flash(f'Caixa "{caixa.nome}" criado com sucesso!', 'success')
                return redirect(url_for('listar_caixas'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao criar caixa: {str(e)}', 'error')
        return render_template('vendas/caixas/nova_caixa.html')

    @app.route('/caixas/<int:caixa_id>/editar', methods=['GET', 'POST'])
    @require_role(*vendas_gestao_roles)
    def editar_caixa(caixa_id):
        caixa = Caixa.query.get_or_404(caixa_id)
        if request.method == 'POST':
            try:
                caixa.nome = request.form.get('nome', caixa.nome)
                caixa.saldo_atual = float(request.form.get('saldo_atual', caixa.saldo_atual))
                aberto = request.form.get('aberto')
                caixa.aberto = bool(aberto == 'on')
                if not caixa.aberto and not caixa.fechado_em:
                    caixa.fechado_em = datetime.utcnow()
                db.session.commit()
                flash(f'Caixa "{caixa.nome}" atualizado com sucesso!', 'success')
                return redirect(url_for('listar_caixas'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao atualizar caixa: {str(e)}', 'error')
        return render_template('vendas/caixas/editar_caixa.html', caixa=caixa)

    @app.route('/caixas/<int:caixa_id>/deletar', methods=['POST'])
    @require_role(*vendas_gestao_roles)
    def deletar_caixa(caixa_id):
        caixa = Caixa.query.get_or_404(caixa_id)
        try:
            db.session.delete(caixa)
            db.session.commit()
            flash(f'Caixa "{caixa.nome}" deletado.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao deletar caixa: {str(e)}', 'error')
        return redirect(url_for('listar_caixas'))

    @app.route('/caixas/<int:caixa_id>/abrir', methods=['GET', 'POST'])
    @require_role(*caixa_operacao_roles)
    def abrir_caixa(caixa_id):
        """Abre uma caixa e a atribui a um funcionário"""
        caixa = Caixa.query.get_or_404(caixa_id)
        
        # Valida se caixa já está aberta
        if caixa.aberto:
            flash(f'Caixa "{caixa.nome}" já está aberta!', 'warning')
            return redirect(url_for('listar_caixas'))
        
        if request.method == 'POST':
            try:
                funcionario_id = request.form.get('funcionario_id', type=int)
                saldo_inicial = float(request.form.get('saldo_inicial', 0))
                observacoes = request.form.get('observacoes', '')
                
                funcionario = Funcionario.query.get(funcionario_id)
                if not funcionario:
                    flash('Funcionário selecionado não existe!', 'danger')
                    return redirect(url_for('abrir_caixa', caixa_id=caixa_id))
                
                # Abre a caixa
                caixa.funcionario_id = funcionario_id
                caixa.saldo_inicial = saldo_inicial
                caixa.saldo_atual = saldo_inicial
                caixa.aberto = True
                caixa.aberto_em = datetime.utcnow()
                caixa.observacoes = observacoes
                
                # Registra a movimentação de abertura
                mov = MovimentacaoCaixa(
                    caixa_id=caixa.id,
                    tipo=MovimentacaoCaixa.TIPO_ENTRADA,
                    valor=saldo_inicial,
                    descricao=f'Abertura de caixa por {funcionario.nome}'
                )
                db.session.add(mov)
                db.session.commit()
                
                flash(f'Caixa "{caixa.nome}" aberta com sucesso! Atribuída a {funcionario.nome}', 'success')
                return redirect(url_for('listar_caixas'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao abrir caixa: {str(e)}', 'error')
        
        funcionarios = Funcionario.query.filter_by(ativo=True).all()
        return render_template('vendas/caixas/abrir_caixa.html', caixa=caixa, funcionarios=funcionarios)

    @app.route('/caixas/<int:caixa_id>/fechar', methods=['GET', 'POST'])
    @require_role(*caixa_operacao_roles)
    def fechar_caixa(caixa_id):
        """Fecha uma caixa com saldo de fechamento"""
        caixa = Caixa.query.get_or_404(caixa_id)
        
        # Valida se caixa está fechada
        if not caixa.aberto:
            flash(f'Caixa "{caixa.nome}" já está fechada!', 'warning')
            return redirect(url_for('listar_caixas'))
        
        if request.method == 'POST':
            try:
                saldo_fechamento = float(request.form.get('saldo_fechamento', 0))
                observacoes = request.form.get('observacoes', '')
                
                # Calcula diferença
                diferenca = saldo_fechamento - caixa.saldo_atual
                
                # Fecha a caixa
                caixa.saldo_fechamento = saldo_fechamento
                caixa.aberto = False
                caixa.fechado_em = datetime.utcnow()
                caixa.observacoes = observacoes
                
                # Registra a movimentação de fechamento
                mov = MovimentacaoCaixa(
                    caixa_id=caixa.id,
                    tipo=MovimentacaoCaixa.TIPO_SAIDA if diferenca < 0 else MovimentacaoCaixa.TIPO_ENTRADA,
                    valor=abs(diferenca),
                    descricao=f'Fechamento de caixa - Diferença: R$ {diferenca:.2f}'
                )
                db.session.add(mov)
                db.session.commit()
                
                msg = f'Caixa "{caixa.nome}" fechada com sucesso!'
                if diferenca != 0:
                    msg += f' Diferença: R$ {diferenca:.2f}'
                flash(msg, 'success')
                return redirect(url_for('listar_caixas'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao fechar caixa: {str(e)}', 'error')
        
        return render_template('vendas/caixas/fechar_caixa.html', caixa=caixa)

    @app.route('/caixas/<int:caixa_id>/historico')
    @require_role(*caixa_operacao_roles)
    def historico_caixa(caixa_id):
        """Exibe histórico de movimentações da caixa"""
        caixa = Caixa.query.get_or_404(caixa_id)
        movimentacoes = MovimentacaoCaixa.query.filter_by(caixa_id=caixa_id).order_by(
            MovimentacaoCaixa.criado_em.desc()
        ).all()
        
        return render_template('vendas/caixas/historico_caixa.html', caixa=caixa, movimentacoes=movimentacoes)

    @app.route('/mesas')
    @require_role(*caixa_operacao_roles)
    def listar_mesas():
        bloqueio = _bloquear_se_atendimento_mesas_desativado()
        if bloqueio:
            return bloqueio
        mesas = Mesa.query.all()
        # Garante que todas as mesas tenham token para QR Code
        for mesa in mesas:
            if not mesa.qr_token:
                mesa.qr_token = secrets.token_urlsafe(12)
        db.session.commit()
        return render_template('vendas/mesas/mesas.html', mesas=mesas)

    @app.route('/mesas/nova', methods=['GET', 'POST'])
    @require_role(*caixa_operacao_roles)
    def nova_mesa():
        bloqueio = _bloquear_se_atendimento_mesas_desativado()
        if bloqueio:
            return bloqueio
        if request.method == 'POST':
            try:
                numero = request.form.get('numero')
                capacidade = int(request.form.get('capacidade') or 1)
                mesa = Mesa(numero=numero, capacidade=capacidade, status='livre', qr_token=secrets.token_urlsafe(12))
                db.session.add(mesa)
                db.session.commit()
                flash(f'Mesa "{mesa.numero}" criada com sucesso!', 'success')
                return redirect(url_for('listar_mesas'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao criar mesa: {str(e)}', 'error')
        return render_template('vendas/mesas/nova_mesa.html')

    @app.route('/mesas/<int:mesa_id>/editar', methods=['GET', 'POST'])
    @require_role(*caixa_operacao_roles)
    def editar_mesa(mesa_id):
        bloqueio = _bloquear_se_atendimento_mesas_desativado()
        if bloqueio:
            return bloqueio
        mesa = Mesa.query.get_or_404(mesa_id)
        if not mesa.qr_token:
            mesa.qr_token = secrets.token_urlsafe(12)
        if request.method == 'POST':
            try:
                mesa.numero = request.form.get('numero', mesa.numero)
                mesa.capacidade = int(request.form.get('capacidade', mesa.capacidade))
                mesa.status = request.form.get('status', mesa.status)
                db.session.commit()
                flash(f'Mesa "{mesa.numero}" atualizada!', 'success')
                return redirect(url_for('listar_mesas'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao atualizar mesa: {str(e)}', 'error')
        return render_template('vendas/mesas/editar_mesa.html', mesa=mesa)

    @app.route('/mesas/<int:mesa_id>/deletar', methods=['POST'])
    @require_role(*caixa_operacao_roles)
    def deletar_mesa(mesa_id):
        bloqueio = _bloquear_se_atendimento_mesas_desativado()
        if bloqueio:
            return bloqueio
        mesa = Mesa.query.get_or_404(mesa_id)
        try:
            db.session.delete(mesa)
            db.session.commit()
            flash(f'Mesa "{mesa.numero}" deletada.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao deletar mesa: {str(e)}', 'error')
        return redirect(url_for('listar_mesas'))

    @app.route('/mesas/<int:mesa_id>/qrcode')
    @require_role(*caixa_operacao_roles)
    def visualizar_qrcode_mesa(mesa_id):
        bloqueio = _bloquear_se_atendimento_mesas_desativado()
        if bloqueio:
            return bloqueio
        """Exibe o QR code da mesa com opções de impressão e download"""
        mesa = Mesa.query.get_or_404(mesa_id)
        
        # Garante que a mesa tenha token
        if not mesa.qr_token:
            mesa.qr_token = secrets.token_urlsafe(12)
            db.session.commit()
        
        # URL publica da comanda (rota QR)
        qr_url = url_for('public.cardapio_mesa', token=mesa.qr_token, _external=True)
        
        return render_template('vendas/mesas/qrcode_mesa.html', mesa=mesa, qr_url=qr_url)

    @app.route('/mesas/<int:mesa_id>/qrcode/download')
    @require_role(*caixa_operacao_roles)
    def download_qrcode_mesa(mesa_id):
        bloqueio = _bloquear_se_atendimento_mesas_desativado()
        if bloqueio:
            return bloqueio
        """Faz download da imagem do QR code"""
        mesa = Mesa.query.get_or_404(mesa_id)
        
        if not mesa.qr_token:
            flash('QR code não disponível para esta mesa', 'error')
            return redirect(url_for('listar_mesas'))
        
        try:
            # Gera o QR code com rota publica da comanda
            qr_url = url_for('public.cardapio_mesa', token=mesa.qr_token, _external=True)
            
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=2,
            )
            qr.add_data(qr_url)
            qr.make(fit=True)
            
            # Cria a imagem em memória
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Salva em bytes
            img_io = BytesIO()
            img.save(img_io, 'PNG')
            img_io.seek(0)
            
            # Retorna como resposta
            return Response(
                img_io.getvalue(),
                mimetype='image/png',
                headers={"Content-Disposition": f"attachment;filename=qrcode_mesa_{mesa.numero}.png"}
            )
        except Exception as e:
            flash(f'Erro ao gerar QR code: {str(e)}', 'error')
            return redirect(url_for('visualizar_qrcode_mesa', mesa_id=mesa_id))

    @app.route('/mesas/<int:mesa_id>/qrcode/print')
    @require_role(*caixa_operacao_roles)
    def print_qrcode_mesa(mesa_id):
        bloqueio = _bloquear_se_atendimento_mesas_desativado()
        if bloqueio:
            return bloqueio
        """Exibe o QR code em formato para impressão"""
        mesa = Mesa.query.get_or_404(mesa_id)
        
        if not mesa.qr_token:
            flash('QR code não disponível para esta mesa', 'error')
            return redirect(url_for('listar_mesas'))
        
        qr_url = url_for('public.cardapio_mesa', token=mesa.qr_token, _external=True)
        
        return render_template('vendas/mesas/print_qrcode_mesa.html', mesa=mesa, qr_url=qr_url)

    @app.route('/pedidos')
    @require_role(*vendas_operacao_roles)
    def listar_pedidos():
        empresa = _obter_empresa_config()
        funcionario = Funcionario.query.get(session.get('funcionario_id')) if session.get('funcionario_id') else None
        paginas_permitidas = _paginas_efetivas_funcionario(funcionario)
        page = max(request.args.get('page', 1, type=int), 1)
        per_page = min(max(request.args.get('per_page', 20, type=int), 1), 100)
        status_filtro = (request.args.get('status') or '').strip().lower()
        busca = (request.args.get('busca') or '').strip()

        query = Pedido.query
        if status_filtro in {'aberto', 'em_preparo', 'entregue', 'fechado', 'cancelado'}:
            query = query.filter(Pedido.status == status_filtro)

        if busca:
            termo = f'%{busca}%'
            query = query.filter(
                db.or_(
                    db.cast(Pedido.id, db.String).ilike(termo),
                    Pedido.cliente_nome.ilike(termo),
                    Pedido.cliente_celular.ilike(termo),
                    Pedido.mesa.has(Mesa.numero.ilike(termo)),
                    Pedido.caixa.has(Caixa.nome.ilike(termo))
                )
            )

        filas_operacionais = _resumir_filas_operacionais_pedidos(
            query.with_entities(
                Pedido.id,
                Pedido.status,
                Pedido.origem,
                Pedido.separacao_entrega_concluida,
                Pedido.etiqueta_entrega_emitida_em,
                Pedido.rota_entrega,
                Pedido.saiu_para_entrega_em,
                Pedido.entrega_concluida_em,
            ).all(),
            empresa=empresa,
        )
        pedidos = (
            query.options(
                load_only(
                    Pedido.id,
                    Pedido.mesa_id,
                    Pedido.caixa_id,
                    Pedido.garcom_id,
                    Pedido.cliente_nome,
                    Pedido.cliente_celular,
                    Pedido.total,
                    Pedido.status,
                    Pedido.origem,
                    Pedido.criado_em,
                    Pedido.separacao_entrega_concluida,
                    Pedido.etiqueta_entrega_emitida_em,
                    Pedido.rota_entrega,
                    Pedido.saiu_para_entrega_em,
                    Pedido.entrega_concluida_em,
                ),
                selectinload(Pedido.mesa),
                selectinload(Pedido.caixa),
                selectinload(Pedido.garcom),
                selectinload(Pedido.itens).selectinload(ItemPedido.produto),
            )
            .order_by(Pedido.criado_em.desc())
            .paginate(page=page, per_page=per_page, error_out=False)
        )
        for pedido in pedidos.items:
            pedido.fluxo_operacional = _visao_operacional_pedido(pedido, empresa=empresa)
            pedido.acoes_operacionais = _acoes_rapidas_pedido(
                pedido,
                empresa=empresa,
                funcionario=funcionario,
                paginas_permitidas=paginas_permitidas,
            )
        return render_template(
            'vendas/pedidos/pedidos.html',
            pedidos=pedidos.items,
            pagination=pedidos,
            per_page=per_page,
            status_filtro=status_filtro,
            busca=busca,
            query_params=request.args.to_dict(),
            status_transitions=ORDER_ALLOWED_TRANSITIONS,
            empresa=empresa,
            filas_operacionais=filas_operacionais,
        )

    @app.route('/pedidos/separacao-entrega')
    @require_role(*separacao_entrega_roles)
    def listar_separacao_entrega():
        empresa = _obter_empresa_config()
        if not _separacao_entrega_ativa(empresa):
            flash('Separacao para entrega esta desativada na configuracao da empresa.', 'warning')
            return redirect(url_for('listar_pedidos'))

        page = max(request.args.get('page', 1, type=int), 1)
        per_page = min(max(request.args.get('per_page', 20, type=int), 1), 100)
        busca = (request.args.get('busca') or '').strip()
        pendente = (request.args.get('pendente') or '1').strip().lower()

        query = Pedido.query.options(
            selectinload(Pedido.caixa),
            selectinload(Pedido.mesa),
            selectinload(Pedido.itens).selectinload(ItemPedido.produto),
        ).filter(
            Pedido.status.in_(DELIVERY_SEPARATION_STATUSES),
            Pedido.origem.in_(_origens_separacao_entrega(empresa)),
        )

        if pendente == '1':
            query = query.filter(
                db.or_(
                    Pedido.separacao_entrega_concluida.is_(False),
                    Pedido.separacao_entrega_concluida.is_(None),
                )
            )
        elif pendente == '0':
            query = query.filter(Pedido.separacao_entrega_concluida.is_(True))

        if busca:
            termo = f'%{busca}%'
            query = query.filter(
                db.or_(
                    db.cast(Pedido.id, db.String).ilike(termo),
                    Pedido.cliente_nome.ilike(termo),
                    Pedido.cliente_celular.ilike(termo),
                )
            )

        pagination = query.order_by(Pedido.criado_em.desc()).paginate(page=page, per_page=per_page, error_out=False)
        veiculos_cadastrados = _carregar_lista_config(empresa.entrega_veiculos_json)
        terceirizadas_cadastradas = _carregar_lista_config(empresa.entrega_terceirizadas_json)
        return render_template(
            'vendas/pedidos/separacao_entrega.html',
            pedidos=pagination.items,
            pagination=pagination,
            per_page=per_page,
            busca=busca,
            pendente=pendente,
            query_params=request.args.to_dict(),
            empresa=empresa,
            etiquetas_ativas=_emissao_etiqueta_entrega_ativa(empresa),
            roteirizacao_ativa=empresa.roteirizacao_entrega_ativa is not False,
            emissao_nota_ativa=empresa.emissao_nota_entrega_ativa is not False,
            veiculos_cadastrados=veiculos_cadastrados,
            terceirizadas_cadastradas=terceirizadas_cadastradas,
        )

    @app.route('/estoque/coletor')
    @require_role(*separacao_entrega_roles)
    def coletor_estoque():
        empresa = _obter_empresa_config()
        if not _separacao_entrega_ativa(empresa):
            flash('Separacao para entrega esta desativada na configuracao da empresa.', 'warning')
            return redirect(url_for('listar_pedidos'))

        busca = (request.args.get('busca') or '').strip()
        etapa = (request.args.get('etapa') or 'todos').strip().lower()

        query = Pedido.query.options(
            selectinload(Pedido.itens).selectinload(ItemPedido.produto),
            selectinload(Pedido.caixa),
            selectinload(Pedido.mesa),
        ).filter(
            Pedido.origem.in_(_origens_separacao_entrega(empresa)),
            Pedido.status.in_(DELIVERY_SEPARATION_STATUSES),
        )

        if busca:
            termo = f'%{busca}%'
            query = query.filter(
                db.or_(
                    db.cast(Pedido.id, db.String).ilike(termo),
                    Pedido.cliente_nome.ilike(termo),
                    Pedido.cliente_celular.ilike(termo),
                    Pedido.rota_entrega.ilike(termo),
                )
            )

        pedidos = query.order_by(
            db.case((Pedido.separacao_entrega_concluida.is_(False), 0), else_=1),
            Pedido.criado_em.asc(),
        ).all()

        cards = []
        for pedido in pedidos:
            if not pedido.separacao_entrega_concluida:
                etapa_atual = 'separacao'
            elif not pedido.etiqueta_entrega_emitida_em:
                etapa_atual = 'embalagem'
            elif not pedido.saiu_para_entrega_em:
                etapa_atual = 'expedicao'
            elif not pedido.entrega_concluida_em:
                etapa_atual = 'em_rota'
            else:
                etapa_atual = 'concluido'

            if etapa != 'todos' and etapa != etapa_atual:
                continue

            cards.append({
                'pedido': pedido,
                'etapa_atual': etapa_atual,
            })

        return render_template(
            'estoque/coletor.html',
            cards=cards,
            empresa=empresa,
            busca=busca,
            etapa=etapa,
            etiquetas_ativas=_emissao_etiqueta_entrega_ativa(empresa),
        )

    @app.route('/pedidos/expedicao/iniciar', methods=['POST'])
    @require_role(*vendas_operacao_roles)
    def iniciar_processo_expedicao():
        empresa = _obter_empresa_config()
        if not _separacao_entrega_ativa(empresa):
            flash('Separacao para entrega esta desativada na configuracao da empresa.', 'warning')
            return redirect(url_for('listar_pedidos'))
        session['expedicao_iniciada_em'] = datetime.utcnow().isoformat()
        flash('Processo de expedicao iniciado para monitoramento diario.', 'success')
        return redirect(url_for('painel_expedicao'))

    @app.route('/pedidos/expedicao/painel')
    @require_role(*vendas_operacao_roles)
    def painel_expedicao():
        empresa = _obter_empresa_config()
        if not _separacao_entrega_ativa(empresa):
            flash('Separacao para entrega esta desativada na configuracao da empresa.', 'warning')
            return redirect(url_for('listar_pedidos'))

        progresso = _coletar_progresso_expedicao_diario(empresa)
        iniciado_em = session.get('expedicao_iniciada_em')
        return render_template(
            'vendas/pedidos/painel_expedicao.html',
            empresa=empresa,
            progresso=progresso,
            iniciado_em=iniciado_em,
        )

    @app.route('/api/pedidos/expedicao/progresso')
    @require_role(*vendas_operacao_roles)
    def api_progresso_expedicao():
        empresa = _obter_empresa_config()
        if not _separacao_entrega_ativa(empresa):
            return jsonify({'success': False, 'message': 'Separacao de entrega desativada.'}), 409

        data = _coletar_progresso_expedicao_diario(empresa)
        data['iniciado_em'] = session.get('expedicao_iniciada_em')
        return jsonify({'success': True, 'data': data})

    @app.route('/pedidos/roteirizacao-entrega')
    @require_role(*separacao_entrega_roles)
    def listar_roteirizacao_entrega():
        empresa = _obter_empresa_config()
        if not _separacao_entrega_ativa(empresa):
            flash('Separacao para entrega esta desativada na configuracao da empresa.', 'warning')
            return redirect(url_for('listar_pedidos'))

        rota_filtro = (request.args.get('rota') or '').strip()
        status_filtro = (request.args.get('status_entrega') or 'todos').strip().lower()

        query = Pedido.query.options(
            selectinload(Pedido.itens).selectinload(ItemPedido.produto),
            selectinload(Pedido.caixa),
        ).filter(
            Pedido.origem.in_(_origens_separacao_entrega(empresa)),
            Pedido.separacao_entrega_concluida.is_(True),
        )

        if rota_filtro:
            query = query.filter(Pedido.rota_entrega == rota_filtro)

        if status_filtro == 'aguardando':
            query = query.filter(Pedido.saiu_para_entrega_em.is_(None))
        elif status_filtro == 'em_rota':
            query = query.filter(
                Pedido.saiu_para_entrega_em.is_not(None),
                Pedido.entrega_concluida_em.is_(None)
            )
        elif status_filtro == 'entregue':
            query = query.filter(Pedido.entrega_concluida_em.is_not(None))

        pedidos_base = query.order_by(
            db.case((Pedido.rota_entrega.is_(None), 1), else_=0),
            Pedido.rota_entrega.asc(),
            db.case((Pedido.ordem_rota.is_(None), 1), else_=0),
            Pedido.ordem_rota.asc(),
            Pedido.criado_em.asc(),
        ).all()
        pedidos, pedidos_proximo_ciclo, corte_roteirizacao = _separar_pedidos_por_corte_roteirizacao(
            pedidos_base,
            empresa,
        )

        rotas_disponiveis = (
            db.session.query(Pedido.rota_entrega)
            .filter(Pedido.rota_entrega.is_not(None), Pedido.rota_entrega != '')
            .distinct()
            .order_by(Pedido.rota_entrega.asc())
            .all()
        )
        rotas_disponiveis = [r[0] for r in rotas_disponiveis if r and r[0]]
        regras_roteirizacao = _carregar_regras_roteirizacao(empresa)
        veiculos_configurados = _carregar_veiculos_config(empresa.entrega_veiculos_json)
        resumo_roteirizacao = {
            'total_pedidos': len(pedidos),
            'aguardando': 0,
            'em_rota': 0,
            'entregue': 0,
            'sem_rota': 0,
            'proximo_ciclo': len(pedidos_proximo_ciclo),
            'rotas_ativas': len({(pedido.rota_entrega or '').strip() for pedido in pedidos if (pedido.rota_entrega or '').strip()}),
            'veiculos_configurados': len(veiculos_configurados),
        }
        for pedido in pedidos:
            if pedido.entrega_concluida_em:
                resumo_roteirizacao['entregue'] += 1
            elif pedido.saiu_para_entrega_em:
                resumo_roteirizacao['em_rota'] += 1
            else:
                resumo_roteirizacao['aguardando'] += 1

            if not (pedido.rota_entrega or '').strip():
                resumo_roteirizacao['sem_rota'] += 1

        return render_template(
            'vendas/pedidos/roteirizacao_entrega.html',
            pedidos=pedidos,
            empresa=empresa,
            rota_filtro=rota_filtro,
            status_filtro=status_filtro,
            rotas_disponiveis=rotas_disponiveis,
            regras_roteirizacao=regras_roteirizacao,
            veiculos_configurados=veiculos_configurados,
            resumo_roteirizacao=resumo_roteirizacao,
            pedidos_proximo_ciclo=pedidos_proximo_ciclo,
            corte_roteirizacao=corte_roteirizacao,
        )

    @app.route('/pedidos/roteirizacao-entrega/otimizar', methods=['POST'])
    @require_role(*separacao_entrega_roles)
    def otimizar_rota_entrega():
        empresa = _obter_empresa_config()
        if not _separacao_entrega_ativa(empresa):
            flash('Separacao para entrega esta desativada na configuracao da empresa.', 'warning')
            return redirect(url_for('listar_pedidos'))

        acao_otimizacao = (request.form.get('acao_otimizacao') or 'ordem').strip().lower()
        regras_roteirizacao = _regras_roteirizacao_do_form(request, empresa)
        empresa.entrega_regras_roteirizacao_json = json.dumps(regras_roteirizacao, ensure_ascii=False)

        try:
            if acao_otimizacao == 'distribuir_automatico':
                pedidos_base = Pedido.query.filter(
                    Pedido.origem.in_(_origens_separacao_entrega(empresa)),
                    Pedido.separacao_entrega_concluida.is_(True),
                    Pedido.status.in_(DELIVERY_SEPARATION_STATUSES),
                ).order_by(Pedido.criado_em.asc()).all()
                pedidos_disponiveis, pedidos_proximo_ciclo, corte_roteirizacao = _separar_pedidos_por_corte_roteirizacao(
                    pedidos_base,
                    empresa,
                )
                if not pedidos_disponiveis:
                    if corte_roteirizacao['ativo'] and pedidos_proximo_ciclo:
                        flash(
                            f'Nenhum pedido liberado para o ciclo atual. {len(pedidos_proximo_ciclo)} pedido(s) ficaram para o proximo ciclo apos o corte das {corte_roteirizacao["horario"]}.',
                            'warning',
                        )
                    else:
                        flash('Nenhum pedido disponivel para roteirizacao automatica.', 'warning')
                    return redirect(url_for('listar_roteirizacao_entrega'))
                veiculos = _carregar_veiculos_config(empresa.entrega_veiculos_json)
                total_alocados = _distribuir_pedidos_automaticamente(
                    pedidos_disponiveis,
                    veiculos,
                    regras_roteirizacao,
                    empresa,
                )
                db.session.commit()
                flash(f'Distribuicao automatica concluida com {total_alocados} pedido(s) roteirizado(s).', 'success')
                if corte_roteirizacao['ativo'] and pedidos_proximo_ciclo:
                    flash(
                        f'{len(pedidos_proximo_ciclo)} pedido(s) ficaram fora do ciclo atual por ultrapassarem o horario de fechamento das {corte_roteirizacao["horario"]}.',
                        'info',
                    )
                return redirect(url_for('listar_roteirizacao_entrega'))

            rota = (request.form.get('rota') or '').strip()
            if not rota:
                db.session.rollback()
                flash('Informe a rota para otimizar a sequencia.', 'warning')
                return redirect(url_for('listar_roteirizacao_entrega'))

            pedidos_rota = Pedido.query.filter(
                Pedido.rota_entrega == rota,
                Pedido.separacao_entrega_concluida.is_(True),
                Pedido.status.in_(DELIVERY_SEPARATION_STATUSES),
            ).order_by(Pedido.ordem_rota.asc().nullslast(), Pedido.criado_em.asc()).all()

            ordem = 1
            for pedido in pedidos_rota:
                pedido.ordem_rota = ordem
                ordem += 1

            db.session.commit()
            flash(f'Rota "{rota}" otimizada com {len(pedidos_rota)} paradas.', 'success')
            return redirect(url_for('listar_roteirizacao_entrega', rota=rota))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao otimizar rota: {str(e)}', 'error')

        return redirect(url_for('listar_roteirizacao_entrega'))

    @app.route('/pedidos/<int:pedido_id>/despacho-entrega', methods=['POST'])
    @require_role(*separacao_entrega_roles)
    def atualizar_despacho_entrega(pedido_id):
        pedido = Pedido.query.get_or_404(pedido_id)
        empresa = _obter_empresa_config()
        if not _pedido_pronto_para_roteirizacao(pedido):
            flash('Pedido nao esta pronto para despacho de entrega.', 'warning')
            return redirect(url_for('listar_roteirizacao_entrega'))

        acao = (request.form.get('acao') or '').strip().lower()
        try:
            if acao == 'sair':
                pedido.saiu_para_entrega_em = datetime.utcnow()
                if not pedido.motorista_nome:
                    pedido.motorista_nome = empresa.entrega_motorista_padrao
                flash(f'Pedido #{pedido.id} marcado como saiu para entrega.', 'success')
            elif acao == 'entregar':
                if not pedido.saiu_para_entrega_em:
                    pedido.saiu_para_entrega_em = datetime.utcnow()
                pedido.entrega_concluida_em = datetime.utcnow()
                pedido.transitar_para(Pedido.STATUS_ENTREGUE)
                flash(f'Pedido #{pedido.id} marcado como entregue.', 'success')
            elif acao == 'reabrir':
                pedido.entrega_concluida_em = None
                pedido.saiu_para_entrega_em = None
                flash(f'Pedido #{pedido.id} retornou para aguardando despacho.', 'success')
            else:
                flash('Acao de despacho invalida.', 'warning')
                return redirect(url_for('listar_roteirizacao_entrega'))

            db.session.commit()
            _publicar_evento_expedicao(pedido, f'despacho_{acao}')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar despacho: {str(e)}', 'error')

        return redirect(url_for('listar_roteirizacao_entrega', rota=(pedido.rota_entrega or '')))

    @app.route('/pedidos/<int:pedido_id>/separacao-entrega', methods=['POST'])
    @require_role(*separacao_entrega_roles)
    def atualizar_separacao_entrega_pedido(pedido_id):
        empresa = _obter_empresa_config()
        if not _separacao_entrega_ativa(empresa):
            flash('Separacao para entrega esta desativada na configuracao da empresa.', 'warning')
            return redirect(request.referrer or url_for('listar_pedidos'))

        pedido = Pedido.query.get_or_404(pedido_id)
        if pedido.origem not in _origens_separacao_entrega(empresa):
            flash('Pedido fora da fila configurada para separacao de entrega.', 'warning')
            return redirect(request.referrer or url_for('listar_separacao_entrega'))

        acao = (request.form.get('acao') or 'concluir').strip().lower()
        try:
            if acao == 'reabrir':
                pedido.marcar_separacao_entrega(False)
                mensagem = f'Pedido #{pedido.id} retornou para fila de separacao.'
            else:
                rota_entrega = (request.form.get('rota_entrega') or '').strip() or None
                ordem_rota = _to_int(request.form.get('ordem_rota'), None)
                local_saida = (request.form.get('local_saida') or '').strip() or None
                veiculo_tipo = (request.form.get('veiculo_tipo') or '').strip() or None
                veiculo_placa = (request.form.get('veiculo_placa') or '').strip().upper() or None
                veiculo_cadastrado = (request.form.get('veiculo_cadastrado') or '').strip()
                motorista_nome = (request.form.get('motorista_nome') or '').strip() or None
                empresa_terceirizada = (request.form.get('empresa_terceirizada') or '').strip() or None
                nota_fiscal_numero = (request.form.get('nota_fiscal_numero') or '').strip() or None
                nota_fiscal_chave = (request.form.get('nota_fiscal_chave') or '').strip() or None
                emitir_nota = (request.form.get('emitir_nota') == 'on')

                if veiculo_cadastrado:
                    nome_veiculo_cfg, placa_veiculo_cfg = _parse_veiculo_cadastrado(veiculo_cadastrado)
                    if nome_veiculo_cfg:
                        veiculo_tipo = nome_veiculo_cfg
                    if placa_veiculo_cfg and not veiculo_placa:
                        veiculo_placa = placa_veiculo_cfg

                pedido.rota_entrega = rota_entrega
                pedido.ordem_rota = ordem_rota
                pedido.local_saida = local_saida or empresa.entrega_local_saida_padrao
                pedido.veiculo_tipo = veiculo_tipo or empresa.entrega_veiculo_padrao
                pedido.veiculo_placa = veiculo_placa
                pedido.motorista_nome = motorista_nome or empresa.entrega_motorista_padrao
                pedido.empresa_terceirizada = empresa_terceirizada
                pedido.nota_fiscal_numero = nota_fiscal_numero
                pedido.nota_fiscal_chave = nota_fiscal_chave
                if emitir_nota and empresa.emissao_nota_entrega_ativa is not False:
                    pedido.nota_fiscal_emitida_em = datetime.utcnow()

                pedido.marcar_separacao_entrega(True)
                mensagem = f'Pedido #{pedido.id} marcado como separado.'
                corte_roteirizacao = _config_corte_roteirizacao(empresa)
                referencia_roteirizacao = _referencia_pedido_roteirizacao(pedido)
                if (
                    corte_roteirizacao['ativo']
                    and referencia_roteirizacao
                    and referencia_roteirizacao > corte_roteirizacao['corte_do_dia']
                ):
                    mensagem += f' Ficara disponivel para o proximo ciclo de roteirizacao apos o corte das {corte_roteirizacao["horario"]}.'
            db.session.commit()
            _publicar_evento_expedicao(pedido, f'separacao_{acao}')
            flash(mensagem, 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar separacao de entrega: {str(e)}', 'error')
        return redirect(request.referrer or url_for('listar_separacao_entrega'))

    @app.route('/pedidos/<int:pedido_id>/etiqueta-entrega')
    @require_role(*separacao_entrega_roles)
    def imprimir_etiqueta_entrega_pedido(pedido_id):
        empresa = _obter_empresa_config()
        if not _emissao_etiqueta_entrega_ativa(empresa):
            flash('Emissao de etiquetas de entrega esta desativada na configuracao da empresa.', 'warning')
            return redirect(request.referrer or url_for('listar_pedidos'))

        pedido = Pedido.query.options(
            selectinload(Pedido.caixa),
            selectinload(Pedido.mesa),
            selectinload(Pedido.itens).selectinload(ItemPedido.produto),
        ).get_or_404(pedido_id)
        if pedido.origem not in _origens_separacao_entrega(empresa):
            flash('Pedido fora da fila configurada para etiquetas de entrega.', 'warning')
            return redirect(request.referrer or url_for('listar_pedidos'))

        try:
            pedido.marcar_etiqueta_entrega_emitida()
            db.session.commit()
            _publicar_evento_expedicao(pedido, 'etiqueta_emitida')
        except Exception:
            db.session.rollback()

        return render_template(
            'vendas/pedidos/etiqueta_entrega.html',
            pedido=pedido,
            empresa=empresa,
        )

    @app.route('/pedidos/pendentes')
    @require_role(*vendas_operacao_roles)
    def listar_pedidos_pendentes():
        pendentes = Pedido.query.filter(Pedido.status.in_(['aberto', 'em_preparo'])).order_by(Pedido.criado_em.desc()).all()
        data = [
            {
                'id': p.id,
                'mesa': p.mesa.numero if p.mesa else None,
                'status': p.status,
                'total': p.total,
                'criado_em': p.criado_em.isoformat()
            } for p in pendentes
        ]
        return jsonify(data)

    @app.route('/pedidos/<int:pedido_id>/status', methods=['POST'])
    @require_role(*vendas_operacao_roles)
    def alterar_status_pedido(pedido_id):
        novo_status = _parse_status(request.form.get('status'), default='')
        if not novo_status:
            flash('Status invalido.', 'danger')
            return redirect(url_for('listar_pedidos'))

        pedido = Pedido.query.get_or_404(pedido_id)
        try:
            _aplicar_transicao_status(pedido, novo_status)
            db.session.commit()
            status_label = 'venda concluida' if novo_status == 'fechado' else novo_status
            flash(f'Pedido {pedido.id} atualizado para {status_label}.', 'success')
        except AppError as exc:
            db.session.rollback()
            flash(str(exc), 'danger')

        return redirect(request.referrer or url_for('listar_pedidos'))

    @app.route('/pedidos/novo', methods=['GET', 'POST'])
    @require_role(*vendas_operacao_roles)
    def novo_pedido():
        produtos = Produto.query.filter_by(ativo=True).all()
        atendimento_mesas_ativo = _atendimento_mesas_ativo()
        mesas = Mesa.query.all() if atendimento_mesas_ativo else []
        caixas = Caixa.query.filter_by(aberto=True).all()
        if request.method == 'POST':
            try:
                mesa_id = request.form.get('mesa_id', type=int) or None
                if not atendimento_mesas_ativo:
                    mesa_id = None
                caixa_id = request.form.get('caixa_id', type=int) or None
                observacoes = request.form.get('observacoes')

                if caixa_id:
                    caixa = Caixa.query.get(caixa_id)
                    if not caixa or not caixa.aberto:
                        flash('Caixa invalida ou fechada.', 'danger')
                        return redirect(url_for('novo_pedido'))

                pedido = Pedido(
                    mesa_id=mesa_id,
                    caixa_id=caixa_id,
                    garcom_id=_garcom_logado_id() if atendimento_mesas_ativo else None,
                    observacoes=observacoes,
                    status='aberto',
                    estoque_processado=False,
                    financeiro_processado=False
                )
                db.session.add(pedido)
                db.session.flush()

                itens_validos = 0
                for i in range(int(request.form.get('item_count', 0))):
                    pid = request.form.get(f'produto_{i}')
                    qty = request.form.get(f'quantidade_{i}', 1)
                    if not pid:
                        continue
                    normalizado, erro = _normalizar_item_payload({'produto_id': pid, 'quantidade': qty})
                    if erro:
                        continue

                    produto = normalizado['produto']
                    quantidade = normalizado['quantidade']
                    ip = ItemPedido(
                        pedido_id=pedido.id,
                        produto_id=produto.id,
                        quantidade=quantidade,
                        preco_unitario=produto.preco_venda
                    )
                    db.session.add(ip)
                    itens_validos += 1

                if itens_validos == 0:
                    raise ValueError('Adicione ao menos um item valido ao pedido.')

                _recalcular_total_pedido(pedido)
                if atendimento_mesas_ativo and pedido.mesa:
                    pedido.mesa.status = 'ocupada'
                db.session.commit()
                flash('Pedido criado com sucesso!', 'success')
                return redirect(url_for('listar_pedidos'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao criar pedido: {str(e)}', 'error')
        return render_template(
            'vendas/pedidos/novo_pedido.html',
            produtos=produtos,
            mesas=mesas,
            caixas=caixas,
            atendimento_mesas_ativo=atendimento_mesas_ativo
        )

    @app.route('/pedidos/<int:pedido_id>/editar', methods=['GET', 'POST'])
    @require_role(*vendas_operacao_roles)
    def editar_pedido(pedido_id):
        pedido = Pedido.query.get_or_404(pedido_id)
        produtos = Produto.query.filter_by(ativo=True).all()
        atendimento_mesas_ativo = _atendimento_mesas_ativo()
        mesas = Mesa.query.all() if atendimento_mesas_ativo else []
        caixas = Caixa.query.all()
        empresa = _obter_empresa_config()
        metodos_pagamento_pdv = load_payment_options(empresa.pagamentos_pdv_json, 'pdv')
        metodos_pagamento_pdv_map = payment_methods_map(empresa.pagamentos_pdv_json, 'pdv')
        if request.method == 'POST':
            try:
                status_atual = _parse_status(pedido.status)
                novo_status = _parse_status(request.form.get('status', pedido.status), default=status_atual)
                if status_atual in ORDER_IMMUTABLE_STATUSES and novo_status != status_atual:
                    raise ValueError(f'Pedido {status_atual} e imutavel.')

                pedido.mesa_id = request.form.get('mesa_id', type=int) or None
                if not atendimento_mesas_ativo:
                    pedido.mesa_id = None
                    pedido.garcom_id = None
                pedido.caixa_id = request.form.get('caixa_id', type=int) or None
                pedido.observacoes = request.form.get('observacoes', pedido.observacoes)

                if pedido.caixa_id:
                    caixa = Caixa.query.get(pedido.caixa_id)
                    if not caixa:
                        raise ValueError('Caixa informada nao existe.')
                    if novo_status == 'fechado' and not caixa.aberto:
                        raise ValueError('Caixa informada esta fechada.')

                if status_atual not in ORDER_IMMUTABLE_STATUSES:
                    pedido.itens.clear()
                    itens_validos = 0
                    for i in range(int(request.form.get('item_count', 0))):
                        pid = request.form.get(f'produto_{i}')
                        qty = request.form.get(f'quantidade_{i}', 1)
                        if not pid:
                            continue
                        normalizado, erro = _normalizar_item_payload({'produto_id': pid, 'quantidade': qty})
                        if erro:
                            continue
                        produto = normalizado['produto']
                        quantidade = normalizado['quantidade']
                        ip = ItemPedido(
                            pedido_id=pedido.id,
                            produto_id=produto.id,
                            quantidade=quantidade,
                            preco_unitario=produto.preco_venda
                        )
                        db.session.add(ip)
                        itens_validos += 1
                    if itens_validos == 0:
                        raise ValueError('Adicione ao menos um item valido no pedido.')

                    _recalcular_total_pedido(pedido)

                metodo = request.form.get('metodo_pagamento')
                if metodo:
                    metodo_texto, valor_pago = _build_payment_data(
                        metodo_raw=metodo,
                        valor_raw=request.form.get('valor_pago'),
                        total_pedido=pedido.total,
                        payment_methods=metodos_pagamento_pdv_map,
                        split_raw={
                            'dinheiro': request.form.get('valor_dinheiro'),
                            'cartao': request.form.get('valor_cartao')
                        },
                        cliente_crediario=request.form.get('cliente_crediario', '')
                    )
                    pedido.metodo_pagamento = metodo_texto
                    pedido.valor_pago = valor_pago
                else:
                    pedido.metodo_pagamento = None
                    pedido.valor_pago = None

                _aplicar_transicao_status(pedido, novo_status)
                db.session.commit()
                flash('Pedido atualizado com sucesso!', 'success')
                return redirect(url_for('listar_pedidos'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao atualizar pedido: {str(e)}', 'error')
        return render_template(
            'vendas/pedidos/editar_pedido.html',
            pedido=pedido,
            produtos=produtos,
            mesas=mesas,
            caixas=caixas,
            atendimento_mesas_ativo=atendimento_mesas_ativo,
            metodos_pagamento_pdv=metodos_pagamento_pdv,
            metodo_pagamento_atual_id=infer_payment_method_id(pedido.metodo_pagamento, metodos_pagamento_pdv),
        )

    @app.route('/pedidos/<int:pedido_id>/deletar', methods=['POST'])
    @require_role(*vendas_gestao_roles)
    def deletar_pedido(pedido_id):
        pedido = Pedido.query.get_or_404(pedido_id)
        try:
            db.session.delete(pedido)
            db.session.commit()
            flash('Pedido excluido.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao excluir pedido: {str(e)}', 'error')
        return redirect(url_for('listar_pedidos'))

    @app.route('/pedidos/<int:pedido_id>/comprovante')
    @require_role(*vendas_operacao_roles)
    def visualizar_comprovante_pedido(pedido_id):
        pedido = Pedido.query.get_or_404(pedido_id)
        empresa = EmpresaConfig.query.first()
        troco_repassado = None
        if pedido.valor_pago is not None:
            metodo = (pedido.metodo_pagamento or '').strip().lower()
            if 'dinheiro' in metodo or 'dividido' in metodo:
                troco_repassado = max(float(pedido.valor_pago or 0.0) - float(pedido.total or 0.0), 0.0)
            else:
                troco_repassado = 0.0
        return render_template(
            'vendas/pedidos/comprovante.html',
            pedido=pedido,
            empresa=empresa,
            troco_repassado=troco_repassado,
        )

    @app.route('/pedidos/<int:pedido_id>/detalhes')
    @require_role(*vendas_operacao_roles)
    def detalhes_pedido(pedido_id):
        pedido = Pedido.query.get_or_404(pedido_id)
        empresa = _obter_empresa_config()
        separacao_ativa = _separacao_entrega_ativa(empresa)
        unir_off = bool(empresa and empresa.separacao_entrega_unir_vendas_off)
        origem_elegivel_separacao = (pedido.origem == 'site') or (unir_off and pedido.origem == 'interno')

        funcionario = Funcionario.query.get(session.get('funcionario_id')) if session.get('funcionario_id') else None
        paginas_permitidas = None
        if funcionario and funcionario.ativo and funcionario.role != 'admin' and funcionario.controle_acesso_ativo:
            paginas_permitidas = _paginas_efetivas_funcionario(funcionario)
        return render_template(
            'vendas/pedidos/detalhes_pedido.html',
            pedido=pedido,
            empresa=empresa,
            status_transitions=ORDER_ALLOWED_TRANSITIONS,
            separacao_ativa=separacao_ativa,
            origem_elegivel_separacao=origem_elegivel_separacao,
            etiquetas_ativas=_emissao_etiqueta_entrega_ativa(empresa),
            pode_editar=_usuario_tem_acesso_endpoint('editar_pedido', funcionario, paginas_permitidas),
            pode_alterar_status=_usuario_tem_acesso_endpoint('alterar_status_pedido', funcionario, paginas_permitidas),
            pode_excluir=_usuario_tem_acesso_endpoint('deletar_pedido', funcionario, paginas_permitidas),
            pode_atualizar_separacao=_usuario_tem_acesso_endpoint('atualizar_separacao_entrega_pedido', funcionario, paginas_permitidas),
            pode_imprimir_etiqueta=_usuario_tem_acesso_endpoint('imprimir_etiqueta_entrega_pedido', funcionario, paginas_permitidas),
            pode_ver_comprovante=_usuario_tem_acesso_endpoint('visualizar_comprovante_pedido', funcionario, paginas_permitidas),
        )

    @app.route('/pdv')
    @require_role(*vendas_operacao_roles)
    def pdv():
        """Interface de PDV (Ponto de Venda) para o operador de caixa"""
        atendimento_mesas_ativo = _atendimento_mesas_ativo()
        empresa = _obter_empresa_config()
        produtos = Produto.query.filter_by(ativo=True).order_by(Produto.nome).all()
        caixas_abertas = Caixa.query.filter_by(aberto=True).all()
        mesas = Mesa.query.all() if atendimento_mesas_ativo else []
        garcons = Garcom.query.filter_by(ativo=True).order_by(Garcom.nome.asc()).all() if atendimento_mesas_ativo else []
        metodos_pagamento_pdv = load_payment_options(empresa.pagamentos_pdv_json, 'pdv')
        return render_template(
            'vendas/pdv.html',
            produtos=produtos,
            caixas_abertas=caixas_abertas,
            mesas=mesas,
            garcons=garcons,
            atendimento_mesas_ativo=atendimento_mesas_ativo,
            metodos_pagamento_pdv=metodos_pagamento_pdv,
            metodo_pagamento_pdv_padrao=default_payment_id(empresa.pagamentos_pdv_json, 'pdv') or 'dinheiro',
        )

    @app.route('/api/pedidos/criar', methods=['POST'])
    @require_role(*vendas_operacao_roles)
    def criar_pedido_api():
        """API para criar pedido via AJAX."""
        try:
            atendimento_mesas_ativo = _atendimento_mesas_ativo()
            data = request.get_json(silent=True) or {}
            caixa_id = data.get('caixa_id')
            mesa_id = data.get('mesa_id') or None
            if not atendimento_mesas_ativo:
                mesa_id = None
            itens = data.get('itens', [])

            if not caixa_id or not itens:
                return json_response(False, 'Caixa e produtos sao obrigatorios.', status=400, code='validation_error')

            caixa = Caixa.query.get(caixa_id)
            if not caixa or not caixa.aberto:
                return json_response(False, 'Caixa nao esta aberta.', status=409, code='business_rule')

            pedido = Pedido(
                mesa_id=mesa_id,
                caixa_id=caixa_id,
                garcom_id=_garcom_logado_id() if atendimento_mesas_ativo else None,
                status='aberto',
                estoque_processado=False,
                financeiro_processado=False
            )
            db.session.add(pedido)
            db.session.flush()

            itens_validos = 0
            for item in itens:
                normalizado, erro = _normalizar_item_payload(item)
                if erro:
                    continue

                produto = normalizado['produto']
                quantidade = normalizado['quantidade']
                ip = ItemPedido(
                    pedido_id=pedido.id,
                    produto_id=produto.id,
                    quantidade=quantidade,
                    preco_unitario=produto.preco_venda
                )
                db.session.add(ip)
                itens_validos += 1

            if itens_validos == 0:
                db.session.rollback()
                return json_response(False, 'Nenhum item valido para criar o pedido.', status=400, code='validation_error')

            _recalcular_total_pedido(pedido)

            mesa = None
            if atendimento_mesas_ativo and mesa_id:
                mesa = Mesa.query.get(mesa_id)
                if mesa:
                    mesa.status = 'ocupada'

            db.session.commit()
            try:
                publish_alert({
                    'pedido_id': pedido.id,
                    'mesa': mesa.numero if mesa else None,
                    'criado_em': pedido.criado_em.isoformat() if pedido.criado_em else datetime.utcnow().isoformat(),
                    'itens': [
                        {'quantidade': ip.quantidade, 'produto': ip.produto.nome if ip.produto else ''}
                        for ip in pedido.itens
                    ]
                })
            except Exception:
                pass

            return json_response(
                True,
                f'Pedido #{pedido.id} criado com sucesso.',
                data={'pedido_id': pedido.id, 'total': float(pedido.total or 0.0)}
            )
        except Exception as e:
            db.session.rollback()
            return json_response(False, str(e), status=500, code='internal_error')

    @app.route('/api/pedidos/<int:pedido_id>/finalizar', methods=['POST'])
    @require_role(*vendas_operacao_roles)
    def finalizar_pedido_api(pedido_id):
        """API para finalizar pedido via AJAX."""
        try:
            pedido = Pedido.query.get_or_404(pedido_id)
            if _parse_status(pedido.status) in ORDER_IMMUTABLE_STATUSES:
                return json_response(False, f'Pedido ja esta {pedido.status}.', status=409, code='business_rule')

            dados = request.get_json(silent=True) or {}
            metodo = dados.get('metodo_pagamento')
            empresa = _obter_empresa_config()
            metodos_pagamento_pdv_map = payment_methods_map(empresa.pagamentos_pdv_json, 'pdv')
            if metodo:
                metodo_texto, valor_pago = _build_payment_data(
                    metodo_raw=metodo,
                    valor_raw=dados.get('valor_pago'),
                    total_pedido=pedido.total,
                    payment_methods=metodos_pagamento_pdv_map,
                    split_raw=dados.get('split_pagamento'),
                    cliente_crediario=dados.get('cliente_crediario', '')
                )
                pedido.metodo_pagamento = metodo_texto
                pedido.valor_pago = valor_pago

            _aplicar_transicao_status(pedido, 'fechado')
            db.session.commit()

            return json_response(
                True,
                'Pedido finalizado com sucesso.',
                data={
                    'pedido_id': pedido_id,
                    'metodo_pagamento': pedido.metodo_pagamento,
                    'valor_pago': pedido.valor_pago,
                    'status': pedido.status
                }
            )
        except AppError as e:
            db.session.rollback()
            status_code, code = _http_status_for_order_error(str(e))
            return json_response(False, str(e), status=getattr(e, 'status_code', status_code), code=getattr(e, 'code', code))
        except Exception as e:
            db.session.rollback()
            return json_response(False, str(e), status=500, code='internal_error')

    @app.route('/api/pedidos/aberto/<int:caixa_id>')
    @require_role(*vendas_operacao_roles)
    def get_pedido_aberto(caixa_id):
        """Retorna pedido aberto para determinada caixa, se existir"""
        pedido = Pedido.query.filter_by(caixa_id=caixa_id, status='aberto').first()
        if not pedido:
            return jsonify({'exists': False})
        itens = []
        for ip in pedido.itens:
            itens.append({
                'produto_id': ip.produto_id,
                'nome': ip.produto.nome,
                'quantidade': ip.quantidade,
                'preco': ip.preco_unitario
            })
        return jsonify({
            'exists': True,
            'pedido_id': pedido.id,
            'itens': itens,
            'total': pedido.total
        })

    @app.route('/api/pedidos/em-aberto')
    @require_role(*vendas_operacao_roles)
    def listar_pedidos_em_aberto_pdv():
        """Lista pedidos nao finalizados para selecao no PDV (todas as caixas ou filtrado)."""
        atendimento_mesas_ativo = _atendimento_mesas_ativo()
        status_filtro = (request.args.get('status') or '').strip().lower()
        mesa_id = request.args.get('mesa_id', type=int)
        garcom_id = request.args.get('garcom_id', type=int)
        caixa_id = request.args.get('caixa_id', type=int)

        query = Pedido.query.filter(
            Pedido.status.in_(['aberto', 'em_preparo', 'entregue'])
        )

        if status_filtro in {'aberto', 'em_preparo', 'entregue'}:
            query = query.filter(Pedido.status == status_filtro)
        if caixa_id:
            query = query.filter(Pedido.caixa_id == caixa_id)
        if atendimento_mesas_ativo and mesa_id:
            query = query.filter(Pedido.mesa_id == mesa_id)
        if atendimento_mesas_ativo and garcom_id:
            query = query.filter(Pedido.garcom_id == garcom_id)

        pedidos = query.order_by(Pedido.criado_em.desc()).all()

        return jsonify({
            'success': True,
            'pedidos': [
                {
                    'id': p.id,
                    'status': p.status,
                    'caixa_id': p.caixa_id,
                    'caixa_nome': p.caixa.nome if p.caixa else None,
                    'mesa_id': p.mesa_id,
                    'mesa_numero': p.mesa.numero if p.mesa else None,
                    'garcom_id': p.garcom_id,
                    'garcom_nome': p.garcom.nome if p.garcom else None,
                    'cliente_nome': p.cliente_nome,
                    'origem': p.origem,
                    'total': p.total or 0.0,
                    'criado_em': p.criado_em.isoformat() if p.criado_em else None
                }
                for p in pedidos
            ]
        })

    @app.route('/api/pedidos/caixa/<int:caixa_id>/em-aberto')
    @require_role(*vendas_operacao_roles)
    def listar_pedidos_caixa_em_aberto(caixa_id):
        """Compat: mantem endpoint legado por caixa."""
        atendimento_mesas_ativo = _atendimento_mesas_ativo()
        status_filtro = (request.args.get('status') or '').strip().lower()
        mesa_id = request.args.get('mesa_id', type=int)
        garcom_id = request.args.get('garcom_id', type=int)

        query = Pedido.query.filter(
            Pedido.caixa_id == caixa_id,
            Pedido.status.in_(['aberto', 'em_preparo', 'entregue'])
        )

        if status_filtro in {'aberto', 'em_preparo', 'entregue'}:
            query = query.filter(Pedido.status == status_filtro)
        if atendimento_mesas_ativo and mesa_id:
            query = query.filter(Pedido.mesa_id == mesa_id)
        if atendimento_mesas_ativo and garcom_id:
            query = query.filter(Pedido.garcom_id == garcom_id)

        pedidos = query.order_by(Pedido.criado_em.desc()).all()
        return jsonify({
            'success': True,
            'pedidos': [
                {
                    'id': p.id,
                    'status': p.status,
                    'caixa_id': p.caixa_id,
                    'caixa_nome': p.caixa.nome if p.caixa else None,
                    'mesa_id': p.mesa_id,
                    'mesa_numero': p.mesa.numero if p.mesa else None,
                    'garcom_id': p.garcom_id,
                    'garcom_nome': p.garcom.nome if p.garcom else None,
                    'cliente_nome': p.cliente_nome,
                    'origem': p.origem,
                    'total': p.total or 0.0,
                    'criado_em': p.criado_em.isoformat() if p.criado_em else None
                }
                for p in pedidos
            ]
        })

    @app.route('/api/pedidos/<int:pedido_id>/detalhes-json')
    @require_role(*vendas_operacao_roles)
    def detalhes_pedido_api(pedido_id):
        """Retorna detalhes do pedido para carregar no PDV."""
        pedido = Pedido.query.get_or_404(pedido_id)

        itens = []
        for ip in pedido.itens:
            nome_produto = ip.produto.nome if ip.produto else f'Produto {ip.produto_id}'
            itens.append({
                'produto_id': ip.produto_id,
                'nome': nome_produto,
                'quantidade': ip.quantidade,
                'preco': ip.preco_unitario
            })

        return jsonify({
            'success': True,
            'pedido': {
                'id': pedido.id,
                'status': pedido.status,
                'mesa_id': pedido.mesa_id,
                'mesa_numero': pedido.mesa.numero if pedido.mesa else None,
                'garcom_id': pedido.garcom_id,
                'garcom_nome': pedido.garcom.nome if pedido.garcom else None,
                'cliente_nome': pedido.cliente_nome,
                'total': pedido.total or 0.0,
                'itens': itens
            }
        })

    @app.route('/api/pedidos/<int:pedido_id>/adicionar', methods=['POST'])
    @require_role(*vendas_operacao_roles)
    def adicionar_itens_pedido_api(pedido_id):
        """Adiciona itens a um pedido ja aberto."""
        pedido = Pedido.query.get_or_404(pedido_id)
        if _parse_status(pedido.status) != 'aberto':
            return json_response(False, 'Somente pedidos com status aberto podem receber itens.', status=409, code='business_rule')

        dados = request.get_json(silent=True) or {}
        itens = dados.get('itens', [])
        if not itens:
            return json_response(False, 'Nenhum item enviado.', status=400, code='validation_error')

        itens_validos = 0
        try:
            for it in itens:
                normalizado, erro = _normalizar_item_payload(it)
                if erro:
                    continue
                prod = normalizado['produto']
                qty = normalizado['quantidade']
                ip = ItemPedido(
                    pedido_id=pedido.id,
                    produto_id=prod.id,
                    quantidade=qty,
                    preco_unitario=prod.preco_venda
                )
                db.session.add(ip)
                itens_validos += 1

            if itens_validos == 0:
                return json_response(False, 'Nenhum item valido para adicionar.', status=400, code='validation_error')

            _recalcular_total_pedido(pedido)
            db.session.commit()
            return json_response(
                True,
                'Itens adicionados com sucesso.',
                data={'pedido_id': pedido.id, 'total': float(pedido.total or 0.0)}
            )
        except Exception as e:
            db.session.rollback()
            return json_response(False, str(e), status=500, code='internal_error')

    @app.route('/eventos/pedidos')
    @require_role(*vendas_operacao_roles)
    def sse_pedidos():
        return Response(sse_stream(), mimetype='text/event-stream')





```


### Arquivo: `run.py`
- Linhas: 9
- Tamanho: 0.1 KB
- Status: completo

```python
from app import create_app


app = create_app()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

```


### Arquivo: `security.py`
- Linhas: 110
- Tamanho: 3.1 KB
- Status: completo

```python
import secrets
from functools import wraps
from typing import Iterable, Optional, Tuple

from flask import abort, jsonify, request, session

CSRF_SESSION_KEY = '_csrf_token'
CSRF_HEADER_CANDIDATES = ('X-CSRF-Token', 'X-CSRFToken')
SAFE_METHODS = {'GET', 'HEAD', 'OPTIONS', 'TRACE'}


def json_response(success, message, *, status=200, data=None, code=None):
    payload = {'success': bool(success), 'message': message}
    if data is not None:
        payload['data'] = data
    if code:
        payload['code'] = code
    return jsonify(payload), status


def is_json_request() -> bool:
    if request.path.startswith('/api/'):
        return True
    accepts = request.headers.get('Accept', '')
    return 'application/json' in accepts.lower()


def ensure_csrf_token() -> str:
    token = session.get(CSRF_SESSION_KEY)
    if not token:
        token = secrets.token_urlsafe(32)
        session[CSRF_SESSION_KEY] = token
        session.modified = True
    return token


def csrf_input_tag() -> str:
    token = ensure_csrf_token()
    return f'<input type="hidden" name="csrf_token" value="{token}">'


def _extract_request_csrf_token() -> Optional[str]:
    for header_name in CSRF_HEADER_CANDIDATES:
        header_token = request.headers.get(header_name)
        if header_token:
            return header_token

    form_token = request.form.get('csrf_token')
    if form_token:
        return form_token

    json_payload = request.get_json(silent=True) or {}
    json_token = json_payload.get('csrf_token') if isinstance(json_payload, dict) else None
    if json_token:
        return json_token

    return None


def validate_csrf_request() -> Tuple[bool, str]:
    expected_token = session.get(CSRF_SESSION_KEY)
    if not expected_token:
        return False, 'Sessao sem token CSRF valido. Recarregue a pagina e tente novamente.'

    informed_token = _extract_request_csrf_token()
    if not informed_token:
        return False, 'Token CSRF ausente.'

    if not secrets.compare_digest(str(expected_token), str(informed_token)):
        return False, 'Token CSRF invalido.'

    return True, ''


def csrf_protect_request(*, exempt_endpoints: Optional[Iterable[str]] = None):
    if request.method in SAFE_METHODS:
        return None

    endpoint = request.endpoint or ''
    if endpoint.startswith('static'):
        return None

    if exempt_endpoints and endpoint in set(exempt_endpoints):
        return None

    ok, reason = validate_csrf_request()
    if ok:
        return None

    if is_json_request():
        return json_response(False, reason, status=400, code='csrf_invalid')

    abort(400, description=reason)


def role_required(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            role = (session.get('funcionario_role') or '').strip().lower()
            if role not in roles:
                if is_json_request():
                    return json_response(False, 'Sem permissao para executar esta operacao.', status=403, code='forbidden')
                abort(403)
            return fn(*args, **kwargs)

        return wrapper

    return decorator

```


### Arquivo: `seed_data.py`
- Linhas: 231
- Tamanho: 10.0 KB
- Status: completo

```python
"""
Script para popular o banco de dados com dados de teste.
Execute: python seed_data.py
"""
import sys
import secrets

from app import app, db
from models import (
    Categoria, Produto, Fornecedor, Funcionario, Mesa, Caixa, 
    Movimentacao, PermissaoAcesso, Pedido
)

def seed_database():
    """Popula o banco com dados de teste"""
    
    with app.app_context():
        # Limpar dados existentes
        print("🗑️  Limpando dados existentes...")
        db.drop_all()
        db.create_all()
        
        print("📝 Criando funcionários...")
        # Criar funcionários
        admin = Funcionario(
            nome="Administrador",
            email="admin@conveniencia.local",
            role="admin",
            ativo=True
        )
        admin.set_password("admin123")
        
        gerente = Funcionario(
            nome="Gerente",
            email="gerente@conveniencia.local",
            role="gerente",
            ativo=True
        )
        gerente.set_password("gerente123")
        
        operador1 = Funcionario(
            nome="João Operador",
            email="joao@conveniencia.local",
            role="operador",
            ativo=True
        )
        operador1.set_password("joao123")
        
        operador2 = Funcionario(
            nome="Maria Caixa",
            email="maria@conveniencia.local",
            role="caixa",
            ativo=True
        )
        operador2.set_password("maria123")
        
        db.session.add_all([admin, gerente, operador1, operador2])
        db.session.commit()
        
        print("📂 Criando categorias...")
        # Criar categorias
        categorias_data = [
            {"nome": "Bebidas", "descricao": "Refrigerantes, sucos e bebidas em geral"},
            {"nome": "Alimentos", "descricao": "Snacks, lanches e alimentos diversos"},
            {"nome": "Doces", "descricao": "Chocolates, balas e doces"},
            {"nome": "Cuidados Pessoais", "descricao": "Produtos de higiene e cuidados"},
            {"nome": "Outros", "descricao": "Diversos"}
        ]
        
        categorias = []
        for cat_data in categorias_data:
            cat = Categoria(**cat_data)
            categorias.append(cat)
            db.session.add(cat)
        db.session.commit()
        
        print("🤝 Criando fornecedores...")
        # Criar fornecedores
        fornecedores_data = [
            {"nome": "Distribuidora ABC", "contato": "João Silva", "telefone": "(11) 3000-0000", "email": "vendas@distributora-abc.com"},
            {"nome": "Sua Bebida", "contato": "Carlos", "telefone": "(11) 2000-0000", "email": "vendas@suabebida.com"},
            {"nome": "Alimentos Brasil", "contato": "Pedro", "telefone": "(11) 1000-0000", "email": "contato@alimentosbrasil.com"},
            {"nome": "Premium Doces", "contato": "Ana", "telefone": "(11) 4000-0000", "email": "vendas@premiumdoces.com"},
        ]
        
        fornecedores = []
        for forn_data in fornecedores_data:
            forn = Fornecedor(**forn_data)
            fornecedores.append(forn)
            db.session.add(forn)
        db.session.commit()
        
        print("📦 Criando produtos...")
        # Criar produtos
        produtos_data = [
            # Bebidas
            {"codigo": "BEB001", "nome": "Coca-Cola 2L", "categoria_id": categorias[0].id, "preco_custo": 5.00, "preco_venda": 8.50, "quantidade_estoque": 50},
            {"codigo": "BEB002", "nome": "Suco Natural Laranja 1L", "categoria_id": categorias[0].id, "preco_custo": 3.50, "preco_venda": 6.90, "quantidade_estoque": 30},
            {"codigo": "BEB003", "nome": "Água Mineral 1.5L", "categoria_id": categorias[0].id, "preco_custo": 1.20, "preco_venda": 2.50, "quantidade_estoque": 100},
            
            # Alimentos
            {"codigo": "ALI001", "nome": "Biscoito Água e Sal", "categoria_id": categorias[1].id, "preco_custo": 1.50, "preco_venda": 3.50, "quantidade_estoque": 80},
            {"codigo": "ALI002", "nome": "Bolo de Chocolate", "categoria_id": categorias[1].id, "preco_custo": 4.00, "preco_venda": 8.90, "quantidade_estoque": 20},
            {"codigo": "ALI003", "nome": "Batata Frita Pequena", "categoria_id": categorias[1].id, "preco_custo": 2.00, "preco_venda": 4.90, "quantidade_estoque": 60},
            
            # Doces
            {"codigo": "DOC001", "nome": "Chocolate Ao Leite", "categoria_id": categorias[2].id, "preco_custo": 3.00, "preco_venda": 6.50, "quantidade_estoque": 45},
            {"codigo": "DOC002", "nome": "Bala Sortida", "categoria_id": categorias[2].id, "preco_custo": 0.50, "preco_venda": 1.50, "quantidade_estoque": 200},
            {"codigo": "DOC003", "nome": "Brigadeiro", "categoria_id": categorias[2].id, "preco_custo": 1.50, "preco_venda": 3.50, "quantidade_estoque": 35},
            
            # Cuidados Pessoais
            {"codigo": "CUI001", "nome": "Papel Higiênico 4 rolos", "categoria_id": categorias[3].id, "preco_custo": 4.50, "preco_venda": 8.90, "quantidade_estoque": 25},
            {"codigo": "CUI002", "nome": "Desinfetante", "categoria_id": categorias[3].id, "preco_custo": 2.50, "preco_venda": 5.50, "quantidade_estoque": 15},
        ]
        
        produtos = []
        for prod_data in produtos_data:
            prod = Produto(**prod_data)
            produtos.append(prod)
            db.session.add(prod)
        db.session.commit()
        
        print("🏪 Criando mesas...")
        # Criar mesas
        mesas_data = [
            {"numero": "1", "capacidade": 2, "status": "livre"},
            {"numero": "2", "capacidade": 2, "status": "livre"},
            {"numero": "3", "capacidade": 4, "status": "ocupada"},
            {"numero": "4", "capacidade": 4, "status": "livre"},
            {"numero": "5", "capacidade": 6, "status": "livre"},
            {"numero": "6", "capacidade": 4, "status": "ocupada"},
        ]
        
        mesas = []
        for mesa_data in mesas_data:
            mesa = Mesa(**mesa_data)
            mesa.qr_token = secrets.token_urlsafe(12)
            mesas.append(mesa)
            db.session.add(mesa)
        db.session.commit()
        
        print("💰 Criando caixas...")
        # Criar caixas
        caixas_data = [
            {"nome": "Caixa 1", "funcionario_id": maria.id if (maria := operador2) else None, "saldo_inicial": 0.0, "aberto": False},
            {"nome": "Caixa 2", "funcionario_id": None, "saldo_inicial": 0.0, "aberto": False},
            {"nome": "Caixa 3", "funcionario_id": None, "saldo_inicial": 0.0, "aberto": False},
        ]
        
        caixas = []
        for caixa_data in caixas_data:
            caixa = Caixa(**caixa_data)
            caixa.saldo_atual = caixa_data["saldo_inicial"]
            caixas.append(caixa)
            db.session.add(caixa)
        db.session.commit()
        
        # sample pedido with payment
        print("💳 Criando um pedido de exemplo com pagamento")
        if caixas and produtos:
            ped = Pedido(caixa_id=caixas[0].id, total=produtos[0].preco_venda, metodo_pagamento='dinheiro', valor_pago=produtos[0].preco_venda)
            db.session.add(ped)
            db.session.commit()

        print("📋 Criando movimentações de estoque...")
        # Criar algumas movimentações para histórico
        for i, produto in enumerate(produtos[:5]):
            mov = Movimentacao(
                produto_id=produto.id,
                fornecedor_id=fornecedores[0].id,
                tipo=Movimentacao.TIPO_ENTRADA,
                quantidade=100,
                motivo="Compra inicial",
                observacoes="Estoque de abertura"
            )
            db.session.add(mov)
        db.session.commit()
        
        print("🔐 Configurando permissões...")
        # Adicionar permissões para funcionários
        paginas_admin = ['inicio', 'produtos', 'categorias', 'fornecedores', 'movimentacoes', 
                        'relatorios', 'caixas', 'mesas', 'pedidos', 'vendas', 'funcionarios']
        paginas_gerente = ['inicio', 'produtos', 'categorias', 'movimentacoes', 'relatorios', 
                          'caixas', 'mesas', 'pedidos', 'vendas']
        paginas_operador = ['inicio', 'produtos', 'pedidos', 'vendas']
        
        # Admin
        for pagina in paginas_admin:
            perm = PermissaoAcesso(funcionario_id=admin.id, pagina=pagina)
            db.session.add(perm)
        
        # Gerente
        for pagina in paginas_gerente:
            perm = PermissaoAcesso(funcionario_id=gerente.id, pagina=pagina)
            db.session.add(perm)
        
        # Operadores
        for pagina in paginas_operador:
            perm = PermissaoAcesso(funcionario_id=operador1.id, pagina=pagina)
            db.session.add(perm)
            perm = PermissaoAcesso(funcionario_id=operador2.id, pagina=pagina)
            db.session.add(perm)
        
        db.session.commit()
        
        print("\n" + "="*60)
        print("✅ BANCO DE DADOS POPULADO COM SUCESSO!")
        print("="*60)
        print("\n📊 Dados Criados:")
        print(f"  • {len([admin, gerente, operador1, operador2])} funcionários")
        print(f"  • {len(categorias)} categorias")
        print(f"  • {len(fornecedores)} fornecedores")
        print(f"  • {len(produtos)} produtos")
        print(f"  • {len(mesas)} mesas")
        print(f"  • {len(caixas)} caixas")
        print("\n🔐 Contas para Teste:")
        print("  Admin:      admin@conveniencia.local / admin123")
        print("  Gerente:    gerente@conveniencia.local / gerente123")
        print("  Operador:   joao@conveniencia.local / joao123")
        print("  Caixa:      maria@conveniencia.local / maria123")
        print("\n" + "="*60)

if __name__ == '__main__':
    try:
        seed_database()
    except Exception as e:
        print(f"❌ Erro ao popular banco: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

```


### Arquivo: `utils/__init__.py`
- Linhas: 2
- Tamanho: 0.0 KB
- Status: completo

```python
# Utilitarios compartilhados do projeto.

```


### Arquivo: `utils/endereco_codigo.py`
- Linhas: 502
- Tamanho: 17.8 KB
- Status: completo

```python
import re
import unicodedata
from dataclasses import dataclass
from typing import Iterable


@dataclass
class EnderecoCodigoConfig:
    zonas_permitidas: set[str]
    permitir_nivel_zero: bool = True
    separador: str = '-'


DEFAULT_ZONAS_PERMITIDAS = {'ZP', 'ZR', 'ZQ', 'ZD'}
_CONFIG = EnderecoCodigoConfig(zonas_permitidas=set(DEFAULT_ZONAS_PERMITIDAS), permitir_nivel_zero=True, separador='-')

_REGEX_CODIGO = re.compile(
    r'^CD(?P<cd>\d{2})-(?P<zona>Z[A-Z0-9]{1,2})-R(?P<rua>\d{2})-RK(?P<rack>\d{2})-N(?P<nivel>\d{2})-V(?P<vao>\d{2})-(?P<lado>L[A-Z0-9]{1,2})$'
)

_MAPA_LADO = {
    'A': 'LA',
    'B': 'LB',
    'LA': 'LA',
    'LB': 'LB',
    'E': 'LA',
    'ESQ': 'LA',
    'ESQUERDA': 'LA',
    'D': 'LB',
    'DIR': 'LB',
    'DIREITA': 'LB',
}


def configurar_endereco(*, zonas_permitidas: Iterable[str] | None = None, permitir_nivel_zero: bool | None = None):
    if zonas_permitidas is not None:
        normalizadas = set()
        for z in zonas_permitidas:
            zona_norm = _normalizar_zona(z, validar_permitidas=False)
            normalizadas.add(zona_norm)
        _CONFIG.zonas_permitidas = normalizadas
    if permitir_nivel_zero is not None:
        _CONFIG.permitir_nivel_zero = bool(permitir_nivel_zero)


def _normalizar_codigo_texto(codigo: str) -> str:
    texto = (codigo or '').strip().upper()
    texto = re.sub(r'[\s_]+', '-', texto)
    texto = re.sub(r'-{2,}', '-', texto)
    return texto


def _normalizar_numero(nome_campo: str, valor, *, minimo: int, maximo: int = 99) -> int:
    if valor is None or str(valor).strip() == '':
        raise ValueError(f'Campo "{nome_campo}" obrigatorio.')
    try:
        numero = int(str(valor).strip())
    except (TypeError, ValueError):
        raise ValueError(f'Campo "{nome_campo}" invalido. Informe numero inteiro.')
    if numero < minimo:
        raise ValueError(f'Campo "{nome_campo}" invalido. Minimo permitido: {minimo}.')
    if numero > maximo:
        raise ValueError(f'Campo "{nome_campo}" invalido. Maximo permitido: {maximo}.')
    return numero


def _normalizar_zona(zona: str, *, validar_permitidas: bool = True) -> str:
    if zona is None or str(zona).strip() == '':
        raise ValueError('Campo "zona" obrigatorio.')

    z = str(zona).strip().upper()
    if not re.fullmatch(r'[A-Z0-9]+', z):
        raise ValueError('Campo "zona" invalido. Use apenas caracteres alfanumericos.')
    if not z:
        raise ValueError('Campo "zona" invalido. Use apenas caracteres alfanumericos.')

    if z.startswith('Z'):
        z = z[1:]

    if not z:
        raise ValueError('Campo "zona" invalido. Informe valor apos o prefixo Z.')
    if len(z) > 2:
        raise ValueError('Campo "zona" invalido. Use no maximo 2 caracteres apos Z.')

    zona_normalizada = f'Z{z}'
    if validar_permitidas and _CONFIG.zonas_permitidas and zona_normalizada not in _CONFIG.zonas_permitidas:
        permitidas = ', '.join(sorted(_CONFIG.zonas_permitidas))
        raise ValueError(f'Campo "zona" invalido. Zona "{zona_normalizada}" nao permitida. Permitidas: {permitidas}.')
    return zona_normalizada


def _normalizar_lado(lado: str) -> str:
    if lado is None or str(lado).strip() == '':
        raise ValueError('Campo "lado" obrigatorio.')

    l = str(lado).strip().upper()
    if not re.fullmatch(r'[A-Z0-9]+', l):
        raise ValueError('Campo "lado" invalido. Use apenas caracteres alfanumericos.')
    if not l:
        raise ValueError('Campo "lado" invalido.')

    if l in _MAPA_LADO:
        return _MAPA_LADO[l]

    if l.startswith('L'):
        sufixo = l[1:]
    else:
        sufixo = l

    if sufixo in _MAPA_LADO:
        return _MAPA_LADO[sufixo]

    if len(sufixo) == 1 and sufixo.isalnum():
        return f'L{sufixo}'

    raise ValueError('Campo "lado" invalido. Use A/B, LA/LB, ESQ/DIR ou E/D.')


def montar_endereco(cd, zona, rua, rack, nivel, vao, lado) -> str:
    cd_n = _normalizar_numero('cd', cd, minimo=1)
    zona_n = _normalizar_zona(zona)
    rua_n = _normalizar_numero('rua', rua, minimo=1)
    rack_n = _normalizar_numero('rack', rack, minimo=1)
    nivel_min = 0 if _CONFIG.permitir_nivel_zero else 1
    nivel_n = _normalizar_numero('nivel', nivel, minimo=nivel_min)
    vao_n = _normalizar_numero('vao', vao, minimo=1)
    lado_n = _normalizar_lado(lado)

    return (
        f'CD{cd_n:02d}{_CONFIG.separador}'
        f'{zona_n}{_CONFIG.separador}'
        f'R{rua_n:02d}{_CONFIG.separador}'
        f'RK{rack_n:02d}{_CONFIG.separador}'
        f'N{nivel_n:02d}{_CONFIG.separador}'
        f'V{vao_n:02d}{_CONFIG.separador}'
        f'{lado_n}'
    ).upper()


def parse_endereco(codigo) -> dict:
    texto = _normalizar_codigo_texto(str(codigo or ''))
    match = _REGEX_CODIGO.match(texto)
    if not match:
        raise ValueError(
            'Codigo invalido. Formato esperado: CD##-Z??-R##-RK##-N##-V##-L? (separadores _, espacos e letras minusculas sao normalizados).'
        )

    partes = match.groupdict()
    cd_n = _normalizar_numero('cd', partes['cd'], minimo=1)
    zona_n = _normalizar_zona(partes['zona'])
    rua_n = _normalizar_numero('rua', partes['rua'], minimo=1)
    rack_n = _normalizar_numero('rack', partes['rack'], minimo=1)
    nivel_min = 0 if _CONFIG.permitir_nivel_zero else 1
    nivel_n = _normalizar_numero('nivel', partes['nivel'], minimo=nivel_min)
    vao_n = _normalizar_numero('vao', partes['vao'], minimo=1)
    lado_n = _normalizar_lado(partes['lado'])

    return {
        'cd': cd_n,
        'zona': zona_n,
        'rua': rua_n,
        'rack': rack_n,
        'nivel': nivel_n,
        'vao': vao_n,
        'lado': lado_n,
    }


def validar_endereco(codigo) -> dict:
    try:
        partes = parse_endereco(codigo)
        return {'valido': True, 'erros': [], 'partes': partes}
    except ValueError as exc:
        return {'valido': False, 'erros': [str(exc)], 'partes': {}}


# ======= Endereco supermercado (rack/area aberta) =======

SETORES_ZONA_VALIDOS = (
    'secos',
    'bebidas',
    'hortifruti',
    'frios',
    'congelados',
    'acougue',
    'padaria',
    'deposito',
    'frente_loja',
    'ecommerce_picking',
    'quarentena',
    'avaria',
    'devolucao',
)

TIPOS_AREA_VALIDOS = (
    'picking',
    'pulmao_reserva',
    'recebimento',
    'expedicao_transferencia',
    'frente_loja',
    'quarentena',
    'avaria',
)

STATUS_ENDERECO_VALIDOS = ('ativo', 'bloqueado', 'inventario')
TIPOS_ESTRUTURA_VALIDOS = ('rack', 'area_aberta')
CONTROLE_VALIDADE_VALIDOS = ('nenhum', 'fifo', 'fefo')
TEMPERATURA_VALIDOS = ('ambiente', 'refrigerado', 'congelado')
RESTRICOES_VALIDAS = ('fragil', 'alto_valor', 'quimicos', 'alimentos')

_SIGLAS_SETOR = {
    'secos': 'SEC',
    'bebidas': 'BEB',
    'hortifruti': 'HOR',
    'frios': 'FRI',
    'congelados': 'CON',
    'acougue': 'ACO',
    'padaria': 'PAD',
    'deposito': 'DEP',
    'frente_loja': 'FL',
    'ecommerce_picking': 'ECP',
    'quarentena': 'QUA',
    'avaria': 'AVA',
    'devolucao': 'DEV',
}

_MAPA_LADO_SUPERMERCADO = {
    'A': 'LA',
    'B': 'LB',
    'LA': 'LA',
    'LB': 'LB',
    'E': 'LE',
    'D': 'LD',
    'LE': 'LE',
    'LD': 'LD',
    'ESQ': 'LE',
    'DIR': 'LD',
}


def _sem_acentos(texto: str) -> str:
    base = unicodedata.normalize('NFKD', str(texto or ''))
    return ''.join(c for c in base if not unicodedata.combining(c))


def _normalizar_token(texto: str) -> str:
    normalizado = _sem_acentos(texto).upper().strip()
    normalizado = re.sub(r'\s+', '', normalizado)
    normalizado = re.sub(r'[^A-Z0-9_]', '', normalizado)
    return normalizado


def _normalizar_slug(texto: str, *, max_len: int = 32) -> str:
    normalizado = _sem_acentos(texto).upper().strip()
    normalizado = re.sub(r'[\s_/]+', '-', normalizado)
    normalizado = re.sub(r'[^A-Z0-9-]', '-', normalizado)
    normalizado = re.sub(r'-{2,}', '-', normalizado).strip('-')
    return normalizado[:max_len]


def _normalizar_setor(setor_zona: str) -> str:
    valor = (_sem_acentos(setor_zona).strip().lower().replace(' ', '_')) if setor_zona is not None else ''
    if valor not in SETORES_ZONA_VALIDOS:
        raise ValueError(f'Campo "setor_zona" invalido. Valores permitidos: {", ".join(SETORES_ZONA_VALIDOS)}.')
    return valor


def _normalizar_lado_supermercado(lado: str) -> str:
    valor = _normalizar_token(lado)
    if valor not in _MAPA_LADO_SUPERMERCADO:
        raise ValueError('Campo "lado" invalido. Use A/B, E/D, LA/LB ou LE/LD.')
    return _MAPA_LADO_SUPERMERCADO[valor]


def _numero_2d(nome_campo: str, valor: str) -> str:
    if valor is None or str(valor).strip() == '':
        raise ValueError(f'Campo "{nome_campo}" obrigatorio.')
    digitos = re.search(r'\d+', str(valor))
    if not digitos:
        raise ValueError(f'Campo "{nome_campo}" invalido. Informe valor numerico.')
    numero = int(digitos.group(0))
    return f'{numero:02d}'


def _normalizar_bool(valor) -> bool:
    if isinstance(valor, bool):
        return valor
    texto = str(valor or '').strip().lower()
    return texto in {'1', 'true', 'on', 'sim', 'yes'}


def _normalizar_int_opcional(nome_campo: str, valor):
    if valor is None or str(valor).strip() == '':
        return None
    try:
        numero = int(str(valor).strip())
    except ValueError:
        raise ValueError(f'Campo "{nome_campo}" invalido. Informe numero inteiro.')
    if numero < 0:
        raise ValueError(f'Campo "{nome_campo}" invalido. Nao pode ser negativo.')
    return numero


def _normalizar_float_opcional(nome_campo: str, valor):
    if valor is None or str(valor).strip() == '':
        return None
    try:
        numero = float(str(valor).strip().replace(',', '.'))
    except ValueError:
        raise ValueError(f'Campo "{nome_campo}" invalido. Informe numero.')
    if numero < 0:
        raise ValueError(f'Campo "{nome_campo}" invalido. Nao pode ser negativo.')
    return numero


def _normalizar_prioridade_picking(valor):
    if valor is None:
        return 0
    texto = str(valor).strip().lower()
    if not texto:
        return 0
    if texto in {'1', 'sim', 's', 'true', 'on', 'yes'}:
        return 1
    if texto in {'0', 'nao', 'não', 'n', 'false', 'off', 'no'}:
        return 0
    try:
        return 1 if int(texto) > 0 else 0
    except ValueError:
        raise ValueError('Campo "prioridade_picking" invalido. Use Sim ou Nao.')


def _codigo_area_aberta(ponto_local: str) -> str:
    texto = _sem_acentos(ponto_local or '').upper()
    texto = re.sub(r'\s+', ' ', texto).strip()
    if not texto:
        raise ValueError('Campo "ponto_local" obrigatorio para estrutura area_aberta.')

    g_match = re.search(r'(?:\bGONDOLA\b|\bG\b)\s*0*(\d+)', texto)
    p_match = re.search(r'(?:\bPRATELEIRA\b|\bP\b)\s*0*(\d+)', texto)
    if g_match and p_match:
        return f'G{int(g_match.group(1)):02d}-P{int(p_match.group(1)):02d}'

    slug = _normalizar_slug(texto, max_len=24)
    if not slug:
        raise ValueError('Campo "ponto_local" invalido.')
    return slug


def gerar_codigo_localizacao_supermercado(
    *,
    loja_cd: str,
    setor_zona: str,
    tipo_estrutura: str,
    rua_corredor: str | None = None,
    rack_estante: str | None = None,
    nivel_prateleira: str | None = None,
    posicao_slot: str | None = None,
    lado: str | None = None,
    ponto_local: str | None = None,
) -> str:
    loja = _normalizar_token(loja_cd)
    if not loja:
        raise ValueError('Campo "loja_cd" obrigatorio.')

    setor = _normalizar_setor(setor_zona)
    sigla_setor = _SIGLAS_SETOR[setor]
    estrutura = (_sem_acentos(tipo_estrutura).strip().lower().replace(' ', '_')) if tipo_estrutura else ''
    if estrutura not in TIPOS_ESTRUTURA_VALIDOS:
        raise ValueError(f'Campo "tipo_estrutura" invalido. Valores permitidos: {", ".join(TIPOS_ESTRUTURA_VALIDOS)}.')

    if estrutura == 'rack':
        r = _numero_2d('rua_corredor', rua_corredor)
        rk = _numero_2d('rack_estante', rack_estante)
        n = _numero_2d('nivel_prateleira', nivel_prateleira)
        v = _numero_2d('posicao_slot', posicao_slot)
        lado_norm = _normalizar_lado_supermercado(lado)
        return f'{loja}-{sigla_setor}-R{r}-RK{rk}-N{n}-V{v}-{lado_norm}'

    codigo_area = _codigo_area_aberta(ponto_local or '')
    return f'{loja}-{sigla_setor}-{codigo_area}'


def validar_endereco_supermercado_payload(payload) -> dict:
    """Valida/normaliza payload do formulario de endereco e gera codigo_localizacao."""
    get = payload.get
    getlist = payload.getlist if hasattr(payload, 'getlist') else None

    loja_cd = _normalizar_token(get('loja_cd', ''))
    if not loja_cd:
        raise ValueError('Campo "loja_cd" obrigatorio.')

    setor_zona = _normalizar_setor(get('setor_zona', ''))

    tipo_area = (_sem_acentos(get('tipo_area', '')).strip().lower().replace(' ', '_'))
    if tipo_area not in TIPOS_AREA_VALIDOS:
        raise ValueError(f'Campo "tipo_area" invalido. Valores permitidos: {", ".join(TIPOS_AREA_VALIDOS)}.')

    status = (_sem_acentos(get('status', '')).strip().lower().replace(' ', '_'))
    if status not in STATUS_ENDERECO_VALIDOS:
        raise ValueError(f'Campo "status" invalido. Valores permitidos: {", ".join(STATUS_ENDERECO_VALIDOS)}.')

    tipo_estrutura = (_sem_acentos(get('tipo_estrutura', '')).strip().lower().replace(' ', '_'))
    if tipo_estrutura not in TIPOS_ESTRUTURA_VALIDOS:
        raise ValueError(f'Campo "tipo_estrutura" invalido. Valores permitidos: {", ".join(TIPOS_ESTRUTURA_VALIDOS)}.')

    controle_validade = (_sem_acentos(get('controle_validade', '')).strip().lower().replace(' ', '_'))
    if controle_validade not in CONTROLE_VALIDADE_VALIDOS:
        raise ValueError(
            f'Campo "controle_validade" invalido. Valores permitidos: {", ".join(CONTROLE_VALIDADE_VALIDOS)}.'
        )

    temperatura = (_sem_acentos(get('temperatura', '')).strip().lower().replace(' ', '_')) or None
    if temperatura and temperatura not in TEMPERATURA_VALIDOS:
        raise ValueError(f'Campo "temperatura" invalido. Valores permitidos: {", ".join(TEMPERATURA_VALIDOS)}.')

    rua_corredor = (_normalizar_token(get('rua_corredor', '')) or None)
    rack_estante = (str(get('rack_estante', '')).strip() or None)
    nivel_prateleira = (str(get('nivel_prateleira', '')).strip() or None)
    posicao_slot = (str(get('posicao_slot', '')).strip() or None)
    lado = (_normalizar_token(get('lado', '')) or None)
    ponto_local = (_sem_acentos(get('ponto_local', '')).strip().upper() or None)

    if tipo_estrutura == 'rack':
        if ponto_local:
            ponto_local = None
        if not (rua_corredor and rack_estante and nivel_prateleira and posicao_slot and lado):
            raise ValueError('Para tipo_estrutura=rack, rua_corredor, rack_estante, nivel_prateleira, posicao_slot e lado sao obrigatorios.')
        coluna_baia = _numero_2d('rack_estante', rack_estante)
        nivel = _numero_2d('nivel_prateleira', nivel_prateleira)
        slot = _numero_2d('posicao_slot', posicao_slot)
        lado_norm = _normalizar_lado_supermercado(lado)
    else:
        if not ponto_local:
            raise ValueError('Para tipo_estrutura=area_aberta, campo "ponto_local" e obrigatorio.')
        coluna_baia = None
        nivel = None
        slot = None
        lado_norm = None
        rua_corredor = None

    codigo_localizacao = gerar_codigo_localizacao_supermercado(
        loja_cd=loja_cd,
        setor_zona=setor_zona,
        tipo_estrutura=tipo_estrutura,
        rua_corredor=rua_corredor,
        rack_estante=rack_estante,
        nivel_prateleira=nivel_prateleira,
        posicao_slot=posicao_slot,
        lado=lado_norm,
        ponto_local=ponto_local,
    )

    restricoes_raw = []
    if getlist:
        restricoes_raw = getlist('restricoes')
    elif get('restricoes'):
        restricoes_raw = [get('restricoes')]
    restricoes_normalizadas = []
    for item in restricoes_raw:
        chave = _sem_acentos(str(item or '')).strip().lower().replace(' ', '_')
        if chave in RESTRICOES_VALIDAS:
            restricoes_normalizadas.append(chave)
    restricoes = ','.join(sorted(set(restricoes_normalizadas))) if restricoes_normalizadas else None
    tipo_produto_reservado = (_sem_acentos(get('tipo_produto_reservado', '')).strip().upper() or None)
    if tipo_produto_reservado:
        tipo_produto_reservado = tipo_produto_reservado[:120]

    return {
        'loja_cd': loja_cd,
        'setor_zona': setor_zona,
        'tipo_area': tipo_area,
        'status': status,
        'descricao': (str(get('descricao', '')).strip() or None),
        'observacoes': (str(get('observacoes', '')).strip() or None),
        'tipo_estrutura': tipo_estrutura,
        'rua_corredor': rua_corredor,
        'coluna_baia': coluna_baia,
        'nivel_prateleira': nivel,
        'posicao_slot': slot,
        'lado': lado_norm,
        'ponto_local': ponto_local,
        'permite_fracionado': _normalizar_bool(get('permite_fracionado')),
        'permite_mistura_sku': _normalizar_bool(get('permite_mistura_sku')),
        'permite_mistura_lote': _normalizar_bool(get('permite_mistura_lote')),
        'controle_validade': controle_validade,
        'temperatura': temperatura,
        'restricoes': restricoes,
        'capacidade_caixas': _normalizar_int_opcional('capacidade_caixas', get('capacidade_caixas')),
        'capacidade_fardos': _normalizar_int_opcional('capacidade_fardos', get('capacidade_fardos')),
        'capacidade_unidades': _normalizar_int_opcional('capacidade_unidades', get('capacidade_unidades')),
        'capacidade_pallets': _normalizar_int_opcional('capacidade_pallets', get('capacidade_pallets')),
        'peso_max_kg': _normalizar_float_opcional('peso_max_kg', get('peso_max_kg')),
        'volume_max_m3': _normalizar_float_opcional('volume_max_m3', get('volume_max_m3')),
        'prioridade_picking': _normalizar_prioridade_picking(get('prioridade_picking')),
        'codigo_localizacao': codigo_localizacao,
        'tipo_produto_reservado': tipo_produto_reservado,
        # Mantem compatibilidade com coluna antiga
        'codigo_armazem': loja_cd,
        'tipo_endereco': tipo_area,
        'sku_produto': (str(get('sku_produto', '')).strip() or None),
    }

```


## 5) Checklist para auditoria tecnica
- Seguranca: auth, autorizacao por perfil, CSRF, validacao de entrada.
- Performance: consultas pesadas, paginação, cache, N+1.
- Qualidade: duplicacao de codigo, tamanho de funcoes, acoplamento.
- Operacao: logs, auditoria, tratamento de erro, observabilidade.
- Testes: cobertura de rotas criticas e regras de negocio.


## 6) Metadados para comparacao de versoes
- Este arquivo pode ser gerado periodicamente e comparado por hash/linhas.
- Recomendacao: salvar junto com hash do commit para trilha de evolucao.

## 7) Pistas de otimizacao para IA
- Mapear funcoes com mais de 80 linhas e sugerir extracao de servicos.
- Identificar queries repetidas por rota e sugerir cache/local batching.
- Verificar N+1 em relacionamentos SQLAlchemy e aplicar selectinload/joinedload.
- Revisar rotas com muita regra de negocio e mover para camada de servico.
- Auditar validacoes de entrada e centralizar em funcoes reutilizaveis.
- Propor padrao unico de respostas de erro e mensagens de usuario.
- Sugerir testes para rotas criticas (auth, pedidos, financeiro, estoque).
- Revisar nomes/encoding para padrao unico e evitar regressao de idioma.

### Prompt recomendado para outra IA
Use este relatorio para:
1. identificar gargalos de performance,
2. sugerir refatoracoes por prioridade (alto/medio/baixo),
3. listar riscos tecnicos,
4. sugerir plano de implementacao em etapas curtas com baixo risco.
