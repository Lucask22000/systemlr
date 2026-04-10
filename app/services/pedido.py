from datetime import datetime

from app.exceptions import BusinessRuleError, NotFound, ValidationError
from app.services.transaction import atomic_transaction
from app.services.workflow import transition_pedido_status
from models import Caixa, ItemPedido, Movimentacao, MovimentacaoCaixa, Pedido, Produto, db


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


def _processar_fechamento_pedido(pedido, *, failure_hook=None):
    with atomic_transaction():
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
            if failure_hook:
                failure_hook('after_stock')
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
            if failure_hook:
                failure_hook('after_cash')
            pedido.financeiro_processado = True

        pedido.fechado_em = datetime.utcnow()
        if pedido.mesa:
            pedido.mesa.status = 'livre'


def _aplicar_transicao_status(pedido, novo_status, *, actor=None, detalhes=None, require_delivery_separation=False):
    return transition_pedido_status(
        pedido,
        novo_status,
        actor=actor,
        detalhes=detalhes,
        require_delivery_separation=require_delivery_separation,
        on_fechamento=_processar_fechamento_pedido,
    )
