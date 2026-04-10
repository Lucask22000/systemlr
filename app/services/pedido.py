from app.exceptions import BusinessRuleError, ValidationError
from app.services.traceability import record_process_event
from app.services.venda_service import VendaService
from app.services.workflow import transition_pedido_status
from models import ItemPedido, Pedido, Produto, db


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
    if produto.vencido:
        raise ValidationError(f'Produto "{produto.nome}" esta vencido e nao pode entrar no pedido.')
    return {'produto': produto, 'quantidade': quantidade}, None


def _recalcular_total_pedido(pedido):
    pedido.total = sum((item.quantidade or 0) * (item.preco_unitario or 0) for item in pedido.itens)
    return pedido.total


def _substituir_itens_pedido(
    pedido,
    itens_payload,
    *,
    normalizar_item_payload=_normalizar_item_payload,
    item_model=ItemPedido,
    clear_existing=True,
    empty_items_message='Adicione ao menos um item valido ao pedido.',
):
    if clear_existing:
        pedido.itens.clear()

    itens_validos = 0
    for item in itens_payload:
        normalizado, erro = normalizar_item_payload(item)
        if erro:
            continue

        produto = normalizado['produto']
        quantidade = normalizado['quantidade']
        pedido.itens.append(
            item_model(
                produto_id=produto.id,
                quantidade=quantidade,
                preco_unitario=produto.preco_venda,
            )
        )
        itens_validos += 1

    if itens_validos == 0:
        raise ValidationError(empty_items_message)

    return itens_validos


def create_order(
    *,
    caixa,
    itens_payload,
    mesa=None,
    garcom_id=None,
    atendimento_mesas_ativo=False,
    pedido_model=Pedido,
    totalizer=_recalcular_total_pedido,
    normalizar_item_payload=_normalizar_item_payload,
    empty_items_message='Adicione ao menos um item valido ao pedido.',
    actor=None,
):
    if not caixa or not caixa.aberto:
        raise BusinessRuleError('Caixa nao esta aberta.')
    if not itens_payload:
        raise ValidationError('Caixa e produtos sao obrigatorios.')

    pedido = pedido_model(
        mesa_id=(mesa.id if atendimento_mesas_ativo and mesa else None),
        caixa_id=caixa.id,
        garcom_id=(garcom_id if atendimento_mesas_ativo else None),
        status=Pedido.STATUS_ABERTO,
        estoque_processado=False,
        financeiro_processado=False,
    )
    db.session.add(pedido)
    db.session.flush()

    _substituir_itens_pedido(
        pedido,
        itens_payload,
        normalizar_item_payload=normalizar_item_payload,
        clear_existing=False,
        empty_items_message=empty_items_message,
    )
    totalizer(pedido)

    if atendimento_mesas_ativo and mesa:
        mesa.status = 'ocupada'

    record_process_event(
        processo_tipo='pedido_venda',
        etapa='criacao',
        acao='pedido_criado',
        entidade='pedido',
        entidade_id=pedido.id,
        pedido_id=pedido.id,
        actor=actor,
        detalhes={
            'status': pedido.status,
            'total': float(pedido.total or 0.0),
            'mesa_id': pedido.mesa_id,
            'caixa_id': pedido.caixa_id,
        },
    )

    return pedido


def update_order(
    pedido,
    *,
    novo_status,
    caixa=None,
    mesa=None,
    atendimento_mesas_ativo=False,
    observacoes=None,
    itens_payload=None,
    metodo_pagamento=None,
    valor_pago=None,
    actor=None,
    detalhes=None,
    require_delivery_separation=False,
    normalizar_item_payload=_normalizar_item_payload,
    totalizer=_recalcular_total_pedido,
    status_transition=None,
    empty_items_message='Adicione ao menos um item valido ao pedido.',
):
    if status_transition is None:
        status_transition = _aplicar_transicao_status
    status_atual = (pedido.status or Pedido.STATUS_ABERTO).strip().lower()
    novo_status = (novo_status or status_atual).strip().lower()

    if status_atual in Pedido.STATUS_IMUTAVEIS and novo_status != status_atual:
        raise ValidationError(f'Pedido {status_atual} e imutavel.')

    pedido.mesa_id = (mesa.id if atendimento_mesas_ativo and mesa else None)
    if not atendimento_mesas_ativo:
        pedido.garcom_id = None
    pedido.caixa_id = caixa.id if caixa else None
    pedido.observacoes = observacoes

    if caixa and novo_status == Pedido.STATUS_FECHADO and not caixa.aberto:
        raise ValidationError('Caixa informada esta fechada.')

    if status_atual not in Pedido.STATUS_IMUTAVEIS:
        _substituir_itens_pedido(
            pedido,
            itens_payload or [],
            normalizar_item_payload=normalizar_item_payload,
            empty_items_message=empty_items_message,
        )
        totalizer(pedido)

    pedido.metodo_pagamento = metodo_pagamento
    pedido.valor_pago = valor_pago

    status_transition(
        pedido,
        novo_status,
        actor=actor,
        detalhes=detalhes,
        require_delivery_separation=require_delivery_separation,
    )
    return pedido


def _processar_fechamento_pedido(pedido, *, actor=None, failure_hook=None):
    VendaService(session=db.session).processar_venda_rapida(
        pedido,
        metodo_pagamento=pedido.metodo_pagamento,
        valor_pago=pedido.valor_pago,
        actor=actor,
        commit=False,
        failure_hook=failure_hook,
    )


def _aplicar_transicao_status(pedido, novo_status, *, actor=None, detalhes=None, require_delivery_separation=False):
    return transition_pedido_status(
        pedido,
        novo_status,
        actor=actor,
        detalhes=detalhes,
        require_delivery_separation=require_delivery_separation,
        on_fechamento=lambda item: _processar_fechamento_pedido(item, actor=actor),
    )
