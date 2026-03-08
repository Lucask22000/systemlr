# Export do Projeto Flask

- Pasta raiz: `C:\Users\lucas\OneDrive\Desktop\conveniencia`
- Gerado em: `2026-03-03 00:10:44`
- Total de arquivos incluídos: **106**

## 1) Árvore do projeto (somente itens relevantes)

```text
.
- .
- app.py
- config.py
- docs
- export_flask_structure.py
- fix_admin_access.py
- info.txt
- models.py
- README.md
- realtime.py
- requirements.txt
- routes
- scripts
- security.py
- seed_data.py
- static
- templates
- tests
- utils
  - fase0_matriz_auditoria.md
  - rollout_checklist.md
  - __init__.py
  - estoque_routes.py
  - public_routes.py
  - vendas_routes.py
  - generate_qrcodes.py
  - healthcheck.py
  - css
  - js
  - robots.txt
  - api
  - base.html
  - components
  - dashboard
  - errors
  - estoque
  - funcionarios
  - public
  - rh
  - sistema
  - vendas
  - test_endereco_codigo.py
  - test_endereco_localizacao.py
  - test_system_flows.py
  - __init__.py
  - endereco_codigo.py
    - core
    - pages
    - style.css
    - csrf.js
    - main.js
    - pages
    - docs.html
    - list_macros.html
    - index.html
    - 404.html
    - 500.html
    - categorias
    - enderecos
    - estoques
    - fornecedores
    - movimentacoes
    - produtos
    - recebimentos
    - relatorios
    - acessos.html
    - criar.html
    - editar.html
    - listar.html
    - abrir_comanda.html
    - cardapio.html
    - pedido_enviado.html
    - editar_funcao.html
    - funcoes.html
    - indicadores.html
    - acessos.html
    - auditoria.html
    - boas_vindas.html
    - empresa.html
    - login.html
    - registro.html
    - caixas
    - garcons
    - mesas
    - pdv.html
    - pedidos
      - layout.css
      - tables.css
      - tokens.css
      - cardapio.css
      - pdv.css
      - pedidos.css
      - dashboard_analytics.js
      - estoque_analytics.js
      - rh_analytics.js
      - categorias.html
      - editar_categoria.html
      - nova_categoria.html
      - detalhes_endereco.html
      - editar_endereco.html
      - enderecos.html
      - novo_endereco.html
      - editar_estoque.html
      - estoques.html
      - novo_estoque.html
      - detalhes_fornecedor.html
      - editar_fornecedor.html
      - fornecedores.html
      - novo_fornecedor.html
      - movimentacao_rapida.html
      - movimentacoes.html
      - nova_movimentacao.html
      - editar_produto.html
      - novo_produto.html
      - produtos.html
      - visualizar_produto.html
      - armazenar_recebimento.html
      - conferir_recebimento.html
      - novo_recebimento.html
      - recebimentos.html
      - relatorios.html
      - abrir_caixa.html
      - caixas.html
      - editar_caixa.html
      - fechar_caixa.html
      - historico_caixa.html
      - nova_caixa.html
      - config_distribuicao.html
      - editar_garcom.html
      - garcons.html
      - novo_garcom.html
      - editar_mesa.html
      - mesas.html
      - nova_mesa.html
      - print_qrcode_mesa.html
      - qrcode_mesa.html
      - comprovante.html
      - detalhes_pedido.html
      - editar_pedido.html
      - novo_pedido.html
      - pedidos.html
```

## 2) Lista de arquivos incluídos

- `app.py`
- `config.py`
- `docs\fase0_matriz_auditoria.md`
- `docs\rollout_checklist.md`
- `export_flask_structure.py`
- `fix_admin_access.py`
- `info.txt`
- `models.py`
- `README.md`
- `realtime.py`
- `requirements.txt`
- `routes\__init__.py`
- `routes\estoque_routes.py`
- `routes\public_routes.py`
- `routes\vendas_routes.py`
- `scripts\generate_qrcodes.py`
- `scripts\healthcheck.py`
- `security.py`
- `seed_data.py`
- `static\css\core\layout.css`
- `static\css\core\tables.css`
- `static\css\core\tokens.css`
- `static\css\pages\cardapio.css`
- `static\css\pages\pdv.css`
- `static\css\pages\pedidos.css`
- `static\css\style.css`
- `static\js\csrf.js`
- `static\js\main.js`
- `static\js\pages\dashboard_analytics.js`
- `static\js\pages\estoque_analytics.js`
- `static\js\pages\rh_analytics.js`
- `static\robots.txt`
- `templates\api\docs.html`
- `templates\base.html`
- `templates\components\list_macros.html`
- `templates\dashboard\index.html`
- `templates\errors\404.html`
- `templates\errors\500.html`
- `templates\estoque\categorias\categorias.html`
- `templates\estoque\categorias\editar_categoria.html`
- `templates\estoque\categorias\nova_categoria.html`
- `templates\estoque\enderecos\detalhes_endereco.html`
- `templates\estoque\enderecos\editar_endereco.html`
- `templates\estoque\enderecos\enderecos.html`
- `templates\estoque\enderecos\novo_endereco.html`
- `templates\estoque\estoques\editar_estoque.html`
- `templates\estoque\estoques\estoques.html`
- `templates\estoque\estoques\novo_estoque.html`
- `templates\estoque\fornecedores\detalhes_fornecedor.html`
- `templates\estoque\fornecedores\editar_fornecedor.html`
- `templates\estoque\fornecedores\fornecedores.html`
- `templates\estoque\fornecedores\novo_fornecedor.html`
- `templates\estoque\movimentacoes\movimentacao_rapida.html`
- `templates\estoque\movimentacoes\movimentacoes.html`
- `templates\estoque\movimentacoes\nova_movimentacao.html`
- `templates\estoque\produtos\editar_produto.html`
- `templates\estoque\produtos\novo_produto.html`
- `templates\estoque\produtos\produtos.html`
- `templates\estoque\produtos\visualizar_produto.html`
- `templates\estoque\recebimentos\armazenar_recebimento.html`
- `templates\estoque\recebimentos\conferir_recebimento.html`
- `templates\estoque\recebimentos\novo_recebimento.html`
- `templates\estoque\recebimentos\recebimentos.html`
- `templates\estoque\relatorios\relatorios.html`
- `templates\funcionarios\acessos.html`
- `templates\funcionarios\criar.html`
- `templates\funcionarios\editar.html`
- `templates\funcionarios\listar.html`
- `templates\public\abrir_comanda.html`
- `templates\public\cardapio.html`
- `templates\public\pedido_enviado.html`
- `templates\rh\editar_funcao.html`
- `templates\rh\funcoes.html`
- `templates\rh\indicadores.html`
- `templates\sistema\acessos.html`
- `templates\sistema\auditoria.html`
- `templates\sistema\boas_vindas.html`
- `templates\sistema\empresa.html`
- `templates\sistema\login.html`
- `templates\sistema\registro.html`
- `templates\vendas\caixas\abrir_caixa.html`
- `templates\vendas\caixas\caixas.html`
- `templates\vendas\caixas\editar_caixa.html`
- `templates\vendas\caixas\fechar_caixa.html`
- `templates\vendas\caixas\historico_caixa.html`
- `templates\vendas\caixas\nova_caixa.html`
- `templates\vendas\garcons\config_distribuicao.html`
- `templates\vendas\garcons\editar_garcom.html`
- `templates\vendas\garcons\garcons.html`
- `templates\vendas\garcons\novo_garcom.html`
- `templates\vendas\mesas\editar_mesa.html`
- `templates\vendas\mesas\mesas.html`
- `templates\vendas\mesas\nova_mesa.html`
- `templates\vendas\mesas\print_qrcode_mesa.html`
- `templates\vendas\mesas\qrcode_mesa.html`
- `templates\vendas\pdv.html`
- `templates\vendas\pedidos\comprovante.html`
- `templates\vendas\pedidos\detalhes_pedido.html`
- `templates\vendas\pedidos\editar_pedido.html`
- `templates\vendas\pedidos\novo_pedido.html`
- `templates\vendas\pedidos\pedidos.html`
- `tests\test_endereco_codigo.py`
- `tests\test_endereco_localizacao.py`
- `tests\test_system_flows.py`
- `utils\__init__.py`
- `utils\endereco_codigo.py`

## 3) Conteúdo dos arquivos


---

### Arquivo: `app.py`

```py
﻿from datetime import datetime, timedelta
from functools import wraps
from collections import deque
import os

from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from sqlalchemy import inspect, text
from werkzeug.utils import secure_filename

from config import DEV_FALLBACK_SECRET, config
from models import Categoria, EnderecoEstoque, Estoque, Fornecedor, Funcionario, FuncaoRH, Movimentacao, Produto, PermissaoAcesso, Caixa, MovimentacaoCaixa, Pedido, ItemPedido, Garcom, EmpresaConfig, AuditoriaEvento, db
from routes.estoque_routes import register_estoque_routes
from routes.vendas_routes import register_vendas_routes
from routes.public_routes import register_public_routes
from security import csrf_input_tag, csrf_protect_request, ensure_csrf_token, is_json_request, json_response

# Informacoes do SystemLR
APP_NAME = 'SystemLR'
APP_VERSION = '1.0.0'
APP_DOMAIN = 'systemlr.com'

LOGIN_MAX_ATTEMPTS = 5
LOGIN_WINDOW_SECONDS = 300  # 5 minutes window
_failed_login_attempts = {}

app = Flask(__name__)
config_name = (os.environ.get('FLASK_CONFIG') or os.environ.get('APP_ENV') or 'development').strip().lower()
if config_name not in config:
    config_name = 'default'
app.config.from_object(config[config_name])
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'

if app.config.get('ENV_NAME') == 'production' and app.config.get('SECRET_KEY') == DEV_FALLBACK_SECRET:
    raise RuntimeError('SECRET_KEY insegura em producao. Defina a variavel de ambiente SECRET_KEY.')

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
    'estoques': 'Estoques',
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
    'auditoria': 'Auditoria',
    'empresa': 'Empresa',
    'garcons': 'Garcons'
}
PAGINAS_SISTEMA_MENU_ORDEM = (
    ('Dashboard', ('inicio',)),
    ('Vendas', ('pdv', 'pedidos', 'mesas', 'caixas', 'garcons')),
    ('Estoque', ('estoques', 'produtos', 'categorias', 'fornecedores', 'enderecos_estoque', 'movimentacoes', 'relatorios')),
    ('Meu RH', ('rh_indicadores', 'funcionarios', 'rh_funcoes', 'auditoria', 'empresa')),
)
PAGINA_ENDPOINTS = {
    'inicio': {'dashboard', 'boas_vindas', 'dashboard_analytics_api'},
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
    'produtos': {'listar_produtos', 'novo_produto', 'editar_produto', 'visualizar_produto', 'deletar_produto'},
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
    'movimentacoes': {
        'listar_movimentacoes',
        'nova_movimentacao',
        'movimentacao_rapida',
        'transferir_armazenamento',
        'listar_recebimentos_fornecedor',
        'novo_recebimento_fornecedor',
        'conferir_recebimento_fornecedor',
        'armazenar_recebimento_fornecedor',
        'cancelar_recebimento_fornecedor',
    },
    'relatorios': {'relatorios', 'analytics_estoque_api'},
    'caixas': {'listar_caixas', 'nova_caixa', 'editar_caixa', 'deletar_caixa', 'abrir_caixa', 'fechar_caixa', 'historico_caixa'},
    'mesas': {'listar_mesas', 'nova_mesa', 'editar_mesa', 'deletar_mesa', 'visualizar_qrcode_mesa', 'download_qrcode_mesa', 'print_qrcode_mesa'},
    'pedidos': {'listar_pedidos', 'listar_pedidos_pendentes', 'novo_pedido', 'editar_pedido', 'deletar_pedido', 'visualizar_comprovante_pedido', 'detalhes_pedido', 'alterar_status_pedido'},
    'funcionarios': {'listar_funcionarios', 'criar_funcionario', 'editar_funcionario', 'deletar_funcionario', 'editar_acessos_funcionario'},
    'rh_funcoes': {'listar_funcoes_rh', 'nova_funcao_rh', 'editar_funcao_rh', 'deletar_funcao_rh'},
    'rh_indicadores': {'indicadores_rh', 'analytics_rh_api'},
    'auditoria': {'auditoria_sistema'},
    'empresa': {'editar_empresa', 'preview_cardapio_empresa'},
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
    if 'endereco_origem_id' not in colunas_movimentacoes:
        db.session.execute(text('ALTER TABLE movimentacoes ADD COLUMN endereco_origem_id INTEGER'))
        db.session.commit()
    if 'endereco_destino_id' not in colunas_movimentacoes:
        db.session.execute(text('ALTER TABLE movimentacoes ADD COLUMN endereco_destino_id INTEGER'))
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
    if 'estoque_processado' not in colunas_pedidos:
        db.session.execute(text('ALTER TABLE pedidos ADD COLUMN estoque_processado BOOLEAN DEFAULT 0'))
        db.session.commit()
    if 'financeiro_processado' not in colunas_pedidos:
        db.session.execute(text('ALTER TABLE pedidos ADD COLUMN financeiro_processado BOOLEAN DEFAULT 0'))
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
    if 'fornecedor_id' not in colunas_produtos:
        db.session.execute(text('ALTER TABLE produtos ADD COLUMN fornecedor_id INTEGER'))
        db.session.commit()
    if 'status_disponibilidade' not in colunas_produtos:
        db.session.execute(text("ALTER TABLE produtos ADD COLUMN status_disponibilidade VARCHAR(30) DEFAULT 'disponivel_venda'"))
        db.session.commit()
    db.session.execute(text("UPDATE produtos SET status_disponibilidade = 'disponivel_venda' WHERE status_disponibilidade IS NULL OR TRIM(status_disponibilidade) = ''"))
    db.session.commit()
    colunas_fornecedores = {col['name'] for col in inspector.get_columns('fornecedores')}
    for col_name, col_type in [
        ('documento', 'VARCHAR(30)'),
        ('endereco_rua', 'VARCHAR(160)'),
        ('endereco_numero', 'VARCHAR(20)'),
        ('endereco_bairro', 'VARCHAR(100)'),
        ('endereco_cidade', 'VARCHAR(100)'),
        ('tipo_produtos_fornece', 'VARCHAR(255)'),
        ('observacoes_gerais', 'TEXT'),
    ]:
        if col_name not in colunas_fornecedores:
            db.session.execute(text(f'ALTER TABLE fornecedores ADD COLUMN {col_name} {col_type}'))
            db.session.commit()

    # Garante fornecedor em todos os produtos:
    # 1) tenta inferir pelo ultimo recebimento/movimentacao com fornecedor informado
    # 2) fallback para fornecedor padrao
    produtos_sem_fornecedor = Produto.query.filter(Produto.fornecedor_id.is_(None)).all()
    if produtos_sem_fornecedor:
        for produto in produtos_sem_fornecedor:
            ultima_mov = Movimentacao.query.filter(
                Movimentacao.produto_id == produto.id,
                Movimentacao.fornecedor_id.isnot(None),
            ).order_by(Movimentacao.criado_em.desc()).first()
            if ultima_mov and ultima_mov.fornecedor_id:
                produto.fornecedor_id = ultima_mov.fornecedor_id

        db.session.flush()
        ainda_sem_fornecedor = Produto.query.filter(Produto.fornecedor_id.is_(None)).all()
        if ainda_sem_fornecedor:
            fornecedor_padrao = Fornecedor.query.filter_by(nome='FORNECEDOR NAO INFORMADO').first()
            if not fornecedor_padrao:
                fornecedor_padrao = Fornecedor(
                    nome='FORNECEDOR NAO INFORMADO',
                    contato='CADASTRO AUTOMATICO',
                    ativo=False,
                    observacoes_gerais='Fornecedor criado automaticamente para produtos legados sem fornecedor.',
                )
                db.session.add(fornecedor_padrao)
                db.session.flush()

            for produto in ainda_sem_fornecedor:
                produto.fornecedor_id = fornecedor_padrao.id
        db.session.commit()
    colunas_enderecos = {col['name'] for col in inspector.get_columns('enderecos_estoque')}
    if 'estoque_id' not in colunas_enderecos:
        db.session.execute(text('ALTER TABLE enderecos_estoque ADD COLUMN estoque_id INTEGER'))
        db.session.commit()
    if 'codigo_localizacao' not in colunas_enderecos:
        db.session.execute(text('ALTER TABLE enderecos_estoque ADD COLUMN codigo_localizacao VARCHAR(40)'))
        db.session.commit()
    for col_name, col_type in [
        ('loja_cd', 'VARCHAR(20)'),
        ('setor_zona', 'VARCHAR(30)'),
        ('tipo_area', 'VARCHAR(40)'),
        ('status', "VARCHAR(20) DEFAULT 'ativo'"),
        ('descricao', 'VARCHAR(255)'),
        ('tipo_estrutura', 'VARCHAR(20)'),
        ('codigo_armazem', 'VARCHAR(20)'),
        ('rua_corredor', 'VARCHAR(20)'),
        ('coluna_baia', 'VARCHAR(10)'),
        ('nivel_prateleira', 'VARCHAR(10)'),
        ('posicao_slot', 'VARCHAR(10)'),
        ('lado', 'VARCHAR(4)'),
        ('ponto_local', 'VARCHAR(255)'),
        ('permite_fracionado', 'BOOLEAN DEFAULT 0'),
        ('permite_mistura_sku', 'BOOLEAN DEFAULT 0'),
        ('permite_mistura_lote', 'BOOLEAN DEFAULT 0'),
        ('controle_validade', "VARCHAR(20) DEFAULT 'nenhum'"),
        ('temperatura', 'VARCHAR(20)'),
        ('restricoes', 'VARCHAR(255)'),
        ('capacidade_caixas', 'INTEGER'),
        ('capacidade_fardos', 'INTEGER'),
        ('capacidade_unidades', 'INTEGER'),
        ('capacidade_pallets', 'INTEGER'),
        ('peso_max_kg', 'FLOAT'),
        ('volume_max_m3', 'FLOAT'),
        ('prioridade_picking', 'INTEGER'),
        ('observacoes', 'TEXT'),
        ('tipo_produto_reservado', 'VARCHAR(120)'),
        ('sku_produto', 'VARCHAR(100)'),
        ('data_alocacao', 'DATETIME'),
        ('tipo_endereco', 'VARCHAR(30)')
    ]:
        if col_name not in colunas_enderecos:
            db.session.execute(text(f'ALTER TABLE enderecos_estoque ADD COLUMN {col_name} {col_type}'))
            db.session.commit()
    tabelas_existentes = set(inspector.get_table_names())
    if 'recebimentos_fornecedor' in tabelas_existentes:
        colunas_recebimentos = {col['name'] for col in inspector.get_columns('recebimentos_fornecedor')}
        for col_name, col_type in [
            ('fornecedor_id', 'INTEGER'),
            ('fornecedor_documento', 'VARCHAR(30)'),
            ('data_entrega', 'DATE'),
            ('info_nota', 'VARCHAR(255)'),
            ('subtotal', 'FLOAT DEFAULT 0'),
            ('desconto', 'FLOAT DEFAULT 0'),
            ('total_pagar', 'FLOAT DEFAULT 0'),
            ('status', "VARCHAR(30) DEFAULT 'criado'"),
            ('observacoes', 'TEXT'),
            ('recebedor_nome', 'VARCHAR(120)'),
            ('recebedor_assinatura', 'VARCHAR(255)'),
            ('entregador_nome', 'VARCHAR(120)'),
            ('entregador_assinatura', 'VARCHAR(255)'),
            ('criado_em', 'DATETIME'),
            ('atualizado_em', 'DATETIME'),
            ('conferido_em', 'DATETIME'),
            ('armazenado_em', 'DATETIME'),
        ]:
            if col_name not in colunas_recebimentos:
                db.session.execute(text(f'ALTER TABLE recebimentos_fornecedor ADD COLUMN {col_name} {col_type}'))
                db.session.commit()
    if 'recebimentos_itens' in tabelas_existentes:
        colunas_recebimentos_itens = {col['name'] for col in inspector.get_columns('recebimentos_itens')}
        for col_name, col_type in [
            ('recebimento_id', 'INTEGER'),
            ('produto_id', 'INTEGER'),
            ('qtd_recebida', 'INTEGER DEFAULT 0'),
            ('unidade', 'VARCHAR(10)'),
            ('descricao_item', 'VARCHAR(255)'),
            ('preco_unitario', 'FLOAT DEFAULT 0'),
            ('total_item', 'FLOAT DEFAULT 0'),
            ('qtd_avaria', 'INTEGER DEFAULT 0'),
            ('lote', 'VARCHAR(80)'),
            ('validade', 'DATE'),
            ('endereco_destino_id', 'INTEGER'),
            ('criado_em', 'DATETIME'),
        ]:
            if col_name not in colunas_recebimentos_itens:
                db.session.execute(text(f'ALTER TABLE recebimentos_itens ADD COLUMN {col_name} {col_type}'))
                db.session.commit()
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
        if 'atendimento_mesas_ativo' not in colunas_empresa:
            db.session.execute(text('ALTER TABLE empresa_config ADD COLUMN atendimento_mesas_ativo BOOLEAN DEFAULT 1'))
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
            if is_json_request():
                return json_response(False, 'Voce precisa fazer login.', status=401, code='auth_required')
            flash('Voce precisa fazer login para acessar esta pagina.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


def require_role(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'funcionario_id' not in session:
                if is_json_request():
                    return json_response(False, 'Voce precisa fazer login.', status=401, code='auth_required')
                flash('Voce precisa fazer login.', 'warning')
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
                flash('Voce nao tem permissao para acessar esta pagina.', 'danger')
                return redirect(url_for('dashboard'))

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def _client_ip():
    forwarded = request.headers.get('X-Forwarded-For', '') or ''
    if forwarded:
        return forwarded.split(',')[0].strip() or (request.remote_addr or 'unknown')
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


def _coletar_dashboard_analytics(inicio_periodo, fim_periodo):
    """Calcula métricas agregadas do dashboard no intervalo informado.

    Args:
        inicio_periodo (datetime): data inicial inclusiva.
        fim_periodo (datetime): data final exclusiva.

    Returns:
        dict: totais de vendas, tickets médios e listas resumidas usadas na home.
    """
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
            'data_iso': chave_dia,
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

    return {
        'periodo_dias': periodo_dias,
        'pedidos_periodo_total': pedidos_periodo_total,
        'faturamento_periodo': float(faturamento_periodo),
        'faturamento_hoje': float(faturamento_hoje),
        'ticket_medio_periodo': float(ticket_medio_periodo),
        'pedidos_abertos': int(pedidos_abertos),
        'pedidos_cancelados_periodo': int(pedidos_cancelados_periodo),
        'vendas_periodo': vendas_periodo,
        'top_produtos_vendidos': top_produtos_vendidos,
        'pedidos_por_status': pedidos_por_status,
        'top_clientes': top_clientes,
        'desempenho_garcons': desempenho_garcons,
        'desempenho_caixas': desempenho_caixas,
        'metodos_pagamento': metodos_pagamento
    }


# ============ ROTAS - AUTENTICACAO ============

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        ip_addr = _client_ip()
        if _is_login_rate_limited(ip_addr):
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
            flash('Email e senha sao obrigatorios.', 'danger')
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
                flash('Usuario inativo. Contate um administrador.', 'danger')
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
            empresa.atendimento_mesas_ativo = (request.form.get('atendimento_mesas_ativo') == 'on')

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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

---

### Arquivo: `config.py`

```py
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

---

### Arquivo: `docs\fase0_matriz_auditoria.md`

```md
# Fase 0 - Matriz de Auditoria de Telas

Data: 2026-03-01
Escopo: 57 templates HTML

## Resumo Geral

- Total de telas: 57
- Telas que estendem `base.html`: 51
- Telas standalone: 6 (`base.html`, `public/*`, `sistema/login`, `sistema/registro`)
- Templates com CSS inline: 18
- Templates com JS inline: 10
- Rotas Flask mapeadas: 79

## Checklist Padrao por Tela

Cada tela deve atender os seguintes itens:

1. Viewport e estrutura responsiva para 360x640, 768x1024 e desktop.
2. Tipografia legivel e espacos de toque adequados.
3. Tabelas com `data-label` e fallback mobile.
4. Estados vazios e mensagens de erro claros.
5. Formularios com CSRF valido.
6. Acoes criticas com confirmacao e permissao por papel.

## Prioridade Alta (Impacto Operacional)

1. `templates/vendas/pdv.html`: fluxo de caixa/vendas, fechamento e pagamento.
2. `templates/vendas/pedidos/pedidos.html`: status, alteracao e monitoramento em tempo real.
3. `templates/vendas/caixas/caixas.html`: abertura/fechamento e seguranca de operacao.
4. `templates/dashboard/index.html`: indicadores e graficos em tempo real.
5. `templates/estoque/relatorios/relatorios.html`: visao analitica para decisao de compra.
6. `templates/rh/indicadores.html`: saude operacional da equipe.

## Riscos Encontrados

1. Ausencia de CSRF global (corrigido nesta etapa).
2. Fluxos divergentes de pedido entre web e API (em consolidacao nesta etapa).
3. Fechamento de pedido sem baixa/financeiro unificado (em consolidacao nesta etapa).
4. Inconsistencia de estilos/listas entre templates legados e novos.

## Backlog Priorizado

1. Migrar restantes de CSS/JS inline para `static/css/pages/*` e `static/js/pages/*`.
2. Completar padronizacao de macros de lista/acoes em todos os modulos.
3. Expandir testes automatizados para fluxos de RH, publico QR e relatorios.
4. Revisar textos com acentuacao quebrada em templates legados.
```

---

### Arquivo: `docs\rollout_checklist.md`

```md
# Checklist de Rollout

## Pre-deploy

1. Definir `FLASK_CONFIG=production`.
2. Definir `SECRET_KEY` forte no ambiente.
3. Confirmar HTTPS e `SESSION_COOKIE_SECURE` ativo.
4. Executar testes automatizados:
   - `.venv\\Scripts\\python.exe -m unittest tests.test_system_flows -v`

## Smoke Test Pos Deploy

1. Login e logout.
2. Criar pedido via PDV e adicionar item.
3. Finalizar pedido e validar:
   - baixa de estoque
   - aumento de saldo da caixa
4. Tentar reabrir pedido fechado (deve falhar).
5. Abrir dashboard, relatorios e RH e validar graficos.

## Rollback

1. Reverter deploy da aplicacao.
2. Restaurar banco via backup anterior.
3. Validar login e fluxo de pedidos basico.
```

---

### Arquivo: `export_flask_structure.py`

```py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Exporta estrutura e arquivos relevantes de um projeto Flask em um único .md.
Rode dentro da pasta do projeto:
    python export_flask_structure.py
Saída:
    flask_export.md
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from datetime import datetime

# =========================
# CONFIGURAÇÕES
# =========================

OUTPUT_FILE = "flask_export.md"

# Pastas para ignorar totalmente
IGNORE_DIRS = {
    ".git", ".hg", ".svn",
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    "venv", ".venv", "env", ".env",  # ambientes virtuais
    "node_modules",
    "dist", "build", ".build", ".eggs",
    ".idea", ".vscode",
    "static/vendor",  # comum ter libs grandes
    "media", "uploads",  # opcional: uploads geralmente são pesados
}

# Arquivos específicos a ignorar
IGNORE_FILES = {
    ".DS_Store",
    "Thumbs.db",
}

# Extensões normalmente desnecessárias para "estrutura+codigo"
IGNORE_EXTS = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico",
    ".pdf", ".zip", ".rar", ".7z", ".tar", ".gz",
    ".mp4", ".mov", ".avi", ".mkv", ".mp3", ".wav",
    ".sqlite", ".db", ".log",
}

# Extensões que queremos capturar
INCLUDE_EXTS = {
    ".py", ".html", ".jinja", ".jinja2", ".css", ".js",
    ".txt", ".md", ".ini", ".cfg", ".toml", ".yaml", ".yml",
    ".env.example",  # caso exista como arquivo literal
}

# Arquivos importantes mesmo sem extensão / nomes comuns de projeto
INCLUDE_FILENAMES = {
    "requirements.txt", "requirements-dev.txt", "pyproject.toml", "poetry.lock",
    "Pipfile", "Pipfile.lock",
    "setup.py", "MANIFEST.in",
    "Dockerfile", "docker-compose.yml", "compose.yml",
    ".flaskenv", ".env.example",
    "wsgi.py", "asgi.py", "manage.py",
    "README", "README.md", "README.rst",
    "config.py",
}

# Limite de tamanho por arquivo (para não puxar coisas enormes sem querer)
MAX_FILE_SIZE_BYTES = 400_000  # 400 KB

# Se quiser evitar capturar minificados mesmo sendo .js/.css
MINIFIED_REGEX = re.compile(r"\.min\.(js|css)$", re.IGNORECASE)

# =========================
# FUNÇÕES
# =========================

def is_ignored_dir(path: Path) -> bool:
    parts = set(path.parts)
    # ignora se qualquer parte do caminho estiver em IGNORE_DIRS
    return any(p in IGNORE_DIRS for p in parts)

def is_included_file(path: Path) -> bool:
    name = path.name

    if name in IGNORE_FILES:
        return False

    if MINIFIED_REGEX.search(name):
        return False

    # ignora extensões pesadas
    if path.suffix.lower() in IGNORE_EXTS:
        return False

    # inclui por nome
    if name in INCLUDE_FILENAMES:
        return True

    # inclui por extensão
    if path.suffix.lower() in INCLUDE_EXTS:
        return True

    # inclui casos como ".env.example" (sufixo é ".example" então não cai em INCLUDE_EXTS)
    if name.endswith(".env.example"):
        return True

    return False

def safe_read_text(path: Path) -> str:
    # Tenta ler como utf-8, com fallback "replace"
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")

def build_tree_lines(root: Path, included_files: set[Path]) -> list[str]:
    """
    Mostra árvore apenas de pastas e arquivos incluídos (pra ficar limpo).
    """
    lines: list[str] = []
    root = root.resolve()

    # Agrupa por diretório
    dirs = set()
    for f in included_files:
        try:
            rel = f.relative_to(root)
        except ValueError:
            continue
        # adiciona todos os pais
        for parent in rel.parents:
            dirs.add(parent)

    # Nós: diretórios e arquivos
    nodes = sorted(
        list(dirs) + [f.relative_to(root) for f in included_files],
        key=lambda p: (len(p.parts), str(p).lower())
    )

    # Monta tree simples por indentação
    for n in nodes:
        indent = "  " * (len(n.parts) - 1)
        lines.append(f"{indent}- {n.name if n.name else '.'}")
    return lines

def collect_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for p in root.rglob("*"):
        if p.is_dir():
            # rglob não permite pular fácil; filtramos nos arquivos
            continue

        if is_ignored_dir(p.parent):
            continue

        if not is_included_file(p):
            continue

        try:
            size = p.stat().st_size
        except OSError:
            continue

        if size > MAX_FILE_SIZE_BYTES:
            continue

        files.append(p)

    # Ordena de forma estável
    files.sort(key=lambda x: str(x).lower())
    return files

def main() -> None:
    root = Path(".").resolve()
    files = collect_files(root)
    included_set = set(files)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write(f"# Export do Projeto Flask\n\n")
        out.write(f"- Pasta raiz: `{root}`\n")
        out.write(f"- Gerado em: `{now}`\n")
        out.write(f"- Total de arquivos incluídos: **{len(files)}**\n\n")

        out.write("## 1) Árvore do projeto (somente itens relevantes)\n\n")
        out.write("```text\n")
        out.write(".\n")
        for line in build_tree_lines(root, included_set):
            out.write(line + "\n")
        out.write("```\n\n")

        out.write("## 2) Lista de arquivos incluídos\n\n")
        for f in files:
            rel = f.relative_to(root)
            out.write(f"- `{rel}`\n")
        out.write("\n")

        out.write("## 3) Conteúdo dos arquivos\n\n")
        for f in files:
            rel = f.relative_to(root)
            out.write(f"\n---\n\n")
            out.write(f"### Arquivo: `{rel}`\n\n")

            # tenta detectar linguagem pelo sufixo
            lang = f.suffix.lower().lstrip(".")
            if rel.name in {"Dockerfile"}:
                lang = "dockerfile"
            elif rel.name in {"docker-compose.yml", "compose.yml"}:
                lang = "yaml"
            elif rel.name in {"requirements.txt", "requirements-dev.txt"}:
                lang = "text"

            out.write(f"```{lang}\n")
            out.write(safe_read_text(f))
            if not safe_read_text(f).endswith("\n"):
                out.write("\n")
            out.write("```\n")

    print(f"[OK] Export gerado: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
```

---

### Arquivo: `fix_admin_access.py`

```py
"""
Script para corrigir/criar acesso do admin
Execute: python fix_admin_access.py
"""
from app import app, db
from models import Funcionario

def fix_admin_access():
    """Cria ou atualiza o admin"""
    
    with app.app_context():
        email = "admin@conveniencia.local"
        senha = "142536"
        
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
                nome="Administrador",
                email=email,
                role="admin",
                ativo=True
            )
            admin.set_password(senha)
            db.session.add(admin)
        
        db.session.commit()
        print(f"✅ Acesso de admin corrigido com sucesso!")
        print(f"   Email: {email}")
        print(f"   Senha: {senha}")
        print(f"   Role: admin")
        print(f"   Ativo: {admin.ativo}")

if __name__ == "__main__":
    fix_admin_access()
```

---

### Arquivo: `info.txt`

```txt
.venv\Scripts\Activate.ps1

9b5c3a7550f15bc08079fd43bf41e54f
```

---

### Arquivo: `models.py`

```py
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

    STATUS_DISPONIVEL_VENDA = 'disponivel_venda'
    STATUS_INDISPONIVEL = 'indisponivel'
    STATUS_SOMENTE_RESSUPRIMENTO = 'somente_ressuprimento'
    STATUS_DISPONIBILIDADE_VALIDOS = [
        STATUS_DISPONIVEL_VENDA,
        STATUS_INDISPONIVEL,
        STATUS_SOMENTE_RESSUPRIMENTO,
    ]
    
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
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
    status_disponibilidade = db.Column(db.String(30), default=STATUS_DISPONIVEL_VENDA, nullable=False)
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

    @property
    def disponivel_para_venda(self):
        status = (self.status_disponibilidade or self.STATUS_DISPONIVEL_VENDA).strip().lower()
        return bool(self.ativo) and status == self.STATUS_DISPONIVEL_VENDA

    @property
    def status_disponibilidade_label(self):
        status = (self.status_disponibilidade or self.STATUS_DISPONIVEL_VENDA).strip().lower()
        labels = {
            self.STATUS_DISPONIVEL_VENDA: 'Disponivel para venda',
            self.STATUS_INDISPONIVEL: 'Indisponivel',
            self.STATUS_SOMENTE_RESSUPRIMENTO: 'Somente ressuprimento',
        }
        return labels.get(status, 'Disponivel para venda')

class Movimentacao(db.Model):
    __tablename__ = 'movimentacoes'
    
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
    
    def __repr__(self):
        return f'<Movimentacao {self.produto_id} - {self.tipo}>'


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
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    movimentacoes = db.relationship('Movimentacao', backref='fornecedor', lazy=True)
    recebimentos = db.relationship('RecebimentoFornecedor', backref='fornecedor', lazy=True)

    def __repr__(self):
        return f'<Fornecedor {self.nome}>'


class Estoque(db.Model):
    __tablename__ = 'estoques'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), unique=True, nullable=False)
    descricao = db.Column(db.String(255))
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

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


class EnderecoEstoque(db.Model):
    __tablename__ = 'enderecos_estoque'
    __table_args__ = (
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
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedores.id'), nullable=False)
    fornecedor_documento = db.Column(db.String(30), nullable=True)
    data_entrega = db.Column(db.Date, nullable=True)
    info_nota = db.Column(db.String(255), nullable=True)
    subtotal = db.Column(db.Float, nullable=True, default=0.0)
    desconto = db.Column(db.Float, nullable=True, default=0.0)
    total_pagar = db.Column(db.Float, nullable=True, default=0.0)
    status = db.Column(db.String(30), default=STATUS_CRIADO, nullable=False)
    observacoes = db.Column(db.Text, nullable=True)
    recebedor_nome = db.Column(db.String(120), nullable=True)
    recebedor_assinatura = db.Column(db.String(255), nullable=True)
    entregador_nome = db.Column(db.String(120), nullable=True)
    entregador_assinatura = db.Column(db.String(255), nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    conferido_em = db.Column(db.DateTime, nullable=True)
    armazenado_em = db.Column(db.DateTime, nullable=True)

    itens = db.relationship('RecebimentoItem', backref='recebimento', lazy=True, cascade='all, delete-orphan')

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

    id = db.Column(db.Integer, primary_key=True)
    mesa_id = db.Column(db.Integer, db.ForeignKey('mesas.id'), nullable=True)
    caixa_id = db.Column(db.Integer, db.ForeignKey('caixas.id'), nullable=True)
    garcom_id = db.Column(db.Integer, db.ForeignKey('garcons.id'), nullable=True)
    cliente_nome = db.Column(db.String(120))
    cliente_celular = db.Column(db.String(30))
    total = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='aberto')  # aberto, em_preparo, entregue, fechado, cancelado
    origem = db.Column(db.String(20), default='interno')  # interno, qr
    metodo_pagamento = db.Column(db.String(50))
    valor_pago = db.Column(db.Float, nullable=True)
    estoque_processado = db.Column(db.Boolean, default=False)
    financeiro_processado = db.Column(db.Boolean, default=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    fechado_em = db.Column(db.DateTime)
    observacoes = db.Column(db.Text)

    itens = db.relationship('ItemPedido', backref='pedido', lazy=True, cascade='all, delete-orphan')

    def calcular_total(self):
        self.total = sum(item.quantidade * item.preco_unitario for item in self.itens)
        return self.total

    def __repr__(self):
        return f'<Pedido {self.id} - {self.status}>'


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

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='operador')  # admin, gerente, caixa, operador
    cargo = db.Column(db.String(100), nullable=True)
    ativo = db.Column(db.Boolean, default=True)
    controle_acesso_ativo = db.Column(db.Boolean, default=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    permissoes = db.relationship('PermissaoAcesso', backref='funcionario', lazy=True, cascade='all, delete-orphan')

    def set_password(self, senha):
        """Hash e armazena a senha."""
        self.senha_hash = generate_password_hash(senha)

    def check_password(self, senha):
        """Verifica se a senha fornecida corresponde ao hash armazenado."""
        return check_password_hash(self.senha_hash, senha)

    def __repr__(self):
        return f'<Funcionario {self.nome} - {self.role}>'


class FuncaoRH(db.Model):
    __tablename__ = 'funcoes_rh'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    descricao = db.Column(db.String(255))
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<FuncaoRH {self.nome}>'


class PermissaoAcesso(db.Model):
    __tablename__ = 'permissoes_acesso'

    id = db.Column(db.Integer, primary_key=True)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=False)
    pagina = db.Column(db.String(80), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('funcionario_id', 'pagina', name='uq_funcionario_pagina'),
    )

    def __repr__(self):
        return f'<PermissaoAcesso funcionario={self.funcionario_id} pagina={self.pagina}>'


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


class EmpresaConfig(db.Model):
    __tablename__ = 'empresa_config'

    id = db.Column(db.Integer, primary_key=True)
    razao_social = db.Column(db.String(150))
    nome_fantasia = db.Column(db.String(150))
    cnpj = db.Column(db.String(20))
    inscricao_estadual = db.Column(db.String(30))
    telefone = db.Column(db.String(30))
    email = db.Column(db.String(120))
    endereco = db.Column(db.String(200))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(2))
    cep = db.Column(db.String(12))
    logo_path = db.Column(db.String(255))
    mensagem_comprovante = db.Column(db.String(255))
    cardapio_titulo = db.Column(db.String(120))
    cardapio_subtitulo = db.Column(db.String(255))
    cardapio_mensagem = db.Column(db.String(255))
    cardapio_mostrar_imagem = db.Column(db.Boolean, default=True)
    cardapio_mostrar_descricao = db.Column(db.Boolean, default=True)
    cardapio_qtd_maxima = db.Column(db.Integer, default=20)
    atendimento_mesas_ativo = db.Column(db.Boolean, default=True)
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


```

---

### Arquivo: `README.md`

```md
# SystemLR - Gestão de Estoque

Um sistema web completo de gerenciamento de estoque para conveniências, desenvolvido com Flask e otimizado para funcionar em PC e dispositivos móveis.

**Website**: [systemlr.com](https://systemlr.com)

## 🎯 Funcionalidades

- ✅ **Dashboard** - Visualize estatísticas e alertas em tempo real
- 📦 **Gerenciamento de Produtos** - Cadastre, edite, visualize e delete produtos
- 🏷️ **Categorias** - Organize produtos por categorias
- 📊 **Movimentações** - Registre entradas e saídas de estoque
- 📈 **Relatórios** - Gere relatórios completos do estoque
- 📱 **Responsivo** - Interface adaptável para mobile e desktop
- 🔔 **Alertas** - Notificações de produtos em falta
- 💰 **Análise Financeira** - Cálculo de lucro e margem de lucro
- 💳 **Sistema de Vendas** - pedidos, mesas e caixas diretamente pela interface web

## 🛠️ Requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

## 📦 Instalação

### 1. Clonar ou extrair o projeto

```bash
cd c:\Users\lucas\OneDrive\Desktop\conveniencia
```

### 2. Criar ambiente virtual (recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

## 🚀 Como Usar

### 📁 Auto‑commit (opcional)
Se desejar que todas as alterações sejam registradas automaticamente no Git, há um pequeno script
`autocommit.ps1` na raiz. Abra o PowerShell na pasta do projeto e execute:

```powershell
.\.\autocommit.ps1
```

O script observa o diretório e faz `git add -A && git commit` com uma mensagem de timestamp cada
vez que um arquivo é modificado/criado/excluído. Pressione Enter para parar o watcher.



### 1. Executar a aplicação

```bash
python app.py
```

### 2. Acessar no navegador

- **Desktop**: http://localhost:5000
- **Mobile**: Acesse via IP da máquina (http://seu-ip:5000)

### 3. Primeiro acesso

- O banco de dados SQLite será criado automaticamente
- **Primeira vez**: Você será direcionado para criar a conta do administrador
- Comece criando categorias de produtos
- Cadastre seus produtos
- Registre movimentações de estoque
- Configure caixas e mesas para iniciar vendas
- Abra pedidos e acompanhe vendas
- Acompanhe relatórios e alertas

### 🔐 Autenticação e Controle de Acesso

O SystemLR agora oferece um sistema completo de autenticação com controle de acesso por função (role-based).

#### Roles Disponíveis:
- **🔴 Admin** - Acesso total ao sistema, gerenciamento de funcionários
- **🟠 Gerente** - Acesso a vendas, pedidos, relatórios e gerenciamento de operadores/caixas
- **🟡 Caixa** - Acesso a vendas, pedidos e movimentação de estoque
- **🟢 Operador** - Acesso limitado a movimentação de estoque e leitura de relatórios

#### Login/Registro:
1. **Primeira vez**: Crie a conta do administrador em `/registro`
2. **Novos funcionários**: Admin cria conta em `Funcionários → Novo Funcionário`
3. **Login**: Acesse `/login` com email e senha

#### Proteger Rotas:
Todas as rotas do sistema (exceto login/registro) requerem autenticação. Tente acessar qualquer página sem logar e será redirecionado para o login.

## 📁 Estrutura do Projeto

```
conveniencia/
├── app.py                 # Aplicação principal Flask
├── config.py              # Configurações
├── models.py              # Modelos de dados (SQLAlchemy)
├── requirements.txt       # Dependências do projeto
├── templates/             # Arquivos HTML
│   ├── base.html          # Template base
│   ├── sistema/           # Autenticação e sistema
│   │   ├── boas_vindas.html
│   │   ├── login.html     # Login
│   │   └── registro.html  # Registro de novo usuário
│   ├── funcionarios/      # Gerenciamento de funcionários (admin/gerente)
│   │   ├── listar.html
│   │   ├── criar.html
│   │   └── editar.html
│   ├── dashboard/         # Dashboard principal
│   │   └── index.html
│   ├── produtos/          # CRUD de produtos
│   │   ├── produtos.html
│   │   ├── novo_produto.html
│   │   ├── editar_produto.html
│   │   └── visualizar_produto.html
│   ├── categorias/        # CRUD de categorias
│   │   ├── categorias.html
│   │   ├── nova_categoria.html
│   │   └── editar_categoria.html
│   ├── movimentacoes/     # Histórico e registro de movimentações
│   │   ├── movimentacoes.html
│   │   ├── nova_movimentacao.html
│   │   └── movimentacao_rapida.html
│   ├── relatorios/        # Relatórios
│   │   └── relatorios.html
│   ├── caixas/            # CRUD de caixas
│   │   ├── caixas.html
│   │   ├── nova_caixa.html
│   │   └── editar_caixa.html
│   ├── mesas/             # CRUD de mesas
│   │   ├── mesas.html
│   │   ├── nova_mesa.html
│   │   └── editar_mesa.html
│   ├── pedidos/           # Pedidos (comandas)
│   │   ├── pedidos.html
│   │   ├── novo_pedido.html
│   │   └── editar_pedido.html
│   ├── vendas/            # Lista de vendas
│   │   └── vendas.html
│   ├── fornecedores/      # CRUD de fornecedores
│   │   ├── fornecedores.html
│   │   ├── novo_fornecedor.html
│   │   └── editar_fornecedor.html
│   ├── errors/            # Páginas de erro
│   │   ├── 404.html
│   │   └── 500.html
├── static/                # Arquivos estáticos
│   ├── css/
│   │   └── style.css      # Estilos responsivos
│   ├── js/
│   │   ├── main.js        # JavaScript e menus
│   │   └── quagga.min.js  # Leitura de código de barras
│   └── img/               # Imagens
└── estoque.db             # Banco de dados (criado automaticamente)
```

## 💾 Banco de Dados

O projeto usa **SQLite** com as seguintes tabelas:

### 1. **categorias**
- id (PK)
- nome (único)
- descricao
- criado_em

### 2. **produtos**
- id (PK)
- codigo (único)
- nome
- descricao
- categoria_id (FK)
- preco_custo
- preco_venda
- quantidade_estoque
- quantidade_minima
- ativo
- criado_em
- atualizado_em

### 3. **movimentacoes**
- id (PK)
- produto_id (FK)
- tipo (entrada/saida)
- quantidade
- motivo
- observacoes
- criado_em

### 4. **funcionarios** (Novo)
- id (PK)
- nome
- email (único)
- senha_hash (bcrypt)
- role (admin/gerente/caixa/operador)
- ativo
- criado_em
- atualizado_em

## 🎨 Design Responsivo

O sistema é totalmente responsivo com breakpoints para:

- **Desktop** (1200px+) - Visualização completa com múltiplas colunas
- **Tablet** (768px - 1199px) - Adaptação de grid e navegação
- **Mobile** (até 767px) - Layout vertical otimizado para toque

### Recursos Mobile:
- Menu hamburger colapsável
- Tabelas em modo de cards no mobile
- Botões grandes e fáceis de tocar
- Navegação intuitiva
- Otimização de performance

## 📊 Principais Funcionalidades

### Dashboard
- Total de produtos cadastrados
- Quantidade de produtos em falta
- Valor total de estoque
- Últimas movimentações registradas

### Produtos
- Busca e filtro por categoria
- Visualização de estoque e status
- Cálculo automático de lucro e margem
- Alertas de produtos em falta

### Movimentações
- Registro de entradas e saídas
- Filtro por produto e tipo
- Histórico completo com timestamps
- Atualização automática de estoque

### Relatórios
- Produtos em falta
- Produtos com maior valor em estoque
- Estatísticas gerais
- Movimentações do mês

## 🔒 Segurança

- ✅ **Autenticação**: Sistema de login com email e senha (bcrypt hashing)
- ✅ **Controle de Acesso**: Role-based access control (RBAC) com 4 níveis
- ✅ **Proteção de Rotas**: Todas as rotas protegidas com @login_required
- ✅ **Sessão Segura**: Cookies de sessão com SameSite=Lax
- ✅ **Senhas Criptografadas**: Uso de werkzeug.security para hash bcrypt
- ⚠️ **Produção**: Configure SECRET_KEY com um valor aleatório forte em produção
- ⚠️ **HTTPS**: Use HTTPS em produção
- ⚠️ **Variáveis de Ambiente**: Nunca commite credenciais no repositório

## 🚦 Fazendo Builds e Deploy

### Para Produção

1. Mude a configuração de debug:
   ```python
   app.run(debug=False)
   ```

2. Configure um servidor WSGI (Gunicorn):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

3. Use um proxy reverso (Nginx) para melhor performance

## 📝 Exemplos de Uso

### Criar primeira categoria
1. Acesse "Categorias"
2. Clique em "➕ Nova Categoria"
3. Preencha o nome (ex: "Bebidas")
4. Clique em "✓ Salvar Categoria"

### Adicionar produto
1. Vá para "Produtos"
2. Clique em "➕ Novo Produto"
3. Preencha os dados:
   - Código: PROD001
   - Nome: Refrigerante 2L
   - Categoria: Bebidas
   - Preço de Custo: 3.50
   - Preço de Venda: 5.50
4. Clique em "✓ Salvar Produto"

### Registrar movimentação
1. Acesse "Movimentações"
2. Clique em "➕ Nova Movimentação"
3. Selecione o produto
4. Escolha o tipo (Entrada/Saída)
5. Informe quantidade e motivo
6. Clique em "✓ Registrar Movimentação"

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"
→ Certifique-se de instalar as dependências: `pip install -r requirements.txt`

### "Erro ao conectar ao banco de dados"
→ Delete o arquivo `estoque.db` e execute novamente. O banco será recriado.

### Aplicação não acessível via mobile
→ Certifique-se de usar o IP correto: `ipconfig` (Windows) ou `ifconfig` (Linux)

## 📞 Suporte e Contribuições

Para melhorias e sugestões, considere adicionar:
- Sistema de backup automático
- Exportação de relatórios em PDF/Excel
- Autenticação de usuários
- Múltiplas validações de entrada
- Notificações por email
- Integração com sistemas de pagamento

## 📄 Licença

Este projeto é fornecido como está para uso educacional e comercial.

## 🌐 Sobre SystemLR

**SystemLR** é uma marca registrada dedicada a fornecer soluções de gestão de estoque simples, intuitivas e poderosas para pequenos e médios negócios.

- 🌟 Website: [systemlr.com](https://systemlr.com)
- 📧 Suporte disponível em tempo real
- 🚀 Sempre inovando para melhor atender seus clientes

---

**Desenvolvido com ❤️ em Flask | SystemLR - Sua Gestão Simplificada**

## Atualizacoes 2026-03-01 (Seguranca, Coerencia e Analytics)

### Seguranca

- CSRF global habilitado para formularios e requisicoes de escrita (`POST/PUT/PATCH/DELETE`).
- Cookies de sessao endurecidos (`HttpOnly`, `SameSite=Lax`, `Secure` em producao).
- Validacao de `SECRET_KEY` em ambiente de producao (fallback de desenvolvimento nao permitido).
- Respostas JSON padronizadas em APIs de escrita: `{ success, message, data?, code? }`.

### Coerencia de Pedidos

- Regra de ciclo de vida consolidada:
  - `aberto -> em_preparo -> entregue -> fechado` ou `cancelado`
  - `fechado` e `cancelado` sao imutaveis
- Fechamento do pedido agora processa estoque e financeiro uma unica vez.
- Baixa de estoque registrada em movimentacao de saida no fechamento.
- Caixa recebe entrada financeira no fechamento (nao mais na criacao).

### Novos Endpoints de Analytics

- `GET /api/dashboard/analytics?data_inicial=YYYY-MM-DD&data_final=YYYY-MM-DD`
- `GET /api/estoque/analytics?periodo=7|30|90`
- `GET /api/rh/analytics?periodo=30|90|365`

### Frontend Dinamico

- Dashboard com graficos Chart.js (faturamento diario, status, pagamentos, top produtos).
- Relatorios de estoque com graficos dinamicos por periodo.
- Indicadores RH com graficos por perfil e admissoes no periodo.

### Testes Automatizados Minimos

- Arquivo: `tests/test_system_flows.py`
- Cobertura inicial:
  - autenticacao obrigatoria em API
  - CSRF obrigatorio para escrita
  - fechamento imutavel de pedido
  - impacto de fechamento em estoque e caixa
```

---

### Arquivo: `realtime.py`

```py
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

---

### Arquivo: `requirements.txt`

```text
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Migrate==4.0.5
python-dotenv==1.0.0
qrcode==7.4.2
pillow==12.1.1
pytest==8.3.5
```

---

### Arquivo: `routes\__init__.py`

```py
# Package de rotas por domínio.
```

---

### Arquivo: `routes\estoque_routes.py`

```py
from datetime import datetime, timedelta
import os
import re
import unicodedata

from sqlalchemy.orm import selectinload

from flask import render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename

from models import (
    db,
    Categoria,
    EnderecoEstoque,
    Estoque,
    Produto,
    Movimentacao,
    Fornecedor,
    RecebimentoFornecedor,
    RecebimentoItem,
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

# pillow será usado para redimensionar/comprimir imagens
from PIL import Image

ALLOWED_IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp', '.gif'}


def register_estoque_routes(app, login_required, require_role, aplicar_movimentacao_estoque):
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
        Produto.STATUS_DISPONIVEL_VENDA: 'Disponivel para venda',
        Produto.STATUS_INDISPONIVEL: 'Indisponivel',
        Produto.STATUS_SOMENTE_RESSUPRIMENTO: 'Somente ressuprimento',
    }
    recebimento_status_labels = {
        RecebimentoFornecedor.STATUS_CRIADO: 'Criado',
        RecebimentoFornecedor.STATUS_AGUARDANDO_ARMAZENAGEM: 'Aguardando armazenagem',
        RecebimentoFornecedor.STATUS_CONCLUIDO: 'Concluido',
        RecebimentoFornecedor.STATUS_CANCELADO: 'Cancelado',
    }

    def _normalizar_status_disponibilidade(valor):
        status = (valor or Produto.STATUS_DISPONIVEL_VENDA).strip().lower()
        if status not in Produto.STATUS_DISPONIBILIDADE_VALIDOS:
            status = Produto.STATUS_DISPONIVEL_VENDA
        return status

    def _sem_acentos(texto):
        base = unicodedata.normalize('NFKD', str(texto or ''))
        return ''.join(c for c in base if not unicodedata.combining(c))

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

    def _aplicar_filtros_produtos(
        query,
        *,
        categoria_id=None,
        busca='',
        status_disponibilidade='',
        estoque_id=None,
        endereco_id=None,
        fornecedor_id=None,
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
        status = (status_disponibilidade or '').strip().lower()
        if status in Produto.STATUS_DISPONIBILIDADE_VALIDOS:
            query = query.filter(Produto.status_disponibilidade == status)
        if endereco_id:
            query = query.filter(Produto.endereco_id == endereco_id)
        if fornecedor_id:
            query = query.filter(Produto.fornecedor_id == fornecedor_id)
        if estoque_id:
            query = query.join(EnderecoEstoque, Produto.endereco_id == EnderecoEstoque.id).filter(
                EnderecoEstoque.estoque_id == estoque_id
            )
        return query
    def _is_allowed_image(filename):
        _, ext = os.path.splitext(filename.lower())
        return ext in ALLOWED_IMAGE_EXTENSIONS

    def _delete_image_file(relative_path):
        if not relative_path:
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

        safe_product_name = secure_filename((product_name or '').strip())
        if not safe_product_name:
            return None, 'Nome do produto invalido para nomear a imagem.'

        _, ext = os.path.splitext(file_storage.filename.lower())

        image_name = f'{safe_product_name}{ext}'
        relative_dir = os.path.join('uploads', 'produtos')
        absolute_dir = os.path.join(app.static_folder, relative_dir)
        os.makedirs(absolute_dir, exist_ok=True)
        relative_path = os.path.join(relative_dir, image_name).replace('\\', '/')
        absolute_path = os.path.join(app.static_folder, relative_path)

        # salvar arquivo temporariamente para depois processar
        file_storage.save(absolute_path)

        # otimizar imagem: redimensionar e comprimir
        try:
            img = Image.open(absolute_path)
            # limitar tamanho máximo (ex: 800x800) mantendo proporção
            max_size = (800, 800)
            img.thumbnail(max_size, Image.ANTIALIAS)
            # sobrescrever no mesmo caminho, usando otimização
            save_kwargs = {'optimize': True}
            if img.format and img.format.lower() in ['jpeg', 'jpg']:
                save_kwargs['quality'] = 85
            img.save(absolute_path, **save_kwargs)
        except Exception:
            # se falhar, não é crítico; deixamos a imagem original
            pass

        return relative_path, None

    def _save_category_image(file_storage, category_name):
        if not file_storage or not file_storage.filename:
            return None, None

        if not _is_allowed_image(file_storage.filename):
            return None, 'Formato de imagem invalido. Use PNG, JPG, JPEG, WEBP ou GIF.'

        safe_category_name = secure_filename((category_name or '').strip())
        if not safe_category_name:
            return None, 'Nome da categoria invalido para nomear a imagem.'

        _, ext = os.path.splitext(file_storage.filename.lower())

        image_name = f'{safe_category_name}{ext}'
        relative_dir = os.path.join('uploads', 'categorias')
        absolute_dir = os.path.join(app.static_folder, relative_dir)
        os.makedirs(absolute_dir, exist_ok=True)
        relative_path = os.path.join(relative_dir, image_name).replace('\\', '/')
        absolute_path = os.path.join(app.static_folder, relative_path)

        file_storage.save(absolute_path)

        try:
            img = Image.open(absolute_path)
            max_size = (800, 800)
            img.thumbnail(max_size, Image.ANTIALIAS)
            save_kwargs = {'optimize': True}
            if img.format and img.format.lower() in ['jpeg', 'jpg']:
                save_kwargs['quality'] = 85
            img.save(absolute_path, **save_kwargs)
        except Exception:
            pass

        return relative_path, None

    @app.route('/produtos')
    @login_required
    def listar_produtos():
        page = max(request.args.get('page', 1, type=int), 1)
        per_page = min(max(request.args.get('per_page', 20, type=int), 1), 100)
        categoria_id = request.args.get('categoria_id', type=int)
        busca = (request.args.get('busca') or '').strip()
        status_disponibilidade = (request.args.get('status_disponibilidade') or '').strip().lower()
        estoque_id = request.args.get('estoque_id', type=int)
        endereco_id = request.args.get('endereco_id', type=int)
        fornecedor_id = request.args.get('fornecedor_id', type=int)

        query = _aplicar_filtros_produtos(
            Produto.query,
            categoria_id=categoria_id,
            busca=busca,
            status_disponibilidade=status_disponibilidade,
            estoque_id=estoque_id,
            endereco_id=endereco_id,
            fornecedor_id=fornecedor_id,
        ).options(
            selectinload(Produto.categoria),
            selectinload(Produto.endereco),
            selectinload(Produto.fornecedor),
        )

        pagination = query.order_by(Produto.nome.asc()).paginate(page=page, per_page=per_page, error_out=False)
        produtos = pagination.items
        categorias = Categoria.query.order_by(Categoria.nome.asc()).all()
        enderecos = EnderecoEstoque.query.filter_by(ativo=True).order_by(EnderecoEstoque.nome.asc()).all()
        estoques = Estoque.query.filter_by(ativo=True).order_by(Estoque.nome.asc()).all()
        fornecedores = Fornecedor.query.filter_by(ativo=True).order_by(Fornecedor.nome.asc()).all()
        return render_template(
            'estoque/produtos/produtos.html',
            produtos=produtos,
            pagination=pagination,
            per_page=per_page,
            categorias=categorias,
            enderecos=enderecos,
            estoques=estoques,
            fornecedores=fornecedores,
            categoria_selecionada=categoria_id,
            busca=busca,
            filtros={
                'status_disponibilidade': status_disponibilidade,
                'estoque_id': estoque_id,
                'endereco_id': endereco_id,
                'fornecedor_id': fornecedor_id,
            },
            status_disponibilidade_labels=STATUS_DISPONIBILIDADE_LABELS,
            query_params=request.args.to_dict()
        )

    @app.route('/produtos/enderecos/armazenar-todos', methods=['POST'])
    @require_role(*estoque_write_roles)
    def armazenar_todos_produtos_enderecos():
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

            estoque = Estoque.query.get(estoque_id)
            if not estoque:
                flash('Estoque informado nao existe.', 'error')
                return redirect(url_for(
                    'listar_produtos',
                    categoria_id=categoria_id or '',
                    busca=busca,
                    status_disponibilidade=status_disponibilidade,
                    estoque_id=filtro_estoque_id or '',
                    endereco_id=filtro_endereco_id or '',
                ))

            enderecos = EnderecoEstoque.query.filter_by(
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
                Produto.query.order_by(Produto.id.asc()),
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

                codigo_raw = (request.form.get('codigo') or '').strip()
                codigo_barras = re.sub(r'\D', '', codigo_raw)
                if len(codigo_barras) not in {8, 12, 13, 14}:
                    flash('Codigo/SKU deve ser um codigo de barras numerico (8, 12, 13 ou 14 digitos).', 'error')
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
                    imagem_path=nova_imagem_path,
                    categoria_id=categoria_id,
                    fornecedor_id=fornecedor.id,
                    endereco_id=request.form.get('endereco_id', type=int) or None,
                    preco_custo=float(request.form.get('preco_custo', 0)),
                    preco_venda=float(request.form.get('preco_venda', 0)),
                    quantidade_estoque=int(request.form.get('quantidade_estoque', 0)),
                    quantidade_minima=int(request.form.get('quantidade_minima', 5)),
                    status_disponibilidade=_normalizar_status_disponibilidade(request.form.get('status_disponibilidade'))
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
        fornecedores = Fornecedor.query.filter_by(ativo=True).order_by(Fornecedor.nome.asc()).all()
        enderecos = EnderecoEstoque.query.filter_by(ativo=True).order_by(EnderecoEstoque.nome.asc()).all()
        return render_template(
            'estoque/produtos/novo_produto.html',
            categorias=categorias,
            fornecedores=fornecedores,
            enderecos=enderecos,
            status_disponibilidade_labels=STATUS_DISPONIBILIDADE_LABELS,
            codigos_existentes=[c[0] for c in db.session.query(Produto.codigo).all()]
        )

    @app.route('/produtos/<int:produto_id>/editar', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def editar_produto(produto_id):
        produto = Produto.query.get_or_404(produto_id)
        if request.method == 'POST':
            nova_imagem_path = None
            imagem_anterior = produto.imagem_path
            try:
                fornecedor_id = request.form.get('fornecedor_id', type=int)
                fornecedor = Fornecedor.query.get(fornecedor_id) if fornecedor_id else None
                if not fornecedor:
                    flash('Fornecedor invalido. Selecione um fornecedor para o produto.', 'error')
                    return redirect(url_for('editar_produto', produto_id=produto_id))
                produto.nome = request.form.get('nome')
                produto.descricao = request.form.get('descricao')
                produto.categoria_id = int(request.form.get('categoria_id'))
                produto.fornecedor_id = fornecedor.id
                produto.endereco_id = request.form.get('endereco_id', type=int) or None
                produto.preco_custo = float(request.form.get('preco_custo', 0))
                produto.preco_venda = float(request.form.get('preco_venda', 0))
                produto.quantidade_minima = int(request.form.get('quantidade_minima', 5))
                produto.status_disponibilidade = _normalizar_status_disponibilidade(request.form.get('status_disponibilidade'))

                remover_imagem = request.form.get('remover_imagem') == 'on'
                arquivo_imagem = request.files.get('imagem')

                if arquivo_imagem and arquivo_imagem.filename:
                    nova_imagem_path, erro_imagem = _save_product_image(arquivo_imagem, produto.nome)
                    if erro_imagem:
                        flash(erro_imagem, 'error')
                        return redirect(url_for('editar_produto', produto_id=produto_id))
                    produto.imagem_path = nova_imagem_path
                elif remover_imagem:
                    produto.imagem_path = None

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
        fornecedores = Fornecedor.query.filter_by(ativo=True).order_by(Fornecedor.nome.asc()).all()
        enderecos = EnderecoEstoque.query.filter_by(ativo=True).order_by(EnderecoEstoque.nome.asc()).all()
        return render_template(
            'estoque/produtos/editar_produto.html',
            produto=produto,
            categorias=categorias,
            fornecedores=fornecedores,
            enderecos=enderecos,
            status_disponibilidade_labels=STATUS_DISPONIBILIDADE_LABELS,
            codigos_existentes=[c[0] for c in db.session.query(Produto.codigo).filter(Produto.id != produto.id).all()]
        )

    @app.route('/produtos/<int:produto_id>')
    @login_required
    def visualizar_produto(produto_id):
        produto = Produto.query.get_or_404(produto_id)
        movimentacoes = Movimentacao.query.filter_by(produto_id=produto_id).order_by(
            Movimentacao.criado_em.desc()
        ).all()
        return render_template('estoque/produtos/visualizar_produto.html', produto=produto, movimentacoes=movimentacoes)

    @app.route('/produtos/<int:produto_id>/deletar', methods=['POST'])
    @require_role(*estoque_write_roles)
    def deletar_produto(produto_id):
        produto = Produto.query.get_or_404(produto_id)
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
        fornecedor_id = request.args.get('fornecedor_id', type=int)
        busca = (request.args.get('busca') or '').strip()
        data_inicio_txt = (request.args.get('data_inicio') or '').strip()
        data_fim_txt = (request.args.get('data_fim') or '').strip()
        data_inicio = _parse_data_filtro(data_inicio_txt)
        data_fim = _parse_data_filtro(data_fim_txt)

        query = RecebimentoFornecedor.query
        if status in RecebimentoFornecedor.STATUS_VALIDOS:
            query = query.filter(RecebimentoFornecedor.status == status)
        if fornecedor_id:
            query = query.filter(RecebimentoFornecedor.fornecedor_id == fornecedor_id)
        if data_inicio:
            query = query.filter(RecebimentoFornecedor.criado_em >= data_inicio)
        if data_fim:
            query = query.filter(RecebimentoFornecedor.criado_em < (data_fim + timedelta(days=1)))
        if busca:
            termo = f'%{busca}%'
            query = query.outerjoin(Fornecedor, Fornecedor.id == RecebimentoFornecedor.fornecedor_id).outerjoin(
                RecebimentoItem, RecebimentoItem.recebimento_id == RecebimentoFornecedor.id
            ).outerjoin(
                Produto, Produto.id == RecebimentoItem.produto_id
            ).filter(
                db.or_(
                    Fornecedor.nome.ilike(termo),
                    RecebimentoFornecedor.info_nota.ilike(termo),
                    RecebimentoFornecedor.observacoes.ilike(termo),
                    Produto.nome.ilike(termo),
                    Produto.codigo.ilike(termo),
                    db.cast(RecebimentoFornecedor.id, db.String).ilike(termo),
                )
            ).distinct()

        recebimentos = query.options(
            selectinload(RecebimentoFornecedor.fornecedor),
            selectinload(RecebimentoFornecedor.itens).selectinload(RecebimentoItem.produto),
        ).order_by(RecebimentoFornecedor.criado_em.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False,
        )
        fornecedores = Fornecedor.query.filter_by(ativo=True).order_by(Fornecedor.nome.asc()).all()
        return render_template(
            'estoque/recebimentos/recebimentos.html',
            recebimentos=recebimentos.items,
            pagination=recebimentos,
            per_page=per_page,
            fornecedores=fornecedores,
            status_labels=recebimento_status_labels,
            filtros={
                'status': status,
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
        fornecedores = Fornecedor.query.filter_by(ativo=True).order_by(Fornecedor.nome.asc()).all()
        produtos = Produto.query.filter_by(ativo=True).order_by(Produto.nome.asc()).all()

        if request.method == 'POST':
            try:
                fornecedor_id = request.form.get('fornecedor_id', type=int)
                fornecedor = Fornecedor.query.get(fornecedor_id) if fornecedor_id else None
                if not fornecedor:
                    flash('Selecione um fornecedor valido.', 'error')
                    return redirect(url_for('novo_recebimento_fornecedor'))

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
                    fornecedor_documento=(request.form.get('fornecedor_documento') or '').strip() or None,
                    data_entrega=data_entrega,
                    info_nota=(request.form.get('info_nota') or '').strip() or None,
                    subtotal=subtotal,
                    desconto=desconto,
                    total_pagar=total_pagar,
                    observacoes=(request.form.get('observacoes') or '').strip() or None,
                    recebedor_nome=(request.form.get('recebedor_nome') or '').strip() or None,
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
        )

    @app.route('/estoque/recebimentos/<int:recebimento_id>/conferir', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def conferir_recebimento_fornecedor(recebimento_id):
        recebimento = RecebimentoFornecedor.query.options(
            selectinload(RecebimentoFornecedor.fornecedor),
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
        )

    @app.route('/estoque/recebimentos/<int:recebimento_id>/armazenar', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def armazenar_recebimento_fornecedor(recebimento_id):
        recebimento = RecebimentoFornecedor.query.options(
            selectinload(RecebimentoFornecedor.fornecedor),
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

        enderecos_ativos = EnderecoEstoque.query.filter(EnderecoEstoque.status == 'ativo').order_by(EnderecoEstoque.nome.asc()).all()
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

                    erro_mov = aplicar_movimentacao_estoque(item.produto, Movimentacao.TIPO_ENTRADA, quantidade_entrada)
                    if erro_mov:
                        raise ValueError(f'Falha ao aplicar entrada de "{item.produto.nome}": {erro_mov}')

                    item.produto.endereco_id = endereco_destino.id
                    observacoes_mov = f'Recebimento #{recebimento.id}'
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
                        motivo='recebimento_fornecedor',
                        observacoes=observacoes_mov,
                    )
                    db.session.add(movimentacao)

                recebimento.status = RecebimentoFornecedor.STATUS_CONCLUIDO
                recebimento.armazenado_em = datetime.utcnow()
                db.session.commit()
                flash('Armazenagem concluida. Estoque atualizado com sucesso.', 'success')
                return redirect(url_for('listar_recebimentos_fornecedor'))
            except ValueError as e:
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

    @app.route('/enderecos-estoque')
    @login_required
    def listar_enderecos_estoque():
        estoque_id = request.args.get('estoque_id', type=int)
        setor_zona = (request.args.get('setor_zona') or '').strip().lower()
        busca = (request.args.get('busca') or '').strip()
        status = (request.args.get('status') or '').strip().lower()

        query = EnderecoEstoque.query
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

        enderecos = query.order_by(EnderecoEstoque.nome.asc()).all()
        estoques = Estoque.query.order_by(Estoque.nome.asc()).all()
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
        endereco = EnderecoEstoque.query.get_or_404(endereco_id)
        produtos = Produto.query.filter_by(endereco_id=endereco.id).order_by(Produto.nome.asc()).all()
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
        endereco = EnderecoEstoque.query.get_or_404(endereco_id)
        return render_template(
            'estoque/enderecos/etiquetas_enderecos.html',
            enderecos=[endereco],
            titulo='Etiqueta de Endereco',
        )

    @app.route('/enderecos-estoque/etiquetas')
    @login_required
    def imprimir_etiquetas_enderecos_estoque():
        estoque_id = request.args.get('estoque_id', type=int)
        query = EnderecoEstoque.query
        if estoque_id:
            query = query.filter(EnderecoEstoque.estoque_id == estoque_id)
        enderecos = query.filter(EnderecoEstoque.ativo.is_(True)).order_by(EnderecoEstoque.nome.asc()).all()
        if not enderecos:
            flash('Nenhum endereco ativo encontrado para imprimir etiquetas.', 'warning')
            return redirect(url_for('listar_enderecos_estoque', estoque_id=estoque_id or ''))
        return render_template(
            'estoque/enderecos/etiquetas_enderecos.html',
            enderecos=enderecos,
            titulo='Etiquetas de Enderecos',
        )

    @app.route('/estoques')
    @login_required
    def listar_estoques():
        busca = (request.args.get('busca') or '').strip()
        status = (request.args.get('status') or '').strip().lower()

        query = Estoque.query
        if busca:
            termo = f'%{busca}%'
            query = query.filter(
                db.or_(
                    Estoque.nome.ilike(termo),
                    Estoque.descricao.ilike(termo),
                )
            )
        if status == 'ativo':
            query = query.filter(Estoque.ativo.is_(True))
        elif status == 'inativo':
            query = query.filter(Estoque.ativo.is_(False))

        estoques = query.order_by(Estoque.nome.asc()).all()
        return render_template(
            'estoque/estoques/estoques.html',
            estoques=estoques,
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
                descricao = (request.form.get('descricao') or '').strip() or None
                ativo = (request.form.get('ativo') == 'on')

                if not nome:
                    flash('Nome do estoque e obrigatorio.', 'error')
                    return redirect(url_for('novo_estoque'))

                estoque = Estoque(nome=nome, descricao=descricao, ativo=ativo)
                db.session.add(estoque)
                db.session.commit()
                flash(f'Estoque "{estoque.nome}" criado com sucesso!', 'success')
                return redirect(url_for('listar_estoques'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao criar estoque: {str(e)}', 'error')
        return render_template('estoque/estoques/novo_estoque.html')

    @app.route('/estoques/<int:estoque_id>/editar', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def editar_estoque(estoque_id):
        estoque = Estoque.query.get_or_404(estoque_id)
        if request.method == 'POST':
            try:
                nome = (request.form.get('nome') or '').strip()
                descricao = (request.form.get('descricao') or '').strip() or None
                ativo = (request.form.get('ativo') == 'on')
                if not nome:
                    flash('Nome do estoque e obrigatorio.', 'error')
                    return redirect(url_for('editar_estoque', estoque_id=estoque.id))

                estoque.nome = nome
                estoque.descricao = descricao
                estoque.ativo = ativo
                db.session.commit()
                flash('Estoque atualizado com sucesso!', 'success')
                return redirect(url_for('listar_estoques'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao atualizar estoque: {str(e)}', 'error')
        return render_template('estoque/estoques/editar_estoque.html', estoque=estoque)

    @app.route('/estoques/<int:estoque_id>/deletar', methods=['POST'])
    @require_role(*estoque_write_roles)
    def deletar_estoque(estoque_id):
        estoque = Estoque.query.get_or_404(estoque_id)
        try:
            if EnderecoEstoque.query.filter_by(estoque_id=estoque.id).count() > 0:
                flash('Nao e possivel excluir estoque com enderecos vinculados.', 'error')
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
        estoques_ativos = Estoque.query.filter_by(ativo=True).order_by(Estoque.nome.asc()).all()
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
                estoque = Estoque.query.get(estoque_id)
                if not estoque:
                    flash('Estoque informado e invalido.', 'error')
                    return redirect(url_for('novo_endereco_estoque'))
                if not categoria_reservada_id:
                    flash('Selecione uma categoria para o tipo de produto reservado.', 'error')
                    return redirect(url_for('novo_endereco_estoque'))
                categoria_reservada = Categoria.query.get(categoria_reservada_id)
                if not categoria_reservada:
                    flash('Categoria de produto reservado invalida.', 'error')
                    return redirect(url_for('novo_endereco_estoque'))

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
                                tipo_produto_reservado=categoria_reservada.nome,
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
                    tipo_produto_reservado=categoria_reservada.nome,
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
        endereco = EnderecoEstoque.query.get_or_404(endereco_id)
        estoques_ativos = Estoque.query.filter_by(ativo=True).order_by(Estoque.nome.asc()).all()
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
                estoque = Estoque.query.get(estoque_id)
                if not estoque:
                    flash('Estoque informado e invalido.', 'error')
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
        endereco = EnderecoEstoque.query.get_or_404(endereco_id)
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
        produto = Produto.query.get_or_404(produto_id)
        if request.method == 'POST':
            try:
                tipo = request.form.get('tipo')
                quantidade = int(request.form.get('quantidade'))
                fornecedor_id = request.form.get('fornecedor_id', type=int)
                recebimento_fornecedor = (request.form.get('recebimento_fornecedor') == 'on')

                if tipo not in {Movimentacao.TIPO_ENTRADA, Movimentacao.TIPO_SAIDA}:
                    flash('Tipo de movimentacao invalido.', 'error')
                    return redirect(url_for('movimentacao_rapida', produto_id=produto_id))

                erro = aplicar_movimentacao_estoque(produto, tipo, quantidade)
                if erro:
                    flash(erro, 'error')
                    return redirect(url_for('movimentacao_rapida', produto_id=produto_id))

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
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao registrar movimentacao: {str(e)}', 'error')

        fornecedores = Fornecedor.query.filter_by(ativo=True).order_by(Fornecedor.nome.asc()).all()
        return render_template('estoque/movimentacoes/movimentacao_rapida.html', produto=produto, fornecedores=fornecedores)

    @app.route('/movimentacoes')
    @login_required
    def listar_movimentacoes():
        page = max(request.args.get('page', 1, type=int), 1)
        per_page = min(max(request.args.get('per_page', 25, type=int), 1), 100)
        produto_id = request.args.get('produto_id', type=int)
        status = (request.args.get('status') or request.args.get('tipo') or '').strip().lower()
        fornecedor_id = request.args.get('fornecedor_id', type=int)
        busca = (request.args.get('busca') or '').strip()
        data_inicio_txt = (request.args.get('data_inicio') or '').strip()
        data_fim_txt = (request.args.get('data_fim') or '').strip()
        data_inicio = _parse_data_filtro(data_inicio_txt)
        data_fim = _parse_data_filtro(data_fim_txt)

        query = Movimentacao.query
        if produto_id:
            query = query.filter_by(produto_id=produto_id)
        if status and status in [Movimentacao.TIPO_ENTRADA, Movimentacao.TIPO_SAIDA, Movimentacao.TIPO_TRANSFERENCIA]:
            query = query.filter_by(tipo=status)
        if fornecedor_id:
            query = query.filter(Movimentacao.fornecedor_id == fornecedor_id)
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
            selectinload(Movimentacao.produto),
            selectinload(Movimentacao.fornecedor)
        ).order_by(Movimentacao.criado_em.desc()).paginate(page=page, per_page=per_page, error_out=False)
        produtos = Produto.query.all()
        fornecedores = Fornecedor.query.filter_by(ativo=True).order_by(Fornecedor.nome.asc()).all()
        return render_template(
            'estoque/movimentacoes/movimentacoes.html',
            movimentacoes=movimentacoes.items,
            pagination=movimentacoes,
            per_page=per_page,
            produtos=produtos,
            fornecedores=fornecedores,
            produto_selecionado=produto_id,
            fornecedor_selecionado=fornecedor_id,
            status_selecionado=status,
            busca=busca,
            data_inicio=data_inicio_txt,
            data_fim=data_fim_txt,
            tipos_movimentacao=Movimentacao.TIPOS,
            query_params=request.args.to_dict()
        )

    @app.route('/movimentacoes/nova', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def nova_movimentacao():
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

                erro = aplicar_movimentacao_estoque(produto, tipo, quantidade)
                if erro:
                    flash(erro, 'error')
                    return redirect(url_for('nova_movimentacao'))

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
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao registrar movimentacao: {str(e)}', 'error')

        produtos = Produto.query.filter_by(ativo=True).all()
        fornecedores = Fornecedor.query.filter_by(ativo=True).order_by(Fornecedor.nome.asc()).all()
        return render_template('estoque/movimentacoes/nova_movimentacao.html', produtos=produtos, fornecedores=fornecedores)

    @app.route('/movimentacoes/transferencia', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def transferir_armazenamento():
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
                if not produto.endereco_id:
                    flash('Produto sem endereco de origem para transferencia.', 'error')
                    return redirect(url_for('transferir_armazenamento'))

                endereco_origem = EnderecoEstoque.query.get(produto.endereco_id)
                endereco_destino = EnderecoEstoque.query.filter_by(id=endereco_destino_id, ativo=True).first()
                if not endereco_destino:
                    flash('Endereco de destino invalido.', 'error')
                    return redirect(url_for('transferir_armazenamento'))
                if endereco_origem and endereco_origem.id == endereco_destino.id:
                    flash('Origem e destino nao podem ser iguais.', 'error')
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
                return redirect(url_for('listar_movimentacoes'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao transferir armazenamento: {str(e)}', 'error')

        produtos = Produto.query.filter(
            Produto.ativo.is_(True),
            Produto.endereco_id.isnot(None)
        ).order_by(Produto.nome.asc()).all()
        enderecos = EnderecoEstoque.query.filter_by(ativo=True).order_by(EnderecoEstoque.nome.asc()).all()
        return render_template(
            'estoque/movimentacoes/transferencia_armazenamento.html',
            produtos=produtos,
            enderecos=enderecos
        )

    @app.route('/api/estoque/analytics')
    @login_required
    def analytics_estoque_api():
        periodo = request.args.get('periodo', type=int) or 30
        if periodo not in {7, 30, 90}:
            periodo = 30

        data_limite = datetime.utcnow() - timedelta(days=periodo)
        movimentos_raw = db.session.query(
            db.func.date(Movimentacao.criado_em).label('dia'),
            Movimentacao.tipo.label('tipo'),
            db.func.sum(Movimentacao.quantidade).label('quantidade')
        ).filter(
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

        valor_categoria_raw = db.session.query(
            Categoria.nome.label('categoria_nome'),
            db.func.sum(Produto.quantidade_estoque * Produto.preco_custo).label('valor_total')
        ).join(Produto, Produto.categoria_id == Categoria.id).filter(
            Produto.ativo == True
        ).group_by(Categoria.id, Categoria.nome).order_by(db.desc('valor_total')).all()

        return jsonify({
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
                'produtos_em_falta': Produto.query.filter(
                    Produto.quantidade_estoque < Produto.quantidade_minima,
                    Produto.ativo == True
                ).count(),
                'produtos_sem_estoque': Produto.query.filter(
                    Produto.ativo == True,
                    Produto.quantidade_estoque <= 0
                ).count()
            }
        })

    @app.route('/relatorios')
    @login_required
    def relatorios():
        total_produtos = Produto.query.count()
        produtos_ativos = Produto.query.filter_by(ativo=True).count()
        produtos_inativos = Produto.query.filter_by(ativo=False).count()
        total_unidades = db.session.query(db.func.sum(Produto.quantidade_estoque)).scalar() or 0

        produtos_em_falta = Produto.query.filter(
            Produto.quantidade_estoque < Produto.quantidade_minima,
            Produto.ativo == True
        ).all()
        produtos_sem_estoque = Produto.query.filter(
            Produto.ativo == True,
            Produto.quantidade_estoque <= 0
        ).count()

        valor_total = db.session.query(
            db.func.sum(Produto.quantidade_estoque * Produto.preco_custo)
        ).scalar() or 0
        custo_medio_estoque = (valor_total / total_unidades) if total_unidades else 0

        produtos_maior_valor = db.session.query(
            Produto,
            (Produto.quantidade_estoque * Produto.preco_custo).label('valor_total')
        ).order_by(db.desc('valor_total')).limit(10).all()

        data_limite = datetime.utcnow() - timedelta(days=30)
        movimentacoes_mes = Movimentacao.query.filter(Movimentacao.criado_em >= data_limite).count()
        entradas_mes = Movimentacao.query.filter(
            Movimentacao.criado_em >= data_limite,
            Movimentacao.tipo == Movimentacao.TIPO_ENTRADA
        ).count()
        saidas_mes = Movimentacao.query.filter(
            Movimentacao.criado_em >= data_limite,
            Movimentacao.tipo == Movimentacao.TIPO_SAIDA
        ).count()

        data_sem_giro = datetime.utcnow() - timedelta(days=60)
        produtos_sem_giro = Produto.query.filter(
            Produto.ativo == True,
            ~Produto.movimentacoes.any(Movimentacao.criado_em >= data_sem_giro)
        ).order_by(Produto.nome.asc()).limit(10).all()

        valor_por_categoria = db.session.query(
            Categoria.nome.label('categoria_nome'),
            db.func.sum(Produto.quantidade_estoque * Produto.preco_custo).label('valor_total'),
            db.func.sum(Produto.quantidade_estoque).label('qtd_total'),
            db.func.count(Produto.id).label('produtos')
        ).join(Produto, Produto.categoria_id == Categoria.id).filter(
            Produto.ativo == True
        ).group_by(Categoria.id, Categoria.nome).order_by(
            db.desc('valor_total')
        ).all()

        valor_por_endereco = db.session.query(
            EnderecoEstoque.nome.label('endereco_nome'),
            db.func.count(Produto.id).label('produtos'),
            db.func.sum(Produto.quantidade_estoque).label('qtd_total'),
            db.func.sum(Produto.quantidade_estoque * Produto.preco_custo).label('valor_total')
        ).join(Produto, Produto.endereco_id == EnderecoEstoque.id).filter(
            Produto.ativo == True
        ).group_by(EnderecoEstoque.id, EnderecoEstoque.nome).order_by(
            db.desc('valor_total')
        ).all()

        return render_template(
            'estoque/relatorios/relatorios.html',
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
            produtos_sem_giro=produtos_sem_giro,
            valor_por_categoria=valor_por_categoria,
            valor_por_endereco=valor_por_endereco
        )
```

---

### Arquivo: `routes\public_routes.py`

```py
import re
import unicodedata

from flask import Blueprint, abort, flash, redirect, render_template, request, session, url_for

from models import Categoria, EmpresaConfig, Garcom, ItemPedido, Mesa, Pedido, Produto, db
from realtime import publish_alert


CLIENTE_SESSION_KEY = 'qr_clientes'


def _obter_empresa_config():
    empresa = EmpresaConfig.query.first()
    if not empresa:
        empresa = EmpresaConfig()
        db.session.add(empresa)
        db.session.commit()
    return empresa


def _slugify(texto):
    normalizado = unicodedata.normalize('NFKD', (texto or '').strip())
    ascii_texto = normalizado.encode('ascii', 'ignore').decode('ascii').lower()
    ascii_texto = re.sub(r'[^a-z0-9]+', '-', ascii_texto).strip('-')
    return ascii_texto or 'cliente'


def _atendimento_mesas_ativo():
    empresa = _obter_empresa_config()
    return empresa.atendimento_mesas_ativo is not False


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


def register_public_routes(app):
    bp = Blueprint('public', __name__)

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

---

### Arquivo: `routes\vendas_routes.py`

```py
from datetime import datetime
import secrets
import qrcode
from io import BytesIO
from flask import render_template, request, redirect, url_for, flash, session, Response, jsonify
from sqlalchemy.orm import selectinload

from models import db, Caixa, Mesa, Pedido, Produto, ItemPedido, Movimentacao, MovimentacaoCaixa, Funcionario, Garcom, EmpresaConfig
from realtime import publish_alert, sse_stream
from security import json_response


METODOS_PAGAMENTO = {'dinheiro', 'cartao', 'pix', 'crediario', 'dividido'}
ORDER_ALLOWED_TRANSITIONS = {
    'aberto': {'em_preparo', 'entregue', 'fechado', 'cancelado'},
    'em_preparo': {'entregue', 'fechado', 'cancelado'},
    'entregue': {'fechado', 'cancelado'},
    'fechado': set(),
    'cancelado': set(),
}
ORDER_IMMUTABLE_STATUSES = {'fechado', 'cancelado'}


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


def _bloquear_se_atendimento_mesas_desativado():
    if _atendimento_mesas_ativo():
        return None
    flash('Modulo de mesas e garcons esta desativado para esta empresa.', 'warning')
    return redirect(url_for('pdv'))


def _to_float(valor, default=None):
    if valor is None or valor == '':
        return default
    if isinstance(valor, str):
        valor = valor.replace(',', '.').strip()
    return float(valor)


def _build_payment_data(metodo_raw, valor_raw, total_pedido, split_raw=None, cliente_crediario=''):
    metodo = (metodo_raw or '').strip().lower()
    if metodo not in METODOS_PAGAMENTO:
        raise ValueError('Metodo de pagamento invalido.')
    total = float(total_pedido or 0.0)

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
        metodo_texto = f'dividido (dinheiro: {valor_dinheiro:.2f} | cartao: {valor_cartao:.2f})'
        return metodo_texto, valor_pago

    valor_pago = _to_float(valor_raw, None)
    if valor_pago is None:
        valor_pago = 0.0 if metodo == 'crediario' else float(total_pedido or 0.0)
    if valor_pago < 0:
        raise ValueError('Valor pago nao pode ser negativo.')

    if metodo == 'crediario':
        cliente = (cliente_crediario or '').strip()
        metodo_texto = f'crediario ({cliente})' if cliente else 'crediario'
    else:
        if metodo == 'dinheiro' and valor_pago < total:
            raise ValueError('Valor recebido insuficiente para finalizar o pedido.')
        metodo_texto = metodo

    return metodo_texto, valor_pago


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


def _normalizar_item_payload(item):
    produto_id = item.get('produto_id')
    quantidade = item.get('quantidade', 1)
    try:
        produto_id = int(produto_id)
        quantidade = int(quantidade)
    except (TypeError, ValueError):
        return None, 'Item invalido.'
    if quantidade <= 0:
        return None, 'Quantidade deve ser maior que zero.'
    produto = Produto.query.get(produto_id)
    if not produto or not produto.ativo:
        return None, 'Produto invalido ou inativo.'
    return {'produto': produto, 'quantidade': quantidade}, None


def _recalcular_total_pedido(pedido):
    pedido.total = sum((item.quantidade or 0) * (item.preco_unitario or 0) for item in pedido.itens)
    return pedido.total


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
    status_atual = _parse_status(pedido.status, default='aberto')
    novo_status = _parse_status(novo_status, default=status_atual)

    if status_atual in ORDER_IMMUTABLE_STATUSES and novo_status != status_atual:
        raise ValueError(f'Pedido {status_atual} e imutavel.')
    if novo_status != status_atual and novo_status not in ORDER_ALLOWED_TRANSITIONS.get(status_atual, set()):
        raise ValueError(f'Transicao invalida: {status_atual} -> {novo_status}.')

    if novo_status == 'fechado' and status_atual != 'fechado':
        _processar_fechamento_pedido(pedido)
    elif novo_status == 'cancelado' and status_atual != 'cancelado':
        pedido.fechado_em = datetime.utcnow()
        if pedido.mesa:
            pedido.mesa.status = 'livre'
    elif pedido.mesa and novo_status in {'aberto', 'em_preparo', 'entregue'}:
        pedido.mesa.status = 'ocupada'

    pedido.status = novo_status
    return pedido.status


def register_vendas_routes(app, login_required, require_role):
    vendas_operacao_roles = ('admin', 'gerente', 'caixa', 'operador', 'garcom')
    vendas_gestao_roles = ('admin', 'gerente')
    caixa_operacao_roles = ('admin', 'gerente', 'caixa')
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
        page = max(request.args.get('page', 1, type=int), 1)
        per_page = min(max(request.args.get('per_page', 20, type=int), 1), 100)
        status_filtro = (request.args.get('status') or '').strip().lower()
        busca = (request.args.get('busca') or '').strip()

        query = Pedido.query.options(
            selectinload(Pedido.mesa),
            selectinload(Pedido.caixa),
            selectinload(Pedido.garcom)
        )
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

        pedidos = query.order_by(Pedido.criado_em.desc()).paginate(page=page, per_page=per_page, error_out=False)
        return render_template(
            'vendas/pedidos/pedidos.html',
            pedidos=pedidos.items,
            pagination=pedidos,
            per_page=per_page,
            status_filtro=status_filtro,
            busca=busca,
            query_params=request.args.to_dict(),
            status_transitions=ORDER_ALLOWED_TRANSITIONS
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
        except ValueError as exc:
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
            atendimento_mesas_ativo=atendimento_mesas_ativo
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
        return render_template('vendas/pedidos/detalhes_pedido.html', pedido=pedido)

    @app.route('/pdv')
    @require_role(*vendas_operacao_roles)
    def pdv():
        """Interface de PDV (Ponto de Venda) para o operador de caixa"""
        atendimento_mesas_ativo = _atendimento_mesas_ativo()
        produtos = Produto.query.filter_by(ativo=True).order_by(Produto.nome).all()
        caixas_abertas = Caixa.query.filter_by(aberto=True).all()
        mesas = Mesa.query.all() if atendimento_mesas_ativo else []
        garcons = Garcom.query.filter_by(ativo=True).order_by(Garcom.nome.asc()).all() if atendimento_mesas_ativo else []
        return render_template(
            'vendas/pdv.html',
            produtos=produtos,
            caixas_abertas=caixas_abertas,
            mesas=mesas,
            garcons=garcons,
            atendimento_mesas_ativo=atendimento_mesas_ativo
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

            if atendimento_mesas_ativo and mesa_id:
                mesa = Mesa.query.get(mesa_id)
                if mesa:
                    mesa.status = 'ocupada'

            db.session.commit()
            publish_alert(f"Nova venda! Pedido #{pedido.id} - Total: R$ {pedido.total:.2f}")

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
            if metodo:
                metodo_texto, valor_pago = _build_payment_data(
                    metodo_raw=metodo,
                    valor_raw=dados.get('valor_pago'),
                    total_pedido=pedido.total,
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
        except ValueError as e:
            db.session.rollback()
            status_code, code = _http_status_for_order_error(str(e))
            return json_response(False, str(e), status=status_code, code=code)
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

---

### Arquivo: `scripts\generate_qrcodes.py`

```py
"""
Gera QR Codes para todas as mesas com token, salvando em ./qrcodes/.
Uso:
    python scripts/generate_qrcodes.py --base-url http://localhost:5000
"""
import argparse
import os

import qrcode
from flask import Flask

from app import app, db
from models import Mesa


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base-url', default='http://localhost:5000', help='Base da aplicação (sem barra final)')
    parser.add_argument('--out-dir', default='qrcodes', help='Diretório de saída')
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    with app.app_context():
        mesas = Mesa.query.all()
        for mesa in mesas:
            if not mesa.qr_token:
                continue
            url = f"{args.base_url}/m/{mesa.qr_token}"
            img = qrcode.make(url)
            filename = os.path.join(args.out_dir, f"mesa_{mesa.numero}.png")
            img.save(filename)
            print(f"QR gerado para mesa {mesa.numero}: {filename}")


if __name__ == '__main__':
    main()
```

---

### Arquivo: `scripts\healthcheck.py`

```py
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import app
from models import (
    Categoria,
    EnderecoEstoque,
    Fornecedor,
    Funcionario,
    Movimentacao,
    Produto,
    RecebimentoFornecedor,
    db,
)


def _run_integrity_checks() -> list[str]:
    issues: list[str] = []

    sem_categoria = (
        db.session.query(Produto)
        .outerjoin(Categoria, Produto.categoria_id == Categoria.id)
        .filter(Categoria.id.is_(None))
        .count()
    )
    sem_fornecedor = (
        db.session.query(Produto)
        .outerjoin(Fornecedor, Produto.fornecedor_id == Fornecedor.id)
        .filter((Produto.fornecedor_id.is_(None)) | (Fornecedor.id.is_(None)))
        .count()
    )
    sem_endereco = (
        db.session.query(Produto)
        .outerjoin(EnderecoEstoque, Produto.endereco_id == EnderecoEstoque.id)
        .filter((Produto.endereco_id.is_(None)) | (EnderecoEstoque.id.is_(None)))
        .count()
    )
    codigos_dup = (
        db.session.query(Produto.codigo, db.func.count(Produto.id))
        .group_by(Produto.codigo)
        .having(db.func.count(Produto.id) > 1)
        .all()
    )
    end_cod_dup = (
        db.session.query(EnderecoEstoque.codigo_localizacao, db.func.count(EnderecoEstoque.id))
        .filter(EnderecoEstoque.codigo_localizacao.isnot(None))
        .group_by(EnderecoEstoque.codigo_localizacao)
        .having(db.func.count(EnderecoEstoque.id) > 1)
        .all()
    )
    mov_qtd_neg = Movimentacao.query.filter(Movimentacao.quantidade <= 0).count()
    receb_status_invalid = (
        db.session.query(RecebimentoFornecedor)
        .filter(~RecebimentoFornecedor.status.in_(RecebimentoFornecedor.STATUS_VALIDOS))
        .count()
    )

    print("INTEGRITY_SUMMARY")
    print(f"PRODUTOS_TOTAL={Produto.query.count()}")
    print(f"PRODUTOS_SEM_CATEGORIA={sem_categoria}")
    print(f"PRODUTOS_SEM_FORNECEDOR={sem_fornecedor}")
    print(f"PRODUTOS_SEM_ENDERECO={sem_endereco}")
    print(f"PRODUTOS_CODIGO_DUP={len(codigos_dup)}")
    print(f"ENDERECOS_TOTAL={EnderecoEstoque.query.count()}")
    print(f"ENDERECOS_CODIGO_DUP={len(end_cod_dup)}")
    print(f"MOVIMENTACOES_QTD_NEG_OU_ZERO={mov_qtd_neg}")
    print(f"RECEBIMENTOS_STATUS_INVALIDO={receb_status_invalid}")

    if sem_categoria:
        issues.append("Produtos sem categoria")
    if sem_fornecedor:
        issues.append("Produtos sem fornecedor")
    if sem_endereco:
        issues.append("Produtos sem endereco")
    if codigos_dup:
        issues.append("Duplicidade de codigo de produto")
    if end_cod_dup:
        issues.append("Duplicidade de codigo_localizacao")
    if mov_qtd_neg:
        issues.append("Movimentacoes com quantidade <= 0")
    if receb_status_invalid:
        issues.append("Recebimentos com status invalido")

    return issues


def _run_smoke_get_checks() -> list[str]:
    issues: list[str] = []
    user = Funcionario.query.filter_by(ativo=True).order_by(Funcionario.id.asc()).first()
    if not user:
        print("SMOKE_SKIPPED=sem_funcionario_ativo")
        return issues

    client = app.test_client()
    with client.session_transaction() as sess:
        sess["funcionario_id"] = user.id
        sess["funcionario_nome"] = user.nome
        sess["funcionario_role"] = user.role

    failures: list[tuple[str, int | str]] = []
    ok = 0
    skipped = 0
    for rule in app.url_map.iter_rules():
        if rule.endpoint == "static":
            continue
        if "GET" not in rule.methods:
            continue
        if rule.arguments:
            skipped += 1
            continue
        path = rule.rule
        if path.startswith("/api/pedidos/sse"):
            skipped += 1
            continue
        if any(k in path for k in ("/download", "/print")):
            skipped += 1
            continue
        try:
            resp = client.get(path)
            if resp.status_code >= 500:
                failures.append((path, resp.status_code))
            else:
                ok += 1
        except Exception:
            failures.append((path, "EXC"))

    print("SMOKE_SUMMARY")
    print(f"SMOKE_USER={user.id}:{user.role}")
    print(f"GET_OK={ok}")
    print(f"GET_SKIPPED={skipped}")
    print(f"GET_500_OR_EXC={len(failures)}")
    for path, status in failures[:30]:
        print(f"FAIL {status} {path}")

    if failures:
        issues.append("Endpoints GET com erro 500/excecao")
    return issues


def main() -> int:
    with app.app_context():
        issues = []
        issues.extend(_run_integrity_checks())
        issues.extend(_run_smoke_get_checks())

    if issues:
        print("HEALTHCHECK_STATUS=ISSUES")
        print("HEALTHCHECK_ISSUES=" + "; ".join(issues))
        return 1

    print("HEALTHCHECK_STATUS=OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

---

### Arquivo: `security.py`

```py
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

---

### Arquivo: `seed_data.py`

```py
"""
Script para popular o banco de dados com dados de teste.
Execute: python seed_data.py
"""
import sys
from datetime import datetime, timedelta
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

---

### Arquivo: `static\css\core\layout.css`

```css
.main-content {
    padding-left: 0;
    padding-right: 0;
}

.content-shell {
    width: 100%;
    max-width: 1320px;
    margin: 0 auto;
    padding-left: 12px;
    padding-right: 12px;
}

.page-container {
    width: 100%;
}

.page-header .header-actions {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}

.btn,
.btn-small {
    max-width: 100%;
}

/* Painel minimizavel/expansivel */
.panel-toggle-head,
.pdv-panel-head,
.card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    flex-wrap: wrap;
}

.panel-toggle-head > h1,
.panel-toggle-head > h2,
.panel-toggle-head > h3,
.panel-toggle-head > h4 {
    margin: 0 !important;
    border: 0 !important;
    padding: 0 !important;
}

.section > .panel-toggle-head {
    border-bottom: 2px solid var(--primary);
    margin-bottom: 16px;
    padding-bottom: 10px;
}

.panel-toggle-btn {
    margin-left: auto;
    white-space: nowrap;
    flex-shrink: 0;
}

.panel-collapsed .panel-collapsible-content {
    display: none !important;
}

/* Harmonizacao responsiva com Bootstrap (aplica em todas as paginas) */
@media (max-width: 992px) {
    .filters-form {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 10px;
        align-items: end;
    }

    .filter-group {
        min-width: 0;
    }

    .page-header {
        align-items: flex-start;
    }

    .page-header .header-actions {
        width: 100%;
    }

    .page-header .header-actions .btn {
        flex: 1 1 180px;
    }
}

@media (max-width: 768px) {
    .content-shell {
        padding-left: 8px;
        padding-right: 8px;
    }

    .form-row {
        grid-template-columns: 1fr !important;
        gap: 12px;
    }

    .form-actions {
        display: grid;
        grid-template-columns: 1fr;
        gap: 10px;
    }

    .form-actions .btn {
        width: 100%;
    }

    .btn,
    .btn-small {
        white-space: normal;
        text-wrap: balance;
        overflow-wrap: anywhere;
    }

    .action-buttons {
        display: grid;
        grid-template-columns: 1fr;
        gap: 10px;
    }

    .action-buttons > * {
        width: 100%;
        min-width: 0;
    }

    .page-header .header-actions {
        display: grid;
        grid-template-columns: 1fr;
        width: 100%;
    }

    .page-header .header-actions > * {
        width: 100%;
        min-width: 0;
    }

    .page-header .header-actions .btn,
    .page-header .header-actions .btn-small {
        width: 100%;
    }

    .barcode-input-group {
        display: grid;
        grid-template-columns: 1fr;
        gap: 8px;
    }

    .barcode-input-group .btn {
        width: 100%;
    }

    .panel-toggle-btn {
        width: 100%;
        margin-left: 0;
    }
}

@media (max-width: 576px) {
    .page-header h1 {
        font-size: 1.35rem;
    }

    .form-container,
    .filters-section,
    .section,
    .card {
        padding: 14px;
    }
}
```

---

### Arquivo: `static\css\core\tables.css`

```css
.table thead th {
    white-space: nowrap;
}

.table td[data-label] {
    vertical-align: middle;
    overflow-wrap: anywhere;
    word-break: break-word;
}

.actions-cell {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 6px;
}

/* Listagens do estoque com cabecalho fixo + rolagem */
.table-scroll-sticky {
    max-height: min(62vh, 720px);
    overflow: auto;
    border: 1px solid var(--border);
    border-radius: 8px;
}

.table-scroll-sticky .table {
    margin: 0;
    box-shadow: none;
    border-radius: 0;
    table-layout: fixed;
    width: 100%;
}

.table-scroll-sticky .table thead th {
    position: sticky;
    top: 0;
    z-index: 4;
    background: var(--dark);
    color: #fff;
}

@media (max-width: 768px) {
    .table-scroll-sticky {
        max-height: none;
        overflow: visible;
        border: none;
    }

    .actions-cell {
        display: grid;
        grid-template-columns: 1fr;
        width: 100%;
    }

    .actions-cell > * {
        width: 100%;
        min-width: 0;
    }

    .actions-cell .btn,
    .actions-cell .btn-small,
    .actions-cell .inline-form {
        width: 100%;
    }

    .actions-cell .inline-form .btn,
    .actions-cell .inline-form .btn-small {
        width: 100%;
    }
}
```

---

### Arquivo: `static\css\core\tokens.css`

```css
:root {
    --bp-mobile: 480px;
    --bp-tablet: 768px;
    --bp-laptop: 1024px;
}
```

---

### Arquivo: `static\css\pages\cardapio.css`

```css
﻿        :root {
            --menu-bg: #f3f5ef;
            --menu-paper: #ffffff;
            --menu-ink: #1f2933;
            --menu-muted: #5f6c76;
            --menu-brand: #14532d;
            --menu-brand-soft: #d8f3dc;
            --menu-border: #d4ded4;
            --menu-accent: #0f766e;
        }

        body.public-menu {
            background:
                radial-gradient(1200px 420px at 10% -5%, #d9f99d 0%, rgba(217, 249, 157, 0) 50%),
                radial-gradient(1200px 440px at 90% -10%, #a7f3d0 0%, rgba(167, 243, 208, 0) 55%),
                var(--menu-bg);
            color: var(--menu-ink);
            margin: 0;
            font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
        }

        .menu-shell {
            max-width: 1180px;
            margin: 0 auto;
            padding: 18px 14px 28px;
        }

        .menu-top {
            background: var(--menu-paper);
            border: 1px solid var(--menu-border);
            border-radius: 18px;
            padding: 18px;
            box-shadow: 0 12px 28px rgba(0, 0, 0, 0.06);
            margin-bottom: 14px;
        }

.menu-logo-wrap {
    margin-bottom: 8px;
}

.menu-logo {
    max-height: 72px;
    width: auto;
}

        .menu-top h1 {
            margin: 0 0 6px;
            font-size: 1.5rem;
            color: #0f172a;
        }

        .menu-subtitle {
            margin: 0;
            color: var(--menu-muted);
        }

        .menu-client {
            margin-top: 10px;
            padding: 10px 12px;
            border-radius: 12px;
            background: var(--menu-brand-soft);
            color: #0b3b22;
            font-weight: 600;
        }

        .flash-stack {
            margin-bottom: 14px;
        }

        .menu-grid {
            display: grid;
            grid-template-columns: minmax(0, 1.8fr) minmax(300px, 1fr);
            gap: 14px;
        }

        .menu-panel {
            background: var(--menu-paper);
            border: 1px solid var(--menu-border);
            border-radius: 18px;
            padding: 16px;
            box-shadow: 0 10px 24px rgba(0, 0, 0, 0.05);
        }

        .menu-panel h2 {
            margin-top: 0;
            margin-bottom: 10px;
        }

        .category-filter {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-bottom: 14px;
        }

        .category-pill {
            border: 1px solid #b8c8bc;
            background: #fff;
            color: #23302a;
            border-radius: 999px;
            padding: 8px 12px;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.9rem;
        }

        .category-pill.active {
            background: var(--menu-brand);
            color: #fff;
            border-color: var(--menu-brand);
        }

        .category-section {
            border: 1px solid #e1e8e2;
            border-radius: 14px;
            overflow: hidden;
            margin-bottom: 12px;
            background: #fcfdfb;
        }

        .category-header {
            display: grid;
            grid-template-columns: 96px minmax(0, 1fr);
            gap: 10px;
            padding: 10px;
            border-bottom: 1px solid #e6ece7;
            background: #f8faf7;
        }

        .category-header.no-image {
            grid-template-columns: 1fr;
        }

        .category-image {
            width: 100%;
            height: 70px;
            object-fit: cover;
            border-radius: 10px;
            border: 1px solid #d8e2da;
        }

        .category-title {
            margin: 0 0 3px;
            font-size: 1.05rem;
        }

        .category-desc {
            margin: 0;
            color: var(--menu-muted);
            font-size: 0.9rem;
        }

        .product-list {
            display: grid;
            gap: 10px;
            padding: 10px;
        }

        .product-item {
            display: grid;
            grid-template-columns: 68px minmax(0, 1fr) 110px;
            gap: 10px;
            border: 1px solid #e2e8e3;
            border-radius: 12px;
            padding: 8px;
            align-items: center;
            background: #fff;
        }

        .product-item.no-image {
            grid-template-columns: minmax(0, 1fr) 110px;
        }

        .product-image {
            width: 68px;
            height: 68px;
            object-fit: cover;
            border-radius: 10px;
        }

        .product-name {
            margin: 0 0 4px;
            font-size: 0.95rem;
        }

        .product-desc {
            margin: 0;
            color: var(--menu-muted);
            font-size: 0.82rem;
        }

        .product-price {
            margin-top: 5px;
            font-weight: 700;
            color: #0b3b22;
        }

        .product-qtd label {
            display: block;
            font-size: 0.78rem;
            color: var(--menu-muted);
            margin-bottom: 4px;
        }

        .product-qtd input {
            width: 100%;
            text-align: center;
        }

        .submit-wrap {
            position: sticky;
            bottom: 8px;
            margin-top: 10px;
            padding-top: 8px;
            background: linear-gradient(to top, #fff 78%, rgba(255, 255, 255, 0));
        }

        .orders-list {
            display: grid;
            gap: 10px;
        }

        .order-card {
            border: 1px solid #dce5de;
            border-radius: 12px;
            padding: 10px;
            background: #fff;
        }

        .order-head {
            display: flex;
            justify-content: space-between;
            gap: 8px;
            flex-wrap: wrap;
            margin-bottom: 6px;
        }

        .order-status {
            border-radius: 999px;
            padding: 4px 10px;
            font-size: 0.8rem;
            font-weight: 700;
            background: #e5e7eb;
        }

        .order-status.aberto {
            background: #dcfce7;
            color: #14532d;
        }

        .order-status.em_preparo {
            background: #fef9c3;
            color: #713f12;
        }

        .order-status.entregue {
            background: #dbeafe;
            color: #1e3a8a;
        }

        .order-status.fechado {
            background: #d1fae5;
            color: #065f46;
        }

        .order-status.cancelado {
            background: #fee2e2;
            color: #991b1b;
        }

        .order-items {
            margin: 0;
            padding-left: 18px;
            color: #334155;
        }

        .order-meta {
            margin-top: 6px;
            color: var(--menu-muted);
            font-size: 0.84rem;
        }

        .empty-box {
            border: 1px dashed #bfd0c2;
            border-radius: 10px;
            padding: 14px;
            color: var(--menu-muted);
            text-align: center;
        }

        @media (max-width: 980px) {
            .menu-grid {
                grid-template-columns: 1fr;
            }
        }

        @media (max-width: 580px) {
            .product-item {
                grid-template-columns: 56px minmax(0, 1fr);
            }

            .product-item.no-image {
                grid-template-columns: minmax(0, 1fr);
            }

            .product-qtd {
                grid-column: 1 / -1;
            }

            .category-header {
                grid-template-columns: 78px minmax(0, 1fr);
            }
        }
```

---

### Arquivo: `static\css\pages\pdv.css`

```css
﻿    .pdv-container {
        display: grid;
        grid-template-columns: minmax(0, 1fr) 360px;
        gap: 16px;
        align-items: start;
    }

    .pdv-panel {
        background: #fff;
        border: 1px solid var(--border);
        border-radius: 14px;
        box-shadow: var(--shadow);
        overflow: hidden;
    }

    .pdv-panel-head {
        padding: 12px 14px;
        border-bottom: 1px solid var(--border);
        background: #f8fafc;
        font-weight: 700;
        color: #0f172a;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
        flex-wrap: wrap;
    }

    .pdv-panel-body {
        padding: 14px;
    }

    .pdv-toolbar {
        display: flex;
        gap: 8px;
        align-items: center;
        margin-bottom: 12px;
    }

    .pdv-produtos {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(152px, 1fr));
        gap: 10px;
        max-height: 72vh;
        overflow-y: auto;
        padding: 2px;
    }

    .produto-card {
        background: #fff;
        border: 1px solid #d7dee6;
        border-radius: 10px;
        padding: 10px;
        text-align: center;
        display: flex;
        flex-direction: column;
        gap: 6px;
        transition: border-color 0.2s, box-shadow 0.2s, transform 0.2s;
    }

    .produto-card:hover {
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(15, 118, 110, 0.1);
        transform: translateY(-1px);
    }

    .produto-card.added {
        border-color: #198754;
        box-shadow: 0 0 0 3px rgba(25, 135, 84, 0.15);
        animation: pulseAdd 0.8s ease-in-out;
    }

    .produto-card.low-stock {
        background-color: #fff8e1;
        border-color: #ffcf66;
    }

    @keyframes pulseAdd {
        0% { transform: scale(1); }
        50% { transform: scale(1.03); }
        100% { transform: scale(1); }
    }

    .produto-imagem {
        width: 100%;
        height: 84px;
        object-fit: contain;
    }

    .produto-nome {
        font-weight: 700;
        font-size: 0.86rem;
        color: #1f2937;
        min-height: 36px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .produto-preco {
        font-size: 0.95rem;
        color: var(--primary);
        font-weight: 700;
    }

    .produto-estoque {
        font-size: 0.75rem;
        color: #64748b;
    }

    .btn-add-produto {
        width: 100%;
        padding: 6px 8px;
        border: none;
        border-radius: 8px;
        background: #198754;
        color: #fff;
        font-size: 0.8rem;
        font-weight: 700;
    }

    .btn-add-produto:hover {
        background: #157347;
    }

    .field-label {
        display: block;
        font-size: 0.75rem;
        color: #64748b;
        font-weight: 600;
        margin-bottom: 5px;
    }

    .pedido-header {
        display: flex;
        gap: 10px;
        margin-bottom: 10px;
        flex-wrap: wrap;
    }

    .pedido-select {
        width: 100%;
        min-height: 40px;
        border: 1px solid #ced5dd;
        border-radius: 8px;
        padding: 8px 10px;
        font-size: 0.9rem;
    }

    .pedido-filtros {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 8px;
        margin-bottom: 10px;
    }

    .pedido-select-hidden {
        display: none;
    }

    .open-orders-panel {
        border: 1px solid #dbe2ea;
        border-radius: 10px;
        padding: 8px;
        margin-bottom: 12px;
        background: #f9fbfe;
    }

    .open-orders-header {
        display: flex;
        justify-content: space-between;
        gap: 8px;
        margin-bottom: 8px;
        align-items: center;
    }

    .open-orders-title {
        font-size: 0.76rem;
        font-weight: 700;
        color: #475569;
    }

    .open-orders-count {
        font-size: 0.75rem;
        color: var(--primary);
        font-weight: 700;
    }

    .open-orders-list {
        max-height: 240px;
        overflow-y: auto;
        display: grid;
        gap: 8px;
    }

    .open-order-item {
        width: 100%;
        text-align: left;
        border: 1px solid #d8e2ef;
        border-radius: 10px;
        background: #fff;
        padding: 10px;
        cursor: pointer;
        transition: border-color 0.2s, box-shadow 0.2s;
    }

    .open-order-item:hover {
        border-color: var(--primary);
        box-shadow: 0 0 0 2px rgba(15, 118, 110, 0.1);
    }

    .open-order-item.active {
        border-color: var(--primary);
        background: #eef8f7;
        box-shadow: 0 0 0 2px rgba(15, 118, 110, 0.16);
    }

    .open-order-top {
        display: flex;
        justify-content: space-between;
        gap: 8px;
        font-size: 0.78rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 4px;
    }

    .open-order-meta {
        display: flex;
        justify-content: space-between;
        gap: 8px;
        color: #64748b;
        font-size: 0.72rem;
    }

    .itens-lista {
        min-height: 190px;
        max-height: 260px;
        overflow-y: auto;
        border: 1px solid #dbe2ea;
        border-radius: 10px;
        padding: 10px;
        background: #fafcff;
        margin-bottom: 12px;
    }

    .item-pedido {
        background: #fff;
        border-radius: 8px;
        border-left: 3px solid var(--primary);
        padding: 10px;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        gap: 10px;
        align-items: center;
        font-size: 0.8rem;
    }

    .item-pedido.highlight {
        background: #fff7db;
        animation: highlightPulse 0.6s ease-in-out;
    }

    @keyframes highlightPulse {
        0% { background-color: #fff7db; }
        50% { background-color: #fff2bf; }
        100% { background-color: #fff7db; }
    }

    .item-info {
        flex: 1;
    }

    .item-produto {
        font-weight: 700;
        color: #1f2937;
    }

    .item-qty {
        color: #64748b;
        font-size: 0.72rem;
    }

    .item-preco {
        color: #047857;
        font-weight: 700;
        white-space: nowrap;
    }

    .btn-remove-item {
        border: none;
        border-radius: 7px;
        background: #dc3545;
        color: #fff;
        padding: 5px 9px;
        font-size: 0.72rem;
    }

    .btn-remove-item:hover {
        background: #bb2d3b;
    }

    .pedido-resumo {
        background: #f8fafc;
        border: 1px solid #dbe2ea;
        border-radius: 10px;
        padding: 11px;
        margin-bottom: 12px;
    }

    .resumo-linha,
    .resumo-total {
        display: flex;
        justify-content: space-between;
        gap: 8px;
    }

    .resumo-linha {
        font-size: 0.83rem;
        margin-bottom: 7px;
    }

    .resumo-total {
        font-size: 1rem;
        color: var(--primary);
        font-weight: 800;
        border-top: 2px solid #d3dce6;
        padding-top: 8px;
    }

    .pedido-acoes {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
    }

    .btn-pedido {
        flex: 1;
        min-height: 44px;
        border: none;
        border-radius: 8px;
        font-size: 0.84rem;
        font-weight: 700;
    }

    .btn-nova-venda {
        background: #198754;
        color: #fff;
    }

    .btn-finalizar {
        background: var(--primary);
        color: #fff;
    }

    .btn-pedido:disabled {
        opacity: 0.55;
        cursor: not-allowed;
    }

    .vazio {
        text-align: center;
        color: #94a3b8;
        padding: 20px 10px;
        font-size: 0.8rem;
    }

    .payment-modal {
        position: fixed;
        inset: 0;
        background: rgba(15, 23, 42, 0.55);
        display: none;
        align-items: center;
        justify-content: center;
        padding: 16px;
        z-index: 1200;
    }

    .payment-modal.open {
        display: flex;
    }

    .payment-modal-content {
        width: 100%;
        max-width: 560px;
        background: #fff;
        border-radius: 12px;
        border: 1px solid var(--border);
        box-shadow: 0 16px 36px rgba(2, 6, 23, 0.3);
        padding: 18px;
    }

    .payment-title {
        margin-top: 0;
        margin-bottom: 8px;
        font-size: 1.2rem;
    }

    .payment-subtitle {
        margin-bottom: 12px;
        color: #475569;
    }

    .payment-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 8px;
        margin-bottom: 10px;
    }

    .payment-option {
        border: 1px solid #d4dce5;
        border-radius: 8px;
        padding: 9px 10px;
        cursor: pointer;
        background: #f8fafc;
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 0.9rem;
        font-weight: 600;
    }

    .payment-option-row {
        grid-column: 1 / -1;
    }

    .payment-fields {
        margin-top: 10px;
        display: grid;
        gap: 10px;
    }

    .payment-row {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 10px;
    }

    .payment-actions {
        display: flex;
        gap: 10px;
        margin-top: 14px;
    }

    .payment-receipt-option {
        margin-top: 10px;
        margin-bottom: 4px;
        font-size: 0.9rem;
    }

    .payment-actions .btn {
        flex: 1;
    }

    @media (max-width: 1100px) {
.is-hidden {
    display: none !important;
}

    .pdv-container {
            grid-template-columns: 1fr;
        }

        .pedido-panel {
            position: static;
        }
    }

    @media (max-width: 768px) {
        .pdv-toolbar {
            flex-wrap: wrap;
        }

        .pdv-toolbar > * {
            width: 100%;
        }

        .pdv-produtos {
            grid-template-columns: repeat(2, minmax(0, 1fr));
            max-height: 56vh;
        }

        .pedido-filtros {
            grid-template-columns: 1fr;
        }

        .pedido-acoes {
            flex-direction: column;
            position: sticky;
            bottom: 0;
            background: #fff;
            border-top: 1px solid #e2e8f0;
            padding-top: 8px;
            z-index: 5;
        }

        .btn-pedido {
            width: 100%;
        }

        .payment-grid,
        .payment-row {
            grid-template-columns: 1fr;
        }

        .payment-actions {
            flex-direction: column;
        }
    }

    @media (max-width: 480px) {
        .pdv-produtos {
            grid-template-columns: 1fr;
            max-height: 46vh;
        }

        .item-pedido {
            flex-wrap: wrap;
        }

        .item-preco {
            width: 100%;
        }
    }
```

---

### Arquivo: `static\css\pages\pedidos.css`

```css
﻿    .pedido-filtros {
        margin-bottom: 14px;
    }

    .pedido-filtros-form {
        display: flex;
        gap: 8px;
        align-items: center;
        flex-wrap: wrap;
    }

    .pedido-filtros-form .form-control,
    .pedido-filtros-form .form-select {
        min-width: 180px;
        flex: 1 1 220px;
    }

    .pedido-status-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 700;
        line-height: 1.2;
    }

    .pedido-status-aberto {
        background: #dbeafe;
        color: #1e3a8a;
    }

    .pedido-status-em_preparo {
        background: #fef3c7;
        color: #92400e;
    }

    .pedido-status-entregue {
        background: #dcfce7;
        color: #166534;
    }

    .pedido-status-fechado {
        background: #ccfbf1;
        color: #115e59;
    }

    .pedido-status-cancelado {
        background: #fee2e2;
        color: #991b1b;
    }

    .pedido-pagamento-linha {
        font-size: 12px;
        color: #64748b;
        margin-top: 4px;
    }

    .pedido-actions-cell {
        min-width: 320px;
    }

    .pedido-actions {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        align-items: flex-start;
    }

    .pedido-status-form {
        display: flex;
        gap: 6px;
        align-items: center;
        flex-wrap: wrap;
        width: 100%;
    }

    .pedido-status-form .form-select {
        min-width: 150px;
        flex: 1 1 150px;
    }

    .pedido-actions .btn {
        white-space: nowrap;
    }

    @media (max-width: 768px) {
        .col-celular,
        .col-garcom,
        .col-pagamento,
        .col-valor-pago {
            display: none;
        }

        .pedido-actions-cell {
            min-width: 0;
        }

        .pedido-filtros-form .form-control,
        .pedido-filtros-form .form-select {
            width: 100%;
            min-width: 0;
        }

        .pedido-actions,
        .pedido-status-form {
            width: 100%;
        }

        .pedido-actions .btn,
        .pedido-status-form .btn,
        .pedido-status-form .form-select {
            width: 100%;
            min-width: 0;
        }
    }
```

---

### Arquivo: `static\css\style.css`

```css
﻿/* ========================================
   VARIÃVEIS E ESTILOS GLOBAIS
   ======================================== */

:root {
    --primary: #0f766e;
    --primary-dark: #0b5d56;
    --secondary: #0ea5a4;
    --success: #28a745;
    --danger: #dc3545;
    --warning: #ffc107;
    --info: #17a2b8;
    --light: #f8fafc;
    --dark: #1f2937;
    --border: #d8e2e7;
    --shadow: 0 8px 20px rgba(15, 23, 42, 0.08);
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html, body {
    height: 100%;
    margin: 0;
    padding: 0;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #ffffff;
    color: var(--dark);
    line-height: 1.6;
}

img, video, canvas, svg {
    max-width: 100%;
    height: auto;
}

/* ========================================
   LAYOUT GERAL
   ======================================== */

body {
    display: flex;
    flex-direction: column;
}

.main-content {
    flex: 1;
    padding: 20px;
}

.footer {
    background-color: var(--dark);
    color: white;
    text-align: center;
    padding: 15px;
    margin-top: 40px;
    font-size: 0.9em;
}

/* ========================================
   NAVBAR - RESPONSIVA
   ======================================== */

.navbar {
    background-color: var(--primary);
    padding: 0;
    margin: 0;
    box-shadow: var(--shadow);
    position: sticky;
    top: 0;
    left: 0;
    right: 0;
    z-index: 100;
}

.navbar-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}


.brand-link {
    color: white;
    text-decoration: none;
}

.brand-link:hover {
    text-decoration: underline;
}

.navbar-menu {
    display: flex;
    align-items: center;
    gap: 0;
}

.item-row {
    display: flex;
    gap: 8px;
    margin-bottom: 8px;
    align-items: center;
}

.actions-cell {
    white-space: nowrap;
}

.nav-dropdown {
    position: relative;
}

.nav-dropdown-toggle {
    background: transparent;
    border: none;
    color: white;
    padding: 15px;
    font-size: 0.95em;
    cursor: pointer;
    font-family: inherit;
}

.nav-dropdown-toggle:hover {
    background-color: var(--primary-dark);
}

.nav-submenu {
    display: none;
    position: absolute;
    left: 0;
    top: 100%;
    min-width: 230px;
    background-color: var(--primary-dark);
    box-shadow: var(--shadow);
    z-index: 200;
}

.nav-dropdown:hover .nav-submenu,
.nav-dropdown.open .nav-submenu {
    display: block;
}

.nav-sublink {
    display: block;
    width: 100%;
    padding: 10px 12px;
}

.nav-submenu-empty {
    display: block;
    padding: 10px 12px;
    color: #fff;
    opacity: 0.85;
    font-size: 0.9em;
}

@media (max-width: 767px) {
    .navbar-menu {
        flex-direction: column;
        align-items: flex-start;
    }

    .nav-dropdown {
        width: 100%;
    }

    .nav-dropdown-toggle {
        width: 100%;
        text-align: left;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }

    .nav-submenu {
        position: static;
        width: 100%;
        background-color: rgba(0,0,0,0.1);
        box-shadow: none;
    }

    .nav-sublink {
        padding-left: 30px;
    }
}

.nav-link {
    color: white;
    padding: 15px 15px;
    text-decoration: none;
    transition: background-color 0.3s;
}

.nav-link:hover {
    background-color: var(--primary-dark);
}

.menu-toggle {
    display: none;
    background: none;
    border: none;
    color: white;
    font-size: 1.5em;
    cursor: pointer;
    width: 42px;
    height: 42px;
    border-radius: 6px;
    align-items: center;
    justify-content: center;
}

.menu-toggle:hover {
    background-color: rgba(255, 255, 255, 0.12);
}

.menu-toggle:focus-visible {
    outline: 2px solid #fff;
    outline-offset: 2px;
}

.nav-dropdown-user {
    margin-left: auto;
}

.nav-user-toggle {
    background-color: var(--primary);
    color: white;
    font-weight: 600;
}

/* ========================================
   CONTAINER
   ======================================== */

.container {
    max-width: 1200px;
    margin: 0 auto;
    width: 100%;
}

/* ========================================
   HEADERS E TÃTULOS
   ======================================== */

.page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
    flex-wrap: wrap;
    gap: 10px;
}

.page-header h1 {
    font-size: 2em;
    color: var(--dark);
}

.page-header .header-actions {
    display: flex;
    gap: 10px;
}

/* ========================================
   CARDS - RESUMO
   ======================================== */

.cards-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.card {
    background: white;
    border-radius: 8px;
    padding: 20px;
    box-shadow: var(--shadow);
    display: flex;
    align-items: center;
    gap: 20px;
    transition: transform 0.3s;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.card-icon {
    font-size: 2.5em;
    flex-shrink: 0;
}

.card-content h3 {
    font-size: 0.9em;
    color: #666;
    margin-bottom: 5px;
}

.card-value {
    font-size: 1.8em;
    font-weight: bold;
    margin: 0;
}

/* VariaÃ§Ãµes de cor */
.card-primary .card-icon { color: var(--primary); }
.card-success .card-icon { color: var(--success); }
.card-danger .card-icon { color: var(--danger); }
.card-warning .card-icon { color: var(--warning); }
.card-info .card-icon { color: var(--info); }

/* ========================================
   BUTTONS
   ======================================== */

.btn, .btn-small {
    display: inline-block;
    padding: 10px 15px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    text-decoration: none;
    font-size: 0.95em;
    transition: all 0.3s;
}

.btn {
    padding: 12px 20px;
    font-size: 1em;
}

.btn-small {
    padding: 5px 10px;
    font-size: 0.85em;
}

.btn-primary, .btn-small.btn-primary {
    background-color: var(--primary);
    color: white;
}

.btn-primary:hover {
    background-color: var(--primary-dark);
}

.btn-secondary, .btn-small.btn-secondary {
    background-color: var(--secondary);
    color: white;
}

.btn-secondary:hover {
    background-color: #653a7f;
}

.btn-success, .btn-small.btn-success {
    background-color: var(--success);
    color: white;
}

.btn-success:hover {
    background-color: #218838;
}

.btn-warning, .btn-small.btn-warning {
    background-color: var(--warning);
    color: white;
}

.btn-warning:hover {
    background-color: #e0a800;
}

.btn-danger, .btn-small.btn-danger {
    background-color: var(--danger);
    color: white;
}

.btn-danger:hover {
    background-color: #c82333;
}

.btn-info, .btn-small.btn-info {
    background-color: var(--info);
    color: white;
}

.btn-info:hover {
    background-color: #138496;
}

.btn-outline {
    background-color: transparent;
    border: 2px solid var(--primary);
    color: var(--primary);
}

.btn-outline:hover {
    background-color: var(--primary);
    color: white;
}

.action-buttons {
    display: flex;
    gap: 10px;
    margin: 20px 0;
    flex-wrap: wrap;
}

/* ========================================
   FORMULÃRIOS
   ======================================== */

.form-container {
    background: white;
    border-radius: 8px;
    padding: 30px;
    box-shadow: var(--shadow);
}

.form {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.form-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
}

.form-group {
    display: flex;
    flex-direction: column;
}

.form-group label {
    font-weight: 500;
    margin-bottom: 5px;
    color: var(--dark);
}

.input-text, .input-select, .input-textarea, .input-search {
    padding: 10px 12px;
    border: 1px solid var(--border);
    border-radius: 4px;
    font-size: 0.95em;
    font-family: inherit;
    transition: border-color 0.3s;
}

.input-text:focus, .input-select:focus, .input-textarea:focus, .input-search:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.input-textarea {
    resize: vertical;
}

.form-actions {
    display: flex;
    gap: 10px;
    margin-top: 10px;
    flex-wrap: wrap;
}

.barcode-input-group {
    display: flex;
    gap: 10px;
    align-items: center;
}

.barcode-input-group .input-text,
.barcode-input-group .input-search {
    flex: 1;
}

.barcode-btn {
    white-space: nowrap;
}

.barcode-scanner-modal {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.55);
    display: none;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    padding: 20px;
}

.barcode-scanner-modal.active {
    display: flex;
}

.barcode-scanner-content {
    background: #fff;
    border-radius: 8px;
    box-shadow: var(--shadow);
    width: 100%;
    max-width: 560px;
    overflow: hidden;
}

.barcode-scanner-header {
    padding: 14px 16px;
    border-bottom: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.barcode-scanner-title {
    font-size: 1rem;
    font-weight: 600;
}

.barcode-scanner-close {
    border: none;
    background: transparent;
    font-size: 1.4rem;
    cursor: pointer;
    line-height: 1;
}

.barcode-scanner-body {
    padding: 16px;
}

.barcode-scanner-video {
    width: 100%;
    border-radius: 6px;
    background: #000;
}

.barcode-scanner-help {
    margin-top: 10px;
    color: #555;
    font-size: 0.9rem;
}

/* ========================================
   TABELAS - RESPONSIVAS
   ======================================== */

.table-responsive {
    overflow-x: auto;
    margin: 20px 0;
    -webkit-overflow-scrolling: touch;
}

.table {
    width: 100%;
    border-collapse: collapse;
    background: white;
    box-shadow: var(--shadow);
    border-radius: 4px;
    overflow: hidden;
}

.table thead {
    background-color: var(--dark);
    color: white;
}

.table th, .table td {
    padding: 12px 15px;
    text-align: left;
}

.table tbody tr {
    border-bottom: 1px solid var(--border);
    transition: background-color 0.3s;
}

.table tbody tr:hover {
    background-color: #f5f5f5;
}

.table tbody tr.row-warning {
    background-color: #FFF8DC;
}

.actions-cell {
    display: flex;
    gap: 5px;
}

/* ========================================
   ALERTAS E BADGES
   ======================================== */

.alert {
    padding: 15px 20px;
    border-radius: 4px;
    margin-bottom: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.alert-success {
    background-color: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
}

.alert-error {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
}

.alert-warning {
    background-color: #fff3cd;
    color: #856404;
    border: 1px solid #ffeeba;
}

.alert-info {
    background-color: #d1ecf1;
    color: #0c5460;
    border: 1px solid #bee5eb;
}

.close-alert {
    cursor: pointer;
    font-size: 1.3em;
    font-weight: bold;
}

.badge {
    display: inline-block;
    padding: 3px 8px;
    border-radius: 12px;
    font-size: 0.85em;
    font-weight: 500;
}

.badge-success {
    background-color: var(--success);
    color: white;
}

.badge-danger {
    background-color: var(--danger);
    color: white;
}

.badge-warning {
    background-color: var(--warning);
    color: white;
}

/* ========================================
   SEÃ‡Ã•ES
   ======================================== */

.section {
    background: white;
    border-radius: 8px;
    padding: 25px;
    margin-bottom: 30px;
    box-shadow: var(--shadow);
}

.section h2 {
    font-size: 1.5em;
    margin-bottom: 20px;
    color: var(--dark);
    border-bottom: 2px solid var(--primary);
    padding-bottom: 10px;
}

/* ========================================
   FILTROS
   ======================================== */

.filters-section {
    background: white;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: var(--shadow);
}

.filters-form {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    align-items: flex-end;
}

.filter-group {
    flex: 1;
    min-width: 200px;
}

.input-search {
    width: 100%;
}

/* ========================================
   GRID DE CATEGORIAS
   ======================================== */

.grid-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
    margin: 20px 0;
}

.card-category {
    background: white;
    border-radius: 8px;
    padding: 20px;
    box-shadow: var(--shadow);
    display: flex;
    flex-direction: column;
    gap: 10px;
    transition: transform 0.3s;
}

.card-category:hover {
    transform: translateY(-3px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.card-category-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.card-category-header h3 {
    margin: 0;
}

.card-category-desc {
    color: #666;
    font-size: 0.9em;
    min-height: 40px;
}

.card-category-actions {
    display: flex;
    gap: 10px;
    padding-top: 10px;
    border-top: 1px solid var(--border);
}

/* ========================================
   INFO CARDS
   ======================================== */

.info-cards-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
    margin-bottom: 20px;
}

.info-card {
    background: white;
    border-left: 4px solid var(--primary);
    padding: 15px;
    border-radius: 4px;
    box-shadow: var(--shadow);
}

.info-card h3 {
    font-size: 0.9em;
    color: #666;
    margin-bottom: 8px;
}

.info-card .value {
    font-size: 1.5em;
    font-weight: bold;
    margin: 0;
}

.info-card.card-warning {
    border-left-color: var(--warning);
}

/* ========================================
   ERRO 404/500
   ======================================== */

.error-container {
    text-align: center;
    padding: 60px 20px;
}

.error-code {
    font-size: 5em;
    font-weight: bold;
    color: var(--danger);
    margin-bottom: 10px;
}

.error-container h1 {
    font-size: 2em;
    margin-bottom: 20px;
}

/* ========================================
   UTILITY CLASSES
   ======================================== */

.text-center {
    text-align: center;
}

.text-right {
    text-align: right;
}

.icon-warning {
    margin-left: 5px;
}

.info-box {
    background-color: #e3f2fd;
    border-left: 4px solid var(--info);
    padding: 15px;
    border-radius: 4px;
    margin: 15px 0;
}

.info-box p {
    margin: 5px 0;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 15px;
}

.stat-box {
    background: white;
    border-radius: 8px;
    padding: 20px;
    text-align: center;
    box-shadow: var(--shadow);
}

.stat-box h4 {
    color: #666;
    margin-bottom: 10px;
}

.stat-value {
    font-size: 2em;
    font-weight: bold;
    color: var(--primary);
    margin: 0;
}

/* ========================================
   PRODUTOS - IMAGENS
   ======================================== */

.product-name-cell {
    display: flex;
    align-items: center;
    gap: 10px;
}

.product-thumb {
    width: 42px;
    height: 42px;
    object-fit: cover;
    border-radius: 6px;
    border: 1px solid var(--border);
    flex-shrink: 0;
}

.product-thumb-sm {
    width: 34px;
    height: 34px;
}

.product-image-preview {
    margin-top: 10px;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.product-image-preview img {
    width: 110px;
    height: 110px;
    object-fit: cover;
    border-radius: 8px;
    border: 1px solid var(--border);
}

.checkbox-inline {
    display: inline-flex;
    align-items: center;
    gap: 8px;
}

.product-detail-image {
    width: min(380px, 100%);
    height: auto;
    object-fit: cover;
    border-radius: 10px;
    border: 1px solid var(--border);
}

/* ========================================
   CARDAPIO PUBLICO
   ======================================== */

.public-menu {
    background-color: #f4f6fb;
}

.narrow {
    max-width: 980px;
    padding: 24px 16px 40px;
}

.grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
    gap: 16px;
}

.card-product-menu {
    display: flex;
    flex-direction: column;
    padding: 0;
    overflow: hidden;
}

.menu-product-image {
    width: 100%;
    height: 160px;
    object-fit: cover;
}

.card-body {
    padding: 16px;
}

.text-muted {
    color: #6c757d;
}

.form-control {
    width: 100%;
    padding: 10px 12px;
    border: 1px solid var(--border);
    border-radius: 4px;
}

.btn-block {
    width: 100%;
}

/* ========================================
   DASHBOARD ANALITICO
   ======================================== */

.analytics-cards .card {
    min-height: 140px;
    justify-content: center;
}

.card-meta {
    margin-top: 8px;
    color: #6b7280;
    font-size: 0.9em;
}

.dashboard-filter-form {
    display: inline-flex;
    align-items: center;
    gap: 8px;
}

.dashboard-filter-label {
    font-weight: 600;
    color: #4b5563;
}

.dashboard-filter-select {
    min-width: 170px;
}

.dashboard-filter-button {
    white-space: nowrap;
}

.analytics-grid {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 20px;
    margin-bottom: 20px;
}

.chart-container {
    position: relative;
    width: 100%;
    height: 300px;
}

.chart-container canvas {
    width: 100% !important;
    height: 100% !important;
}

.performance-chart-container {
    height: 300px;
    margin-bottom: 14px;
}

.analytics-kpi-list {
    display: grid;
    gap: 10px;
}

.analytics-kpi-item {
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 12px 14px;
    background: #fafbff;
}

.analytics-kpi-item span {
    color: #6b7280;
    font-size: 0.85em;
    display: block;
}

.analytics-kpi-item strong {
    display: block;
    margin-top: 2px;
    font-size: 1.1em;
}

.trend-list {
    display: grid;
    gap: 12px;
}

.trend-row {
    display: grid;
    grid-template-columns: 90px 1fr 150px;
    gap: 12px;
    align-items: center;
}

.trend-day strong {
    display: block;
    font-size: 0.95em;
}

.trend-day span {
    color: #6b7280;
    font-size: 0.8em;
    text-transform: capitalize;
}

.trend-bar-wrap {
    width: 100%;
    height: 10px;
    border-radius: 999px;
    background: #e9edf7;
    overflow: hidden;
}

.trend-bar {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%);
}

.trend-values strong {
    display: block;
    font-size: 0.95em;
}

.trend-values span {
    color: #6b7280;
    font-size: 0.8em;
}

/* ========================================
   RESPONSIVE - TABLET
   ======================================== */

@media (max-width: 768px) {
    .page-header {
        flex-direction: column;
        align-items: flex-start;
    }

    .page-header h1 {
        font-size: 1.5em;
    }

    .cards-container {
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 15px;
    }

    .card {
        flex-direction: column;
        text-align: center;
    }

    .form-row {
        grid-template-columns: 1fr;
    }

    .filters-form {
        flex-direction: column;
    }

    .filter-group {
        min-width: 100%;
    }

    .table{
        font-size: 0.9em;
    }

    .table th, .table td {
        padding: 8px 10px;
    }

    .actions-cell {
        flex-direction: column;
    }

    .navbar-menu {
        display: none;
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background-color: var(--primary);
        width: 100%;
        flex-direction: column;
        align-items: stretch;
        border-top: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 10px 24px rgba(0, 0, 0, 0.2);
        max-height: calc(100vh - 64px);
        overflow-y: auto;
        z-index: 300;
    }

    .navbar-menu.active {
        display: flex;
    }

    .menu-toggle {
        display: inline-flex;
    }

    .nav-link {
        padding: 12px 20px;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }

    .header-actions {
        width: 100%;
    }

    .grid-container {
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    }

    .nav-dropdown-user {
        margin-left: 0;
    }

    .nav-dropdown-toggle {
        padding: 13px 20px;
    }

    .nav-sublink {
        padding: 11px 30px;
    }

    .analytics-grid {
        grid-template-columns: 1fr;
    }

    .chart-container {
        height: 260px;
    }

    .performance-chart-container {
        min-height: 220px;
        height: auto;
    }

    .trend-row {
        grid-template-columns: 1fr;
        gap: 6px;
    }

    .dashboard-filter-form {
        width: 100%;
    }

    .dashboard-filter-select {
        width: 100%;
    }

    .dashboard-filter-button {
        width: 100%;
    }

    .form-actions .btn,
    .form-actions .btn-small {
        width: 100%;
    }

    .alert {
        align-items: flex-start;
        gap: 8px;
    }

    .alert .close-alert {
        margin-left: auto;
    }

    /* Compatibilidade mobile para templates legados com estilo inline */
    .container [style*="grid-template-columns: 1fr 1fr"] {
        grid-template-columns: 1fr !important;
    }

    .container [style*="display: flex"][style*="justify-content: space-between"] {
        flex-wrap: wrap;
        gap: 10px !important;
    }

    .container [style*="display: flex"][style*="gap: 10px"] {
        flex-wrap: wrap;
    }

    .container [style*="max-width: 600px"],
    .container [style*="max-width: 700px"],
    .container [style*="max-width: 1000px"],
    .container [style*="max-width: 500px"],
    .container [style*="max-width: 1100px"] {
        width: 100%;
        margin: 20px auto !important;
    }

    .container [style*="grid-template-columns: repeat(auto-fit, minmax(260px, 1fr))"] {
        grid-template-columns: 1fr !important;
    }
}

/* ========================================
   RESPONSIVE - MOBILE
   ======================================== */

@media (max-width: 480px) {
    .main-content {
        padding: 10px;
    }

    .page-header h1 {
        font-size: 1.3em;
    }

    .page-header .header-actions {
        width: 100%;
        flex-direction: column;
    }

    .page-header .header-actions a {
        width: 100%;
    }

    .cards-container {
        grid-template-columns: 1fr;
        gap: 10px;
    }

    .card-value {
        font-size: 1.5em;
    }

    .form-container {
        padding: 15px;
    }

    .action-buttons {
        flex-direction: column;
    }

    .action-buttons a {
        width: 100%;
    }

    .btn, .btn-small {
        width: 100%;
        text-align: center;
    }

    .table-responsive {
        overflow-x: auto;
    }

    .table-responsive .table {
        min-width: 620px;
        font-size: 0.86rem;
    }

    .table:has(td[data-label]) {
        min-width: 0;
        display: block;
        overflow: visible;
    }

    .table:has(td[data-label]) thead {
        display: none;
    }

    .table:has(td[data-label]) tbody,
    .table:has(td[data-label]) tr,
    .table:has(td[data-label]) td {
        display: block;
        width: 100%;
    }

    .table:has(td[data-label]) tbody tr {
        margin-bottom: 15px;
        border: 1px solid var(--border);
        border-radius: 4px;
        overflow: hidden;
    }

    .table:has(td[data-label]) td {
        border: none;
        padding: 10px;
        text-align: right;
        position: relative;
        padding-left: 50%;
    }

    .table:has(td[data-label]) td:before {
        content: attr(data-label);
        position: absolute;
        left: 10px;
        font-weight: bold;
        color: var(--primary);
    }

    .filters-form {
        flex-direction: column;
    }

    .section {
        padding: 15px;
    }

    .chart-container {
        height: 220px;
    }

    .performance-chart-container {
        min-height: 200px;
        height: auto;
        margin-bottom: 10px;
    }

    .grid-container {
        grid-template-columns: 1fr;
    }

    .info-cards-row {
        grid-template-columns: 1fr;
    }

    .error-code {
        font-size: 3em;
    }

    .error-container h1 {
        font-size: 1.5em;
    }

    /* Colapsa ações inline em coluna em telas pequenas */
    .container [style*="display: flex"][style*="gap: 10px"] > * {
        width: 100% !important;
        flex: 1 1 100% !important;
    }

    .container [style*="display:flex"][style*="gap:5px"] {
        flex-wrap: wrap;
    }

    .container [style*="display:flex"][style*="gap:5px"] > * {
        width: 100% !important;
    }
}

/* ========================================
   BOOTSTRAP 5 + PADRAO VISUAL
   ======================================== */

.app-body {
    min-height: 100%;
    background:
        radial-gradient(circle at 0% 0%, rgba(15, 118, 110, 0.08), transparent 45%),
        radial-gradient(circle at 100% 20%, rgba(14, 165, 164, 0.12), transparent 42%),
        #f1f5f9;
}

.main-content {
    padding: 24px 0;
}

.content-shell {
    max-width: 1320px;
}

.page-container {
    padding-left: 0;
    padding-right: 0;
}

.footer {
    margin-top: auto;
    background: #0f172a;
    border-top: 1px solid rgba(255, 255, 255, 0.12);
}

.footer-inner {
    display: flex;
    justify-content: center;
}

.footer p {
    margin: 0;
}

.app-navbar {
    background: linear-gradient(90deg, #0f766e 0%, #155e75 100%);
    box-shadow: 0 8px 18px rgba(15, 23, 42, 0.2);
    position: sticky;
    top: 0;
    z-index: 1030;
}

.navbar-container {
    gap: 14px;
    min-height: 68px;
}

.brand-logo {
    width: auto;
    height: 34px;
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.18);
    padding: 2px;
}

.brand-name {
    font-size: 1.1rem;
    font-weight: 700;
    letter-spacing: 0.2px;
}

.brand-link:hover {
    text-decoration: none;
    opacity: 0.95;
}

.menu-toggle {
    border: 1px solid rgba(255, 255, 255, 0.45);
}

.menu-toggle .navbar-toggler-icon {
    background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 30 30'%3e%3cpath stroke='rgba%28255,255,255,0.95%29' stroke-linecap='round' stroke-miterlimit='10' stroke-width='2' d='M4 7h22M4 15h22M4 23h22'/%3e%3c/svg%3e");
}

.navbar-menu {
    flex: 1;
    justify-content: flex-end;
}

.nav-link,
.nav-dropdown-toggle {
    border-radius: 8px;
}

.nav-submenu {
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.08);
}

.card,
.section,
.filters-section,
.form-container,
.table {
    border: 1px solid var(--border);
}

.card,
.section,
.filters-section,
.form-container {
    border-radius: 12px;
}

.card,
.section,
.filters-section {
    background: #ffffff;
}

.card {
    padding: 0;
}

.card-header {
    padding: 0.9rem 1rem;
    border-bottom: 1px solid var(--border);
    background: #f8fafc;
    font-weight: 700;
}

.card-body {
    padding: 1rem;
}

.table {
    border-radius: 10px;
}

.table thead {
    background: #0f172a;
}

.btn,
.btn-small {
    border-radius: 8px;
    font-weight: 600;
}

.form-control,
.form-select,
.input-text,
.input-select,
.input-textarea,
.input-search {
    border-radius: 8px;
    border-color: #cdd6dd;
    min-height: 42px;
}

.form-control:focus,
.form-select:focus,
.input-text:focus,
.input-select:focus,
.input-textarea:focus,
.input-search:focus {
    border-color: var(--primary);
    box-shadow: 0 0 0 0.2rem rgba(15, 118, 110, 0.16);
}

.alert {
    border-radius: 10px;
}

@media (max-width: 768px) {
    .content-shell {
        padding-left: 12px;
        padding-right: 12px;
    }

    .page-container {
        padding-left: 0;
        padding-right: 0;
    }
}

.inline-form {
    display: inline;
}

canvas {
    width: 100% !important;
    max-width: 100%;
}

@media (max-width: 640px) {
    .receipt-items thead {
        display: none;
    }

    .receipt-items,
    .receipt-items tbody,
    .receipt-items tr,
    .receipt-items td {
        display: block;
        width: 100%;
    }

    .receipt-items tr {
        border-bottom: 1px solid var(--border);
        margin-bottom: 10px;
        padding-bottom: 8px;
    }

    .receipt-items td[data-label] {
        text-align: right;
        padding-left: 48%;
        position: relative;
    }

    .receipt-items td[data-label]::before {
        content: attr(data-label);
        position: absolute;
        left: 6px;
        font-weight: 700;
        color: var(--primary);
    }
}
```

---

### Arquivo: `static\js\csrf.js`

```js
(function () {
    function readMetaToken() {
        var meta = document.querySelector('meta[name="csrf-token"]');
        return meta ? (meta.getAttribute('content') || '') : '';
    }

    function getCsrfToken() {
        if (window.__CSRF_TOKEN__) {
            return window.__CSRF_TOKEN__;
        }
        var token = readMetaToken();
        if (token) {
            window.__CSRF_TOKEN__ = token;
        }
        return token;
    }

    function isUnsafeMethod(method) {
        var m = (method || 'GET').toUpperCase();
        return ['POST', 'PUT', 'PATCH', 'DELETE'].indexOf(m) >= 0;
    }

    function injectCsrfIntoForms() {
        var token = getCsrfToken();
        if (!token) return;

        var forms = document.querySelectorAll('form');
        forms.forEach(function (form) {
            var method = (form.getAttribute('method') || 'GET').toUpperCase();
            if (!isUnsafeMethod(method)) return;
            if (form.querySelector('input[name="csrf_token"]')) return;

            var input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'csrf_token';
            input.value = token;
            form.appendChild(input);
        });
    }

    function patchFetchWithCsrf() {
        if (!window.fetch) return;
        if (window.__fetch_csrf_patched__) return;
        window.__fetch_csrf_patched__ = true;

        var nativeFetch = window.fetch.bind(window);
        window.fetch = function (input, init) {
            init = init || {};
            var method = (init.method || 'GET').toUpperCase();
            if (!isUnsafeMethod(method)) {
                return nativeFetch(input, init);
            }

            var token = getCsrfToken();
            if (!token) {
                return nativeFetch(input, init);
            }

            var headers = new Headers(init.headers || {});
            if (!headers.has('X-CSRF-Token')) {
                headers.set('X-CSRF-Token', token);
            }
            init.headers = headers;
            return nativeFetch(input, init);
        };
    }

    document.addEventListener('DOMContentLoaded', function () {
        window.getCsrfToken = getCsrfToken;
        injectCsrfIntoForms();
        patchFetchWithCsrf();
    });
})();
```

---

### Arquivo: `static\js\main.js`

```js
﻿document.addEventListener('DOMContentLoaded', function () {
    const menuToggle = document.getElementById('menuToggle');
    const navbarMenu = document.getElementById('navbarMenu');
    const dropdownToggles = document.querySelectorAll('.nav-dropdown-toggle');
    const mobileBreakpoint = window.matchMedia('(max-width: 768px)');

    if (menuToggle && navbarMenu) {
        const closeDropdowns = function () {
            document.querySelectorAll('.nav-dropdown.open').forEach(function (drop) {
                drop.classList.remove('open');
            });
        };

        const setMenuState = function (isOpen) {
            navbarMenu.classList.toggle('active', isOpen);
            menuToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
            menuToggle.setAttribute('aria-label', isOpen ? 'Fechar menu' : 'Abrir menu');
        };

        menuToggle.addEventListener('click', function () {
            const isOpen = !navbarMenu.classList.contains('active');
            setMenuState(isOpen);
        });

        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(function (link) {
            link.addEventListener('click', function () {
                setMenuState(false);
                closeDropdowns();
            });
        });

        document.addEventListener('keydown', function (event) {
            if (event.key !== 'Escape') return;
            setMenuState(false);
            closeDropdowns();
        });

        document.addEventListener('click', function (event) {
            if (!mobileBreakpoint.matches) return;
            const clickedInsideMenu = navbarMenu.contains(event.target);
            const clickedToggle = menuToggle.contains(event.target);
            if (!clickedInsideMenu && !clickedToggle) {
                setMenuState(false);
                closeDropdowns();
            }
        });

        const handleBreakpoint = function (event) {
            if (event.matches) return;
            setMenuState(false);
            closeDropdowns();
        };

        if (typeof mobileBreakpoint.addEventListener === 'function') {
            mobileBreakpoint.addEventListener('change', handleBreakpoint);
        } else {
            mobileBreakpoint.addListener(handleBreakpoint);
        }
    }

    dropdownToggles.forEach(function (toggle) {
        toggle.addEventListener('click', function () {
            const parentDropdown = this.closest('.nav-dropdown');
            document.querySelectorAll('.nav-dropdown.open').forEach(function (drop) {
                if (drop !== parentDropdown) {
                    drop.classList.remove('open');
                }
            });
            parentDropdown.classList.toggle('open');
        });
    });

    const closeButtons = document.querySelectorAll('.close-alert');
    closeButtons.forEach(function (btn) {
        btn.addEventListener('click', function () {
            this.parentElement.style.display = 'none';
        });
    });

    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            alert.style.display = 'none';
        }, 5000);
    });

    initConfirmActionModal();
    initBarcodeScannerButtons();
    initFormFieldTooltips();
    initCollapsiblePanels();
});

function formatarMoeda(valor) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(valor);
}

function formatarData(data) {
    return new Intl.DateTimeFormat('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    }).format(new Date(data));
}

function validarFormulario(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;

    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    let valido = true;

    inputs.forEach(function (input) {
        if (!input.value.trim()) {
            input.style.borderColor = '#D9534F';
            valido = false;
        } else {
            input.style.borderColor = '';
        }
    });

    return valido;
}

function initConfirmActionModal() {
    const modalEl = document.getElementById('confirmActionModal');
    const messageEl = document.getElementById('confirmActionModalMessage');
    const okBtn = document.getElementById('confirmActionModalOk');
    if (!modalEl || !messageEl || !okBtn || typeof bootstrap === 'undefined') return;

    const modal = new bootstrap.Modal(modalEl, { backdrop: 'static', keyboard: true });
    let pendingForm = null;

    document.addEventListener('submit', function (event) {
        const form = event.target;
        if (!(form instanceof HTMLFormElement)) return;
        const confirmMessage = form.getAttribute('data-confirm-message');
        if (!confirmMessage) return;
        if (form.dataset.confirmedSubmit === '1') {
            delete form.dataset.confirmedSubmit;
            return;
        }
        event.preventDefault();
        pendingForm = form;
        messageEl.textContent = confirmMessage;
        modal.show();
    });

    okBtn.addEventListener('click', function () {
        if (!pendingForm) {
            modal.hide();
            return;
        }
        pendingForm.dataset.confirmedSubmit = '1';
        const form = pendingForm;
        pendingForm = null;
        modal.hide();
        if (typeof form.requestSubmit === 'function') {
            form.requestSubmit();
        } else {
            form.submit();
        }
    });

    modalEl.addEventListener('hidden.bs.modal', function () {
        pendingForm = null;
    });
}

function initBarcodeScannerButtons() {
    const buttons = document.querySelectorAll('.js-open-barcode-scanner');
    if (!buttons.length) return;

    let modalState = null;

    buttons.forEach(function (button) {
        button.addEventListener('click', async function () {
            const targetId = this.getAttribute('data-barcode-target');
            const targetInput = document.getElementById(targetId);
            const mode = (this.getAttribute('data-barcode-mode') || 'single').toLowerCase();
            const continuous = mode === 'continuous' || mode === 'sequence';

            if (!targetInput) {
                alert('Campo de codigo nao encontrado.');
                return;
            }

            if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
                alert('Seu navegador nao suporta acesso a camera.');
                return;
            }

            if (typeof window.BarcodeDetector === 'undefined') {
                alert('Leitura por camera indisponivel neste navegador. Use Chrome/Edge atualizados.');
                return;
            }

            try {
                if (modalState && typeof modalState.close === 'function') {
                    modalState.close();
                }

                const detector = new window.BarcodeDetector({
                    formats: ['ean_13', 'ean_8', 'code_128', 'upc_a', 'upc_e', 'code_39', 'codabar']
                });
                modalState = await openBarcodeScannerModal(targetInput, detector, {
                    continuous: continuous
                });
            } catch (error) {
                console.error('Erro ao iniciar leitura de codigo:', error);
                alert('Nao foi possivel iniciar a leitura. Verifique permissoes da camera.');
            }
        });
    });

    window.addEventListener('beforeunload', function () {
        if (modalState && typeof modalState.close === 'function') {
            modalState.close();
        }
    });
}

function initFormFieldTooltips() {
    if (typeof bootstrap === 'undefined' || typeof bootstrap.Tooltip === 'undefined') return;

    const controls = document.querySelectorAll('form input, form select, form textarea');
    controls.forEach(function (field) {
        if (!field || field.dataset.tooltipReady === '1') return;
        if (field.type === 'hidden') return;
        if (field.disabled) return;

        const explicit = (field.getAttribute('data-tooltip') || '').trim();
        const label = getFieldLabelText(field);
        const placeholder = (field.getAttribute('placeholder') || '').trim();
        const requiredText = field.required ? 'Campo obrigatorio.' : '';

        let tooltipText = explicit;
        if (!tooltipText) {
            const parts = [];
            if (label) parts.push(label + '.');
            if (placeholder) parts.push('Exemplo: ' + placeholder + '.');
            if (requiredText) parts.push(requiredText);
            tooltipText = parts.join(' ').trim();
        }

        if (!tooltipText) return;

        field.setAttribute('data-bs-toggle', 'tooltip');
        field.setAttribute('data-bs-placement', 'top');
        field.setAttribute('data-bs-trigger', 'hover focus');
        field.setAttribute('title', tooltipText);
        field.dataset.tooltipReady = '1';
        bootstrap.Tooltip.getOrCreateInstance(field);
    });
}

function getFieldLabelText(field) {
    if (!field || !field.id) return '';
    const label = document.querySelector('label[for="' + field.id + '"]');
    if (!label) return '';
    return (label.textContent || '').replace(/\s+/g, ' ').replace(/\*/g, '').trim();
}

async function openBarcodeScannerModal(targetInput, detector, options) {
    options = options || {};
    const continuous = Boolean(options.continuous);
    const scanIntervalMs = continuous ? 120 : 250;
    const duplicateCooldownMs = continuous ? 350 : 0;
    const lastReadByCode = {};

    const modal = document.createElement('div');
    modal.className = 'barcode-scanner-modal active';
    modal.innerHTML = [
        '<div class="barcode-scanner-content">',
        '  <div class="barcode-scanner-header">',
        '    <span class="barcode-scanner-title">Leitura de Codigo de Barras</span>',
        '    <button type="button" class="barcode-scanner-close" aria-label="Fechar">&times;</button>',
        '  </div>',
        '  <div class="barcode-scanner-body">',
        '    <video class="barcode-scanner-video" autoplay playsinline muted></video>',
        continuous
            ? '    <p class="barcode-scanner-help">Modo continuo ativo: aproxime e afaste os produtos para leitura em sequencia.</p>'
            : '    <p class="barcode-scanner-help">Aponte a camera para o codigo de barras.</p>',
        '  </div>',
        '</div>'
    ].join('');

    document.body.appendChild(modal);

    const video = modal.querySelector('.barcode-scanner-video');
    const closeBtn = modal.querySelector('.barcode-scanner-close');
    let running = true;
    let stream = null;

    const close = function () {
        running = false;
        if (stream) {
            stream.getTracks().forEach(function (track) {
                track.stop();
            });
        }
        modal.remove();
    };

    closeBtn.addEventListener('click', close);
    modal.addEventListener('click', function (event) {
        if (event.target === modal) {
            close();
        }
    });

    stream = await navigator.mediaDevices.getUserMedia({
        video: {
            facingMode: { ideal: 'environment' },
            width: { ideal: 1280 },
            height: { ideal: 720 }
        },
        audio: false
    });

    video.srcObject = stream;

    const scanLoop = async function () {
        if (!running) return;

        try {
            const barcodes = await detector.detect(video);
            if (barcodes && barcodes.length > 0) {
                let rawValue = '';
                for (let i = 0; i < barcodes.length; i++) {
                    const candidate = (barcodes[i].rawValue || '').trim();
                    if (candidate) {
                        rawValue = candidate;
                        break;
                    }
                }

                if (rawValue) {
                    const now = Date.now();
                    const lastReadAt = lastReadByCode[rawValue] || 0;
                    if (duplicateCooldownMs > 0 && (now - lastReadAt) < duplicateCooldownMs) {
                        setTimeout(scanLoop, scanIntervalMs);
                        return;
                    }
                    lastReadByCode[rawValue] = now;

                    targetInput.value = rawValue;
                    targetInput.dispatchEvent(new Event('input', { bubbles: true }));
                    targetInput.dispatchEvent(new Event('change', { bubbles: true }));
                    targetInput.dispatchEvent(new CustomEvent('barcode:detected', {
                        bubbles: true,
                        detail: { value: rawValue, continuous: continuous }
                    }));

                    if (continuous && navigator.vibrate) {
                        navigator.vibrate(30);
                    }

                    if (!continuous) {
                        close();
                        return;
                    }
                }
            }
        } catch (error) {
            // Ignora falhas pontuais de detecção por frame.
        }

        setTimeout(scanLoop, scanIntervalMs);
    };

    scanLoop();

    return { close: close };
}

function initCollapsiblePanels() {
    const panels = [];

    document.querySelectorAll('.pdv-panel').forEach(function (panel) {
        const header = panel.querySelector(':scope > .pdv-panel-head') || panel.querySelector('.pdv-panel-head');
        const body = panel.querySelector(':scope > .pdv-panel-body') || panel.querySelector('.pdv-panel-body');
        if (!header || !body) return;
        panels.push({ panel: panel, header: header, contentNodes: [body], idHint: 'pdv-' + header.textContent.trim() });
    });

    document.querySelectorAll('.card').forEach(function (panel) {
        const header = panel.querySelector(':scope > .card-header') || panel.querySelector('.card-header');
        if (!header) return;
        const body = panel.querySelector(':scope > .card-body') || panel.querySelector('.card-body');
        const contentNodes = body ? [body] : Array.from(panel.children).filter(function (child) { return child !== header; });
        if (!contentNodes.length) return;
        panels.push({ panel: panel, header: header, contentNodes: contentNodes, idHint: 'card-' + header.textContent.trim() });
    });

    document.querySelectorAll('.section').forEach(function (panel) {
        if (panel.closest('.card')) return;
        const title = panel.querySelector(':scope > h1, :scope > h2, :scope > h3, :scope > h4');
        if (!title) return;
        const contentNodes = Array.from(panel.children).filter(function (child) { return child !== title; });
        if (!contentNodes.length) return;

        let headerWrap = panel.querySelector(':scope > .panel-toggle-head');
        if (!headerWrap) {
            headerWrap = document.createElement('div');
            headerWrap.className = 'panel-toggle-head';
            panel.insertBefore(headerWrap, title);
            headerWrap.appendChild(title);
        }

        panels.push({ panel: panel, header: headerWrap, contentNodes: contentNodes, idHint: 'section-' + title.textContent.trim() });
    });

    const seen = new WeakSet();
    panels.forEach(function (item, index) {
        if (!item.panel || !item.header || seen.has(item.panel)) return;
        seen.add(item.panel);

        item.panel.classList.add('panel-collapsible');
        item.contentNodes.forEach(function (node) {
            if (node && node.classList) node.classList.add('panel-collapsible-content');
        });

        let btn = item.header.querySelector('.panel-toggle-btn');
        if (!btn) {
            btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'btn btn-sm btn-outline-secondary panel-toggle-btn';
            item.header.appendChild(btn);
        }

        const storageKey = 'panel-collapse:' + window.location.pathname + ':' + slugifyPanelId(item.idHint || String(index));
        const stored = window.localStorage ? localStorage.getItem(storageKey) : null;
        let collapsed = stored === '1';

        const applyState = function () {
            item.panel.classList.toggle('panel-collapsed', collapsed);
            btn.setAttribute('aria-expanded', collapsed ? 'false' : 'true');
            btn.textContent = collapsed ? 'Expandir' : 'Minimizar';
        };

        btn.addEventListener('click', function () {
            collapsed = !collapsed;
            if (window.localStorage) {
                localStorage.setItem(storageKey, collapsed ? '1' : '0');
            }
            applyState();
        });

        applyState();
    });
}

function slugifyPanelId(value) {
    return (value || 'panel')
        .toString()
        .toLowerCase()
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')
        .replace(/[^a-z0-9]+/g, '-')
        .replace(/(^-|-$)/g, '')
        .slice(0, 80) || 'panel';
}
```

---

### Arquivo: `static\js\pages\dashboard_analytics.js`

```js
(function () {
    function moeda(v) {
        return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(v || 0);
    }

    function getFiltro() {
        var ini = document.getElementById('data_inicial');
        var fim = document.getElementById('data_final');
        return {
            data_inicial: ini ? ini.value : '',
            data_final: fim ? fim.value : ''
        };
    }

    function buildUrl() {
        var filtro = getFiltro();
        var params = new URLSearchParams();
        if (filtro.data_inicial) params.set('data_inicial', filtro.data_inicial);
        if (filtro.data_final) params.set('data_final', filtro.data_final);
        return '/api/dashboard/analytics?' + params.toString();
    }

    function isMobileViewport() {
        return window.matchMedia('(max-width: 768px)').matches;
    }

    function buildChartOptions(type, mobile) {
        var options = {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: mobile ? 'bottom' : 'top',
                    labels: {
                        boxWidth: mobile ? 10 : 14,
                        usePointStyle: mobile,
                        font: {
                            size: mobile ? 10 : 12
                        }
                    }
                }
            }
        };

        if (type !== 'doughnut') {
            options.scales = {
                x: {
                    ticks: {
                        autoSkip: true,
                        maxTicksLimit: mobile ? 6 : 12,
                        maxRotation: mobile ? 0 : 40,
                        minRotation: 0,
                        font: {
                            size: mobile ? 10 : 11
                        }
                    }
                },
                y: {
                    ticks: {
                        font: {
                            size: mobile ? 10 : 11
                        }
                    }
                }
            };
        }

        return options;
    }

    var charts = {
        faturamento: null,
        status: null,
        pagamento: null,
        topProdutos: null,
        desempenhoGarcons: null,
        desempenhoCaixas: null
    };
    var analyticsData = null;
    var lastMobileState = isMobileViewport();

    function destroyCharts() {
        Object.keys(charts).forEach(function (k) {
            if (charts[k]) {
                charts[k].destroy();
                charts[k] = null;
            }
        });
    }

    function atualizarKpis(data) {
        var map = {
            kpiFaturamentoPeriodo: moeda(data.faturamento_periodo),
            kpiTicketMedio: moeda(data.ticket_medio_periodo),
            kpiFaturamentoHoje: moeda(data.faturamento_hoje),
            kpiPedidosAbertos: String(data.pedidos_abertos || 0),
            kpiPedidosCancelados: String(data.pedidos_cancelados_periodo || 0)
        };

        Object.keys(map).forEach(function (id) {
            var el = document.getElementById(id);
            if (el) el.textContent = map[id];
        });

        var metaPedidos = document.getElementById('kpiPedidosPeriodo');
        if (metaPedidos) {
            metaPedidos.textContent = String(data.pedidos_periodo_total || 0) + ' pedidos fechados';
        }
    }

    function renderCharts(data) {
        analyticsData = data;
        destroyCharts();
        var mobile = isMobileViewport();

        var ctxFat = document.getElementById('chartFaturamento');
        if (ctxFat) {
            var fatOptions = buildChartOptions('line', mobile);
            fatOptions.plugins.legend.display = false;
            charts.faturamento = new Chart(ctxFat, {
                type: 'line',
                data: {
                    labels: (data.vendas_periodo || []).map(function (d) { return d.data_curta; }),
                    datasets: [{
                        label: 'Faturamento',
                        data: (data.vendas_periodo || []).map(function (d) { return d.faturamento; }),
                        borderColor: '#0f766e',
                        backgroundColor: 'rgba(15, 118, 110, 0.16)',
                        tension: 0.25,
                        pointRadius: mobile ? 0 : 2,
                        pointHoverRadius: mobile ? 3 : 4,
                        fill: true
                    }]
                },
                options: fatOptions
            });
        }

        var ctxStatus = document.getElementById('chartStatus');
        if (ctxStatus) {
            var statusOptions = buildChartOptions('doughnut', mobile);
            charts.status = new Chart(ctxStatus, {
                type: 'doughnut',
                data: {
                    labels: (data.pedidos_por_status || []).map(function (s) { return s.label; }),
                    datasets: [{
                        data: (data.pedidos_por_status || []).map(function (s) { return s.quantidade; }),
                        backgroundColor: ['#0f766e', '#f59e0b', '#2563eb', '#16a34a', '#dc2626']
                    }]
                },
                options: statusOptions
            });
        }

        var ctxPag = document.getElementById('chartPagamento');
        if (ctxPag) {
            var pagOptions = buildChartOptions('bar', mobile);
            pagOptions.plugins.legend.display = false;
            charts.pagamento = new Chart(ctxPag, {
                type: 'bar',
                data: {
                    labels: (data.metodos_pagamento || []).map(function (m) { return m.metodo; }),
                    datasets: [{
                        label: 'Pedidos',
                        data: (data.metodos_pagamento || []).map(function (m) { return m.quantidade; }),
                        backgroundColor: '#155e75'
                    }]
                },
                options: pagOptions
            });
        }

        var ctxTop = document.getElementById('chartTopProdutos');
        if (ctxTop) {
            var topOptions = buildChartOptions('bar', mobile);
            topOptions.plugins.legend.display = false;
            if (mobile) {
                topOptions.indexAxis = 'y';
                topOptions.scales.y.ticks.autoSkip = false;
            }
            charts.topProdutos = new Chart(ctxTop, {
                type: 'bar',
                data: {
                    labels: (data.top_produtos_vendidos || []).map(function (p) { return p.nome; }),
                    datasets: [{
                        label: 'Receita (R$)',
                        data: (data.top_produtos_vendidos || []).map(function (p) { return p.receita; }),
                        backgroundColor: '#0ea5a4'
                    }]
                },
                options: topOptions
            });
        }

        var ctxGarcons = document.getElementById('chartDesempenhoGarcons');
        if (ctxGarcons) {
            var chartWrapperGarcons = ctxGarcons.closest('.performance-chart-container');
            var garconsData = data.desempenho_garcons || [];
            if (chartWrapperGarcons) {
                chartWrapperGarcons.style.height = mobile
                    ? Math.max(220, garconsData.length * 56) + 'px'
                    : '300px';
            }

            var garconsOptions = buildChartOptions('bar', mobile);
            garconsOptions.indexAxis = 'y';
            garconsOptions.plugins.legend.display = false;
            garconsOptions.scales.x.ticks.callback = function (value) {
                return moeda(value);
            };
            garconsOptions.scales.y.ticks.autoSkip = false;

            charts.desempenhoGarcons = new Chart(ctxGarcons, {
                type: 'bar',
                data: {
                    labels: garconsData.map(function (item) { return item.nome; }),
                    datasets: [{
                        label: 'Faturamento (R$)',
                        data: garconsData.map(function (item) { return item.faturamento; }),
                        backgroundColor: '#0f766e',
                        borderRadius: 6,
                        barThickness: mobile ? 14 : 18
                    }]
                },
                options: garconsOptions
            });
        }

        var ctxCaixas = document.getElementById('chartDesempenhoCaixas');
        if (ctxCaixas) {
            var chartWrapperCaixas = ctxCaixas.closest('.performance-chart-container');
            var caixasData = data.desempenho_caixas || [];
            if (chartWrapperCaixas) {
                chartWrapperCaixas.style.height = mobile
                    ? Math.max(220, caixasData.length * 56) + 'px'
                    : '300px';
            }

            var caixasOptions = buildChartOptions('bar', mobile);
            caixasOptions.indexAxis = 'y';
            caixasOptions.plugins.legend.display = false;
            caixasOptions.scales.x.ticks.callback = function (value) {
                return moeda(value);
            };
            caixasOptions.scales.y.ticks.autoSkip = false;

            charts.desempenhoCaixas = new Chart(ctxCaixas, {
                type: 'bar',
                data: {
                    labels: caixasData.map(function (item) { return item.nome; }),
                    datasets: [{
                        label: 'Faturamento (R$)',
                        data: caixasData.map(function (item) { return item.faturamento; }),
                        backgroundColor: '#155e75',
                        borderRadius: 6,
                        barThickness: mobile ? 14 : 18
                    }]
                },
                options: caixasOptions
            });
        }
    }

    function carregarAnalytics() {
        fetch(buildUrl())
            .then(function (r) { return r.json(); })
            .then(function (res) {
                if (!res || !res.success || !res.data) return;
                atualizarKpis(res.data);
                renderCharts(res.data);
            })
            .catch(function (err) {
                console.error('Falha ao carregar analytics do dashboard', err);
            });
    }

    document.addEventListener('DOMContentLoaded', function () {
        carregarAnalytics();
        var form = document.querySelector('.dashboard-filter-form');
        if (form) {
            form.addEventListener('submit', function (event) {
                event.preventDefault();
                var filtro = getFiltro();
                var params = new URLSearchParams();
                if (filtro.data_inicial) params.set('data_inicial', filtro.data_inicial);
                if (filtro.data_final) params.set('data_final', filtro.data_final);
                var newUrl = window.location.pathname + '?' + params.toString();
                history.replaceState({}, '', newUrl);
                carregarAnalytics();
            });
        }

        window.addEventListener('resize', function () {
            var mobileNow = isMobileViewport();
            if (mobileNow === lastMobileState) return;
            lastMobileState = mobileNow;
            if (analyticsData) renderCharts(analyticsData);
        });
    });
})();
```

---

### Arquivo: `static\js\pages\estoque_analytics.js`

```js
(function () {
    var chartMov = null;
    var chartCategoria = null;
    var analyticsData = null;
    var lastMobileState = isMobileViewport();

    function isMobileViewport() {
        return window.matchMedia('(max-width: 768px)').matches;
    }

    function buildChartOptions(type, mobile) {
        var options = {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: mobile ? 'bottom' : 'top',
                    labels: {
                        boxWidth: mobile ? 10 : 14,
                        usePointStyle: mobile,
                        font: {
                            size: mobile ? 10 : 12
                        }
                    }
                }
            }
        };

        if (type !== 'doughnut') {
            options.scales = {
                x: {
                    ticks: {
                        autoSkip: true,
                        maxTicksLimit: mobile ? 6 : 12,
                        maxRotation: mobile ? 0 : 35,
                        minRotation: 0,
                        font: {
                            size: mobile ? 10 : 11
                        }
                    }
                },
                y: {
                    ticks: {
                        font: {
                            size: mobile ? 10 : 11
                        }
                    }
                }
            };
        }

        return options;
    }

    function carregar(periodo) {
        fetch('/api/estoque/analytics?periodo=' + encodeURIComponent(periodo))
            .then(function (r) { return r.json(); })
            .then(function (res) {
                if (!res || !res.success || !res.data) return;
                renderizar(res.data);
            })
            .catch(function (err) {
                console.error('Erro ao carregar analytics de estoque', err);
            });
    }

    function renderizar(data) {
        analyticsData = data;
        if (chartMov) chartMov.destroy();
        if (chartCategoria) chartCategoria.destroy();
        var mobile = isMobileViewport();

        var c1 = document.getElementById('chartMovimentacoesEstoque');
        if (c1) {
            var movOptions = buildChartOptions('line', mobile);
            chartMov = new Chart(c1, {
                type: 'line',
                data: {
                    labels: (data.movimentacao_diaria || []).map(function (x) { return x.dia.slice(5); }),
                    datasets: [
                        { label: 'Entradas', data: (data.movimentacao_diaria || []).map(function (x) { return x.entradas; }), borderColor: '#16a34a', backgroundColor: 'rgba(22,163,74,0.15)', fill: true, tension: 0.2, pointRadius: mobile ? 0 : 2, pointHoverRadius: mobile ? 3 : 4 },
                        { label: 'Saidas', data: (data.movimentacao_diaria || []).map(function (x) { return x.saidas; }), borderColor: '#dc2626', backgroundColor: 'rgba(220,38,38,0.12)', fill: true, tension: 0.2, pointRadius: mobile ? 0 : 2, pointHoverRadius: mobile ? 3 : 4 }
                    ]
                },
                options: movOptions
            });
        }

        var c2 = document.getElementById('chartValorCategoriaEstoque');
        if (c2) {
            var categoriaOptions = buildChartOptions('bar', mobile);
            categoriaOptions.plugins.legend.display = false;
            if (mobile) {
                categoriaOptions.indexAxis = 'y';
                categoriaOptions.scales.y.ticks.autoSkip = false;
            }
            chartCategoria = new Chart(c2, {
                type: 'bar',
                data: {
                    labels: (data.valor_por_categoria || []).map(function (x) { return x.categoria; }),
                    datasets: [{
                        label: 'Valor (R$)',
                        data: (data.valor_por_categoria || []).map(function (x) { return x.valor_total; }),
                        backgroundColor: '#0f766e'
                    }]
                },
                options: categoriaOptions
            });
        }
    }

    document.addEventListener('DOMContentLoaded', function () {
        var select = document.getElementById('estoquePeriodo');
        var periodo = select ? select.value : '30';
        carregar(periodo);
        if (select) {
            select.addEventListener('change', function () {
                carregar(select.value || '30');
            });
        }

        window.addEventListener('resize', function () {
            var mobileNow = isMobileViewport();
            if (mobileNow === lastMobileState) return;
            lastMobileState = mobileNow;
            if (analyticsData) renderizar(analyticsData);
        });
    });
})();
```

---

### Arquivo: `static\js\pages\rh_analytics.js`

```js
(function () {
    var chartPerfis = null;
    var chartAdmissoes = null;
    var analyticsData = null;
    var lastMobileState = isMobileViewport();

    function isMobileViewport() {
        return window.matchMedia('(max-width: 768px)').matches;
    }

    function buildChartOptions(type, mobile) {
        var options = {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: mobile ? 'bottom' : 'top',
                    labels: {
                        boxWidth: mobile ? 10 : 14,
                        usePointStyle: mobile,
                        font: {
                            size: mobile ? 10 : 12
                        }
                    }
                }
            }
        };

        if (type !== 'doughnut') {
            options.scales = {
                x: {
                    ticks: {
                        autoSkip: true,
                        maxTicksLimit: mobile ? 6 : 12,
                        maxRotation: mobile ? 0 : 35,
                        minRotation: 0,
                        font: {
                            size: mobile ? 10 : 11
                        }
                    }
                },
                y: {
                    ticks: {
                        font: {
                            size: mobile ? 10 : 11
                        }
                    }
                }
            };
        }

        return options;
    }

    function carregar(periodo) {
        fetch('/api/rh/analytics?periodo=' + encodeURIComponent(periodo))
            .then(function (r) { return r.json(); })
            .then(function (res) {
                if (!res || !res.success || !res.data) return;
                renderizar(res.data);
            })
            .catch(function (err) {
                console.error('Erro ao carregar analytics RH', err);
            });
    }

    function renderizar(data) {
        analyticsData = data;
        if (chartPerfis) chartPerfis.destroy();
        if (chartAdmissoes) chartAdmissoes.destroy();
        var mobile = isMobileViewport();

        var c1 = document.getElementById('chartRhPerfis');
        if (c1) {
            var perfisOptions = buildChartOptions('doughnut', mobile);
            chartPerfis = new Chart(c1, {
                type: 'doughnut',
                data: {
                    labels: (data.distribuicao_roles || []).map(function (x) { return (x.role || '').toUpperCase(); }),
                    datasets: [{
                        data: (data.distribuicao_roles || []).map(function (x) { return x.quantidade; }),
                        backgroundColor: ['#0f766e', '#2563eb', '#f59e0b', '#16a34a', '#dc2626']
                    }]
                },
                options: perfisOptions
            });
        }

        var c2 = document.getElementById('chartRhAdmissoes');
        if (c2) {
            var admissoesOptions = buildChartOptions('bar', mobile);
            admissoesOptions.plugins.legend.display = false;
            chartAdmissoes = new Chart(c2, {
                type: 'bar',
                data: {
                    labels: (data.admissoes_diarias || []).map(function (x) { return x.dia.slice(5); }),
                    datasets: [{
                        label: 'Admissoes',
                        data: (data.admissoes_diarias || []).map(function (x) { return x.quantidade; }),
                        backgroundColor: '#0ea5a4'
                    }]
                },
                options: admissoesOptions
            });
        }
    }

    document.addEventListener('DOMContentLoaded', function () {
        var select = document.getElementById('rhPeriodo');
        var periodo = select ? select.value : '30';
        carregar(periodo);
        if (select) {
            select.addEventListener('change', function () {
                carregar(select.value || '30');
            });
        }

        window.addEventListener('resize', function () {
            var mobileNow = isMobileViewport();
            if (mobileNow === lastMobileState) return;
            lastMobileState = mobileNow;
            if (analyticsData) renderizar(analyticsData);
        });
    });
})();
```

---

### Arquivo: `static\robots.txt`

```txt
# robots.txt - SystemLR
# https://systemlr.com

User-agent: *
Allow: /
Allow: /api/
Disallow: /admin/
Disallow: /private/


# Sitemaps
Sitemap: https://systemlr.com/sitemap.xml

# Crawl delay (para não sobrecarregar o servidor)
Crawl-delay: 1

# Allow major search engines
User-agent: Googlebot
Crawl-delay: 0

User-agent: Bingbot
Crawl-delay: 1
```

---

### Arquivo: `templates\api\docs.html`

```html
{% extends "base.html" %}

{% block title %}Documentacao da API{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Documentacao da API</h1>
    <p class="text-muted">Endpoints principais em JSON. Todos exigem CSRF/credenciais conforme configuracao.</p>
</div>

<div class="card">
    <div class="card-body">
        <h3>Pedidos</h3>
        <ul>
            <li><code>POST /api/pedidos/criar</code> – cria pedido rápido. Body: <code>{itens:[{produto_id, quantidade}]}</code>. Resposta: <code>{success, pedido_id}</code></li>
            <li><code>POST /api/pedidos/&lt;id&gt;/finalizar</code> – finaliza com pagamento. Body: <code>{metodo_pagamento, valor_recebido}</code>. Resposta: <code>{success, total}</code></li>
            <li><code>GET /api/pedidos/em-aberto</code> – lista pedidos abertos.</li>
            <li><code>GET /api/pedidos/&lt;id&gt;/detalhes-json</code> – detalhes completos do pedido.</li>
            <li><code>POST /api/pedidos/&lt;id&gt;/adicionar</code> – adiciona itens. Body: <code>{itens:[...]}</code>.</li>
        </ul>

        <h3>Estoque</h3>
        <ul>
            <li><code>GET /api/estoque/analytics</code> – métricas de estoque.</li>
            <li><code>POST /movimentacoes/nova</code> – movimentação manual (form-data); ver telas internas.</li>
        </ul>

        <h3>Dashboard / RH</h3>
        <ul>
            <li><code>GET /api/dashboard/analytics?inicio=YYYY-MM-DD&amp;fim=YYYY-MM-DD</code> – métricas de vendas.</li>
            <li><code>GET /api/rh/analytics</code> – indicadores de RH.</li>
        </ul>

        <p class="text-muted mt-3">Estrutura de resposta padrão: <code>{ success: bool, message: str, data?: any, code?: str }</code>.</p>
    </div>
</div>
{% endblock %}
```

---

### Arquivo: `templates\base.html`

```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="csrf-token" content="{{ csrf_token }}">
    <title>{% block title %}SystemLR - Gestao de Estoque{% endblock %}</title>
    <link rel="preconnect" href="https://cdn.jsdelivr.net">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/core/tokens.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/core/layout.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/core/tables.css') }}">
    {% block extra_css %}{% endblock %}
</head>
<body class="app-body">
    <header class="navbar app-navbar">
        <div class="container navbar-container">
            <a href="{{ url_for('boas_vindas') }}" class="navbar-brand brand-link d-flex align-items-center gap-2 me-2">
                {% if empresa_config and empresa_config.logo_path %}
                <img src="{{ url_for('static', filename=empresa_config.logo_path) }}" alt="Logo" class="brand-logo">
                {% endif %}
                <span class="brand-name">{{ empresa_config.nome_fantasia if empresa_config and empresa_config.nome_fantasia else 'SystemLR' }}</span>
            </a>

            <button class="menu-toggle navbar-toggler" id="menuToggle" type="button" aria-label="Abrir menu" aria-controls="navbarMenu" aria-expanded="false">
                <span class="navbar-toggler-icon"></span>
            </button>

            <nav class="navbar-menu" id="navbarMenu">
                {% if funcionario_logado %}
                <a href="{{ url_for('dashboard') }}" class="nav-link">Dashboard</a>

                <div class="nav-dropdown">
                    <button type="button" class="nav-dropdown-toggle">Vendas</button>
                    <div class="nav-submenu">
                        <a href="{{ url_for('pdv') }}" class="nav-link nav-sublink">PDV</a>
                        <a href="{{ url_for('listar_pedidos') }}" class="nav-link nav-sublink">Pedidos</a>
                        {% if atendimento_mesas_ativo %}
                        <a href="{{ url_for('listar_mesas') }}" class="nav-link nav-sublink">Mesas</a>
                        {% endif %}
                        <a href="{{ url_for('listar_caixas') }}" class="nav-link nav-sublink">Caixas</a>
                        {% if atendimento_mesas_ativo %}
                        <a href="{{ url_for('listar_garcons') }}" class="nav-link nav-sublink">Garcons</a>
                        <a href="{{ url_for('configurar_distribuicao_garcons') }}" class="nav-link nav-sublink">Distribuicao</a>
                        {% endif %}
                        {% if funcionario_logado.role in ['admin', 'gerente'] and atendimento_mesas_ativo %}
                        <a href="{{ url_for('editar_empresa') }}#config-cardapio" class="nav-link nav-sublink">Cardapio QR</a>
                        {% endif %}
                    </div>
                </div>

                <div class="nav-dropdown">
                    <button type="button" class="nav-dropdown-toggle">Estoque</button>
                    <div class="nav-submenu">
                        <a href="{{ url_for('listar_produtos') }}" class="nav-link nav-sublink">Produtos</a>
                        <a href="{{ url_for('listar_estoques') }}" class="nav-link nav-sublink">Estoques</a>
                        <a href="{{ url_for('listar_categorias') }}" class="nav-link nav-sublink">Categorias</a>
                        <a href="{{ url_for('listar_fornecedores') }}" class="nav-link nav-sublink">Fornecedores</a>
                        <a href="{{ url_for('listar_recebimentos_fornecedor') }}" class="nav-link nav-sublink">Recebimentos</a>
                        <a href="{{ url_for('listar_movimentacoes') }}" class="nav-link nav-sublink">Movimentacoes</a>
                        <a href="{{ url_for('relatorios') }}" class="nav-link nav-sublink">Relatorios</a>
                    </div>
                </div>

                {% if funcionario_logado.role in ['admin', 'gerente'] %}
                <div class="nav-dropdown">
                    <button type="button" class="nav-dropdown-toggle">Meu RH</button>
                    <div class="nav-submenu">
                        <a href="{{ url_for('indicadores_rh') }}" class="nav-link nav-sublink">Indicadores RH</a>
                        <a href="{{ url_for('listar_funcionarios') }}" class="nav-link nav-sublink">Funcionarios</a>
                        <a href="{{ url_for('listar_funcoes_rh') }}" class="nav-link nav-sublink">Funcoes</a>
                        <a href="{{ url_for('auditoria_sistema') }}" class="nav-link nav-sublink">Auditoria</a>
                        <a href="{{ url_for('editar_empresa') }}" class="nav-link nav-sublink">Empresa</a>
                    </div>
                </div>
                {% endif %}

                <div class="nav-dropdown nav-dropdown-user">
                    <button type="button" class="nav-dropdown-toggle nav-user-toggle">{{ funcionario_logado.nome }}</button>
                    <div class="nav-submenu">
                        <a href="{{ url_for('logout') }}" class="nav-link nav-sublink">Sair</a>
                    </div>
                </div>
                {% else %}
                <a href="{{ url_for('login') }}" class="nav-link">Login</a>
                <a href="{{ url_for('registro') }}" class="nav-link">Registrar</a>
                {% endif %}
            </nav>
        </div>
    </header>

    <main class="main-content">
        <div class="container content-shell">
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        {% set bs_category = 'danger' if category in ['error', 'danger'] else category %}
                        <div class="alert alert-{{ bs_category }} alert-dismissible fade show shadow-sm" role="alert">
                            {{ message }}
                            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Fechar"></button>
                        </div>
                    {% endfor %}
                {% endif %}
            {% endwith %}

            <div class="container page-container">
                {% block content %}{% endblock %}
            </div>
        </div>
    </main>

    <footer class="footer">
        <div class="container footer-inner">
            <p>&copy; {{ ano_atual }} SystemLR - Gestao de Estoque. Visite <strong>systemlr.com</strong></p>
        </div>
    </footer>

    <div class="modal fade" id="confirmActionModal" tabindex="-1" aria-labelledby="confirmActionModalTitle" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="confirmActionModalTitle">Confirmar Acao</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Fechar"></button>
                </div>
                <div class="modal-body" id="confirmActionModalMessage">
                    Tem certeza que deseja continuar?
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Cancelar</button>
                    <button type="button" class="btn btn-danger" id="confirmActionModalOk">Confirmar</button>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="{{ url_for('static', filename='js/csrf.js') }}"></script>
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

---

### Arquivo: `templates\components\list_macros.html`

```html
{% macro post_action_button(action_url, label, btn_class='btn-small btn-danger', confirm_message='') -%}
<form method="POST" action="{{ action_url }}" class="inline-form"{% if confirm_message %} data-confirm-message="{{ confirm_message }}"{% endif %}>
    {{ csrf_input|safe }}
    <button type="submit" class="{{ btn_class }}">{{ label }}</button>
</form>
{%- endmacro %}
```

---

### Arquivo: `templates\dashboard\index.html`

```html
{% extends "base.html" %}

{% block title %}Dashboard - SystemLR{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Dashboard Financeiro e Gestao</h1>
    <form method="get" class="dashboard-filter-form">
        <label for="data_inicial" class="dashboard-filter-label">De:</label>
        <input type="date" id="data_inicial" name="data_inicial" value="{{ data_inicial }}" class="input-text dashboard-filter-select">
        <label for="data_final" class="dashboard-filter-label">Ate:</label>
        <input type="date" id="data_final" name="data_final" value="{{ data_final }}" class="input-text dashboard-filter-select">
        <button type="submit" class="btn btn-primary dashboard-filter-button">Aplicar</button>
    </form>
</div>

<div class="cards-container analytics-cards">
    <div class="card card-primary">
        <div class="card-content">
            <h3>Faturamento no Periodo</h3>
            <p class="card-value" id="kpiFaturamentoPeriodo">R$ {{ '%.2f'|format(faturamento_periodo) }}</p>
            <p class="card-meta" id="kpiPedidosPeriodo">{{ pedidos_periodo_total }} pedidos fechados</p>
        </div>
    </div>
    <div class="card card-success">
        <div class="card-content">
            <h3>Ticket Medio</h3>
            <p class="card-value" id="kpiTicketMedio">R$ {{ '%.2f'|format(ticket_medio_periodo) }}</p>
            <p class="card-meta">Media por pedido fechado</p>
        </div>
    </div>
    <div class="card card-info">
        <div class="card-content">
            <h3>Faturamento Hoje</h3>
            <p class="card-value" id="kpiFaturamentoHoje">R$ {{ '%.2f'|format(faturamento_hoje) }}</p>
            <p class="card-meta">Somente pedidos concluidos hoje</p>
        </div>
    </div>
    <div class="card card-warning">
        <div class="card-content">
            <h3>Pedidos em Aberto / Cancelados</h3>
            <p class="card-value"><span id="kpiPedidosAbertos">{{ pedidos_abertos }}</span> / <span id="kpiPedidosCancelados">{{ pedidos_cancelados_periodo }}</span></p>
            <p class="card-meta">Abertos agora / cancelados no periodo</p>
        </div>
    </div>
</div>

<div class="analytics-grid">
    <section class="section">
        <h2>Grafico - Faturamento Diario</h2>
        <div class="chart-container">
            <canvas id="chartFaturamento"></canvas>
        </div>
    </section>
    <section class="section">
        <h2>Grafico - Status de Pedidos</h2>
        <div class="chart-container">
            <canvas id="chartStatus"></canvas>
        </div>
    </section>
</div>

<div class="analytics-grid">
    <section class="section">
        <h2>Grafico - Metodos de Pagamento</h2>
        <div class="chart-container">
            <canvas id="chartPagamento"></canvas>
        </div>
    </section>
    <section class="section">
        <h2>Grafico - Top Produtos (Receita)</h2>
        <div class="chart-container">
            <canvas id="chartTopProdutos"></canvas>
        </div>
    </section>
</div>

<div class="analytics-grid">
    <section class="section analytics-trend-section">
        <h2>Tendencia de Vendas - Ultimos {{ periodo_dias }} Dias</h2>
        <div class="trend-list">
            {% for dia in vendas_periodo %}
            <div class="trend-row">
                <div class="trend-day">
                    <strong>{{ dia.data_curta }}</strong>
                    <span>{{ dia.data_semana }}</span>
                </div>
                <div class="trend-bar-wrap">
                    <div class="trend-bar" style="width: {{ '%.2f'|format(dia.faturamento_pct) }}%;"></div>
                </div>
                <div class="trend-values">
                    <strong>R$ {{ '%.2f'|format(dia.faturamento) }}</strong>
                    <span>{{ dia.pedidos }} pedidos</span>
                </div>
            </div>
            {% endfor %}
        </div>
    </section>

    <section class="section analytics-summary-section">
        <h2>Pedidos por Status</h2>
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Status</th>
                        <th>Quantidade</th>
                    </tr>
                </thead>
                <tbody>
                    {% for item in pedidos_por_status %}
                    <tr>
                        <td data-label="Status">{{ item.label }}</td>
                        <td data-label="Quantidade">{{ item.quantidade }}</td>
                    </tr>
                    {% else %}
                    <tr>
                        <td colspan="2" class="text-center">Sem pedidos no periodo selecionado.</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </section>
</div>

<div class="analytics-grid">
    <section class="section">
        <h2>Top Produtos Vendidos</h2>
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Produto</th>
                        <th>Qtd Vendida</th>
                        <th>Receita</th>
                    </tr>
                </thead>
                <tbody>
                    {% for produto, qtd, receita in top_produtos_vendidos %}
                    <tr>
                        <td data-label="Produto">{{ produto.nome }}</td>
                        <td data-label="Qtd Vendida">{{ qtd or 0 }}</td>
                        <td data-label="Receita">R$ {{ '%.2f'|format(receita or 0) }}</td>
                    </tr>
                    {% else %}
                    <tr>
                        <td colspan="3" class="text-center">Sem vendas fechadas no periodo selecionado.</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </section>

    <section class="section">
        <h2>Top Clientes</h2>
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Cliente</th>
                        <th>Pedidos</th>
                        <th>Faturamento</th>
                    </tr>
                </thead>
                <tbody>
                    {% for item in top_clientes %}
                    <tr>
                        <td data-label="Cliente">{{ item.cliente_nome }}</td>
                        <td data-label="Pedidos">{{ item.pedidos or 0 }}</td>
                        <td data-label="Faturamento">R$ {{ '%.2f'|format(item.faturamento or 0) }}</td>
                    </tr>
                    {% else %}
                    <tr>
                        <td colspan="3" class="text-center">Sem clientes identificados no periodo.</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </section>
</div>

<div class="analytics-grid">
    <section class="section">
        <h2>Desempenho de Garcons</h2>
        <div class="chart-container performance-chart-container">
            <canvas id="chartDesempenhoGarcons"></canvas>
        </div>
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Garcom</th>
                        <th>Pedidos</th>
                        <th>Faturamento</th>
                    </tr>
                </thead>
                <tbody>
                    {% for item in desempenho_garcons %}
                    <tr>
                        <td data-label="Garcom">{{ item.nome }}</td>
                        <td data-label="Pedidos">{{ item.pedidos or 0 }}</td>
                        <td data-label="Faturamento">R$ {{ '%.2f'|format(item.faturamento or 0) }}</td>
                    </tr>
                    {% else %}
                    <tr>
                        <td colspan="3" class="text-center">Sem pedidos com garcom no periodo.</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </section>

    <section class="section">
        <h2>Desempenho de Caixas</h2>
        <div class="chart-container performance-chart-container">
            <canvas id="chartDesempenhoCaixas"></canvas>
        </div>
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Caixa</th>
                        <th>Pedidos</th>
                        <th>Faturamento</th>
                    </tr>
                </thead>
                <tbody>
                    {% for item in desempenho_caixas %}
                    <tr>
                        <td data-label="Caixa">{{ item.nome }}</td>
                        <td data-label="Pedidos">{{ item.pedidos or 0 }}</td>
                        <td data-label="Faturamento">R$ {{ '%.2f'|format(item.faturamento or 0) }}</td>
                    </tr>
                    {% else %}
                    <tr>
                        <td colspan="3" class="text-center">Sem pedidos em caixa no periodo.</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </section>
</div>

<div class="section">
    <h2>Formas de Pagamento</h2>
    <div class="table-responsive">
        <table class="table">
            <thead>
                <tr>
                    <th>Metodo</th>
                    <th>Quantidade de Pedidos</th>
                </tr>
            </thead>
            <tbody>
                {% for item in metodos_pagamento %}
                <tr>
                    <td data-label="Metodo">{{ item.metodo|capitalize }}</td>
                    <td data-label="Quantidade">{{ item.quantidade }}</td>
                </tr>
                {% else %}
                <tr>
                    <td colspan="2" class="text-center">Sem informacao de pagamento no periodo.</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>

<div class="action-buttons">
    <a href="{{ url_for('pdv') }}" class="btn btn-primary">Abrir PDV</a>
    <a href="{{ url_for('listar_pedidos') }}" class="btn btn-secondary">Gerenciar Pedidos</a>
    <a href="{{ url_for('relatorios') }}" class="btn btn-info">Relatorios de Estoque</a>
    {% if funcionario_logado and funcionario_logado.role in ['admin', 'gerente'] %}
    <a href="{{ url_for('indicadores_rh') }}" class="btn btn-success">Indicadores RH</a>
    {% endif %}
</div>
{% endblock %}

{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js"></script>
<script src="{{ url_for('static', filename='js/pages/dashboard_analytics.js') }}"></script>
{% endblock %}
```

---

### Arquivo: `templates\errors\404.html`

```html
{% extends "base.html" %}

{% block title %}Erro 404 - SystemLR{% endblock %}

{% block content %}
<div class="error-container">
    <div class="error-code">404</div>
    <h1>Página Não Encontrada</h1>
    <p>Desculpe, a página que você procura não existe.</p>
    <a href="{{ url_for('index') }}" class="btn btn-primary">← Voltar para Home</a>
</div>
{% endblock %}
```

---

### Arquivo: `templates\errors\500.html`

```html
{% extends "base.html" %}

{% block title %}Erro 500 - SystemLR{% endblock %}

{% block content %}
<div class="error-container">
    <div class="error-code">500</div>
    <h1>Erro Interno do Servidor</h1>
    <p>{{ error_message if error_message else 'Desculpe, algo deu errado. Estamos trabalhando para corrigir.' }}</p>
    <a href="{{ url_for('index') }}" class="btn btn-primary">Voltar para Home</a>
</div>
{% endblock %}
```

---

### Arquivo: `templates\estoque\categorias\categorias.html`

```html
﻿{% extends "base.html" %}

{% block title %}Categorias - SystemLR{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Categorias</h1>
    <a href="{{ url_for('nova_categoria') }}" class="btn btn-primary">Nova Categoria</a>
</div>

<div class="grid-container">
    {% for categoria in categorias %}
    <div class="card-category">
        {% if categoria.imagem_path %}
        <img src="{{ url_for('static', filename=categoria.imagem_path) }}" alt="{{ categoria.nome }}" style="width:100%;height:160px;object-fit:cover;border-radius:8px;border:1px solid var(--border);margin-bottom:10px;">
        {% endif %}
        <div class="card-category-header">
            <h3>{{ categoria.nome }}</h3>
            <span class="badge">{{ categoria.produtos|length }} produtos</span>
        </div>
        <p class="card-category-desc">{{ categoria.descricao or 'Sem descricao' }}</p>
        <div class="card-category-actions">
            <a href="{{ url_for('editar_categoria', categoria_id=categoria.id) }}" class="btn-small btn-warning">Editar</a>
            <form method="POST" action="{{ url_for('deletar_categoria', categoria_id=categoria.id) }}" class="inline-form" data-confirm-message="Tem certeza? Todos os produtos desta categoria serao removidos!">
                <button type="submit" class="btn-small btn-danger">Deletar</button>
            </form>
        </div>
    </div>
    {% else %}
    <div class="section">
        <p class="text-center">Nenhuma categoria cadastrada</p>
    </div>
    {% endfor %}
</div>
{% endblock %}

```

---

### Arquivo: `templates\estoque\categorias\editar_categoria.html`

```html
{% extends "base.html" %}

{% block title %}Editar Categoria - SystemLR{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Editar Categoria</h1>
</div>

<div class="form-container">
    <form method="POST" enctype="multipart/form-data" class="form">
        <div class="form-group">
            <label for="nome">Nome da Categoria *</label>
            <input type="text" id="nome" name="nome" required value="{{ categoria.nome }}" class="input-text">
        </div>

        <div class="form-group">
            <label for="descricao">Descricao</label>
            <textarea id="descricao" name="descricao" class="input-textarea" rows="4">{{ categoria.descricao or '' }}</textarea>
        </div>

        <div class="form-group">
            <label for="imagem">Imagem da Categoria</label>
            <input type="file" id="imagem" name="imagem" accept=".png,.jpg,.jpeg,.webp,.gif" class="input-text">
            {% if categoria.imagem_path %}
            <div class="product-image-preview">
                <img src="{{ url_for('static', filename=categoria.imagem_path) }}" alt="{{ categoria.nome }}">
                <label class="checkbox-inline">
                    <input type="checkbox" name="remover_imagem">
                    Remover imagem atual
                </label>
            </div>
            {% endif %}
        </div>

        <div class="form-actions">
            <button type="submit" class="btn btn-primary">Salvar Alteracoes</button>
            <a href="{{ url_for('listar_categorias') }}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>
{% endblock %}
```

---

### Arquivo: `templates\estoque\categorias\nova_categoria.html`

```html
{% extends "base.html" %}

{% block title %}Nova Categoria - SystemLR{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Nova Categoria</h1>
</div>

<div class="form-container">
    <form method="POST" enctype="multipart/form-data" class="form">
        <div class="form-group">
            <label for="nome">Nome da Categoria *</label>
            <input type="text" id="nome" name="nome" required placeholder="Ex: Bebidas" class="input-text">
        </div>

        <div class="form-group">
            <label for="descricao">Descricao</label>
            <textarea id="descricao" name="descricao" placeholder="Descrever a categoria..." class="input-textarea" rows="4"></textarea>
        </div>

        <div class="form-group">
            <label for="imagem">Imagem da Categoria</label>
            <input type="file" id="imagem" name="imagem" accept=".png,.jpg,.jpeg,.webp,.gif" class="input-text">
        </div>

        <div class="form-actions">
            <button type="submit" class="btn btn-primary">Salvar Categoria</button>
            <a href="{{ url_for('listar_categorias') }}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>
{% endblock %}
```

---

### Arquivo: `templates\estoque\enderecos\detalhes_endereco.html`

```html
{% extends "base.html" %}

{% block title %}Produtos no Endereco - SystemLR{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Produtos Armazenados no Endereco</h1>
    <div class="header-actions">
        <a href="{{ url_for('listar_enderecos_estoque', estoque_id=endereco.estoque_id or '') }}" class="btn btn-secondary">Voltar para Enderecos</a>
    </div>
</div>

<div class="cards-container analytics-cards">
    <div class="card card-info">
        <div class="card-content">
            <h3>Endereco</h3>
            <p class="card-value">{{ endereco.nome }}</p>
            <p class="card-meta"><code>{{ endereco.codigo_localizacao or '-' }}</code></p>
        </div>
    </div>
    <div class="card card-primary">
        <div class="card-content">
            <h3>Produtos</h3>
            <p class="card-value">{{ produtos|length }}</p>
            <p class="card-meta">Itens vinculados</p>
        </div>
    </div>
    <div class="card card-success">
        <div class="card-content">
            <h3>Total Unidades</h3>
            <p class="card-value">{{ total_unidades }}</p>
            <p class="card-meta">Saldo fisico</p>
        </div>
    </div>
    <div class="card card-warning">
        <div class="card-content">
            <h3>Valor em Custo</h3>
            <p class="card-value">R$ {{ "%.2f"|format(valor_total) }}</p>
            <p class="card-meta">Estimado</p>
        </div>
    </div>
</div>

<div class="table-responsive table-scroll-sticky">
    <table class="table">
        <thead>
            <tr>
                <th>Codigo</th>
                <th>Produto</th>
                <th>Categoria</th>
                <th>Estoque</th>
                <th>Minimo</th>
                <th>Status</th>
                <th>Acoes</th>
            </tr>
        </thead>
        <tbody>
            {% for produto in produtos %}
            <tr class="{% if produto.em_falta %}row-warning{% endif %}">
                <td data-label="Codigo"><code>{{ produto.codigo }}</code></td>
                <td data-label="Produto">{{ produto.nome }}</td>
                <td data-label="Categoria">{{ produto.categoria.nome if produto.categoria else '-' }}</td>
                <td data-label="Estoque">{{ produto.quantidade_estoque }}</td>
                <td data-label="Minimo">{{ produto.quantidade_minima }}</td>
                <td data-label="Status">
                    {% if produto.ativo %}
                    <span class="badge badge-success">Ativo</span>
                    {% else %}
                    <span class="badge badge-danger">Inativo</span>
                    {% endif %}
                </td>
                <td data-label="Acoes">
                    <a href="{{ url_for('visualizar_produto', produto_id=produto.id) }}" class="btn-small btn-info">Ver</a>
                </td>
            </tr>
            {% else %}
            <tr>
                <td colspan="7" class="text-center">Nenhum produto armazenado neste endereco.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
```

---

### Arquivo: `templates\estoque\enderecos\editar_endereco.html`

```html
{% extends "base.html" %}

{% block title %}Editar Endereco de Estoque - SystemLR{% endblock %}

{% block content %}
{% set restricoes_atuais = (endereco.restricoes or '').split(',') %}
<div class="page-header">
    <h1>Editar Endereco de Estoque</h1>
</div>

<div class="form-container">
    <form method="POST" class="form">
        {{ csrf_input|safe }}

        <h3 class="mb-2">Secao 1: Identificacao</h3>
        <div class="form-row">
            <div class="form-group">
                <label for="estoque_id">Estoque *</label>
                <select id="estoque_id" name="estoque_id" class="input-select" required>
                    <option value="">Selecione um estoque</option>
                    {% for estoque in estoques %}
                    <option value="{{ estoque.id }}" {% if endereco.estoque_id == estoque.id %}selected{% endif %}>{{ estoque.nome }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="form-group">
                <label for="nome">Nome do Endereco *</label>
                <input type="text" id="nome" name="nome" class="input-text" required maxlength="120" value="{{ endereco.nome }}">
            </div>
        </div>

        <div class="form-row">
            <div class="form-group">
                <label for="loja_cd">Loja/CD *</label>
                <input type="text" id="loja_cd" name="loja_cd" class="input-text" required maxlength="20" value="{{ endereco.loja_cd or endereco.codigo_armazem or '' }}">
            </div>
            <div class="form-group">
                <label for="setor_zona">Setor/Zona *</label>
                <select id="setor_zona" name="setor_zona" class="input-select" required>
                    <option value="">Selecione</option>
                    {% for item in setores_zona_validos %}
                    <option value="{{ item }}" {% if endereco.setor_zona == item %}selected{% endif %}>{{ item.replace('_', ' ')|title }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="form-group">
                <label for="tipo_area">Tipo de Area *</label>
                <select id="tipo_area" name="tipo_area" class="input-select" required>
                    <option value="">Selecione</option>
                    {% for item in tipos_area_validos %}
                    <option value="{{ item }}" {% if endereco.tipo_area == item %}selected{% endif %}>{{ item.replace('_', ' ')|title }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="form-group">
                <label for="status">Status *</label>
                <select id="status" name="status" class="input-select" required>
                    <option value="">Selecione</option>
                    {% for item in status_endereco_validos %}
                    <option value="{{ item }}" {% if endereco.status == item %}selected{% endif %}>{{ item|title }}</option>
                    {% endfor %}
                </select>
            </div>
        </div>

        <div class="form-group">
            <label for="descricao">Descricao</label>
            <input type="text" id="descricao" name="descricao" class="input-text" maxlength="255" value="{{ endereco.descricao or '' }}">
        </div>
        <div class="form-group">
            <label for="tipo_produto_reservado_categoria_id">Tipo de produto reservado *</label>
            <select id="tipo_produto_reservado_categoria_id" name="tipo_produto_reservado_categoria_id" class="input-select" required>
                <option value="">Selecione uma categoria</option>
                {% for categoria in categorias %}
                <option value="{{ categoria.id }}" {% if endereco.tipo_produto_reservado == categoria.nome %}selected{% endif %}>
                    {{ categoria.nome }}
                </option>
                {% endfor %}
            </select>
        </div>
        <div class="form-group">
            <label for="observacoes">Observacoes</label>
            <textarea id="observacoes" name="observacoes" class="input-textarea" rows="3" maxlength="1000">{{ endereco.observacoes or '' }}</textarea>
        </div>

        <h3 class="mb-2 mt-3">Secao 2: Tipo de Estrutura</h3>
        <div class="form-group">
            <label class="checkbox-inline me-3">
                <input type="radio" name="tipo_estrutura" value="rack" {% if (endereco.tipo_estrutura or 'rack') == 'rack' %}checked{% endif %}>
                Rack / Estante
            </label>
            <label class="checkbox-inline">
                <input type="radio" name="tipo_estrutura" value="area_aberta" {% if endereco.tipo_estrutura == 'area_aberta' %}checked{% endif %}>
                Area Aberta
            </label>
        </div>

        <div id="grupo-rack">
            <div class="form-row">
                <div class="form-group">
                    <label for="rua_corredor">Rua/Corredor *</label>
                    <input type="text" id="rua_corredor" name="rua_corredor" class="input-text" maxlength="20" value="{{ endereco.rua_corredor or '' }}">
                </div>
                <div class="form-group">
                    <label for="rack_estante">Rack/Estante *</label>
                    <input type="text" id="rack_estante" name="rack_estante" class="input-text" maxlength="10" value="{{ endereco.coluna_baia or '' }}">
                </div>
                <div class="form-group">
                    <label for="nivel_prateleira">Nivel/Prateleira *</label>
                    <input type="text" id="nivel_prateleira" name="nivel_prateleira" class="input-text" maxlength="10" value="{{ endereco.nivel_prateleira or '' }}">
                </div>
                <div class="form-group">
                    <label for="posicao_slot">Vao/Slot *</label>
                    <input type="text" id="posicao_slot" name="posicao_slot" class="input-text" maxlength="10" value="{{ endereco.posicao_slot or '' }}">
                </div>
                <div class="form-group">
                    <label for="lado">Lado *</label>
                    <select id="lado" name="lado" class="input-select">
                        <option value="">Selecione</option>
                        <option value="A" {% if endereco.lado in ['A', 'LA'] %}selected{% endif %}>A (LA)</option>
                        <option value="B" {% if endereco.lado in ['B', 'LB'] %}selected{% endif %}>B (LB)</option>
                        <option value="E" {% if endereco.lado in ['E', 'LE'] %}selected{% endif %}>E (LE)</option>
                        <option value="D" {% if endereco.lado in ['D', 'LD'] %}selected{% endif %}>D (LD)</option>
                    </select>
                </div>
            </div>
        </div>

        <div id="grupo-area-aberta" class="is-hidden">
            <div class="form-group">
                <label for="ponto_local">Ponto/Local *</label>
                <input type="text" id="ponto_local" name="ponto_local" class="input-text" maxlength="255" value="{{ endereco.ponto_local or '' }}">
            </div>
        </div>

        <h3 class="mb-2 mt-3">Secao 3: Regras de Armazenagem</h3>
        <div class="form-row">
            <div class="form-group">
                <label class="checkbox-inline"><input type="checkbox" name="permite_fracionado" {% if endereco.permite_fracionado %}checked{% endif %}> Permite fracionado</label>
            </div>
            <div class="form-group">
                <label class="checkbox-inline"><input type="checkbox" name="permite_mistura_sku" {% if endereco.permite_mistura_sku %}checked{% endif %}> Permite mistura SKU</label>
            </div>
            <div class="form-group">
                <label class="checkbox-inline"><input type="checkbox" name="permite_mistura_lote" {% if endereco.permite_mistura_lote %}checked{% endif %}> Permite mistura lote</label>
            </div>
        </div>
        <div class="form-row">
            <div class="form-group">
                <label for="controle_validade">Controle de validade *</label>
                <select id="controle_validade" name="controle_validade" class="input-select" required>
                    {% for item in controle_validade_validos %}
                    <option value="{{ item }}" {% if (endereco.controle_validade or 'nenhum') == item %}selected{% endif %}>{{ item|upper }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="form-group">
                <label for="temperatura">Temperatura</label>
                <select id="temperatura" name="temperatura" class="input-select">
                    <option value="">Selecione</option>
                    {% for item in temperatura_validos %}
                    <option value="{{ item }}" {% if endereco.temperatura == item %}selected{% endif %}>{{ item|title }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="form-group">
                <label for="sku_produto">SKU principal (opcional)</label>
                <input type="text" id="sku_produto" name="sku_produto" class="input-text" maxlength="100" value="{{ endereco.sku_produto or '' }}">
            </div>
        </div>
        <div class="form-group">
            <label>Restricoes</label>
            <div class="form-row">
                {% for item in restricoes_validas %}
                <label class="checkbox-inline me-3"><input type="checkbox" name="restricoes" value="{{ item }}" {% if item in restricoes_atuais %}checked{% endif %}> {{ item.replace('_', ' ')|title }}</label>
                {% endfor %}
            </div>
        </div>

        <h3 class="mb-2 mt-3">Secao 4: Capacidade</h3>
        <div class="form-row">
            <div class="form-group"><label for="capacidade_caixas">Capacidade caixas</label><input type="number" min="0" id="capacidade_caixas" name="capacidade_caixas" class="input-text" value="{{ endereco.capacidade_caixas if endereco.capacidade_caixas is not none else '' }}"></div>
            <div class="form-group"><label for="capacidade_fardos">Capacidade fardos</label><input type="number" min="0" id="capacidade_fardos" name="capacidade_fardos" class="input-text" value="{{ endereco.capacidade_fardos if endereco.capacidade_fardos is not none else '' }}"></div>
            <div class="form-group"><label for="capacidade_unidades">Capacidade unidades</label><input type="number" min="0" id="capacidade_unidades" name="capacidade_unidades" class="input-text" value="{{ endereco.capacidade_unidades if endereco.capacidade_unidades is not none else '' }}"></div>
            <div class="form-group"><label for="capacidade_pallets">Capacidade pallets</label><input type="number" min="0" id="capacidade_pallets" name="capacidade_pallets" class="input-text" value="{{ endereco.capacidade_pallets if endereco.capacidade_pallets is not none else '' }}"></div>
        </div>
        <div class="form-row">
            <div class="form-group"><label for="peso_max_kg">Peso max. (kg)</label><input type="number" min="0" step="0.01" id="peso_max_kg" name="peso_max_kg" class="input-text" value="{{ endereco.peso_max_kg if endereco.peso_max_kg is not none else '' }}"></div>
            <div class="form-group"><label for="volume_max_m3">Volume max. (m3)</label><input type="number" min="0" step="0.001" id="volume_max_m3" name="volume_max_m3" class="input-text" value="{{ endereco.volume_max_m3 if endereco.volume_max_m3 is not none else '' }}"></div>
            <div class="form-group">
                <label for="prioridade_picking">Prioridade picking</label>
                <select id="prioridade_picking" name="prioridade_picking" class="input-select">
                    <option value="0" {% if not endereco.prioridade_picking %}selected{% endif %}>Nao</option>
                    <option value="1" {% if endereco.prioridade_picking %}selected{% endif %}>Sim</option>
                </select>
            </div>
        </div>

        <h3 class="mb-2 mt-3">Secao 5: Codigo Gerado</h3>
        <div class="form-group">
            <label for="codigo_localizacao_preview">Codigo do Endereco</label>
            <input type="text" id="codigo_localizacao_preview" name="codigo_localizacao" class="input-text" readonly required value="{{ endereco.codigo_localizacao or '' }}">
            <small class="text-muted">Gerado automaticamente conforme os campos preenchidos.</small>
        </div>

        <div class="form-row">
            <div class="form-group"><label for="rua">Endereco civil (rua)</label><input type="text" id="rua" name="rua" class="input-text" maxlength="160" value="{{ endereco.rua or '' }}"></div>
            <div class="form-group"><label for="numero">Numero</label><input type="text" id="numero" name="numero" class="input-text" maxlength="20" value="{{ endereco.numero or '' }}"></div>
            <div class="form-group"><label for="bairro">Bairro</label><input type="text" id="bairro" name="bairro" class="input-text" maxlength="100" value="{{ endereco.bairro or '' }}"></div>
        </div>
        <div class="form-row">
            <div class="form-group"><label for="cidade">Cidade</label><input type="text" id="cidade" name="cidade" class="input-text" maxlength="100" value="{{ endereco.cidade or '' }}"></div>
            <div class="form-group"><label for="estado">UF</label><input type="text" id="estado" name="estado" class="input-text" maxlength="2" value="{{ endereco.estado or '' }}"></div>
            <div class="form-group"><label for="cep">CEP</label><input type="text" id="cep" name="cep" class="input-text" maxlength="12" value="{{ endereco.cep or '' }}"></div>
            <div class="form-group"><label for="complemento">Complemento</label><input type="text" id="complemento" name="complemento" class="input-text" maxlength="120" value="{{ endereco.complemento or '' }}"></div>
        </div>

        <div class="form-actions">
            <button type="submit" class="btn btn-primary">Salvar Alteracoes</button>
            <a href="{{ url_for('listar_enderecos_estoque') }}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>

<script>
function semAcento(texto) {
    return (texto || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '');
}
function token(texto) {
    return semAcento(texto).toUpperCase().trim().replace(/\s+/g, '').replace(/[^A-Z0-9_]/g, '');
}
function slug(texto) {
    return semAcento(texto).toUpperCase().trim().replace(/[\s_/]+/g, '-').replace(/[^A-Z0-9-]/g, '-').replace(/-+/g, '-').replace(/^-|-$/g, '');
}
function n2(valor) {
    const m = String(valor || '').match(/\d+/);
    if (!m) return '';
    return String(parseInt(m[0], 10)).padStart(2, '0');
}
function ladoNorm(lado) {
    const mapa = {A: 'LA', B: 'LB', E: 'LE', D: 'LD', LA: 'LA', LB: 'LB', LE: 'LE', LD: 'LD'};
    return mapa[token(lado)] || '';
}
function siglaSetor(setor) {
    const mapa = {
        secos: 'SEC', bebidas: 'BEB', hortifruti: 'HOR', frios: 'FRI', congelados: 'CON',
        acougue: 'ACO', padaria: 'PAD', deposito: 'DEP', frente_loja: 'FL',
        ecommerce_picking: 'ECP', quarentena: 'QUA', avaria: 'AVA', devolucao: 'DEV'
    };
    return mapa[setor] || '';
}
function codigoAreaAberta(ponto) {
    const t = semAcento(ponto || '').toUpperCase();
    const gm = t.match(/(?:\bGONDOLA\b|\bG\b)\s*0*(\d+)/);
    const pm = t.match(/(?:\bPRATELEIRA\b|\bP\b)\s*0*(\d+)/);
    if (gm && pm) return `G${String(parseInt(gm[1], 10)).padStart(2, '0')}-P${String(parseInt(pm[1], 10)).padStart(2, '0')}`;
    return slug(t).slice(0, 24);
}
function estruturaAtual() {
    const el = document.querySelector('input[name="tipo_estrutura"]:checked');
    return el ? el.value : 'rack';
}
function atualizarGrupos() {
    const tipo = estruturaAtual();
    const rack = document.getElementById('grupo-rack');
    const area = document.getElementById('grupo-area-aberta');
    const reqRack = ['rua_corredor', 'rack_estante', 'nivel_prateleira', 'posicao_slot', 'lado'];
    rack.classList.toggle('is-hidden', tipo !== 'rack');
    area.classList.toggle('is-hidden', tipo !== 'area_aberta');
    reqRack.forEach((id) => {
        const e = document.getElementById(id);
        if (e) e.required = tipo === 'rack';
    });
    const ponto = document.getElementById('ponto_local');
    if (ponto) ponto.required = tipo === 'area_aberta';
    atualizarPreviewCodigo();
}
function atualizarPreviewCodigo() {
    const loja = token(document.getElementById('loja_cd').value);
    const setor = siglaSetor(document.getElementById('setor_zona').value);
    const tipo = estruturaAtual();
    let codigo = '';
    if (loja && setor && tipo === 'rack') {
        const r = n2(document.getElementById('rua_corredor').value);
        const rk = n2(document.getElementById('rack_estante').value);
        const n = n2(document.getElementById('nivel_prateleira').value);
        const v = n2(document.getElementById('posicao_slot').value);
        const l = ladoNorm(document.getElementById('lado').value);
        if (r && rk && n && v && l) codigo = `${loja}-${setor}-R${r}-RK${rk}-N${n}-V${v}-${l}`;
    }
    if (loja && setor && tipo === 'area_aberta') {
        const p = codigoAreaAberta(document.getElementById('ponto_local').value);
        if (p) codigo = `${loja}-${setor}-${p}`;
    }
    document.getElementById('codigo_localizacao_preview').value = codigo;
}
document.querySelectorAll('input,select,textarea').forEach((el) => el.addEventListener('input', atualizarPreviewCodigo));
document.querySelectorAll('input[name="tipo_estrutura"]').forEach((el) => el.addEventListener('change', atualizarGrupos));
atualizarGrupos();
</script>
{% endblock %}
```

---

### Arquivo: `templates\estoque\enderecos\enderecos.html`

```html
﻿{% extends "base.html" %}

{% block title %}Enderecos de Estoque - SystemLR{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Enderecos de Estoque</h1>
    <div class="header-actions">
        <a href="{{ url_for('listar_estoques') }}" class="btn btn-secondary">Ver Estoques</a>
        <a href="{{ url_for('novo_endereco_estoque') }}" class="btn btn-primary">Novo Endereco</a>
    </div>
</div>

<section class="filters-section">
    <form method="GET" class="filters-form">
        <div class="filter-group">
            <label for="estoque_id">Estoque</label>
            <select id="estoque_id" name="estoque_id" class="input-select">
                <option value="">Todos os estoques</option>
                {% for estoque in estoques %}
                <option value="{{ estoque.id }}" {% if filtros and filtros.estoque_id == estoque.id %}selected{% endif %}>{{ estoque.nome }}</option>
                {% endfor %}
            </select>
        </div>
        <div class="filter-group">
            <label for="busca">Busca</label>
            <input type="text" id="busca" name="busca" class="input-search" value="{{ filtros.busca if filtros else '' }}" placeholder="Nome, rua, bairro ou cidade">
        </div>
        <div class="filter-group">
            <label for="status">Status</label>
            <select id="status" name="status" class="input-select">
                <option value="" {% if not filtros or not filtros.status %}selected{% endif %}>Todos</option>
                {% for item in status_endereco_validos %}
                <option value="{{ item }}" {% if filtros and filtros.status == item %}selected{% endif %}>{{ item|title }}</option>
                {% endfor %}
                <option value="inativo" {% if filtros and filtros.status == 'inativo' %}selected{% endif %}>Inativo (legado)</option>
            </select>
        </div>
        <div class="filter-group">
            <label for="setor_zona">Setor/Zona</label>
            <select id="setor_zona" name="setor_zona" class="input-select">
                <option value="">Todos</option>
                {% for item in setores_zona_validos %}
                <option value="{{ item }}" {% if filtros and filtros.setor_zona == item %}selected{% endif %}>{{ item.replace('_', ' ')|title }}</option>
                {% endfor %}
            </select>
        </div>
        <div class="form-actions">
            <button type="submit" class="btn btn-primary">Filtrar</button>
            <a href="{{ url_for('listar_enderecos_estoque') }}" class="btn btn-secondary">Limpar</a>
        </div>
    </form>
</section>

<div class="table-responsive table-scroll-sticky">
    <table class="table">
        <thead>
            <tr>
                <th>Nome</th>
                <th>Loja/CD</th>
                <th>Setor/Zona</th>
                <th>Tipo Area</th>
                <th>Estrutura</th>
                <th>Reservado Para</th>
                <th>Codigo</th>
                <th>Status</th>
                <th>Descricao</th>
                <th>Acoes</th>
            </tr>
        </thead>
        <tbody>
            {% for endereco in enderecos %}
            <tr>
                <td data-label="Nome"><strong>{{ endereco.nome }}</strong></td>
                <td data-label="Loja/CD">{{ endereco.loja_cd or endereco.codigo_armazem or '-' }}</td>
                <td data-label="Setor/Zona">{{ (endereco.setor_zona or '-')|replace('_', ' ')|title }}</td>
                <td data-label="Tipo Area">{{ (endereco.tipo_area or '-')|replace('_', ' ')|title }}</td>
                <td data-label="Estrutura">{{ (endereco.tipo_estrutura or '-')|replace('_', ' ')|title }}</td>
                <td data-label="Reservado Para">{{ endereco.tipo_produto_reservado or '-' }}</td>
                <td data-label="Codigo"><code>{{ endereco.codigo_localizacao or '-' }}</code></td>
                <td data-label="Status">
                    {% set st = (endereco.status or ('ativo' if endereco.ativo else 'bloqueado')) %}
                    <span class="badge {% if st == 'ativo' %}badge-success{% elif st == 'inventario' %}badge-warning{% else %}badge-danger{% endif %}">{{ st|title }}</span>
                </td>
                <td data-label="Descricao">{{ endereco.descricao or '-' }}</td>
                <td data-label="Acoes" class="actions-cell">
                    <a href="{{ url_for('detalhes_endereco_estoque', endereco_id=endereco.id) }}" class="btn-small btn-info">Produtos</a>
                    <a href="{{ url_for('editar_endereco_estoque', endereco_id=endereco.id) }}" class="btn-small btn-warning">Editar</a>
                    <form method="POST" action="{{ url_for('deletar_endereco_estoque', endereco_id=endereco.id) }}" class="inline-form" data-confirm-message="Excluir endereco {{ endereco.nome }}?">
                        {{ csrf_input|safe }}
                        <button type="submit" class="btn-small btn-danger">Excluir</button>
                    </form>
                </td>
            </tr>
            {% else %}
            <tr>
                <td colspan="10" class="text-center">Nenhum endereco cadastrado</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}

```

---

### Arquivo: `templates\estoque\enderecos\novo_endereco.html`

```html
{% extends "base.html" %}

{% block title %}Novo Endereco de Estoque - SystemLR{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Novo Endereco de Estoque</h1>
</div>

<div class="form-container">
    <form method="POST" class="form">
        {{ csrf_input|safe }}

        <h3 class="mb-2">Secao 1: Identificacao</h3>
        <div class="form-row">
            <div class="form-group">
                <label for="estoque_id">Estoque *</label>
                <select id="estoque_id" name="estoque_id" class="input-select" required>
                    <option value="">Selecione um estoque</option>
                    {% for estoque in estoques %}
                    <option value="{{ estoque.id }}">{{ estoque.nome }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="form-group">
                <label for="nome">Nome do Endereco *</label>
                <input type="text" id="nome" name="nome" class="input-text" required maxlength="120" placeholder="Ex: Deposito Secos A">
            </div>
        </div>

        <div class="form-row">
            <div class="form-group">
                <label for="loja_cd">Loja/CD *</label>
                <input type="text" id="loja_cd" name="loja_cd" class="input-text" required maxlength="20" placeholder="Ex: LJ01 ou CD01">
            </div>
            <div class="form-group">
                <label for="setor_zona">Setor/Zona *</label>
                <select id="setor_zona" name="setor_zona" class="input-select" required>
                    <option value="">Selecione</option>
                    {% for item in setores_zona_validos %}
                    <option value="{{ item }}">{{ item.replace('_', ' ')|title }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="form-group">
                <label for="tipo_area">Tipo de Area *</label>
                <select id="tipo_area" name="tipo_area" class="input-select" required>
                    <option value="">Selecione</option>
                    {% for item in tipos_area_validos %}
                    <option value="{{ item }}">{{ item.replace('_', ' ')|title }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="form-group">
                <label for="status">Status *</label>
                <select id="status" name="status" class="input-select" required>
                    <option value="">Selecione</option>
                    {% for item in status_endereco_validos %}
                    <option value="{{ item }}">{{ item|title }}</option>
                    {% endfor %}
                </select>
            </div>
        </div>

        <div class="form-group">
            <label for="descricao">Descricao</label>
            <input type="text" id="descricao" name="descricao" class="input-text" maxlength="255" placeholder="Apelido operacional">
        </div>
        <div class="form-group">
            <label for="tipo_produto_reservado_categoria_id">Tipo de produto reservado *</label>
            <select id="tipo_produto_reservado_categoria_id" name="tipo_produto_reservado_categoria_id" class="input-select" required>
                <option value="">Selecione uma categoria</option>
                {% for categoria in categorias %}
                <option value="{{ categoria.id }}">{{ categoria.nome }}</option>
                {% endfor %}
            </select>
        </div>
        <div class="form-group">
            <label for="observacoes">Observacoes</label>
            <textarea id="observacoes" name="observacoes" class="input-textarea" rows="3" maxlength="1000" placeholder="Instrucoes operacionais do endereco"></textarea>
        </div>

        <h3 class="mb-2 mt-3">Secao 2: Tipo de Estrutura</h3>
        <div class="form-group">
            <label class="checkbox-inline me-3">
                <input type="radio" name="tipo_estrutura" value="rack" checked>
                Rack / Estante
            </label>
            <label class="checkbox-inline">
                <input type="radio" name="tipo_estrutura" value="area_aberta">
                Area Aberta
            </label>
        </div>

        <div id="grupo-rack">
            <div class="form-row">
                <div class="form-group">
                    <label for="rua_corredor">Rua/Corredor *</label>
                    <input type="text" id="rua_corredor" name="rua_corredor" class="input-text" maxlength="20" placeholder="Ex: 03">
                </div>
                <div class="form-group">
                    <label for="rack_estante">Rack/Estante *</label>
                    <input type="text" id="rack_estante" name="rack_estante" class="input-text" maxlength="10" placeholder="Ex: 02">
                </div>
                <div class="form-group">
                    <label for="nivel_prateleira">Nivel/Prateleira *</label>
                    <input type="text" id="nivel_prateleira" name="nivel_prateleira" class="input-text" maxlength="10" placeholder="Ex: 01">
                </div>
                <div class="form-group">
                    <label for="posicao_slot">Vao/Slot *</label>
                    <input type="text" id="posicao_slot" name="posicao_slot" class="input-text" maxlength="10" placeholder="Ex: 08">
                </div>
                <div class="form-group">
                    <label for="lado">Lado *</label>
                    <select id="lado" name="lado" class="input-select">
                        <option value="">Selecione</option>
                        <option value="A">A (LA)</option>
                        <option value="B">B (LB)</option>
                        <option value="E">E (LE)</option>
                        <option value="D">D (LD)</option>
                    </select>
                </div>
            </div>
            <div class="form-group">
                <label class="checkbox-inline">
                    <input type="checkbox" id="cadastrar_lote_rack" name="cadastrar_lote_rack">
                    Cadastrar varios enderecos para este Rack/Estante
                </label>
            </div>
            <div id="grupo-lote-rack" class="is-hidden">
                <div class="form-row">
                    <div class="form-group">
                        <label for="lote_nivel_inicial">Nivel inicial</label>
                        <input type="number" id="lote_nivel_inicial" name="lote_nivel_inicial" class="input-text" min="0" max="99" placeholder="0">
                    </div>
                    <div class="form-group">
                        <label for="lote_nivel_final">Nivel final</label>
                        <input type="number" id="lote_nivel_final" name="lote_nivel_final" class="input-text" min="0" max="99" placeholder="3">
                    </div>
                    <div class="form-group">
                        <label for="lote_vao_inicial">Vao inicial</label>
                        <input type="number" id="lote_vao_inicial" name="lote_vao_inicial" class="input-text" min="1" max="99" placeholder="1">
                    </div>
                    <div class="form-group">
                        <label for="lote_vao_final">Vao final</label>
                        <input type="number" id="lote_vao_final" name="lote_vao_final" class="input-text" min="1" max="99" placeholder="8">
                    </div>
                </div>
                <small class="text-muted">Serao criados enderecos com nome base + N## V## e codigo automatico para cada combinacao.</small>
            </div>
        </div>

        <div id="grupo-area-aberta" class="is-hidden">
            <div class="form-group">
                <label for="ponto_local">Ponto/Local *</label>
                <input type="text" id="ponto_local" name="ponto_local" class="input-text" maxlength="255" placeholder="Ex: Gondola 12 - Prateleira 03">
            </div>
        </div>

        <h3 class="mb-2 mt-3">Secao 3: Regras de Armazenagem</h3>
        <div class="form-row">
            <div class="form-group">
                <label class="checkbox-inline"><input type="checkbox" name="permite_fracionado"> Permite fracionado</label>
            </div>
            <div class="form-group">
                <label class="checkbox-inline"><input type="checkbox" name="permite_mistura_sku"> Permite mistura SKU</label>
            </div>
            <div class="form-group">
                <label class="checkbox-inline"><input type="checkbox" name="permite_mistura_lote"> Permite mistura lote</label>
            </div>
        </div>
        <div class="form-row">
            <div class="form-group">
                <label for="controle_validade">Controle de validade *</label>
                <select id="controle_validade" name="controle_validade" class="input-select" required>
                    {% for item in controle_validade_validos %}
                    <option value="{{ item }}" {% if item == 'nenhum' %}selected{% endif %}>{{ item|upper }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="form-group">
                <label for="temperatura">Temperatura</label>
                <select id="temperatura" name="temperatura" class="input-select">
                    <option value="">Selecione</option>
                    {% for item in temperatura_validos %}
                    <option value="{{ item }}">{{ item|title }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="form-group">
                <label for="sku_produto">SKU principal (opcional)</label>
                <input type="text" id="sku_produto" name="sku_produto" class="input-text" maxlength="100">
            </div>
        </div>
        <div class="form-group">
            <label>Restricoes</label>
            <div class="form-row">
                {% for item in restricoes_validas %}
                <label class="checkbox-inline me-3"><input type="checkbox" name="restricoes" value="{{ item }}"> {{ item.replace('_', ' ')|title }}</label>
                {% endfor %}
            </div>
        </div>

        <h3 class="mb-2 mt-3">Secao 4: Capacidade</h3>
        <div class="form-row">
            <div class="form-group"><label for="capacidade_caixas">Capacidade caixas</label><input type="number" min="0" id="capacidade_caixas" name="capacidade_caixas" class="input-text"></div>
            <div class="form-group"><label for="capacidade_fardos">Capacidade fardos</label><input type="number" min="0" id="capacidade_fardos" name="capacidade_fardos" class="input-text"></div>
            <div class="form-group"><label for="capacidade_unidades">Capacidade unidades</label><input type="number" min="0" id="capacidade_unidades" name="capacidade_unidades" class="input-text"></div>
            <div class="form-group"><label for="capacidade_pallets">Capacidade pallets</label><input type="number" min="0" id="capacidade_pallets" name="capacidade_pallets" class="input-text"></div>
        </div>
        <div class="form-row">
            <div class="form-group"><label for="peso_max_kg">Peso max. (kg)</label><input type="number" min="0" step="0.01" id="peso_max_kg" name="peso_max_kg" class="input-text"></div>
            <div class="form-group"><label for="volume_max_m3">Volume max. (m3)</label><input type="number" min="0" step="0.001" id="volume_max_m3" name="volume_max_m3" class="input-text"></div>
            <div class="form-group">
                <label for="prioridade_picking">Prioridade picking</label>
                <select id="prioridade_picking" name="prioridade_picking" class="input-select">
                    <option value="0" selected>Nao</option>
                    <option value="1">Sim</option>
                </select>
            </div>
        </div>

        <input type="hidden" id="codigo_localizacao_preview" name="codigo_localizacao" value="">

        <div class="form-actions">
            <button type="submit" class="btn btn-primary">Salvar Endereco</button>
            <a href="{{ url_for('listar_enderecos_estoque') }}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>

<script>
function semAcento(texto) {
    return (texto || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '');
}
function token(texto) {
    return semAcento(texto).toUpperCase().trim().replace(/\s+/g, '').replace(/[^A-Z0-9_]/g, '');
}
function slug(texto) {
    return semAcento(texto).toUpperCase().trim().replace(/[\s_/]+/g, '-').replace(/[^A-Z0-9-]/g, '-').replace(/-+/g, '-').replace(/^-|-$/g, '');
}
function n2(valor) {
    const m = String(valor || '').match(/\d+/);
    if (!m) return '';
    return String(parseInt(m[0], 10)).padStart(2, '0');
}
function ladoNorm(lado) {
    const mapa = {A: 'LA', B: 'LB', E: 'LE', D: 'LD', LA: 'LA', LB: 'LB', LE: 'LE', LD: 'LD'};
    return mapa[token(lado)] || '';
}
function siglaSetor(setor) {
    const mapa = {
        secos: 'SEC', bebidas: 'BEB', hortifruti: 'HOR', frios: 'FRI', congelados: 'CON',
        acougue: 'ACO', padaria: 'PAD', deposito: 'DEP', frente_loja: 'FL',
        ecommerce_picking: 'ECP', quarentena: 'QUA', avaria: 'AVA', devolucao: 'DEV'
    };
    return mapa[setor] || '';
}
function codigoAreaAberta(ponto) {
    const t = semAcento(ponto || '').toUpperCase();
    const gm = t.match(/(?:\bGONDOLA\b|\bG\b)\s*0*(\d+)/);
    const pm = t.match(/(?:\bPRATELEIRA\b|\bP\b)\s*0*(\d+)/);
    if (gm && pm) return `G${String(parseInt(gm[1], 10)).padStart(2, '0')}-P${String(parseInt(pm[1], 10)).padStart(2, '0')}`;
    return slug(t).slice(0, 24);
}
function estruturaAtual() {
    const el = document.querySelector('input[name="tipo_estrutura"]:checked');
    return el ? el.value : 'rack';
}
function atualizarGrupos() {
    const tipo = estruturaAtual();
    const rack = document.getElementById('grupo-rack');
    const area = document.getElementById('grupo-area-aberta');
    const lote = document.getElementById('grupo-lote-rack');
    const loteAtivo = document.getElementById('cadastrar_lote_rack')?.checked;
    const reqRackFixos = ['rua_corredor', 'rack_estante', 'lado'];
    const reqRackVariaveis = ['nivel_prateleira', 'posicao_slot'];
    rack.classList.toggle('is-hidden', tipo !== 'rack');
    area.classList.toggle('is-hidden', tipo !== 'area_aberta');
    if (lote) {
        lote.classList.toggle('is-hidden', !(tipo === 'rack' && loteAtivo));
    }
    reqRackFixos.forEach((id) => {
        const e = document.getElementById(id);
        if (e) e.required = tipo === 'rack';
    });
    reqRackVariaveis.forEach((id) => {
        const e = document.getElementById(id);
        if (!e) return;
        const bloquear = (tipo === 'rack' && loteAtivo);
        e.required = (tipo === 'rack' && !loteAtivo);
        e.disabled = bloquear;
    });
    const ponto = document.getElementById('ponto_local');
    if (ponto) ponto.required = tipo === 'area_aberta';

    const loteCampos = ['lote_nivel_inicial', 'lote_nivel_final', 'lote_vao_inicial', 'lote_vao_final'];
    loteCampos.forEach((id) => {
        const e = document.getElementById(id);
        if (!e) return;
        const habilitar = (tipo === 'rack' && loteAtivo);
        e.disabled = !habilitar;
        e.required = habilitar;
    });
    atualizarPreviewCodigo();
}
function atualizarPreviewCodigo() {
    const loja = token(document.getElementById('loja_cd').value);
    const setor = siglaSetor(document.getElementById('setor_zona').value);
    const tipo = estruturaAtual();
    let codigo = '';
    if (loja && setor && tipo === 'rack') {
        const r = n2(document.getElementById('rua_corredor').value);
        const rk = n2(document.getElementById('rack_estante').value);
        const n = n2(document.getElementById('nivel_prateleira').value);
        const v = n2(document.getElementById('posicao_slot').value);
        const l = ladoNorm(document.getElementById('lado').value);
        if (r && rk && n && v && l) codigo = `${loja}-${setor}-R${r}-RK${rk}-N${n}-V${v}-${l}`;
    }
    if (loja && setor && tipo === 'area_aberta') {
        const p = codigoAreaAberta(document.getElementById('ponto_local').value);
        if (p) codigo = `${loja}-${setor}-${p}`;
    }
    document.getElementById('codigo_localizacao_preview').value = codigo;
}
document.querySelectorAll('input,select,textarea').forEach((el) => el.addEventListener('input', atualizarPreviewCodigo));
document.querySelectorAll('input[name="tipo_estrutura"]').forEach((el) => el.addEventListener('change', atualizarGrupos));
const loteCheck = document.getElementById('cadastrar_lote_rack');
if (loteCheck) loteCheck.addEventListener('change', atualizarGrupos);
atualizarGrupos();
</script>
{% endblock %}
```

---

### Arquivo: `templates\estoque\estoques\editar_estoque.html`

```html
{% extends "base.html" %}

{% block title %}Editar Estoque - SystemLR{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Editar Estoque</h1>
</div>

<div class="form-container">
    <form method="POST" class="form">
        {{ csrf_input|safe }}
        <div class="form-group">
            <label for="nome">Nome *</label>
            <input type="text" id="nome" name="nome" class="input-text" required maxlength="120" value="{{ estoque.nome }}">
        </div>

        <div class="form-group">
            <label for="descricao">Descricao</label>
            <input type="text" id="descricao" name="descricao" class="input-text" maxlength="255" value="{{ estoque.descricao or '' }}">
        </div>

        <div class="form-group">
            <label class="checkbox-inline">
                <input type="checkbox" name="ativo" {% if estoque.ativo %}checked{% endif %}>
                Estoque ativo
            </label>
        </div>

        <div class="form-actions">
            <button type="submit" class="btn btn-primary">Salvar Alteracoes</button>
            <a href="{{ url_for('listar_estoques') }}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>
{% endblock %}
```

---

### Arquivo: `templates\estoque\estoques\estoques.html`

```html
{% extends "base.html" %}

{% block title %}Estoques - SystemLR{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Estoques</h1>
    <div class="header-actions">
        <a href="{{ url_for('listar_enderecos_estoque') }}" class="btn btn-secondary">Ver Enderecos</a>
        <a href="{{ url_for('novo_estoque') }}" class="btn btn-primary">Novo Estoque</a>
    </div>
</div>

<section class="filters-section">
    <form method="GET" class="filters-form">
        <div class="filter-group">
            <label for="busca">Busca</label>
            <input type="text" id="busca" name="busca" class="input-search" value="{{ filtros.busca if filtros else '' }}" placeholder="Nome ou descricao do estoque">
        </div>
        <div class="filter-group">
            <label for="status">Status</label>
            <select id="status" name="status" class="input-select">
                <option value="" {% if not filtros or not filtros.status %}selected{% endif %}>Todos</option>
                <option value="ativo" {% if filtros and filtros.status == 'ativo' %}selected{% endif %}>Ativos</option>
                <option value="inativo" {% if filtros and filtros.status == 'inativo' %}selected{% endif %}>Inativos</option>
            </select>
        </div>
        <div class="form-actions">
            <button type="submit" class="btn btn-primary">Filtrar</button>
            <a href="{{ url_for('listar_estoques') }}" class="btn btn-secondary">Limpar</a>
        </div>
    </form>
</section>

<div class="table-responsive table-scroll-sticky">
    <table class="table">
        <thead>
            <tr>
                <th>Nome</th>
                <th>Descricao</th>
                <th>Enderecos</th>
                <th>Status</th>
                <th>Acoes</th>
            </tr>
        </thead>
        <tbody>
            {% for estoque in estoques %}
            <tr>
                <td data-label="Nome"><strong>{{ estoque.nome }}</strong></td>
                <td data-label="Descricao">{{ estoque.descricao or '-' }}</td>
                <td data-label="Enderecos">{{ estoque.enderecos|length }}</td>
                <td data-label="Status">
                    {% if estoque.ativo %}
                    <span class="badge badge-success">Ativo</span>
                    {% else %}
                    <span class="badge badge-danger">Inativo</span>
                    {% endif %}
                </td>
                <td data-label="Acoes" class="actions-cell">
                    <a href="{{ url_for('listar_enderecos_estoque', estoque_id=estoque.id) }}" class="btn-small btn-info">Enderecos</a>
                    <a href="{{ url_for('editar_estoque', estoque_id=estoque.id) }}" class="btn-small btn-warning">Editar</a>
                    <form method="POST" action="{{ url_for('deletar_estoque', estoque_id=estoque.id) }}" class="inline-form" data-confirm-message="Excluir estoque {{ estoque.nome }}?">
                        {{ csrf_input|safe }}
                        <button type="submit" class="btn-small btn-danger">Excluir</button>
                    </form>
                </td>
            </tr>
            {% else %}
            <tr>
                <td colspan="5" class="text-center">Nenhum estoque cadastrado.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
```

---

### Arquivo: `templates\estoque\estoques\novo_estoque.html`

```html
{% extends "base.html" %}

{% block title %}Novo Estoque - SystemLR{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Novo Estoque</h1>
</div>

<div class="form-container">
    <form method="POST" class="form">
        {{ csrf_input|safe }}
        <div class="form-group">
            <label for="nome">Nome *</label>
            <input type="text" id="nome" name="nome" class="input-text" required maxlength="120" placeholder="Ex: CD Principal">
        </div>

        <div class="form-group">
            <label for="descricao">Descricao</label>
            <input type="text" id="descricao" name="descricao" class="input-text" maxlength="255" placeholder="Descricao opcional do estoque">
        </div>

        <div class="form-group">
            <label class="checkbox-inline">
                <input type="checkbox" name="ativo" checked>
                Estoque ativo
            </label>
        </div>

        <div class="form-actions">
            <button type="submit" class="btn btn-primary">Salvar Estoque</button>
            <a href="{{ url_for('listar_estoques') }}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>
{% endblock %}
```

---

### Arquivo: `templates\estoque\fornecedores\detalhes_fornecedor.html`

```html
{% extends "base.html" %}

{% block title %}Detalhes do Fornecedor - SystemLR{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Detalhes do Fornecedor</h1>
    <a href="{{ url_for('listar_fornecedores') }}" class="btn btn-secondary">Voltar</a>
</div>

<div class="form-container">
    <div class="form">
        <div class="form-row">
            <div class="form-group">
                <label>Nome / Razao Social</label>
                <div>{{ fornecedor.nome }}</div>
            </div>
            <div class="form-group">
                <label>CNPJ ou CPF</label>
                <div>{{ fornecedor.documento or '-' }}</div>
            </div>
        </div>

        <div class="form-row">
            <div class="form-group">
                <label>Contato</label>
                <div>{{ fornecedor.contato or '-' }}</div>
            </div>
            <div class="form-group">
                <label>Telefone</label>
                <div>{{ fornecedor.telefone or '-' }}</div>
            </div>
            <div class="form-group">
                <label>Email</label>
                <div>{{ fornecedor.email or '-' }}</div>
            </div>
        </div>

        <div class="form-row">
            <div class="form-group">
                <label>Endereco</label>
                <div>
                    {% set endereco = [fornecedor.endereco_rua, fornecedor.endereco_numero, fornecedor.endereco_bairro, fornecedor.endereco_cidade] | select | list %}
                    {{ endereco | join(', ') if endereco else '-' }}
                </div>
            </div>
            <div class="form-group">
                <label>Status</label>
                <div>
                    {% if fornecedor.ativo %}
                    <span class="badge badge-success">Ativo</span>
                    {% else %}
                    <span class="badge badge-danger">Inativo</span>
                    {% endif %}
                </div>
            </div>
        </div>

        <div class="form-group">
            <label>Tipo de produtos que fornece</label>
            <div>{{ fornecedor.tipo_produtos_fornece or '-' }}</div>
        </div>

        <div class="form-group">
            <label>Observacoes gerais</label>
            <div>{{ fornecedor.observacoes_gerais or '-' }}</div>
        </div>
    </div>
</div>

<div class="table-responsive table-scroll-sticky">
    <h3>Recebimentos recentes</h3>
    <table class="table">
        <thead>
            <tr>
                <th>ID</th>
                <th>Nota</th>
                <th>Status</th>
                <th>Criado em</th>
            </tr>
        </thead>
        <tbody>
            {% for recebimento in recebimentos %}
            <tr>
                <td data-label="ID">{{ recebimento.id }}</td>
                <td data-label="Nota">{{ recebimento.info_nota or '-' }}</td>
                <td data-label="Status">{{ recebimento.status }}</td>
                <td data-label="Criado em">{{ recebimento.criado_em.strftime('%d/%m/%Y %H:%M') if recebimento.criado_em else '-' }}</td>
            </tr>
            {% else %}
            <tr>
                <td colspan="4" class="text-center">Nenhum recebimento encontrado</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>

<div class="table-responsive table-scroll-sticky">
    <h3>Movimentacoes recentes</h3>
    <table class="table">
        <thead>
            <tr>
                <th>ID</th>
                <th>Produto</th>
                <th>Tipo</th>
                <th>Quantidade</th>
                <th>Data</th>
            </tr>
        </thead>
        <tbody>
            {% for mov in movimentacoes %}
            <tr>
                <td data-label="ID">{{ mov.id }}</td>
                <td data-label="Produto">{{ mov.produto.nome if mov.produto else '-' }}</td>
                <td data-label="Tipo">{{ mov.tipo }}</td>
                <td data-label="Quantidade">{{ mov.quantidade }}</td>
                <td data-label="Data">{{ mov.criado_em.strftime('%d/%m/%Y %H:%M') if mov.criado_em else '-' }}</td>
            </tr>
            {% else %}
            <tr>
                <td colspan="5" class="text-center">Nenhuma movimentacao encontrada</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
```

---

### Arquivo: `templates\estoque\fornecedores\editar_fornecedor.html`

```html
{% extends "base.html" %}

{% block title %}Editar Fornecedor - SystemLR{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Editar Fornecedor</h1>
</div>

<div class="form-container">
    <form method="POST" class="form">
        {{ csrf_input|safe }}
        <div class="form-group">
            <label for="nome">Nome / Razao Social *</label>
            <input type="text" id="nome" name="nome" required class="input-text" value="{{ fornecedor.nome }}">
        </div>

        <div class="form-group">
            <label for="documento">CNPJ ou CPF</label>
            <input type="text" id="documento" name="documento" class="input-text" value="{{ fornecedor.documento or '' }}">
        </div>

        <div class="form-group">
            <label for="contato">Contato</label>
            <input type="text" id="contato" name="contato" class="input-text" value="{{ fornecedor.contato or '' }}">
        </div>

        <div class="form-row">
            <div class="form-group">
                <label for="telefone">Telefone</label>
                <input type="text" id="telefone" name="telefone" class="input-text" value="{{ fornecedor.telefone or '' }}">
            </div>

            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" id="email" name="email" class="input-text" value="{{ fornecedor.email or '' }}">
            </div>
        </div>

        <div class="form-row">
            <div class="form-group">
                <label for="endereco_rua">Endereco - Rua</label>
                <input type="text" id="endereco_rua" name="endereco_rua" class="input-text" value="{{ fornecedor.endereco_rua or '' }}">
            </div>
            <div class="form-group">
                <label for="endereco_numero">Numero</label>
                <input type="text" id="endereco_numero" name="endereco_numero" class="input-text" value="{{ fornecedor.endereco_numero or '' }}">
            </div>
        </div>

        <div class="form-row">
            <div class="form-group">
                <label for="endereco_bairro">Bairro</label>
                <input type="text" id="endereco_bairro" name="endereco_bairro" class="input-text" value="{{ fornecedor.endereco_bairro or '' }}">
            </div>
            <div class="form-group">
                <label for="endereco_cidade">Cidade</label>
                <input type="text" id="endereco_cidade" name="endereco_cidade" class="input-text" value="{{ fornecedor.endereco_cidade or '' }}">
            </div>
        </div>

        <div class="form-group">
            <label for="tipo_produtos_fornece">Tipo de produtos que fornece</label>
            <input type="text" id="tipo_produtos_fornece" name="tipo_produtos_fornece" class="input-text" value="{{ fornecedor.tipo_produtos_fornece or '' }}">
        </div>

        <div class="form-group">
            <label for="observacoes_gerais">Observacoes gerais</label>
            <textarea id="observacoes_gerais" name="observacoes_gerais" class="input-textarea" rows="4">{{ fornecedor.observacoes_gerais or '' }}</textarea>
        </div>

        <div class="form-group">
            <label>
                <input type="checkbox" name="ativo" {% if fornecedor.ativo %}checked{% endif %}>
                Fornecedor ativo
            </label>
        </div>

        <div class="form-actions">
            <button type="submit" class="btn btn-primary">Salvar alteracoes</button>
            <a href="{{ url_for('listar_fornecedores') }}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>
{% endblock %}
```

---

### Arquivo: `templates\estoque\fornecedores\fornecedores.html`

```html
﻿{% extends "base.html" %}

{% block title %}Fornecedores - SystemLR{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Fornecedores</h1>
    <a href="{{ url_for('novo_fornecedor') }}" class="btn btn-primary">Novo Fornecedor</a>
</div>

<div class="filters-section">
    <form method="GET" class="filters-form">
        <div class="filter-group">
            <label for="busca">Busca</label>
            <input type="text" id="busca" name="busca" class="input-search" value="{{ filtros.busca if filtros else '' }}" placeholder="Nome, CNPJ/CPF, contato, telefone ou email">
        </div>
        <div class="filter-group">
            <label for="status">Status</label>
            <select id="status" name="status" class="input-select">
                <option value="" {% if not filtros or not filtros.status %}selected{% endif %}>Todos</option>
                <option value="ativo" {% if filtros and filtros.status == 'ativo' %}selected{% endif %}>Ativos</option>
                <option value="inativo" {% if filtros and filtros.status == 'inativo' %}selected{% endif %}>Inativos</option>
            </select>
        </div>
        <div class="form-actions">
            <button type="submit" class="btn btn-primary">Filtrar</button>
            <a href="{{ url_for('listar_fornecedores') }}" class="btn btn-secondary">Limpar</a>
        </div>
    </form>
</div>

<div class="table-responsive table-scroll-sticky">
    <table class="table">
        <thead>
            <tr>
                <th>Nome</th>
                <th>CNPJ/CPF</th>
                <th>Contato</th>
                <th>Telefone</th>
                <th>Email</th>
                <th>Status</th>
                <th>Acoes</th>
            </tr>
        </thead>
        <tbody>
            {% for fornecedor in fornecedores %}
            <tr>
                <td data-label="Nome">{{ fornecedor.nome }}</td>
                <td data-label="CNPJ/CPF">{{ fornecedor.documento or '-' }}</td>
                <td data-label="Contato">{{ fornecedor.contato or '-' }}</td>
                <td data-label="Telefone">{{ fornecedor.telefone or '-' }}</td>
                <td data-label="Email">{{ fornecedor.email or '-' }}</td>
                <td data-label="Status">
                    {% if fornecedor.ativo %}
                    <span class="badge badge-success">Ativo</span>
                    {% else %}
                    <span class="badge badge-danger">Inativo</span>
                    {% endif %}
                </td>
                <td data-label="Acoes" class="actions-cell">
                    <a href="{{ url_for('detalhes_fornecedor', fornecedor_id=fornecedor.id) }}" class="btn-small btn-secondary">Detalhes</a>
                    <a href="{{ url_for('editar_fornecedor', fornecedor_id=fornecedor.id) }}" class="btn-small btn-warning">Editar</a>
                    <form method="POST" action="{{ url_for('deletar_fornecedor', fornecedor_id=fornecedor.id) }}" class="inline-form" data-confirm-message="Tem certeza que deseja remover este fornecedor?">
                        {{ csrf_input|safe }}
                        <button type="submit" class="btn-small btn-danger">Excluir</button>
                    </form>
                </td>
            </tr>
            {% else %}
            <tr>
                <td colspan="7" class="text-center">Nenhum fornecedor cadastrado</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>

{% if pagination and pagination.pages > 1 %}
<div class="pagination">
    {% set params = query_params.copy() if query_params else {} %}
    {% if pagination.has_prev %}
        {% set params_prev = params.copy() %}
        {% set _ = params_prev.update({'page': pagination.prev_num, 'per_page': per_page}) %}
        <a class="btn btn-outline-secondary" href="{{ url_for('listar_fornecedores', **params_prev) }}">Anterior</a>
    {% else %}
        <span class="btn btn-outline-secondary disabled">Anterior</span>
    {% endif %}

    <span class="pagination-info">Pagina {{ pagination.page }} de {{ pagination.pages }}</span>

    {% if pagination.has_next %}
        {% set params_next = params.copy() %}
        {% set _ = params_next.update({'page': pagination.next_num, 'per_page': per_page}) %}
        <a class="btn btn-outline-secondary" href="{{ url_for('listar_fornecedores', **params_next) }}">Proxima</a>
    {% else %}
        <span class="btn btn-outline-secondary disabled">Proxima</span>
    {% endif %}
</div>
{% endif %}
{% endblock %}

```

---

### Arquivo: `templates\estoque\fornecedores\novo_fornecedor.html`

```html
{% extends "base.html" %}

{% block title %}Novo Fornecedor - SystemLR{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Novo Fornecedor</h1>
</div>

<div class="form-container">
    <form method="POST" class="form">
        {{ csrf_input|safe }}
        <div class="form-group">
            <label for="nome">Nome / Razao Social *</label>
            <input type="text" id="nome" name="nome" required class="input-text" placeholder="Nome da empresa ou pessoa fornecedora">
        </div>

        <div class="form-group">
            <label for="documento">CNPJ ou CPF</label>
            <input type="text" id="documento" name="documento" class="input-text" placeholder="00.000.000/0000-00 ou 000.000.000-00">
        </div>

        <div class="form-group">
            <label for="contato">Contato</label>
            <input type="text" id="contato" name="contato" class="input-text" placeholder="Nome da pessoa de contato">
        </div>

        <div class="form-row">
            <div class="form-group">
                <label for="telefone">Telefone</label>
                <input type="text" id="telefone" name="telefone" class="input-text" placeholder="(00) 00000-0000">
            </div>

            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" id="email" name="email" class="input-text" placeholder="contato@fornecedor.com">
            </div>
        </div>

        <div class="form-row">
            <div class="form-group">
                <label for="endereco_rua">Endereco - Rua</label>
                <input type="text" id="endereco_rua" name="endereco_rua" class="input-text" placeholder="Rua, avenida, travessa...">
            </div>
            <div class="form-group">
                <label for="endereco_numero">Numero</label>
                <input type="text" id="endereco_numero" name="endereco_numero" class="input-text" placeholder="Numero">
            </div>
        </div>

        <div class="form-row">
            <div class="form-group">
                <label for="endereco_bairro">Bairro</label>
                <input type="text" id="endereco_bairro" name="endereco_bairro" class="input-text" placeholder="Bairro">
            </div>
            <div class="form-group">
                <label for="endereco_cidade">Cidade</label>
                <input type="text" id="endereco_cidade" name="endereco_cidade" class="input-text" placeholder="Cidade">
            </div>
        </div>

        <div class="form-group">
            <label for="tipo_produtos_fornece">Tipo de produtos que fornece</label>
            <input type="text" id="tipo_produtos_fornece" name="tipo_produtos_fornece" class="input-text" placeholder="Ex: graos, bebidas, limpeza, frios...">
        </div>

        <div class="form-group">
            <label for="observacoes_gerais">Observacoes gerais</label>
            <textarea id="observacoes_gerais" name="observacoes_gerais" class="input-textarea" rows="4" placeholder="Pontualidade, restricoes, qualidade, condicoes comerciais, etc."></textarea>
        </div>

        <div class="form-group">
            <label>
                <input type="checkbox" name="ativo" checked>
                Fornecedor ativo
            </label>
        </div>

        <div class="form-actions">
            <button type="submit" class="btn btn-primary">Salvar fornecedor</button>
            <a href="{{ url_for('listar_fornecedores') }}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>
{% endblock %}
```

---

### Arquivo: `templates\estoque\movimentacoes\movimentacao_rapida.html`

```html
﻿{% extends "base.html" %}

{% block title %}Movimentacao Rapida - SystemLR{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Movimentacao Rapida</h1>
    <a href="{{ url_for('listar_movimentacoes') }}" class="btn btn-secondary">Voltar</a>
</div>

<div class="section">
    <h2>{{ produto.nome }}</h2>

    <div class="info-cards-row">
        <div class="info-card">
            <h3>Codigo</h3>
            <p class="value">{{ produto.codigo }}</p>
        </div>
        <div class="info-card">
            <h3>Categoria</h3>
            <p class="value">{{ produto.categoria.nome }}</p>
        </div>
        <div class="info-card">
            <h3>Preco Venda</h3>
            <p class="value">R$ {{ "%.2f"|format(produto.preco_venda) }}</p>
        </div>
        <div class="info-card">
            <h3>Estoque Atual</h3>
            <p class="value">{{ produto.quantidade_estoque }}</p>
        </div>
    </div>
</div>

<div class="section">
    <h2>Registrar Movimentacao</h2>

    <form method="POST" class="form">
        <input type="hidden" name="produto_id" value="{{ produto.id }}">

        <div class="form-row">
            <div class="form-group">
                <label for="tipo">Tipo de Movimentacao *</label>
                <select id="tipo" name="tipo" required class="input-select">
                    <option value="entrada">Entrada</option>
                    <option value="saida">Saida</option>
                </select>
            </div>

            <div class="form-group">
                <label for="quantidade">Quantidade *</label>
                <input type="number" id="quantidade" name="quantidade" required min="1" placeholder="0" class="input-text" autofocus>
            </div>
        </div>

        <div class="form-group" id="fornecedor-wrapper" style="display:block;">
            <label for="fornecedor_id">Fornecedor (opcional no recebimento)</label>
            <select id="fornecedor_id" name="fornecedor_id" class="input-select">
                <option value="">Sem fornecedor</option>
                {% for fornecedor in fornecedores %}
                <option value="{{ fornecedor.id }}">{{ fornecedor.nome }}</option>
                {% endfor %}
            </select>
        </div>

        <div class="form-group" id="valor-compra-wrapper" style="display:none;">
            <label for="valor_compra">Valor de compra (R$)</label>
            <input type="number" step="0.01" id="valor_compra" name="valor_compra" placeholder="0.00" class="input-text">
        </div>

        <div class="form-group" id="nota-wrapper" style="display:none;">
            <label for="info_nota">Informações da nota</label>
            <input type="text" id="info_nota" name="info_nota" placeholder="Número, série, observações..." class="input-text">
        </div>

        <div class="form-group">
            <label for="motivo">Motivo</label>
            <input type="text" id="motivo" name="motivo" placeholder="Ex: Venda, Compra, Devolucao..." class="input-text">
        </div>

        <div class="form-group">
            <label for="observacoes">Observacoes</label>
            <textarea id="observacoes" name="observacoes" placeholder="Observacoes adicionais..." class="input-textarea" rows="3"></textarea>
        </div>

        <div class="form-actions">
            <button type="submit" class="btn btn-primary">Registrar movimentacao</button>
            <a href="{{ url_for('nova_movimentacao') }}" class="btn btn-success">Nova movimentacao</a>
            <a href="{{ url_for('listar_movimentacoes') }}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>
{% endblock %}

{% block extra_js %}
<script>
document.addEventListener('DOMContentLoaded', function () {
    const tipo = document.getElementById('tipo');
    const fornecedorWrapper = document.getElementById('fornecedor-wrapper');
    const fornecedorSelect = document.getElementById('fornecedor_id');

    const valorCompraWrapper = document.getElementById('valor-compra-wrapper');
    const notaWrapper = document.getElementById('nota-wrapper');

    function atualizarFornecedor() {
        const entrada = tipo.value === 'entrada';
        fornecedorWrapper.style.display = entrada ? 'block' : 'none';
        valorCompraWrapper.style.display = entrada ? 'block' : 'none';
        notaWrapper.style.display = entrada ? 'block' : 'none';
        if (!entrada) {
            fornecedorSelect.value = '';
            document.getElementById('valor_compra').value = '';
            document.getElementById('info_nota').value = '';
        }
    }

    tipo.addEventListener('change', atualizarFornecedor);
    atualizarFornecedor();
});
</script>
{% endblock %}
```

---

### Arquivo: `templates\estoque\movimentacoes\movimentacoes.html`

```html
﻿{% extends "base.html" %}

{% block title %}Movimentacoes - SystemLR{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Movimentacoes</h1>
    <div class="header-actions">
        <a href="{{ url_for('listar_recebimentos_fornecedor') }}" class="btn btn-secondary">Recebimentos</a>
        <a href="{{ url_for('nova_movimentacao') }}" class="btn btn-primary">Nova Movimentacao</a>
    </div>
</div>

<div class="filters-section">
    <form method="GET" class="filters-form">
        <div class="filter-group">
            <input type="text" name="busca" class="input-search" value="{{ busca or '' }}" placeholder="Buscar por codigo/nome do produto, nota, motivo ou fornecedor">
        </div>
        <div class="filter-group">
            <select name="produto_id" class="input-select">
                <option value="">Todos os produtos</option>
                {% for prod in produtos %}
                <option value="{{ prod.id }}" {% if produto_selecionado == prod.id %}selected{% endif %}>{{ prod.codigo }} - {{ prod.nome }}</option>
                {% endfor %}
            </select>
        </div>
        <div class="filter-group">
            <select name="fornecedor_id" class="input-select">
                <option value="">Todos os fornecedores</option>
                {% for fornecedor in fornecedores %}
                <option value="{{ fornecedor.id }}" {% if fornecedor_selecionado == fornecedor.id %}selected{% endif %}>{{ fornecedor.nome }}</option>
                {% endfor %}
            </select>
        </div>
        <div class="filter-group">
            <select name="status" class="input-select">
                <option value="">Todos os status</option>
                <option value="entrada" {% if status_selecionado == 'entrada' %}selected{% endif %}>Entrada</option>
                <option value="saida" {% if status_selecionado == 'saida' %}selected{% endif %}>Saida</option>
                <option value="transferencia" {% if status_selecionado == 'transferencia' %}selected{% endif %}>Transferencia</option>
            </select>
        </div>
        <div class="filter-group">
            <input type="date" name="data_inicio" class="input-search" value="{{ data_inicio or '' }}" title="Data inicial">
        </div>
        <div class="filter-group">
            <input type="date" name="data_fim" class="input-search" value="{{ data_fim or '' }}" title="Data final">
        </div>
        <button type="submit" class="btn btn-secondary">Filtrar</button>
        <a href="{{ url_for('listar_movimentacoes') }}" class="btn btn-secondary">Limpar</a>
    </form>
</div>

<div class="table-responsive table-scroll-sticky">
    <table class="table">
        <thead>
            <tr>
                <th>Codigo</th>
                <th>Produto</th>
                <th>Movimentacao</th>
                <th>Quantidade</th>
                <th>Status</th>
                <th>Data</th>
            </tr>
        </thead>
        <tbody>
                {% for mov in movimentacoes %}
            <tr>
                <td data-label="Codigo"><code>{{ mov.produto.codigo if mov.produto else '-' }}</code></td>
                <td data-label="Produto">
                    <div class="product-name-cell">
                        {% if mov.produto and mov.produto.imagem_path %}
                        <img src="{{ url_for('static', filename=mov.produto.imagem_path) }}" alt="{{ mov.produto.nome }}" class="product-thumb product-thumb-sm">
                        {% endif %}
                        <a href="{{ url_for('visualizar_produto', produto_id=mov.produto_id) }}">{{ mov.produto.nome if mov.produto else 'Produto removido' }}</a>
                    </div>
                </td>
                <td data-label="Tipo">
                    <span class="badge {% if mov.tipo == 'entrada' %}badge-success{% else %}badge-danger{% endif %}">
                        {{ mov.tipo|capitalize }}
                    </span>
                </td>
                <td data-label="Quantidade">{{ mov.quantidade }}</td>
                <td data-label="Status">
                    <span class="badge badge-info">Registrada</span>
                </td>
                <td data-label="Data">{{ mov.criado_em.strftime('%d/%m/%Y %H:%M') }}</td>
            </tr>
            {% else %}
            <tr>
                <td colspan="6" class="text-center">Nenhuma movimentacao encontrada</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>

{% if pagination and pagination.pages > 1 %}
<div class="pagination">
    {% set params = query_params.copy() if query_params else {} %}
    {% if pagination.has_prev %}
        {% set params_prev = params.copy() %}
        {% set _ = params_prev.update({'page': pagination.prev_num, 'per_page': per_page}) %}
        <a class="btn btn-outline-secondary" href="{{ url_for('listar_movimentacoes', **params_prev) }}">Anterior</a>
    {% else %}
        <span class="btn btn-outline-secondary disabled">Anterior</span>
    {% endif %}

    <span class="pagination-info">Pagina {{ pagination.page }} de {{ pagination.pages }}</span>

    {% if pagination.has_next %}
        {% set params_next = params.copy() %}
        {% set _ = params_next.update({'page': pagination.next_num, 'per_page': per_page}) %}
        <a class="btn btn-outline-secondary" href="{{ url_for('listar_movimentacoes', **params_next) }}">Proxima</a>
    {% else %}
        <span class="btn btn-outline-secondary disabled">Proxima</span>
    {% endif %}
</div>
{% endif %}
{% endblock %}
```

---

### Arquivo: `templates\estoque\movimentacoes\nova_movimentacao.html`

```html
﻿{% extends "base.html" %}

{% block title %}Nova Movimentacao - SystemLR{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Nova Movimentacao</h1>
    <div class="header-actions">
        <a href="{{ url_for('novo_recebimento_fornecedor') }}" class="btn btn-secondary">Recebimento do fornecedor</a>
    </div>
</div>

<div class="form-container">
    <form method="POST" class="form">
        {{ csrf_input|safe }}
        <div class="form-group">
            <label for="produto_id">Produto *</label>
            <select id="produto_id" name="produto_id" required class="input-select">
                <option value="">Selecione um produto</option>
                {% for prod in produtos %}
                <option value="{{ prod.id }}">{{ prod.codigo }} - {{ prod.nome }} (Estoque: {{ prod.quantidade_estoque }})</option>
                {% endfor %}
            </select>
        </div>

        <div class="form-group">
            <label for="tipo">Tipo de Movimentacao *</label>
            <select id="tipo" name="tipo" required class="input-select">
                <option value="">Selecione um tipo</option>
                <option value="entrada">Entrada</option>
                <option value="saida">Saida</option>
            </select>
        </div>

        <div class="form-group" id="fornecedor-wrapper" style="display:none;">
            <label for="fornecedor_id">Fornecedor (opcional no recebimento)</label>
            <select id="fornecedor_id" name="fornecedor_id" class="input-select">
                <option value="">Sem fornecedor</option>
                {% for fornecedor in fornecedores %}
                <option value="{{ fornecedor.id }}">{{ fornecedor.nome }}</option>
                {% endfor %}
            </select>
        </div>

        <div class="form-group" id="recebimento-fornecedor-wrapper" style="display:none;">
            <label class="checkbox-inline">
                <input type="checkbox" id="recebimento_fornecedor" name="recebimento_fornecedor">
                Recebimento de produtos do fornecedor
            </label>
        </div>

        <div class="form-group" id="valor-compra-wrapper" style="display:none;">
            <label for="valor_compra">Valor de compra (R$)</label>
            <input type="number" step="0.01" id="valor_compra" name="valor_compra" placeholder="0.00" class="input-text">
        </div>

        <div class="form-group" id="nota-wrapper" style="display:none;">
            <label for="info_nota">Informações da nota</label>
            <input type="text" id="info_nota" name="info_nota" placeholder="Número, série, observações..." class="input-text">
        </div>

        <div class="form-group">
            <label for="quantidade">Quantidade *</label>
            <input type="number" id="quantidade" name="quantidade" required min="1" placeholder="0" class="input-text">
        </div>

        <div class="form-group">
            <label for="motivo">Motivo</label>
            <input type="text" id="motivo" name="motivo" placeholder="Ex: Venda, Compra, Devolucao, Perda..." class="input-text">
        </div>

        <div class="form-group">
            <label for="observacoes">Observacoes</label>
            <textarea id="observacoes" name="observacoes" placeholder="Observacoes adicionais..." class="input-textarea" rows="4"></textarea>
        </div>

        <div class="form-actions">
            <button type="submit" class="btn btn-primary">Salvar movimentacao</button>
            <a href="{{ url_for('listar_movimentacoes') }}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>
{% endblock %}

{% block extra_js %}
<script>
document.addEventListener('DOMContentLoaded', function () {
    const tipo = document.getElementById('tipo');
    const recebimentoWrapper = document.getElementById('recebimento-fornecedor-wrapper');
    const recebimentoCheckbox = document.getElementById('recebimento_fornecedor');
    const fornecedorWrapper = document.getElementById('fornecedor-wrapper');
    const fornecedorSelect = document.getElementById('fornecedor_id');
    const valorCompraWrapper = document.getElementById('valor-compra-wrapper');
    const notaWrapper = document.getElementById('nota-wrapper');
    const valorCompraInput = document.getElementById('valor_compra');
    const notaInput = document.getElementById('info_nota');
    const motivoInput = document.getElementById('motivo');

    function atualizarObrigatoriedadeFornecedor() {
        const exigirFornecedor = tipo.value === 'entrada' && recebimentoCheckbox.checked;
        fornecedorSelect.required = exigirFornecedor;
    }

    function atualizarFornecedor() {
        const entrada = tipo.value === 'entrada';
        recebimentoWrapper.style.display = entrada ? 'block' : 'none';
        fornecedorWrapper.style.display = entrada ? 'block' : 'none';
        valorCompraWrapper.style.display = entrada ? 'block' : 'none';
        notaWrapper.style.display = entrada ? 'block' : 'none';
        if (!entrada) {
            recebimentoCheckbox.checked = false;
            fornecedorSelect.value = '';
            valorCompraInput.value = '';
            notaInput.value = '';
        }
        atualizarObrigatoriedadeFornecedor();
    }

    tipo.addEventListener('change', atualizarFornecedor);
    recebimentoCheckbox.addEventListener('change', function () {
        atualizarObrigatoriedadeFornecedor();
        if (this.checked && !motivoInput.value.trim()) {
            motivoInput.value = 'recebimento_fornecedor';
        }
    });
    atualizarFornecedor();
});
</script>
{% endblock %}
```

---

### Arquivo: `templates\estoque\produtos\editar_produto.html`

```html
{% extends "base.html" %}

{% block title %}Editar Produto - SystemLR{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Editar Produto</h1>
</div>

<div class="form-container">
    <form method="POST" enctype="multipart/form-data" class="form">
        {{ csrf_input|safe }}
        <div class="form-group">
            <label for="codigo">Codigo</label>
            <input type="text" id="codigo" value="{{ produto.codigo }}" disabled class="input-text">
        </div>

        <div class="form-group">
            <label for="nome">Nome do Produto *</label>
            <input type="text" id="nome" name="nome" required value="{{ produto.nome }}" class="input-text">
        </div>

        <div class="form-group">
            <label for="descricao">Descricao</label>
            <textarea id="descricao" name="descricao" class="input-textarea" rows="4">{{ produto.descricao or '' }}</textarea>
        </div>

        <div class="form-group">
            <label for="imagem">Imagem do Produto</label>
            <input type="file" id="imagem" name="imagem" accept=".png,.jpg,.jpeg,.webp,.gif" class="input-text">
            {% if produto.imagem_path %}
            <div class="product-image-preview">
                <img src="{{ url_for('static', filename=produto.imagem_path) }}" alt="{{ produto.nome }}">
                <label class="checkbox-inline">
                    <input type="checkbox" name="remover_imagem">
                    Remover imagem atual
                </label>
            </div>
            {% endif %}
        </div>

        <div class="form-group">
            <label for="categoria_id">Categoria *</label>
            <select id="categoria_id" name="categoria_id" required class="input-select">
                {% for cat in categorias %}
                <option value="{{ cat.id }}" {% if produto.categoria_id == cat.id %}selected{% endif %}>
                    {{ cat.nome }}
                </option>
                {% endfor %}
            </select>
        </div>

        <div class="form-group">
            <label for="fornecedor_id">Fornecedor *</label>
            <select id="fornecedor_id" name="fornecedor_id" required class="input-select">
                <option value="">Selecione um fornecedor</option>
                {% for fornecedor in fornecedores %}
                <option value="{{ fornecedor.id }}" {% if produto.fornecedor_id == fornecedor.id %}selected{% endif %}>
                    {{ fornecedor.nome }}
                </option>
                {% endfor %}
            </select>
        </div>

        <div class="form-group">
            <label for="endereco_id">Endereco de Estoque</label>
            <select id="endereco_id" name="endereco_id" class="input-select">
                <option value="">Nao definido</option>
                {% for endereco in enderecos %}
                <option value="{{ endereco.id }}" {% if produto.endereco_id == endereco.id %}selected{% endif %}>
                    {{ endereco.nome }}
                </option>
                {% endfor %}
            </select>
        </div>

        <div class="form-row">
            <div class="form-group">
                <label for="preco_custo">Preco de Custo *</label>
                <input type="number" id="preco_custo" name="preco_custo" step="0.01" required value="{{ produto.preco_custo }}" class="input-text">
            </div>

            <div class="form-group">
                <label for="preco_venda">Preco de Venda *</label>
                <input type="number" id="preco_venda" name="preco_venda" step="0.01" required value="{{ produto.preco_venda }}" class="input-text">
            </div>
        </div>

        <div class="form-row">
            <div class="form-group">
                <label for="quantidade_estoque">Quantidade Atual</label>
                <input type="number" id="quantidade_estoque" value="{{ produto.quantidade_estoque }}" disabled class="input-text">
            </div>

            <div class="form-group">
                <label for="quantidade_minima">Quantidade Minima</label>
                <input type="number" id="quantidade_minima" name="quantidade_minima" value="{{ produto.quantidade_minima }}" class="input-text">
            </div>
        </div>

        <div class="info-box">
            <p><strong>Lucro Unitario:</strong> R$ {{ "%.2f"|format(produto.lucro_unitario) }}</p>
            <p><strong>Margem de Lucro:</strong> {{ "%.2f"|format(produto.margem_lucro) }}%</p>
        </div>

        <div class="form-actions">
            <button type="submit" class="btn btn-primary">Salvar Alteracoes</button>
            <a href="{{ url_for('visualizar_produto', produto_id=produto.id) }}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>
{% endblock %}
```

---

### Arquivo: `templates\estoque\produtos\novo_produto.html`

```html
﻿{% extends "base.html" %}

{% block title %}Novo Produto - SystemLR{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Novo Produto</h1>
</div>

<div class="form-container">
    <form method="POST" enctype="multipart/form-data" class="form">
        {{ csrf_input|safe }}
        <div class="form-group">
            <label for="codigo">Codigo *</label>
            <div class="barcode-input-group">
                <input type="text" id="codigo" name="codigo" required placeholder="Ex: PROD001" class="input-text">
                <button type="button" class="btn btn-secondary barcode-btn js-open-barcode-scanner" data-barcode-target="codigo">Camera</button>
            </div>
            <small id="codigoErro" class="text-danger"></small>
        </div>

        <div class="form-group">
            <label for="nome">Nome do Produto *</label>
            <input type="text" id="nome" name="nome" required placeholder="Ex: Refrigerante 2L" class="input-text">
        </div>

        <div class="form-group">
            <label for="descricao">Descricao</label>
            <textarea id="descricao" name="descricao" placeholder="Descrever o produto..." class="input-textarea" rows="4"></textarea>
        </div>

        <div class="form-group">
            <label for="imagem">Imagem do Produto</label>
            <input type="file" id="imagem" name="imagem" accept=".png,.jpg,.jpeg,.webp,.gif" class="input-text">
        </div>

        <div class="form-group">
            <label for="categoria_id">Categoria *</label>
            <select id="categoria_id" name="categoria_id" required class="input-select">
                <option value="">Selecione uma categoria</option>
                {% for cat in categorias %}
                <option value="{{ cat.id }}">{{ cat.nome }}</option>
                {% endfor %}
            </select>
        </div>

        <div class="form-group">
            <label for="fornecedor_id">Fornecedor *</label>
            <select id="fornecedor_id" name="fornecedor_id" required class="input-select">
                <option value="">Selecione um fornecedor</option>
                {% for fornecedor in fornecedores %}
                <option value="{{ fornecedor.id }}">{{ fornecedor.nome }}</option>
                {% endfor %}
            </select>
        </div>

        <div class="form-group">
            <label for="endereco_id">Endereco de Estoque</label>
            <select id="endereco_id" name="endereco_id" class="input-select">
                <option value="">Nao definido</option>
                {% for endereco in enderecos %}
                <option value="{{ endereco.id }}">{{ endereco.nome }}</option>
                {% endfor %}
            </select>
        </div>

        <div class="form-row">
            <div class="form-group">
                <label for="preco_custo">Preco de Custo *</label>
                <input type="number" id="preco_custo" name="preco_custo" step="0.01" required placeholder="0.00" class="input-text">
            </div>

            <div class="form-group">
                <label for="preco_venda">Preco de Venda *</label>
                <input type="number" id="preco_venda" name="preco_venda" step="0.01" required placeholder="0.00" class="input-text">
            </div>
        </div>

        <div class="form-row">
            <div class="form-group">
                <label for="status_disponibilidade">Disponibilidade operacional</label>
                <select id="status_disponibilidade" name="status_disponibilidade" class="input-select">
                    {% for chave, label in status_disponibilidade_labels.items() %}
                    <option value="{{ chave }}" {% if chave == 'disponivel_venda' %}selected{% endif %}>{{ label }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="form-group">
                <label for="quantidade_estoque">Quantidade Inicial</label>
                <input type="number" id="quantidade_estoque" name="quantidade_estoque" value="0" placeholder="0" class="input-text">
            </div>

            <div class="form-group">
                <label for="quantidade_minima">Quantidade Minima</label>
                <input type="number" id="quantidade_minima" name="quantidade_minima" value="5" placeholder="5" class="input-text">
            </div>
        </div>

        <div class="form-actions">
            <button type="submit" class="btn btn-primary">Salvar produto</button>
            <a href="{{ url_for('listar_produtos') }}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>

<script>
const codigosExistentes = {{ codigos_existentes|tojson }};
const codigoInput = document.getElementById('codigo');
const submitBtn = document.querySelector('form button[type="submit"]');
const codigoErro = document.getElementById('codigoErro');

function validarCodigoUnico() {
    const valor = (codigoInput.value || '').trim().toUpperCase();
    codigoInput.value = valor;
    const duplicado = valor && codigosExistentes.includes(valor);
    if (duplicado) {
        codigoErro.textContent = 'Codigo já utilizado por outro produto.';
        if (submitBtn) submitBtn.disabled = true;
    } else {
        codigoErro.textContent = '';
        if (submitBtn) submitBtn.disabled = false;
    }
}

codigoInput.addEventListener('input', validarCodigoUnico);
validarCodigoUnico();
</script>
{% endblock %}
```

---

### Arquivo: `templates\estoque\produtos\produtos.html`

```html
﻿{% extends "base.html" %}

{% block title %}Produtos - SystemLR{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Produtos</h1>
    <a href="{{ url_for('novo_produto') }}" class="btn btn-primary">Novo Produto</a>
</div>

<div class="filters-section">
    <form method="GET" class="filters-form">
        <div class="filter-group">
            <div class="barcode-input-group">
                <input type="text" id="busca" name="busca" placeholder="Buscar por nome ou codigo..."
                       value="{{ busca }}" class="input-search">
                <button type="button" class="btn btn-secondary barcode-btn js-open-barcode-scanner" data-barcode-target="busca">Camera</button>
            </div>
        </div>
        <div class="filter-group">
            <select name="categoria_id" class="input-select">
                <option value="">Todas as categorias</option>
                {% for cat in categorias %}
                <option value="{{ cat.id }}" {% if categoria_selecionada == cat.id %}selected{% endif %}>
                    {{ cat.nome }}
                </option>
                {% endfor %}
            </select>
        </div>
        <div class="filter-group">
            <select name="status_disponibilidade" class="input-select">
                <option value="">Todas as disponibilidades</option>
                {% for chave, label in status_disponibilidade_labels.items() %}
                <option value="{{ chave }}" {% if filtros and filtros.status_disponibilidade == chave %}selected{% endif %}>{{ label }}</option>
                {% endfor %}
            </select>
        </div>
        <div class="filter-group">
            <select name="estoque_id" class="input-select">
                <option value="">Todos os estoques</option>
                {% for estoque in estoques %}
                <option value="{{ estoque.id }}" {% if filtros and filtros.estoque_id == estoque.id %}selected{% endif %}>{{ estoque.nome }}</option>
                {% endfor %}
            </select>
        </div>
        <div class="filter-group">
            <select name="endereco_id" class="input-select">
                <option value="">Todos os enderecos</option>
                {% for endereco in enderecos %}
                <option value="{{ endereco.id }}" {% if filtros and filtros.endereco_id == endereco.id %}selected{% endif %}>{{ endereco.nome }}</option>
                {% endfor %}
            </select>
        </div>
        <div class="filter-group">
            <select name="fornecedor_id" class="input-select">
                <option value="">Todos os fornecedores</option>
                {% for fornecedor in fornecedores %}
                <option value="{{ fornecedor.id }}" {% if filtros and filtros.fornecedor_id == fornecedor.id %}selected{% endif %}>{{ fornecedor.nome }}</option>
                {% endfor %}
            </select>
        </div>
        <button type="submit" class="btn btn-secondary">Filtrar</button>
    </form>
</div>

<div class="table-responsive table-scroll-sticky">
    <table class="table">
        <thead>
            <tr>
                <th>Codigo</th>
                <th>Nome</th>
                <th>Categoria</th>
                <th>Fornecedor</th>
                <th>Endereco</th>
                <th>Disponibilidade</th>
                <th>Preco Venda</th>
                <th>Estoque</th>
                <th>Status</th>
                <th>Acoes</th>
            </tr>
        </thead>
        <tbody>
            {% for produto in produtos %}
            <tr class="{% if produto.em_falta %}row-warning{% endif %}">
                <td data-label="Codigo">{{ produto.codigo }}</td>
                <td data-label="Nome">
                    <div class="product-name-cell">
                        {% if produto.imagem_path %}
                        <img src="{{ url_for('static', filename=produto.imagem_path) }}" alt="{{ produto.nome }}" class="product-thumb">
                        {% endif %}
                        <span>{{ produto.nome }}</span>
                    </div>
                </td>
                <td data-label="Categoria">{{ produto.categoria.nome }}</td>
                <td data-label="Fornecedor">{{ produto.fornecedor.nome if produto.fornecedor else '-' }}</td>
                <td data-label="Endereco">{{ produto.endereco.nome if produto.endereco else '-' }}</td>
                <td data-label="Disponibilidade">
                    {% if produto.status_disponibilidade == 'disponivel_venda' %}
                    <span class="badge badge-success">Disponivel para venda</span>
                    {% elif produto.status_disponibilidade == 'somente_ressuprimento' %}
                    <span class="badge badge-warning">Somente ressuprimento</span>
                    {% else %}
                    <span class="badge badge-danger">Indisponivel</span>
                    {% endif %}
                </td>
                <td data-label="Preco">R$ {{ "%.2f"|format(produto.preco_venda) }}</td>
                <td data-label="Estoque">
                    {{ produto.quantidade_estoque }}
                    {% if produto.em_falta %}<span class="icon-warning">!</span>{% endif %}
                </td>
                <td data-label="Status">
                    {% if produto.ativo %}
                        <span class="badge badge-success">Ativo</span>
                    {% else %}
                        <span class="badge badge-danger">Inativo</span>
                    {% endif %}
                </td>
                <td data-label="Acoes" class="actions-cell">
                    <a href="{{ url_for('visualizar_produto', produto_id=produto.id) }}" class="btn-small btn-info">Ver</a>
                    <a href="{{ url_for('editar_produto', produto_id=produto.id) }}" class="btn-small btn-warning">Editar</a>
                    <form method="POST" action="{{ url_for('deletar_produto', produto_id=produto.id) }}" class="inline-form" data-confirm-message="Excluir produto {{ produto.nome }}?">
                        {{ csrf_input|safe }}
                        <button type="submit" class="btn-small btn-danger">Excluir</button>
                    </form>
                </td>
            </tr>
            {% else %}
            <tr>
                <td colspan="10" class="text-center">Nenhum produto encontrado</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>

{% if pagination and pagination.pages > 1 %}
<div class="pagination">
    {% set params = query_params.copy() if query_params else {} %}
    {% if pagination.has_prev %}
        {% set params_prev = params.copy() %}
        {% set _ = params_prev.update({'page': pagination.prev_num, 'per_page': per_page}) %}
        <a class="btn btn-outline-secondary" href="{{ url_for('listar_produtos', **params_prev) }}">Anterior</a>
    {% else %}
        <span class="btn btn-outline-secondary disabled">Anterior</span>
    {% endif %}

    <span class="pagination-info">Pagina {{ pagination.page }} de {{ pagination.pages }}</span>

    {% if pagination.has_next %}
        {% set params_next = params.copy() %}
        {% set _ = params_next.update({'page': pagination.next_num, 'per_page': per_page}) %}
        <a class="btn btn-outline-secondary" href="{{ url_for('listar_produtos', **params_next) }}">Proxima</a>
    {% else %}
        <span class="btn btn-outline-secondary disabled">Proxima</span>
    {% endif %}
</div>
{% endif %}
{% endblock %}

```

---

### Arquivo: `templates\estoque\produtos\visualizar_produto.html`

```html
{% extends "base.html" %}

{% block title %}{{ produto.nome }} - SystemLR{% endblock %}

{% block content %}
<div class="page-header">
    <h1>{{ produto.nome }}</h1>
    <div class="header-actions">
        <a href="{{ url_for('editar_produto', produto_id=produto.id) }}" class="btn btn-warning">Editar</a>
        <a href="{{ url_for('listar_produtos') }}" class="btn btn-secondary">Voltar</a>
    </div>
</div>

{% if produto.imagem_path %}
<div class="section">
    <h2>Imagem do Produto</h2>
    <img src="{{ url_for('static', filename=produto.imagem_path) }}" alt="{{ produto.nome }}" class="product-detail-image">
</div>
{% endif %}

<div class="info-cards-row">
    <div class="info-card">
        <h3>Codigo</h3>
        <p class="value">{{ produto.codigo }}</p>
    </div>
    <div class="info-card">
        <h3>Categoria</h3>
        <p class="value">{{ produto.categoria.nome }}</p>
    </div>
    <div class="info-card">
        <h3>Fornecedor</h3>
        <p class="value">{{ produto.fornecedor.nome if produto.fornecedor else '-' }}</p>
    </div>
    <div class="info-card">
        <h3>Preco de Custo</h3>
        <p class="value">R$ {{ "%.2f"|format(produto.preco_custo) }}</p>
    </div>
    <div class="info-card">
        <h3>Preco de Venda</h3>
        <p class="value">R$ {{ "%.2f"|format(produto.preco_venda) }}</p>
    </div>
</div>

<div class="info-cards-row">
    <div class="info-card {% if produto.em_falta %}card-warning{% endif %}">
        <h3>Estoque Atual</h3>
        <p class="value">{{ produto.quantidade_estoque }}</p>
        {% if produto.em_falta %}
        <p class="alert-text">Abaixo do minimo</p>
        {% endif %}
    </div>
    <div class="info-card">
        <h3>Estoque Minimo</h3>
        <p class="value">{{ produto.quantidade_minima }}</p>
    </div>
    <div class="info-card">
        <h3>Lucro Unitario</h3>
        <p class="value">R$ {{ "%.2f"|format(produto.lucro_unitario) }}</p>
    </div>
    <div class="info-card">
        <h3>Margem de Lucro</h3>
        <p class="value">{{ "%.2f"|format(produto.margem_lucro) }}%</p>
    </div>
</div>

{% if produto.descricao %}
<div class="section">
    <h2>Descricao</h2>
    <p>{{ produto.descricao }}</p>
</div>
{% endif %}

<div class="section">
    <h2>Ultimas Movimentacoes</h2>
    <div class="table-responsive">
        <table class="table">
            <thead>
                <tr>
                    <th>Tipo</th>
                    <th>Quantidade</th>
                    <th>Motivo</th>
                    <th>Data</th>
                </tr>
            </thead>
            <tbody>
                {% for mov in movimentacoes %}
                <tr>
                    <td data-label="Tipo">
                        <span class="badge {% if mov.tipo == 'entrada' %}badge-success{% else %}badge-danger{% endif %}">
                            {% if mov.tipo == 'entrada' %}Entrada{% else %}Saida{% endif %}
                        </span>
                    </td>
                    <td data-label="Quantidade">{{ mov.quantidade }}</td>
                    <td data-label="Motivo">{{ mov.motivo or '-' }}</td>
                    <td data-label="Data">{{ mov.criado_em.strftime('%d/%m/%Y %H:%M') }}</td>
                </tr>
                {% else %}
                <tr>
                    <td colspan="4" class="text-center">Nenhuma movimentacao encontrada</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>

<div class="action-buttons">
    <a href="{{ url_for('editar_produto', produto_id=produto.id) }}" class="btn btn-warning">Editar Produto</a>
    <a href="{{ url_for('listar_produtos') }}" class="btn btn-secondary">Voltar para Produtos</a>
</div>
{% endblock %}
```

---

### Arquivo: `templates\estoque\recebimentos\armazenar_recebimento.html`

```html
{% extends "base.html" %}

{% block title %}Armazenar Recebimento #{{ recebimento.id }} - SystemLR{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Armazenagem (Put-away) - Recebimento #{{ recebimento.id }}</h1>
    <div class="header-actions">
        <a href="{{ url_for('conferir_recebimento_fornecedor', recebimento_id=recebimento.id) }}" class="btn btn-secondary">Voltar para conferencia</a>
    </div>
</div>

<div class="card mb-3">
    <div class="card-body">
        <p><strong>Fornecedor:</strong> {{ recebimento.fornecedor.nome if recebimento.fornecedor else '-' }}</p>
        <p><strong>Status:</strong> {{ status_labels.get(recebimento.status, recebimento.status|title) }}</p>
        <p><strong>Nota:</strong> {{ recebimento.info_nota or '-' }}</p>
        <p><strong>Regra:</strong> Estoque so sera atualizado ao confirmar esta armazenagem.</p>
    </div>
</div>

<div class="form-container">
    <form method="POST" class="form">
        {{ csrf_input|safe }}
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Produto</th>
                        <th>Codigo</th>
                        <th>Qtd recebida</th>
                        <th>Qtd avaria</th>
                        <th>Qtd liquida</th>
                        <th>Lote</th>
                        <th>Validade</th>
                        <th>Endereco destino (ativo)</th>
                    </tr>
                </thead>
                <tbody>
                    {% for item in recebimento.itens %}
                    <tr>
                        <td data-label="Produto">{{ item.produto.nome if item.produto else '-' }}</td>
                        <td data-label="Codigo"><code>{{ item.produto.codigo if item.produto else '-' }}</code></td>
                        <td data-label="Qtd recebida">{{ item.qtd_recebida or 0 }}</td>
                        <td data-label="Qtd avaria">{{ item.qtd_avaria or 0 }}</td>
                        <td data-label="Qtd liquida">{{ item.qtd_liquida }}</td>
                        <td data-label="Lote">{{ item.lote or '-' }}</td>
                        <td data-label="Validade">{{ item.validade.strftime('%d/%m/%Y') if item.validade else '-' }}</td>
                        <td data-label="Endereco destino">
                            <select name="endereco_destino_{{ item.id }}" class="input-select" required>
                                <option value="">Selecione</option>
                                {% for endereco in enderecos_ativos %}
                                <option value="{{ endereco.id }}" {% if item.endereco_destino_id == endereco.id %}selected{% endif %}>
                                    {{ endereco.nome }} - {{ endereco.codigo_localizacao or '-' }}
                                </option>
                                {% endfor %}
                            </select>
                        </td>
                    </tr>
                    {% else %}
                    <tr>
                        <td colspan="8" class="text-center">Nenhum item para armazenar.</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>

        <div class="form-actions">
            <button type="submit" class="btn btn-primary">Confirmar armazenagem</button>
            <a href="{{ url_for('listar_recebimentos_fornecedor') }}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>
{% endblock %}
```

---

### Arquivo: `templates\estoque\recebimentos\conferir_recebimento.html`

```html
{% extends "base.html" %}

{% block title %}Conferir Recebimento #{{ recebimento.id }} - SystemLR{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Conferir Recebimento #{{ recebimento.id }}</h1>
    <div class="header-actions">
        <a href="{{ url_for('listar_recebimentos_fornecedor') }}" class="btn btn-secondary">Voltar</a>
    </div>
</div>

<div class="card mb-3">
    <div class="card-body">
        <p><strong>Fornecedor:</strong> {{ recebimento.fornecedor.nome if recebimento.fornecedor else '-' }}</p>
        <p><strong>Status:</strong> {{ status_labels.get(recebimento.status, recebimento.status|title) }}</p>
        <p><strong>Nota:</strong> {{ recebimento.info_nota or '-' }}</p>
    </div>
</div>

<div class="form-container">
    <form method="POST" class="form">
        {{ csrf_input|safe }}
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Produto</th>
                        <th>Codigo</th>
                        <th>Qtd recebida</th>
                        <th>Qtd avaria</th>
                        <th>Lote</th>
                        <th>Validade</th>
                        <th>Qtd liquida</th>
                    </tr>
                </thead>
                <tbody>
                    {% for item in recebimento.itens %}
                    <tr>
                        <td data-label="Produto">{{ item.produto.nome if item.produto else '-' }}</td>
                        <td data-label="Codigo"><code>{{ item.produto.codigo if item.produto else '-' }}</code></td>
                        <td data-label="Qtd recebida">
                            <input type="number" min="0" class="input-text" name="item_{{ item.id }}_qtd_recebida" value="{{ item.qtd_recebida or 0 }}" required>
                        </td>
                        <td data-label="Qtd avaria">
                            <input type="number" min="0" class="input-text" name="item_{{ item.id }}_qtd_avaria" value="{{ item.qtd_avaria or 0 }}" required>
                        </td>
                        <td data-label="Lote">
                            <input type="text" class="input-text" name="item_{{ item.id }}_lote" value="{{ item.lote or '' }}" maxlength="80">
                        </td>
                        <td data-label="Validade">
                            <input type="date" class="input-text" name="item_{{ item.id }}_validade" value="{{ item.validade.strftime('%Y-%m-%d') if item.validade else '' }}">
                        </td>
                        <td data-label="Qtd liquida">{{ item.qtd_liquida }}</td>
                    </tr>
                    {% else %}
                    <tr>
                        <td colspan="7" class="text-center">Nenhum item no recebimento.</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>

        <div class="form-actions">
            <button type="submit" class="btn btn-primary">Salvar conferencia</button>
            {% if recebimento.status == 'aguardando_armazenagem' %}
            <a href="{{ url_for('armazenar_recebimento_fornecedor', recebimento_id=recebimento.id) }}" class="btn btn-warning">Ir para armazenagem</a>
            {% endif %}
        </div>
    </form>
</div>
{% endblock %}
```

---

### Arquivo: `templates\estoque\recebimentos\novo_recebimento.html`

```html
{% extends "base.html" %}

{% block title %}Novo Recebimento - SystemLR{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Novo Recebimento de Fornecedor</h1>
</div>

<div class="form-container">
    <form method="POST" class="form">
        {{ csrf_input|safe }}
        <h3 class="mb-2">1. Cabecalho (Identificacao da entrega)</h3>
        <div class="form-row">
            <div class="form-group">
                <label for="fornecedor_id">Fornecedor *</label>
                <select id="fornecedor_id" name="fornecedor_id" class="input-select" required>
                    <option value="">Selecione</option>
                    {% for fornecedor in fornecedores %}
                    <option
                        value="{{ fornecedor.id }}"
                        data-documento="{{ fornecedor.documento or '' }}"
                        data-contato="{{ fornecedor.contato or '' }}"
                        data-telefone="{{ fornecedor.telefone or '' }}"
                        data-endereco-rua="{{ fornecedor.endereco_rua or '' }}"
                        data-endereco-numero="{{ fornecedor.endereco_numero or '' }}"
                        data-endereco-bairro="{{ fornecedor.endereco_bairro or '' }}"
                        data-endereco-cidade="{{ fornecedor.endereco_cidade or '' }}"
                        data-tipo-produtos="{{ fornecedor.tipo_produtos_fornece or '' }}"
                        data-observacoes="{{ fornecedor.observacoes_gerais or '' }}"
                    >{{ fornecedor.nome }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="form-group">
                <label for="fornecedor_documento">CNPJ/CPF</label>
                <input type="text" id="fornecedor_documento" name="fornecedor_documento" class="input-text" placeholder="00.000.000/0000-00 ou 000.000.000-00">
            </div>
            <div class="form-group">
                <label for="fornecedor_telefone_info">Telefone do fornecedor</label>
                <input type="text" id="fornecedor_telefone_info" class="input-text" readonly>
            </div>
            <div class="form-group">
                <label for="fornecedor_endereco_info">Endereco do fornecedor</label>
                <input type="text" id="fornecedor_endereco_info" class="input-text" readonly>
            </div>
        </div>
        <div class="form-row">
            <div class="form-group">
                <label for="fornecedor_tipo_produtos_info">Tipo de produtos que fornece</label>
                <input type="text" id="fornecedor_tipo_produtos_info" class="input-text" readonly>
            </div>
            <div class="form-group">
                <label for="fornecedor_observacoes_info">Observacoes do fornecedor</label>
                <input type="text" id="fornecedor_observacoes_info" class="input-text" readonly>
            </div>
            <div class="form-group">
                <label for="data_entrega">Data da entrega</label>
                <input type="date" id="data_entrega" name="data_entrega" class="input-text">
            </div>
            <div class="form-group">
                <label for="info_nota">No Nota Fiscal</label>
                <input type="text" id="info_nota" name="info_nota" class="input-text" placeholder="Ex: NF 12345 Serie 1">
            </div>
        </div>

        <h3 class="mb-2 mt-3">2. Tabela de Produtos (itens recebidos)</h3>
        <div class="form-row">
            <div class="form-group">
                <label for="codigo_produto_rapido">Codigo de barras / codigo do produto</label>
                <div class="barcode-input-group">
                    <input type="text" id="codigo_produto_rapido" class="input-text" placeholder="Leia ou digite o codigo e adicione">
                    <button type="button" class="btn btn-secondary barcode-btn js-open-barcode-scanner" data-barcode-target="codigo_produto_rapido">Camera</button>
                    <button type="button" class="btn btn-primary" id="adicionar-por-codigo">Adicionar por codigo</button>
                </div>
            </div>
        </div>
        <div class="table-responsive">
            <table class="table" id="itens-table">
                <thead>
                    <tr>
                        <th>Produto</th>
                        <th>Qtd recebida</th>
                        <th>Unidade</th>
                        <th>Descricao do produto</th>
                        <th>Preco unitario (R$)</th>
                        <th>Total (R$)</th>
                        <th>Acoes</th>
                    </tr>
                </thead>
                <tbody id="itens-body">
                    <tr>
                        <td>
                            <select name="produto_id[]" class="input-select" required>
                                <option value="">Selecione</option>
                                {% for produto in produtos %}
                                <option
                                    value="{{ produto.id }}"
                                    data-codigo="{{ (produto.codigo or '')|upper }}"
                                    data-preco-custo="{{ produto.preco_custo or 0 }}"
                                >{{ produto.codigo }} - {{ produto.nome }} (Estoque atual: {{ produto.quantidade_estoque }})</option>
                                {% endfor %}
                            </select>
                        </td>
                        <td>
                            <input type="number" name="qtd_recebida[]" class="input-text" min="0" value="0" required>
                        </td>
                        <td>
                            <select name="unidade[]" class="input-select">
                                <option value="UN">UN</option>
                                <option value="KG">KG</option>
                                <option value="LT">LT</option>
                                <option value="PCT">PCT</option>
                                <option value="CX">CX</option>
                            </select>
                        </td>
                        <td>
                            <input type="text" name="descricao_item[]" class="input-text" placeholder="Descricao detalhada do item">
                        </td>
                        <td>
                            <input type="number" name="preco_unitario[]" class="input-text js-preco-unitario" min="0" step="0.01" value="0.00">
                        </td>
                        <td>
                            <input type="text" name="total_item[]" class="input-text js-total-item" value="0.00" readonly>
                        </td>
                        <td>
                            <button type="button" class="btn-small btn-danger remover-item">Remover</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <button type="button" class="btn btn-secondary" id="adicionar-item">Adicionar item</button>

        <h3 class="mb-2 mt-3">3. Totais e Pagamento</h3>
        <div class="form-row">
            <div class="form-group">
                <label for="subtotal">Subtotal (R$)</label>
                <input type="text" id="subtotal" name="subtotal" class="input-text" value="0.00" readonly>
            </div>
            <div class="form-group">
                <label for="desconto">Desconto (R$)</label>
                <input type="number" id="desconto" name="desconto" class="input-text" min="0" step="0.01" value="0.00">
            </div>
            <div class="form-group">
                <label for="total_pagar">Total a pagar (R$)</label>
                <input type="text" id="total_pagar" name="total_pagar" class="input-text" value="0.00" readonly>
            </div>
        </div>

        <h3 class="mb-2 mt-3">4. Observacoes</h3>
        <div class="form-group">
            <label for="observacoes">Avarias, diferencas, atrasos e ocorrencias</label>
            <textarea id="observacoes" name="observacoes" class="input-textarea" rows="3" placeholder="Descreva avarias, diferencas, atrasos e outras ocorrencias"></textarea>
        </div>

        <h3 class="mb-2 mt-3">5. Assinaturas</h3>
        <div class="form-row">
            <div class="form-group">
                <label for="recebedor_nome">Recebedor (mercado)</label>
                <input type="text" id="recebedor_nome" name="recebedor_nome" class="input-text" placeholder="Nome do funcionario que conferiu">
            </div>
            <div class="form-group">
                <label for="recebedor_assinatura">Assinatura do recebedor</label>
                <input type="text" id="recebedor_assinatura" name="recebedor_assinatura" class="input-text" placeholder="Nome completo / rubrica">
            </div>
        </div>
        <div class="form-row">
            <div class="form-group">
                <label for="entregador_nome">Fornecedor / Entregador</label>
                <input type="text" id="entregador_nome" name="entregador_nome" class="input-text" placeholder="Nome de quem realizou a entrega">
            </div>
            <div class="form-group">
                <label for="entregador_assinatura">Assinatura do fornecedor / entregador</label>
                <input type="text" id="entregador_assinatura" name="entregador_assinatura" class="input-text" placeholder="Nome completo / rubrica">
            </div>
        </div>

        <div class="form-actions mt-3">
            <button type="submit" class="btn btn-primary">Criar recebimento</button>
            <a href="{{ url_for('listar_recebimentos_fornecedor') }}" class="btn btn-secondary">Cancelar</a>
        </div>
        <div class="form-group mt-2">
            <label class="checkbox-inline">
                <input type="checkbox" name="ir_para_armazenagem" checked>
                Ir direto para armazenagem apos criar (enderecos ativos)
            </label>
        </div>
    </form>
</div>
{% endblock %}

{% block extra_js %}
<script>
document.addEventListener('DOMContentLoaded', function () {
    const adicionarBtn = document.getElementById('adicionar-item');
    const adicionarCodigoBtn = document.getElementById('adicionar-por-codigo');
    const codigoRapidoEl = document.getElementById('codigo_produto_rapido');
    const itensBody = document.getElementById('itens-body');
    const rowTemplate = itensBody.querySelector('tr').cloneNode(true);
    const fornecedorSelect = document.getElementById('fornecedor_id');
    const fornecedorDocumento = document.getElementById('fornecedor_documento');
    const fornecedorTelefoneInfo = document.getElementById('fornecedor_telefone_info');
    const fornecedorEnderecoInfo = document.getElementById('fornecedor_endereco_info');
    const fornecedorTipoProdutosInfo = document.getElementById('fornecedor_tipo_produtos_info');
    const fornecedorObservacoesInfo = document.getElementById('fornecedor_observacoes_info');
    const subtotalEl = document.getElementById('subtotal');
    const descontoEl = document.getElementById('desconto');
    const totalPagarEl = document.getElementById('total_pagar');

    function toNumber(value) {
        const normalized = String(value || '').replace(',', '.').trim();
        const num = parseFloat(normalized);
        return Number.isFinite(num) ? num : 0;
    }

    function money(value) {
        return toNumber(value).toFixed(2);
    }

    function normalizeDoc(value) {
        return String(value || '').replace(/\D/g, '');
    }

    function cleanCode(value) {
        return String(value || '').trim().toUpperCase();
    }

    function updateFornecedorInfo(option) {
        const telefone = option ? (option.dataset.telefone || '') : '';
        const rua = option ? (option.dataset.enderecoRua || '') : '';
        const numero = option ? (option.dataset.enderecoNumero || '') : '';
        const bairro = option ? (option.dataset.enderecoBairro || '') : '';
        const cidade = option ? (option.dataset.enderecoCidade || '') : '';
        const tipoProdutos = option ? (option.dataset.tipoProdutos || '') : '';
        const obs = option ? (option.dataset.observacoes || '') : '';
        const documento = option ? (option.dataset.documento || '') : '';
        const endereco = [rua, numero, bairro, cidade].filter(Boolean).join(', ');

        fornecedorTelefoneInfo.value = telefone;
        fornecedorEnderecoInfo.value = endereco;
        fornecedorTipoProdutosInfo.value = tipoProdutos;
        fornecedorObservacoesInfo.value = obs;
        if (documento) fornecedorDocumento.value = documento;
    }

    function syncFornecedorByDocumento() {
        const docDigitado = normalizeDoc(fornecedorDocumento.value);
        if (!docDigitado) return;
        const options = Array.from(fornecedorSelect.options || []);
        const match = options.find((opt) => normalizeDoc(opt.dataset.documento || '') === docDigitado);
        if (!match) return;
        fornecedorSelect.value = match.value;
        updateFornecedorInfo(match);
    }

    function atualizarTotais() {
        let subtotal = 0;
        itensBody.querySelectorAll('tr').forEach((row) => {
            const qtdInput = row.querySelector('input[name="qtd_recebida[]"]');
            const precoInput = row.querySelector('input[name="preco_unitario[]"]');
            const totalItemInput = row.querySelector('input[name="total_item[]"]');
            const qtd = toNumber(qtdInput ? qtdInput.value : 0);
            const preco = toNumber(precoInput ? precoInput.value : 0);
            const totalItem = qtd * preco;
            subtotal += totalItem;
            if (totalItemInput) totalItemInput.value = money(totalItem);
        });
        const desconto = toNumber(descontoEl ? descontoEl.value : 0);
        const totalPagar = Math.max(subtotal - desconto, 0);
        if (subtotalEl) subtotalEl.value = money(subtotal);
        if (totalPagarEl) totalPagarEl.value = money(totalPagar);
    }

    function selecionarProdutoNaLinha(row, codigo) {
        const produtoSelect = row.querySelector('select[name="produto_id[]"]');
        const precoInput = row.querySelector('input[name="preco_unitario[]"]');
        const descricaoInput = row.querySelector('input[name="descricao_item[]"]');
        if (!produtoSelect) return false;

        const codigoLimpo = cleanCode(codigo);
        if (!codigoLimpo) return false;
        const option = Array.from(produtoSelect.options || []).find((opt) => cleanCode(opt.dataset.codigo) === codigoLimpo);
        if (!option) return false;

        produtoSelect.value = option.value;
        if (precoInput && (!precoInput.value || toNumber(precoInput.value) === 0)) {
            precoInput.value = money(option.dataset.precoCusto || 0);
        }
        if (descricaoInput && !descricaoInput.value.trim()) {
            descricaoInput.value = option.textContent.split('(Estoque atual:')[0].trim();
        }
        atualizarTotais();
        return true;
    }

    function bindRemover(btn) {
        btn.addEventListener('click', function () {
            const rows = itensBody.querySelectorAll('tr');
            if (rows.length <= 1) {
                const select = rows[0].querySelector('select');
                const qtd = rows[0].querySelector('input[name=\"qtd_recebida[]\"]');
                const preco = rows[0].querySelector('input[name=\"preco_unitario[]\"]');
                const total = rows[0].querySelector('input[name=\"total_item[]\"]');
                if (select) select.value = '';
                if (qtd) qtd.value = '0';
                if (preco) preco.value = '0.00';
                if (total) total.value = '0.00';
                atualizarTotais();
                return;
            }
            this.closest('tr').remove();
            atualizarTotais();
        });
    }

    itensBody.querySelectorAll('.remover-item').forEach(bindRemover);
    itensBody.addEventListener('change', function (event) {
        const target = event.target;
        if (!target) return;
        if (target.name === 'produto_id[]') {
            const row = target.closest('tr');
            const selected = target.selectedOptions && target.selectedOptions[0] ? target.selectedOptions[0] : null;
            if (!row || !selected) return;
            const preco = row.querySelector('input[name="preco_unitario[]"]');
            const desc = row.querySelector('input[name="descricao_item[]"]');
            if (preco && (!preco.value || toNumber(preco.value) === 0)) {
                preco.value = money(selected.dataset.precoCusto || 0);
            }
            if (desc && !desc.value.trim()) {
                desc.value = selected.textContent.split('(Estoque atual:')[0].trim();
            }
            atualizarTotais();
        }
    });
    itensBody.addEventListener('input', function (event) {
        const target = event.target;
        if (!target) return;
        if (target.name === 'qtd_recebida[]' || target.name === 'preco_unitario[]') {
            atualizarTotais();
        }
    });
    if (descontoEl) {
        descontoEl.addEventListener('input', atualizarTotais);
    }

    fornecedorSelect.addEventListener('change', function () {
        const selected = fornecedorSelect.selectedOptions && fornecedorSelect.selectedOptions[0] ? fornecedorSelect.selectedOptions[0] : null;
        updateFornecedorInfo(selected);
    });
    fornecedorDocumento.addEventListener('input', syncFornecedorByDocumento);

    adicionarBtn.addEventListener('click', function () {
        const novaLinha = rowTemplate.cloneNode(true);
        const select = novaLinha.querySelector('select');
        const qtd = novaLinha.querySelector('input[name=\"qtd_recebida[]\"]');
        const unidade = novaLinha.querySelector('select[name=\"unidade[]\"]');
        const descricao = novaLinha.querySelector('input[name=\"descricao_item[]\"]');
        const preco = novaLinha.querySelector('input[name=\"preco_unitario[]\"]');
        const total = novaLinha.querySelector('input[name=\"total_item[]\"]');
        if (select) select.value = '';
        if (qtd) qtd.value = '0';
        if (unidade) unidade.value = 'UN';
        if (descricao) descricao.value = '';
        if (preco) preco.value = '0.00';
        if (total) total.value = '0.00';
        bindRemover(novaLinha.querySelector('.remover-item'));
        itensBody.appendChild(novaLinha);
        atualizarTotais();
    });

    function adicionarPorCodigo() {
        const codigo = cleanCode(codigoRapidoEl.value);
        if (!codigo) return;
        const rows = Array.from(itensBody.querySelectorAll('tr'));
        const linhaVazia = rows.find((row) => {
            const select = row.querySelector('select[name="produto_id[]"]');
            return select && !select.value;
        });
        if (linhaVazia) {
            if (selecionarProdutoNaLinha(linhaVazia, codigo)) {
                codigoRapidoEl.value = '';
                return;
            }
        }
        const novaLinha = rowTemplate.cloneNode(true);
        const select = novaLinha.querySelector('select');
        const qtd = novaLinha.querySelector('input[name=\"qtd_recebida[]\"]');
        const unidade = novaLinha.querySelector('select[name=\"unidade[]\"]');
        const descricao = novaLinha.querySelector('input[name=\"descricao_item[]\"]');
        const preco = novaLinha.querySelector('input[name=\"preco_unitario[]\"]');
        const total = novaLinha.querySelector('input[name=\"total_item[]\"]');
        if (select) select.value = '';
        if (qtd) qtd.value = '0';
        if (unidade) unidade.value = 'UN';
        if (descricao) descricao.value = '';
        if (preco) preco.value = '0.00';
        if (total) total.value = '0.00';
        bindRemover(novaLinha.querySelector('.remover-item'));
        itensBody.appendChild(novaLinha);
        const ok = selecionarProdutoNaLinha(novaLinha, codigo);
        if (!ok) {
            novaLinha.remove();
            alert('Codigo nao encontrado na lista de produtos.');
            return;
        }
        codigoRapidoEl.value = '';
    }

    if (adicionarCodigoBtn) {
        adicionarCodigoBtn.addEventListener('click', adicionarPorCodigo);
    }
    if (codigoRapidoEl) {
        codigoRapidoEl.addEventListener('keydown', function (event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                adicionarPorCodigo();
            }
        });
        codigoRapidoEl.addEventListener('barcode:detected', function () {
            adicionarPorCodigo();
        });
    }

    if (fornecedorSelect && fornecedorSelect.value) {
        const selected = fornecedorSelect.selectedOptions && fornecedorSelect.selectedOptions[0] ? fornecedorSelect.selectedOptions[0] : null;
        updateFornecedorInfo(selected);
    }
    atualizarTotais();
});
</script>
{% endblock %}
```

---

### Arquivo: `templates\estoque\recebimentos\recebimentos.html`

```html
{% extends "base.html" %}

{% block title %}Recebimentos de Fornecedor - SystemLR{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Recebimentos de Fornecedor</h1>
    <div class="header-actions">
        <a href="{{ url_for('listar_movimentacoes') }}" class="btn btn-secondary">Ver Movimentacoes</a>
        <a href="{{ url_for('novo_recebimento_fornecedor') }}" class="btn btn-primary">Novo Recebimento</a>
    </div>
</div>

<div class="filters-section">
    <form method="GET" class="filters-form">
        <div class="filter-group">
            <label for="busca">Busca</label>
            <input type="text" id="busca" name="busca" class="input-search" value="{{ filtros.busca if filtros else '' }}" placeholder="ID, nota, fornecedor, codigo ou nome do produto">
        </div>
        <div class="filter-group">
            <label for="fornecedor_id">Fornecedor</label>
            <select id="fornecedor_id" name="fornecedor_id" class="input-select">
                <option value="">Todos</option>
                {% for fornecedor in fornecedores %}
                <option value="{{ fornecedor.id }}" {% if filtros and filtros.fornecedor_id == fornecedor.id %}selected{% endif %}>{{ fornecedor.nome }}</option>
                {% endfor %}
            </select>
        </div>
        <div class="filter-group">
            <label for="status">Status</label>
            <select id="status" name="status" class="input-select">
                <option value="">Todos</option>
                {% for st in status_labels.keys() %}
                <option value="{{ st }}" {% if filtros and filtros.status == st %}selected{% endif %}>{{ status_labels[st] }}</option>
                {% endfor %}
            </select>
        </div>
        <div class="filter-group">
            <label for="data_inicio">De</label>
            <input type="date" id="data_inicio" name="data_inicio" class="input-search" value="{{ filtros.data_inicio if filtros else '' }}">
        </div>
        <div class="filter-group">
            <label for="data_fim">Ate</label>
            <input type="date" id="data_fim" name="data_fim" class="input-search" value="{{ filtros.data_fim if filtros else '' }}">
        </div>
        <div class="form-actions">
            <button type="submit" class="btn btn-primary">Filtrar</button>
            <a href="{{ url_for('listar_recebimentos_fornecedor') }}" class="btn btn-secondary">Limpar</a>
        </div>
    </form>
</div>

<div class="table-responsive table-scroll-sticky">
    <table class="table">
        <thead>
            <tr>
                <th>ID</th>
                <th>Fornecedor</th>
                <th>Nota</th>
                <th>Itens</th>
                <th>Codigos Produtos</th>
                <th>Status</th>
                <th>Criado em</th>
                <th>Acoes</th>
            </tr>
        </thead>
        <tbody>
            {% for recebimento in recebimentos %}
            <tr>
                <td data-label="ID">#{{ recebimento.id }}</td>
                <td data-label="Fornecedor">{{ recebimento.fornecedor.nome if recebimento.fornecedor else '-' }}</td>
                <td data-label="Nota">{{ recebimento.info_nota or '-' }}</td>
                <td data-label="Itens">{{ recebimento.itens|length }}</td>
                <td data-label="Codigos Produtos">
                    {% set codigos = [] %}
                    {% for item in recebimento.itens %}
                        {% if item.produto and item.produto.codigo %}
                            {% set _ = codigos.append(item.produto.codigo) %}
                        {% endif %}
                    {% endfor %}
                    {% if codigos %}
                        {{ codigos|join(', ') }}
                    {% else %}
                        -
                    {% endif %}
                </td>
                <td data-label="Status">
                    {% set st = recebimento.status %}
                    <span class="badge {% if st == 'concluido' %}badge-success{% elif st == 'cancelado' %}badge-danger{% elif st == 'aguardando_armazenagem' %}badge-warning{% else %}badge-info{% endif %}">
                        {{ status_labels.get(st, st|title) }}
                    </span>
                </td>
                <td data-label="Criado em">{{ recebimento.criado_em.strftime('%d/%m/%Y %H:%M') if recebimento.criado_em else '-' }}</td>
                <td data-label="Acoes" class="actions-cell">
                    {% if recebimento.status != 'cancelado' and recebimento.status != 'concluido' %}
                    <a href="{{ url_for('conferir_recebimento_fornecedor', recebimento_id=recebimento.id) }}" class="btn-small btn-warning">Conferir</a>
                    {% endif %}
                    {% if recebimento.status == 'aguardando_armazenagem' %}
                    <a href="{{ url_for('armazenar_recebimento_fornecedor', recebimento_id=recebimento.id) }}" class="btn-small btn-primary">Armazenar</a>
                    {% endif %}
                    {% if recebimento.status != 'cancelado' and recebimento.status != 'concluido' %}
                    <form method="POST" action="{{ url_for('cancelar_recebimento_fornecedor', recebimento_id=recebimento.id) }}" class="inline-form" data-confirm-message="Cancelar recebimento #{{ recebimento.id }}?">
                        {{ csrf_input|safe }}
                        <button type="submit" class="btn-small btn-danger">Cancelar</button>
                    </form>
                    {% endif %}
                </td>
            </tr>
            {% else %}
            <tr>
                <td colspan="8" class="text-center">Nenhum recebimento encontrado</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>

{% if pagination and pagination.pages > 1 %}
<div class="pagination">
    {% set params = query_params.copy() if query_params else {} %}
    {% if pagination.has_prev %}
        {% set params_prev = params.copy() %}
        {% set _ = params_prev.update({'page': pagination.prev_num, 'per_page': per_page}) %}
        <a class="btn btn-outline-secondary" href="{{ url_for('listar_recebimentos_fornecedor', **params_prev) }}">Anterior</a>
    {% else %}
        <span class="btn btn-outline-secondary disabled">Anterior</span>
    {% endif %}

    <span class="pagination-info">Pagina {{ pagination.page }} de {{ pagination.pages }}</span>

    {% if pagination.has_next %}
        {% set params_next = params.copy() %}
        {% set _ = params_next.update({'page': pagination.next_num, 'per_page': per_page}) %}
        <a class="btn btn-outline-secondary" href="{{ url_for('listar_recebimentos_fornecedor', **params_next) }}">Proxima</a>
    {% else %}
        <span class="btn btn-outline-secondary disabled">Proxima</span>
    {% endif %}
</div>
{% endif %}
{% endblock %}
```

---

### Arquivo: `templates\estoque\relatorios\relatorios.html`

```html
{% extends "base.html" %}

{% block title %}Relatorios de Estoque - SystemLR{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Relatorios de Estoque</h1>
</div>

<div class="cards-container analytics-cards">
    <div class="card card-primary">
        <div class="card-content">
            <h3>Total de Produtos</h3>
            <p class="card-value">{{ total_produtos }}</p>
            <p class="card-meta">{{ produtos_ativos }} ativos / {{ produtos_inativos }} inativos</p>
        </div>
    </div>
    <div class="card card-info">
        <div class="card-content">
            <h3>Unidades em Estoque</h3>
            <p class="card-value">{{ total_unidades }}</p>
            <p class="card-meta">{{ produtos_sem_estoque }} produtos com saldo zerado</p>
        </div>
    </div>
    <div class="card card-success">
        <div class="card-content">
            <h3>Valor Total do Estoque</h3>
            <p class="card-value">R$ {{ valor_total_estoque }}</p>
            <p class="card-meta">Custo medio unitario: R$ {{ custo_medio_estoque }}</p>
        </div>
    </div>
    <div class="card card-warning">
        <div class="card-content">
            <h3>Movimentacoes (30 dias)</h3>
            <p class="card-value">{{ movimentacoes_mes }}</p>
            <p class="card-meta">{{ entradas_mes }} entradas / {{ saidas_mes }} saidas</p>
        </div>
    </div>
</div>

<div class="section">
    <div class="page-header">
        <h2>Graficos Dinamicos de Estoque</h2>
        <div class="header-actions">
            <select id="estoquePeriodo" class="input-select">
                <option value="7">Ultimos 7 dias</option>
                <option value="30" selected>Ultimos 30 dias</option>
                <option value="90">Ultimos 90 dias</option>
            </select>
        </div>
    </div>
    <div class="analytics-grid">
        <section class="section">
            <h2>Movimentacoes Diarias</h2>
            <div class="chart-container">
                <canvas id="chartMovimentacoesEstoque"></canvas>
            </div>
        </section>
        <section class="section">
            <h2>Valor por Categoria</h2>
            <div class="chart-container">
                <canvas id="chartValorCategoriaEstoque"></canvas>
            </div>
        </section>
    </div>
</div>

<div class="analytics-grid">
    <section class="section">
        <h2>Produtos em Falta</h2>
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Codigo</th>
                        <th>Produto</th>
                        <th>Categoria</th>
                        <th>Endereco</th>
                        <th>Atual</th>
                        <th>Minimo</th>
                    </tr>
                </thead>
                <tbody>
                    {% for prod in produtos_em_falta %}
                    <tr class="row-warning">
                        <td data-label="Codigo"><code>{{ prod.codigo }}</code></td>
                        <td data-label="Produto">
                            <div class="product-name-cell">
                                {% if prod.imagem_path %}
                                <img src="{{ url_for('static', filename=prod.imagem_path) }}" alt="{{ prod.nome }}" class="product-thumb product-thumb-sm">
                                {% endif %}
                                <a href="{{ url_for('visualizar_produto', produto_id=prod.id) }}">{{ prod.nome }}</a>
                            </div>
                        </td>
                        <td data-label="Categoria">{{ prod.categoria.nome if prod.categoria else '-' }}</td>
                        <td data-label="Endereco">{{ prod.endereco.nome if prod.endereco else '-' }}</td>
                        <td data-label="Atual">{{ prod.quantidade_estoque }}</td>
                        <td data-label="Minimo">{{ prod.quantidade_minima }}</td>
                    </tr>
                    {% else %}
                    <tr>
                        <td colspan="6" class="text-center">Nenhum produto abaixo do estoque minimo.</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </section>

    <section class="section">
        <h2>Produtos com Maior Valor em Estoque</h2>
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Codigo</th>
                        <th>Produto</th>
                        <th>Qtd</th>
                        <th>Custo Unit.</th>
                        <th>Valor Total</th>
                    </tr>
                </thead>
                <tbody>
                    {% for prod, valor in produtos_maior_valor %}
                    <tr>
                        <td data-label="Codigo"><code>{{ prod.codigo }}</code></td>
                        <td data-label="Produto">{{ prod.nome }}</td>
                        <td data-label="Qtd">{{ prod.quantidade_estoque }}</td>
                        <td data-label="Custo Unit.">R$ {{ "%.2f"|format(prod.preco_custo) }}</td>
                        <td data-label="Valor Total">R$ {{ "%.2f"|format(valor or 0) }}</td>
                    </tr>
                    {% else %}
                    <tr>
                        <td colspan="5" class="text-center">Sem dados de valor em estoque.</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </section>
</div>

<div class="analytics-grid">
    <section class="section">
        <h2>Valor de Estoque por Categoria</h2>
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Categoria</th>
                        <th>Produtos</th>
                        <th>Unidades</th>
                        <th>Valor</th>
                    </tr>
                </thead>
                <tbody>
                    {% for item in valor_por_categoria %}
                    <tr>
                        <td data-label="Categoria">{{ item.categoria_nome }}</td>
                        <td data-label="Produtos">{{ item.produtos or 0 }}</td>
                        <td data-label="Unidades">{{ item.qtd_total or 0 }}</td>
                        <td data-label="Valor">R$ {{ "%.2f"|format(item.valor_total or 0) }}</td>
                    </tr>
                    {% else %}
                    <tr>
                        <td colspan="4" class="text-center">Sem dados por categoria.</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </section>

    <section class="section">
        <h2>Distribuicao por Endereco</h2>
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Endereco</th>
                        <th>Produtos</th>
                        <th>Unidades</th>
                        <th>Valor</th>
                    </tr>
                </thead>
                <tbody>
                    {% for item in valor_por_endereco %}
                    <tr>
                        <td data-label="Endereco">{{ item.endereco_nome }}</td>
                        <td data-label="Produtos">{{ item.produtos or 0 }}</td>
                        <td data-label="Unidades">{{ item.qtd_total or 0 }}</td>
                        <td data-label="Valor">R$ {{ "%.2f"|format(item.valor_total or 0) }}</td>
                    </tr>
                    {% else %}
                    <tr>
                        <td colspan="4" class="text-center">Nenhum endereco vinculado a produtos.</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </section>
</div>

<div class="section">
    <h2>Produtos sem Giro (60 dias)</h2>
    <div class="table-responsive">
        <table class="table">
            <thead>
                <tr>
                    <th>Codigo</th>
                    <th>Produto</th>
                    <th>Categoria</th>
                    <th>Endereco</th>
                    <th>Estoque</th>
                    <th>Acao</th>
                </tr>
            </thead>
            <tbody>
                {% for prod in produtos_sem_giro %}
                <tr>
                    <td data-label="Codigo"><code>{{ prod.codigo }}</code></td>
                    <td data-label="Produto">{{ prod.nome }}</td>
                    <td data-label="Categoria">{{ prod.categoria.nome if prod.categoria else '-' }}</td>
                    <td data-label="Endereco">{{ prod.endereco.nome if prod.endereco else '-' }}</td>
                    <td data-label="Estoque">{{ prod.quantidade_estoque }}</td>
                    <td data-label="Acao">
                        <a href="{{ url_for('visualizar_produto', produto_id=prod.id) }}" class="btn-small btn-info">Ver Produto</a>
                    </td>
                </tr>
                {% else %}
                <tr>
                    <td colspan="6" class="text-center">Todos os produtos tiveram movimentacao recente.</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js"></script>
<script src="{{ url_for('static', filename='js/pages/estoque_analytics.js') }}"></script>
{% endblock %}
```

---

### Arquivo: `templates\funcionarios\acessos.html`

```html
{% extends "base.html" %}

{% block title %}Editar Acessos - {{ funcionario.nome }} - SystemLR{% endblock %}

{% block content %}
<div class="funcionario-access-page">
    <div class="funcionario-access-header">
        <a href="{{ url_for('listar_funcionarios') }}" class="funcionario-back-link" aria-label="Voltar para funcionarios">&larr;</a>
        <h1>Editar Acessos</h1>
    </div>

    <div class="funcionario-access-card">
        <div class="funcionario-access-summary">
            <p>
                <strong>Funcionario:</strong> {{ funcionario.nome }}<br>
                <strong>Email:</strong> {{ funcionario.email }}<br>
                <strong>Funcao:</strong>
                <span class="funcionario-role role-{{ funcionario.role }}">{{ funcionario.role.upper() }}</span>
            </p>
        </div>

        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
                        {{ message }}
                        <button type="button" class="close" data-dismiss="alert">&times;</button>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        <form method="POST" action="{{ url_for('editar_acessos_funcionario', funcionario_id=funcionario.id) }}">
            {{ csrf_input|safe }}
            <div>
                <h3 class="funcionario-access-title">Permissoes de Acesso</h3>

                <div class="funcionario-access-tip">
                    Selecione as paginas que este funcionario tera acesso no sistema.
                </div>

                {% for secao_nome, secao_itens in paginas_ordenadas_menu %}
                    <section class="funcionario-access-section">
                        <h4>{{ secao_nome }}</h4>
                        <div class="funcionario-access-grid">
                            {% for pagina_key, pagina_nome in secao_itens %}
                                <label class="funcionario-access-option">
                                    <input type="checkbox" name="paginas" value="{{ pagina_key }}"
                                           {% if pagina_key in permissoes_atuais %}checked{% endif %}>
                                    <span>{{ pagina_nome }}</span>
                                </label>
                            {% endfor %}
                        </div>
                    </section>
                {% endfor %}
            </div>

            <div class="funcionario-access-actions">
                <button type="submit" class="btn btn-primary">Salvar Acessos</button>
                <a href="{{ url_for('listar_funcionarios') }}" class="btn btn-secondary">Cancelar</a>
            </div>
        </form>
    </div>
</div>

<style>
    .funcionario-access-page {
        max-width: 700px;
        margin: 40px auto;
    }

    .funcionario-access-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 20px;
    }

    .funcionario-access-header h1 {
        margin: 0;
        color: #343a40;
    }

    .funcionario-back-link {
        font-size: 24px;
        color: #0f766e;
        text-decoration: none;
        font-weight: 700;
        line-height: 1;
    }

    .funcionario-access-card {
        background: #fff;
        padding: 24px;
        border-radius: 10px;
        border: 1px solid #dbe3e8;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }

    .funcionario-access-summary {
        background-color: #f8f9fa;
        padding: 14px;
        border-radius: 8px;
        margin-bottom: 20px;
    }

    .funcionario-access-summary p {
        margin: 0;
        color: #343a40;
    }

    .funcionario-role {
        display: inline-block;
        margin-top: 6px;
        color: #fff;
        padding: 3px 8px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 700;
    }

    .role-admin {
        background-color: #dc3545;
    }

    .role-gerente {
        background-color: #f59e0b;
        color: #111827;
    }

    .role-caixa {
        background-color: #0ea5e9;
    }

    .role-operador,
    .role-garcom {
        background-color: #64748b;
    }

    .funcionario-access-title {
        color: #343a40;
        margin-bottom: 14px;
        margin-top: 0;
    }

    .funcionario-access-tip {
        background-color: #f0f7ff;
        padding: 14px;
        border-left: 4px solid #0f766e;
        border-radius: 6px;
        margin-bottom: 20px;
        color: #0f4c81;
        font-size: 14px;
    }

    .funcionario-access-section {
        margin-bottom: 18px;
    }

    .funcionario-access-section h4 {
        margin: 0 0 10px;
        color: #334155;
        font-size: 1rem;
    }

    .funcionario-access-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
        gap: 10px;
    }

    .funcionario-access-option {
        display: flex;
        align-items: center;
        padding: 12px;
        background-color: #f8f9fa;
        border-radius: 6px;
        border: 2px solid transparent;
        cursor: pointer;
        transition: background-color 0.2s, border-color 0.2s;
    }

    .funcionario-access-option:hover {
        background-color: #eef3f8;
    }

    .funcionario-access-option:has(input:checked) {
        border-color: #0f766e;
        background-color: #edf9f7;
    }

    .funcionario-access-option input {
        width: 18px;
        height: 18px;
        margin-right: 12px;
        cursor: pointer;
        flex-shrink: 0;
    }

    .funcionario-access-option span {
        color: #343a40;
        font-weight: 500;
    }

    .funcionario-access-actions {
        display: flex;
        gap: 10px;
        margin-top: 28px;
    }

    .funcionario-access-actions > * {
        flex: 1;
        text-align: center;
    }

    .btn {
        display: inline-block;
        text-decoration: none;
    }

    .btn-primary {
        background-color: #28a745;
        border-color: #28a745;
    }

    .btn-primary:hover {
        background-color: #218838;
        border-color: #218838;
    }

    .btn-secondary:hover {
        background-color: #5a6268;
    }

    .alert {
        padding: 12px 14px;
        border-radius: 5px;
        border: 1px solid;
        margin-bottom: 14px;
    }

    .alert-success {
        background-color: #d4edda;
        color: #155724;
        border-color: #c3e6cb;
    }

    .alert-danger {
        background-color: #f8d7da;
        color: #721c24;
        border-color: #f5c6cb;
    }

    @media (max-width: 700px) {
        .funcionario-access-page {
            margin: 20px auto;
        }

        .funcionario-access-card {
            padding: 16px;
        }

        .funcionario-access-actions {
            flex-direction: column;
        }

        .funcionario-access-actions > * {
            width: 100%;
        }
    }
</style>
{% endblock %}
```

---

### Arquivo: `templates\funcionarios\criar.html`

```html
﻿{% extends "base.html" %}

{% block title %}Criar Funcionario - SystemLR{% endblock %}

{% block content %}
<div class="form-container funcionario-form-page">
    <div class="funcionario-form-wrap">
        <h1>Novo Funcionario</h1>

        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
                        {{ message }}
                        <button type="button" class="close" data-dismiss="alert">&times;</button>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        <form method="POST" action="{{ url_for('criar_funcionario') }}" class="form">
            {{ csrf_input|safe }}
            <div class="form-group">
                <label for="nome">Nome Completo <span class="required">*</span></label>
                <input type="text" id="nome" name="nome" class="form-control" required autofocus>
            </div>

            <div class="form-group">
                <label for="email">Email <span class="required">*</span></label>
                <input type="email" id="email" name="email" class="form-control" required>
            </div>

            <div class="form-group">
                <label for="senha">Senha <span class="required">*</span></label>
                <input type="password" id="senha" name="senha" class="form-control" required minlength="6" placeholder="Minimo 6 caracteres">
            </div>

            <div class="form-group">
                <label for="confirmacao_senha">Confirmar Senha <span class="required">*</span></label>
                <input type="password" id="confirmacao_senha" name="confirmacao_senha" class="form-control" required minlength="6">
            </div>

            <div class="form-group">
                <label for="role">Perfil de Acesso <span class="required">*</span></label>
                <select id="role" name="role" class="form-control" required>
                    <option value="">Selecione um perfil</option>
                    <option value="operador">Operador</option>
                    <option value="caixa">Caixa</option>
                    <option value="gerente">Gerente</option>
                    <option value="garcom">Garcom</option>
                </select>
            </div>

            <div class="form-group">
                <label for="cargo">Cargo/Funcao (RH) <span class="required">*</span></label>
                <select id="cargo" name="cargo" class="form-control" required>
                    <option value="">Selecione um cargo</option>
                    {% for funcao in funcoes_rh %}
                        <option value="{{ funcao.nome }}">{{ funcao.nome }}</option>
                    {% endfor %}
                </select>
                <small style="display:block; margin-top:8px; color:#6c757d;">
                    Nao encontrou o cargo? <a href="{{ url_for('nova_funcao_rh') }}">Criar nova funcao</a>.
                </small>
            </div>

            <div class="funcionario-form-actions">
                <button type="submit" class="btn btn-success">Criar Funcionario</button>
                <a href="{{ url_for('listar_funcionarios') }}" class="btn btn-secondary">Cancelar</a>
            </div>
        </form>
    </div>
</div>

<style>
    .funcionario-form-page {
        padding: 40px 20px;
        max-width: 1000px;
        margin: 0 auto;
    }

    .funcionario-form-wrap {
        max-width: 500px;
        margin: 0 auto;
    }

    .funcionario-form-page h1 {
        color: #343a40;
        margin-bottom: 30px;
        font-size: 28px;
    }

    .form-group {
        margin-bottom: 20px;
    }

    .form-group label {
        display: block;
        margin-bottom: 8px;
        color: #343a40;
        font-weight: 600;
    }

    .required {
        color: #dc3545;
    }

    .form-control {
        width: 100%;
        padding: 12px;
        border: 2px solid #dee2e6;
        border-radius: 5px;
        font-size: 16px;
        font-family: inherit;
        transition: border-color 0.3s;
    }

    .form-control:focus {
        outline: none;
        border-color: #667eea;
    }

    .btn {
        padding: 12px 20px;
        border-radius: 5px;
        text-decoration: none;
        font-weight: 600;
        cursor: pointer;
        border: none;
        transition: all 0.3s;
        font-size: 16px;
    }

    .btn-success {
        background-color: #28a745;
        color: white;
    }

    .btn-success:hover {
        background-color: #218838;
    }

    .btn-secondary {
        background-color: #6c757d;
        color: white;
    }

    .btn-secondary:hover {
        background-color: #5a6268;
    }

    .funcionario-form-actions {
        display: flex;
        gap: 10px;
        margin-top: 30px;
    }

    .funcionario-form-actions > * {
        flex: 1;
        text-align: center;
    }

    .alert {
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
    }

    .alert-danger {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }

    .alert-success {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }

    @media (max-width: 640px) {
        .funcionario-form-page {
            padding: 28px 12px;
        }

        .funcionario-form-page h1 {
            margin-bottom: 20px;
            font-size: 24px;
        }

        .funcionario-form-actions {
            flex-direction: column;
            margin-top: 20px;
        }

        .funcionario-form-actions > * {
            width: 100%;
        }
    }
</style>
{% endblock %}
```

---

### Arquivo: `templates\funcionarios\editar.html`

```html
﻿{% extends "base.html" %}

{% block title %}Editar Funcionario - SystemLR{% endblock %}

{% block content %}
<div class="form-container funcionario-form-page">
    <div class="funcionario-form-wrap">
        <h1>Editar Funcionario</h1>

        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
                        {{ message }}
                        <button type="button" class="close" data-dismiss="alert">&times;</button>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        <form method="POST" action="{{ url_for('editar_funcionario', funcionario_id=funcionario.id) }}" class="form">
            {{ csrf_input|safe }}
            <div class="form-group">
                <label for="nome">Nome Completo <span class="required">*</span></label>
                <input type="text" id="nome" name="nome" class="form-control" value="{{ funcionario.nome }}" required autofocus>
            </div>

            <div class="form-group">
                <label for="email">Email <span class="required">*</span></label>
                <input type="email" id="email" name="email" class="form-control" value="{{ funcionario.email }}" required>
            </div>

            <div class="form-group">
                <label for="role">Perfil de Acesso
                    {% if funcionario_logado.role != 'admin' %}
                        <span class="hint">(apenas admin pode alterar)</span>
                    {% endif %}
                </label>
                <select id="role" name="role" class="form-control" {% if funcionario_logado.role != 'admin' %}disabled{% endif %}>
                    <option value="operador" {% if funcionario.role == 'operador' %}selected{% endif %}>Operador</option>
                    <option value="caixa" {% if funcionario.role == 'caixa' %}selected{% endif %}>Caixa</option>
                    <option value="gerente" {% if funcionario.role == 'gerente' %}selected{% endif %}>Gerente</option>
                    <option value="garcom" {% if funcionario.role == 'garcom' %}selected{% endif %}>Garcom</option>
                    {% if funcionario_logado.role == 'admin' %}
                        <option value="admin" {% if funcionario.role == 'admin' %}selected{% endif %}>Admin</option>
                    {% endif %}
                </select>
            </div>

            <div class="form-group">
                <label for="cargo">Cargo/Funcao (RH) <span class="required">*</span></label>
                <select id="cargo" name="cargo" class="form-control" required>
                    <option value="">Selecione um cargo</option>
                    {% for funcao in funcoes_rh %}
                        <option value="{{ funcao.nome }}" {% if funcionario.cargo == funcao.nome %}selected{% endif %}>{{ funcao.nome }}</option>
                    {% endfor %}
                    {% if funcionario.cargo and (funcionario.cargo not in funcoes_rh_nomes) %}
                        <option value="{{ funcionario.cargo }}" selected>{{ funcionario.cargo }}</option>
                    {% endif %}
                </select>
            </div>

            <div class="form-group">
                <label for="ativo">
                    <input type="checkbox" id="ativo" name="ativo" {% if funcionario.ativo %}checked{% endif %}>
                    Funcionario Ativo
                </label>
            </div>

            <hr class="funcionario-divider">

            <h4 class="funcionario-subtitle">Alterar Senha (opcional)</h4>

            <div class="form-group">
                <label for="nova_senha">Nova Senha</label>
                <input type="password" id="nova_senha" name="nova_senha" class="form-control" minlength="6" placeholder="Deixe vazio para manter a senha atual">
            </div>

            <div class="funcionario-form-actions">
                <button type="submit" class="btn btn-success">Salvar Alteracoes</button>
                <a href="{{ url_for('listar_funcionarios') }}" class="btn btn-secondary">Cancelar</a>
            </div>
        </form>
    </div>
</div>

<style>
    .funcionario-form-page {
        padding: 40px 20px;
        max-width: 1000px;
        margin: 0 auto;
    }

    .funcionario-form-wrap {
        max-width: 500px;
        margin: 0 auto;
    }

    .funcionario-form-page h1 {
        color: #343a40;
        margin-bottom: 30px;
        font-size: 28px;
    }

    .funcionario-subtitle {
        color: #343a40;
        margin-bottom: 20px;
        font-size: 16px;
    }

    .funcionario-divider {
        margin: 30px 0;
        border: none;
        border-top: 1px solid #dee2e6;
    }

    .form-group {
        margin-bottom: 20px;
    }

    .form-group label {
        display: block;
        margin-bottom: 8px;
        color: #343a40;
        font-weight: 600;
    }

    .form-group input[type="checkbox"] {
        margin-right: 8px;
        cursor: pointer;
    }

    .required {
        color: #dc3545;
    }

    .hint {
        color: #6c757d;
        font-size: 12px;
        font-weight: normal;
    }

    .form-control {
        width: 100%;
        padding: 12px;
        border: 2px solid #dee2e6;
        border-radius: 5px;
        font-size: 16px;
        font-family: inherit;
        transition: border-color 0.3s;
    }

    .form-control:focus {
        outline: none;
        border-color: #667eea;
    }

    .form-control:disabled {
        background-color: #f8f9fa;
        cursor: not-allowed;
    }

    .btn {
        padding: 12px 20px;
        border-radius: 5px;
        text-decoration: none;
        font-weight: 600;
        cursor: pointer;
        border: none;
        transition: all 0.3s;
        font-size: 16px;
    }

    .btn-success {
        background-color: #28a745;
        color: white;
    }

    .btn-success:hover {
        background-color: #218838;
    }

    .btn-secondary {
        background-color: #6c757d;
        color: white;
    }

    .btn-secondary:hover {
        background-color: #5a6268;
    }

    .funcionario-form-actions {
        display: flex;
        gap: 10px;
        margin-top: 30px;
    }

    .funcionario-form-actions > * {
        flex: 1;
        text-align: center;
    }

    .alert {
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
    }

    .alert-danger {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }

    .alert-success {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }

    @media (max-width: 640px) {
        .funcionario-form-page {
            padding: 28px 12px;
        }

        .funcionario-form-page h1 {
            margin-bottom: 20px;
            font-size: 24px;
        }

        .funcionario-form-actions {
            flex-direction: column;
            margin-top: 20px;
        }

        .funcionario-form-actions > * {
            width: 100%;
        }
    }
</style>
{% endblock %}

```

---

### Arquivo: `templates\funcionarios\listar.html`

```html
{% extends "base.html" %}

{% block title %}Funcionarios - SystemLR{% endblock %}

{% block content %}
<div class="container mt-5 funcionarios-list-page">
    <div class="page-header">
        <h1>Funcionarios</h1>
        {% if funcionario_logado.role == 'admin' %}
            <a href="{{ url_for('criar_funcionario') }}" class="btn btn-primary">Novo Funcionario</a>
        {% endif %}
    </div>

    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
                    {{ message }}
                    <button type="button" class="close" data-dismiss="alert">&times;</button>
                </div>
            {% endfor %}
        {% endif %}
    {% endwith %}

    {% if funcionarios %}
        <div class="table-responsive">
            <table class="table funcionarios-table">
                <thead>
                    <tr>
                        <th>Nome</th>
                        <th>Email</th>
                        <th>Perfil</th>
                        <th>Cargo RH</th>
                        <th class="text-center">Status</th>
                        <th class="text-center">Acoes</th>
                    </tr>
                </thead>
                <tbody>
                    {% for func in funcionarios %}
                        <tr>
                            <td data-label="Nome"><strong>{{ func.nome }}</strong></td>
                            <td data-label="Email" class="funcionario-email">{{ func.email }}</td>
                            <td data-label="Perfil">
                                <span class="funcionario-pill role-{{ func.role }}">{{ func.role.upper() }}</span>
                            </td>
                            <td data-label="Cargo RH">{{ func.cargo or '-' }}</td>
                            <td data-label="Status" class="text-center">
                                <span class="funcionario-pill status-{{ 'ativo' if func.ativo else 'inativo' }}">
                                    {{ 'ATIVO' if func.ativo else 'INATIVO' }}
                                </span>
                            </td>
                            <td data-label="Acoes" class="actions-cell funcionario-actions">
                                <a href="{{ url_for('editar_funcionario', funcionario_id=func.id) }}" class="btn-small btn-primary">Editar</a>
                                {% if funcionario_logado.role == 'admin' %}
                                    <a href="{{ url_for('editar_acessos_funcionario', funcionario_id=func.id) }}" class="btn-small btn-success">Acessos</a>
                                {% endif %}
                                {% if func.id != funcionario_logado.id and funcionario_logado.role == 'admin' %}
                                    <form method="POST" action="{{ url_for('deletar_funcionario', funcionario_id=func.id) }}" class="funcionario-inline-form" data-confirm-message="Tem certeza que deseja deletar {{ func.nome }}?">
                                        {{ csrf_input|safe }}
                                        <button type="submit" class="btn-small btn-danger">Deletar</button>
                                    </form>
                                {% endif %}
                            </td>
                        </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    {% else %}
        <div class="funcionario-empty">
            <p>Nenhum funcionario cadastrado.</p>
            {% if funcionario_logado.role == 'admin' %}
                <a href="{{ url_for('criar_funcionario') }}">Criar o primeiro funcionario</a>
            {% endif %}
        </div>
    {% endif %}
</div>

<style>
    .funcionarios-list-page {
        max-width: 1100px;
        margin: 0 auto;
    }

    .funcionarios-table th,
    .funcionarios-table td {
        vertical-align: middle;
    }

    .funcionario-email {
        overflow-wrap: anywhere;
    }

    .funcionario-pill {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        border-radius: 999px;
        padding: 4px 10px;
        font-size: 12px;
        font-weight: 700;
        color: #fff;
        line-height: 1.3;
    }

    .role-admin {
        background-color: #dc3545;
    }

    .role-gerente {
        background-color: #f59e0b;
        color: #111827;
    }

    .role-caixa {
        background-color: #0ea5e9;
    }

    .role-garcom {
        background-color: #14b8a6;
    }

    .role-operador {
        background-color: #64748b;
    }

    .status-ativo {
        background-color: #16a34a;
    }

    .status-inativo {
        background-color: #dc3545;
    }

    .funcionario-actions {
        justify-content: center;
        gap: 6px;
        flex-wrap: wrap;
    }

    .funcionario-inline-form {
        display: inline;
        margin: 0;
    }

    .funcionario-empty {
        background-color: #f8f9fa;
        padding: 30px;
        border-radius: 8px;
        text-align: center;
        color: #6c757d;
    }

    .funcionario-empty p {
        margin: 0;
        font-size: 16px;
    }

    .funcionario-empty a {
        display: inline-block;
        margin-top: 10px;
        color: #0f766e;
        font-weight: 600;
        text-decoration: none;
    }

    .funcionario-empty a:hover {
        text-decoration: underline;
    }

    @media (max-width: 768px) {
        .funcionarios-list-page {
            margin-top: 0;
        }

        .funcionarios-table td[data-label="Acoes"] {
            text-align: left;
        }
    }
</style>
{% endblock %}
```

---

### Arquivo: `templates\public\abrir_comanda.html`

```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="csrf-token" content="{{ csrf_token }}">
    <title>Abrir Comanda - Mesa {{ mesa.numero }}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body class="public-menu">
    <div class="container narrow">
        <div class="form-container">
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <div class="alert alert-{{ category }}">{{ message }}</div>
                    {% endfor %}
                {% endif %}
            {% endwith %}

            {% if empresa and empresa.logo_path %}
            <div style="text-align:center; margin-bottom:10px;">
                <img src="{{ url_for('static', filename=empresa.logo_path) }}" alt="Logo da empresa" style="max-height:72px; width:auto;">
            </div>
            {% endif %}
            <h1>{{ (empresa.cardapio_titulo if empresa and empresa.cardapio_titulo else ('Abrir Comanda - Mesa ' ~ mesa.numero)) }}</h1>
            <p class="text-muted">Para iniciar seu pedido, informe seus dados.</p>

            <form method="POST" action="{{ url_for('public.abrir_comanda_qr', token=mesa.qr_token) }}" class="form">
                {{ csrf_input|safe }}
                <div class="form-group">
                    <label for="cliente_nome">Nome</label>
                    <input type="text" id="cliente_nome" name="cliente_nome" required class="input-text" maxlength="120">
                </div>

                <div class="form-group">
                    <label for="cliente_celular">Celular</label>
                    <input type="text" id="cliente_celular" name="cliente_celular" required class="input-text" maxlength="30" placeholder="(xx) xxxxx-xxxx">
                </div>

                <button type="submit" class="btn btn-primary btn-block">Abrir Comanda</button>
            </form>
        </div>
    </div>
    <script src="{{ url_for('static', filename='js/csrf.js') }}"></script>
</body>
</html>
```

---

### Arquivo: `templates\public\cardapio.html`

```html
﻿<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="csrf-token" content="{{ csrf_token }}">
    <title>Comanda Mesa {{ mesa.numero }}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/pages/cardapio.css') }}">
</head>
<body class="public-menu">
    <div class="menu-shell">
        <section class="menu-top">
            {% if empresa and empresa.logo_path %}
            <div class="menu-logo-wrap">
                <img src="{{ url_for('static', filename=empresa.logo_path) }}" alt="Logo da empresa" class="menu-logo">
            </div>
            {% endif %}
            <h1>{{ (empresa.cardapio_titulo if empresa and empresa.cardapio_titulo else ('Comanda - Mesa ' ~ mesa.numero)) }}</h1>
            <p class="menu-subtitle">{{ (empresa.cardapio_subtitulo if empresa and empresa.cardapio_subtitulo else 'Escolha os itens por categoria e envie novos pedidos quando quiser.') }}</p>
            <div class="menu-client">
                Mesa {{ mesa.numero }} | {{ cliente_nome }} | {{ cliente_celular }}
            </div>
        </section>

        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                <div class="flash-stack">
                    {% for category, message in messages %}
                        <div class="alert alert-{{ category }}">{{ message }}</div>
                    {% endfor %}
                </div>
            {% endif %}
        {% endwith %}

        <div class="menu-grid">
            <section class="menu-panel">
                <h2>Fazer pedido</h2>
                <div class="category-filter" id="categoryFilter">
                    <button type="button" class="category-pill active" data-category="all">Todas</button>
                    {% for bloco in categorias_cardapio %}
                    <button type="button" class="category-pill" data-category="cat-{{ bloco.categoria.id }}">{{ bloco.categoria.nome }}</button>
                    {% endfor %}
                </div>

                <form method="POST" action="{% if preview_mode %}#{% else %}{{ url_for('public.enviar_pedido_qr', mesa_numero=mesa.numero, cliente_slug=cliente_slug) }}{% endif %}" {% if preview_mode %}onsubmit="return false;"{% endif %}>
                    {{ csrf_input|safe }}
                    {% if categorias_cardapio %}
                    {% for bloco in categorias_cardapio %}
                    <article class="category-section" data-category-id="cat-{{ bloco.categoria.id }}">
                        <header class="category-header {% if not bloco.categoria.imagem_path %}no-image{% endif %}">
                            {% if bloco.categoria.imagem_path %}
                            <img src="{{ url_for('static', filename=bloco.categoria.imagem_path) }}" alt="{{ bloco.categoria.nome }}" class="category-image">
                            {% endif %}
                            <div>
                                <h3 class="category-title">{{ bloco.categoria.nome }}</h3>
                                <p class="category-desc">{{ bloco.categoria.descricao or 'Selecao especial desta categoria.' }}</p>
                            </div>
                        </header>

                        <div class="product-list">
                            {% for produto in bloco.produtos %}
                            <div class="product-item {% if not ((not empresa or empresa.cardapio_mostrar_imagem != False) and produto.imagem_path) %}no-image{% endif %}">
                                {% if (not empresa or empresa.cardapio_mostrar_imagem != False) and produto.imagem_path %}
                                <img src="{{ url_for('static', filename=produto.imagem_path) }}" alt="{{ produto.nome }}" class="product-image">
                                {% endif %}
                                <div>
                                    <h4 class="product-name">{{ produto.nome }}</h4>
                                    {% if not empresa or empresa.cardapio_mostrar_descricao != False %}
                                    <p class="product-desc">{{ produto.descricao or 'Sem descricao' }}</p>
                                    {% endif %}
                                    <div class="product-price">R$ {{ '%.2f'|format(produto.preco_venda) }}</div>
                                </div>
                                <div class="product-qtd">
                                    <label for="produto_{{ produto.id }}">Qtd</label>
                                    <input id="produto_{{ produto.id }}" type="number" name="produto_{{ produto.id }}" min="0" max="{{ qtd_max }}" value="0" class="form-control" {% if preview_mode %}disabled{% endif %}>
                                </div>
                            </div>
                            {% endfor %}
                        </div>
                    </article>
                    {% endfor %}
                    {% else %}
                    <div class="empty-box">
                        Nenhum produto disponivel no momento.
                    </div>
                    {% endif %}

                    <div class="submit-wrap">
                        <button type="submit" class="btn btn-primary btn-block" {% if preview_mode %}disabled{% endif %}>
                            {% if preview_mode %}Visualizacao (modo cliente){% else %}Enviar pedido{% endif %}
                        </button>
                    </div>
                </form>
            </section>

            <aside class="menu-panel">
                <h2>{% if preview_mode %}Area de pedidos do cliente{% else %}Meus pedidos{% endif %}</h2>
                {% if pedidos_cliente %}
                <div class="orders-list">
                    {% for pedido in pedidos_cliente %}
                    <article class="order-card">
                        <div class="order-head">
                            <strong>Pedido #{{ pedido.id }}</strong>
                            <span class="order-status {{ pedido.status }}">{{ pedido.status_label }}</span>
                        </div>
                        <ul class="order-items">
                            {% for item in pedido.itens %}
                            <li>{{ item.quantidade }}x {{ item.produto.nome if item.produto else 'Item removido' }}</li>
                            {% endfor %}
                        </ul>
                        <div class="order-meta">
                            {{ pedido.criado_em.strftime('%d/%m/%Y %H:%M') if pedido.criado_em else '-' }} | Total R$ {{ '%.2f'|format(pedido.total or 0) }}
                        </div>
                    </article>
                    {% endfor %}
                </div>
                {% else %}
                <div class="empty-box">
                    {% if preview_mode %}Sem pedidos na visualizacao de exemplo.{% else %}Voce ainda nao fez pedidos nesta comanda.{% endif %}
                </div>
                {% endif %}
            </aside>
        </div>
    </div>

    <script src="{{ url_for('static', filename='js/csrf.js') }}"></script>
    <script>
        (function () {
            const filter = document.getElementById('categoryFilter');
            if (!filter) return;

            const pills = Array.from(filter.querySelectorAll('.category-pill'));
            const sections = Array.from(document.querySelectorAll('.category-section'));

            function applyFilter(key) {
                sections.forEach((section) => {
                    const sectionKey = section.getAttribute('data-category-id');
                    section.style.display = (key === 'all' || key === sectionKey) ? '' : 'none';
                });
                pills.forEach((pill) => pill.classList.toggle('active', pill.dataset.category === key));
            }

            pills.forEach((pill) => {
                pill.addEventListener('click', () => applyFilter(pill.dataset.category));
            });
        })();
    </script>
</body>
</html>

```

---

### Arquivo: `templates\public\pedido_enviado.html`

```html
﻿<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="csrf-token" content="{{ csrf_token }}">
    <title>Pedido enviado</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body class="public-menu">
    <div class="container narrow">
        {% if empresa and empresa.logo_path %}
        <div style="text-align:center; margin-bottom:10px;">
            <img src="{{ url_for('static', filename=empresa.logo_path) }}" alt="Logo da empresa" style="max-height:72px; width:auto;">
        </div>
        {% endif %}
        <h1>Pedido recebido!</h1>
        <p>Seu pedido foi enviado para a equipe. Numero da mesa: <strong>{{ mesa.numero }}</strong></p>
        <p>Status inicial: <strong>{{ pedido.status }}</strong></p>
        <p class="text-muted">{{ (empresa.cardapio_mensagem if empresa and empresa.cardapio_mensagem else 'Um garcom ira confirmar e iniciar o preparo.') }}</p>
    </div>
</body>
</html>
```

---

### Arquivo: `templates\rh\editar_funcao.html`

```html
{% extends "base.html" %}

{% block title %}Editar Funcao RH - SystemLR{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Editar Funcao RH</h1>
    <a href="{{ url_for('listar_funcoes_rh') }}" class="btn btn-secondary">Voltar</a>
</div>

<div class="form-container">
    <form method="POST" class="form">
        {{ csrf_input|safe }}
        <div class="form-group">
            <label for="nome">Nome da Funcao *</label>
            <input type="text" id="nome" name="nome" class="input-text" maxlength="100" required value="{{ funcao.nome }}">
        </div>

        <div class="form-group">
            <label for="descricao">Descricao</label>
            <input type="text" id="descricao" name="descricao" class="input-text" maxlength="255" value="{{ funcao.descricao or '' }}">
        </div>

        <div class="form-group">
            <label class="checkbox-inline">
                <input type="checkbox" name="ativo" {% if funcao.ativo %}checked{% endif %}>
                Funcao ativa
            </label>
        </div>

        <div class="form-actions">
            <button type="submit" class="btn btn-primary">Salvar Alteracoes</button>
            <a href="{{ url_for('listar_funcoes_rh') }}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>
{% endblock %}
```

---

### Arquivo: `templates\rh\funcoes.html`

```html
﻿{% extends "base.html" %}

{% block title %}Funcoes RH - SystemLR{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Funcoes - Meu RH</h1>
</div>

<div class="card">
    <div class="card-header">Nova Funcao</div>
    <div class="card-body">
        <form method="POST" action="{{ url_for('nova_funcao_rh') }}" class="form">
            {{ csrf_input|safe }}
            <div class="form-row">
                <div class="form-group">
                    <label for="nome">Nome da Funcao *</label>
                    <input type="text" id="nome" name="nome" class="input-text" maxlength="100" required placeholder="Ex: Atendente, Supervisor, Estoquista">
                </div>
                <div class="form-group">
                    <label for="descricao">Descricao</label>
                    <input type="text" id="descricao" name="descricao" class="input-text" maxlength="255" placeholder="Descricao resumida da funcao">
                </div>
            </div>
            <div class="form-group">
                <label class="checkbox-inline">
                    <input type="checkbox" name="ativo" checked>
                    Funcao ativa
                </label>
            </div>
            <div class="form-actions">
                <button type="submit" class="btn btn-primary">Salvar Funcao</button>
            </div>
        </form>
    </div>
</div>

<div class="section">
    <h2>Funcoes Cadastradas</h2>
    <div class="table-responsive">
        <table class="table">
            <thead>
                <tr>
                    <th>Nome</th>
                    <th>Descricao</th>
                    <th>Status</th>
                    <th>Criado em</th>
                    <th>Acoes</th>
                </tr>
            </thead>
            <tbody>
                {% for funcao in funcoes %}
                <tr>
                    <td data-label="Nome"><strong>{{ funcao.nome }}</strong></td>
                    <td data-label="Descricao">{{ funcao.descricao or '-' }}</td>
                    <td data-label="Status">
                        {% if funcao.ativo %}
                        <span class="badge badge-success">Ativa</span>
                        {% else %}
                        <span class="badge badge-danger">Inativa</span>
                        {% endif %}
                    </td>
                    <td data-label="Criado em">{{ funcao.criado_em.strftime('%d/%m/%Y %H:%M') if funcao.criado_em else '-' }}</td>
                    <td data-label="Acoes" class="actions-cell">
                        <a href="{{ url_for('editar_funcao_rh', funcao_id=funcao.id) }}" class="btn-small btn-warning">Editar</a>
                        <form method="POST" action="{{ url_for('deletar_funcao_rh', funcao_id=funcao.id) }}" class="inline-form" data-confirm-message="Excluir funcao {{ funcao.nome }}?">
                            {{ csrf_input|safe }}
                            <button type="submit" class="btn-small btn-danger">Excluir</button>
                        </form>
                    </td>
                </tr>
                {% else %}
                <tr>
                    <td colspan="5" class="text-center">Nenhuma funcao cadastrada.</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}

```

---

### Arquivo: `templates\rh\indicadores.html`

```html
{% extends "base.html" %}

{% block title %}Indicadores RH - SystemLR{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Indicadores RH</h1>
</div>

<div class="cards-container analytics-cards">
    <div class="card card-primary">
        <div class="card-content">
            <h3>Total de Funcionarios</h3>
            <p class="card-value">{{ total_funcionarios }}</p>
            <p class="card-meta">{{ funcionarios_ativos }} ativos / {{ funcionarios_inativos }} inativos</p>
        </div>
    </div>
    <div class="card card-success">
        <div class="card-content">
            <h3>Admissoes (30 dias)</h3>
            <p class="card-value">{{ admissoes_30_dias }}</p>
            <p class="card-meta">Novos cadastros de funcionarios</p>
        </div>
    </div>
    <div class="card card-info">
        <div class="card-content">
            <h3>Funcoes RH</h3>
            <p class="card-value">{{ funcoes_total }}</p>
            <p class="card-meta">{{ funcoes_ativas }} funcoes ativas</p>
        </div>
    </div>
    <div class="card card-warning">
        <div class="card-content">
            <h3>Controle de Acesso</h3>
            <p class="card-value">{{ acessos_controlados }}</p>
            <p class="card-meta">Funcionarios com acesso customizado</p>
        </div>
    </div>
</div>

<div class="section">
    <div class="page-header">
        <h2>Graficos Dinamicos RH</h2>
        <div class="header-actions">
            <select id="rhPeriodo" class="input-select">
                <option value="30" selected>Ultimos 30 dias</option>
                <option value="90">Ultimos 90 dias</option>
                <option value="365">Ultimos 365 dias</option>
            </select>
        </div>
    </div>
    <div class="analytics-grid">
        <section class="section">
            <h2>Distribuicao por Perfil</h2>
            <div class="chart-container">
                <canvas id="chartRhPerfis"></canvas>
            </div>
        </section>
        <section class="section">
            <h2>Admissoes no Periodo</h2>
            <div class="chart-container">
                <canvas id="chartRhAdmissoes"></canvas>
            </div>
        </section>
    </div>
</div>

<div class="analytics-grid">
    <section class="section">
        <h2>Distribuicao por Perfil</h2>
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Perfil</th>
                        <th>Quantidade</th>
                    </tr>
                </thead>
                <tbody>
                    {% for item in distribuicao_roles %}
                    <tr>
                        <td data-label="Perfil">{{ item.role|upper }}</td>
                        <td data-label="Quantidade">{{ item.quantidade }}</td>
                    </tr>
                    {% else %}
                    <tr>
                        <td colspan="2" class="text-center">Sem dados de perfis.</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </section>

    <section class="section">
        <h2>Ultimos Funcionarios Cadastrados</h2>
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Nome</th>
                        <th>Email</th>
                        <th>Perfil</th>
                        <th>Status</th>
                        <th>Cadastro</th>
                    </tr>
                </thead>
                <tbody>
                    {% for funcionario in funcionarios_recentes %}
                    <tr>
                        <td data-label="Nome">{{ funcionario.nome }}</td>
                        <td data-label="Email">{{ funcionario.email }}</td>
                        <td data-label="Perfil">{{ funcionario.role|upper }}</td>
                        <td data-label="Status">
                            {% if funcionario.ativo %}
                            <span class="badge badge-success">Ativo</span>
                            {% else %}
                            <span class="badge badge-danger">Inativo</span>
                            {% endif %}
                        </td>
                        <td data-label="Cadastro">{{ funcionario.criado_em.strftime('%d/%m/%Y %H:%M') if funcionario.criado_em else '-' }}</td>
                    </tr>
                    {% else %}
                    <tr>
                        <td colspan="5" class="text-center">Nenhum funcionario cadastrado.</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </section>
</div>

<div class="action-buttons">
    <a href="{{ url_for('listar_funcionarios') }}" class="btn btn-primary">Funcionarios</a>
    <a href="{{ url_for('listar_funcoes_rh') }}" class="btn btn-secondary">Funcoes RH</a>
</div>
{% endblock %}

{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js"></script>
<script src="{{ url_for('static', filename='js/pages/rh_analytics.js') }}"></script>
{% endblock %}
```

---

### Arquivo: `templates\sistema\acessos.html`

```html
{% extends "base.html" %}

{% block title %}Gestao de Acessos - SystemLR{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Gestao de Acessos</h1>
</div>

<div class="section">
    <p>Selecione as paginas que cada usuario pode acessar. Ao salvar, o controle de acesso e ativado para esse usuario.</p>
</div>

<div class="grid-container">
    {% for funcionario in funcionarios %}
    <div class="card-category">
        <div class="card-category-header">
            <h3>{{ funcionario.nome }}</h3>
            <span class="badge">{{ funcionario.role }}</span>
        </div>
        <p class="card-category-desc">{{ funcionario.email }}</p>

        <form method="POST" action="{{ url_for('salvar_acessos_funcionario', funcionario_id=funcionario.id) }}">
            {{ csrf_input|safe }}
            <div class="form-group" style="gap:8px;">
                {% for chave, rotulo in paginas_sistema.items() %}
                <label>
                    <input
                        type="checkbox"
                        name="paginas"
                        value="{{ chave }}"
                        {% if funcionario.id in permissoes_por_funcionario and chave in permissoes_por_funcionario[funcionario.id] %}checked{% endif %}
                        {% if funcionario.role == 'admin' %}disabled{% endif %}
                    >
                    {{ rotulo }}
                </label>
                {% endfor %}
            </div>

            {% if funcionario.role == 'admin' %}
            <p class="text-center">Admin possui acesso total.</p>
            {% else %}
            <div class="form-actions">
                <button type="submit" class="btn btn-primary">Salvar acessos</button>
            </div>
            {% endif %}
        </form>
    </div>
    {% endfor %}
</div>
{% endblock %}
```

---

### Arquivo: `templates\sistema\auditoria.html`

```html
{% extends "base.html" %}

{% block title %}Auditoria do Sistema - SystemLR{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Auditoria do Sistema</h1>
</div>

<section class="section">
    <form method="GET" class="filters-form">
        <div class="filter-group">
            <label for="funcionario_id">Usuario</label>
            <select id="funcionario_id" name="funcionario_id" class="input-select">
                <option value="">Todos</option>
                {% for funcionario in funcionarios %}
                <option value="{{ funcionario.id }}" {% if filtros.funcionario_id == funcionario.id %}selected{% endif %}>
                    {{ funcionario.nome }} ({{ funcionario.role }})
                </option>
                {% endfor %}
            </select>
        </div>
        <div class="filter-group">
            <label for="metodo">Metodo</label>
            <select id="metodo" name="metodo" class="input-select">
                <option value="">Todos</option>
                {% for metodo in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'] %}
                <option value="{{ metodo }}" {% if filtros.metodo == metodo %}selected{% endif %}>{{ metodo }}</option>
                {% endfor %}
            </select>
        </div>
        <div class="filter-group">
            <label for="entidade">Entidade</label>
            <input type="text" id="entidade" name="entidade" class="input-text" value="{{ filtros.entidade }}">
        </div>
        <div class="filter-group">
            <label for="acao">Acao</label>
            <input type="text" id="acao" name="acao" class="input-text" value="{{ filtros.acao }}">
        </div>
        <div class="form-actions">
            <button type="submit" class="btn btn-primary">Filtrar</button>
            <a href="{{ url_for('auditoria_sistema') }}" class="btn btn-secondary">Limpar</a>
        </div>
    </form>
</section>

<div class="table-responsive">
    <table class="table">
        <thead>
            <tr>
                <th>Data/Hora</th>
                <th>Usuario</th>
                <th>Metodo</th>
                <th>Rota</th>
                <th>Acao</th>
                <th>Status</th>
                <th>Detalhes</th>
            </tr>
        </thead>
        <tbody>
            {% for evento in eventos %}
            <tr>
                <td data-label="Data/Hora">{{ evento.criado_em.strftime('%d/%m/%Y %H:%M:%S') if evento.criado_em else '-' }}</td>
                <td data-label="Usuario">
                    {{ evento.funcionario_nome or 'Nao identificado' }}
                    {% if evento.funcionario_role %}<br><small>{{ evento.funcionario_role }}</small>{% endif %}
                </td>
                <td data-label="Metodo">{{ evento.metodo }}</td>
                <td data-label="Rota">{{ evento.rota }}</td>
                <td data-label="Acao">{{ evento.acao }}</td>
                <td data-label="Status">{{ evento.status_code or '-' }}</td>
                <td data-label="Detalhes">{{ evento.detalhes or '-' }}</td>
            </tr>
            {% else %}
            <tr>
                <td colspan="7" class="text-center">Nenhum evento de auditoria encontrado.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
```

---

### Arquivo: `templates\sistema\boas_vindas.html`

```html
﻿{% extends "base.html" %}

{% block title %}Boas-vindas - SystemLR{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Bem-vindo ao {{ app_name }}</h1>
</div>

<div class="section">
    <h2>Informacoes Gerais</h2>
    <p><strong>Sistema:</strong> {{ app_name }}</p>
    <p><strong>Versao:</strong> {{ app_version }}</p>
    <p><strong>Dominio:</strong> {{ app_domain }}</p>
    <p><strong>Criador:</strong> Lucas Ramalho</p>
    <p><strong>Telefone:</strong> 67 981029292</p>
    <p><strong>Total de Produtos:</strong> {{ total_produtos }}</p>
    <p><strong>Total de Categorias:</strong> {{ total_categorias }}</p>
</div>

<div class="action-buttons">
    <a href="{{ url_for('dashboard') }}" class="btn btn-primary">Ir para Dashboard</a>
    <a href="{{ url_for('listar_produtos') }}" class="btn btn-secondary">Ver Produtos</a>
    <a href="{{ url_for('relatorios') }}" class="btn btn-info">Ver Relatorios</a>
</div>
{% endblock %}
```

---

### Arquivo: `templates\sistema\empresa.html`

```html
{% extends "base.html" %}

{% block title %}Dados da Empresa - SystemLR{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Cadastro da Empresa</h1>
</div>

<div class="form-container">
    <form method="POST" enctype="multipart/form-data" class="form">
        {{ csrf_input|safe }}
        <div class="form-group">
            <label for="logo">Logo da Empresa</label>
            <input type="file" id="logo" name="logo" accept=".png,.jpg,.jpeg,.webp,.gif" class="input-text">
            {% if empresa and empresa.logo_path %}
            <div class="product-image-preview">
                <img src="{{ url_for('static', filename=empresa.logo_path) }}" alt="Logo da empresa">
                <label class="checkbox-inline">
                    <input type="checkbox" name="remover_logo">
                    Remover logo atual
                </label>
            </div>
            {% endif %}
        </div>
        <div class="form-row">
            <div class="form-group">
                <label for="razao_social">Razão Social</label>
                <input type="text" id="razao_social" name="razao_social" value="{{ empresa.razao_social if empresa else '' }}" class="input-text">
            </div>
            <div class="form-group">
                <label for="nome_fantasia">Nome Fantasia</label>
                <input type="text" id="nome_fantasia" name="nome_fantasia" value="{{ empresa.nome_fantasia if empresa else '' }}" class="input-text">
            </div>
        </div>

        <div class="form-row">
            <div class="form-group">
                <label for="cnpj">CNPJ</label>
                <input type="text" id="cnpj" name="cnpj" value="{{ empresa.cnpj if empresa else '' }}" class="input-text">
            </div>
            <div class="form-group">
                <label for="inscricao_estadual">Inscrição Estadual</label>
                <input type="text" id="inscricao_estadual" name="inscricao_estadual" value="{{ empresa.inscricao_estadual if empresa else '' }}" class="input-text">
            </div>
        </div>

        <div class="form-row">
            <div class="form-group">
                <label for="telefone">Telefone</label>
                <input type="text" id="telefone" name="telefone" value="{{ empresa.telefone if empresa else '' }}" class="input-text">
            </div>
            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" id="email" name="email" value="{{ empresa.email if empresa else '' }}" class="input-text">
            </div>
        </div>

        <div class="form-group">
            <label for="endereco">Endereço</label>
            <input type="text" id="endereco" name="endereco" value="{{ empresa.endereco if empresa else '' }}" class="input-text">
        </div>

        <div class="form-row">
            <div class="form-group">
                <label for="cidade">Cidade</label>
                <input type="text" id="cidade" name="cidade" value="{{ empresa.cidade if empresa else '' }}" class="input-text">
            </div>
            <div class="form-group">
                <label for="estado">UF</label>
                <input type="text" id="estado" name="estado" maxlength="2" value="{{ empresa.estado if empresa else '' }}" class="input-text">
            </div>
            <div class="form-group">
                <label for="cep">CEP</label>
                <input type="text" id="cep" name="cep" value="{{ empresa.cep if empresa else '' }}" class="input-text">
            </div>
        </div>

        <div class="form-group">
            <label for="mensagem_comprovante">Mensagem no Comprovante</label>
            <textarea id="mensagem_comprovante" name="mensagem_comprovante" rows="3" class="input-textarea">{{ empresa.mensagem_comprovante if empresa else '' }}</textarea>
        </div>

        <div id="config-cardapio" class="section" style="margin: 0;">
            <h2>Configuração da Comanda QR</h2>

            <div class="form-row">
                <label class="checkbox-inline">
                    <input type="checkbox" name="atendimento_mesas_ativo" {% if not empresa or empresa.atendimento_mesas_ativo != False %}checked{% endif %}>
                    Ativar atendimento por mesas e garcons (comanda QR)
                </label>
            </div>

            <div class="form-group">
                <label for="cardapio_titulo">Título da comanda</label>
                <input type="text" id="cardapio_titulo" name="cardapio_titulo" value="{{ empresa.cardapio_titulo if empresa else '' }}" class="input-text">
            </div>

            <div class="form-group">
                <label for="cardapio_subtitulo">Subtítulo da comanda</label>
                <input type="text" id="cardapio_subtitulo" name="cardapio_subtitulo" value="{{ empresa.cardapio_subtitulo if empresa else '' }}" class="input-text">
            </div>

            <div class="form-group">
                <label for="cardapio_mensagem">Mensagem após envio do pedido</label>
                <input type="text" id="cardapio_mensagem" name="cardapio_mensagem" value="{{ empresa.cardapio_mensagem if empresa else '' }}" class="input-text">
            </div>

            <div class="form-row">
                <div class="form-group">
                    <label for="cardapio_qtd_maxima">Quantidade máxima por item</label>
                    <input type="number" id="cardapio_qtd_maxima" name="cardapio_qtd_maxima" min="1" max="999" value="{{ empresa.cardapio_qtd_maxima if empresa and empresa.cardapio_qtd_maxima else 20 }}" class="input-text">
                </div>
            </div>

            <div class="form-row">
                <label class="checkbox-inline">
                    <input type="checkbox" name="cardapio_mostrar_imagem" {% if not empresa or empresa.cardapio_mostrar_imagem != False %}checked{% endif %}>
                    Mostrar imagem dos produtos na comanda
                </label>
                <label class="checkbox-inline">
                    <input type="checkbox" name="cardapio_mostrar_descricao" {% if not empresa or empresa.cardapio_mostrar_descricao != False %}checked{% endif %}>
                    Mostrar descrição dos produtos na comanda
                </label>
            </div>

            <div class="form-actions" style="margin-top: 12px;">
                <a href="{{ url_for('preview_cardapio_empresa') }}" target="_blank" class="btn btn-secondary">Visualizar cardapio como cliente</a>
            </div>
        </div>

        <div class="form-actions">
            <button type="submit" class="btn btn-success">Salvar Dados</button>
        </div>
    </form>
</div>
{% endblock %}

```

---

### Arquivo: `templates\sistema\login.html`

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="csrf-token" content="{{ csrf_token }}">
    <title>Login - SystemLR</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .container {
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
            width: 100%;
            max-width: 400px;
        }
        
        .login-header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .login-header h1 {
            color: #667eea;
            font-size: 28px;
            margin-bottom: 5px;
        }
        
        .login-header p {
            color: #6c757d;
            font-size: 14px;
        }
        
        .form-group {
            margin-bottom: 16px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 6px;
            color: #343a40;
            font-weight: 600;
            font-size: 14px;
        }
        
        .form-group input {
            width: 100%;
            padding: 10px 12px;
            border: 2px solid #dee2e6;
            border-radius: 5px;
            font-size: 14px;
            font-family: inherit;
            transition: border-color 0.3s;
        }
        
        .form-group input:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .alerts {
            margin-bottom: 20px;
        }
        
        .alert {
            padding: 12px;
            border-radius: 5px;
            font-size: 14px;
            margin-bottom: 10px;
        }
        
        .alert-danger {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .alert-warning {
            background-color: #fff3cd;
            color: #856404;
            border: 1px solid #ffeeba;
        }
        
        .alert-info {
            background-color: #d1ecf1;
            color: #334155;
            border: 1px solid #bee5eb;
        }
        
        .btn {
            width: 100%;
            padding: 12px;
            background-color: #667eea;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.3s;
            margin-bottom: 10px;
        }
        
        .btn:hover {
            background-color: #5568d3;
        }
        
        .btn:active {
            transform: scale(0.98);
        }
        
        .login-footer {
            text-align: center;
            margin-top: 20px;
            color: #6c757d;
            font-size: 14px;
        }
        
        .login-footer a {
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
        }
        
        .login-footer a:hover {
            text-decoration: underline;
        }
        
        @media (max-width: 480px) {
            .container {
                padding: 20px;
            }
            
            .login-header h1 {
                font-size: 24px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="login-header">
            <h1>SystemLR</h1>
            <p>Sistema de Gerenciamento</p>
        </div>
        
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                <div class="alerts">
                    {% for category, message in messages %}
                        <div class="alert alert-{{ category }}">
                            {{ message }}
                        </div>
                    {% endfor %}
                </div>
            {% endif %}
        {% endwith %}
        
        <form method="POST" action="{{ url_for('login') }}">
            {{ csrf_input|safe }}
            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" id="email" name="email" required autofocus>
            </div>
            
            <div class="form-group">
                <label for="senha">Senha</label>
                <input type="password" id="senha" name="senha" required>
            </div>
            
            <button type="submit" class="btn">Fazer Login</button>
        </form>
        
        <div class="login-footer">
            <p>Primeira vez aqui? <a href="{{ url_for('registro') }}">Criar conta</a></p>
        </div>
    </div>
    <script src="{{ url_for('static', filename='js/csrf.js') }}"></script>
</body>
</html>
```

---

### Arquivo: `templates\sistema\registro.html`

```html
﻿<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="csrf-token" content="{{ csrf_token }}">
    <title>Registro - SystemLR</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
            width: 100%;
            max-width: 400px;
        }
        
        .registro-header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .registro-header h1 {
            color: #667eea;
            font-size: 28px;
            margin-bottom: 5px;
        }
        
        .registro-header p {
            color: #6c757d;
            font-size: 14px;
        }
        
        .form-group {
            margin-bottom: 16px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 6px;
            color: #343a40;
            font-weight: 600;
            font-size: 14px;
        }
        
        .form-group input,
        .form-group select {
            width: 100%;
            padding: 10px 12px;
            border: 2px solid #dee2e6;
            border-radius: 5px;
            font-size: 14px;
            font-family: inherit;
            transition: border-color 0.3s;
        }
        
        .form-group input:focus,
        .form-group select:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .alerts {
            margin-bottom: 20px;
        }
        
        .alert {
            padding: 12px;
            border-radius: 5px;
            font-size: 14px;
            margin-bottom: 10px;
        }
        
        .alert-danger {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .alert-warning {
            background-color: #fff3cd;
            color: #856404;
            border: 1px solid #ffeeba;
        }
        
        .alert-info {
            background-color: #d1ecf1;
            color: #334155;
            border: 1px solid #bee5eb;
        }
        
        .btn {
            width: 100%;
            padding: 12px;
            background-color: #667eea;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.3s;
            margin-bottom: 10px;
        }
        
        .btn:hover {
            background-color: #5568d3;
        }
        
        .btn:active {
            transform: scale(0.98);
        }
        
        .btn-secondary {
            background-color: #343a40;
        }
        
        .btn-secondary:hover {
            background-color: #555555;
        }
        
        .registro-footer {
            text-align: center;
            margin-top: 20px;
            color: #6c757d;
            font-size: 14px;
        }
        
        .registro-footer a {
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
        }
        
        .registro-footer a:hover {
            text-decoration: underline;
        }
        
        .info-text {
            background-color: #e7ebf6;
            border-left: 4px solid #667eea;
            padding: 12px;
            margin-bottom: 20px;
            border-radius: 3px;
            font-size: 13px;
            color: #334155;
        }
        
        @media (max-width: 480px) {
            .container {
                padding: 20px;
            }
            
            .registro-header h1 {
                font-size: 24px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="registro-header">
            <h1>SystemLR</h1>
            <p>{% if primeira_vez %}Criar Conta Admin{% else %}Registrar Novo FuncionÃ¡rio{% endif %}</p>
        </div>
        
        {% if primeira_vez %}
            <div class="info-text">
                â„¹ï¸ Esta Ã© sua primeira vez. Crie a conta do administrador do sistema.
            </div>
        {% endif %}
        
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                <div class="alerts">
                    {% for category, message in messages %}
                        <div class="alert alert-{{ category }}">
                            {{ message }}
                        </div>
                    {% endfor %}
                </div>
            {% endif %}
        {% endwith %}
        
        <form method="POST" action="{{ url_for('registro') }}">
            {{ csrf_input|safe }}
            <div class="form-group">
                <label for="nome">Nome Completo</label>
                <input type="text" id="nome" name="nome" required autofocus>
            </div>
            
            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" id="email" name="email" required>
            </div>
            
            <div class="form-group">
                <label for="senha">Senha</label>
                <input type="password" id="senha" name="senha" required minlength="6" placeholder="MÃ­nimo 6 caracteres">
            </div>
            
            <div class="form-group">
                <label for="confirmacao_senha">Confirmar Senha</label>
                <input type="password" id="confirmacao_senha" name="confirmacao_senha" required minlength="6">
            </div>
            
            {% if not primeira_vez %}
                <div class="form-group">
                    <label for="role">Perfil de Acesso</label>
                    <select id="role" name="role" required>
                        <option value="operador">Operador</option>
                        <option value="caixa">Caixa</option>
                        <option value="gerente">Gerente</option>
                        <option value="garcom">Garcom</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="cargo">Cargo/Funcao (RH)</label>
                    <select id="cargo" name="cargo" required>
                        <option value="">Selecione um cargo</option>
                        {% for funcao in funcoes_rh %}
                            <option value="{{ funcao.nome }}">{{ funcao.nome }}</option>
                        {% endfor %}
                    </select>
                    <small style="display:block; margin-top: 8px;">
                        Nao encontrou o cargo? <a href="{{ url_for('nova_funcao_rh') }}">Criar nova funcao</a>.
                    </small>
                </div>
            {% endif %}
            
            <button type="submit" class="btn">
                {% if primeira_vez %}Criar Conta Admin{% else %}Registrar{% endif %}
            </button>
            
            {% if not primeira_vez %}
                <a href="{{ url_for('listar_funcionarios') }}" style="display: block; text-align: center; text-decoration: none;">
                    <button type="button" class="btn btn-secondary">Cancelar</button>
                </a>
            {% else %}
                <div class="registro-footer">
                    <p>JÃ¡ tem uma conta? <a href="{{ url_for('login') }}">Fazer login</a></p>
                </div>
            {% endif %}
        </form>
    </div>
    <script src="{{ url_for('static', filename='js/csrf.js') }}"></script>
</body>
</html>

```

---

### Arquivo: `templates\vendas\caixas\abrir_caixa.html`

```html
{% extends "base.html" %}

{% block title %}Abrir Caixa - SystemLR{% endblock %}

{% block content %}
<div class="caixa-form-page">
    <h1>Abrir Caixa: {{ caixa.nome }}</h1>

    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <div class="alert alert-{{ category }}">
                    {{ message }}
                </div>
            {% endfor %}
        {% endif %}
    {% endwith %}

    <div class="caixa-card">
        <form method="POST" action="{{ url_for('abrir_caixa', caixa_id=caixa.id) }}">
            <div class="caixa-field">
                <label for="funcionario_id">Funcionario <span class="required">*</span></label>
                <select id="funcionario_id" name="funcionario_id" required class="caixa-input">
                    <option value="">Selecione um funcionario</option>
                    {% for func in funcionarios %}
                        <option value="{{ func.id }}">{{ func.nome }} ({{ func.role.upper() }})</option>
                    {% endfor %}
                </select>
            </div>

            <div class="caixa-field">
                <label for="saldo_inicial">Saldo Inicial <span class="required">*</span></label>
                <input type="number" id="saldo_inicial" name="saldo_inicial" step="0.01" min="0" value="0" required class="caixa-input">
                <small>Valor inicial que sera colocado na caixa.</small>
            </div>

            <div class="caixa-field">
                <label for="observacoes">Observacoes (opcional)</label>
                <textarea id="observacoes" name="observacoes" rows="3" class="caixa-input"></textarea>
            </div>

            <div class="caixa-actions">
                <button type="submit" class="btn btn-primary">Abrir Caixa</button>
                <a href="{{ url_for('listar_caixas') }}" class="btn btn-secondary">Cancelar</a>
            </div>
        </form>
    </div>
</div>

<style>
    .caixa-form-page {
        max-width: 600px;
        margin: 40px auto;
    }

    .caixa-form-page h1 {
        color: #343a40;
        margin-bottom: 24px;
    }

    .caixa-card {
        background: #fff;
        padding: 24px;
        border-radius: 10px;
        border: 1px solid #dbe3e8;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }

    .caixa-field {
        margin-bottom: 18px;
    }

    .caixa-field label {
        display: block;
        margin-bottom: 8px;
        color: #343a40;
        font-weight: 600;
    }

    .required {
        color: #dc3545;
    }

    .caixa-input {
        width: 100%;
        padding: 12px;
        border: 2px solid #dee2e6;
        border-radius: 6px;
        font-size: 16px;
        font-family: inherit;
    }

    .caixa-input:focus {
        outline: none;
        border-color: #0f766e;
    }

    .caixa-field small {
        display: block;
        margin-top: 6px;
        color: #6c757d;
    }

    .caixa-actions {
        display: flex;
        gap: 10px;
        margin-top: 24px;
    }

    .caixa-actions > * {
        flex: 1;
        text-align: center;
    }

    @media (max-width: 640px) {
        .caixa-form-page {
            margin: 20px auto;
        }

        .caixa-card {
            padding: 16px;
        }

        .caixa-actions {
            flex-direction: column;
        }

        .caixa-actions > * {
            width: 100%;
        }
    }
</style>
{% endblock %}
```

---

### Arquivo: `templates\vendas\caixas\caixas.html`

```html
{% extends "base.html" %}
{% from "components/list_macros.html" import post_action_button %}

{% block title %}Caixas - SystemLR{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Caixas</h1>
    <a href="{{ url_for('nova_caixa') }}" class="btn btn-primary">Novo Caixa</a>
</div>

<div class="table-responsive">
    <table class="table">
        <thead>
            <tr>
                <th>Nome</th>
                <th>Funcionario</th>
                <th>Saldo Inicial</th>
                <th>Saldo Atual</th>
                <th>Abertura</th>
                <th>Status</th>
                <th>Acoes</th>
            </tr>
        </thead>
        <tbody>
            {% for caixa in caixas %}
            <tr>
                <td data-label="Nome"><strong>{{ caixa.nome }}</strong></td>
                <td data-label="Funcionario">{{ caixa.funcionario.nome if caixa.funcionario else '-' }}</td>
                <td data-label="Saldo Inicial">R$ {{ '%.2f'|format(caixa.saldo_inicial) }}</td>
                <td data-label="Saldo Atual">R$ {{ '%.2f'|format(caixa.saldo_atual) }}</td>
                <td data-label="Abertura">
                    {% if caixa.aberto_em %}
                    {{ caixa.aberto_em.strftime('%d/%m/%Y %H:%M') }}
                    {% else %}
                    -
                    {% endif %}
                </td>
                <td data-label="Status">
                    {% if caixa.aberto %}
                    <span class="badge badge-success">Aberto</span>
                    {% else %}
                    <span class="badge bg-secondary">Fechado</span>
                    {% endif %}
                </td>
                <td data-label="Acoes" class="actions-cell">
                    {% if not caixa.aberto %}
                    <a href="{{ url_for('abrir_caixa', caixa_id=caixa.id) }}" class="btn-small btn-success" title="Abrir caixa">Abrir</a>
                    {% else %}
                    <a href="{{ url_for('fechar_caixa', caixa_id=caixa.id) }}" class="btn-small btn-warning" title="Fechar caixa">Fechar</a>
                    <a href="{{ url_for('historico_caixa', caixa_id=caixa.id) }}" class="btn-small btn-info" title="Historico">Historico</a>
                    {% endif %}
                    <a href="{{ url_for('editar_caixa', caixa_id=caixa.id) }}" class="btn-small btn-primary" title="Editar">Editar</a>
                    {{ post_action_button(url_for('deletar_caixa', caixa_id=caixa.id), 'Excluir', 'btn-small btn-danger', 'Tem certeza que deseja excluir este caixa?') }}
                </td>
            </tr>
            {% else %}
            <tr>
                <td colspan="7" class="text-center">Nenhum caixa encontrado.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
```

---

### Arquivo: `templates\vendas\caixas\editar_caixa.html`

```html
{% extends "base.html" %}

{% block title %}Editar Caixa - SystemLR{% endblock %}

{% block content %}
<h1>Editar Caixa</h1>
<form method="POST" id="formCaixaEdit" onsubmit="return validarFormulario('formCaixaEdit')">
    <div class="form-group">
        <label for="nome">Nome</label>
        <input type="text" name="nome" id="nome" value="{{ caixa.nome }}" required class="form-control">
    </div>
    <div class="form-group">
        <label for="saldo_atual">Saldo Atual</label>
        <input type="number" step="0.01" name="saldo_atual" id="saldo_atual" value="{{ caixa.saldo_atual }}" required class="form-control">
    </div>
    <div class="form-group">
        <label><input type="checkbox" name="aberto" {% if caixa.aberto %}checked{% endif %}> Aberto</label>
    </div>
    <button type="submit" class="btn btn-primary">Salvar</button>
    <a href="{{ url_for('listar_caixas') }}" class="btn btn-secondary">✕ Cancelar</a>
</form>
{% endblock %}
```

---

### Arquivo: `templates\vendas\caixas\fechar_caixa.html`

```html
{% extends "base.html" %}

{% block title %}Fechar Caixa - SystemLR{% endblock %}

{% block content %}
<div class="caixa-close-page">
    <h1>Fechar Caixa: {{ caixa.nome }}</h1>

    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <div class="alert alert-{{ category }}">
                    {{ message }}
                </div>
            {% endfor %}
        {% endif %}
    {% endwith %}

    <section class="caixa-card">
        <h3>Informacoes da Caixa</h3>
        <div class="caixa-info-grid">
            <div class="caixa-info-item">
                <small>Funcionario</small>
                <strong>{{ caixa.funcionario.nome if caixa.funcionario else '-' }}</strong>
            </div>
            <div class="caixa-info-item">
                <small>Saldo Inicial</small>
                <strong>R$ {{ '%.2f'|format(caixa.saldo_inicial) }}</strong>
            </div>
            <div class="caixa-info-item">
                <small>Saldo Atual</small>
                <strong>R$ {{ '%.2f'|format(caixa.saldo_atual) }}</strong>
            </div>
            <div class="caixa-info-item">
                <small>Aberto em</small>
                <strong>{{ caixa.aberto_em.strftime('%d/%m/%Y %H:%M') if caixa.aberto_em else '-' }}</strong>
            </div>
        </div>
    </section>

    <section class="caixa-card">
        <form method="POST" action="{{ url_for('fechar_caixa', caixa_id=caixa.id) }}">
            <div class="caixa-field">
                <label for="saldo_fechamento">Saldo de Fechamento <span class="required">*</span></label>
                <input type="number" id="saldo_fechamento" name="saldo_fechamento" step="0.01" min="0" value="{{ caixa.saldo_atual }}" required class="caixa-input">
                <small>Valor total contado no caixa fisico.</small>
            </div>

            <div id="diferenca-info" class="diferenca-info">
                <div class="diferenca-head">
                    <strong>Diferenca:</strong>
                    <strong id="diferenca-valor">R$ 0,00</strong>
                </div>
                <small id="diferenca-texto"></small>
            </div>

            <div class="caixa-field">
                <label for="observacoes">Observacoes (opcional)</label>
                <textarea id="observacoes" name="observacoes" rows="3" class="caixa-input"></textarea>
            </div>

            <div class="caixa-actions">
                <button type="submit" class="btn btn-danger">Fechar Caixa</button>
                <a href="{{ url_for('listar_caixas') }}" class="btn btn-secondary">Cancelar</a>
            </div>
        </form>
    </section>
</div>

<script>
document.getElementById('saldo_fechamento').addEventListener('input', function () {
    const saldoFechamento = parseFloat(this.value) || 0;
    const saldoAtual = {{ caixa.saldo_atual }};
    const diferenca = saldoFechamento - saldoAtual;

    const infoDiv = document.getElementById('diferenca-info');
    const valorDiv = document.getElementById('diferenca-valor');
    const textoDiv = document.getElementById('diferenca-texto');

    infoDiv.style.display = 'block';
    valorDiv.textContent = 'R$ ' + Math.abs(diferenca).toFixed(2).replace('.', ',');

    if (diferenca > 0) {
        infoDiv.style.backgroundColor = '#d4edda';
        textoDiv.textContent = 'Sobra no caixa de R$ ' + Math.abs(diferenca).toFixed(2).replace('.', ',');
        textoDiv.style.color = '#155724';
    } else if (diferenca < 0) {
        infoDiv.style.backgroundColor = '#f8d7da';
        textoDiv.textContent = 'Falta no caixa de R$ ' + Math.abs(diferenca).toFixed(2).replace('.', ',');
        textoDiv.style.color = '#721c24';
    } else {
        infoDiv.style.backgroundColor = '#fff3cd';
        textoDiv.textContent = 'Caixa fechado sem diferenca';
        textoDiv.style.color = '#856404';
    }
});

document.getElementById('saldo_fechamento').dispatchEvent(new Event('input'));
</script>

<style>
    .caixa-close-page {
        max-width: 700px;
        margin: 40px auto;
        display: grid;
        gap: 16px;
    }

    .caixa-close-page h1 {
        margin-bottom: 0;
        color: #343a40;
    }

    .caixa-card {
        background: #fff;
        padding: 22px;
        border-radius: 10px;
        border: 1px solid #dbe3e8;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }

    .caixa-card h3 {
        margin-top: 0;
        margin-bottom: 14px;
        color: #0f766e;
        font-size: 1.1rem;
    }

    .caixa-info-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 12px;
    }

    .caixa-info-item {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 12px;
    }

    .caixa-info-item small {
        display: block;
        color: #6c757d;
        margin-bottom: 4px;
    }

    .caixa-info-item strong {
        color: #1f2937;
        font-size: 1rem;
    }

    .caixa-field {
        margin-bottom: 16px;
    }

    .caixa-field label {
        display: block;
        margin-bottom: 8px;
        color: #343a40;
        font-weight: 600;
    }

    .required {
        color: #dc3545;
    }

    .caixa-input {
        width: 100%;
        padding: 12px;
        border: 2px solid #dee2e6;
        border-radius: 6px;
        font-size: 16px;
        font-family: inherit;
    }

    .caixa-input:focus {
        outline: none;
        border-color: #0f766e;
    }

    .caixa-field small {
        display: block;
        margin-top: 6px;
        color: #6c757d;
    }

    .diferenca-info {
        display: none;
        padding: 14px;
        border-radius: 8px;
        margin-bottom: 16px;
    }

    .diferenca-head {
        display: flex;
        justify-content: space-between;
        gap: 10px;
        align-items: center;
    }

    .diferenca-info small {
        display: block;
        margin-top: 6px;
    }

    .caixa-actions {
        display: flex;
        gap: 10px;
        margin-top: 22px;
    }

    .caixa-actions > * {
        flex: 1;
        text-align: center;
    }

    @media (max-width: 640px) {
        .caixa-close-page {
            margin: 20px auto;
            gap: 12px;
        }

        .caixa-card {
            padding: 16px;
        }

        .caixa-info-grid {
            grid-template-columns: 1fr;
        }

        .diferenca-head {
            flex-direction: column;
            align-items: flex-start;
        }

        .caixa-actions {
            flex-direction: column;
        }

        .caixa-actions > * {
            width: 100%;
        }
    }
</style>
{% endblock %}
```

---

### Arquivo: `templates\vendas\caixas\historico_caixa.html`

```html
{% extends "base.html" %}

{% block title %}Historico da Caixa - SystemLR{% endblock %}

{% block content %}
<div class="caixa-history-page">
    <div class="caixa-history-header">
        <h1>Historico: {{ caixa.nome }}</h1>
        <a href="{{ url_for('listar_caixas') }}" class="btn btn-primary">Voltar</a>
    </div>

    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <div class="alert alert-{{ category }}">
                    {{ message }}
                </div>
            {% endfor %}
        {% endif %}
    {% endwith %}

    <section class="caixa-card">
        <div class="caixa-summary-grid">
            <div class="caixa-summary-item summary-func">
                <small>Funcionario</small>
                <strong>{{ caixa.funcionario.nome if caixa.funcionario else '-' }}</strong>
            </div>
            <div class="caixa-summary-item summary-inicial">
                <small>Saldo Inicial</small>
                <strong>R$ {{ '%.2f'|format(caixa.saldo_inicial) }}</strong>
            </div>
            <div class="caixa-summary-item summary-atual">
                <small>Saldo Atual</small>
                <strong>R$ {{ '%.2f'|format(caixa.saldo_atual) }}</strong>
            </div>
            {% if caixa.saldo_fechamento is not none %}
                <div class="caixa-summary-item summary-fechamento">
                    <small>Saldo Fechamento</small>
                    <strong>R$ {{ '%.2f'|format(caixa.saldo_fechamento) }}</strong>
                </div>
            {% endif %}
        </div>
    </section>

    <section class="caixa-card">
        <h2>Movimentacoes</h2>

        {% if movimentacoes %}
            <div class="table-responsive">
                <table class="table caixa-history-table">
                    <thead>
                        <tr>
                            <th>Data/Hora</th>
                            <th>Tipo</th>
                            <th class="text-right">Valor</th>
                            <th>Descricao</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for mov in movimentacoes %}
                            <tr>
                                <td data-label="Data/Hora">{{ mov.criado_em.strftime('%d/%m/%Y %H:%M:%S') }}</td>
                                <td data-label="Tipo">
                                    <span class="mov-badge mov-badge-{{ mov.tipo }}">
                                        {{ 'ENTRADA' if mov.tipo == 'entrada' else 'SAIDA' }}
                                    </span>
                                </td>
                                <td data-label="Valor" class="text-right">
                                    <span class="mov-valor mov-valor-{{ mov.tipo }}">
                                        {{ '+' if mov.tipo == 'entrada' else '-' }} R$ {{ '%.2f'|format(mov.valor) }}
                                    </span>
                                </td>
                                <td data-label="Descricao" class="mov-desc">{{ mov.descricao }}</td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        {% else %}
            <div class="caixa-empty-box">
                <p>Nenhuma movimentacao registrada para esta caixa.</p>
            </div>
        {% endif %}
    </section>
</div>

<style>
    .caixa-history-page {
        max-width: 1000px;
        margin: 40px auto;
        display: grid;
        gap: 16px;
    }

    .caixa-history-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 10px;
    }

    .caixa-history-header h1 {
        margin: 0;
        color: #343a40;
    }

    .caixa-card {
        background: #fff;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #dbe3e8;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }

    .caixa-card h2 {
        margin-top: 0;
        margin-bottom: 16px;
        color: #343a40;
        font-size: 1.2rem;
    }

    .caixa-summary-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 12px;
    }

    .caixa-summary-item {
        border-left: 4px solid #0f766e;
        padding: 12px;
        background: #f8fafc;
        border-radius: 6px;
    }

    .summary-inicial {
        border-left-color: #16a34a;
    }

    .summary-atual {
        border-left-color: #0ea5e9;
    }

    .summary-fechamento {
        border-left-color: #f59e0b;
    }

    .caixa-summary-item small {
        display: block;
        color: #6c757d;
        margin-bottom: 4px;
    }

    .caixa-summary-item strong {
        font-size: 1rem;
    }

    .caixa-history-table tbody tr:hover {
        background-color: #f8f9fa;
    }

    .mov-badge {
        display: inline-flex;
        align-items: center;
        border-radius: 999px;
        padding: 5px 10px;
        font-size: 12px;
        font-weight: 700;
        color: #fff;
    }

    .mov-badge-entrada {
        background-color: #16a34a;
    }

    .mov-badge-saida {
        background-color: #dc3545;
    }

    .mov-valor {
        font-weight: 700;
    }

    .mov-valor-entrada {
        color: #16a34a;
    }

    .mov-valor-saida {
        color: #dc3545;
    }

    .mov-desc {
        overflow-wrap: anywhere;
    }

    .caixa-empty-box {
        background-color: #f8f9fa;
        padding: 30px;
        border-radius: 8px;
        text-align: center;
        color: #6c757d;
    }

    .caixa-empty-box p {
        margin: 0;
        font-size: 16px;
    }

    @media (max-width: 768px) {
        .caixa-history-page {
            margin: 20px auto;
            gap: 12px;
        }

        .caixa-history-header {
            flex-direction: column;
            align-items: stretch;
        }

        .caixa-history-header .btn {
            width: 100%;
        }

        .caixa-card {
            padding: 16px;
        }
    }
</style>
{% endblock %}
```

---

### Arquivo: `templates\vendas\caixas\nova_caixa.html`

```html
{% extends "base.html" %}

{% block title %}Novo Caixa - SystemLR{% endblock %}

{% block content %}
<h1>Novo Caixa</h1>
<form method="POST" id="formCaixa" onsubmit="return validarFormulario('formCaixa')">
    <div class="form-group">
        <label for="nome">Nome</label>
        <input type="text" name="nome" id="nome" required class="form-control">
    </div>
    <div class="form-group">
        <label for="saldo_inicial">Saldo Inicial</label>
        <input type="number" step="0.01" name="saldo_inicial" id="saldo_inicial" required class="form-control">
    </div>
    <button type="submit" class="btn btn-primary">Salvar</button>
    <a href="{{ url_for('listar_caixas') }}" class="btn btn-secondary">✕ Cancelar</a>
</form>
{% endblock %}
```

---

### Arquivo: `templates\vendas\garcons\config_distribuicao.html`

```html
{% extends "base.html" %}

{% block title %}Configuração de Distribuição - SystemLR{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Distribuição de Pedidos para Garçons</h1>
</div>

<div class="form-container">
    <form method="POST" class="form">
        <label class="checkbox-inline">
            <input type="checkbox" name="distribuicao_ativa" {% if empresa.distribuicao_ativa != False %}checked{% endif %}>
            Ativar distribuição automática para pedidos QR
        </label>

        <div class="form-group">
            <label for="modo_distribuicao_pedidos">Modo de separação</label>
            <select id="modo_distribuicao_pedidos" name="modo_distribuicao_pedidos" class="input-select">
                <option value="round_robin" {% if empresa.modo_distribuicao_pedidos == 'round_robin' %}selected{% endif %}>Rodízio (round-robin)</option>
                <option value="menos_pedidos" {% if empresa.modo_distribuicao_pedidos == 'menos_pedidos' %}selected{% endif %}>Menor carga (menos pedidos em andamento)</option>
                <option value="manual" {% if empresa.modo_distribuicao_pedidos == 'manual' %}selected{% endif %}>Manual (sem atribuição automática)</option>
            </select>
        </div>

        <div class="info-box">
            <p><strong>Rodízio:</strong> alterna automaticamente entre garçons ativos.</p>
            <p><strong>Menor carga:</strong> envia para o garçom com menos pedidos em aberto/em preparo.</p>
            <p><strong>Manual:</strong> pedido entra sem garçom atribuído.</p>
        </div>

        <div class="form-actions">
            <button type="submit" class="btn btn-success">Salvar Configuração</button>
            <a href="{{ url_for('listar_garcons') }}" class="btn btn-secondary">Voltar</a>
        </div>
    </form>
</div>
{% endblock %}
```

---

### Arquivo: `templates\vendas\garcons\editar_garcom.html`

```html
{% extends "base.html" %}

{% block title %}Editar Garçom - SystemLR{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Editar Garçom</h1>
</div>

<div class="form-container">
    <form method="POST" class="form">
        <div class="form-group">
            <label for="nome">Nome</label>
            <input type="text" id="nome" name="nome" required class="input-text" value="{{ garcom.nome }}">
        </div>

        <div class="form-group">
            <label for="celular">Celular</label>
            <input type="text" id="celular" name="celular" class="input-text" value="{{ garcom.celular or '' }}">
        </div>

        <label class="checkbox-inline">
            <input type="checkbox" name="ativo" {% if garcom.ativo %}checked{% endif %}>
            Garçom ativo
        </label>

        <div class="form-actions">
            <button type="submit" class="btn btn-success">Salvar Alterações</button>
            <a href="{{ url_for('listar_garcons') }}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>
{% endblock %}
```

---

### Arquivo: `templates\vendas\garcons\garcons.html`

```html
﻿{% extends "base.html" %}

{% block title %}GarÃ§ons - SystemLR{% endblock %}

{% block content %}
<div class="page-header">
    <h1>GarÃ§ons</h1>
    <div class="header-actions">
        <a href="{{ url_for('novo_garcom') }}" class="btn btn-primary">Novo GarÃ§om</a>
        <a href="{{ url_for('configurar_distribuicao_garcons') }}" class="btn btn-secondary">Configurar DistribuiÃ§Ã£o</a>
    </div>
</div>

<div class="section">
    <h2>Equipe de GarÃ§ons</h2>
    <div class="table-responsive">
        <table class="table">
            <thead>
                <tr>
                    <th>Nome</th>
                    <th>Celular</th>
                    <th>Status</th>
                    <th>AÃ§Ãµes</th>
                </tr>
            </thead>
            <tbody>
                {% for garcom in garcons %}
                <tr>
                    <td data-label="Nome">{{ garcom.nome }}</td>
                    <td data-label="Celular">{{ garcom.celular or '-' }}</td>
                    <td data-label="Status">
                        <span class="badge {% if garcom.ativo %}badge-success{% else %}badge-danger{% endif %}">
                            {% if garcom.ativo %}Ativo{% else %}Inativo{% endif %}
                        </span>
                    </td>
                    <td data-label="AÃ§Ãµes" class="actions-cell">
                        <a href="{{ url_for('editar_garcom', garcom_id=garcom.id) }}" class="btn-small btn-warning">Editar</a>
                        <form method="POST" action="{{ url_for('deletar_garcom', garcom_id=garcom.id) }}" class="inline-form" data-confirm-message="Remover garcom?">
                            <button type="submit" class="btn-small btn-danger">Remover</button>
                        </form>
                    </td>
                </tr>
                {% else %}
                <tr>
                    <td colspan="4" class="text-center">Nenhum garÃ§om cadastrado.</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>

<div class="section">
    <h2>Pedidos e Etapas</h2>
    <div class="table-responsive">
        <table class="table">
            <thead>
                <tr>
                    <th>Pedido</th>
                    <th>Cliente</th>
                    <th>Mesa</th>
                    <th>GarÃ§om</th>
                    <th>Etapa</th>
                    <th>Origem</th>
                </tr>
            </thead>
            <tbody>
                {% for pedido in pedidos_em_andamento %}
                <tr>
                    <td data-label="Pedido">#{{ pedido.id }}</td>
                    <td data-label="Cliente">{{ pedido.cliente_nome or '-' }}</td>
                    <td data-label="Mesa">{{ pedido.mesa.numero if pedido.mesa else '-' }}</td>
                    <td data-label="GarÃ§om">{{ pedido.garcom.nome if pedido.garcom else 'NÃ£o atribuÃ­do' }}</td>
                    <td data-label="Etapa">
                        <span class="badge {% if pedido.status == 'entregue' %}badge-success{% elif pedido.status == 'em_preparo' %}badge-warning{% else %}badge-info{% endif %}">
                            {{ pedido.status }}
                        </span>
                    </td>
                    <td data-label="Origem">{{ pedido.origem or '-' }}</td>
                </tr>
                {% else %}
                <tr>
                    <td colspan="6" class="text-center">Nenhum pedido em andamento.</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}

```

---

### Arquivo: `templates\vendas\garcons\novo_garcom.html`

```html
{% extends "base.html" %}

{% block title %}Novo Garçom - SystemLR{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Novo Garçom</h1>
</div>

<div class="form-container">
    <form method="POST" class="form">
        <div class="form-group">
            <label for="nome">Nome</label>
            <input type="text" id="nome" name="nome" required class="input-text">
        </div>

        <div class="form-group">
            <label for="celular">Celular</label>
            <input type="text" id="celular" name="celular" class="input-text">
        </div>

        <label class="checkbox-inline">
            <input type="checkbox" name="ativo" checked>
            Garçom ativo
        </label>

        <div class="form-actions">
            <button type="submit" class="btn btn-success">Salvar</button>
            <a href="{{ url_for('listar_garcons') }}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>
{% endblock %}
```

---

### Arquivo: `templates\vendas\mesas\editar_mesa.html`

```html
{% extends "base.html" %}

{% block title %}Editar Mesa - SystemLR{% endblock %}

{% block content %}
<h1>Editar Mesa</h1>
<form method="POST" id="formMesaEdit" onsubmit="return validarFormulario('formMesaEdit')">
    <div class="form-group">
        <label for="numero">Número</label>
        <input type="text" name="numero" id="numero" value="{{ mesa.numero }}" required class="form-control">
    </div>
    <div class="form-group">
        <label for="capacidade">Capacidade</label>
        <input type="number" name="capacidade" id="capacidade" value="{{ mesa.capacidade }}" required class="form-control">
    </div>
    <div class="form-group">
        <label for="status">Status</label>
        <select name="status" id="status" class="form-control">
            <option value="livre" {% if mesa.status=='livre' %}selected{% endif %}>Livre</option>
            <option value="ocupada" {% if mesa.status=='ocupada' %}selected{% endif %}>Ocupada</option>
        </select>
    </div>
    <button type="submit" class="btn btn-primary">Salvar</button>
    <a href="{{ url_for('listar_mesas') }}" class="btn btn-secondary">✕ Cancelar</a>
</form>
{% endblock %}
```

---

### Arquivo: `templates\vendas\mesas\mesas.html`

```html
﻿{% extends "base.html" %}

{% block title %}Mesas - SystemLR{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Mesas</h1>
    <a href="{{ url_for('nova_mesa') }}" class="btn btn-primary">Nova Mesa</a>
</div>

<div class="table-responsive">
    <table class="table">
        <thead>
            <tr>
                <th>Numero</th>
                <th>Capacidade</th>
                <th>Status</th>
                <th>Link da Comanda</th>
                <th>Acoes</th>
            </tr>
        </thead>
        <tbody>
            {% for mesa in mesas %}
            <tr>
                <td data-label="Numero">{{ mesa.numero }}</td>
                <td data-label="Capacidade">{{ mesa.capacidade }}</td>
                <td data-label="Status">{{ mesa.status }}</td>
                <td data-label="Link da Comanda">
                    <input
                        type="text"
                        readonly
                        class="form-control mesa-link-input"
                        value="{{ url_for('public.cardapio_mesa', token=mesa.qr_token, _external=True) }}"
                        onclick="this.select();"
                    >
                </td>
                <td data-label="Acoes" class="actions-cell">
                    <a href="{{ url_for('public.cardapio_mesa', token=mesa.qr_token) }}" class="btn-small btn-secondary" target="_blank" title="Abrir link da mesa">Abrir link</a>
                    <a href="{{ url_for('visualizar_qrcode_mesa', mesa_id=mesa.id) }}" class="btn-small btn-info" title="Ver QR Code">QR</a>
                    <a href="{{ url_for('editar_mesa', mesa_id=mesa.id) }}" class="btn-small btn-warning">Editar</a>
                    <form method="POST" action="{{ url_for('deletar_mesa', mesa_id=mesa.id) }}" class="inline-form" data-confirm-message="Excluir mesa {{ mesa.numero }}?">
                        <button type="submit" class="btn-small btn-danger">Excluir</button>
                    </form>
                </td>
            </tr>
            {% else %}
            <tr>
                <td colspan="5" class="text-center">Nenhuma mesa encontrada</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>

<style>
.btn-info {
    background-color: #17a2b8;
    color: white;
    padding: 5px 10px;
    border-radius: 3px;
    text-decoration: none;
    font-size: 12px;
    display: inline-block;
}

.btn-info:hover {
    background-color: #138496;
}

.mesa-link-input {
    min-width: 220px;
}

@media (max-width: 768px) {
    .mesa-link-input {
        min-width: 180px;
        font-size: 0.85rem;
    }
}
</style>
{% endblock %}

```

---

### Arquivo: `templates\vendas\mesas\nova_mesa.html`

```html
{% extends "base.html" %}

{% block title %}Nova Mesa - SystemLR{% endblock %}

{% block content %}
<h1>Nova Mesa</h1>
<form method="POST" id="formMesa" onsubmit="return validarFormulario('formMesa')">
    <div class="form-group">
        <label for="numero">Número</label>
        <input type="text" name="numero" id="numero" required class="form-control">
    </div>
    <div class="form-group">
        <label for="capacidade">Capacidade</label>
        <input type="number" name="capacidade" id="capacidade" value="4" required class="form-control">
    </div>
    <button type="submit" class="btn btn-primary">Salvar</button>
    <a href="{{ url_for('listar_mesas') }}" class="btn btn-secondary">✕ Cancelar</a>
</form>
{% endblock %}
```

---

### Arquivo: `templates\vendas\mesas\print_qrcode_mesa.html`

```html
{% extends "base.html" %}

{% block title %}Imprimir QR Code - Mesa {{ mesa.numero }} - SystemLR{% endblock %}

{% block content %}
<style>
    @media print {
        body, html {
            margin: 0;
            padding: 0;
        }
        
        .print-header {
            display: none;
        }
        
        .page-header {
            display: none;
        }
        
        .no-print {
            display: none !important;
        }
        
        .print-qrcode-container {
            page-break-inside: avoid;
            margin: 0;
            padding: 0;
        }
    }
    
    @media screen {
        .print-controls {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        
        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            font-size: 14px;
        }
        
        .btn-primary {
            background-color: #007bff;
            color: white;
        }
        
        .btn-primary:hover {
            background-color: #0056b3;
        }
        
        .btn-secondary {
            background-color: #6c757d;
            color: white;
        }
    }
    
    .print-qrcode-container {
        text-align: center;
        padding: 20px;
        background: white;
        border: 1px solid #ddd;
        border-radius: 5px;
    }
    
    .print-content {
        display: inline-block;
        page-break-inside: avoid;
    }
    
    .mesa-info {
        margin-bottom: 20px;
        font-weight: bold;
        font-size: 18px;
    }
    
    #qrcode {
        display: inline-block;
        padding: 10px;
        background: white;
        border: 2px solid #333;
    }
    
    .url-info {
        margin-top: 15px;
        font-size: 12px;
        color: #666;
        word-break: break-all;
    }
    
    .print-options {
        margin-top: 20px;
        font-size: 12px;
        color: #999;
    }
</style>

<div class="print-controls no-print">
    <button onclick="window.print()" class="btn btn-primary">🖨️ Imprimir</button>
    <button onclick="window.history.back()" class="btn btn-secondary">← Voltar</button>
</div>

<div class="print-qrcode-container">
    <div class="print-content">
        <div class="mesa-info">
            Mesa {{ mesa.numero }}
        </div>
        
        <div id="qrcode" style="display: inline-block;"></div>
        
        <div class="url-info">
            {{ qr_url }}
        </div>
        
        <div class="print-options">
            <p>Capacidade: {{ mesa.capacidade }} pessoas</p>
        </div>
    </div>
</div>

<!-- Script QRCode.js -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>

<script>
document.addEventListener('DOMContentLoaded', function() {
    // Gera o QR code dinamicamente
    var qrcodeElement = document.getElementById('qrcode');
    qrcodeElement.innerHTML = '';
    
    new QRCode(qrcodeElement, {
        text: "{{ qr_url }}",
        width: 400,
        height: 400,
        colorDark: "#000000",
        colorLight: "#ffffff",
        correctLevel: QRCode.CorrectLevel.H
    });
});
</script>
{% endblock %}
```

---

### Arquivo: `templates\vendas\mesas\qrcode_mesa.html`

```html
{% extends "base.html" %}

{% block title %}QR Code - Mesa {{ mesa.numero }} - SystemLR{% endblock %}

{% block content %}
<div class="page-header">
    <h1>QR Code - Mesa {{ mesa.numero }}</h1>
    <a href="{{ url_for('listar_mesas') }}" class="btn btn-secondary">Voltar</a>
</div>

<div class="qrcode-container" style="background-color: white; padding: 30px; border-radius: 8px; max-width: 600px; margin: 30px auto;">
    <div class="qrcode-info" style="text-align: center; margin-bottom: 30px;">
        <h3>Mesa {{ mesa.numero }}</h3>
        <p style="color: #666; margin: 10px 0;">Capacidade: {{ mesa.capacidade }} pessoas</p>
        <p style="font-size: 12px; color: #999; word-break: break-all;">{{ qr_url }}</p>
    </div>

    <!-- QR Code gerado pelo servidor -->
    <div id="qrcode-display" style="text-align: center; margin: 30px 0;">
        <div id="qrcode" style="display: inline-block; padding: 20px; background: white; border: 2px solid #333;"></div>
    </div>

    <!-- Botões de ação -->
    <div class="actions" style="text-align: center; margin-top: 30px; display: flex; gap: 10px; justify-content: center; flex-wrap: wrap;">
        <a href="{{ url_for('download_qrcode_mesa', mesa_id=mesa.id) }}" class="btn btn-primary" title="Baixar como PNG">
            <i class="icon">📥</i> Baixar Imagem
        </a>
        <a href="{{ url_for('print_qrcode_mesa', mesa_id=mesa.id) }}" class="btn btn-primary" title="Abrir em modo impressão" target="_blank">
            <i class="icon">🖨️</i> Imprimir
        </a>
        <button onclick="copiarURL()" class="btn btn-secondary" title="Copiar URL para clipboard">
            <i class="icon">📋</i> Copiar URL
        </button>
    </div>

    <!-- Informações adicionais -->
    <div class="info-box" style="margin-top: 30px; padding: 15px; background-color: #f5f5f5; border-radius: 5px; border-left: 4px solid #007bff;">
        <h4 style="margin-top: 0;">💡 Como usar:</h4>
        <ul style="margin: 10px 0; padding-left: 20px;">
            <li><strong>Imprimir:</strong> Clique em "Imprimir" para abrir em modo de impressão, ajuste o tamanho conforme necessário</li>
            <li><strong>Baixar:</strong> Clique em "Baixar Imagem" para salvar como arquivo PNG</li>
            <li><strong>Colar:</strong> Após baixar, você pode imprimir ou colar a imagem em qualquer documento</li>
            <li><strong>URL:</strong> Copie a URL para compartilhar via WhatsApp ou email</li>
        </ul>
    </div>
</div>

<!-- Script QRCode.js -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>

<script>
document.addEventListener('DOMContentLoaded', function() {
    // Gera o QR code dinamicamente
    var qrcodeElement = document.getElementById('qrcode');
    qrcodeElement.innerHTML = '';
    
    new QRCode(qrcodeElement, {
        text: "{{ qr_url }}",
        width: 300,
        height: 300,
        colorDark: "#000000",
        colorLight: "#ffffff",
        correctLevel: QRCode.CorrectLevel.H
    });
});

function copiarURL() {
    const url = "{{ qr_url }}";
    navigator.clipboard.writeText(url).then(function() {
        alert('URL copiada para a área de transferência!');
    }).catch(function(err) {
        console.error('Erro ao copiar URL:', err);
    });
}
</script>

<style>
.qrcode-container {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.actions {
    gap: 10px;
}

.btn {
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    text-decoration: none;
    display: inline-block;
    font-size: 14px;
    transition: background-color 0.3s;
}

.btn-primary {
    background-color: #007bff;
    color: white;
}

.btn-primary:hover {
    background-color: #0056b3;
}

.btn-secondary {
    background-color: #6c757d;
    color: white;
}

.btn-secondary:hover {
    background-color: #545b62;
}

.info-box ul li {
    margin: 5px 0;
}

@media (max-width: 768px) {
    .qrcode-container {
        padding: 15px;
    }
    
    #qrcode {
        transform: scale(0.8);
    }
}
</style>
{% endblock %}
```

---

### Arquivo: `templates\vendas\pdv.html`

```html
﻿{% extends "base.html" %}

{% block title %}PDV - Ponto de Venda - SystemLR{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/pages/pdv.css') }}">
{% endblock %}

{% block content %}
<div class="page-header">
    <h1>PDV</h1>
    <div class="text-muted">Fluxo rapido de vendas e pagamento</div>
</div>

<div class="pdv-container">
    <section class="pdv-panel">
        <div class="pdv-panel-head">Produtos</div>
        <div class="pdv-panel-body">
            <div class="pdv-toolbar">
                <input type="text" id="filtroNome" class="form-control" placeholder="Filtrar produtos...">
                <button type="button" class="btn btn-outline-secondary js-open-barcode-scanner" data-barcode-target="barcodeInput" data-barcode-mode="continuous" title="Ler codigo de barras">
                    Scanner
                </button>
                <input type="text" id="barcodeInput" class="d-none">
            </div>

            <div class="pdv-produtos" id="produtosGrid">
                {% for produto in produtos %}
                <div class="produto-card {% if produto.quantidade_estoque < produto.quantidade_minima %}low-stock{% endif %}"
                    data-id="{{ produto.id }}" data-codigo="{{ produto.codigo }}" data-preco="{{ produto.preco_venda }}" data-nome="{{ produto.nome }}" data-categoria="{{ produto.categoria.nome if produto.categoria else '' }}" data-detalhe-url="{{ url_for('visualizar_produto', produto_id=produto.id) }}" data-estoque="{{ produto.quantidade_estoque }}">
                    {% if produto.imagem_path %}
                    <img src="{{ url_for('static', filename=produto.imagem_path) }}" alt="{{ produto.nome }}" class="produto-imagem">
                    {% endif %}
                    <div class="produto-nome">{{ produto.nome }}</div>
                    <div class="produto-preco">R$ {{ '%.2f'|format(produto.preco_venda) }}</div>
                    <div class="produto-estoque">
                        {% if produto.quantidade_estoque < produto.quantidade_minima %}
                            Estoque baixo: {{ produto.quantidade_estoque }}
                        {% else %}
                            Estoque: {{ produto.quantidade_estoque }}
                        {% endif %}
                    </div>
                    <button type="button" class="btn-add-produto" aria-label="Adicionar {{ produto.nome }} ao pedido" onclick="adicionarAoCarrinho({{ produto.id }}, '{{ produto.nome }}', {{ produto.preco_venda }})" {% if produto.quantidade_estoque <= 0 %}disabled title="Sem estoque"{% endif %}>
                        {% if produto.quantidade_estoque <= 0 %}Indisponivel{% else %}Adicionar{% endif %}
                    </button>
                </div>
                {% endfor %}
            </div>
        </div>
    </section>

    <section class="pdv-panel pedido-panel">
        <div class="pdv-panel-head">Pedido</div>
        <div class="pdv-panel-body">
            <div id="alertas"></div>

            <div class="pedido-header">
                <div class="w-100">
                    <label for="caixaSelect" class="field-label">Caixa</label>
                    <select id="caixaSelect" class="pedido-select" required onchange="atualizarCaixa()">
                        <option value="">Selecione a caixa</option>
                        {% for caixa in caixas_abertas %}
                        <option value="{{ caixa.id }}">{{ caixa.nome }}</option>
                        {% endfor %}
                    </select>
                </div>
            </div>

            {% if atendimento_mesas_ativo %}
            <div class="mb-2">
                <label for="mesaSelect" class="field-label">Mesa (opcional)</label>
                <select id="mesaSelect" class="pedido-select">
                    <option value="">Sem mesa</option>
                    {% for mesa in mesas %}
                    <option value="{{ mesa.id }}">Mesa {{ mesa.numero }}</option>
                    {% endfor %}
                </select>
            </div>
            {% endif %}

            <label class="field-label">Pedidos em andamento (todas as caixas)</label>
            <div class="pedido-filtros">
                {% if atendimento_mesas_ativo %}
                <select id="filtroPedidoMesa" class="pedido-select" onchange="carregarPedidosEmAberto()">
                    <option value="">Todas as mesas</option>
                    {% for mesa in mesas %}
                    <option value="{{ mesa.id }}">Mesa {{ mesa.numero }}</option>
                    {% endfor %}
                </select>
                <select id="filtroPedidoGarcom" class="pedido-select" onchange="carregarPedidosEmAberto()">
                    <option value="">Todos os garcons</option>
                    {% for garcom in garcons %}
                    <option value="{{ garcom.id }}">{{ garcom.nome }}</option>
                    {% endfor %}
                </select>
                {% endif %}
                <select id="filtroPedidoStatus" class="pedido-select" onchange="carregarPedidosEmAberto()">
                    <option value="">Todos os status</option>
                    <option value="aberto">Aberto</option>
                    <option value="em_preparo">Em preparo</option>
                    <option value="entregue">Entregue</option>
                </select>
            </div>

            <div class="open-orders-panel">
                <div class="open-orders-header">
                    <span class="open-orders-title">Clique para abrir o pagamento</span>
                    <span id="openOrdersCount" class="open-orders-count">0 pedidos</span>
                </div>
                <div id="pedidoAbertoLista" class="open-orders-list">
                    <div class="vazio">Carregando pedidos em andamento...</div>
                </div>
            </div>

            <select id="pedidoAbertoSelect" class="pedido-select pedido-select-hidden" onchange="onChangePedidoAberto()">
                <option value="">Selecione um pedido aberto</option>
            </select>

            <label class="field-label" for="itensPedido">Itens do pedido</label>
            <div class="itens-lista" id="itensPedido">
                <div class="vazio">Nenhum item adicionado</div>
            </div>

            <div class="pedido-resumo">
                <div class="resumo-linha">
                    <span>Subtotal:</span>
                    <span id="subtotal">R$ 0.00</span>
                </div>
                <div class="resumo-total">
                    <span>Total:</span>
                    <span id="total">R$ 0.00</span>
                </div>
                <div class="resumo-itens" id="itemCount">0 itens</div>
            </div>

            <div class="pedido-acoes">
                <button type="button" class="btn-pedido btn-nova-venda" onclick="novaVenda()" id="btnNovaVenda" disabled>
                    + Adicionar Produtos
                </button>
                <button type="button" class="btn-pedido btn-finalizar" onclick="finalizarVenda()" id="btnFinalizar" disabled>
                    Finalizar
                </button>
            </div>
        </div>
    </section>
</div>

<div class="payment-modal" id="paymentModal" role="dialog" aria-modal="true" aria-labelledby="paymentModalTitle">
    <div class="payment-modal-content" tabindex="-1">
        <h3 class="payment-title" id="paymentModalTitle">Finalizar pagamento</h3>
        <p class="payment-subtitle">Total do pedido: <strong id="paymentTotalLabel">R$ 0.00</strong></p>

        <div class="payment-grid">
            <label class="payment-option"><input type="radio" name="metodo_pagamento_pdv" value="dinheiro" checked>Dinheiro</label>
            <label class="payment-option"><input type="radio" name="metodo_pagamento_pdv" value="cartao">Cartao</label>
            <label class="payment-option"><input type="radio" name="metodo_pagamento_pdv" value="pix">Pix</label>
            <label class="payment-option"><input type="radio" name="metodo_pagamento_pdv" value="crediario">Crediario</label>
            <label class="payment-option payment-option-row"><input type="radio" name="metodo_pagamento_pdv" value="dividido">Dividido (dinheiro + cartao)</label>
        </div>

        <div class="payment-fields" id="paymentDefaultFields">
            <div>
                <label for="paymentValor" class="field-label">Valor recebido</label>
                <input type="number" step="0.01" id="paymentValor" class="pedido-select" placeholder="Ex.: 100.00">
            </div>
            <small id="trocoInfo" class="text-muted">Troco: R$ 0.00</small>
        </div>

        <div class="payment-fields is-hidden" id="paymentSplitFields">
            <div class="payment-row">
                <div>
                    <label for="paymentDinheiro" class="field-label">Dinheiro</label>
                    <input type="number" step="0.01" id="paymentDinheiro" class="pedido-select" placeholder="0.00">
                </div>
                <div>
                    <label for="paymentCartao" class="field-label">Cartao</label>
                    <input type="number" step="0.01" id="paymentCartao" class="pedido-select" placeholder="0.00">
                </div>
            </div>
            <small id="splitTotalInfo" class="text-muted">Total informado: R$ 0.00</small>
        </div>

        <div class="payment-fields is-hidden" id="paymentCrediarioFields">
            <div>
                <label for="paymentClienteCrediario" class="field-label">Cliente (opcional)</label>
                <input type="text" id="paymentClienteCrediario" class="pedido-select" placeholder="Nome do cliente">
            </div>
        </div>

        <div class="payment-receipt-option">
            <label class="checkbox-inline">
                <input type="checkbox" id="paymentEmitirComprovante" checked>
                Emitir comprovante do cliente apos finalizar
            </label>
        </div>

        <div class="payment-actions">
            <button type="button" class="btn btn-outline-secondary" onclick="fecharModalPagamento()">Cancelar</button>
            <button type="button" class="btn btn-primary" id="btnConfirmarPagamento" onclick="confirmarFinalizacaoPagamento()">Confirmar</button>
        </div>
    </div>
</div>

<script>
let carrinho = {};
let carrinhoOriginal = {};
let pedidoAtual = null;
let pedidoStatusAtual = null;
let caixaSelecionada = null;
let ultimoElementoComFoco = null;

function setButtonLoading(buttonEl, isLoading, loadingText, idleText) {
    if (!buttonEl) return;
    if (isLoading) {
        if (!buttonEl.dataset.idleText) {
            buttonEl.dataset.idleText = idleText || buttonEl.textContent.trim();
        }
        buttonEl.disabled = true;
        buttonEl.innerHTML = `<span class="spinner-border spinner-border-sm me-1" role="status" aria-hidden="true"></span>${loadingText || 'Processando...'}`;
        return;
    }
    const textoPadrao = buttonEl.dataset.idleText || idleText || buttonEl.textContent.trim();
    buttonEl.textContent = textoPadrao;
    delete buttonEl.dataset.idleText;
}

function adicionarAoCarrinho(produtoId, nome, preco) {
    if (!document.getElementById('caixaSelect').value && !pedidoAtual) {
        mostrarAlerta('Selecione uma caixa para iniciar nova venda.', 'error');
        return;
    }
    const card = document.querySelector(`.produto-card[data-id="${produtoId}"]`);
    if (card) {
        const estoque = parseInt(card.dataset.estoque || '0', 10);
        if (estoque <= 0) {
            mostrarAlerta('Produto sem estoque disponivel.', 'warning');
            return;
        }
    }

    const isNew = !carrinho[produtoId];
    if (!carrinho[produtoId]) {
        carrinho[produtoId] = { nome, preco, quantidade: 0 };
    }
    carrinho[produtoId].quantidade++;
    
    // highlight produto card briefly
    if (card) {
        card.classList.add('added');
        setTimeout(() => card.classList.remove('added'), 900);
    }

    atualizarCarrinho(isNew ? produtoId : null);
}

function removerDoCarrinho(produtoId) {
    delete carrinho[produtoId];
    atualizarCarrinho();
}

function atualizarCarrinho(highlightId) {
    const itensList = document.getElementById('itensPedido');
    const itens = Object.entries(carrinho);

    if (itens.length === 0) {
        itensList.innerHTML = '<div class="vazio">Nenhum item adicionado</div>';
        document.getElementById('subtotal').textContent = 'R$ 0.00';
        document.getElementById('total').textContent = 'R$ 0.00';
        document.getElementById('itemCount').textContent = '0 itens';
        atualizarEstadoAcoes();
        return;
    }

    let total = 0;
    let totalItens = 0;
    itensList.innerHTML = itens.map(([id, item]) => {
        const subtotal = item.quantidade * item.preco;
        total += subtotal;
        totalItens += item.quantidade;
        return `
            <div class="item-pedido" data-id="${id}">
                <div class="item-info">
                    <div class="item-produto">${item.nome}</div>
                    <div class="item-qty">${item.quantidade}x R$ ${item.preco.toFixed(2)}</div>
                </div>
                <div class="item-preco">R$ ${subtotal.toFixed(2)}</div>
                <button type="button" class="btn-remove-item" onclick="removerDoCarrinho(${id})">Remover</button>
            </div>
        `;
    }).join('');

    if (highlightId) {
        const elem = itensList.querySelector(`.item-pedido[data-id="${highlightId}"]`);
        if (elem) {
            elem.classList.add('highlight');
            setTimeout(() => elem.classList.remove('highlight'), 1000);
        }
    }

    document.getElementById('subtotal').textContent = `R$ ${total.toFixed(2)}`;
    document.getElementById('total').textContent = `R$ ${total.toFixed(2)}`;
    document.getElementById('itemCount').textContent = `${totalItens} ${totalItens === 1 ? 'item' : 'itens'}`;
    atualizarEstadoAcoes();
}

function formatStatusPedido(status) {
    const mapa = {
        aberto: 'Aberto',
        em_preparo: 'Em preparo',
        entregue: 'Entregue',
        fechado: 'Fechado',
        cancelado: 'Cancelado'
    };
    return mapa[status] || status || 'Sem status';
}

function limparPedidoAtual() {
    pedidoAtual = null;
    pedidoStatusAtual = null;
    carrinho = {};
    carrinhoOriginal = {};
    atualizarCarrinho();
    atualizarListaSelecaoAtiva();
}

function atualizarEstadoAcoes() {
    const possuiItens = Object.keys(carrinho).length > 0;
    const btnFinalizar = document.getElementById('btnFinalizar');
    const btnNovaVenda = document.getElementById('btnNovaVenda');

    btnFinalizar.disabled = !pedidoAtual;

    if (!possuiItens) {
        btnNovaVenda.disabled = true;
    } else if (!pedidoAtual) {
        btnNovaVenda.disabled = false;
    } else {
        btnNovaVenda.disabled = pedidoStatusAtual !== 'aberto';
    }

    atualizarBotaoNovaVenda();
}

function popularSelectPedidos(pedidos) {
    const select = document.getElementById('pedidoAbertoSelect');
    const valorAtual = pedidoAtual ? String(pedidoAtual) : '';
    select.innerHTML = '<option value="">Selecione um pedido aberto</option>';

    pedidos.forEach((pedido) => {
        const option = document.createElement('option');
        option.value = pedido.id;
        const mesaTxt = pedido.mesa_numero ? `Mesa ${pedido.mesa_numero}` : 'Sem mesa';
        const garcomTxt = pedido.garcom_nome || 'Sem garcom';
        option.textContent = `#${pedido.id} | ${mesaTxt} | ${garcomTxt} | ${formatStatusPedido(pedido.status)} | R$ ${(pedido.total || 0).toFixed(2)}`;
        select.appendChild(option);
    });

    if (valorAtual && pedidos.some((p) => String(p.id) === valorAtual)) {
        select.value = valorAtual;
    } else {
        select.value = '';
    }

    renderPedidosEmAberto(pedidos);
}

function carregarPedidosEmAberto() {
    const caixaId = document.getElementById('caixaSelect').value;
    const pedidoSelect = document.getElementById('pedidoAbertoSelect');
    const pedidoLista = document.getElementById('pedidoAbertoLista');
    const openOrdersCount = document.getElementById('openOrdersCount');
    const filtroMesaEl = document.getElementById('filtroPedidoMesa');
    const filtroGarcomEl = document.getElementById('filtroPedidoGarcom');

    const mesaId = filtroMesaEl ? (filtroMesaEl.value || '') : '';
    const garcomId = filtroGarcomEl ? (filtroGarcomEl.value || '') : '';
    const status = document.getElementById('filtroPedidoStatus').value || '';
    const params = new URLSearchParams();
    if (caixaId) params.append('caixa_id', caixaId);
    if (mesaId) params.append('mesa_id', mesaId);
    if (garcomId) params.append('garcom_id', garcomId);
    if (status) params.append('status', status);

    fetch(`/api/pedidos/em-aberto?${params.toString()}`)
        .then(r => r.json())
        .then(data => {
            if (!data.success) {
                mostrarAlerta('Erro ao carregar pedidos em aberto.', 'error');
                return;
            }
            const pedidos = data.pedidos || [];
            popularSelectPedidos(pedidos);

            if (pedidoAtual && !pedidos.some((p) => p.id === pedidoAtual)) {
                limparPedidoAtual();
            }
        })
        .catch((e) => {
            console.error('Erro ao carregar pedidos em aberto', e);
            mostrarAlerta('Erro ao consultar pedidos em aberto.', 'error');
        });
}

function carregarPedidoPorId(pedidoId) {
    if (!pedidoId) {
        limparPedidoAtual();
        return;
    }

    fetch(`/api/pedidos/${pedidoId}/detalhes-json`)
        .then(r => r.json())
        .then(data => {
            if (!data.success || !data.pedido) {
                mostrarAlerta('Pedido nao encontrado.', 'error');
                return;
            }
            const pedido = data.pedido;
            pedidoAtual = pedido.id;
            pedidoStatusAtual = pedido.status;
            carrinho = {};
            (pedido.itens || []).forEach((item) => {
                carrinho[item.produto_id] = {
                    nome: item.nome,
                    preco: item.preco,
                    quantidade: item.quantidade
                };
            });
            carrinhoOriginal = JSON.parse(JSON.stringify(carrinho));
            const mesaSelect = document.getElementById('mesaSelect');
            if (mesaSelect && pedido.mesa_id) {
                mesaSelect.value = String(pedido.mesa_id);
            }
            document.getElementById('pedidoAbertoSelect').value = String(pedido.id);
            atualizarListaSelecaoAtiva();
            atualizarCarrinho();
            mostrarAlerta(`Pedido #${pedido.id} carregado para pagamento.`, 'success');
        })
        .catch((e) => {
            console.error('Erro ao carregar pedido', e);
            mostrarAlerta('Erro ao carregar pedido selecionado.', 'error');
        });
}

function onChangePedidoAberto() {
    const pedidoId = parseInt(document.getElementById('pedidoAbertoSelect').value, 10);
    if (!pedidoId) {
        limparPedidoAtual();
        return;
    }
    carregarPedidoPorId(pedidoId);
}

function renderPedidosEmAberto(pedidos) {
    const pedidoLista = document.getElementById('pedidoAbertoLista');
    const openOrdersCount = document.getElementById('openOrdersCount');

    if (!pedidos.length) {
        openOrdersCount.textContent = '0 pedidos';
        pedidoLista.innerHTML = '<div class="vazio">Nenhum pedido em aberto com os filtros aplicados</div>';
        return;
    }

    openOrdersCount.textContent = `${pedidos.length} pedido${pedidos.length > 1 ? 's' : ''}`;
    pedidoLista.innerHTML = pedidos.map((pedido) => {
        const mesaTxt = pedido.mesa_numero ? `Mesa ${pedido.mesa_numero}` : 'Sem mesa';
        const garcomTxt = pedido.garcom_nome || 'Sem garcom';
        const caixaTxt = pedido.caixa_nome || 'Sem caixa';
        const clienteTxt = pedido.cliente_nome || 'Cliente nao informado';
        const statusTxt = formatStatusPedido(pedido.status);
        const activeClass = pedidoAtual === pedido.id ? 'active' : '';
        return `
            <button type="button" class="open-order-item ${activeClass}" data-pedido-id="${pedido.id}">
                <div class="open-order-top">
                    <span>Pedido #${pedido.id}</span>
                    <span>R$ ${(pedido.total || 0).toFixed(2)}</span>
                </div>
                <div class="open-order-meta">
                    <span>${mesaTxt}</span>
                    <span>${garcomTxt}</span>
                </div>
                <div class="open-order-meta">
                    <span>${caixaTxt}</span>
                    <span>${clienteTxt}</span>
                </div>
                <div class="open-order-meta">
                    <span>Status: ${statusTxt}</span>
                </div>
            </button>
        `;
    }).join('');

    pedidoLista.querySelectorAll('.open-order-item').forEach((item) => {
        item.addEventListener('click', () => {
            const pedidoId = parseInt(item.dataset.pedidoId, 10);
            const select = document.getElementById('pedidoAbertoSelect');
            select.value = String(pedidoId);
            onChangePedidoAberto();
        });
    });
}

function atualizarListaSelecaoAtiva() {
    const itens = document.querySelectorAll('.open-order-item');
    itens.forEach((item) => {
        const pedidoId = parseInt(item.dataset.pedidoId, 10);
        item.classList.toggle('active', pedidoId === pedidoAtual);
    });
}

function atualizarCaixa() {
    caixaSelecionada = document.getElementById('caixaSelect').value;
    if (!caixaSelecionada) {
        if (Object.keys(carrinho).length > 0) {
            mostrarAlerta('Selecione uma caixa para continuar', 'error');
        }
        limparPedidoAtual();
        document.getElementById('pedidoAbertoSelect').value = '';
        carregarPedidosEmAberto();
        return;
    }

    limparPedidoAtual();
    carregarPedidosEmAberto();
}

function novaVenda() {
    const btnNovaVenda = document.getElementById('btnNovaVenda');
    if (btnNovaVenda && btnNovaVenda.dataset.loading === '1') {
        return;
    }
    if (btnNovaVenda) {
        btnNovaVenda.dataset.loading = '1';
        setButtonLoading(btnNovaVenda, true, 'Processando...', '+ Adicionar Produtos');
    }

    const caixaId = document.getElementById('caixaSelect').value;
    const mesaSelect = document.getElementById('mesaSelect');
    const mesaId = mesaSelect ? (mesaSelect.value || null) : null;

    const itensTodos = Object.entries(carrinho).map(([id, item]) => ({
        produto_id: parseInt(id),
        quantidade: item.quantidade
    }));

    if (pedidoAtual) {
        if (pedidoStatusAtual !== 'aberto') {
            mostrarAlerta('Somente pedidos com status "aberto" podem receber novos itens.', 'error');
            if (btnNovaVenda) {
                btnNovaVenda.dataset.loading = '0';
                setButtonLoading(btnNovaVenda, false, '', '+ Adicionar Produtos');
                atualizarEstadoAcoes();
            }
            return;
        }
        // calcular apenas diferenca em relacao ao carrinhoOriginal
        const delta = [];
        Object.entries(carrinho).forEach(([id, item]) => {
            const origQty = carrinhoOriginal[id] ? carrinhoOriginal[id].quantidade : 0;
            if (item.quantidade > origQty) {
                delta.push({ produto_id: parseInt(id), quantidade: item.quantidade - origQty });
            }
        });
        if (delta.length === 0) {
            mostrarAlerta('Nenhum item novo para adicionar.', 'error');
            if (btnNovaVenda) {
                btnNovaVenda.dataset.loading = '0';
                setButtonLoading(btnNovaVenda, false, '', '+ Adicionar Produtos');
                atualizarEstadoAcoes();
            }
            return;
        }
        fetch(`/api/pedidos/${pedidoAtual}/adicionar`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ itens: delta })
        })
        .then(r => r.json())
        .then(data => {
            const payload = data.data || {};
            if (data.success) {
                mostrarAlerta(`${data.message}`, 'success');
                carrinhoOriginal = JSON.parse(JSON.stringify(carrinho));
                if (payload.total !== undefined) {
                    document.getElementById('total').textContent = `R$ ${parseFloat(payload.total || 0).toFixed(2)}`;
                }
                carregarPedidosEmAberto();
            } else {
                mostrarAlerta(`${data.message}`, 'error');
            }
        })
        .catch(e => mostrarAlerta('Erro ao atualizar pedido: ' + e, 'error'))
        .finally(() => {
            if (btnNovaVenda) {
                btnNovaVenda.dataset.loading = '0';
                setButtonLoading(btnNovaVenda, false, '', '+ Adicionar Produtos');
                atualizarEstadoAcoes();
            }
        });
    } else {
        if (!caixaId) {
            mostrarAlerta('Selecione uma caixa para iniciar nova venda.', 'error');
            if (btnNovaVenda) {
                btnNovaVenda.dataset.loading = '0';
                setButtonLoading(btnNovaVenda, false, '', '+ Adicionar Produtos');
                atualizarEstadoAcoes();
            }
            return;
        }
        if (Object.keys(carrinho).length === 0) {
            mostrarAlerta('Adicione produtos ao carrinho!', 'error');
            if (btnNovaVenda) {
                btnNovaVenda.dataset.loading = '0';
                setButtonLoading(btnNovaVenda, false, '', '+ Adicionar Produtos');
                atualizarEstadoAcoes();
            }
            return;
        }
        fetch('{{ url_for("criar_pedido_api") }}', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ caixa_id: parseInt(caixaId), mesa_id: mesaId, itens: itensTodos })
        })
        .then(r => r.json())
        .then(data => {
            const payload = data.data || {};
            if (data.success) {
                pedidoAtual = data.pedido_id || payload.pedido_id;
                pedidoStatusAtual = 'aberto';
                mostrarAlerta(`${data.message}`, 'success');
                // manter os itens no carrinho ate o operador finalizar
                atualizarBotaoNovaVenda();
                carrinhoOriginal = JSON.parse(JSON.stringify(carrinho));
                carregarPedidosEmAberto();
                document.getElementById('pedidoAbertoSelect').value = String(pedidoAtual);
                atualizarEstadoAcoes();
            } else {
                mostrarAlerta(`${data.message}`, 'error');
            }
        })
        .catch(e => mostrarAlerta('Erro ao criar pedido: ' + e, 'error'))
        .finally(() => {
            if (btnNovaVenda) {
                btnNovaVenda.dataset.loading = '0';
                setButtonLoading(btnNovaVenda, false, '', '+ Adicionar Produtos');
                atualizarEstadoAcoes();
            }
        });
    }
}

function finalizarVenda() {
    if (!pedidoAtual) {
        mostrarAlerta('Nenhum pedido aberto!', 'error');
        return;
    }
    abrirModalPagamento();
}

function obterTotalCarrinho() {
    return Object.values(carrinho).reduce((acc, item) => acc + (item.preco * item.quantidade), 0);
}

function abrirModalPagamento() {
    ultimoElementoComFoco = document.activeElement;
    const total = obterTotalCarrinho();
    document.getElementById('paymentTotalLabel').textContent = `R$ ${total.toFixed(2)}`;
    document.getElementById('paymentValor').value = total.toFixed(2);
    document.getElementById('paymentDinheiro').value = '';
    document.getElementById('paymentCartao').value = '';
    document.getElementById('paymentClienteCrediario').value = '';
    document.getElementById('paymentEmitirComprovante').checked = true;
    document.querySelector('input[name="metodo_pagamento_pdv"][value="dinheiro"]').checked = true;
    atualizarCamposPagamento();
    atualizarInfoDividido();
    const modal = document.getElementById('paymentModal');
    modal.classList.add('open');
    const focusTarget = document.getElementById('btnConfirmarPagamento');
    if (focusTarget) {
        focusTarget.focus();
    }
}

function fecharModalPagamento() {
    const modal = document.getElementById('paymentModal');
    modal.classList.remove('open');
    if (ultimoElementoComFoco && typeof ultimoElementoComFoco.focus === 'function') {
        ultimoElementoComFoco.focus();
    }
}

function atualizarInfoDividido() {
    const dinheiro = parseFloat((document.getElementById('paymentDinheiro').value || '0').replace(',', '.')) || 0;
    const cartao = parseFloat((document.getElementById('paymentCartao').value || '0').replace(',', '.')) || 0;
    const total = obterTotalCarrinho();
    const totalInformado = dinheiro + cartao;
    const diferenca = totalInformado - total;
    if (diferenca >= 0) {
        document.getElementById('splitTotalInfo').textContent = `Total informado: R$ ${totalInformado.toFixed(2)} | Troco: R$ ${diferenca.toFixed(2)}`;
    } else {
        document.getElementById('splitTotalInfo').textContent = `Total informado: R$ ${totalInformado.toFixed(2)} | Falta: R$ ${Math.abs(diferenca).toFixed(2)}`;
    }
}

function atualizarInfoTroco() {
    const metodo = document.querySelector('input[name="metodo_pagamento_pdv"]:checked').value;
    const trocoInfo = document.getElementById('trocoInfo');
    if (!trocoInfo) return;

    const total = obterTotalCarrinho();
    const valorPago = parseFloat((document.getElementById('paymentValor').value || '0').replace(',', '.')) || 0;
    const diferenca = valorPago - total;

    if (metodo === 'dinheiro') {
        if (diferenca >= 0) {
            trocoInfo.textContent = `Troco: R$ ${diferenca.toFixed(2)}`;
        } else {
            trocoInfo.textContent = `Falta: R$ ${Math.abs(diferenca).toFixed(2)}`;
        }
        return;
    }

    if (metodo === 'pix' || metodo === 'cartao') {
        trocoInfo.textContent = `Valor informado: R$ ${valorPago.toFixed(2)}`;
        return;
    }

    trocoInfo.textContent = 'Troco: R$ 0.00';
}

function atualizarCamposPagamento() {
    const metodo = document.querySelector('input[name="metodo_pagamento_pdv"]:checked').value;
    const splitFields = document.getElementById('paymentSplitFields');
    const crediarioFields = document.getElementById('paymentCrediarioFields');
    const defaultFields = document.getElementById('paymentDefaultFields');

    if (metodo === 'dividido') {
        splitFields.style.display = 'grid';
        crediarioFields.style.display = 'none';
        defaultFields.style.display = 'none';
    } else if (metodo === 'crediario') {
        splitFields.style.display = 'none';
        crediarioFields.style.display = 'grid';
        defaultFields.style.display = 'grid';
        document.getElementById('paymentValor').value = '0.00';
    } else {
        splitFields.style.display = 'none';
        crediarioFields.style.display = 'none';
        defaultFields.style.display = 'grid';
    }
    atualizarInfoTroco();
    atualizarInfoDividido();
}

function confirmarFinalizacaoPagamento() {
    const btnConfirmar = document.getElementById('btnConfirmarPagamento');
    if (btnConfirmar && btnConfirmar.dataset.loading === '1') {
        return;
    }
    if (btnConfirmar) {
        btnConfirmar.dataset.loading = '1';
        setButtonLoading(btnConfirmar, true, 'Processando...', 'Confirmar');
    }

    const metodo = document.querySelector('input[name="metodo_pagamento_pdv"]:checked').value;
    const emitirComprovante = document.getElementById('paymentEmitirComprovante').checked;
    let janelaComprovante = null;
    if (emitirComprovante) {
        janelaComprovante = window.open('', '_blank');
    }

    const payload = { metodo_pagamento: metodo };

    if (metodo === 'dividido') {
        const dinheiro = parseFloat((document.getElementById('paymentDinheiro').value || '0').replace(',', '.')) || 0;
        const cartao = parseFloat((document.getElementById('paymentCartao').value || '0').replace(',', '.')) || 0;
        const totalPedido = obterTotalCarrinho();
        if ((dinheiro + cartao) < totalPedido) {
            mostrarAlerta(`Valor informado insuficiente. Falta R$ ${(totalPedido - (dinheiro + cartao)).toFixed(2)}.`, 'error');
            if (btnConfirmar) {
                btnConfirmar.dataset.loading = '0';
                setButtonLoading(btnConfirmar, false, '', 'Confirmar');
            }
            return;
        }
        payload.split_pagamento = { dinheiro, cartao };
    } else {
        const valorPago = parseFloat((document.getElementById('paymentValor').value || '').replace(',', '.'));
        if (!Number.isNaN(valorPago)) {
            if (metodo === 'dinheiro') {
                const totalPedido = obterTotalCarrinho();
                if (valorPago < totalPedido) {
                    mostrarAlerta(`Valor recebido insuficiente. Falta R$ ${(totalPedido - valorPago).toFixed(2)}.`, 'error');
                    if (btnConfirmar) {
                        btnConfirmar.dataset.loading = '0';
                        setButtonLoading(btnConfirmar, false, '', 'Confirmar');
                    }
                    return;
                }
            }
            payload.valor_pago = valorPago;
        }
        if (metodo === 'crediario') {
            payload.cliente_crediario = document.getElementById('paymentClienteCrediario').value || '';
        }
    }

    fetch(`/api/pedidos/${pedidoAtual}/finalizar`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(r => r.json())
    .then(data => {
        const payload = data.data || {};
        if (data.success) {
            const pedidoIdComprovante = payload.pedido_id || pedidoAtual;
            let msg = data.message;
            const metodoPagamento = data.metodo_pagamento || payload.metodo_pagamento;
            const valorPago = (data.valor_pago !== undefined ? data.valor_pago : payload.valor_pago);
            if (metodoPagamento) {
                msg += ' (pagamento: ' + metodoPagamento;
                if (valorPago !== null && valorPago !== undefined) {
                    msg += ' R$ ' + parseFloat(valorPago).toFixed(2);
                }
                msg += ')';
            }
            mostrarAlerta(`OK ${msg}`, 'success');
            fecharModalPagamento();
            if (emitirComprovante && pedidoIdComprovante) {
                const comprovanteUrl = `/pedidos/${pedidoIdComprovante}/comprovante`;
                if (janelaComprovante) {
                    janelaComprovante.location.href = comprovanteUrl;
                } else {
                    window.open(comprovanteUrl, '_blank');
                }
            } else if (janelaComprovante) {
                janelaComprovante.close();
            }
            limparPedidoAtual();
            carregarPedidosEmAberto();
        } else {
            if (janelaComprovante) janelaComprovante.close();
            mostrarAlerta(`Erro: ${data.message}`, 'error');
        }
    })
    .catch(e => {
        if (janelaComprovante) janelaComprovante.close();
        mostrarAlerta('Erro ao finalizar: ' + e, 'error');
    })
    .finally(() => {
        if (btnConfirmar) {
            btnConfirmar.dataset.loading = '0';
            setButtonLoading(btnConfirmar, false, '', 'Confirmar');
        }
    });
}
function mostrarAlerta(msg, tipo) {
    const alertas = document.getElementById('alertas');
    const alert = document.createElement('div');
    alert.className = `alert alert-${tipo}`;
    alert.textContent = msg;
    alertas.appendChild(alert);
    setTimeout(() => alert.remove(), 3000);
}

function mostrarAlertaTemporario(msg, tipo, duracaoMs) {
    const alertas = document.getElementById('alertas');
    const alert = document.createElement('div');
    alert.className = `alert alert-${tipo}`;
    alert.textContent = msg;
    alertas.appendChild(alert);
    setTimeout(() => alert.remove(), duracaoMs || 1800);
}

function atualizarBotaoNovaVenda() {
    const btn = document.getElementById('btnNovaVenda');
    if (pedidoAtual && pedidoStatusAtual === 'aberto') {
        btn.textContent = '+ Adicionar Produtos';
    } else if (pedidoAtual) {
        btn.textContent = 'Pedido bloqueado';
    } else {
        btn.textContent = '+ Nova Venda';
    }
}

// Filtro de produtos
function normalizeSearchText(text) {
    return (text || '').toString().trim().toLowerCase();
}

function normalizeCode(text) {
    return normalizeSearchText(text).replace(/[^a-z0-9]/g, '');
}

function getProductCards() {
    return Array.from(document.querySelectorAll('.produto-card'));
}

function initProdutoDetalhesNoPdv() {
    getProductCards().forEach((card) => {
        card.addEventListener('click', (event) => {
            if (event.target.closest('.btn-add-produto')) {
                return;
            }

            const detalheUrl = card.dataset.detalheUrl;
            if (!detalheUrl) return;
            window.location.href = detalheUrl;
        });
    });
}

function findProductCardByCodeExact(codeValue) {
    const normalizedCode = normalizeCode(codeValue);
    if (!normalizedCode) return null;
    return getProductCards().find((card) => normalizeCode(card.dataset.codigo) === normalizedCode) || null;
}

function addProductFromCard(card) {
    if (!card) return false;
    const estoque = parseInt(card.dataset.estoque || '0', 10);
    if (estoque <= 0) {
        mostrarAlerta('Produto sem estoque disponivel.', 'warning');
        return false;
    }
    adicionarAoCarrinho(parseInt(card.dataset.id, 10), card.dataset.nome, parseFloat(card.dataset.preco));
    return true;
}

function applyProductFilter(queryText) {
    const query = normalizeSearchText(queryText);
    const queryCode = normalizeCode(queryText);

    getProductCards().forEach((card) => {
        if (!query) {
            card.style.display = '';
            return;
        }

        const nome = normalizeSearchText(card.dataset.nome);
        const codigo = normalizeSearchText(card.dataset.codigo);
        const codigoNormalizado = normalizeCode(card.dataset.codigo);
        const categoria = normalizeSearchText(card.dataset.categoria);

        const matchNome = nome.includes(query);
        const matchCategoria = categoria.includes(query);
        const matchCodigo = codigo.includes(query) || (queryCode && codigoNormalizado.includes(queryCode));

        card.style.display = (matchNome || matchCategoria || matchCodigo) ? '' : 'none';
    });
}

// quando scanner preencher o campo escondido, procurar e adicionar
const barcodeInput = document.getElementById('barcodeInput');
if (barcodeInput) {
    barcodeInput.addEventListener('change', function (e) {
        const code = e.target.value.trim();
        if (code) {
            const card = findProductCardByCodeExact(code);
            if (addProductFromCard(card)) {
                mostrarAlertaTemporario(`Produto "${card.dataset.nome}" adicionado pelo codigo ${code}.`, 'success', 1700);
                const filtroInput = document.getElementById('filtroNome');
                if (filtroInput) filtroInput.value = '';
                applyProductFilter('');
            } else {
                mostrarAlerta('Produto nao encontrado para o codigo: ' + code, 'error');
            }
            e.target.value = '';
        }
    });
}

document.getElementById('filtroNome').addEventListener('input', (e) => {
    const valorDigitado = e.target.value || '';
    const cardCodigoExato = findProductCardByCodeExact(valorDigitado);

    if (cardCodigoExato) {
        addProductFromCard(cardCodigoExato);
        mostrarAlertaTemporario(`Produto "${cardCodigoExato.dataset.nome}" adicionado pelo codigo ${valorDigitado}.`, 'success', 1700);
        e.target.value = '';
        applyProductFilter('');
        return;
    }

    applyProductFilter(valorDigitado);
});

document.getElementById('filtroNome').addEventListener('keydown', (e) => {
    if (e.key !== 'Enter') return;
    e.preventDefault();
    const cardDisponivel = getProductCards().find((card) => {
        const estoque = parseInt(card.dataset.estoque || '0', 10);
        return card.style.display !== 'none' && estoque > 0;
    });
    if (cardDisponivel) {
        addProductFromCard(cardDisponivel);
    } else {
        mostrarAlerta('Nenhum produto disponivel para adicionar.', 'warning');
    }
});

document.querySelectorAll('input[name="metodo_pagamento_pdv"]').forEach((radio) => {
    radio.addEventListener('change', atualizarCamposPagamento);
});
document.getElementById('paymentValor').addEventListener('input', atualizarInfoTroco);
document.getElementById('paymentDinheiro').addEventListener('input', atualizarInfoDividido);
document.getElementById('paymentCartao').addEventListener('input', atualizarInfoDividido);
document.getElementById('paymentModal').addEventListener('click', (event) => {
    if (event.target.id === 'paymentModal') {
        fecharModalPagamento();
    }
});
document.addEventListener('keydown', (event) => {
    const modal = document.getElementById('paymentModal');
    if (!modal.classList.contains('open')) return;
    if (event.key === 'Escape') {
        fecharModalPagamento();
        return;
    }
    if (event.key !== 'Tab') return;
    const focaveis = Array.from(modal.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex=\"-1\"])'))
        .filter((el) => !el.disabled && el.offsetParent !== null);
    if (!focaveis.length) return;
    const primeiro = focaveis[0];
    const ultimo = focaveis[focaveis.length - 1];
    if (event.shiftKey && document.activeElement === primeiro) {
        event.preventDefault();
        ultimo.focus();
    } else if (!event.shiftKey && document.activeElement === ultimo) {
        event.preventDefault();
        primeiro.focus();
    }
});

document.addEventListener('keydown', (event) => {
    const filtroInput = document.getElementById('filtroNome');
    if (event.ctrlKey && event.key.toLowerCase() === 'f') {
        event.preventDefault();
        if (filtroInput) {
            filtroInput.focus();
            filtroInput.select();
        }
        return;
    }
    if (event.key === 'F4') {
        const btnNova = document.getElementById('btnNovaVenda');
        if (btnNova && !btnNova.disabled) {
            event.preventDefault();
            novaVenda();
        }
        return;
    }
    if (event.key === 'F2') {
        const btnFin = document.getElementById('btnFinalizar');
        if (btnFin && !btnFin.disabled) {
            event.preventDefault();
            finalizarVenda();
        }
    }
});
// ajustar texto inicial do botao de venda
atualizarEstadoAcoes();
carregarPedidosEmAberto();
initProdutoDetalhesNoPdv();
</script>
{% endblock %}






```

---

### Arquivo: `templates\vendas\pedidos\comprovante.html`

```html
{% extends "base.html" %}

{% block title %}Comprovante Pedido #{{ pedido.id }}{% endblock %}

{% block extra_css %}
<style>
    .receipt-wrap {
        max-width: 780px;
        margin: 0 auto;
    }

    .receipt-card {
        background: #fff;
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 20px;
        box-shadow: var(--shadow);
    }

    .receipt-header {
        text-align: center;
        padding-bottom: 12px;
        margin-bottom: 16px;
        border-bottom: 1px dashed #9ca3af;
    }

    .receipt-logo-wrap {
        margin-bottom: 8px;
    }

    .receipt-logo {
        max-height: 72px;
        width: auto;
    }

    .receipt-header h2 {
        margin: 0 0 6px;
        font-size: 1.2rem;
    }

    .receipt-muted {
        color: #64748b;
        font-size: 0.9rem;
    }

    .receipt-meta {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 8px;
        margin-bottom: 14px;
    }

    .receipt-items {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 16px;
    }

    .receipt-items th,
    .receipt-items td {
        border-bottom: 1px solid #e5e7eb;
        padding: 8px 4px;
        text-align: left;
        font-size: 0.95rem;
    }

    .receipt-total {
        text-align: right;
        font-size: 1.1rem;
        font-weight: 700;
    }

    .receipt-actions {
        margin-top: 16px;
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
    }

    @media print {
        .navbar,
        .footer,
        .receipt-actions {
            display: none !important;
        }

        .main-content {
            padding: 0;
        }

        .receipt-card {
            border: none;
            box-shadow: none;
        }
    }

    @media (max-width: 640px) {
        .receipt-meta {
            grid-template-columns: 1fr;
        }
    }
</style>
{% endblock %}

{% block content %}
<div class="receipt-wrap">
    <div class="page-header">
        <h1>Comprovante #{{ pedido.id }}</h1>
    </div>

    <div class="receipt-card">
        <div class="receipt-header">
            {% if empresa and empresa.logo_path %}
            <div class="receipt-logo-wrap">
                <img src="{{ url_for('static', filename=empresa.logo_path) }}" alt="Logo da empresa" class="receipt-logo">
            </div>
            {% endif %}
            <h2>{{ (empresa.nome_fantasia if empresa and empresa.nome_fantasia else (empresa.razao_social if empresa and empresa.razao_social else 'Empresa nao cadastrada')) }}</h2>
            {% if empresa and empresa.razao_social and empresa.nome_fantasia and empresa.razao_social != empresa.nome_fantasia %}
            <div class="receipt-muted">{{ empresa.razao_social }}</div>
            {% endif %}
            {% if empresa and empresa.cnpj %}
            <div class="receipt-muted">CNPJ: {{ empresa.cnpj }}</div>
            {% endif %}
            {% if empresa and empresa.endereco %}
            <div class="receipt-muted">
                {{ empresa.endereco }}{% if empresa.cidade %} - {{ empresa.cidade }}{% endif %}{% if empresa.estado %}/{{ empresa.estado }}{% endif %}
            </div>
            {% endif %}
            {% if empresa and empresa.telefone %}
            <div class="receipt-muted">Telefone: {{ empresa.telefone }}</div>
            {% endif %}
        </div>

        <div class="receipt-meta">
            <div><strong>Pedido:</strong> #{{ pedido.id }}</div>
            <div><strong>Mesa:</strong> {{ pedido.mesa.numero if pedido.mesa else '-' }}</div>
            <div><strong>Caixa:</strong> {{ pedido.caixa.nome if pedido.caixa else '-' }}</div>
            <div><strong>Criado em:</strong> {{ pedido.criado_em.strftime('%d/%m/%Y %H:%M') if pedido.criado_em else '-' }}</div>
            <div><strong>Fechado em:</strong> {{ pedido.fechado_em.strftime('%d/%m/%Y %H:%M') if pedido.fechado_em else '-' }}</div>
            <div><strong>Pagamento:</strong> {{ pedido.metodo_pagamento or '-' }}</div>
            <div><strong>Valor pago:</strong> {% if pedido.valor_pago is not none %}R$ {{ '%.2f'|format(pedido.valor_pago) }}{% else %}-{% endif %}</div>
            <div><strong>Troco repassado:</strong> {% if troco_repassado is not none %}R$ {{ '%.2f'|format(troco_repassado) }}{% else %}-{% endif %}</div>
        </div>

        <table class="receipt-items">
            <thead>
                <tr>
                    <th>Item</th>
                    <th>Qtd</th>
                    <th>Unitario</th>
                    <th>Total</th>
                </tr>
            </thead>
            <tbody>
                {% for item in pedido.itens %}
                <tr>
                    <td data-label="Item">{{ item.produto.nome if item.produto else ('Produto #' ~ item.produto_id) }}</td>
                    <td data-label="Qtd">{{ item.quantidade }}</td>
                    <td data-label="Unitario">R$ {{ '%.2f'|format(item.preco_unitario) }}</td>
                    <td data-label="Total">R$ {{ '%.2f'|format(item.quantidade * item.preco_unitario) }}</td>
                </tr>
                {% else %}
                <tr>
                    <td colspan="4">Sem itens no pedido.</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>

        <div class="receipt-total">Total: R$ {{ '%.2f'|format(pedido.total or 0) }}</div>

        {% if empresa and empresa.mensagem_comprovante %}
        <p class="receipt-muted text-center mt-3">{{ empresa.mensagem_comprovante }}</p>
        {% endif %}
    </div>

    <div class="receipt-actions">
        <button type="button" class="btn btn-primary" onclick="window.print()">Imprimir</button>
        <a href="{{ url_for('listar_pedidos') }}" class="btn btn-outline-secondary">Voltar</a>
    </div>
</div>
{% endblock %}
```

---

### Arquivo: `templates\vendas\pedidos\detalhes_pedido.html`

```html
{% extends "base.html" %}

{% block title %}Detalhes do Pedido - SystemLR{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Detalhes da Venda #{{ pedido.id }}</h1>
    <a href="{{ url_for('listar_pedidos') }}" class="btn btn-outline-secondary">Voltar</a>
</div>

<div class="card mb-3">
    <div class="card-header">Informacoes Gerais</div>
    <div class="card-body p-0">
        <div class="table-responsive m-0">
            <table class="table table-striped table-sm m-0">
                <tbody>
                    <tr>
                        <th>Status</th>
                        <td>
                            {% if pedido.status == 'aberto' %}
                                Aberto
                            {% elif pedido.status == 'em_preparo' %}
                                Em preparo
                            {% elif pedido.status == 'entregue' %}
                                Entregue
                            {% elif pedido.status == 'fechado' %}
                                Venda concluida
                            {% elif pedido.status == 'cancelado' %}
                                Cancelado
                            {% else %}
                                {{ pedido.status }}
                            {% endif %}
                        </td>
                    </tr>
                    <tr>
                        <th>Horario do pedido</th>
                        <td>{{ pedido.criado_em.strftime('%d/%m/%Y %H:%M:%S') if pedido.criado_em else '-' }}</td>
                    </tr>
                    <tr>
                        <th>Horario de fechamento</th>
                        <td>{{ pedido.fechado_em.strftime('%d/%m/%Y %H:%M:%S') if pedido.fechado_em else '-' }}</td>
                    </tr>
                    <tr>
                        <th>Garcom</th>
                        <td>{{ pedido.garcom.nome if pedido.garcom else 'Nao atribuido' }}</td>
                    </tr>
                    <tr>
                        <th>Caixa</th>
                        <td>{{ pedido.caixa.nome if pedido.caixa else '-' }}</td>
                    </tr>
                    <tr>
                        <th>Operador de caixa</th>
                        <td>
                            {% if pedido.caixa and pedido.caixa.funcionario %}
                                {{ pedido.caixa.funcionario.nome }}
                            {% else %}
                                -
                            {% endif %}
                        </td>
                    </tr>
                    <tr>
                        <th>Mesa</th>
                        <td>{{ pedido.mesa.numero if pedido.mesa else '-' }}</td>
                    </tr>
                    <tr>
                        <th>Cliente</th>
                        <td>{{ pedido.cliente_nome or '-' }}</td>
                    </tr>
                    <tr>
                        <th>Celular</th>
                        <td>{{ pedido.cliente_celular or '-' }}</td>
                    </tr>
                    <tr>
                        <th>Pagamento</th>
                        <td>{{ pedido.metodo_pagamento or '-' }}</td>
                    </tr>
                    <tr>
                        <th>Valor pago</th>
                        <td>{% if pedido.valor_pago is not none %}R$ {{ '%.2f'|format(pedido.valor_pago) }}{% else %}-{% endif %}</td>
                    </tr>
                    <tr>
                        <th>Total</th>
                        <td><strong>R$ {{ '%.2f'|format(pedido.total or 0) }}</strong></td>
                    </tr>
                    <tr>
                        <th>Observacoes</th>
                        <td>{{ pedido.observacoes or '-' }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</div>

<div class="card">
    <div class="card-header">Itens do Pedido</div>
    <div class="card-body p-0">
        <div class="table-responsive m-0">
            <table class="table table-hover m-0">
                <thead>
                    <tr>
                        <th>Produto</th>
                        <th>Quantidade</th>
                        <th>Preco unitario</th>
                        <th>Subtotal</th>
                    </tr>
                </thead>
                <tbody>
                    {% for item in pedido.itens %}
                    <tr>
                        <td data-label="Produto">{{ item.produto.nome if item.produto else '-' }}</td>
                        <td data-label="Quantidade">{{ item.quantidade }}</td>
                        <td data-label="Preco unitario">R$ {{ '%.2f'|format(item.preco_unitario) }}</td>
                        <td data-label="Subtotal">R$ {{ '%.2f'|format(item.quantidade * item.preco_unitario) }}</td>
                    </tr>
                    {% else %}
                    <tr>
                        <td colspan="4" class="text-center">Nenhum item no pedido</td>
                    </tr>
                    {% endfor %}
                </tbody>
                <tfoot>
                    <tr>
                        <th colspan="3" class="text-end">Total</th>
                        <th>R$ {{ '%.2f'|format(pedido.total or 0) }}</th>
                    </tr>
                </tfoot>
            </table>
        </div>
    </div>
</div>
{% endblock %}
```

---

### Arquivo: `templates\vendas\pedidos\editar_pedido.html`

```html
{% extends "base.html" %}

{% block title %}Editar Pedido - SystemLR{% endblock %}

{% block extra_css %}
<style>
    .pedido-form-wrap {
        max-width: 980px;
        margin: 0 auto;
    }

    .pedido-item-row {
        display: grid;
        grid-template-columns: minmax(0, 1fr) 130px auto;
        gap: 8px;
        align-items: center;
        margin-bottom: 8px;
    }

    @media (max-width: 768px) {
        .pedido-item-row {
            grid-template-columns: 1fr;
        }
    }
</style>
{% endblock %}

{% block extra_js %}
<script>
let itemCount = {{ pedido.itens|length }};

function adicionarItem() {
    const container = document.getElementById('itensContainer');
    const row = document.createElement('div');
    row.className = 'pedido-item-row';
    row.innerHTML = `
        <select name="produto_${itemCount}" required class="form-select">
            <option value="">Selecione um produto</option>
            {% for p in produtos %}
            <option value="{{ p.id }}">{{ p.nome }}</option>
            {% endfor %}
        </select>
        <input type="number" name="quantidade_${itemCount}" value="1" min="1" required class="form-control">
        <button type="button" class="btn btn-outline-danger" onclick="this.parentElement.remove();">Remover</button>
    `;
    container.appendChild(row);
    itemCount++;
    document.getElementById('item_count').value = itemCount;
}

function togglePagamentoFields() {
    const metodo = document.getElementById('metodo_pagamento').value;
    const split = document.getElementById('splitPagamentoFields');
    const crediario = document.getElementById('crediarioFields');
    const valor = document.getElementById('valorPagoField');

    if (metodo === 'dividido') {
        split.style.display = 'grid';
        crediario.style.display = 'none';
        valor.style.display = 'none';
    } else if (metodo === 'crediario') {
        split.style.display = 'none';
        crediario.style.display = 'block';
        valor.style.display = 'block';
    } else if (metodo) {
        split.style.display = 'none';
        crediario.style.display = 'none';
        valor.style.display = 'block';
    } else {
        split.style.display = 'none';
        crediario.style.display = 'none';
        valor.style.display = 'none';
    }
}

document.addEventListener('DOMContentLoaded', togglePagamentoFields);
</script>
{% endblock %}

{% block content %}
<div class="pedido-form-wrap">
    <div class="page-header">
        <h1>Editar Pedido #{{ pedido.id }}</h1>
        <a href="{{ url_for('listar_pedidos') }}" class="btn btn-outline-secondary">Voltar</a>
    </div>

    <div class="form-container">
        <form method="POST" id="formPedidoEdit" class="form" onsubmit="return validarFormulario('formPedidoEdit')">
            <div class="form-row">
                {% if atendimento_mesas_ativo %}
                <div class="form-group">
                    <label for="mesa_id">Mesa (opcional)</label>
                    <select name="mesa_id" id="mesa_id" class="form-select">
                        <option value="">Nenhuma</option>
                        {% for m in mesas %}
                        <option value="{{ m.id }}" {% if pedido.mesa_id==m.id %}selected{% endif %}>{{ m.numero }}</option>
                        {% endfor %}
                    </select>
                </div>
                {% endif %}

                <div class="form-group">
                    <label for="caixa_id">Caixa</label>
                    <select name="caixa_id" id="caixa_id" class="form-select" required>
                        <option value="">Selecione</option>
                        {% for c in caixas %}
                        <option value="{{ c.id }}" {% if pedido.caixa_id==c.id %}selected{% endif %}>{{ c.nome }}</option>
                        {% endfor %}
                    </select>
                </div>
            </div>

            <div class="form-row">
                <div class="form-group">
                    <label for="metodo_pagamento">Metodo de pagamento</label>
                    <select name="metodo_pagamento" id="metodo_pagamento" class="form-select" onchange="togglePagamentoFields()">
                        <option value="" {% if not pedido.metodo_pagamento %}selected{% endif %}>Nao informado</option>
                        <option value="dinheiro" {% if pedido.metodo_pagamento and 'dinheiro' in pedido.metodo_pagamento and 'dividido' not in pedido.metodo_pagamento %}selected{% endif %}>Dinheiro</option>
                        <option value="cartao" {% if pedido.metodo_pagamento and 'cartao' in pedido.metodo_pagamento and 'dividido' not in pedido.metodo_pagamento %}selected{% endif %}>Cartao</option>
                        <option value="pix" {% if pedido.metodo_pagamento and 'pix' in pedido.metodo_pagamento %}selected{% endif %}>Pix</option>
                        <option value="crediario" {% if pedido.metodo_pagamento and 'crediario' in pedido.metodo_pagamento %}selected{% endif %}>Crediario</option>
                        <option value="dividido" {% if pedido.metodo_pagamento and 'dividido' in pedido.metodo_pagamento %}selected{% endif %}>Dividido (dinheiro + cartao)</option>
                    </select>
                </div>

                <div class="form-group" id="valorPagoField">
                    <label for="valor_pago">Valor pago</label>
                    <input type="number" step="0.01" name="valor_pago" id="valor_pago" class="form-control" value="{% if pedido.valor_pago is not none %}{{ '%.2f'|format(pedido.valor_pago) }}{% endif %}">
                </div>
            </div>

            <div class="form-group" id="crediarioFields" style="display:none;">
                <label for="cliente_crediario">Cliente crediario (opcional)</label>
                <input type="text" name="cliente_crediario" id="cliente_crediario" class="form-control" placeholder="Nome do cliente">
            </div>

            <div class="form-row" id="splitPagamentoFields" style="display:none;">
                <div class="form-group">
                    <label for="valor_dinheiro">Valor em dinheiro</label>
                    <input type="number" step="0.01" name="valor_dinheiro" id="valor_dinheiro" class="form-control" placeholder="0.00">
                </div>
                <div class="form-group">
                    <label for="valor_cartao">Valor em cartao</label>
                    <input type="number" step="0.01" name="valor_cartao" id="valor_cartao" class="form-control" placeholder="0.00">
                </div>
            </div>

            <div class="form-row">
                <div class="form-group">
                    <label for="status">Status</label>
                    <select name="status" id="status" class="form-select" required>
                        <option value="aberto" {% if pedido.status=='aberto' %}selected{% endif %}>Aberto</option>
                        <option value="em_preparo" {% if pedido.status=='em_preparo' %}selected{% endif %}>Em preparo</option>
                        <option value="entregue" {% if pedido.status=='entregue' %}selected{% endif %}>Entregue</option>
                        <option value="fechado" {% if pedido.status=='fechado' %}selected{% endif %}>Fechado</option>
                        <option value="cancelado" {% if pedido.status=='cancelado' %}selected{% endif %}>Cancelado</option>
                    </select>
                </div>
            </div>

            <div class="form-group">
                <label for="observacoes">Observacoes</label>
                <textarea name="observacoes" id="observacoes" class="form-control" rows="3">{{ pedido.observacoes }}</textarea>
            </div>

            <div class="d-flex flex-wrap justify-content-between align-items-center gap-2">
                <h3 class="m-0">Itens</h3>
                <button type="button" class="btn btn-outline-primary" onclick="adicionarItem()">Adicionar Item</button>
            </div>

            <div id="itensContainer" class="mt-2">
                {% for item in pedido.itens %}
                <div class="pedido-item-row">
                    <select name="produto_{{ loop.index0 }}" required class="form-select">
                        <option value="">Selecione um produto</option>
                        {% for p in produtos %}
                        <option value="{{ p.id }}" {% if p.id==item.produto_id %}selected{% endif %}>{{ p.nome }}</option>
                        {% endfor %}
                    </select>
                    <input type="number" name="quantidade_{{ loop.index0 }}" value="{{ item.quantidade }}" min="1" required class="form-control">
                    <button type="button" class="btn btn-outline-danger" onclick="this.parentElement.remove();">Remover</button>
                </div>
                {% endfor %}
            </div>

            <input type="hidden" name="item_count" id="item_count" value="{{ pedido.itens|length }}">

            <div class="form-actions">
                <button type="submit" class="btn btn-primary">Salvar Pedido</button>
                <a href="{{ url_for('listar_pedidos') }}" class="btn btn-outline-secondary">Cancelar</a>
            </div>
        </form>
    </div>
</div>
{% endblock %}
```

---

### Arquivo: `templates\vendas\pedidos\novo_pedido.html`

```html
{% extends "base.html" %}

{% block title %}Novo Pedido - SystemLR{% endblock %}

{% block extra_css %}
<style>
    .pedido-form-wrap {
        max-width: 980px;
        margin: 0 auto;
    }

    .pedido-item-row {
        display: grid;
        grid-template-columns: minmax(0, 1fr) 130px auto;
        gap: 8px;
        align-items: center;
        margin-bottom: 8px;
    }

    @media (max-width: 768px) {
        .pedido-item-row {
            grid-template-columns: 1fr;
        }
    }
</style>
{% endblock %}

{% block extra_js %}
<script>
let itemCount = 0;

function adicionarItem() {
    const container = document.getElementById('itensContainer');
    const row = document.createElement('div');
    row.className = 'pedido-item-row';
    row.innerHTML = `
        <select name="produto_${itemCount}" required class="form-select">
            <option value="">Selecione um produto</option>
            {% for p in produtos %}
            <option value="{{ p.id }}">{{ p.nome }}</option>
            {% endfor %}
        </select>
        <input type="number" name="quantidade_${itemCount}" value="1" min="1" required class="form-control">
        <button type="button" class="btn btn-outline-danger" onclick="this.parentElement.remove();">Remover</button>
    `;
    container.appendChild(row);
    itemCount++;
    document.getElementById('item_count').value = itemCount;
}
</script>
{% endblock %}

{% block content %}
<div class="pedido-form-wrap">
    <div class="page-header">
        <h1>Novo Pedido</h1>
        <a href="{{ url_for('listar_pedidos') }}" class="btn btn-outline-secondary">Voltar</a>
    </div>

    <div class="form-container">
        <form method="POST" id="formPedido" class="form" onsubmit="return validarFormulario('formPedido')">
            <div class="form-row">
                {% if atendimento_mesas_ativo %}
                <div class="form-group">
                    <label for="mesa_id">Mesa (opcional)</label>
                    <select name="mesa_id" id="mesa_id" class="form-select">
                        <option value="">Nenhuma</option>
                        {% for m in mesas %}
                        <option value="{{ m.id }}">{{ m.numero }}</option>
                        {% endfor %}
                    </select>
                </div>
                {% endif %}

                <div class="form-group">
                    <label for="caixa_id">Caixa</label>
                    <select name="caixa_id" id="caixa_id" class="form-select" required>
                        <option value="">Selecione</option>
                        {% for c in caixas %}
                        <option value="{{ c.id }}">{{ c.nome }}</option>
                        {% endfor %}
                    </select>
                </div>
            </div>

            <div class="form-group">
                <label for="observacoes">Observacoes</label>
                <textarea name="observacoes" id="observacoes" class="form-control" rows="3"></textarea>
            </div>

            <div class="d-flex flex-wrap justify-content-between align-items-center gap-2">
                <h3 class="m-0">Itens</h3>
                <button type="button" class="btn btn-outline-primary" onclick="adicionarItem()">Adicionar Item</button>
            </div>

            <div id="itensContainer" class="mt-2"></div>
            <input type="hidden" name="item_count" id="item_count" value="0">

            <div class="form-actions">
                <button type="submit" class="btn btn-primary">Salvar Pedido</button>
                <a href="{{ url_for('listar_pedidos') }}" class="btn btn-outline-secondary">Cancelar</a>
            </div>
        </form>
    </div>
</div>
{% endblock %}
```

---

### Arquivo: `templates\vendas\pedidos\pedidos.html`

```html
﻿{% extends "base.html" %}

{% block title %}Pedidos - SystemLR{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/pages/pedidos.css') }}">
{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Pedidos</h1>
    <a href="{{ url_for('novo_pedido') }}" class="btn btn-primary">Novo Pedido</a>
</div>

<div class="section pedido-filtros">
    <form method="GET" class="pedido-filtros-form">
        <input type="text" name="busca" class="form-control" placeholder="Buscar por pedido, cliente, celular, mesa ou caixa" value="{{ busca or '' }}">
        <select name="status" class="form-select">
            <option value="">Todos os status</option>
            <option value="aberto" {% if status_filtro=='aberto' %}selected{% endif %}>Aberto</option>
            <option value="em_preparo" {% if status_filtro=='em_preparo' %}selected{% endif %}>Em preparo</option>
            <option value="entregue" {% if status_filtro=='entregue' %}selected{% endif %}>Entregue</option>
            <option value="fechado" {% if status_filtro=='fechado' %}selected{% endif %}>Venda concluida</option>
            <option value="cancelado" {% if status_filtro=='cancelado' %}selected{% endif %}>Cancelado</option>
        </select>
        <button type="submit" class="btn btn-primary">Filtrar</button>
        <a href="{{ url_for('listar_pedidos') }}" class="btn btn-outline-secondary">Limpar</a>
    </form>
</div>

<div class="card mb-3">
    <div class="card-header">Alertas de Comandas (QR Code)</div>
    <div class="card-body">
        <p id="sse-status" class="text-muted mb-2">Aguardando novos pedidos...</p>
        <ul id="alert-list" class="list-unstyled m-0"></ul>
    </div>
</div>

<div class="table-responsive">
    <table class="table table-hover align-middle">
        <thead>
            <tr>
                <th>ID</th>
                <th>Mesa</th>
                <th>Caixa</th>
                <th>Cliente</th>
                <th class="col-celular">Celular</th>
                <th class="col-garcom">Garcom</th>
                <th>Total</th>
                <th class="col-pagamento">Pagamento</th>
                <th class="col-valor-pago">Valor pago</th>
                <th>Status</th>
                <th>Acoes</th>
            </tr>
        </thead>
        <tbody>
            {% for pedido in pedidos %}
            <tr>
                <td data-label="ID">{{ pedido.id }}</td>
                <td data-label="Mesa">{{ pedido.mesa.numero if pedido.mesa else '' }}</td>
                <td data-label="Caixa">{{ pedido.caixa.nome if pedido.caixa else '' }}</td>
                <td data-label="Cliente">{{ pedido.cliente_nome or '-' }}</td>
                <td data-label="Celular" class="col-celular">{{ pedido.cliente_celular or '-' }}</td>
                <td data-label="Garcom" class="col-garcom">{{ pedido.garcom.nome if pedido.garcom else 'Nao atribuido' }}</td>
                <td data-label="Total">R$ {{ '%.2f'|format(pedido.total) }}</td>
                <td data-label="Pagamento" class="col-pagamento">
                    {% if pedido.metodo_pagamento %}
                        {% set metodo = pedido.metodo_pagamento|lower %}
                        {% if 'dividido' in metodo %}
                            <span class="badge text-bg-info">Dividido</span>
                        {% elif 'crediario' in metodo %}
                            <span class="badge text-bg-warning">Crediario</span>
                        {% elif 'dinheiro' in metodo %}
                            <span class="badge text-bg-success">Dinheiro</span>
                        {% elif 'cartao' in metodo %}
                            <span class="badge text-bg-primary">Cartao</span>
                        {% elif 'pix' in metodo %}
                            <span class="badge text-bg-success">Pix</span>
                        {% else %}
                            <span class="badge text-bg-secondary">{{ pedido.metodo_pagamento }}</span>
                        {% endif %}
                        <div class="pedido-pagamento-linha">{{ pedido.metodo_pagamento }}</div>
                    {% else %}
                        -
                    {% endif %}
                </td>
                <td data-label="Valor pago" class="col-valor-pago">{% if pedido.valor_pago is not none %}R$ {{ '%.2f'|format(pedido.valor_pago) }}{% else %}-{% endif %}</td>
                <td data-label="Status">
                    {% if pedido.status == 'aberto' %}
                        <span class="pedido-status-badge pedido-status-aberto">Aberto</span>
                    {% elif pedido.status == 'em_preparo' %}
                        <span class="pedido-status-badge pedido-status-em_preparo">Em preparo</span>
                    {% elif pedido.status == 'entregue' %}
                        <span class="pedido-status-badge pedido-status-entregue">Entregue</span>
                    {% elif pedido.status == 'fechado' %}
                        <span class="pedido-status-badge pedido-status-fechado">Venda concluida</span>
                    {% elif pedido.status == 'cancelado' %}
                        <span class="pedido-status-badge pedido-status-cancelado">Cancelado</span>
                    {% else %}
                        {{ pedido.status }}
                    {% endif %}
                </td>
                <td data-label="Acoes" class="actions-cell pedido-actions-cell">
                    <div class="pedido-actions">
                        <form method="POST" action="{{ url_for('alterar_status_pedido', pedido_id=pedido.id) }}" class="pedido-status-form">
                            {{ csrf_input|safe }}
                            {% set permitidos = status_transitions.get(pedido.status, []) %}
                            <select name="status" class="form-select form-select-sm">
                                <option value="aberto" {% if pedido.status=='aberto' %}selected{% endif %} {% if pedido.status!='aberto' and 'aberto' not in permitidos %}disabled{% endif %}>Aberto</option>
                                <option value="em_preparo" {% if pedido.status=='em_preparo' %}selected{% endif %} {% if pedido.status!='em_preparo' and 'em_preparo' not in permitidos %}disabled{% endif %}>Em preparo</option>
                                <option value="entregue" {% if pedido.status=='entregue' %}selected{% endif %} {% if pedido.status!='entregue' and 'entregue' not in permitidos %}disabled{% endif %}>Entregue</option>
                                <option value="fechado" {% if pedido.status=='fechado' %}selected{% endif %} {% if pedido.status!='fechado' and 'fechado' not in permitidos %}disabled{% endif %}>Venda concluida</option>
                                <option value="cancelado" {% if pedido.status=='cancelado' %}selected{% endif %} {% if pedido.status!='cancelado' and 'cancelado' not in permitidos %}disabled{% endif %}>Cancelado</option>
                            </select>
                            <button type="submit" class="btn btn-sm btn-primary">Atualizar</button>
                        </form>
                        <a href="{{ url_for('editar_pedido', pedido_id=pedido.id) }}" class="btn btn-sm btn-warning">Editar</a>
                        <a href="{{ url_for('detalhes_pedido', pedido_id=pedido.id) }}" class="btn btn-sm btn-outline-secondary">Detalhes</a>
                        <a href="{{ url_for('visualizar_comprovante_pedido', pedido_id=pedido.id) }}" class="btn btn-sm btn-info" target="_blank">Comprovante</a>
                        <form method="POST" action="{{ url_for('deletar_pedido', pedido_id=pedido.id) }}" data-confirm-message="Excluir pedido #{{ pedido.id }}?">
                            {{ csrf_input|safe }}
                            <button type="submit" class="btn btn-sm btn-danger">Excluir</button>
                        </form>
                    </div>
                </td>
            </tr>
            {% else %}
            <tr>
                <td colspan="11" class="text-center">Nenhum pedido cadastrado</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>

{% if pagination and pagination.pages > 1 %}
<div class="pagination">
    {% set params = query_params.copy() if query_params else {} %}
    {% if pagination.has_prev %}
        {% set params_prev = params.copy() %}
        {% set _ = params_prev.update({'page': pagination.prev_num, 'per_page': per_page}) %}
        <a class="btn btn-outline-secondary" href="{{ url_for('listar_pedidos', **params_prev) }}">Anterior</a>
    {% else %}
        <span class="btn btn-outline-secondary disabled">Anterior</span>
    {% endif %}

    <span class="pagination-info">Pagina {{ pagination.page }} de {{ pagination.pages }}</span>

    {% if pagination.has_next %}
        {% set params_next = params.copy() %}
        {% set _ = params_next.update({'page': pagination.next_num, 'per_page': per_page}) %}
        <a class="btn btn-outline-secondary" href="{{ url_for('listar_pedidos', **params_next) }}">Proxima</a>
    {% else %}
        <span class="btn btn-outline-secondary disabled">Proxima</span>
    {% endif %}
</div>
{% endif %}
{% endblock %}

{% block extra_js %}
<script>
document.addEventListener('DOMContentLoaded', function () {
    const statusEl = document.getElementById('sse-status');
    const listEl = document.getElementById('alert-list');
    if (!window.EventSource) {
        statusEl.textContent = 'Seu navegador nao suporta atualizacoes em tempo real. Recarregue para ver novos pedidos.';
        return;
    }
    const es = new EventSource('{{ url_for('sse_pedidos') }}');
    es.addEventListener('open', () => statusEl.textContent = 'Conectado. Aguardando novos pedidos...');
    es.addEventListener('pedido', (event) => {
        const data = JSON.parse(event.data || '{}');
        statusEl.textContent = 'Novo pedido recebido!';
        const li = document.createElement('li');
        li.className = 'alert alert-info';
        li.innerHTML = `<strong>Mesa ${data.mesa || '?'}:</strong> Pedido #${data.pedido_id} as ${new Date(data.criado_em).toLocaleTimeString('pt-BR')}<br>` +
            (data.itens ? data.itens.map(i => `${i.quantidade}x ${i.produto}`).join(', ') : '');
        listEl.prepend(li);
    });
    es.addEventListener('error', () => statusEl.textContent = 'Conexao com alertas foi perdida. Tentando reconectar...');
});
</script>
{% endblock %}

```

---

### Arquivo: `tests\test_endereco_codigo.py`

```py
import unittest

from utils.endereco_codigo import (
    configurar_endereco,
    gerar_codigo_localizacao_supermercado,
    montar_endereco,
    parse_endereco,
    validar_endereco_supermercado_payload,
    validar_endereco,
)


class EnderecoCodigoTestCase(unittest.TestCase):
    def setUp(self):
        configurar_endereco(zonas_permitidas={'ZP', 'ZR', 'ZQ', 'ZD'}, permitir_nivel_zero=True)

    def test_montar_endereco_valido(self):
        codigo = montar_endereco(cd=1, zona='P', rua=5, rack=3, nivel=2, vao=12, lado='A')
        self.assertEqual(codigo, 'CD01-ZP-R05-RK03-N02-V12-LA')

    def test_montar_endereco_lado_direita_e_zona_com_prefixo(self):
        codigo = montar_endereco(cd=12, zona='ZR', rua=9, rack=1, nivel=0, vao=7, lado='DIR')
        self.assertEqual(codigo, 'CD12-ZR-R09-RK01-N00-V07-LB')

    def test_parse_endereco_normaliza_minusculo_espaco_e_underscore(self):
        partes = parse_endereco('cd01_zp r05_rk03_n02_v12_la')
        esperado = {
            'cd': 1,
            'zona': 'ZP',
            'rua': 5,
            'rack': 3,
            'nivel': 2,
            'vao': 12,
            'lado': 'LA',
        }
        self.assertEqual(partes, esperado)

    def test_validar_endereco_invalido_por_campo(self):
        resp = validar_endereco('CD00-ZP-R00-RK03-N02-V12-LA')
        self.assertFalse(resp['valido'])
        self.assertTrue(resp['erros'])
        self.assertEqual(resp['partes'], {})

    def test_validar_endereco_invalido_zona_nao_permitida(self):
        resp = validar_endereco('CD01-ZX-R05-RK03-N02-V12-LA')
        self.assertFalse(resp['valido'])
        self.assertIn('nao permitida', resp['erros'][0])

    def test_montar_endereco_rejeita_zona_nao_alfanumerica(self):
        with self.assertRaises(ValueError):
            montar_endereco(cd=1, zona='P@', rua=5, rack=3, nivel=2, vao=12, lado='A')

    def test_montar_endereco_rejeita_lado_nao_alfanumerico(self):
        with self.assertRaises(ValueError):
            montar_endereco(cd=1, zona='P', rua=5, rack=3, nivel=2, vao=12, lado='A-1')

    def test_configuracao_nivel_zero_desabilitado(self):
        configurar_endereco(permitir_nivel_zero=False)
        resp = validar_endereco('CD01-ZP-R05-RK03-N00-V12-LA')
        self.assertFalse(resp['valido'])
        self.assertIn('nivel', resp['erros'][0].lower())

    def test_configuracao_zonas_personalizadas(self):
        configurar_endereco(zonas_permitidas={'ZA1', 'ZB2'})
        codigo = montar_endereco(cd=2, zona='A1', rua=1, rack=1, nivel=1, vao=1, lado='ESQ')
        self.assertEqual(codigo, 'CD02-ZA1-R01-RK01-N01-V01-LA')

        invalido = validar_endereco('CD02-ZP-R01-RK01-N01-V01-LA')
        self.assertFalse(invalido['valido'])


class EnderecoSupermercadoCodigoTestCase(unittest.TestCase):
    def test_gerar_codigo_rack(self):
        codigo = gerar_codigo_localizacao_supermercado(
            loja_cd='lj01',
            setor_zona='bebidas',
            tipo_estrutura='rack',
            rua_corredor='3',
            rack_estante='2',
            nivel_prateleira='1',
            posicao_slot='8',
            lado='a',
        )
        self.assertEqual(codigo, 'LJ01-BEB-R03-RK02-N01-V08-LA')

    def test_gerar_codigo_area_aberta(self):
        codigo = gerar_codigo_localizacao_supermercado(
            loja_cd='LJ01',
            setor_zona='frente_loja',
            tipo_estrutura='area_aberta',
            ponto_local='Gondola 12 - Prateleira 3',
        )
        self.assertEqual(codigo, 'LJ01-FL-G12-P03')

    def test_validacao_condicional_rack(self):
        payload = {
            'loja_cd': 'LJ01',
            'setor_zona': 'bebidas',
            'tipo_area': 'picking',
            'status': 'ativo',
            'tipo_estrutura': 'rack',
            'rua_corredor': '3',
            'rack_estante': '2',
            'nivel_prateleira': '1',
            'posicao_slot': '8',
            'lado': 'B',
            'controle_validade': 'fifo',
        }
        dados = validar_endereco_supermercado_payload(payload)
        self.assertEqual(dados['codigo_localizacao'], 'LJ01-BEB-R03-RK02-N01-V08-LB')
        self.assertIsNone(dados['ponto_local'])

    def test_validacao_condicional_area_aberta(self):
        payload = {
            'loja_cd': 'LJ01',
            'setor_zona': 'frente_loja',
            'tipo_area': 'frente_loja',
            'status': 'ativo',
            'tipo_estrutura': 'area_aberta',
            'ponto_local': 'Camara fria 1',
            'controle_validade': 'nenhum',
        }
        dados = validar_endereco_supermercado_payload(payload)
        self.assertTrue(dados['codigo_localizacao'].startswith('LJ01-FL-'))
        self.assertIsNone(dados['rua_corredor'])

    def test_validacao_rack_sem_campos_obrigatorios(self):
        payload = {
            'loja_cd': 'LJ01',
            'setor_zona': 'bebidas',
            'tipo_area': 'picking',
            'status': 'ativo',
            'tipo_estrutura': 'rack',
            'controle_validade': 'fifo',
        }
        with self.assertRaises(ValueError):
            validar_endereco_supermercado_payload(payload)


if __name__ == '__main__':
    unittest.main()
```

---

### Arquivo: `tests\test_endereco_localizacao.py`

```py
from models import EnderecoEstoque


def test_build_codigo_localizacao_zero_padding():
    endereco = EnderecoEstoque(
        rua_corredor='A',
        coluna_baia='1',
        nivel_prateleira='2',
        posicao_slot='3'
    )
    assert endereco.build_codigo_localizacao() == 'A-01-02-03'


def test_build_codigo_localizacao_keeps_letters():
    endereco = EnderecoEstoque(
        rua_corredor='RZ',
        coluna_baia='A1',
        nivel_prateleira='B2',
        posicao_slot='C3'
    )
    assert endereco.build_codigo_localizacao() == 'RZ-A1-B2-C3'
```

---

### Arquivo: `tests\test_system_flows.py`

```py
import os
import unittest

os.environ['FLASK_CONFIG'] = 'testing'

from app import app, db, sincronizar_garcom_funcionario  # noqa: E402
from models import AuditoriaEvento, Caixa, Categoria, EmpresaConfig, EnderecoEstoque, Estoque, Fornecedor, Funcionario, Garcom, Mesa, Movimentacao, Pedido, PermissaoAcesso, Produto, RecebimentoFornecedor  # noqa: E402


class SystemFlowsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.drop_all()
        db.create_all()

        self.funcionario = Funcionario(nome='Admin', email='admin@test.local', role='admin', ativo=True)
        self.funcionario.set_password('123456')
        db.session.add(self.funcionario)

        self.categoria = Categoria(nome='Bebidas', descricao='Categoria de teste')
        db.session.add(self.categoria)
        db.session.flush()

        self.produto = Produto(
            codigo='P001',
            nome='Refrigerante',
            categoria_id=self.categoria.id,
            preco_custo=4.0,
            preco_venda=10.0,
            quantidade_estoque=10,
            quantidade_minima=2,
            ativo=True,
        )
        db.session.add(self.produto)

        self.caixa = Caixa(
            nome='Caixa 1',
            saldo_inicial=100.0,
            saldo_atual=100.0,
            aberto=True,
            funcionario_id=None,
        )
        db.session.add(self.caixa)
        db.session.commit()

        self.csrf_token = 'test-csrf-token'
        with self.client.session_transaction() as sess:
            sess['funcionario_id'] = self.funcionario.id
            sess['funcionario_nome'] = self.funcionario.nome
            sess['funcionario_role'] = self.funcionario.role
            sess['_csrf_token'] = self.csrf_token

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_api_requires_authentication(self):
        with self.client.session_transaction() as sess:
            sess.clear()

        response = self.client.get('/api/dashboard/analytics')
        self.assertEqual(response.status_code, 401)
        payload = response.get_json()
        self.assertFalse(payload['success'])

    def test_csrf_required_for_api_write(self):
        response = self.client.post('/api/pedidos/criar', json={
            'caixa_id': self.caixa.id,
            'itens': [{'produto_id': self.produto.id, 'quantidade': 1}],
        })
        self.assertEqual(response.status_code, 400)
        payload = response.get_json()
        self.assertFalse(payload['success'])
        self.assertEqual(payload.get('code'), 'csrf_invalid')

    def test_order_close_is_immutable_and_updates_stock_and_cash_once(self):
        headers = {'X-CSRF-Token': self.csrf_token}

        create_response = self.client.post('/api/pedidos/criar', json={
            'caixa_id': self.caixa.id,
            'itens': [{'produto_id': self.produto.id, 'quantidade': 2}],
        }, headers=headers)
        self.assertEqual(create_response.status_code, 200)
        create_payload = create_response.get_json()
        self.assertTrue(create_payload['success'])
        pedido_id = create_payload['data']['pedido_id']

        pedido = Pedido.query.get(pedido_id)
        self.assertEqual(float(pedido.total), 20.0)
        self.assertFalse(pedido.estoque_processado)
        self.assertFalse(pedido.financeiro_processado)

        finalize_response = self.client.post(f'/api/pedidos/{pedido_id}/finalizar', json={
            'metodo_pagamento': 'dinheiro',
            'valor_pago': 20.0,
        }, headers=headers)
        self.assertEqual(finalize_response.status_code, 200)
        finalize_payload = finalize_response.get_json()
        self.assertTrue(finalize_payload['success'])

        db.session.refresh(self.produto)
        db.session.refresh(self.caixa)
        db.session.refresh(pedido)

        self.assertEqual(self.produto.quantidade_estoque, 8)
        self.assertEqual(float(self.caixa.saldo_atual), 120.0)
        self.assertEqual(pedido.status, 'fechado')
        self.assertTrue(pedido.estoque_processado)
        self.assertTrue(pedido.financeiro_processado)

        finalize_again_response = self.client.post(f'/api/pedidos/{pedido_id}/finalizar', json={
            'metodo_pagamento': 'dinheiro',
            'valor_pago': 20.0,
        }, headers=headers)
        self.assertEqual(finalize_again_response.status_code, 409)

        reopen_response = self.client.post(f'/pedidos/{pedido_id}/status', data={
            'status': 'aberto',
            'csrf_token': self.csrf_token,
        })
        self.assertEqual(reopen_response.status_code, 302)
        db.session.refresh(pedido)
        self.assertEqual(pedido.status, 'fechado')

    def test_access_control_blocks_order_api_when_page_not_permitted(self):
        gerente = Funcionario(
            nome='Gerente Restrito',
            email='gerente@test.local',
            role='gerente',
            ativo=True,
            controle_acesso_ativo=True,
        )
        gerente.set_password('123456')
        db.session.add(gerente)
        db.session.flush()
        db.session.add(PermissaoAcesso(funcionario_id=gerente.id, pagina='inicio'))
        db.session.commit()

        with self.client.session_transaction() as sess:
            sess['funcionario_id'] = gerente.id
            sess['funcionario_nome'] = gerente.nome
            sess['funcionario_role'] = gerente.role
            sess['_csrf_token'] = self.csrf_token

        response = self.client.post('/api/pedidos/criar', json={
            'caixa_id': self.caixa.id,
            'itens': [{'produto_id': self.produto.id, 'quantidade': 1}],
        }, headers={'X-CSRF-Token': self.csrf_token})

        self.assertEqual(response.status_code, 403)
        payload = response.get_json()
        self.assertFalse(payload['success'])
        self.assertEqual(payload.get('code'), 'forbidden')

    def test_waiter_profile_is_disabled_when_role_changes(self):
        funcionario = Funcionario(
            nome='Garcom Teste',
            email='garcom@test.local',
            role='garcom',
            cargo='Garcom',
            ativo=True,
        )
        funcionario.set_password('123456')
        db.session.add(funcionario)
        db.session.flush()

        sincronizar_garcom_funcionario(funcionario)
        db.session.commit()

        garcom = Garcom.query.filter_by(funcionario_id=funcionario.id).first()
        self.assertIsNotNone(garcom)
        self.assertTrue(garcom.ativo)

        funcionario.role = 'caixa'
        funcionario.cargo = 'Caixa'
        sincronizar_garcom_funcionario(funcionario)
        db.session.commit()

        db.session.refresh(garcom)
        self.assertFalse(garcom.ativo)

    def test_order_api_ignores_table_when_waiter_table_module_is_disabled(self):
        empresa = EmpresaConfig(atendimento_mesas_ativo=False)
        mesa = Mesa(numero='99', capacidade=4, status='livre', qr_token='mesa-99')
        db.session.add(empresa)
        db.session.add(mesa)
        db.session.commit()

        headers = {'X-CSRF-Token': self.csrf_token}
        response = self.client.post('/api/pedidos/criar', json={
            'caixa_id': self.caixa.id,
            'mesa_id': mesa.id,
            'itens': [{'produto_id': self.produto.id, 'quantidade': 1}],
        }, headers=headers)
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertTrue(payload['success'])

        pedido_id = payload['data']['pedido_id']
        pedido = Pedido.query.get(pedido_id)
        self.assertIsNone(pedido.mesa_id)
        self.assertIsNone(pedido.garcom_id)

    def test_public_qr_routes_return_404_when_waiter_table_module_is_disabled(self):
        empresa = EmpresaConfig(atendimento_mesas_ativo=False)
        mesa = Mesa(numero='10', capacidade=4, status='livre', qr_token='mesa-publica-10')
        db.session.add(empresa)
        db.session.add(mesa)
        db.session.commit()

        response = self.client.get(f'/m/{mesa.qr_token}')
        self.assertEqual(response.status_code, 404)

    def test_stock_address_creation_requires_and_accepts_csrf(self):
        estoque = Estoque(nome='CD Principal', ativo=True)
        db.session.add(estoque)
        db.session.commit()

        without_csrf = self.client.post('/enderecos-estoque/novo', data={
            'estoque_id': estoque.id,
            'nome': 'Deposito Central',
            'loja_cd': 'LJ01',
            'setor_zona': 'deposito',
            'tipo_area': 'picking',
            'status': 'ativo',
            'tipo_estrutura': 'area_aberta',
            'ponto_local': 'Deposito Central',
            'controle_validade': 'nenhum',
            'cidade': 'Cuiaba',
            'estado': 'MT',
            'ativo': 'on',
        })
        self.assertEqual(without_csrf.status_code, 400)

        with_csrf = self.client.post('/enderecos-estoque/novo', data={
            'estoque_id': estoque.id,
            'nome': 'Deposito Central',
            'loja_cd': 'LJ01',
            'setor_zona': 'deposito',
            'tipo_area': 'picking',
            'status': 'ativo',
            'tipo_estrutura': 'area_aberta',
            'ponto_local': 'Deposito Central',
            'controle_validade': 'nenhum',
            'cidade': 'Cuiaba',
            'estado': 'MT',
            'ativo': 'on',
            'csrf_token': self.csrf_token,
        })
        self.assertEqual(with_csrf.status_code, 302)

        endereco = EnderecoEstoque.query.filter_by(nome='Deposito Central').first()
        self.assertIsNotNone(endereco)
        self.assertEqual(endereco.estoque_id, estoque.id)
        self.assertEqual(endereco.estado, 'MT')
        self.assertTrue(endereco.ativo)

    def test_stock_analytics_api_returns_success(self):
        response = self.client.get('/api/estoque/analytics?periodo=30')
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertTrue(payload['success'])
        self.assertEqual(payload['data']['periodo_dias'], 30)

    def test_multiple_stocks_can_be_created_and_linked_to_addresses(self):
        create_a = self.client.post('/estoques/novo', data={
            'nome': 'CD Norte',
            'descricao': 'Centro de distribuicao norte',
            'ativo': 'on',
            'csrf_token': self.csrf_token,
        })
        create_b = self.client.post('/estoques/novo', data={
            'nome': 'CD Sul',
            'descricao': 'Centro de distribuicao sul',
            'ativo': 'on',
            'csrf_token': self.csrf_token,
        })
        self.assertEqual(create_a.status_code, 302)
        self.assertEqual(create_b.status_code, 302)

        estoque_a = Estoque.query.filter_by(nome='CD Norte').first()
        estoque_b = Estoque.query.filter_by(nome='CD Sul').first()
        self.assertIsNotNone(estoque_a)
        self.assertIsNotNone(estoque_b)

        addr_a = self.client.post('/enderecos-estoque/novo', data={
            'estoque_id': estoque_a.id,
            'nome': 'Rua A',
            'loja_cd': 'LJ01',
            'setor_zona': 'deposito',
            'tipo_area': 'picking',
            'status': 'ativo',
            'tipo_estrutura': 'area_aberta',
            'ponto_local': 'Rua A',
            'controle_validade': 'nenhum',
            'cidade': 'Cuiaba',
            'estado': 'MT',
            'ativo': 'on',
            'csrf_token': self.csrf_token,
        })
        addr_b = self.client.post('/enderecos-estoque/novo', data={
            'estoque_id': estoque_b.id,
            'nome': 'Rua B',
            'loja_cd': 'LJ01',
            'setor_zona': 'deposito',
            'tipo_area': 'picking',
            'status': 'ativo',
            'tipo_estrutura': 'area_aberta',
            'ponto_local': 'Rua B',
            'controle_validade': 'nenhum',
            'cidade': 'Cuiaba',
            'estado': 'MT',
            'ativo': 'on',
            'csrf_token': self.csrf_token,
        })
        self.assertEqual(addr_a.status_code, 302)
        self.assertEqual(addr_b.status_code, 302)

        end_a = EnderecoEstoque.query.filter_by(nome='Rua A').first()
        end_b = EnderecoEstoque.query.filter_by(nome='Rua B').first()
        self.assertEqual(end_a.estoque_id, estoque_a.id)
        self.assertEqual(end_b.estoque_id, estoque_b.id)

    def test_bulk_store_products_distributes_items_across_stock_addresses(self):
        produto_2 = Produto(
            codigo='P002',
            nome='Agua',
            categoria_id=self.categoria.id,
            preco_custo=2.0,
            preco_venda=5.0,
            quantidade_estoque=20,
            quantidade_minima=3,
            ativo=True,
        )
        db.session.add(produto_2)

        estoque = Estoque(nome='CD Bulk', ativo=True)
        db.session.add(estoque)
        db.session.flush()

        endereco_a = EnderecoEstoque(nome='CD Bulk A', estoque_id=estoque.id, cidade='Cuiaba', estado='MT', ativo=True)
        endereco_b = EnderecoEstoque(nome='CD Bulk B', estoque_id=estoque.id, cidade='Cuiaba', estado='MT', ativo=True)
        db.session.add(endereco_a)
        db.session.add(endereco_b)
        db.session.commit()

        response = self.client.post('/produtos/enderecos/armazenar-todos', data={
            'estoque_id': estoque.id,
            'csrf_token': self.csrf_token,
        })
        self.assertEqual(response.status_code, 302)

        db.session.refresh(self.produto)
        db.session.refresh(produto_2)
        self.assertIn(self.produto.endereco_id, {endereco_a.id, endereco_b.id})
        self.assertIn(produto_2.endereco_id, {endereco_a.id, endereco_b.id})
        self.assertNotEqual(self.produto.endereco_id, produto_2.endereco_id)

    def test_audit_log_area_registers_mutation_events(self):
        response = self.client.post('/estoques/novo', data={
            'nome': 'CD Auditoria',
            'descricao': 'Teste de log',
            'ativo': 'on',
            'csrf_token': self.csrf_token,
        })
        self.assertEqual(response.status_code, 302)

        eventos = AuditoriaEvento.query.filter(
            AuditoriaEvento.rota == '/estoques/novo',
            AuditoriaEvento.metodo == 'POST'
        ).all()
        self.assertTrue(len(eventos) >= 1)

        audit_page = self.client.get('/auditoria')
        self.assertEqual(audit_page.status_code, 200)

    def test_new_movement_requires_supplier_when_receiving_from_supplier(self):
        fornecedor = Fornecedor(nome='Fornecedor X', ativo=True)
        db.session.add(fornecedor)
        db.session.commit()

        sem_fornecedor = self.client.post('/movimentacoes/nova', data={
            'produto_id': self.produto.id,
            'tipo': 'entrada',
            'quantidade': 2,
            'recebimento_fornecedor': 'on',
            'csrf_token': self.csrf_token,
        })
        self.assertEqual(sem_fornecedor.status_code, 302)
        self.assertEqual(Movimentacao.query.count(), 0)

        com_fornecedor = self.client.post('/movimentacoes/nova', data={
            'produto_id': self.produto.id,
            'tipo': 'entrada',
            'quantidade': 2,
            'recebimento_fornecedor': 'on',
            'fornecedor_id': fornecedor.id,
            'csrf_token': self.csrf_token,
        })
        self.assertEqual(com_fornecedor.status_code, 302)
        self.assertEqual(Movimentacao.query.count(), 1)

        mov = Movimentacao.query.first()
        self.assertEqual(mov.fornecedor_id, fornecedor.id)
        self.assertEqual(mov.motivo, 'recebimento_fornecedor')

    def test_recebimento_put_away_updates_stock_only_on_armazenagem(self):
        fornecedor = Fornecedor(nome='Fornecedor PutAway', ativo=True)
        estoque = Estoque(nome='CD Recebimento', ativo=True)
        db.session.add(fornecedor)
        db.session.add(estoque)
        db.session.flush()

        endereco = EnderecoEstoque(
            estoque_id=estoque.id,
            nome='Endereco Recebimento A',
            loja_cd='LJ01',
            setor_zona='deposito',
            tipo_area='recebimento',
            status='ativo',
            tipo_estrutura='rack',
            codigo_armazem='LJ01',
            rua_corredor='03',
            coluna_baia='02',
            nivel_prateleira='01',
            posicao_slot='08',
            lado='LA',
            controle_validade='fifo',
            codigo_localizacao='LJ01-DEP-R03-RK02-N01-V08-LA',
            ativo=True,
        )
        db.session.add(endereco)
        db.session.commit()

        estoque_inicial = self.produto.quantidade_estoque
        create_response = self.client.post('/estoque/recebimentos/novo', data={
            'fornecedor_id': fornecedor.id,
            'info_nota': 'NF 123',
            'produto_id[]': [self.produto.id],
            'qtd_recebida[]': ['5'],
            'csrf_token': self.csrf_token,
        })
        self.assertEqual(create_response.status_code, 302)

        recebimento = RecebimentoFornecedor.query.order_by(RecebimentoFornecedor.id.desc()).first()
        self.assertIsNotNone(recebimento)
        self.assertEqual(recebimento.status, RecebimentoFornecedor.STATUS_CRIADO)

        db.session.refresh(self.produto)
        self.assertEqual(self.produto.quantidade_estoque, estoque_inicial)

        item = recebimento.itens[0]
        conferir_response = self.client.post(f'/estoque/recebimentos/{recebimento.id}/conferir', data={
            f'item_{item.id}_qtd_recebida': '5',
            f'item_{item.id}_qtd_avaria': '1',
            f'item_{item.id}_lote': 'L001',
            f'item_{item.id}_validade': '2027-12-31',
            'csrf_token': self.csrf_token,
        })
        self.assertEqual(conferir_response.status_code, 302)

        db.session.refresh(recebimento)
        db.session.refresh(self.produto)
        self.assertEqual(recebimento.status, RecebimentoFornecedor.STATUS_AGUARDANDO_ARMAZENAGEM)
        self.assertEqual(self.produto.quantidade_estoque, estoque_inicial)

        armazenar_response = self.client.post(f'/estoque/recebimentos/{recebimento.id}/armazenar', data={
            f'endereco_destino_{item.id}': endereco.id,
            'csrf_token': self.csrf_token,
        })
        self.assertEqual(armazenar_response.status_code, 302)

        db.session.refresh(recebimento)
        db.session.refresh(self.produto)
        self.assertEqual(recebimento.status, RecebimentoFornecedor.STATUS_CONCLUIDO)
        self.assertEqual(self.produto.quantidade_estoque, estoque_inicial + 4)

        mov = Movimentacao.query.filter_by(motivo='recebimento_fornecedor').first()
        self.assertIsNotNone(mov)
        self.assertEqual(mov.fornecedor_id, fornecedor.id)
        self.assertEqual(mov.endereco_destino_id, endereco.id)
        self.assertEqual(mov.quantidade, 4)

    def test_recebimento_multiplos_fornecedores_e_armazenagem_em_enderecos(self):
        produto_2 = Produto(
            codigo='P200',
            nome='Arroz 5Kg',
            categoria_id=self.categoria.id,
            preco_custo=20.0,
            preco_venda=29.9,
            quantidade_estoque=30,
            quantidade_minima=5,
            ativo=True,
        )
        produto_3 = Produto(
            codigo='P300',
            nome='Cafe 500g',
            categoria_id=self.categoria.id,
            preco_custo=9.0,
            preco_venda=14.9,
            quantidade_estoque=15,
            quantidade_minima=4,
            ativo=True,
        )
        db.session.add(produto_2)
        db.session.add(produto_3)

        estoque = Estoque(nome='CD Multi Forn', ativo=True)
        db.session.add(estoque)
        db.session.flush()

        endereco_a = EnderecoEstoque(
            estoque_id=estoque.id,
            nome='Rack A',
            loja_cd='LJ01',
            setor_zona='deposito',
            tipo_area='recebimento',
            status='ativo',
            tipo_estrutura='rack',
            codigo_armazem='LJ01',
            rua_corredor='01',
            coluna_baia='01',
            nivel_prateleira='01',
            posicao_slot='01',
            lado='LA',
            controle_validade='fifo',
            codigo_localizacao='LJ01-DEP-R01-RK01-N01-V01-LA',
            ativo=True,
        )
        endereco_b = EnderecoEstoque(
            estoque_id=estoque.id,
            nome='Rack B',
            loja_cd='LJ01',
            setor_zona='deposito',
            tipo_area='recebimento',
            status='ativo',
            tipo_estrutura='rack',
            codigo_armazem='LJ01',
            rua_corredor='01',
            coluna_baia='02',
            nivel_prateleira='01',
            posicao_slot='02',
            lado='LB',
            controle_validade='fifo',
            codigo_localizacao='LJ01-DEP-R01-RK02-N01-V02-LB',
            ativo=True,
        )
        db.session.add(endereco_a)
        db.session.add(endereco_b)

        fornecedores = [
            Fornecedor(nome='Fornecedor Alfa', ativo=True),
            Fornecedor(nome='Fornecedor Beta', ativo=True),
            Fornecedor(nome='Fornecedor Gama', ativo=True),
        ]
        for fornecedor in fornecedores:
            db.session.add(fornecedor)
        db.session.commit()

        produtos = [self.produto, produto_2, produto_3]
        estoque_inicial = {p.id: p.quantidade_estoque for p in produtos}
        totais_liquidos = {p.id: 0 for p in produtos}

        for idx, fornecedor in enumerate(fornecedores):
            produto = produtos[idx]
            qtd_recebida = 8 + idx
            qtd_avaria = 1
            destino = endereco_a if idx % 2 == 0 else endereco_b

            criar = self.client.post('/estoque/recebimentos/novo', data={
                'fornecedor_id': fornecedor.id,
                'info_nota': f'NF-MULTI-{idx + 1}',
                'produto_id[]': [produto.id],
                'qtd_recebida[]': [str(qtd_recebida)],
                'csrf_token': self.csrf_token,
            })
            self.assertEqual(criar.status_code, 302)

            recebimento = RecebimentoFornecedor.query.filter_by(info_nota=f'NF-MULTI-{idx + 1}').first()
            self.assertIsNotNone(recebimento)
            item = recebimento.itens[0]

            conferir = self.client.post(f'/estoque/recebimentos/{recebimento.id}/conferir', data={
                f'item_{item.id}_qtd_recebida': str(qtd_recebida),
                f'item_{item.id}_qtd_avaria': str(qtd_avaria),
                f'item_{item.id}_lote': f'LOTE-{idx + 1}',
                f'item_{item.id}_validade': '2028-01-30',
                'csrf_token': self.csrf_token,
            })
            self.assertEqual(conferir.status_code, 302)

            armazenar = self.client.post(f'/estoque/recebimentos/{recebimento.id}/armazenar', data={
                f'endereco_destino_{item.id}': destino.id,
                'csrf_token': self.csrf_token,
            })
            self.assertEqual(armazenar.status_code, 302)

            db.session.refresh(recebimento)
            self.assertEqual(recebimento.status, RecebimentoFornecedor.STATUS_CONCLUIDO)
            totais_liquidos[produto.id] += (qtd_recebida - qtd_avaria)

        for produto in produtos:
            db.session.refresh(produto)
            self.assertEqual(produto.quantidade_estoque, estoque_inicial[produto.id] + totais_liquidos[produto.id])
            self.assertIn(produto.endereco_id, {endereco_a.id, endereco_b.id})

        movimentos_recebimento = Movimentacao.query.filter_by(motivo='recebimento_fornecedor').all()
        self.assertEqual(len(movimentos_recebimento), 3)


if __name__ == '__main__':
    unittest.main()
```

---

### Arquivo: `utils\__init__.py`

```py
# Utilitarios compartilhados do projeto.
```

---

### Arquivo: `utils\endereco_codigo.py`

```py
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
