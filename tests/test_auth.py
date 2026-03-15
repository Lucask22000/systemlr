from models import Funcionario


def test_login_logout_flow(client, db_session, csrf_token):
    funcionario = Funcionario(nome='Usuario', email='usuario@test.local', role='admin', ativo=True)
    funcionario.set_password('123456')
    db_session.add(funcionario)
    db_session.commit()

    with client.session_transaction() as sess:
        sess['_csrf_token'] = csrf_token

    response = client.post('/login', data={
        'login': 'usuario@test.local',
        'senha': '123456',
        'csrf_token': csrf_token,
    }, follow_redirects=False)
    assert response.status_code == 302

    logout = client.get('/logout', follow_redirects=False)
    assert logout.status_code == 302


def test_login_rate_limit_with_missing_credentials(client, csrf_token):
    with client.session_transaction() as sess:
        sess['_csrf_token'] = csrf_token

    response = client.post('/login', data={
        'login': '',
        'senha': '',
        'csrf_token': csrf_token,
    }, follow_redirects=False)
    assert response.status_code == 302


def test_registro_requires_required_fields(authenticated_client, csrf_token):
    response = authenticated_client.post('/registro', data={
        'nome': '',
        'email': '',
        'senha': '',
        'csrf_token': csrf_token,
    }, follow_redirects=False)
    assert response.status_code == 302
