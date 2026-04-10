"""Validadores do dominio de estoque."""

from app.utils.validators import normalizar_codigo_barras


def normalize_barcode(value):
    """Normaliza codigo de barras e reaproveita a regra legada."""
    return normalizar_codigo_barras(value)
