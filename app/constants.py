"""Constantes de domínio do SystemLR."""

TIPOS_MOVIMENTACAO_VALIDOS = {'entrada', 'saida'}
ROLES_PERMITIDOS = {'admin', 'gerente', 'caixa', 'operador', 'garcom'}

CARGOS_PERMANENTES = (
    ('Garcom', 'Atendimento de mesas e acompanhamento de pedidos.'),
)

PAGINAS_SISTEMA = {
    'inicio': 'Início e Dashboard',
    'pdv': 'PDV',
    'estoques': 'Estoques',
    'produtos': 'Produtos',
    'categorias': 'Categorias',
    'fornecedores': 'Fornecedores',
    'enderecos_estoque': 'Endereços de Estoque',
    'movimentacoes': 'Movimentações',
    'relatorios': 'Relatórios',
    'caixas': 'Caixas',
    'mesas': 'Mesas',
    'pedidos': 'Pedidos',
    'funcionarios': 'Funcionários',
    'rh_funcoes': 'RH - Funções',
    'rh_indicadores': 'RH - Indicadores',
    'auditoria': 'Auditoria',
    'empresa': 'Empresa',
    'ecommerce_config': 'E-commerce - Configuração',
    'garcons': 'Garçons',
    'ajuda': 'Ajuda e Treinamento',
}

PAGINAS_SISTEMA_MENU_ORDEM = (
    ('Dashboard', ('inicio',)),
    ('Vendas', ('pdv', 'pedidos', 'mesas', 'caixas', 'garcons')),
    ('Estoque', ('estoques', 'produtos', 'categorias', 'fornecedores', 'enderecos_estoque', 'movimentacoes', 'relatorios')),
    ('Meu RH', ('rh_indicadores', 'funcionarios', 'rh_funcoes', 'auditoria', 'empresa')),
    ('E-commerce', ('ecommerce_config',)),
    ('Ajuda', ('ajuda',)),
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
    'pedidos': {
        'listar_pedidos',
        'listar_pedidos_pendentes',
        'listar_separacao_entrega',
        'atualizar_separacao_entrega_pedido',
        'imprimir_etiqueta_entrega_pedido',
        'novo_pedido',
        'editar_pedido',
        'deletar_pedido',
        'visualizar_comprovante_pedido',
        'detalhes_pedido',
        'alterar_status_pedido',
    },
    'funcionarios': {'listar_funcionarios', 'criar_funcionario', 'editar_funcionario', 'deletar_funcionario', 'editar_acessos_funcionario'},
    'rh_funcoes': {'listar_funcoes_rh', 'nova_funcao_rh', 'editar_funcao_rh', 'deletar_funcao_rh'},
    'rh_indicadores': {'indicadores_rh', 'analytics_rh_api'},
    'auditoria': {'auditoria_sistema'},
    'empresa': {'editar_empresa', 'preview_cardapio_empresa'},
    'ecommerce_config': {'configurar_ecommerce'},
    'garcons': {'listar_garcons', 'novo_garcom', 'editar_garcom', 'deletar_garcom', 'configurar_distribuicao_garcons'},
    'ajuda': {'central_ajuda', 'detalhe_ajuda'},
}

ENDPOINT_TO_PAGINA = {
    endpoint: pagina
    for pagina, endpoints in PAGINA_ENDPOINTS.items()
    for endpoint in endpoints
}
