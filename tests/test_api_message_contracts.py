from app.exceptions import ValidationError
from app import handle_validation_error
from security import json_response


def test_json_response_exposes_standard_contract(app_ctx):
    response, status_code = json_response(
        False,
        'Pergunta obrigatoria.',
        status=400,
        code='assistant_question_required',
        fields={'pergunta': 'Informe uma pergunta com ate 500 caracteres.'},
        action='Preencha o campo de pergunta antes de enviar.',
    )

    payload = response.get_json()
    assert status_code == 400
    assert payload == {
        'success': False,
        'message': 'Pergunta obrigatoria.',
        'code': 'assistant_question_required',
        'fields': {'pergunta': 'Informe uma pergunta com ate 500 caracteres.'},
        'action': 'Preencha o campo de pergunta antes de enviar.',
    }


def test_assistente_question_validation_returns_fields_and_action(authenticated_client, csrf_token):
    response = authenticated_client.post(
        '/api/assistente-local/perguntar',
        json={'pergunta': ''},
        headers={'X-CSRF-Token': csrf_token},
    )

    payload = response.get_json()
    assert response.status_code == 400
    assert payload['success'] is False
    assert payload['code'] == 'assistant_question_required'
    assert payload['fields']['pergunta'] == 'Informe uma pergunta com ate 500 caracteres.'
    assert payload['action'] == 'Preencha o campo de pergunta antes de enviar.'


def test_validation_error_handler_returns_standard_json_contract(app):
    with app.test_request_context('/api/_test/validation-error', headers={'Accept': 'application/json'}):
        response, status_code = handle_validation_error(
            ValidationError(
                'CPF invalido. Informe no formato 000.000.000-00.',
                action='Corrija o CPF informado e tente novamente.',
                fields={'cpf': 'Use o formato 000.000.000-00.'},
            )
        )
    payload = response.get_json()

    assert status_code == 400
    assert payload['success'] is False
    assert payload['code'] == 'validation_error'
    assert payload['message'] == 'CPF invalido. Informe no formato 000.000.000-00.'
    assert payload['fields'] == {'cpf': 'Use o formato 000.000.000-00.'}
    assert payload['action'] == 'Corrija o CPF informado e tente novamente.'
