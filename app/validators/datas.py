"""Validadores de datas."""

from app.utils.validators import validar_data


def parse_date_iso(value):
    """Converte uma data ISO no padrao aceito pelo sistema."""
    return validar_data(value)
