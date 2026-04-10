from app.services.auth_service import AuthService
from app.services.permissao_service import PermissaoService
from models import Funcionario, db


def test_auth_service_login_accepts_email(db_session):
    funcionario = Funcionario(nome='Usuario', email='usuario@test.local', role='admin', ativo=True)
    funcionario.set_password('123456')
    db.session.add(funcionario)
    db.session.commit()

    service = AuthService(
        normalizar_matricula=lambda value: value,
        normalizar_texto=lambda value: (value or '').strip().lower(),
        normalizar_cpf=lambda value: value,
    )
    autenticado, erro = service.login('usuario@test.local', '123456')

    assert autenticado is not None
    assert autenticado.email == 'usuario@test.local'
    assert erro == ''


def test_permissao_service_uses_api_fallback_pages():
    funcionario = Funcionario(nome='Gerente', email='gerente@test.local', role='gerente', ativo=True)
    funcionario.controle_acesso_ativo = True

    service = PermissaoService(resolver_paginas=lambda _funcionario: ['empresa'])

    assert service.tem_acesso(funcionario, 'api_inexistente', is_api_request=True) is True
    assert service.tem_acesso(funcionario, 'api_inexistente', is_api_request=False) is True
