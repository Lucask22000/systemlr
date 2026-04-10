"""Regras de permissao e paginas por colaborador.

Este modulo replica o comportamento legado de app/__init__.py com isolamento.
"""

import json

from flask import current_app, has_request_context, request

from app.constants import PAGINAS_SISTEMA
from models import PermissaoAcesso, db


def carregar_paginas_json(valor_json):
    if not valor_json:
        return set()
    try:
        dados = json.loads(valor_json)
    except Exception:
        return set()
    if not isinstance(dados, list):
        return set()
    return {
        str(item)
        for item in dados
        if isinstance(item, str) and item in PAGINAS_SISTEMA
    }


def serializar_paginas_json(paginas):
    return json.dumps(sorted(set(paginas)))


def expandir_paginas_relacionadas(paginas, bloqueadas=None):
    paginas_normalizadas = set(paginas or [])
    bloqueadas = set(bloqueadas or [])
    if 'movimentacoes' in paginas_normalizadas and 'recebimentos' not in bloqueadas:
        paginas_normalizadas.add('recebimentos')
    if 'movimentacoes' in paginas_normalizadas and 'almoxarifado' not in bloqueadas:
        paginas_normalizadas.add('almoxarifado')
    if 'expedicao' in paginas_normalizadas and 'transferencias_estoque' not in bloqueadas:
        paginas_normalizadas.add('transferencias_estoque')
    return paginas_normalizadas


def paginas_perfil_acesso(perfil_acesso):
    if not perfil_acesso:
        return set()
    return expandir_paginas_relacionadas(carregar_paginas_json(perfil_acesso.permissoes_padrao))


def mapa_permissoes_personalizadas_funcionario(funcionario):
    if not funcionario:
        return {}
    return {
        permissao.pagina: bool(permissao.permitido)
        for permissao in PermissaoAcesso.query.filter_by(funcionario_id=funcionario.id).all()
        if permissao.pagina in PAGINAS_SISTEMA
    }


def paginas_efetivas_funcionario(funcionario):
    if not funcionario:
        return set()

    if funcionario.role == 'admin' or not funcionario.controle_acesso_ativo:
        permitidas = set(PAGINAS_SISTEMA.keys())
    else:
        mapa_personalizado = mapa_permissoes_personalizadas_funcionario(funcionario)
        paginas_base = paginas_perfil_acesso(funcionario.perfil_acesso)
        bloqueadas = {
            pagina
            for pagina, permitido in mapa_personalizado.items()
            if not permitido
        }
        permitidas = set(paginas_base)
        permitidas.update(
            pagina
            for pagina, permitido in mapa_personalizado.items()
            if permitido
        )
        permitidas.difference_update(bloqueadas)
        permitidas = expandir_paginas_relacionadas(permitidas, bloqueadas=bloqueadas)
        if not permitidas and has_request_context():
            current_app.logger.warning(
                'menu_debug_empty funcionario_id=%s role=%s controle=%s perfil_acesso_id=%s endpoint=%s mapa_personalizado=%s paginas_base=%s',
                getattr(funcionario, 'id', None),
                getattr(funcionario, 'role', None),
                getattr(funcionario, 'controle_acesso_ativo', None),
                getattr(funcionario, 'perfil_acesso_id', None),
                request.endpoint,
                mapa_personalizado,
                sorted(paginas_base),
            )

    permitidas.add('ajuda')
    return permitidas


def salvar_permissoes_funcionario(funcionario, paginas_selecionadas):
    paginas_validas = set(PAGINAS_SISTEMA.keys())
    paginas_salvas = set(paginas_selecionadas).intersection(paginas_validas)
    paginas_base = paginas_perfil_acesso(funcionario.perfil_acesso)

    PermissaoAcesso.query.filter_by(funcionario_id=funcionario.id).delete()

    if funcionario.perfil_acesso_id:
        for pagina in sorted(paginas_validas):
            presente_na_base = pagina in paginas_base
            presente_no_resultado = pagina in paginas_salvas
            if presente_na_base == presente_no_resultado:
                continue
            db.session.add(
                PermissaoAcesso(
                    funcionario_id=funcionario.id,
                    pagina=pagina,
                    permitido=presente_no_resultado,
                )
            )
    else:
        for pagina in sorted(paginas_salvas):
            db.session.add(
                PermissaoAcesso(
                    funcionario_id=funcionario.id,
                    pagina=pagina,
                    permitido=True,
                )
            )

    funcionario.controle_acesso_ativo = True


def paginas_permitidas_para_funcionario(funcionario):
    return paginas_efetivas_funcionario(funcionario)
