from app import local_ai_assistant
from models import AssistenteLocalFeedback


def test_local_ai_status_endpoint_returns_available_mode(authenticated_client):
    response = authenticated_client.get('/api/assistente-local/status')
    assert response.status_code == 200
    payload = response.get_json()
    assert payload['success'] is True
    assert payload['data']['mode'] in {'lexical', 'semantic'}
    assert payload['data']['document_count'] > 0


def test_local_ai_semantic_fallback_encoder_builds_without_sentence_transformers(app_ctx):
    local_ai_assistant._ensure_documents(force=True)
    assert local_ai_assistant._try_prepare_semantic_model() is True
    assert local_ai_assistant.model_id
    assert local_ai_assistant._encoder is not None
    assert local_ai_assistant._document_vectors


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


def test_local_ai_broad_question_teaches_before_suggesting_navigation(authenticated_client, csrf_token):
    response = authenticated_client.post('/api/assistente-local/perguntar', json={
        'pergunta': 'quero saber sobre estoque',
        'endpoint_atual': 'listar_produtos',
        'tela_atual': 'Produtos',
    }, headers={'X-CSRF-Token': csrf_token})
    assert response.status_code == 200
    payload = response.get_json()
    assert payload['success'] is True
    answer = payload['data']['answer'].lower()
    assert 'posso te explicar estoque passo a passo' in answer
    assert 'fluxo mais comum' in answer
    assert 'qual parte primeiro' in answer
    assert payload['data']['actions'] == []


def test_local_ai_single_topic_question_returns_instructional_overview(authenticated_client, csrf_token):
    response = authenticated_client.post('/api/assistente-local/perguntar', json={
        'pergunta': 'estoque',
        'endpoint_atual': 'listar_produtos',
        'tela_atual': 'Produtos',
    }, headers={'X-CSRF-Token': csrf_token})
    assert response.status_code == 200
    payload = response.get_json()
    assert payload['success'] is True
    answer = payload['data']['answer'].lower()
    assert 'posso te explicar estoque passo a passo' in answer
    assert 'cadastre categorias, produtos e dados basicos do item' in answer
    assert 'recebimentos' in answer
    assert payload['data']['actions'] == []


def test_intent_greeting(authenticated_client, csrf_token):
    resp = authenticated_client.post('/api/assistente-local/perguntar', json={
        'pergunta': 'Ola',
        'endpoint_atual': 'dashboard',
        'tela_atual': 'Dashboard',
    }, headers={'X-CSRF-Token': csrf_token})
    payload = resp.get_json()
    assert payload['success'] is True
    assert payload['data']['answer'].lower().startswith('ola')
    assert payload['data']['actions'] == []


def test_broad_exploration_estoque(authenticated_client, csrf_token):
    resp = authenticated_client.post('/api/assistente-local/perguntar', json={
        'pergunta': 'quero saber sobre estoque',
        'endpoint_atual': 'listar_produtos',
        'tela_atual': 'Produtos',
    }, headers={'X-CSRF-Token': csrf_token})
    payload = resp.get_json()
    answer = payload['data']['answer'].lower()
    assert 'estoque' in answer
    assert 'passo a passo' in answer
    assert payload['data']['actions'] == []


def test_operational_receber_fornecedor_coerent(authenticated_client, csrf_token):
    resp = authenticated_client.post('/api/assistente-local/perguntar', json={
        'pergunta': 'como receber um fornecedor',
        'endpoint_atual': 'listar_recebimentos_fornecedor',
        'tela_atual': 'Recebimentos',
    }, headers={'X-CSRF-Token': csrf_token})
    payload = resp.get_json()
    answer = payload['data']['answer'].lower()
    assert 'receber' in answer or 'entrada' in answer
    assert 'fornecedor' in answer or 'mercadoria' in answer or 'estoque' in answer
    assert 'rh' not in answer and 'pdv' not in answer


def test_access_permission_financeiro(authenticated_client, csrf_token):
    resp = authenticated_client.post('/api/assistente-local/perguntar', json={
        'pergunta': 'nao tenho acesso ao menu financeiro',
        'endpoint_atual': 'financeiro_lancamentos',
        'tela_atual': 'Financeiro',
    }, headers={'X-CSRF-Token': csrf_token})
    payload = resp.get_json()
    answer = payload['data']['answer'].lower()
    assert 'permissao' in answer or 'acesso' in answer
    assert 'estoque' not in answer


def test_incident_problem_estoque_negativo(authenticated_client, csrf_token):
    resp = authenticated_client.post('/api/assistente-local/perguntar', json={
        'pergunta': 'estoque ficou negativo',
        'endpoint_atual': 'listar_produtos',
        'tela_atual': 'Produtos',
    }, headers={'X-CSRF-Token': csrf_token})
    payload = resp.get_json()
    answer = payload['data']['answer'].lower()
    assert 'problema' in answer or 'ajuste' in answer or 'revisar' in answer
    assert 'passo a passo' not in answer


def test_navigation_request_recebimento(authenticated_client, csrf_token):
    resp = authenticated_client.post('/api/assistente-local/perguntar', json={
        'pergunta': 'onde fica a entrada de mercadoria?',
        'endpoint_atual': 'listar_recebimentos_fornecedor',
        'tela_atual': 'Recebimentos',
    }, headers={'X-CSRF-Token': csrf_token})
    payload = resp.get_json()
    answer = payload['data']['answer'].lower()
    assert 'onde' in answer or 'voce encontra' in answer
    assert 'erro' not in answer


def test_ambiguous_fornecedor_refinement(authenticated_client, csrf_token):
    resp = authenticated_client.post('/api/assistente-local/perguntar', json={
        'pergunta': 'como lancar fornecedor',
        'endpoint_atual': 'listar_fornecedores',
        'tela_atual': 'Fornecedores',
    }, headers={'X-CSRF-Token': csrf_token})
    payload = resp.get_json()
    answer = payload['data']['answer'].lower()
    assert 'quero te responder certo' in answer or 'voce quer saber' in answer
