from models import EnderecoEstoque, Estoque, Fornecedor, Movimentacao, Produto, RecebimentoFornecedor


def test_stock_address_creation_requires_and_accepts_csrf(authenticated_client, csrf_token):
    estoque = Estoque(nome='CD Principal', ativo=True)
    from app import db
    db.session.add(estoque)
    db.session.commit()

    without_csrf = authenticated_client.post('/enderecos-estoque/novo', data={
        'estoque_id': estoque.id,
        'nome': 'Deposito Central',
        'loja_cd': 'LJ01',
        'setor_zona': 'deposito',
        'tipo_area': 'picking',
        'status': 'ativo',
        'tipo_estrutura': 'area_aberta',
        'cidade': 'Cuiaba',
        'estado': 'MT',
        'ativo': 'on',
    })
    assert without_csrf.status_code == 400

    with_csrf = authenticated_client.post('/enderecos-estoque/novo', data={
        'estoque_id': estoque.id,
        'nome': 'Deposito Central',
        'loja_cd': 'LJ01',
        'setor_zona': 'deposito',
        'tipo_area': 'picking',
        'status': 'ativo',
        'tipo_estrutura': 'area_aberta',
        'cidade': 'Cuiaba',
        'estado': 'MT',
        'ativo': 'on',
        'csrf_token': csrf_token,
    })
    assert with_csrf.status_code == 302


def test_new_movement_requires_supplier_when_receiving_from_supplier(authenticated_client, produto, csrf_token):
    from app import db
    fornecedor = Fornecedor(nome='Fornecedor X', ativo=True)
    db.session.add(fornecedor)
    db.session.commit()

    sem_fornecedor = authenticated_client.post('/movimentacoes/nova', data={
        'produto_id': produto.id,
        'tipo': 'entrada',
        'quantidade': 2,
        'recebimento_fornecedor': 'on',
        'csrf_token': csrf_token,
    })
    assert sem_fornecedor.status_code == 302
    assert Movimentacao.query.count() == 0

    com_fornecedor = authenticated_client.post('/movimentacoes/nova', data={
        'produto_id': produto.id,
        'tipo': 'entrada',
        'quantidade': 2,
        'recebimento_fornecedor': 'on',
        'fornecedor_id': fornecedor.id,
        'csrf_token': csrf_token,
    })
    assert com_fornecedor.status_code == 302
    assert Movimentacao.query.count() == 1


def test_recebimento_put_away_updates_stock_only_on_armazenagem(authenticated_client, produto, csrf_token):
    from app import db
    fornecedor = Fornecedor(nome='Fornecedor PutAway', ativo=True)
    estoque = Estoque(nome='CD Recebimento', ativo=True)
    db.session.add_all([fornecedor, estoque])
    db.session.flush()

    endereco = EnderecoEstoque(
        estoque_id=estoque.id,
        nome='Endereco Recebimento A',
        loja_cd='LJ01',
        setor_zona='deposito',
        tipo_area='recebimento',
        status='ativo',
        tipo_estrutura='rack',
        codigo_armazem='LJ01',
        rua_corredor='03',
        coluna_baia='02',
        nivel_prateleira='01',
        posicao_slot='08',
        lado='LA',
        controle_validade='fifo',
        codigo_localizacao='LJ01-DEP-R03-RK02-N01-V08-LA',
        ativo=True,
    )
    db.session.add(endereco)
    db.session.commit()

    estoque_inicial = produto.quantidade_estoque
    criar = authenticated_client.post('/estoque/recebimentos/novo', data={
        'fornecedor_id': fornecedor.id,
        'tipo_recebimento': RecebimentoFornecedor.TIPO_COMPRA_REVENDA,
        'local_recebimento_id': endereco.id,
        'info_nota': 'NF 123',
        'produto_id[]': [produto.id],
        'qtd_recebida[]': ['5'],
        'csrf_token': csrf_token,
    })
    assert criar.status_code == 302

    recebimento = RecebimentoFornecedor.query.order_by(RecebimentoFornecedor.id.desc()).first()
    item = recebimento.itens[0]

    conferir = authenticated_client.post(f'/estoque/recebimentos/{recebimento.id}/conferir', data={
        f'item_{item.id}_qtd_recebida': '5',
        f'item_{item.id}_qtd_avaria': '1',
        f'item_{item.id}_lote': 'L001',
        f'item_{item.id}_validade': '2027-12-31',
        'csrf_token': csrf_token,
    })
    assert conferir.status_code == 302

    db.session.refresh(produto)
    assert produto.quantidade_estoque == estoque_inicial

    armazenar = authenticated_client.post(f'/estoque/recebimentos/{recebimento.id}/armazenar', data={
        f'endereco_destino_{item.id}': endereco.id,
        'csrf_token': csrf_token,
    })
    assert armazenar.status_code == 302

    db.session.refresh(produto)
    assert produto.quantidade_estoque == estoque_inicial + 4


def test_cadastro_dependente_retorna_para_recebimento_com_entidade(authenticated_client, csrf_token):
    response = authenticated_client.post('/fornecedores/novo', data={
        'nome': 'Fornecedor Retorno',
        'documento': '12345678000199',
        'ativo': 'on',
        'return_to': '/estoque/recebimentos/novo?context_key=abc123',
        'origem': 'novo_recebimento_fornecedor',
        'contexto': 'recebimento_fornecedor',
        'context_key': 'abc123',
        'csrf_token': csrf_token,
    })

    assert response.status_code == 302
    assert '/estoque/recebimentos/novo?context_key=abc123' in response.headers['Location']
    assert 'flow_entity=fornecedor' in response.headers['Location']
