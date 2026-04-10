import re
from datetime import datetime

from app.services.utils import (
    _normalizar_contato,
    _sem_acentos,
    _slugify,
    _to_float,
    _to_int,
)


to_float = _to_float
to_int = _to_int
normalizar_contato = _normalizar_contato
sem_acentos = _sem_acentos
slugify = _slugify


def validar_float(valor, default=None):
    try:
        return _to_float(valor, default)
    except (TypeError, ValueError):
        return default


def validar_int(valor, default=None):
    try:
        return _to_int(valor, default)
    except (TypeError, ValueError):
        return default


def validar_data(valor, formato='%Y-%m-%d'):
    texto = str(valor or '').strip()
    if not texto:
        return None
    try:
        return datetime.strptime(texto, formato).date()
    except ValueError:
        return None


def validar_email(valor):
    texto = str(valor or '').strip().lower()
    if not texto:
        return None
    if re.fullmatch(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', texto):
        return texto
    return None


def validar_telefone(valor, *, minimo=10):
    digits = re.sub(r'[^0-9]+', '', str(valor or ''))
    if len(digits) < minimo:
        return None
    return digits


def validar_cpf(valor):
    digits = re.sub(r'[^0-9]+', '', str(valor or ''))
    if len(digits) != 11 or len(set(digits)) == 1:
        return None

    soma = sum(int(digits[i]) * (10 - i) for i in range(9))
    dv1 = (soma * 10 % 11) % 10
    soma = sum(int(digits[i]) * (11 - i) for i in range(10))
    dv2 = (soma * 10 % 11) % 10
    if digits[-2:] != f'{dv1}{dv2}':
        return None
    return digits


__all__ = [
    '_to_float',
    '_to_int',
    '_normalizar_contato',
    '_sem_acentos',
    '_slugify',
    'to_float',
    'to_int',
    'normalizar_contato',
    'sem_acentos',
    'slugify',
    'validar_float',
    'validar_int',
    'validar_data',
    'validar_email',
    'validar_telefone',
    'validar_cpf',
]
