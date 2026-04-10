"""Validacoes basicas do dominio de vendas."""


class PedidoFiltroSchema:
    """Valida filtros simples de listagem de pedidos."""

    def validate(self, data):
        errors = {}
        status = (data.get('status') or '').strip().lower()
        if status and status not in {'aberto', 'em_preparo', 'entregue', 'fechado', 'cancelado'}:
            errors['status'] = 'Status de pedido invalido.'
        return (not errors), errors
