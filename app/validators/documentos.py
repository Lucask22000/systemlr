"""Validacoes de documentos pessoais."""

from app.utils.validators import validar_cpf


def validate_cpf(value):
    """Valida CPF no formato usado pelo dominio atual."""
    return validar_cpf(value)
