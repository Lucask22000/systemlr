import re
from datetime import datetime


def validar_cpf(cpf):
    digitos = re.sub(r'\D', '', str(cpf or ''))
    if not digitos:
        return None
    if len(digitos) != 11:
        return '__invalid__'
    return f'{digitos[:3]}.{digitos[3:6]}.{digitos[6:9]}-{digitos[9:]}'


def validar_cnpj(cnpj):
    digitos = re.sub(r'\D', '', str(cnpj or ''))
    if not digitos:
        return None
    return digitos if len(digitos) == 14 else '__invalid__'


def validar_email(email):
    texto = str(email or '').strip().lower()
    if not texto:
        return None
    if re.fullmatch(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', texto):
        return texto
    return None


def validar_telefone(telefone):
    digitos = re.sub(r'[^0-9]+', '', str(telefone or ''))
    return digitos if len(digitos) >= 10 else None


def validar_cep(cep):
    digitos = re.sub(r'[^0-9]+', '', str(cep or ''))
    if not digitos:
        return None
    return digitos if len(digitos) == 8 else '__invalid__'


def validar_data(data_str):
    texto = str(data_str or '').strip()
    if not texto:
        return None
    try:
        return datetime.strptime(texto, '%Y-%m-%d').date()
    except ValueError:
        return None


def validar_float(valor):
    if valor is None or valor == '':
        return None
    try:
        return float(str(valor).replace(',', '.').strip())
    except (TypeError, ValueError):
        return None


def validar_int(valor):
    if valor is None or valor == '':
        return None
    try:
        return int(valor)
    except (TypeError, ValueError):
        return None


def normalizar_matricula(valor):
    matricula = re.sub(r'[^A-Z0-9]+', '', str(valor or '').strip().upper())
    return matricula or None


def _ean13_digito_verificador(base12):
    soma_impares = sum(int(base12[i]) for i in range(0, 12, 2))
    soma_pares = sum(int(base12[i]) for i in range(1, 12, 2))
    total = soma_impares + (soma_pares * 3)
    return str((10 - (total % 10)) % 10)


def normalizar_codigo_barras(codigo):
    digits = re.sub(r'\D', '', str(codigo or '').strip())
    if len(digits) == 12:
        digits = f'0{digits}'
    if len(digits) != 13:
        return None, 'Codigo de barras deve seguir EAN-13 (13 digitos numericos).'
    esperado = _ean13_digito_verificador(digits[:12])
    if digits[-1] != esperado:
        return None, 'Codigo de barras EAN-13 invalido (digito verificador incorreto).'
    return digits, None


__all__ = [
    'validar_cpf',
    'validar_cnpj',
    'validar_email',
    'validar_telefone',
    'validar_cep',
    'validar_data',
    'validar_float',
    'validar_int',
    'normalizar_matricula',
    'normalizar_codigo_barras',
]
