import re
import unicodedata
from dataclasses import dataclass
from typing import Iterable


@dataclass
class EnderecoCodigoConfig:
    zonas_permitidas: set[str]
    permitir_nivel_zero: bool = True
    separador: str = '-'


DEFAULT_ZONAS_PERMITIDAS = {'ZP', 'ZR', 'ZQ', 'ZD'}
_CONFIG = EnderecoCodigoConfig(zonas_permitidas=set(DEFAULT_ZONAS_PERMITIDAS), permitir_nivel_zero=True, separador='-')

_REGEX_CODIGO = re.compile(
    r'^CD(?P<cd>\d{2})-(?P<zona>Z[A-Z0-9]{1,2})-R(?P<rua>\d{2})-RK(?P<rack>\d{2})-N(?P<nivel>\d{2})-V(?P<vao>\d{2})-(?P<lado>L[A-Z0-9]{1,2})$'
)

_MAPA_LADO = {
    'A': 'LA',
    'B': 'LB',
    'LA': 'LA',
    'LB': 'LB',
    'E': 'LA',
    'ESQ': 'LA',
    'ESQUERDA': 'LA',
    'D': 'LB',
    'DIR': 'LB',
    'DIREITA': 'LB',
}


def configurar_endereco(*, zonas_permitidas: Iterable[str] | None = None, permitir_nivel_zero: bool | None = None):
    if zonas_permitidas is not None:
        normalizadas = set()
        for z in zonas_permitidas:
            zona_norm = _normalizar_zona(z, validar_permitidas=False)
            normalizadas.add(zona_norm)
        _CONFIG.zonas_permitidas = normalizadas
    if permitir_nivel_zero is not None:
        _CONFIG.permitir_nivel_zero = bool(permitir_nivel_zero)


def _normalizar_codigo_texto(codigo: str) -> str:
    texto = (codigo or '').strip().upper()
    texto = re.sub(r'[\s_]+', '-', texto)
    texto = re.sub(r'-{2,}', '-', texto)
    return texto


def _normalizar_numero(nome_campo: str, valor, *, minimo: int, maximo: int = 99) -> int:
    if valor is None or str(valor).strip() == '':
        raise ValueError(f'Campo "{nome_campo}" obrigatorio.')
    try:
        numero = int(str(valor).strip())
    except (TypeError, ValueError):
        raise ValueError(f'Campo "{nome_campo}" invalido. Informe numero inteiro.')
    if numero < minimo:
        raise ValueError(f'Campo "{nome_campo}" invalido. Minimo permitido: {minimo}.')
    if numero > maximo:
        raise ValueError(f'Campo "{nome_campo}" invalido. Maximo permitido: {maximo}.')
    return numero


def _normalizar_zona(zona: str, *, validar_permitidas: bool = True) -> str:
    if zona is None or str(zona).strip() == '':
        raise ValueError('Campo "zona" obrigatorio.')

    z = str(zona).strip().upper()
    if not re.fullmatch(r'[A-Z0-9]+', z):
        raise ValueError('Campo "zona" invalido. Use apenas caracteres alfanumericos.')
    if not z:
        raise ValueError('Campo "zona" invalido. Use apenas caracteres alfanumericos.')

    if z.startswith('Z'):
        z = z[1:]

    if not z:
        raise ValueError('Campo "zona" invalido. Informe valor apos o prefixo Z.')
    if len(z) > 2:
        raise ValueError('Campo "zona" invalido. Use no maximo 2 caracteres apos Z.')

    zona_normalizada = f'Z{z}'
    if validar_permitidas and _CONFIG.zonas_permitidas and zona_normalizada not in _CONFIG.zonas_permitidas:
        permitidas = ', '.join(sorted(_CONFIG.zonas_permitidas))
        raise ValueError(f'Campo "zona" invalido. Zona "{zona_normalizada}" nao permitida. Permitidas: {permitidas}.')
    return zona_normalizada


def _normalizar_lado(lado: str) -> str:
    if lado is None or str(lado).strip() == '':
        raise ValueError('Campo "lado" obrigatorio.')

    l = str(lado).strip().upper()
    if not re.fullmatch(r'[A-Z0-9]+', l):
        raise ValueError('Campo "lado" invalido. Use apenas caracteres alfanumericos.')
    if not l:
        raise ValueError('Campo "lado" invalido.')

    if l in _MAPA_LADO:
        return _MAPA_LADO[l]

    if l.startswith('L'):
        sufixo = l[1:]
    else:
        sufixo = l

    if sufixo in _MAPA_LADO:
        return _MAPA_LADO[sufixo]

    if len(sufixo) == 1 and sufixo.isalnum():
        return f'L{sufixo}'

    raise ValueError('Campo "lado" invalido. Use A/B, LA/LB, ESQ/DIR ou E/D.')


def montar_endereco(cd, zona, rua, rack, nivel, vao, lado) -> str:
    cd_n = _normalizar_numero('cd', cd, minimo=1)
    zona_n = _normalizar_zona(zona)
    rua_n = _normalizar_numero('rua', rua, minimo=1)
    rack_n = _normalizar_numero('rack', rack, minimo=1)
    nivel_min = 0 if _CONFIG.permitir_nivel_zero else 1
    nivel_n = _normalizar_numero('nivel', nivel, minimo=nivel_min)
    vao_n = _normalizar_numero('vao', vao, minimo=1)
    lado_n = _normalizar_lado(lado)

    return (
        f'CD{cd_n:02d}{_CONFIG.separador}'
        f'{zona_n}{_CONFIG.separador}'
        f'R{rua_n:02d}{_CONFIG.separador}'
        f'RK{rack_n:02d}{_CONFIG.separador}'
        f'N{nivel_n:02d}{_CONFIG.separador}'
        f'V{vao_n:02d}{_CONFIG.separador}'
        f'{lado_n}'
    ).upper()


def parse_endereco(codigo) -> dict:
    texto = _normalizar_codigo_texto(str(codigo or ''))
    match = _REGEX_CODIGO.match(texto)
    if not match:
        raise ValueError(
            'Codigo invalido. Formato esperado: CD##-Z??-R##-RK##-N##-V##-L? (separadores _, espacos e letras minusculas sao normalizados).'
        )

    partes = match.groupdict()
    cd_n = _normalizar_numero('cd', partes['cd'], minimo=1)
    zona_n = _normalizar_zona(partes['zona'])
    rua_n = _normalizar_numero('rua', partes['rua'], minimo=1)
    rack_n = _normalizar_numero('rack', partes['rack'], minimo=1)
    nivel_min = 0 if _CONFIG.permitir_nivel_zero else 1
    nivel_n = _normalizar_numero('nivel', partes['nivel'], minimo=nivel_min)
    vao_n = _normalizar_numero('vao', partes['vao'], minimo=1)
    lado_n = _normalizar_lado(partes['lado'])

    return {
        'cd': cd_n,
        'zona': zona_n,
        'rua': rua_n,
        'rack': rack_n,
        'nivel': nivel_n,
        'vao': vao_n,
        'lado': lado_n,
    }


def validar_endereco(codigo) -> dict:
    try:
        partes = parse_endereco(codigo)
        return {'valido': True, 'erros': [], 'partes': partes}
    except ValueError as exc:
        return {'valido': False, 'erros': [str(exc)], 'partes': {}}


# ======= Endereco supermercado (rack/area aberta) =======

SETORES_ZONA_VALIDOS = (
    'secos',
    'bebidas',
    'hortifruti',
    'frios',
    'congelados',
    'acougue',
    'padaria',
    'deposito',
    'frente_loja',
    'ecommerce_picking',
    'quarentena',
    'avaria',
    'devolucao',
)

TIPOS_AREA_VALIDOS = (
    'picking',
    'pulmao_reserva',
    'recebimento',
    'expedicao_transferencia',
    'frente_loja',
    'quarentena',
    'avaria',
)

STATUS_ENDERECO_VALIDOS = ('ativo', 'bloqueado', 'inventario')
TIPOS_ESTRUTURA_VALIDOS = ('rack', 'area_aberta')
CONTROLE_VALIDADE_VALIDOS = ('nenhum', 'fifo', 'fefo')
TEMPERATURA_VALIDOS = ('ambiente', 'refrigerado', 'congelado')
RESTRICOES_VALIDAS = ('fragil', 'alto_valor', 'quimicos', 'alimentos')

_SIGLAS_SETOR = {
    'secos': 'SEC',
    'bebidas': 'BEB',
    'hortifruti': 'HOR',
    'frios': 'FRI',
    'congelados': 'CON',
    'acougue': 'ACO',
    'padaria': 'PAD',
    'deposito': 'DEP',
    'frente_loja': 'FL',
    'ecommerce_picking': 'ECP',
    'quarentena': 'QUA',
    'avaria': 'AVA',
    'devolucao': 'DEV',
}

_MAPA_LADO_SUPERMERCADO = {
    'A': 'LA',
    'B': 'LB',
    'LA': 'LA',
    'LB': 'LB',
    'E': 'LE',
    'D': 'LD',
    'LE': 'LE',
    'LD': 'LD',
    'ESQ': 'LE',
    'DIR': 'LD',
}


def _sem_acentos(texto: str) -> str:
    base = unicodedata.normalize('NFKD', str(texto or ''))
    return ''.join(c for c in base if not unicodedata.combining(c))


def _normalizar_token(texto: str) -> str:
    normalizado = _sem_acentos(texto).upper().strip()
    normalizado = re.sub(r'\s+', '', normalizado)
    normalizado = re.sub(r'[^A-Z0-9_]', '', normalizado)
    return normalizado


def _normalizar_slug(texto: str, *, max_len: int = 32) -> str:
    normalizado = _sem_acentos(texto).upper().strip()
    normalizado = re.sub(r'[\s_/]+', '-', normalizado)
    normalizado = re.sub(r'[^A-Z0-9-]', '-', normalizado)
    normalizado = re.sub(r'-{2,}', '-', normalizado).strip('-')
    return normalizado[:max_len]


def _normalizar_setor(setor_zona: str) -> str:
    valor = (_sem_acentos(setor_zona).strip().lower().replace(' ', '_')) if setor_zona is not None else ''
    if valor not in SETORES_ZONA_VALIDOS:
        raise ValueError(f'Campo "setor_zona" invalido. Valores permitidos: {", ".join(SETORES_ZONA_VALIDOS)}.')
    return valor


def _normalizar_lado_supermercado(lado: str) -> str:
    valor = _normalizar_token(lado)
    if valor not in _MAPA_LADO_SUPERMERCADO:
        raise ValueError('Campo "lado" invalido. Use A/B, E/D, LA/LB ou LE/LD.')
    return _MAPA_LADO_SUPERMERCADO[valor]


def _numero_2d(nome_campo: str, valor: str) -> str:
    if valor is None or str(valor).strip() == '':
        raise ValueError(f'Campo "{nome_campo}" obrigatorio.')
    digitos = re.search(r'\d+', str(valor))
    if not digitos:
        raise ValueError(f'Campo "{nome_campo}" invalido. Informe valor numerico.')
    numero = int(digitos.group(0))
    return f'{numero:02d}'


def _normalizar_bool(valor) -> bool:
    if isinstance(valor, bool):
        return valor
    texto = str(valor or '').strip().lower()
    return texto in {'1', 'true', 'on', 'sim', 'yes'}


def _normalizar_int_opcional(nome_campo: str, valor):
    if valor is None or str(valor).strip() == '':
        return None
    try:
        numero = int(str(valor).strip())
    except ValueError:
        raise ValueError(f'Campo "{nome_campo}" invalido. Informe numero inteiro.')
    if numero < 0:
        raise ValueError(f'Campo "{nome_campo}" invalido. Nao pode ser negativo.')
    return numero


def _normalizar_float_opcional(nome_campo: str, valor):
    if valor is None or str(valor).strip() == '':
        return None
    try:
        numero = float(str(valor).strip().replace(',', '.'))
    except ValueError:
        raise ValueError(f'Campo "{nome_campo}" invalido. Informe numero.')
    if numero < 0:
        raise ValueError(f'Campo "{nome_campo}" invalido. Nao pode ser negativo.')
    return numero


def _normalizar_prioridade_picking(valor):
    if valor is None:
        return 0
    texto = str(valor).strip().lower()
    if not texto:
        return 0
    if texto in {'1', 'sim', 's', 'true', 'on', 'yes'}:
        return 1
    if texto in {'0', 'nao', 'não', 'n', 'false', 'off', 'no'}:
        return 0
    try:
        return 1 if int(texto) > 0 else 0
    except ValueError:
        raise ValueError('Campo "prioridade_picking" invalido. Use Sim ou Nao.')


def _codigo_area_aberta(ponto_local: str) -> str:
    texto = _sem_acentos(ponto_local or '').upper()
    texto = re.sub(r'\s+', ' ', texto).strip()
    if not texto:
        raise ValueError('Campo "ponto_local" obrigatorio para estrutura area_aberta.')

    g_match = re.search(r'(?:\bGONDOLA\b|\bG\b)\s*0*(\d+)', texto)
    p_match = re.search(r'(?:\bPRATELEIRA\b|\bP\b)\s*0*(\d+)', texto)
    if g_match and p_match:
        return f'G{int(g_match.group(1)):02d}-P{int(p_match.group(1)):02d}'

    slug = _normalizar_slug(texto, max_len=24)
    if not slug:
        raise ValueError('Campo "ponto_local" invalido.')
    return slug


def gerar_codigo_localizacao_supermercado(
    *,
    loja_cd: str,
    setor_zona: str,
    tipo_estrutura: str,
    rua_corredor: str | None = None,
    rack_estante: str | None = None,
    nivel_prateleira: str | None = None,
    posicao_slot: str | None = None,
    lado: str | None = None,
    ponto_local: str | None = None,
) -> str:
    loja = _normalizar_token(loja_cd)
    if not loja:
        raise ValueError('Campo "loja_cd" obrigatorio.')

    setor = _normalizar_setor(setor_zona)
    sigla_setor = _SIGLAS_SETOR[setor]
    estrutura = (_sem_acentos(tipo_estrutura).strip().lower().replace(' ', '_')) if tipo_estrutura else ''
    if estrutura not in TIPOS_ESTRUTURA_VALIDOS:
        raise ValueError(f'Campo "tipo_estrutura" invalido. Valores permitidos: {", ".join(TIPOS_ESTRUTURA_VALIDOS)}.')

    if estrutura == 'rack':
        r = _numero_2d('rua_corredor', rua_corredor)
        rk = _numero_2d('rack_estante', rack_estante)
        n = _numero_2d('nivel_prateleira', nivel_prateleira)
        v = _numero_2d('posicao_slot', posicao_slot)
        lado_norm = _normalizar_lado_supermercado(lado)
        return f'{loja}-{sigla_setor}-R{r}-RK{rk}-N{n}-V{v}-{lado_norm}'

    codigo_area = _codigo_area_aberta(ponto_local or '')
    return f'{loja}-{sigla_setor}-{codigo_area}'


def validar_endereco_supermercado_payload(payload) -> dict:
    """Valida/normaliza payload do formulario de endereco e gera codigo_localizacao."""
    get = payload.get
    getlist = payload.getlist if hasattr(payload, 'getlist') else None

    loja_cd = _normalizar_token(get('loja_cd', ''))
    if not loja_cd:
        raise ValueError('Campo "loja_cd" obrigatorio.')

    setor_zona = _normalizar_setor(get('setor_zona', ''))

    tipo_area = (_sem_acentos(get('tipo_area', '')).strip().lower().replace(' ', '_'))
    if tipo_area not in TIPOS_AREA_VALIDOS:
        raise ValueError(f'Campo "tipo_area" invalido. Valores permitidos: {", ".join(TIPOS_AREA_VALIDOS)}.')

    status = (_sem_acentos(get('status', '')).strip().lower().replace(' ', '_'))
    if status not in STATUS_ENDERECO_VALIDOS:
        raise ValueError(f'Campo "status" invalido. Valores permitidos: {", ".join(STATUS_ENDERECO_VALIDOS)}.')

    tipo_estrutura = (_sem_acentos(get('tipo_estrutura', '')).strip().lower().replace(' ', '_'))
    if tipo_estrutura not in TIPOS_ESTRUTURA_VALIDOS:
        raise ValueError(f'Campo "tipo_estrutura" invalido. Valores permitidos: {", ".join(TIPOS_ESTRUTURA_VALIDOS)}.')

    controle_validade = (_sem_acentos(get('controle_validade', '')).strip().lower().replace(' ', '_'))
    if controle_validade not in CONTROLE_VALIDADE_VALIDOS:
        raise ValueError(
            f'Campo "controle_validade" invalido. Valores permitidos: {", ".join(CONTROLE_VALIDADE_VALIDOS)}.'
        )

    temperatura = (_sem_acentos(get('temperatura', '')).strip().lower().replace(' ', '_')) or None
    if temperatura and temperatura not in TEMPERATURA_VALIDOS:
        raise ValueError(f'Campo "temperatura" invalido. Valores permitidos: {", ".join(TEMPERATURA_VALIDOS)}.')

    rua_corredor = (_normalizar_token(get('rua_corredor', '')) or None)
    rack_estante = (str(get('rack_estante', '')).strip() or None)
    nivel_prateleira = (str(get('nivel_prateleira', '')).strip() or None)
    posicao_slot = (str(get('posicao_slot', '')).strip() or None)
    lado = (_normalizar_token(get('lado', '')) or None)
    ponto_local = (_sem_acentos(get('ponto_local', '')).strip().upper() or None)

    if tipo_estrutura == 'rack':
        if ponto_local:
            ponto_local = None
        if not (rua_corredor and rack_estante and nivel_prateleira and posicao_slot and lado):
            raise ValueError('Para tipo_estrutura=rack, rua_corredor, rack_estante, nivel_prateleira, posicao_slot e lado sao obrigatorios.')
        coluna_baia = _numero_2d('rack_estante', rack_estante)
        nivel = _numero_2d('nivel_prateleira', nivel_prateleira)
        slot = _numero_2d('posicao_slot', posicao_slot)
        lado_norm = _normalizar_lado_supermercado(lado)
    else:
        if not ponto_local:
            raise ValueError('Para tipo_estrutura=area_aberta, campo "ponto_local" e obrigatorio.')
        coluna_baia = None
        nivel = None
        slot = None
        lado_norm = None
        rua_corredor = None

    codigo_localizacao = gerar_codigo_localizacao_supermercado(
        loja_cd=loja_cd,
        setor_zona=setor_zona,
        tipo_estrutura=tipo_estrutura,
        rua_corredor=rua_corredor,
        rack_estante=rack_estante,
        nivel_prateleira=nivel_prateleira,
        posicao_slot=posicao_slot,
        lado=lado_norm,
        ponto_local=ponto_local,
    )

    restricoes_raw = []
    if getlist:
        restricoes_raw = getlist('restricoes')
    elif get('restricoes'):
        restricoes_raw = [get('restricoes')]
    restricoes_normalizadas = []
    for item in restricoes_raw:
        chave = _sem_acentos(str(item or '')).strip().lower().replace(' ', '_')
        if chave in RESTRICOES_VALIDAS:
            restricoes_normalizadas.append(chave)
    restricoes = ','.join(sorted(set(restricoes_normalizadas))) if restricoes_normalizadas else None
    tipo_produto_reservado = (_sem_acentos(get('tipo_produto_reservado', '')).strip().upper() or None)
    if tipo_produto_reservado:
        tipo_produto_reservado = tipo_produto_reservado[:120]

    return {
        'loja_cd': loja_cd,
        'setor_zona': setor_zona,
        'tipo_area': tipo_area,
        'status': status,
        'descricao': (str(get('descricao', '')).strip() or None),
        'observacoes': (str(get('observacoes', '')).strip() or None),
        'tipo_estrutura': tipo_estrutura,
        'rua_corredor': rua_corredor,
        'coluna_baia': coluna_baia,
        'nivel_prateleira': nivel,
        'posicao_slot': slot,
        'lado': lado_norm,
        'ponto_local': ponto_local,
        'permite_fracionado': _normalizar_bool(get('permite_fracionado')),
        'permite_mistura_sku': _normalizar_bool(get('permite_mistura_sku')),
        'permite_mistura_lote': _normalizar_bool(get('permite_mistura_lote')),
        'controle_validade': controle_validade,
        'temperatura': temperatura,
        'restricoes': restricoes,
        'capacidade_caixas': _normalizar_int_opcional('capacidade_caixas', get('capacidade_caixas')),
        'capacidade_fardos': _normalizar_int_opcional('capacidade_fardos', get('capacidade_fardos')),
        'capacidade_unidades': _normalizar_int_opcional('capacidade_unidades', get('capacidade_unidades')),
        'capacidade_pallets': _normalizar_int_opcional('capacidade_pallets', get('capacidade_pallets')),
        'peso_max_kg': _normalizar_float_opcional('peso_max_kg', get('peso_max_kg')),
        'volume_max_m3': _normalizar_float_opcional('volume_max_m3', get('volume_max_m3')),
        'prioridade_picking': _normalizar_prioridade_picking(get('prioridade_picking')),
        'codigo_localizacao': codigo_localizacao,
        'tipo_produto_reservado': tipo_produto_reservado,
        # Mantem compatibilidade com coluna antiga
        'codigo_armazem': loja_cd,
        'tipo_endereco': tipo_area,
        'sku_produto': (str(get('sku_produto', '')).strip() or None),
    }
