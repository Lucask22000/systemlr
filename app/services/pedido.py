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
