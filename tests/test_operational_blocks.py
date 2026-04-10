from app import db
from models import Caixa, EnderecoEstoque, Estoque, Fornecedor, FundoSolicitacao, ItemPedido, LancamentoFinanceiro, Pedido, Produto, RecebimentoFornecedor


def _create_supplier_and_stock():
    fornecedor = Fornecedor(nome='Fornecedor Regras', ativo=True)
    estoque = Estoque(nome='CD Regras', ativo=True)
    db.session.add_all([fornecedor, estoque])
    db.session.flush()
    endereco = EnderecoEstoque(
        estoque_id=estoque.id,
        nome='Endereco Regras',
        loja_cd='LJ01',
        setor_zona='deposito',
        tipo_area='recebimento',
        status='ativo',
        tipo_estrutura='rack',
        codigo_armazem='LJ01',
        rua_corredor='02',
        coluna_baia='01',
        nivel_prateleira='01',
        posicao_slot='01',
        lado='LA',
        controle_validade='fifo',
        codigo_localizacao='LJ01-DEP-R02-RK01-N01-V01-LA',
        ativo=True,
    )
    db.session.add(endereco)
    db.session.commit()
    return fornecedor, estoque, endereco


def test_finalized_order_cannot_be_edited(authenticated_client, produto, caixa, csrf_token):
    pedido = Pedido(caixa_id=caixa.id, status=Pedido.STATUS_FECHADO, total=10.0, estoque_processado=True, financeiro_processado=True)
    db.session.add(pedido)
    db.session.flush()
    db.session.add(ItemPedido(pedido_id=pedido.id, produto_id=produto.id, quantidade=1, preco_unitario=produto.preco_venda))
    db.session.commit()

    response = authenticated_client.post(f'/pedidos/{pedido.id}/editar', data={
        'status': Pedido.STATUS_FECHADO,
        'observacoes': 'tentativa de alteracao',
        'item_count': 1,
        'produto_0': produto.id,
        'quantidade_0': 2,
        'csrf_token': csrf_token,
    })
    assert response.status_code == 302
    db.session.refresh(pedido)
    assert pedido.observacoes != 'tentativa de alteracao'


def test_saida_estoque_exige_motivo_classificado(authenticated_client, produto, csrf_token):
    estoque_inicial = produto.quantidade_estoque
    response = authenticated_client.post('/movimentacoes/nova', data={
        'produto_id': produto.id,
        'tipo': 'saida',
        'quantidade': 2,
        'csrf_token': csrf_token,
    })
    assert response.status_code == 302
    db.session.refresh(produto)
    assert produto.quantidade_estoque == estoque_inicial


def test_estoque_nao_pode_ficar_negativo_em_saida(authenticated_client, produto, csrf_token):
    response = authenticated_client.post('/movimentacoes/nova', data={
        'produto_id': produto.id,
        'tipo': 'saida',
        'quantidade': produto.quantidade_estoque + 5,
        'motivo': 'uso_interno',
        'csrf_token': csrf_token,
    })
    assert response.status_code == 302
    db.session.refresh(produto)
    assert produto.quantidade_estoque == 10


def test_produto_ativo_exige_cadastro_minimo(authenticated_client, categoria, csrf_token):
    fornecedor = Fornecedor(nome='Fornecedor Produto', ativo=True)
    db.session.add(fornecedor)
    db.session.commit()

    response = authenticated_client.post('/produtos/novo', data={
        'codigo': 'P999',
        'nome': 'Produto Invalido',
        'categoria_id': categoria.id,
        'fornecedor_id': fornecedor.id,
        'preco_custo': '5',
        'preco_venda': '0',
        'quantidade_estoque': '1',
        'quantidade_minima': '1',
        'csrf_token': csrf_token,
    })
    assert response.status_code == 200
    assert Produto.query.filter_by(codigo='P999').first() is None


def test_recebimento_nao_pode_ser_armazenado_sem_conferencia(authenticated_client, produto, csrf_token):
    fornecedor, _, endereco = _create_supplier_and_stock()
    create_response = authenticated_client.post('/estoque/recebimentos/novo', data={
        'fornecedor_id': fornecedor.id,
        'tipo_recebimento': RecebimentoFornecedor.TIPO_COMPRA_REVENDA,
        'local_recebimento_id': endereco.id,
        'info_nota': 'NF-BLOCK',
        'produto_id[]': [produto.id],
        'qtd_recebida[]': ['2'],
        'csrf_token': csrf_token,
    })
    assert create_response.status_code == 302
    recebimento = RecebimentoFornecedor.query.filter_by(info_nota='NF-BLOCK').first()

    response = authenticated_client.post(f'/estoque/recebimentos/{recebimento.id}/armazenar', data={
        'csrf_token': csrf_token,
    })
    assert response.status_code == 302
    db.session.refresh(recebimento)
    assert recebimento.status == RecebimentoFornecedor.STATUS_CRIADO


def test_solicitacao_fundo_nao_pode_ser_liberada_sem_aprovacao(authenticated_client, admin_user, csrf_token):
    fundo = FundoSolicitacao(
        tipo=FundoSolicitacao.TIPO_APORTE,
        descricao='Fundo sem aprovacao',
        valor=100.0,
        status=FundoSolicitacao.STATUS_SOLICITADA,
        solicitado_por_id=admin_user.id,
    )
    db.session.add(fundo)
    db.session.commit()

    response = authenticated_client.post('/financeiro/fundos', data={
        'acao': 'liberar',
        'fundo_id': fundo.id,
        'csrf_token': csrf_token,
    })
    assert response.status_code == 302
    db.session.refresh(fundo)
    assert fundo.status == FundoSolicitacao.STATUS_SOLICITADA
    assert fundo.lancamento_financeiro_id is None


def test_lancamento_financeiro_critico_exige_referencia_e_centro_custo(authenticated_client, produto, csrf_token):
    response = authenticated_client.post('/financeiro/lancamentos', data={
        'tipo': LancamentoFinanceiro.TIPO_CONSUMO_PROPRIO,
        'descricao': 'Consumo interno sem lastro',
        'produto_id': produto.id,
        'quantidade': '2',
        'csrf_token': csrf_token,
    })
    assert response.status_code == 302
    assert LancamentoFinanceiro.query.count() == 0


def test_transferencia_exige_origem_destino_validos_e_diferentes(authenticated_client, produto, csrf_token):
    _, _, endereco = _create_supplier_and_stock()
    produto.endereco_id = endereco.id
    db.session.commit()

    response = authenticated_client.post('/movimentacoes/transferencia', data={
        'produto_id': produto.id,
        'endereco_destino_id': endereco.id,
        'motivo': 'reposicao_loja',
        'csrf_token': csrf_token,
    })
    assert response.status_code == 302
    db.session.refresh(produto)
    assert produto.endereco_id == endereco.id


def test_cancelamentos_exigem_motivo(authenticated_client, produto, caixa, csrf_token):
    pedido = Pedido(caixa_id=caixa.id, status=Pedido.STATUS_ABERTO)
    db.session.add(pedido)
    db.session.flush()
    db.session.add(ItemPedido(pedido_id=pedido.id, produto_id=produto.id, quantidade=1, preco_unitario=produto.preco_venda))
    db.session.commit()

    response = authenticated_client.post(f'/pedidos/{pedido.id}/status', data={
        'status': Pedido.STATUS_CANCELADO,
        'csrf_token': csrf_token,
    })
    assert response.status_code == 302
    db.session.refresh(pedido)
    assert pedido.status == Pedido.STATUS_ABERTO
