import os

import pytest

os.environ['FLASK_CONFIG'] = 'testing'

from app import app as flask_app, db  # noqa: E402
from models import Caixa, Categoria, Funcionario, Produto  # noqa: E402


@pytest.fixture
def app():
    return flask_app


@pytest.fixture
def app_ctx(app):
    ctx = app.app_context()
    ctx.push()
    yield ctx
    ctx.pop()


@pytest.fixture
def db_session(app_ctx):
    db.drop_all()
    db.create_all()
    yield db.session
    db.session.remove()
    db.drop_all()


@pytest.fixture
def client(app, db_session):
    return app.test_client()


@pytest.fixture
def csrf_token():
    return 'test-csrf-token'


@pytest.fixture
def admin_user(db_session):
    funcionario = Funcionario(nome='Admin', email='admin@test.local', role='admin', ativo=True)
    funcionario.set_password('123456')
    db.session.add(funcionario)
    db.session.commit()
    return funcionario


@pytest.fixture
def authenticated_client(client, admin_user, csrf_token):
    with client.session_transaction() as sess:
        sess['funcionario_id'] = admin_user.id
        sess['funcionario_nome'] = admin_user.nome
        sess['funcionario_role'] = admin_user.role
        sess['_csrf_token'] = csrf_token
    return client


@pytest.fixture
def categoria(db_session):
    registro = Categoria(nome='Bebidas', descricao='Categoria de teste')
    db.session.add(registro)
    db.session.commit()
    return registro


@pytest.fixture
def produto(categoria):
    registro = Produto(
        codigo='P001',
        nome='Refrigerante',
        categoria_id=categoria.id,
        preco_custo=4.0,
        preco_venda=10.0,
        quantidade_estoque=10,
        quantidade_minima=2,
        ativo=True,
    )
    db.session.add(registro)
    db.session.commit()
    return registro


@pytest.fixture
def caixa(db_session):
    registro = Caixa(
        nome='Caixa 1',
        saldo_inicial=100.0,
        saldo_atual=100.0,
        aberto=True,
        funcionario_id=None,
    )
    db.session.add(registro)
    db.session.commit()
    return registro
