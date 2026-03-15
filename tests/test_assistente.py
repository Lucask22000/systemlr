from models import AssistenteLocalFeedback


def test_local_ai_status_endpoint_returns_available_mode(authenticated_client):
    response = authenticated_client.get('/api/assistente-local/status')
    assert response.status_code == 200
    payload = response.get_json()
    assert payload['success'] is True
    assert payload['data']['mode'] in {'lexical', 'semantic'}
    assert payload['data']['document_count'] > 0


def test_local_ai_question_returns_answer_and_actions(authenticated_client, csrf_token):
    response = authenticated_client.post('/api/assistente-local/perguntar', json={
        'pergunta': 'Como registrar um recebimento?',
        'endpoint_atual': 'listar_recebimentos_fornecedor',
        'tela_atual': 'Central de Recebimentos',
    }, headers={'X-CSRF-Token': csrf_token})
    assert response.status_code == 200
    payload = response.get_json()
    assert payload['success'] is True
    assert payload['data']['answer']
    assert payload['data']['actions']


def test_local_ai_greeting_returns_simple_reply(authenticated_client, csrf_token):
    response = authenticated_client.post('/api/assistente-local/perguntar', json={
        'pergunta': 'bom dia',
        'endpoint_atual': 'dashboard',
        'tela_atual': 'Dashboard',
    }, headers={'X-CSRF-Token': csrf_token})
    assert response.status_code == 200
    payload = response.get_json()
    assert payload['data']['answer'] == 'Bom dia! Em que posso ajudar?'
    assert payload['data']['actions'] == []


def test_local_ai_feedback_persists_vote(authenticated_client, csrf_token):
    pergunta = authenticated_client.post('/api/assistente-local/perguntar', json={
        'pergunta': 'Nao consigo liberar um pedido para roteirizacao',
        'endpoint_atual': 'listar_roteirizacao_entrega',
        'tela_atual': 'Roteirizacao',
    }, headers={'X-CSRF-Token': csrf_token})
    payload = pergunta.get_json()
    response_id = payload['data']['response_id']

    feedback = authenticated_client.post('/api/assistente-local/feedback', json={
        'response_id': response_id,
        'vote': 'like',
        'question_text': 'Nao consigo liberar um pedido para roteirizacao',
        'answer_text': payload['data']['answer'],
        'endpoint_atual': 'listar_roteirizacao_entrega',
        'tela_atual': 'Roteirizacao',
        'matched_doc_ids': payload['data']['matched_doc_ids'],
    }, headers={'X-CSRF-Token': csrf_token})
    assert feedback.status_code == 200
    registro = AssistenteLocalFeedback.query.filter_by(response_id=response_id).first()
    assert registro is not None
    assert registro.vote == 'like'
