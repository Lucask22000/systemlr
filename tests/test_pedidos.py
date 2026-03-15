from models import Caixa, Pedido, PermissaoAcesso, Produto


def test_criar_pedido_api(authenticated_client, caixa, produto, csrf_token):
    response = authenticated_client.post('/api/pedidos/criar', json={
        'caixa_id': caixa.id,
        'itens': [{'produto_id': produto.id, 'quantidade': 2}],
    }, headers={'X-CSRF-Token': csrf_token})
    assert response.status_code == 200
    assert response.get_json()['success'] is True


def test_finalizar_pedido_atualiza_estoque_e_caixa(authenticated_client, caixa, produto, csrf_token):
    create_response = authenticated_client.post('/api/pedidos/criar', json={
        'caixa_id': caixa.id,
        'itens': [{'produto_id': produto.id, 'quantidade': 2}],
    }, headers={'X-CSRF-Token': csrf_token})
    pedido_id = create_response.get_json()['data']['pedido_id']

    finalize_response = authenticated_client.post(f'/api/pedidos/{pedido_id}/finalizar', json={
        'metodo_pagamento': 'dinheiro',
        'valor_pago': 20.0,
    }, headers={'X-CSRF-Token': csrf_token})
    assert finalize_response.status_code == 200

    pedido = Pedido.query.get(pedido_id)
    db_produto = Produto.query.get(produto.id)
    db_caixa = Caixa.query.get(caixa.id)
    assert pedido.status == 'fechado'
    assert db_produto.quantidade_estoque == 8
    assert float(db_caixa.saldo_atual) == 120.0


def test_transicao_invalida_retorna_conflito(authenticated_client, caixa, produto, csrf_token):
    create_response = authenticated_client.post('/api/pedidos/criar', json={
        'caixa_id': caixa.id,
        'itens': [{'produto_id': produto.id, 'quantidade': 1}],
    }, headers={'X-CSRF-Token': csrf_token})
    pedido_id = create_response.get_json()['data']['pedido_id']

    authenticated_client.post(f'/api/pedidos/{pedido_id}/finalizar', json={
        'metodo_pagamento': 'dinheiro',
        'valor_pago': 10.0,
    }, headers={'X-CSRF-Token': csrf_token})

    second = authenticated_client.post(f'/api/pedidos/{pedido_id}/finalizar', json={
        'metodo_pagamento': 'dinheiro',
        'valor_pago': 10.0,
    }, headers={'X-CSRF-Token': csrf_token})
    assert second.status_code == 409


def test_pedido_api_bloqueado_sem_permissao(client, db_session, caixa, produto, csrf_token):
    gerente = PermissaoAcesso
    from models import Funcionario
    usuario = Funcionario(
        nome='Gerente Restrito',
        email='gerente@test.local',
        role='gerente',
        ativo=True,
        controle_acesso_ativo=True,
    )
    usuario.set_password('123456')
    db_session.add(usuario)
    db_session.flush()
    db_session.add(gerente(funcionario_id=usuario.id, pagina='inicio'))
    db_session.commit()

    with client.session_transaction() as sess:
        sess['funcionario_id'] = usuario.id
        sess['funcionario_nome'] = usuario.nome
        sess['funcionario_role'] = usuario.role
        sess['_csrf_token'] = csrf_token

    response = client.post('/api/pedidos/criar', json={
        'caixa_id': caixa.id,
        'itens': [{'produto_id': produto.id, 'quantidade': 1}],
    }, headers={'X-CSRF-Token': csrf_token})
    assert response.status_code == 403
