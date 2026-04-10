from datetime import datetime, timedelta

from sqlalchemy.orm import selectinload

from models import Caixa, Garcom, ItemPedido, LancamentoFinanceiro, Pedido, Produto, db


FINANCIAL_CATEGORIES_OUTSIDE_OPERATING_RESULT = {
    'pagamento_fornecedor',
    'sangria',
    'fundo_operacional',
}


def construir_metricas_dashboard_vazias(inicio_periodo, fim_periodo, *, schema_inconsistente=False):
    """Retorna um payload seguro para manter o dashboard funcional em degradacao controlada."""
    periodo_dias = max((fim_periodo - inicio_periodo).days, 0)
    alertas = []
    if schema_inconsistente:
        alertas.append({
            'nivel': 'warning',
            'titulo': 'Analytics temporariamente indisponivel',
            'descricao': 'O schema do banco esta desatualizado em relacao ao codigo atual. Execute as migrations para restaurar os indicadores.',
        })

    comparativos_zerados = {
        'atual': 0.0,
        'anterior': 0.0,
        'variacao_pct': 0.0,
    }

    return {
        'periodo_dias': periodo_dias,
        'pedidos_periodo_total': 0,
        'faturamento_periodo': 0.0,
        'faturamento_periodo_anterior': 0.0,
        'crescimento_receita_pct': 0.0,
        'faturamento_hoje': 0.0,
        'receita_media_dia': 0.0,
        'pedidos_media_dia': 0.0,
        'ticket_medio_periodo': 0.0,
        'ticket_medio_periodo_anterior': 0.0,
        'tempo_medio_preparo_minutos': 0.0,
        'cmv_periodo': 0.0,
        'lucro_bruto_periodo': 0.0,
        'margem_bruta_pct': 0.0,
        'despesas_operacionais_periodo': 0.0,
        'despesas_operacionais_pct_faturamento': 0.0,
        'movimentacoes_financeiras_excluidas_periodo': 0.0,
        'categorias_excluidas_resultado': sorted(FINANCIAL_CATEGORIES_OUTSIDE_OPERATING_RESULT),
        'ajustes_financeiros_periodo': 0.0,
        'resultado_operacional_periodo': 0.0,
        'margem_operacional_pct': 0.0,
        'pedidos_abertos': 0,
        'pedidos_cancelados_periodo': 0,
        'valor_cancelado_periodo': 0.0,
        'taxa_cancelamento_pct': 0.0,
        'metodo_mais_usado': 'nao informado',
        'concentracao_top_pagamento_pct': 0.0,
        'comparativos': {
            'faturamento': dict(comparativos_zerados),
            'ticket_medio': dict(comparativos_zerados),
            'margem_bruta_pct': dict(comparativos_zerados),
            'margem_operacional_pct': dict(comparativos_zerados),
            'despesas_operacionais': dict(comparativos_zerados),
            'taxa_cancelamento_pct': dict(comparativos_zerados),
        },
        'vendas_periodo': [],
        'receita_vs_despesas': [],
        'margens_periodo': [],
        'margem_meta_pct': None,
        'cmv_vs_categorias': [{'categoria': 'CMV', 'valor': 0.0}],
        'top_produtos_vendidos': [],
        'pedidos_por_status': [],
        'top_clientes': [],
        'desempenho_garcons': [],
        'desempenho_caixas': [],
        'desempenho_operacional': [],
        'metodos_pagamento': [],
        'pendencias_lancamento': 0,
        'alertas': alertas,
    }


def _sum_financial_entries_by_types(inicio_periodo, fim_periodo, tipos, *, exclude_categories=None):
    query = db.session.query(
        db.func.sum(LancamentoFinanceiro.valor)
    ).filter(
        LancamentoFinanceiro.tipo.in_(tipos),
        LancamentoFinanceiro.data_competencia >= inicio_periodo.date(),
        LancamentoFinanceiro.data_competencia < fim_periodo.date()
    )
    categorias_excluidas = {str(item).strip().lower() for item in (exclude_categories or set()) if str(item).strip()}
    if categorias_excluidas:
        query = query.filter(
            db.or_(
                LancamentoFinanceiro.categoria.is_(None),
                db.func.lower(LancamentoFinanceiro.categoria).notin_(categorias_excluidas)
            )
        )
    return float(query.scalar() or 0.0)


def _pct_delta(current, previous):
    current = float(current or 0.0)
    previous = float(previous or 0.0)
    if previous == 0:
        return 0.0
    return ((current - previous) / previous) * 100.0


def _margin_pct(receita, valor):
    receita = float(receita or 0.0)
    valor = float(valor or 0.0)
    return (valor / receita * 100.0) if receita > 0 else 0.0


def _sum_financial_entries_by_category(inicio_periodo, fim_periodo, tipos):
    rows = db.session.query(
        LancamentoFinanceiro.categoria.label('categoria'),
        db.func.sum(LancamentoFinanceiro.valor).label('valor')
    ).filter(
        LancamentoFinanceiro.tipo.in_(tipos),
        LancamentoFinanceiro.data_competencia >= inicio_periodo.date(),
        LancamentoFinanceiro.data_competencia < fim_periodo.date()
    ).group_by(
        LancamentoFinanceiro.categoria
    ).order_by(
        db.desc('valor')
    ).all()
    return [
        {
            'categoria': item.categoria or 'Sem categoria',
            'valor': float(item.valor or 0.0),
        }
        for item in rows
    ]


def calcular_metricas_dashboard(inicio_periodo, fim_periodo):
    """Calcula metricas agregadas do dashboard no intervalo informado."""
    inicio_hoje = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    fim_hoje = inicio_hoje + timedelta(days=1)
    periodo_dias = (fim_periodo - inicio_periodo).days

    pedidos_periodo = Pedido.query.options(
        selectinload(Pedido.itens).selectinload(ItemPedido.produto)
    ).filter(
        Pedido.status == 'fechado',
        Pedido.fechado_em >= inicio_periodo,
        Pedido.fechado_em < fim_periodo
    ).all()
    pedidos_periodo_total = len(pedidos_periodo)
    faturamento_periodo = sum((pedido.total or 0) for pedido in pedidos_periodo)
    ticket_medio_periodo = (faturamento_periodo / pedidos_periodo_total) if pedidos_periodo_total else 0
    tempos_preparo_segundos = [
        max((pedido.fechado_em - pedido.criado_em).total_seconds(), 0)
        for pedido in pedidos_periodo
        if pedido.criado_em and pedido.fechado_em
    ]
    tempo_medio_preparo_minutos = (
        sum(tempos_preparo_segundos) / len(tempos_preparo_segundos) / 60.0
        if tempos_preparo_segundos else 0.0
    )

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

    despesas_operacionais_periodo = _sum_financial_entries_by_types(
        inicio_periodo,
        fim_periodo,
        [
            LancamentoFinanceiro.TIPO_DESPESA,
            LancamentoFinanceiro.TIPO_CONSUMO_PROPRIO
        ],
        exclude_categories=FINANCIAL_CATEGORIES_OUTSIDE_OPERATING_RESULT,
    )

    movimentacoes_financeiras_excluidas_periodo = _sum_financial_entries_by_types(
        inicio_periodo,
        fim_periodo,
        [
            LancamentoFinanceiro.TIPO_DESPESA,
            LancamentoFinanceiro.TIPO_CONSUMO_PROPRIO
        ],
    ) - despesas_operacionais_periodo

    ajustes_financeiros_periodo = _sum_financial_entries_by_types(
        inicio_periodo,
        fim_periodo,
        [LancamentoFinanceiro.TIPO_AJUSTE],
    )

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
    pedidos_periodo_anterior = Pedido.query.filter(
        Pedido.status == 'fechado',
        Pedido.fechado_em >= periodo_anterior_inicio,
        Pedido.fechado_em < periodo_anterior_fim
    ).count()

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

    despesas_diarias_raw = db.session.query(
        LancamentoFinanceiro.data_competencia.label('dia'),
        db.func.sum(LancamentoFinanceiro.valor).label('valor')
    ).filter(
        LancamentoFinanceiro.tipo.in_([
            LancamentoFinanceiro.TIPO_DESPESA,
            LancamentoFinanceiro.TIPO_CONSUMO_PROPRIO,
        ]),
        LancamentoFinanceiro.data_competencia >= inicio_periodo.date(),
        LancamentoFinanceiro.data_competencia < fim_periodo.date()
    ).group_by(
        LancamentoFinanceiro.data_competencia
    ).all()
    despesas_diarias_map = {
        str(item.dia): float(item.valor or 0.0)
        for item in despesas_diarias_raw
    }

    vendas_periodo = []
    for i in range(periodo_dias):
        dia = inicio_periodo + timedelta(days=i)
        chave_dia = dia.strftime('%Y-%m-%d')
        valores_dia = vendas_periodo_map.get(chave_dia, {'faturamento': 0.0, 'pedidos': 0})
        despesa_dia = float(despesas_diarias_map.get(chave_dia, 0.0))
        faturamento_dia = float(valores_dia['faturamento'])
        cmv_estimado_dia = (cmv_periodo / faturamento_periodo * faturamento_dia) if faturamento_periodo > 0 else 0.0
        lucro_bruto_dia = faturamento_dia - cmv_estimado_dia
        resultado_operacional_dia = lucro_bruto_dia - despesa_dia
        vendas_periodo.append({
            'data_iso': chave_dia,
            'data_curta': dia.strftime('%d/%m'),
            'data_semana': dia.strftime('%a'),
            'faturamento': faturamento_dia,
            'pedidos': valores_dia['pedidos'],
            'despesas': despesa_dia,
            'margem_bruta_pct': _margin_pct(faturamento_dia, lucro_bruto_dia),
            'margem_operacional_pct': _margin_pct(faturamento_dia, resultado_operacional_dia),
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
            'sku': produto.codigo,
            'nome': produto.nome,
            'quantidade': int(qtd or 0),
            'receita': float(receita or 0),
            'margem_contribuicao': float(((produto.preco_venda or 0.0) - (produto.preco_custo or 0.0)) / (produto.preco_venda or 1.0)) if produto.preco_venda else 0.0,
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
            'faturamento': float(item.faturamento or 0),
            'ticket_medio': float((item.faturamento or 0) / item.pedidos) if item.pedidos else 0.0,
            'tipo': 'Garcom',
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
            'faturamento': float(item.faturamento or 0),
            'ticket_medio': float((item.faturamento or 0) / item.pedidos) if item.pedidos else 0.0,
            'tipo': 'Caixa',
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

    cmv_vs_categorias = [{'categoria': 'CMV', 'valor': float(cmv_periodo)}]
    cmv_vs_categorias.extend(
        _sum_financial_entries_by_category(
            inicio_periodo,
            fim_periodo,
            [LancamentoFinanceiro.TIPO_DESPESA, LancamentoFinanceiro.TIPO_CONSUMO_PROPRIO]
        )[:6]
    )

    desempenho_operacional = sorted(
        desempenho_garcons + desempenho_caixas,
        key=lambda item: (item['faturamento'], item['pedidos']),
        reverse=True
    )[:8]

    pendencias_lancamento = Pedido.query.filter(
        Pedido.status == Pedido.STATUS_FECHADO,
        Pedido.fechado_em >= inicio_periodo,
        Pedido.fechado_em < fim_periodo,
        db.or_(
            Pedido.financeiro_processado.is_(False),
            Pedido.financeiro_processado.is_(None),
        )
    ).count()

    alertas = []
    if margem_bruta_pct < 25:
        alertas.append({
            'nivel': 'danger',
            'titulo': 'Margem bruta abaixo do esperado',
            'descricao': f'Margem bruta atual em {margem_bruta_pct:.1f}% no periodo analisado.',
        })
    if taxa_cancelamento_pct >= 5:
        alertas.append({
            'nivel': 'warning',
            'titulo': 'Cancelamento acima do limite',
            'descricao': f'{pedidos_cancelados_periodo} pedido(s) cancelado(s), taxa de {taxa_cancelamento_pct:.1f}%.',
        })
    despesas_pct_faturamento = _margin_pct(faturamento_periodo, despesas_operacionais_periodo)
    if despesas_pct_faturamento >= 30:
        alertas.append({
            'nivel': 'warning',
            'titulo': 'Despesas operacionais elevadas',
            'descricao': f'Despesas consumindo {despesas_pct_faturamento:.1f}% do faturamento.',
        })
    if pendencias_lancamento:
        alertas.append({
            'nivel': 'info',
            'titulo': 'Pendencias de lancamento financeiro',
            'descricao': f'{pendencias_lancamento} pedido(s) fechado(s) ainda nao processado(s) no financeiro.',
        })

    ticket_medio_anterior = (
        float(faturamento_periodo_anterior) / pedidos_periodo_anterior
        if pedidos_periodo_anterior and faturamento_periodo_anterior else 0.0
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
        'ticket_medio_periodo_anterior': float(ticket_medio_anterior),
        'tempo_medio_preparo_minutos': float(tempo_medio_preparo_minutos),
        'cmv_periodo': float(cmv_periodo),
        'lucro_bruto_periodo': float(lucro_bruto_periodo),
        'margem_bruta_pct': float(margem_bruta_pct),
        'despesas_operacionais_periodo': float(despesas_operacionais_periodo),
        'despesas_operacionais_pct_faturamento': float(despesas_pct_faturamento),
        'movimentacoes_financeiras_excluidas_periodo': float(movimentacoes_financeiras_excluidas_periodo),
        'categorias_excluidas_resultado': sorted(FINANCIAL_CATEGORIES_OUTSIDE_OPERATING_RESULT),
        'ajustes_financeiros_periodo': float(ajustes_financeiros_periodo),
        'resultado_operacional_periodo': float(resultado_operacional_periodo),
        'margem_operacional_pct': float(margem_operacional_pct),
        'pedidos_abertos': int(pedidos_abertos),
        'pedidos_cancelados_periodo': int(pedidos_cancelados_periodo),
        'valor_cancelado_periodo': float(valor_cancelado_periodo),
        'taxa_cancelamento_pct': float(taxa_cancelamento_pct),
        'metodo_mais_usado': metodo_mais_usado,
        'concentracao_top_pagamento_pct': float(concentracao_top_pagamento_pct),
        'comparativos': {
            'faturamento': {
                'atual': float(faturamento_periodo),
                'anterior': float(faturamento_periodo_anterior),
                'variacao_pct': float(_pct_delta(faturamento_periodo, faturamento_periodo_anterior)),
            },
            'ticket_medio': {
                'atual': float(ticket_medio_periodo),
                'anterior': float(ticket_medio_anterior),
                'variacao_pct': float(_pct_delta(ticket_medio_periodo, ticket_medio_anterior)),
            },
            'margem_bruta_pct': {
                'atual': float(margem_bruta_pct),
                'anterior': 0.0,
                'variacao_pct': 0.0,
            },
            'margem_operacional_pct': {
                'atual': float(margem_operacional_pct),
                'anterior': 0.0,
                'variacao_pct': 0.0,
            },
            'despesas_operacionais': {
                'atual': float(despesas_operacionais_periodo),
                'anterior': 0.0,
                'variacao_pct': 0.0,
            },
            'taxa_cancelamento_pct': {
                'atual': float(taxa_cancelamento_pct),
                'anterior': 0.0,
                'variacao_pct': 0.0,
            },
        },
        'vendas_periodo': vendas_periodo,
        'receita_vs_despesas': vendas_periodo,
        'margens_periodo': vendas_periodo,
        'margem_meta_pct': None,
        'cmv_vs_categorias': cmv_vs_categorias,
        'top_produtos_vendidos': top_produtos_vendidos,
        'pedidos_por_status': pedidos_por_status,
        'top_clientes': top_clientes,
        'desempenho_garcons': desempenho_garcons,
        'desempenho_caixas': desempenho_caixas,
        'desempenho_operacional': desempenho_operacional,
        'metodos_pagamento': metodos_pagamento,
        'pendencias_lancamento': int(pendencias_lancamento),
        'alertas': alertas,
    }
