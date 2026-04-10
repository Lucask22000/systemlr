from app import db
from app.services.financeiro_operacional import aplicar_acao_fundo, criar_solicitacao_fundo
from app.services.pedido_service import _aplicar_transicao_status, create_order
from app.services.recebimento_service import armazenar_recebimento, conferir_recebimento, create_recebimento
from app.services.traceability import build_timeline
from app.services.workflow import ExpedicaoStatus, transition_expedicao_status
from models import (
    Caixa,
    EnderecoEstoque,
    Estoque,
    Fornecedor,
    FundoSolicitacao,
    Movimentacao,
    Pedido,
    ProcessoEvento,
    RecebimentoFornecedor,
)


def _create_logistics_structure():
    fornecedor = Fornecedor(
        nome='Fornecedor Timeline',
        documento='123',
        telefone='65999999999',
        endereco_cidade='Cuiaba',
        tipo_produtos_fornece='Mercearia',
        ativo=True,
    )
    estoque_a = Estoque(nome='Estoque Timeline A', codigo_filial='EA', ativo=True)
    estoque_b = Estoque(nome='Estoque Timeline B', codigo_filial='EB', ativo=True)
    db.session.add_all([fornecedor, estoque_a, estoque_b])
    db.session.flush()
    origem = EnderecoEstoque(
        estoque_id=estoque_a.id,
        nome='Origem Timeline',
        loja_cd='LJ01',
        setor_zona='deposito',
        tipo_area='recebimento',
        status='ativo',
        tipo_estrutura='rack',
        codigo_armazem='LJ01',
        rua_corredor='21',
        coluna_baia='01',
        nivel_prateleira='01',
        posicao_slot='01',
        lado='LA',
        controle_validade='fifo',
        codigo_localizacao='LJ01-DEP-R21-RK01-N01-V01-LA',
        ativo=True,
    )
    destino = EnderecoEstoque(
        estoque_id=estoque_b.id,
        nome='Destino Timeline',
        loja_cd='LJ02',
        setor_zona='deposito',
        tipo_area='armazenagem',
        status='ativo',
        tipo_estrutura='rack',
        codigo_armazem='LJ02',
        rua_corredor='22',
        coluna_baia='01',
        nivel_prateleira='01',
        posicao_slot='01',
        lado='LB',
        controle_validade='fifo',
        codigo_localizacao='LJ02-DEP-R22-RK01-N01-V01-LB',
        ativo=True,
    )
    db.session.add_all([origem, destino])
    db.session.flush()
    return fornecedor, origem, destino


def test_pedido_timeline_tracks_sale_stock_and_delivery(db_session, admin_user, produto, caixa):
    pedido = create_order(
        caixa=caixa,
        itens_payload=[{'produto_id': produto.id, 'quantidade': 2}],
        actor=admin_user,
    )
    pedido.origem = 'site'
    db.session.flush()

    transition_expedicao_status(
        pedido,
        ExpedicaoStatus.SEPARADO,
        actor=admin_user,
        enabled=True,
        allowed_origins={'site'},
    )
    _aplicar_transicao_status(pedido, Pedido.STATUS_FECHADO, actor=admin_user)
    db.session.commit()

    timeline = build_timeline(pedido=pedido)
    acoes = [item['acao'] for item in timeline]

    assert 'pedido_criado' in acoes
    assert 'movimentacao_estoque_gerada' in acoes
    assert 'caixa_atualizado' in acoes
    assert 'pedido_fechado' in acoes
    assert 'expedicao_separado' in acoes
    assert Movimentacao.query.filter_by(pedido_id=pedido.id).count() == 1


def test_recebimento_timeline_tracks_conference_and_putaway(authenticated_client, admin_user, produto, csrf_token):
    fornecedor, origem, destino = _create_logistics_structure()
    response = authenticated_client.post('/estoque/recebimentos/novo', data={
        'fornecedor_id': fornecedor.id,
        'tipo_recebimento': RecebimentoFornecedor.TIPO_COMPRA_REVENDA,
        'local_recebimento_id': origem.id,
        'info_nota': 'NF-TIMELINE',
        'produto_id[]': [produto.id],
        'qtd_recebida[]': ['3'],
        'csrf_token': csrf_token,
    })
    assert response.status_code == 302
    recebimento = RecebimentoFornecedor.query.filter_by(info_nota='NF-TIMELINE').first()
    item = recebimento.itens[0]

    conferir_recebimento(
        recebimento,
        conferencias_por_item={item.id: {'qtd_recebida': '3', 'qtd_avaria': '0', 'validade': '2027-05-01'}},
        actor=admin_user,
    )
    armazenar_recebimento(
        recebimento,
        destinos_por_item={item.id: destino},
        actor=admin_user,
        categoria_quimico_predicate=lambda _: False,
        tipo_labels={RecebimentoFornecedor.TIPO_COMPRA_REVENDA: 'Compra'},
    )
    db.session.commit()

    api_response = authenticated_client.get(f'/api/rastreabilidade/recebimentos/{recebimento.id}/timeline')
    assert api_response.status_code == 200
    payload = api_response.get_json()
    acoes = [item['acao'] for item in payload['timeline']]
    assert 'recebimento_criado' in acoes
    assert 'recebimento_conferido' in acoes
    assert 'recebimento_armazenado' in acoes
    assert Movimentacao.query.filter_by(recebimento_id=recebimento.id).count() == 1


def test_fundo_timeline_links_financial_release(db_session, admin_user):
    fundo = criar_solicitacao_fundo(
        tipo=FundoSolicitacao.TIPO_APORTE,
        descricao='Fundo timeline',
        valor=150.0,
        solicitado_por_id=admin_user.id,
        actor=admin_user,
    )
    db.session.flush()
    aplicar_acao_fundo(fundo, acao='aprovar', actor=admin_user)
    aplicar_acao_fundo(fundo, acao='liberar', actor=admin_user)
    db.session.commit()

    timeline = build_timeline(fundo=fundo)
    assert any(item['acao'] == 'solicitacao_fundo_criada' for item in timeline)
    assert any(item['acao'] == 'fundo_aprovada' for item in timeline)
    evento_liberacao = next(item for item in timeline if item['acao'] == 'fundo_liberada')
    assert evento_liberacao['lancamento_financeiro_id'] is not None
    assert ProcessoEvento.query.filter_by(fundo_solicitacao_id=fundo.id).count() >= 3
