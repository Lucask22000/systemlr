import re
import unicodedata


def _to_float(valor, default=None):
    if valor is None or valor == '':
        return default
    if isinstance(valor, str):
        valor = valor.replace(',', '.').strip()
    return float(valor)


def _to_int(valor, default=None):
    if valor is None or valor == '':
        return default
    return int(valor)


def _sem_acentos(texto):
    base = unicodedata.normalize('NFKD', str(texto or ''))
    return ''.join(char for char in base if not unicodedata.combining(char))


def _slugify(value):
    texto = _sem_acentos(value)
    texto = re.sub(r'[^a-zA-Z0-9]+', '-', texto).strip('-').lower()
    return texto


def _normalizar_contato(valor):
    texto = (valor or '').strip()
    if not texto:
        return None
    return re.sub(r'\s+', ' ', texto)
