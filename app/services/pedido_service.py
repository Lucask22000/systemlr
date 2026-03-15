from app.services.pedido import (
    _aplicar_transicao_status,
    _normalizar_item_payload,
    _processar_fechamento_pedido,
    _recalcular_total_pedido,
)


normalizar_item_payload = _normalizar_item_payload
recalcular_total_pedido = _recalcular_total_pedido
processar_fechamento_pedido = _processar_fechamento_pedido
aplicar_transicao_status = _aplicar_transicao_status


__all__ = [
    '_normalizar_item_payload',
    '_recalcular_total_pedido',
    '_processar_fechamento_pedido',
    '_aplicar_transicao_status',
    'normalizar_item_payload',
    'recalcular_total_pedido',
    'processar_fechamento_pedido',
    'aplicar_transicao_status',
]
