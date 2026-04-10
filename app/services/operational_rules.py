from __future__ import annotations

from app.exceptions import BusinessRuleError, ValidationError
from app.services.master_data import (
    validate_cancel_reason_classified,
    validate_movement_reason_classified,
)
from models import LancamentoFinanceiro, Movimentacao


CRITICAL_FINANCIAL_TYPES = {
    LancamentoFinanceiro.TIPO_CONSUMO_PROPRIO,
    LancamentoFinanceiro.TIPO_DESPESA,
    LancamentoFinanceiro.TIPO_AJUSTE,
}


def require_cancel_reason(reason, *, entity_label='registro'):
    return validate_cancel_reason_classified(reason, entity_label=entity_label)


def validate_active_product_payload(
    *,
    codigo,
    nome,
    categoria_id,
    fornecedor_id,
    preco_custo,
    preco_venda,
    quantidade_minima,
    ativo=True,
):
    if not ativo:
        return
    if not (str(codigo or '').strip()):
        raise ValidationError('Produto ativo exige codigo.')
    if not (str(nome or '').strip()):
        raise ValidationError('Produto ativo exige nome.')
    if not categoria_id:
        raise ValidationError('Produto ativo exige categoria.')
    if not fornecedor_id:
        raise ValidationError('Produto ativo exige fornecedor.')
    if preco_custo is None or float(preco_custo) < 0:
        raise ValidationError('Produto ativo exige preco de custo valido.')
    if preco_venda is None or float(preco_venda) <= 0:
        raise ValidationError('Produto ativo exige preco de venda maior que zero.')
    if quantidade_minima is None or int(quantidade_minima) < 0:
        raise ValidationError('Produto ativo exige quantidade minima valida.')


def validate_stock_movement_payload(*, tipo, quantidade, motivo, recebimento_fornecedor=False):
    if tipo not in {Movimentacao.TIPO_ENTRADA, Movimentacao.TIPO_SAIDA, Movimentacao.TIPO_TRANSFERENCIA}:
        raise ValidationError('Tipo de movimentacao invalido.')
    if quantidade is None or int(quantidade) <= 0:
        raise ValidationError('Quantidade deve ser maior que zero.')
    motivo_normalizado = (motivo or '').strip().lower()
    if tipo == Movimentacao.TIPO_SAIDA and not motivo_normalizado:
        raise ValidationError('Saida de estoque exige motivo classificado.')
    if tipo == Movimentacao.TIPO_ENTRADA and not recebimento_fornecedor and not motivo_normalizado:
        raise ValidationError('Entrada manual exige motivo classificado.')
    if tipo in {Movimentacao.TIPO_SAIDA, Movimentacao.TIPO_TRANSFERENCIA}:
        return validate_movement_reason_classified(motivo, tipo=tipo)
    if tipo == Movimentacao.TIPO_ENTRADA:
        if recebimento_fornecedor:
            motivo_normalizado = (motivo or 'recebimento_fornecedor').strip().lower()
        else:
            motivo_normalizado = validate_movement_reason_classified(motivo, tipo=tipo)
        return motivo_normalizado
    return (motivo or '').strip().lower()


def validate_financial_entry_payload(*, tipo, referencia_documento, centro_custo):
    if tipo in CRITICAL_FINANCIAL_TYPES:
        if not (referencia_documento or '').strip():
            raise ValidationError('Lancamento financeiro critico exige referencia.')
        if not (centro_custo or '').strip():
            raise ValidationError('Lancamento financeiro critico exige centro de custo.')


def validate_stock_transfer_payload(*, produto, endereco_origem, endereco_destino, motivo):
    if not produto:
        raise ValidationError('Produto nao encontrado.')
    if not endereco_origem:
        raise ValidationError('Transferencia exige endereco de origem valido.')
    if not endereco_destino:
        raise ValidationError('Transferencia exige endereco de destino valido.')
    if endereco_origem.id == endereco_destino.id:
        raise BusinessRuleError('Origem e destino nao podem ser iguais.')
    validate_movement_reason_classified(motivo, tipo=Movimentacao.TIPO_TRANSFERENCIA)
