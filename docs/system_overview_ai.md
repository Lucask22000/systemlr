# Documentacao Tecnica do Sistema (Leitura Humana e IA)

- Gerado em: `2026-03-15 16:57:55`
- Projeto: `C:/Users/lucas/OneDrive/Desktop/conveniencia`
- Objetivo: apresentar arquitetura, tecnologias e codigo-chave para interpretacao rapida.

## 1) Tecnologias e Dependencias
| Tecnologia | Uso no sistema |
| --- | --- |
| `Flask` | Web framework (routing, request handling, templates). |
| `Flask-SQLAlchemy` | ORM integration with SQLAlchemy. |
| `Flask-Migrate` | Database schema migrations (Alembic integration). |
| `Flask-WTF` | Forms and CSRF protection. |
| `Flask-Limiter` | Rate limiting for endpoints. |
| `Flask-Caching` | Caching layer for computed data/queries. |
| `redis` | Cache backend/message broker support. |
| `python-dotenv` | Environment variable loading from .env. |
| `qrcode` | QR code generation. |
| `pillow` | Image processing. |
| `pytest` | Automated tests. |
| `openpyxl` | Excel export generation. |
| `docker-compose` | Container orchestration for local/dev execution. |
| `SQLite` | Primary local database file detected (instance/estoque.db). |

## 2) Arquivos Estruturais Principais
- `app/__init__.py`
- `app/constants.py`
- `app/services/analytics.py`
- `models.py`
- `config.py`
- `security.py`
- `realtime.py`
- `routes/estoque_routes.py`
- `routes/vendas_routes.py`
- `routes/public_routes.py`
- `templates/base.html`

## 3) Rotas HTTP Principais
| Metodos | Rota | Funcao | Arquivo |
| --- | --- | --- | --- |
| `POST` | `/operacao/contexto-filial` | `atualizar_contexto_filial` | `app/__init__.py:1212` |
| `GET` | `/` | `index` | `app/__init__.py:1241` |
| `GET, POST` | `/dashboard` | `dashboard` | `app/__init__.py:1324` |
| `GET` | `/gestao-negocio` | `gestao_negocio` | `app/__init__.py:1467` |
| `GET` | `/financeiro` | `financeiro` | `app/__init__.py:1591` |
| `GET, POST` | `/financeiro/fundos` | `financeiro_fundos` | `app/__init__.py:1637` |
| `GET, POST` | `/financeiro/lancamentos` | `financeiro_lancamentos` | `app/__init__.py:1778` |
| `POST` | `/financeiro/lancamentos/<int:lancamento_id>/marcar-enviado` | `marcar_lancamento_enviado_contador` | `app/__init__.py:1900` |
| `GET` | `/financeiro/lancamentos/exportar` | `exportar_lancamentos_financeiros` | `app/__init__.py:1915` |
| `GET` | `/financeiro/lancamentos/exportar-xlsx` | `exportar_lancamentos_financeiros_xlsx` | `app/__init__.py:1984` |
| `GET, POST` | `/empresa` | `editar_empresa` | `app/__init__.py:2061` |
| `GET, POST` | `/ecommerce-config` | `configurar_ecommerce` | `app/__init__.py:2290` |
| `GET, POST` | `/ecommerce-ativacao` | `configurar_ativacao_ecommerce` | `app/__init__.py:2573` |
| `GET` | `/empresa/config-cardapio/preview` | `preview_cardapio_empresa` | `app/__init__.py:2595` |
| `GET` | `/boas-vindas` | `boas_vindas` | `app/__init__.py:2880` |
| `GET` | `/ajuda` | `central_ajuda` | `app/__init__.py:3916` |
| `GET` | `/ajuda/<string:topico_slug>` | `detalhe_ajuda` | `app/__init__.py:3960` |
| `GET` | `/funcionarios` | `listar_funcionarios` | `app/__init__.py:3986` |
| `GET, POST` | `/funcionarios/novo` | `criar_funcionario` | `app/__init__.py:4066` |
| `GET, POST` | `/funcionarios/<int:funcionario_id>/editar` | `editar_funcionario` | `app/__init__.py:4209` |
| `POST` | `/funcionarios/<int:funcionario_id>/deletar` | `deletar_funcionario` | `app/__init__.py:4382` |
| `GET, POST` | `/funcionarios/<int:funcionario_id>/acessos` | `editar_acessos_funcionario` | `app/__init__.py:4405` |
| `GET` | `/rh/funcoes` | `listar_funcoes_rh` | `app/__init__.py:4482` |
| `GET` | `/rh/perfis` | `listar_perfis_rh` | `app/__init__.py:4508` |
| `GET` | `/rh/indicadores` | `indicadores_rh` | `app/__init__.py:4540` |
| `GET` | `/rh/organograma` | `organograma_rh` | `app/__init__.py:4719` |
| `GET` | `/api/rh/analytics` | `analytics_rh_api` | `app/__init__.py:4892` |
| `GET` | `/auditoria` | `auditoria_sistema` | `app/__init__.py:4964` |
| `POST` | `/rh/funcoes/nova` | `nova_funcao_rh` | `app/__init__.py:5002` |
| `GET, POST` | `/rh/funcoes/<int:funcao_id>/editar` | `editar_funcao_rh` | `app/__init__.py:5030` |
| `POST` | `/rh/funcoes/<int:funcao_id>/deletar` | `deletar_funcao_rh` | `app/__init__.py:5074` |
| `POST` | `/rh/perfis-acesso/novo` | `novo_perfil_acesso_rh` | `app/__init__.py:5094` |
| `GET, POST` | `/rh/perfis-acesso/<int:perfil_id>/editar` | `editar_perfil_acesso_rh` | `app/__init__.py:5128` |
| `POST` | `/rh/perfis-acesso/<int:perfil_id>/deletar` | `deletar_perfil_acesso_rh` | `app/__init__.py:5173` |
| `GET` | `/chamados` | `listar_chamados_internos` | `app/__init__.py:5216` |
| `GET, POST` | `/chamados/novo` | `criar_chamado_interno` | `app/__init__.py:5271` |
| `GET, POST` | `/chamados/<int:chamado_id>/editar` | `editar_chamado_interno` | `app/__init__.py:5340` |
| `POST` | `/chamados/<int:chamado_id>/status` | `atualizar_status_chamado_interno` | `app/__init__.py:5397` |
| `GET` | `/servicos` | `listar_ordens_servico` | `app/__init__.py:5430` |
| `GET` | `/servicos/minhas-ordens` | `minhas_ordens_servico` | `app/__init__.py:5473` |
| `GET, POST` | `/servicos/nova` | `criar_ordem_servico` | `app/__init__.py:5494` |
| `GET, POST` | `/servicos/<int:ordem_id>/editar` | `editar_ordem_servico` | `app/__init__.py:5605` |
| `POST` | `/servicos/<int:ordem_id>/enviar` | `enviar_ordem_servico` | `app/__init__.py:5686` |
| `GET, POST` | `/servicos/<int:ordem_id>/tecnico` | `executar_ordem_servico_tecnico` | `app/__init__.py:5708` |
| `GET` | `/manifest.webmanifest` | `pwa_manifest` | `app/__init__.py:5899` |
| `GET` | `/manifest-loja.webmanifest` | `store_pwa_manifest` | `app/__init__.py:5950` |
| `GET` | `/sw.js` | `pwa_service_worker` | `app/__init__.py:6006` |
| `GET` | `/produtos` | `listar_produtos` | `routes/estoque_routes.py:524` |
| `GET` | `/produtos/etiquetas-loja` | `imprimir_etiquetas_loja` | `routes/estoque_routes.py:688` |
| `POST` | `/produtos/enderecos/armazenar-todos` | `armazenar_todos_produtos_enderecos` | `routes/estoque_routes.py:748` |
| `GET, POST` | `/produtos/novo` | `novo_produto` | `routes/estoque_routes.py:853` |
| `GET, POST` | `/produtos/<int:produto_id>/editar` | `editar_produto` | `routes/estoque_routes.py:934` |
| `GET` | `/produtos/<int:produto_id>` | `visualizar_produto` | `routes/estoque_routes.py:1021` |
| `POST` | `/produtos/<int:produto_id>/deletar` | `deletar_produto` | `routes/estoque_routes.py:1034` |
| `POST` | `/produtos/<int:produto_id>/marcar-fora-picking` | `marcar_produto_fora_picking` | `routes/estoque_routes.py:1054` |
| `POST` | `/produtos/<int:produto_id>/baixar-para-picking` | `baixar_produto_para_picking` | `routes/estoque_routes.py:1071` |
| `GET` | `/estoque/enderecos-inteligentes` | `enderecos_inteligentes` | `routes/estoque_routes.py:1089` |
| `POST` | `/produtos/<int:produto_id>/enderecar-inteligente` | `enderecar_produto_inteligente` | `routes/estoque_routes.py:1169` |
| `GET` | `/estoque/equipamentos` | `listar_equipamentos_movimentacao` | `routes/estoque_routes.py:1193` |
| `GET, POST` | `/estoque/equipamentos/novo` | `novo_equipamento_movimentacao` | `routes/estoque_routes.py:1228` |
| `GET, POST` | `/estoque/equipamentos/<int:equipamento_id>/editar` | `editar_equipamento_movimentacao` | `routes/estoque_routes.py:1281` |
| `GET` | `/categorias` | `listar_categorias` | `routes/estoque_routes.py:1361` |
| `GET, POST` | `/categorias/nova` | `nova_categoria` | `routes/estoque_routes.py:1367` |
| `GET, POST` | `/categorias/<int:categoria_id>/editar` | `editar_categoria` | `routes/estoque_routes.py:1398` |
| `POST` | `/categorias/<int:categoria_id>/deletar` | `deletar_categoria` | `routes/estoque_routes.py:1436` |
| `GET` | `/fornecedores` | `listar_fornecedores` | `routes/estoque_routes.py:1452` |
| `GET` | `/fornecedores/<int:fornecedor_id>` | `detalhes_fornecedor` | `routes/estoque_routes.py:1489` |
| `GET, POST` | `/fornecedores/novo` | `novo_fornecedor` | `routes/estoque_routes.py:1510` |
| `GET, POST` | `/fornecedores/<int:fornecedor_id>/editar` | `editar_fornecedor` | `routes/estoque_routes.py:1541` |
| `POST` | `/fornecedores/<int:fornecedor_id>/deletar` | `deletar_fornecedor` | `routes/estoque_routes.py:1571` |
| `GET` | `/estoque/recebimentos` | `listar_recebimentos_fornecedor` | `routes/estoque_routes.py:1584` |
| `GET, POST` | `/estoque/recebimentos/novo` | `novo_recebimento_fornecedor` | `routes/estoque_routes.py:1687` |
| `GET, POST` | `/estoque/recebimentos/<int:recebimento_id>/conferir` | `conferir_recebimento_fornecedor` | `routes/estoque_routes.py:1884` |
| `GET, POST` | `/estoque/recebimentos/<int:recebimento_id>/armazenar` | `armazenar_recebimento_fornecedor` | `routes/estoque_routes.py:1953` |
| `POST` | `/estoque/recebimentos/<int:recebimento_id>/cancelar` | `cancelar_recebimento_fornecedor` | `routes/estoque_routes.py:2066` |
| `GET` | `/estoque/almoxarifado` | `listar_almoxarifado` | `routes/estoque_routes.py:2085` |
| `GET, POST` | `/estoque/almoxarifado/nova` | `nova_atribuicao_almoxarifado` | `routes/estoque_routes.py:2157` |
| `GET` | `/enderecos-estoque` | `listar_enderecos_estoque` | `routes/estoque_routes.py:2257` |
| `GET` | `/enderecos-estoque/<int:endereco_id>/detalhes` | `detalhes_endereco_estoque` | `routes/estoque_routes.py:2351` |
| `GET` | `/enderecos-estoque/<int:endereco_id>/etiqueta` | `imprimir_etiqueta_endereco_estoque` | `routes/estoque_routes.py:2370` |
| `GET` | `/enderecos-estoque/etiquetas` | `imprimir_etiquetas_enderecos_estoque` | `routes/estoque_routes.py:2389` |
| `GET` | `/estoques` | `listar_estoques` | `routes/estoque_routes.py:2415` |
| `GET, POST` | `/estoques/novo` | `novo_estoque` | `routes/estoque_routes.py:2452` |
| `GET, POST` | `/estoques/<int:estoque_id>/editar` | `editar_estoque` | `routes/estoque_routes.py:2481` |
| `POST` | `/estoques/<int:estoque_id>/deletar` | `deletar_estoque` | `routes/estoque_routes.py:2520` |
| `GET, POST` | `/enderecos-estoque/novo` | `novo_endereco_estoque` | `routes/estoque_routes.py:2548` |
| `GET, POST` | `/enderecos-estoque/<int:endereco_id>/editar` | `editar_endereco_estoque` | `routes/estoque_routes.py:2790` |
| `POST` | `/enderecos-estoque/<int:endereco_id>/deletar` | `deletar_endereco_estoque` | `routes/estoque_routes.py:2899` |
| `GET, POST` | `/movimentacoes/rapido/<int:produto_id>` | `movimentacao_rapida` | `routes/estoque_routes.py:2917` |
| `GET` | `/movimentacoes` | `listar_movimentacoes` | `routes/estoque_routes.py:2981` |
| `GET, POST` | `/movimentacoes/nova` | `nova_movimentacao` | `routes/estoque_routes.py:3060` |
| `GET` | `/movimentacoes/transferencias` | `listar_transferencias_estoque` | `routes/estoque_routes.py:3130` |
| `GET, POST` | `/movimentacoes/transferencia` | `transferir_armazenamento` | `routes/estoque_routes.py:3186` |
| `GET` | `/api/estoque/analytics` | `analytics_estoque_api` | `routes/estoque_routes.py:3272` |
| `GET` | `/relatorios` | `relatorios` | `routes/estoque_routes.py:3353` |
| `GET` | `/expedicao` | `central_expedicao` | `routes/vendas_routes.py:911` |
| `GET, POST` | `/expedicao/frota` | `frota_expedicao` | `routes/vendas_routes.py:930` |
| `GET` | `/garcons` | `listar_garcons` | `routes/vendas_routes.py:971` |
| `GET, POST` | `/garcons/novo` | `novo_garcom` | `routes/vendas_routes.py:987` |
| `GET, POST` | `/garcons/<int:garcom_id>/editar` | `editar_garcom` | `routes/vendas_routes.py:1012` |
| `POST` | `/garcons/<int:garcom_id>/deletar` | `deletar_garcom` | `routes/vendas_routes.py:1036` |
| `GET, POST` | `/garcons/config` | `configurar_distribuicao_garcons` | `routes/vendas_routes.py:1053` |
| `GET` | `/caixas` | `listar_caixas` | `routes/vendas_routes.py:1075` |
| `GET, POST` | `/caixas/nova` | `nova_caixa` | `routes/vendas_routes.py:1081` |
| `GET, POST` | `/caixas/<int:caixa_id>/editar` | `editar_caixa` | `routes/vendas_routes.py:1098` |
| `POST` | `/caixas/<int:caixa_id>/deletar` | `deletar_caixa` | `routes/vendas_routes.py:1118` |
| `GET, POST` | `/caixas/<int:caixa_id>/abrir` | `abrir_caixa` | `routes/vendas_routes.py:1131` |
| `GET, POST` | `/caixas/<int:caixa_id>/fechar` | `fechar_caixa` | `routes/vendas_routes.py:1180` |
| `GET` | `/caixas/<int:caixa_id>/historico` | `historico_caixa` | `routes/vendas_routes.py:1226` |
| `GET` | `/mesas` | `listar_mesas` | `routes/vendas_routes.py:1237` |
| `GET, POST` | `/mesas/nova` | `nova_mesa` | `routes/vendas_routes.py:1251` |
| `GET, POST` | `/mesas/<int:mesa_id>/editar` | `editar_mesa` | `routes/vendas_routes.py:1271` |
| `POST` | `/mesas/<int:mesa_id>/deletar` | `deletar_mesa` | `routes/vendas_routes.py:1293` |
| `GET` | `/mesas/<int:mesa_id>/qrcode` | `visualizar_qrcode_mesa` | `routes/vendas_routes.py:1309` |
| `GET` | `/mesas/<int:mesa_id>/qrcode/download` | `download_qrcode_mesa` | `routes/vendas_routes.py:1328` |
| `GET` | `/mesas/<int:mesa_id>/qrcode/print` | `print_qrcode_mesa` | `routes/vendas_routes.py:1372` |
| `GET` | `/pedidos` | `listar_pedidos` | `routes/vendas_routes.py:1389` |
| `GET` | `/pedidos/separacao-entrega` | `listar_separacao_entrega` | `routes/vendas_routes.py:1477` |
| `GET` | `/estoque/coletor` | `coletor_estoque` | `routes/vendas_routes.py:1538` |
| `POST` | `/pedidos/expedicao/iniciar` | `iniciar_processo_expedicao` | `routes/vendas_routes.py:1604` |
| `GET` | `/pedidos/expedicao/painel` | `painel_expedicao` | `routes/vendas_routes.py:1615` |
| `GET` | `/api/pedidos/expedicao/progresso` | `api_progresso_expedicao` | `routes/vendas_routes.py:1632` |
| `GET` | `/pedidos/roteirizacao-entrega` | `listar_roteirizacao_entrega` | `routes/vendas_routes.py:1643` |
| `POST` | `/pedidos/roteirizacao-entrega/otimizar` | `otimizar_rota_entrega` | `routes/vendas_routes.py:1732` |
| `POST` | `/pedidos/<int:pedido_id>/despacho-entrega` | `atualizar_despacho_entrega` | `routes/vendas_routes.py:1806` |
| `POST` | `/pedidos/<int:pedido_id>/separacao-entrega` | `atualizar_separacao_entrega_pedido` | `routes/vendas_routes.py:1844` |
| `GET` | `/pedidos/<int:pedido_id>/etiqueta-entrega` | `imprimir_etiqueta_entrega_pedido` | `routes/vendas_routes.py:1912` |
| `GET` | `/pedidos/pendentes` | `listar_pedidos_pendentes` | `routes/vendas_routes.py:1942` |
| `POST` | `/pedidos/<int:pedido_id>/status` | `alterar_status_pedido` | `routes/vendas_routes.py:1957` |
| `GET, POST` | `/pedidos/novo` | `novo_pedido` | `routes/vendas_routes.py:1977` |
| `GET, POST` | `/pedidos/<int:pedido_id>/editar` | `editar_pedido` | `routes/vendas_routes.py:2051` |
| `POST` | `/pedidos/<int:pedido_id>/deletar` | `deletar_pedido` | `routes/vendas_routes.py:2146` |
| `GET` | `/pedidos/<int:pedido_id>/comprovante` | `visualizar_comprovante_pedido` | `routes/vendas_routes.py:2159` |
| `GET` | `/pedidos/<int:pedido_id>/detalhes` | `detalhes_pedido` | `routes/vendas_routes.py:2178` |
| `GET` | `/pdv` | `pdv` | `routes/vendas_routes.py:2207` |
| `POST` | `/api/pedidos/criar` | `criar_pedido_api` | `routes/vendas_routes.py:2229` |
| `POST` | `/api/pedidos/<int:pedido_id>/finalizar` | `finalizar_pedido_api` | `routes/vendas_routes.py:2312` |
| `GET` | `/api/pedidos/aberto/<int:caixa_id>` | `get_pedido_aberto` | `routes/vendas_routes.py:2358` |
| `GET` | `/api/pedidos/em-aberto` | `listar_pedidos_em_aberto_pdv` | `routes/vendas_routes.py:2380` |
| `GET` | `/api/pedidos/caixa/<int:caixa_id>/em-aberto` | `listar_pedidos_caixa_em_aberto` | `routes/vendas_routes.py:2426` |
| `GET` | `/api/pedidos/<int:pedido_id>/detalhes-json` | `detalhes_pedido_api` | `routes/vendas_routes.py:2469` |
| `POST` | `/api/pedidos/<int:pedido_id>/adicionar` | `adicionar_itens_pedido_api` | `routes/vendas_routes.py:2500` |
| `GET` | `/eventos/pedidos` | `sse_pedidos` | `routes/vendas_routes.py:2544` |

## 4) Modelos de Dados Centrais
### Modelo: `Categoria`
- `id: db.Integer, primary_key=True`
- `nome: db.String(100), unique=True, nullable=False`
- `descricao: db.Text`
- `imagem_path: db.String(255)`
- `criado_em: db.DateTime, default=datetime.utcnow`

### Modelo: `Produto`
- `id: db.Integer, primary_key=True`
- `codigo: db.String(50), unique=True, nullable=False, index=True`
- `nome: db.String(200), nullable=False`
- `descricao: db.Text`
- `imagem_path: db.String(255)`
- `categoria_id: db.Integer, db.ForeignKey('categorias.id'), nullable=False`
- `fornecedor_id: db.Integer, db.ForeignKey('fornecedores.id'), nullable=True`
- `endereco_id: db.Integer, db.ForeignKey('enderecos_estoque.id'), nullable=True`
- `preco_custo: db.Float, nullable=False`
- `preco_venda: db.Float, nullable=False`
- `quantidade_estoque: db.Integer, default=0`
- `quantidade_minima: db.Integer, default=5`
- `status_disponibilidade: db.String(30), default=STATUS_DISPONIVEL_ONLINE, nullable=False`
- `tipo_movimentacao: db.String(20), default='manual', nullable=False`
- `fora_picking: db.Boolean, default=False`
- `prioridade_reabastecimento: db.Integer, nullable=True`
- `ultima_baixa_picking_em: db.DateTime, nullable=True`
- `servico_montagem_disponivel: db.Boolean, default=False`
- `servico_instalacao_disponivel: db.Boolean, default=False`
- `ativo: db.Boolean, default=True`

### Modelo: `Movimentacao`
- `id: db.Integer, primary_key=True`
- `produto_id: db.Integer, db.ForeignKey('produtos.id'), nullable=False`
- `fornecedor_id: db.Integer, db.ForeignKey('fornecedores.id'), nullable=True`
- `endereco_origem_id: db.Integer, db.ForeignKey('enderecos_estoque.id'), nullable=True`
- `endereco_destino_id: db.Integer, db.ForeignKey('enderecos_estoque.id'), nullable=True`
- `quantidade: db.Integer, nullable=False`
- `valor_compra: db.Float, nullable=True`
- `info_nota: db.String(255)`
- `observacoes: db.Text`
- `criado_em: db.DateTime, default=datetime.utcnow`

### Modelo: `EquipamentoMovimentacao`
- `id: db.Integer, primary_key=True`
- `codigo: db.String(40), unique=True, nullable=False, index=True`
- `nome: db.String(120), nullable=False`
- `tipo: db.String(20), nullable=False, default=TIPO_EMPILHADEIRA`
- `placa: db.String(20), nullable=True`
- `capacidade_kg: db.Float, nullable=True`
- `bateria_codigo: db.String(40), nullable=True`
- `bateria_nivel: db.Integer, nullable=True`
- `status: db.String(20), nullable=False, default=STATUS_OPERACIONAL`
- `proxima_manutencao_em: db.Date, nullable=True`
- `observacoes: db.Text, nullable=True`
- `ativo: db.Boolean, default=True`
- `criado_em: db.DateTime, default=datetime.utcnow, nullable=False`
- `atualizado_em: db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False`

### Modelo: `ManutencaoEquipamento`
- `id: db.Integer, primary_key=True`
- `equipamento_id: db.Integer, db.ForeignKey('equipamentos_movimentacao.id'), nullable=False, index=True`
- `tipo: db.String(20), nullable=False, default='preventiva'`
- `descricao: db.String(255), nullable=False`
- `custo: db.Float, nullable=True`
- `realizado_em: db.Date, nullable=True`
- `proxima_em: db.Date, nullable=True`
- `responsavel: db.String(120), nullable=True`
- `criado_em: db.DateTime, default=datetime.utcnow, nullable=False`

### Modelo: `Fornecedor`
- `id: db.Integer, primary_key=True`
- `nome: db.String(150), unique=True, nullable=False`
- `documento: db.String(30), nullable=True`
- `contato: db.String(120)`
- `telefone: db.String(30)`
- `email: db.String(120)`
- `endereco_rua: db.String(160), nullable=True`
- `endereco_numero: db.String(20), nullable=True`
- `endereco_bairro: db.String(100), nullable=True`
- `endereco_cidade: db.String(100), nullable=True`
- `tipo_produtos_fornece: db.String(255), nullable=True`
- `observacoes_gerais: db.Text, nullable=True`
- `ativo: db.Boolean, default=True`
- `criado_em: db.DateTime, default=datetime.utcnow, index=True`

### Modelo: `Estoque`
- `id: db.Integer, primary_key=True`
- `nome: db.String(120), unique=True, nullable=False`
- `codigo_filial: db.String(20), nullable=True, index=True`
- `descricao: db.String(255)`
- `ativo: db.Boolean, default=True`
- `criado_em: db.DateTime, default=datetime.utcnow, index=True`
- `endereco_origem_id: db.Integer, db.ForeignKey('enderecos_estoque.id'), nullable=True`
- `endereco_destino_id: db.Integer, db.ForeignKey('enderecos_estoque.id'), nullable=True`

### Modelo: `EnderecoEstoque`
- `id: db.Integer, primary_key=True`
- `estoque_id: db.Integer, db.ForeignKey('estoques.id'), nullable=True`
- `nome: db.String(120), nullable=False, unique=True`
- `codigo_localizacao: db.String(60), unique=True, nullable=True`
- `loja_cd: db.String(20), nullable=True`
- `setor_zona: db.String(30), nullable=True`
- `tipo_area: db.String(40), nullable=True`
- `status: db.String(20), default='ativo', nullable=False`
- `descricao: db.String(255), nullable=True`
- `tipo_estrutura: db.String(20), nullable=True`
- `codigo_armazem: db.String(20), nullable=True`
- `rua_corredor: db.String(20), nullable=True`
- `coluna_baia: db.String(10), nullable=True`
- `nivel_prateleira: db.String(10), nullable=True`
- `posicao_slot: db.String(10), nullable=True`
- `lado: db.String(4), nullable=True`
- `ponto_local: db.String(255), nullable=True`
- `permite_fracionado: db.Boolean, default=False`
- `permite_mistura_sku: db.Boolean, default=False`
- `permite_mistura_lote: db.Boolean, default=False`

### Modelo: `RecebimentoFornecedor`
- `id: db.Integer, primary_key=True`
- `fornecedor_id: db.Integer, db.ForeignKey('fornecedores.id'), nullable=True`
- `tipo_recebimento: db.String(40), nullable=False, default=TIPO_COMPRA_REVENDA`
- `fornecedor_documento: db.String(30), nullable=True`
- `data_entrega: db.Date, nullable=True`
- `info_nota: db.String(255), nullable=True`
- `subtotal: db.Float, nullable=True, default=0.0`
- `desconto: db.Float, nullable=True, default=0.0`
- `total_pagar: db.Float, nullable=True, default=0.0`
- `status: db.String(30), default=STATUS_CRIADO, nullable=False`
- `observacoes: db.Text, nullable=True`
- `recebedor_funcionario_id: db.Integer, db.ForeignKey('funcionarios.id'), nullable=True`
- `recebedor_nome: db.String(120), nullable=True`
- `recebedor_assinatura: db.String(255), nullable=True`
- `entregador_nome: db.String(120), nullable=True`
- `entregador_assinatura: db.String(255), nullable=True`
- `criado_em: db.DateTime, default=datetime.utcnow`
- `atualizado_em: db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow`
- `conferido_em: db.DateTime, nullable=True`
- `armazenado_em: db.DateTime, nullable=True`

### Modelo: `RecebimentoItem`
- `id: db.Integer, primary_key=True`
- `recebimento_id: db.Integer, db.ForeignKey('recebimentos_fornecedor.id'), nullable=False`
- `produto_id: db.Integer, db.ForeignKey('produtos.id'), nullable=False`
- `qtd_recebida: db.Integer, nullable=False, default=0`
- `unidade: db.String(10), nullable=True`
- `descricao_item: db.String(255), nullable=True`
- `preco_unitario: db.Float, nullable=True, default=0.0`
- `total_item: db.Float, nullable=True, default=0.0`
- `qtd_avaria: db.Integer, nullable=False, default=0`
- `lote: db.String(80), nullable=True`
- `validade: db.Date, nullable=True`
- `endereco_destino_id: db.Integer, db.ForeignKey('enderecos_estoque.id'), nullable=True`
- `criado_em: db.DateTime, default=datetime.utcnow`

### Modelo: `Caixa`
- `id: db.Integer, primary_key=True`
- `nome: db.String(100), unique=True, nullable=False`
- `funcionario_id: db.Integer, db.ForeignKey('funcionarios.id'), nullable=True`
- `saldo_inicial: db.Float, default=0.0`
- `saldo_atual: db.Float, default=0.0`
- `saldo_fechamento: db.Float, nullable=True`
- `aberto: db.Boolean, default=False`
- `aberto_em: db.DateTime, nullable=True`
- `fechado_em: db.DateTime, nullable=True`
- `observacoes: db.Text`
- `criado_em: db.DateTime, default=datetime.utcnow`

### Modelo: `Mesa`
- `id: db.Integer, primary_key=True`
- `numero: db.String(20), unique=True, nullable=False`
- `capacidade: db.Integer, default=4`
- `qr_token: db.String(64), unique=True, nullable=True`
- `descricao: db.Text`

### Modelo: `Pedido`
- `id: db.Integer, primary_key=True`
- `mesa_id: db.Integer, db.ForeignKey('mesas.id'), nullable=True`
- `caixa_id: db.Integer, db.ForeignKey('caixas.id'), nullable=True`
- `garcom_id: db.Integer, db.ForeignKey('garcons.id'), nullable=True`
- `cliente_nome: db.String(120)`
- `cliente_celular: db.String(30)`
- `total: db.Float, default=0.0`
- `metodo_pagamento: db.String(50)`
- `valor_pago: db.Float, nullable=True`
- `estoque_processado: db.Boolean, default=False`
- `financeiro_processado: db.Boolean, default=False`
- `separacao_entrega_concluida: db.Boolean, default=False`
- `separacao_entrega_em: db.DateTime, nullable=True`
- `etiqueta_entrega_emitida_em: db.DateTime, nullable=True`
- `rota_entrega: db.String(120), nullable=True`
- `ordem_rota: db.Integer, nullable=True`
- `local_saida: db.String(160), nullable=True`
- `veiculo_tipo: db.String(80), nullable=True`
- `veiculo_placa: db.String(20), nullable=True`
- `motorista_nome: db.String(120), nullable=True`

### Modelo: `ClientePublico`
- `id: db.Integer, primary_key=True`
- `nome: db.String(120), nullable=False`
- `email: db.String(120), nullable=False, index=True`
- `celular: db.String(30), nullable=False, index=True`
- `cpf_cnpj: db.String(20), nullable=True, index=True`
- `cep: db.String(12), nullable=True`
- `endereco: db.String(180), nullable=True`
- `numero: db.String(20), nullable=True`
- `complemento: db.String(120), nullable=True`
- `bairro: db.String(100), nullable=True`
- `cidade: db.String(100), nullable=True`
- `estado: db.String(2), nullable=True`
- `referencia: db.String(180), nullable=True`
- `recebe_ofertas: db.Boolean, default=False`
- `observacoes: db.Text, nullable=True`
- `criado_em: db.DateTime, default=datetime.utcnow, index=True`
- `atualizado_em: db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow`

### Modelo: `ItemPedido`
- `id: db.Integer, primary_key=True`
- `pedido_id: db.Integer, db.ForeignKey('pedidos.id'), nullable=False`
- `produto_id: db.Integer, db.ForeignKey('produtos.id'), nullable=False`
- `quantidade: db.Integer, default=1`
- `preco_unitario: db.Float, nullable=False`

### Modelo: `Garcom`
- `id: db.Integer, primary_key=True`
- `funcionario_id: db.Integer, db.ForeignKey('funcionarios.id'), nullable=True`
- `nome: db.String(120), nullable=False`
- `celular: db.String(30)`
- `ativo: db.Boolean, default=True`
- `criado_em: db.DateTime, default=datetime.utcnow`

### Modelo: `Funcionario`
- `id: db.Integer, primary_key=True`
- `nome: db.String(100), nullable=False`
- `email: db.String(120), unique=True, nullable=False, index=True`
- `numero_cadastro: db.Integer, unique=True, nullable=True, index=True`
- `matricula: db.String(30), unique=True, nullable=True, index=True`
- `cpf: db.String(14), nullable=True, index=True`
- `rg: db.String(20), nullable=True`
- `data_nascimento: db.Date, nullable=True`
- `celular: db.String(30), nullable=True`
- `cep: db.String(12), nullable=True`
- `endereco: db.String(180), nullable=True`
- `bairro: db.String(100), nullable=True`
- `cidade: db.String(100), nullable=True`
- `estado: db.String(2), nullable=True`
- `senha_hash: db.String(255), nullable=False`
- `imagem_perfil_path: db.String(255), nullable=True`
- `permitir_editar_imagem_perfil: db.Boolean, default=False`
- `senha_provisoria: db.Boolean, default=False`
- `cargo: db.String(100), nullable=True`
- `departamento: db.String(80), nullable=True`

### Modelo: `AlmoxarifadoAtribuicao`
- `id: db.Integer, primary_key=True`
- `produto_id: db.Integer, db.ForeignKey('produtos.id'), nullable=False, index=True`
- `funcionario_id: db.Integer, db.ForeignKey('funcionarios.id'), nullable=True, index=True`
- `registrado_por_id: db.Integer, db.ForeignKey('funcionarios.id'), nullable=True`
- `destino_tipo: db.String(20), nullable=False, default=DESTINO_FUNCIONARIO`
- `nome_destino: db.String(120), nullable=False`
- `setor_destino: db.String(80), nullable=True`
- `matricula_referencia: db.String(30), nullable=True`
- `quantidade: db.Integer, nullable=False, default=1`
- `observacoes: db.Text, nullable=True`
- `criado_em: db.DateTime, default=datetime.utcnow, nullable=False, index=True`
- `atualizado_em: db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False`

### Modelo: `FuncaoRH`
- `id: db.Integer, primary_key=True`
- `nome: db.String(100), unique=True, nullable=False`
- `descricao: db.String(255)`
- `ativo: db.Boolean, default=True`
- `criado_em: db.DateTime, default=datetime.utcnow`
- `atualizado_em: db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow`

### Modelo: `PerfilAcesso`
- `id: db.Integer, primary_key=True`
- `nome: db.String(100), unique=True, nullable=False`
- `descricao: db.String(255)`
- `permissoes_padrao: db.Text`
- `ativo: db.Boolean, default=True`
- `criado_em: db.DateTime, default=datetime.utcnow`
- `atualizado_em: db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow`

### Modelo: `PermissaoAcesso`
- `id: db.Integer, primary_key=True`
- `funcionario_id: db.Integer, db.ForeignKey('funcionarios.id'), nullable=False`
- `pagina: db.String(80), nullable=False`
- `permitido: db.Boolean, default=True, nullable=False`
- `criado_em: db.DateTime, default=datetime.utcnow`

### Modelo: `MovimentacaoCaixa`
- `id: db.Integer, primary_key=True`
- `caixa_id: db.Integer, db.ForeignKey('caixas.id'), nullable=False`
- `valor: db.Float, nullable=False`
- `descricao: db.String(200), nullable=False`
- `criado_em: db.DateTime, default=datetime.utcnow`

### Modelo: `LancamentoFinanceiro`
- `id: db.Integer, primary_key=True`
- `tipo: db.String(30), nullable=False, index=True`
- `categoria: db.String(80), nullable=True`
- `descricao: db.String(255), nullable=False`
- `valor: db.Float, nullable=False`
- `data_competencia: db.Date, nullable=False, index=True`
- `incluir_contabilidade: db.Boolean, default=True, nullable=False`
- `enviado_contador: db.Boolean, default=False, nullable=False`
- `enviado_em: db.DateTime, nullable=True`
- `referencia_documento: db.String(120), nullable=True`
- `centro_custo: db.String(120), nullable=True`
- `produto_id: db.Integer, db.ForeignKey('produtos.id'), nullable=True`
- `quantidade: db.Float, nullable=True`
- `criado_por_id: db.Integer, db.ForeignKey('funcionarios.id'), nullable=True`
- `criado_em: db.DateTime, default=datetime.utcnow, nullable=False`
- `atualizado_em: db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False`

### Modelo: `FundoSolicitacao`
- `id: db.Integer, primary_key=True`
- `tipo: db.String(20), nullable=False, default=TIPO_APORTE`
- `categoria: db.String(80), nullable=True`
- `descricao: db.String(255), nullable=False`
- `valor: db.Float, nullable=False`
- `centro_custo: db.String(120), nullable=True`
- `referencia_documento: db.String(120), nullable=True`
- `status: db.String(20), nullable=False, default=STATUS_SOLICITADA, index=True`
- `motivo_rejeicao: db.String(255), nullable=True`
- `solicitado_por_id: db.Integer, db.ForeignKey('funcionarios.id'), nullable=True, index=True`
- `aprovado_por_id: db.Integer, db.ForeignKey('funcionarios.id'), nullable=True`
- `liberado_por_id: db.Integer, db.ForeignKey('funcionarios.id'), nullable=True`
- `lancamento_financeiro_id: db.Integer, db.ForeignKey('lancamentos_financeiros.id'), nullable=True`
- `solicitado_em: db.DateTime, default=datetime.utcnow, nullable=False`
- `aprovado_em: db.DateTime, nullable=True`
- `liberado_em: db.DateTime, nullable=True`
- `atualizado_em: db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False`

### Modelo: `EmpresaConfig`
- `id: db.Integer, primary_key=True`
- `razao_social: db.String(150)`
- `nome_fantasia: db.String(150)`
- `codigo_empresa: db.String(20)`
- `cnpj: db.String(20)`
- `inscricao_estadual: db.String(30)`
- `telefone: db.String(30)`
- `email: db.String(120)`
- `endereco: db.String(200)`
- `cidade: db.String(100)`
- `estado: db.String(2)`
- `cep: db.String(12)`
- `logo_path: db.String(255)`
- `favicon_path: db.String(255), nullable=True`
- `app_icon_path: db.String(255), nullable=True`
- `mensagem_comprovante: db.String(255)`
- `cardapio_titulo: db.String(120)`
- `cardapio_subtitulo: db.String(255)`
- `cardapio_mensagem: db.String(255)`
- `cardapio_mostrar_imagem: db.Boolean, default=True`

### Modelo: `AuditoriaEvento`
- `id: db.Integer, primary_key=True`
- `funcionario_id: db.Integer, db.ForeignKey('funcionarios.id'), nullable=True`
- `funcionario_nome: db.String(120)`
- `funcionario_email: db.String(120)`
- `funcionario_role: db.String(20)`
- `metodo: db.String(10), nullable=False`
- `endpoint: db.String(120)`
- `rota: db.String(255)`
- `acao: db.String(120), nullable=False`
- `entidade: db.String(80)`
- `detalhes: db.Text`
- `status_code: db.Integer`
- `ip: db.String(64)`
- `criado_em: db.DateTime, default=datetime.utcnow`

### Modelo: `AssistenteLocalFeedback`
- `id: db.Integer, primary_key=True`
- `funcionario_id: db.Integer, db.ForeignKey('funcionarios.id'), nullable=False, index=True`
- `response_id: db.String(64), nullable=False, index=True`
- `vote: db.String(10), nullable=False, index=True`
- `question: db.Text, nullable=True`
- `answer: db.Text, nullable=True`
- `reason: db.String(255), nullable=True`
- `endpoint_atual: db.String(120), nullable=True`
- `pagina_atual: db.String(80), nullable=True, index=True`
- `tela_atual: db.String(120), nullable=True`
- `matched_doc_ids_json: db.Text, nullable=True`
- `criado_em: db.DateTime, default=datetime.utcnow, nullable=False, index=True`
- `atualizado_em: db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False`

### Modelo: `OrdemServico`
- `id: db.Integer, primary_key=True`
- `titulo: db.String(160), nullable=False`
- `tipo: db.String(30), nullable=False, default=TIPO_ORDEM_SERVICO, index=True`
- `servico_tipo: db.String(20), nullable=False, default=SERVICO_NENHUM`
- `prioridade: db.String(20), nullable=True`
- `status: db.String(30), nullable=False, default=STATUS_ABERTA, index=True`
- `descricao: db.Text, nullable=True`
- `observacoes: db.Text, nullable=True`
- `avaria_detalhes: db.Text, nullable=True`
- `inspecao_detalhes: db.Text, nullable=True`
- `resultado_inspecao: db.String(120), nullable=True`
- `produto_id: db.Integer, db.ForeignKey('produtos.id'), nullable=True`
- `pedido_id: db.Integer, db.ForeignKey('pedidos.id'), nullable=True, index=True`
- `funcionario_destino_id: db.Integer, db.ForeignKey('funcionarios.id'), nullable=True, index=True`
- `criado_por_id: db.Integer, db.ForeignKey('funcionarios.id'), nullable=True`
- `data_agendada: db.Date, nullable=True`
- `enviada_em: db.DateTime, nullable=True`
- `iniciado_em: db.DateTime, nullable=True`
- `concluida_em: db.DateTime, nullable=True`
- `retorno_tecnico: db.Text, nullable=True`

### Modelo: `ChamadoInterno`
- `id: db.Integer, primary_key=True`
- `titulo: db.String(160), nullable=False, index=True`
- `categoria: db.String(40), nullable=False, default=CATEGORIA_SISTEMA, index=True`
- `prioridade: db.String(20), nullable=False, default='media', index=True`
- `status: db.String(30), nullable=False, default=STATUS_ABERTO, index=True`
- `setor_origem: db.String(80), nullable=True`
- `descricao: db.Text, nullable=False`
- `resolucao: db.Text, nullable=True`
- `solicitante_id: db.Integer, db.ForeignKey('funcionarios.id'), nullable=False, index=True`
- `responsavel_id: db.Integer, db.ForeignKey('funcionarios.id'), nullable=True, index=True`
- `aberto_em: db.DateTime, default=datetime.utcnow, nullable=False, index=True`
- `concluido_em: db.DateTime, nullable=True`
- `atualizado_em: db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False`

## 5) Fluxos de Negocio (Resumo)
- **Cadastro e acesso**: login por funcionario com controle de permissao por pagina.
- **Estoque**: produtos, movimentacoes, recebimentos, enderecamento e relatorios.
- **Vendas**: PDV, pedidos, status e comprovantes.
- **Expedicao**: separacao, roteirizacao, etiquetas, frota e painel em tempo real.
- **Financeiro**: indicadores, lancamentos, fundos e exportacao para contador.
- **RH**: funcionarios, funcoes/perfis, organograma e auditoria.
- **E-commerce**: tema, banners, promocoes e configuracoes de loja.

## 6) Codigo Mais Importante (Snippets)
### Arquivo: `app/__init__.py`
#### `dashboard` (`app/__init__.py:1322`)
```python
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
```

#### `gestao_negocio` (`app/__init__.py:1465`)
```python
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
```

#### `financeiro` (`app/__init__.py:1589`)
```python
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
```

#### `editar_empresa` (`app/__init__.py:2059`)
```python
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
```

#### `configurar_ecommerce` (`app/__init__.py:2288`)
```python
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
```

#### `central_ajuda` (`app/__init__.py:3914`)
```python
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
```

#### `detalhe_ajuda` (`app/__init__.py:3958`)
```python
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
```

#### `listar_funcionarios` (`app/__init__.py:3984`)
```python
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
```

#### `listar_perfis_rh` (`app/__init__.py:4506`)
```python
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
```

### Arquivo: `routes/estoque_routes.py`
#### `listar_produtos` (`routes/estoque_routes.py:522`)
```python
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
```

#### `novo_produto` (`routes/estoque_routes.py:851`)
```python
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
```

#### `editar_produto` (`routes/estoque_routes.py:932`)
```python
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
```

#### `listar_movimentacoes` (`routes/estoque_routes.py:2979`)
```python
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
```

#### `transferir_armazenamento` (`routes/estoque_routes.py:3184`)
```python
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
```

#### `relatorios` (`routes/estoque_routes.py:3351`)
```python
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
```

### Arquivo: `routes/vendas_routes.py`
#### `register_vendas_routes` (`routes/vendas_routes.py:903`)
```python
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
```

#### `listar_pedidos` (`routes/vendas_routes.py:1387`)
```python
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
```

#### `detalhes_pedido` (`routes/vendas_routes.py:2176`)
```python
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
```

#### `atualizar_separacao_entrega_pedido` (`routes/vendas_routes.py:1842`)
```python
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
```

#### `listar_roteirizacao_entrega` (`routes/vendas_routes.py:1641`)
```python
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
```

#### `painel_expedicao` (`routes/vendas_routes.py:1613`)
```python
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
```

#### `central_expedicao` (`routes/vendas_routes.py:909`)
```python
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
```

#### `frota_expedicao` (`routes/vendas_routes.py:928`)
```python
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
```

## 7) Como Atualizar Esta Documentacao
```bash
python scripts/generate_system_documentation.py
```

Parametros uteis:
- `--output docs/system_overview_ai.md`
- `--max-snippet-lines 120`
- `--max-model-fields 20`

Observacao: este arquivo e um resumo tecnico orientado a entendimento rapido. Para dump completo de backend, use `scripts/generate_backend_ai_report.py`.
