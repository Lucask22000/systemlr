"""Validadores e normalizadores compartilhados."""


def normalize_text(value):
    """Normaliza texto livre para comparacoes simples."""
    return (value or '').strip().lower()
