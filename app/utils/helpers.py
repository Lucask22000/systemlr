import re
import unicodedata

from app.utils.data import parse_date_range


def sem_acentos(texto):
    base = unicodedata.normalize('NFKD', str(texto or ''))
    return ''.join(char for char in base if not unicodedata.combining(char))


def slugify(valor):
    texto = sem_acentos(valor)
    return re.sub(r'[^a-zA-Z0-9]+', '-', texto).strip('-').lower()


__all__ = ['sem_acentos', 'slugify', 'parse_date_range']
