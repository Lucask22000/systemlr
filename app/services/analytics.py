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
