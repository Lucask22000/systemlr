"""Montagem de menu e diagnositco de navegacao.

Extracao do bloco de menu de app/__init__.py para reduzir acoplamento.
"""

from flask import current_app, has_request_context, request, url_for

from app.constants import PAGINAS_SISTEMA, PAGINAS_SISTEMA_MENU_ORDEM


def paginas_ordenadas_menu():
    paginas_ordenadas = []
    for secao_nome, secao_paginas in PAGINAS_SISTEMA_MENU_ORDEM:
        itens_secao = [
            (pagina_key, PAGINAS_SISTEMA[pagina_key])
            for pagina_key in secao_paginas
            if pagina_key in PAGINAS_SISTEMA
        ]
        if itens_secao:
            paginas_ordenadas.append((secao_nome, itens_secao))
    return paginas_ordenadas


def menu_agrupado_para_paginas(paginas_permitidas):
    paginas_permitidas = set(paginas_permitidas or [])
    menu_agrupado = []
    for secao_nome, secao_paginas in PAGINAS_SISTEMA_MENU_ORDEM:
        itens_secao = [
            {
                'key': pagina_key,
                'label': PAGINAS_SISTEMA[pagina_key],
            }
            for pagina_key in secao_paginas
            if pagina_key in paginas_permitidas and pagina_key in PAGINAS_SISTEMA
        ]
        if itens_secao:
            menu_agrupado.append({
                'secao': secao_nome,
                'paginas': itens_secao,
            })
    return menu_agrupado


def url_for_safe(endpoint, **values):
    try:
        return url_for(endpoint, **values)
    except Exception:
        return '#'


def item_menu_interno(*, label, endpoint, page_keys, current_page_key=None, visible=True):
    if not visible:
        return None
    page_keys = tuple(page_keys or ())
    current = bool(current_page_key and current_page_key in page_keys)
    return {
        'label': label,
        'url': url_for_safe(endpoint),
        'current': current,
        'page_keys': page_keys,
    }


def menu_navegacao_principal(
    funcionario,
    *,
    resolver_paginas_permitidas,
    empresa_config=None,
    atendimento_mesas_ativo=True,
    current_page_key=None,
):
    paginas_permitidas = resolver_paginas_permitidas(funcionario)
    menu = []

    definicoes = [
        {
            'id': 'gestao',
            'label': 'Gestão',
            'icon': 'management',
            'items': [
                item_menu_interno(label='Central do Negócio', endpoint='gestao_negocio', page_keys=('gestao_negocio',), current_page_key=current_page_key, visible='gestao_negocio' in paginas_permitidas),
                item_menu_interno(label='Empresa', endpoint='editar_empresa', page_keys=('empresa',), current_page_key=current_page_key, visible='empresa' in paginas_permitidas),
            ],
        },
        {
            'id': 'financeiro',
            'label': 'Financeiro',
            'icon': 'finance',
            'items': [
                item_menu_interno(label='Visão Financeira', endpoint='financeiro', page_keys=('financeiro',), current_page_key=current_page_key, visible='financeiro' in paginas_permitidas),
                item_menu_interno(label='Lançamentos Contábeis', endpoint='financeiro_lancamentos', page_keys=('financeiro',), current_page_key=current_page_key, visible='financeiro' in paginas_permitidas),
                item_menu_interno(label='Gestão Monetária e Fundos', endpoint='financeiro_fundos', page_keys=('financeiro',), current_page_key=current_page_key, visible='financeiro' in paginas_permitidas),
            ],
        },
        {
            'id': 'vendas',
            'label': 'Vendas',
            'icon': 'sales',
            'items': [
                item_menu_interno(label='PDV', endpoint='pdv', page_keys=('pdv',), current_page_key=current_page_key, visible='pdv' in paginas_permitidas),
                item_menu_interno(label='Pedidos', endpoint='listar_pedidos', page_keys=('pedidos',), current_page_key=current_page_key, visible='pedidos' in paginas_permitidas),
                item_menu_interno(label='Mesas', endpoint='listar_mesas', page_keys=('mesas',), current_page_key=current_page_key, visible=atendimento_mesas_ativo and 'mesas' in paginas_permitidas),
                item_menu_interno(label='Caixas', endpoint='listar_caixas', page_keys=('caixas',), current_page_key=current_page_key, visible='caixas' in paginas_permitidas),
                item_menu_interno(label='Garçons', endpoint='listar_garcons', page_keys=('garcons',), current_page_key=current_page_key, visible=atendimento_mesas_ativo and 'garcons' in paginas_permitidas),
            ],
        },
        {
            'id': 'estoque',
            'label': 'Estoque',
            'icon': 'inventory',
            'items': [
                item_menu_interno(label='Produtos', endpoint='listar_produtos', page_keys=('produtos',), current_page_key=current_page_key, visible='produtos' in paginas_permitidas),
                item_menu_interno(label='Etiquetas de Loja', endpoint='imprimir_etiquetas_loja', page_keys=('produtos',), current_page_key=current_page_key, visible='produtos' in paginas_permitidas and (not empresa_config or empresa_config.emissao_etiqueta_loja_ativa is not False)),
                item_menu_interno(label='Estoques', endpoint='listar_estoques', page_keys=('estoques',), current_page_key=current_page_key, visible='estoques' in paginas_permitidas),
                item_menu_interno(label='Categorias', endpoint='listar_categorias', page_keys=('categorias',), current_page_key=current_page_key, visible='categorias' in paginas_permitidas),
                item_menu_interno(label='Endereços de Estoque', endpoint='listar_enderecos_estoque', page_keys=('enderecos_estoque',), current_page_key=current_page_key, visible='enderecos_estoque' in paginas_permitidas),
                item_menu_interno(label='Equipamentos', endpoint='listar_equipamentos_movimentacao', page_keys=('equipamentos_estoque',), current_page_key=current_page_key, visible='equipamentos_estoque' in paginas_permitidas),
                item_menu_interno(label='Endereços Inteligentes', endpoint='enderecos_inteligentes', page_keys=('enderecos_inteligentes',), current_page_key=current_page_key, visible='enderecos_inteligentes' in paginas_permitidas),
                item_menu_interno(label='Etiquetas de Endereço', endpoint='imprimir_etiquetas_enderecos_estoque', page_keys=('enderecos_estoque',), current_page_key=current_page_key, visible='enderecos_estoque' in paginas_permitidas and (not empresa_config or empresa_config.emissao_etiqueta_endereco_ativa is not False)),
                item_menu_interno(label='Entradas e Saídas Internas', endpoint='listar_movimentacoes', page_keys=('movimentacoes',), current_page_key=current_page_key, visible='movimentacoes' in paginas_permitidas),
                item_menu_interno(label='Almoxarifado', endpoint='listar_almoxarifado', page_keys=('almoxarifado',), current_page_key=current_page_key, visible='almoxarifado' in paginas_permitidas),
                item_menu_interno(label='Relatórios', endpoint='relatorios', page_keys=('relatorios',), current_page_key=current_page_key, visible='relatorios' in paginas_permitidas),
            ],
        },
        {
            'id': 'recebimento',
            'label': 'Recebimento',
            'icon': 'receiving',
            'items': [
                item_menu_interno(label='Central de Recebimentos', endpoint='listar_recebimentos_fornecedor', page_keys=('recebimentos',), current_page_key=current_page_key, visible='recebimentos' in paginas_permitidas),
                item_menu_interno(label='Novo Recebimento', endpoint='novo_recebimento_fornecedor', page_keys=('recebimentos',), current_page_key=current_page_key, visible='recebimentos' in paginas_permitidas),
                item_menu_interno(label='Fornecedores', endpoint='listar_fornecedores', page_keys=('fornecedores',), current_page_key=current_page_key, visible='fornecedores' in paginas_permitidas),
            ],
        },
        {
            'id': 'expedicao',
            'label': 'Expedição',
            'icon': 'shipping',
            'items': [
                item_menu_interno(label='Central de Expedição', endpoint='central_expedicao', page_keys=('expedicao',), current_page_key=current_page_key, visible='expedicao' in paginas_permitidas),
                item_menu_interno(label='Separação e Entrega', endpoint='listar_separacao_entrega', page_keys=('expedicao',), current_page_key=current_page_key, visible='expedicao' in paginas_permitidas),
                item_menu_interno(label='Roteirização', endpoint='listar_roteirizacao_entrega', page_keys=('expedicao',), current_page_key=current_page_key, visible='expedicao' in paginas_permitidas),
                item_menu_interno(label='Painel em Tempo Real', endpoint='painel_expedicao', page_keys=('expedicao',), current_page_key=current_page_key, visible='expedicao' in paginas_permitidas),
                item_menu_interno(label='Coletor Operacional', endpoint='coletor_estoque', page_keys=('expedicao',), current_page_key=current_page_key, visible='expedicao' in paginas_permitidas),
                item_menu_interno(label='Frota Própria e Terceiros', endpoint='frota_expedicao', page_keys=('expedicao',), current_page_key=current_page_key, visible='expedicao' in paginas_permitidas),
                item_menu_interno(label='Histórico de Transferências', endpoint='listar_transferencias_estoque', page_keys=('transferencias_estoque',), current_page_key=current_page_key, visible='transferencias_estoque' in paginas_permitidas),
                item_menu_interno(label='Nova Transferência entre Lojas/CDs', endpoint='transferir_armazenamento', page_keys=('transferencias_estoque',), current_page_key=current_page_key, visible='transferencias_estoque' in paginas_permitidas),
            ],
        },
        {
            'id': 'meu-rh',
            'label': 'Meu RH',
            'icon': 'hr',
            'items': [
                item_menu_interno(label='Indicadores RH', endpoint='indicadores_rh', page_keys=('rh_indicadores',), current_page_key=current_page_key, visible='rh_indicadores' in paginas_permitidas),
                item_menu_interno(label='Organograma', endpoint='organograma_rh', page_keys=('rh_organograma',), current_page_key=current_page_key, visible='rh_organograma' in paginas_permitidas),
                item_menu_interno(label='Funcionários', endpoint='listar_funcionarios', page_keys=('funcionarios',), current_page_key=current_page_key, visible='funcionarios' in paginas_permitidas),
                item_menu_interno(label='Cargos', endpoint='listar_funcoes_rh', page_keys=('rh_funcoes',), current_page_key=current_page_key, visible='rh_funcoes' in paginas_permitidas),
                item_menu_interno(label='Perfis de Acesso', endpoint='listar_perfis_rh', page_keys=('rh_funcoes',), current_page_key=current_page_key, visible='rh_funcoes' in paginas_permitidas),
                item_menu_interno(label='Auditoria', endpoint='auditoria_sistema', page_keys=('auditoria',), current_page_key=current_page_key, visible='auditoria' in paginas_permitidas),
            ],
        },
        {
            'id': 'ecommerce',
            'label': 'E-commerce',
            'icon': 'ecommerce',
            'items': [
                item_menu_interno(label='Ativação da Loja', endpoint='configurar_ativacao_ecommerce', page_keys=('ecommerce_config',), current_page_key=current_page_key, visible='ecommerce_config' in paginas_permitidas),
                item_menu_interno(label='Tema e Loja Online', endpoint='configurar_ecommerce', page_keys=('ecommerce_config',), current_page_key=current_page_key, visible='ecommerce_config' in paginas_permitidas),
                item_menu_interno(label='Marketing, Campanhas e Cupons', endpoint='configurar_marketing_ecommerce', page_keys=('ecommerce_marketing',), current_page_key=current_page_key, visible='ecommerce_marketing' in paginas_permitidas),
            ],
        },
        {
            'id': 'servicos',
            'label': 'Serviços',
            'icon': 'services',
            'items': [
                item_menu_interno(label='Chamados Internos', endpoint='listar_chamados_internos', page_keys=('chamados_internos',), current_page_key=current_page_key, visible='chamados_internos' in paginas_permitidas),
                item_menu_interno(label='Minhas Ordens', endpoint='minhas_ordens_servico', page_keys=('servicos_tecnicos',), current_page_key=current_page_key, visible='servicos_tecnicos' in paginas_permitidas),
                item_menu_interno(label='Ordens de Serviço', endpoint='listar_ordens_servico', page_keys=('servicos_tecnicos',), current_page_key=current_page_key, visible='servicos_tecnicos' in paginas_permitidas),
            ],
        },
        {
            'id': 'ajuda',
            'label': 'Ajuda',
            'icon': 'help',
            'items': [
                item_menu_interno(label='Guia do Sistema', endpoint='central_ajuda', page_keys=('ajuda',), current_page_key=current_page_key, visible='ajuda' in paginas_permitidas),
            ],
        },
    ]

    for grupo in definicoes:
        itens = [item for item in grupo['items'] if item]
        if not itens:
            continue
        menu.append({
            'id': grupo['id'],
            'label': grupo['label'],
            'icon': grupo['icon'],
            'items': itens,
            'current': any(item['current'] for item in itens),
        })
    return menu


def registrar_debug_menu(funcionario, paginas_permitidas, menu_agrupado=None, *, resolver_menu_agrupado=None):
    if not funcionario or not current_app.config.get('MENU_DEBUG_ENABLED'):
        return
    if not has_request_context():
        return

    if menu_agrupado is None:
        resolver = resolver_menu_agrupado or menu_agrupado_para_paginas
        menu_agrupado = resolver(paginas_permitidas)

    secoes_resumo = {
        item['secao']: [pagina['key'] for pagina in item['paginas']]
        for item in menu_agrupado
    }
    current_app.logger.info(
        'menu_debug funcionario_id=%s role=%s controle=%s perfil_acesso_id=%s endpoint=%s paginas=%s secoes=%s',
        getattr(funcionario, 'id', None),
        getattr(funcionario, 'role', None),
        getattr(funcionario, 'controle_acesso_ativo', None),
        getattr(funcionario, 'perfil_acesso_id', None),
        request.endpoint,
        sorted(set(paginas_permitidas or [])),
        secoes_resumo,
    )
