from models import Caixa


def test_caixa_fixture_starts_open(caixa):
    assert caixa.aberto is True
    assert float(caixa.saldo_atual) == 100.0


def test_pedido_finalizado_movimenta_saldo_do_caixa(authenticated_client, caixa, produto, csrf_token):
    response = authenticated_client.post('/api/pedidos/criar', json={
        'caixa_id': caixa.id,
        'itens': [{'produto_id': produto.id, 'quantidade': 1}],
    }, headers={'X-CSRF-Token': csrf_token})
    pedido_id = response.get_json()['data']['pedido_id']

    authenticated_client.post(f'/api/pedidos/{pedido_id}/finalizar', json={
        'metodo_pagamento': 'dinheiro',
        'valor_pago': 10.0,
    }, headers={'X-CSRF-Token': csrf_token})

    db_caixa = Caixa.query.get(caixa.id)
    assert float(db_caixa.saldo_atual) == 110.0
