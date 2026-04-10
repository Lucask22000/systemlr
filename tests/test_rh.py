from app import db, sincronizar_garcom_funcionario
from models import Funcionario, Garcom


def test_waiter_profile_is_disabled_when_role_changes(db_session):
    funcionario = Funcionario(
        nome='Garcom Teste',
        email='garcom@test.local',
        role='garcom',
        cargo='Garcom',
        ativo=True,
    )
    funcionario.set_password('123456')
    db.session.add(funcionario)
    db.session.flush()

    sincronizar_garcom_funcionario(funcionario)
    db.session.commit()

    garcom = Garcom.query.filter_by(funcionario_id=funcionario.id).first()
    assert garcom is not None
    assert garcom.ativo is True

    funcionario.role = 'caixa'
    funcionario.cargo = 'Caixa'
    sincronizar_garcom_funcionario(funcionario)
    db.session.commit()

    db.session.refresh(garcom)
    assert garcom.ativo is False


def test_auditoria_page_requires_authenticated_profile(authenticated_client):
    response = authenticated_client.get('/auditoria')
    assert response.status_code == 200
