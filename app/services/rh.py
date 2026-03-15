from flask import request

from app.helpers import _normalizar_texto
from app.constants import ENDPOINT_TO_PAGINA
from models import Garcom


def sincronizar_garcom_funcionario(funcionario):
    if not funcionario:
        return

    role_norm = _normalizar_texto(funcionario.role)
    cargo_norm = _normalizar_texto(funcionario.cargo)
    deve_ser_garcom = role_norm == 'garcom' or cargo_norm in {'garcom', 'garçom'}

    garcom = Garcom.query.filter_by(funcionario_id=funcionario.id).first()
    if deve_ser_garcom:
        if not garcom:
            garcom = Garcom(
                funcionario_id=funcionario.id,
                nome=funcionario.nome,
                ativo=funcionario.ativo,
            )
            from models import db
            db.session.add(garcom)
        else:
            garcom.nome = funcionario.nome
            garcom.ativo = funcionario.ativo
        return

    if garcom:
        garcom.nome = funcionario.nome
        garcom.ativo = False


def funcionario_tem_acesso(funcionario, endpoint, paginas_resolvidas):
    if not funcionario:
        return False
    if funcionario.role == 'admin':
        return True
    if not funcionario.controle_acesso_ativo:
        return True

    pagina = ENDPOINT_TO_PAGINA.get(endpoint)
    if not pagina:
        if request.path.startswith('/api/'):
            return False
        return True

    return pagina in paginas_resolvidas


def _paginas_permitidas_para_funcionario(funcionario, resolver_paginas):
    return resolver_paginas(funcionario)
