import json

from app import db
from routes import vendas_routes
from models import (
    Caixa,
    EnderecoEstoque,
    Estoque,
    FrotaVeiculo,
    ItemPedido,
    LancamentoFinanceiro,
    Pedido,
    PermissaoAcesso,
    Produto,
)


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


def test_busca_produtos_pdv_retorna_payload_ranqueado(authenticated_client, produto):
    response = authenticated_client.get('/api/pdv/produtos/buscar?q=Refr')
    payload = response.get_json()

    assert response.status_code == 200
    assert payload['success'] is True
    assert payload['data']['items']
    assert payload['data']['items'][0]['produto_id'] == produto.id
    assert payload['data']['search_strategy'] == 'barcode_first_then_ranked_text'


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


def test_checkout_site_bloqueia_estoque_insuficiente(client, produto, csrf_token):
    produto.quantidade_estoque = 1
    db.session.commit()

    with client.session_transaction() as sess:
        sess['site_carrinho'] = {str(produto.id): 2}
        sess['_csrf_token'] = csrf_token

    response = client.post('/checkout', data={
        'nome': 'Cliente Site',
        'email': 'cliente@site.test',
        'celular': '65999999999',
        'cep': '78000000',
        'endereco': 'Rua A',
        'numero': '10',
        'bairro': 'Centro',
        'cidade': 'Cuiaba',
        'estado': 'MT',
        'metodo_pagamento': 'pix',
        'csrf_token': csrf_token,
    }, follow_redirects=True)

    assert response.status_code == 200
    assert Pedido.query.count() == 0


def test_editar_pedido_com_status_fechado_usa_fluxo_unificado(authenticated_client, caixa, produto, csrf_token):
    pedido = Pedido(
        caixa_id=caixa.id,
        status=Pedido.STATUS_ABERTO,
        total=10.0,
        estoque_processado=False,
        financeiro_processado=False,
    )
    db.session.add(pedido)
    db.session.flush()
    db.session.add(ItemPedido(pedido_id=pedido.id, produto_id=produto.id, quantidade=1, preco_unitario=produto.preco_venda))
    db.session.commit()

    response = authenticated_client.post(f'/pedidos/{pedido.id}/editar', data={
        'status': Pedido.STATUS_FECHADO,
        'caixa_id': caixa.id,
        'item_count': 1,
        'produto_0': produto.id,
        'quantidade_0': 2,
        'metodo_pagamento': 'dinheiro',
        'valor_pago': '20',
        'observacoes': 'fechamento pela edicao',
        'csrf_token': csrf_token,
    })

    assert response.status_code == 302
    db.session.refresh(pedido)
    db.session.refresh(produto)
    db.session.refresh(caixa)
    assert pedido.status == Pedido.STATUS_FECHADO
    assert pedido.estoque_processado is True
    assert pedido.financeiro_processado is True
    assert produto.quantidade_estoque == 8
    assert float(caixa.saldo_atual) == 120.0
    assert LancamentoFinanceiro.query.filter_by(pedido_id=pedido.id).count() == 1


def test_separacao_entrega_bloqueia_produto_fora_de_picking(authenticated_client, caixa, produto, csrf_token):
    estoque = Estoque(nome='CD Pedido', ativo=True)
    db.session.add(estoque)
    db.session.flush()
    endereco = EnderecoEstoque(
        estoque_id=estoque.id,
        nome='Rua 01',
        loja_cd='CD01',
        setor_zona='deposito',
        tipo_area='armazenagem',
        status='ativo',
        tipo_estrutura='rack',
        codigo_armazem='CD01',
        rua_corredor='01',
        coluna_baia='01',
        nivel_prateleira='01',
        posicao_slot='01',
        lado='LA',
        controle_validade='fifo',
        codigo_localizacao='CD01-DEP-R01-RK01-N01-V01-LA',
        ativo=True,
    )
    db.session.add(endereco)
    db.session.flush()
    produto.endereco_id = endereco.id

    pedido = Pedido(
        caixa_id=caixa.id,
        origem='site',
        status=Pedido.STATUS_ENTREGUE,
        total=10.0,
        estoque_processado=False,
        financeiro_processado=False,
    )
    db.session.add(pedido)
    db.session.flush()
    db.session.add(ItemPedido(pedido_id=pedido.id, produto_id=produto.id, quantidade=1, preco_unitario=produto.preco_venda))
    db.session.commit()

    response = authenticated_client.post(f'/pedidos/{pedido.id}/separacao-entrega', data={
        'acao': 'concluir',
        'csrf_token': csrf_token,
    })

    assert response.status_code == 302
    db.session.refresh(pedido)
    assert pedido.separacao_entrega_concluida in (False, None)
    assert pedido.separacao_entrega_em is None


def test_frota_expedicao_salva_veiculo_em_tabela(authenticated_client, csrf_token):
    response = authenticated_client.post('/expedicao/frota', data={
        'acao': 'salvar_veiculo',
        'nome': 'Moto Centro',
        'placa': 'ABC1D23',
        'tipo': 'moto',
        'tipo_entrega': 'site',
        'capacidade_pedidos': '8',
        'capacidade_kg': '35',
        'capacidade_volume': '0.4',
        'motorista_padrao': 'Joao',
        'ativo': 'on',
        'csrf_token': csrf_token,
    })

    assert response.status_code == 302
    veiculo = FrotaVeiculo.query.filter_by(nome='Moto Centro').first()
    assert veiculo is not None
    assert veiculo.tipo_entrega == 'site'
    assert veiculo.capacidade_pedidos == 8


def test_ordenacao_de_rotas_prioriza_pedido_mais_proximo(monkeypatch):
    pedido_perto = Pedido(id=1, observacoes=json.dumps({'cliente_cadastro': {'cep': '78000000'}}))
    pedido_longe = Pedido(id=2, observacoes=json.dumps({'cliente_cadastro': {'cep': '01000000'}}))

    coordenadas = {
        '78000000': (-15.60, -56.10),
        '01000000': (-23.55, -46.63),
        '79000000': (-20.45, -54.61),
    }

    monkeypatch.setattr(vendas_routes, '_obter_coordenadas_cep', lambda cep: coordenadas.get(str(cep).replace('-', '')))

    ordenados = vendas_routes._ordenar_pedidos_por_proximidade(
        [pedido_longe, pedido_perto],
        '79000000',
    )

    assert [pedido.id for pedido in ordenados] == [1, 2]
