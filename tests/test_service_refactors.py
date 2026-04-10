from datetime import date

import pytest

from app import db
from app.exceptions import BusinessRuleError
from app.services.estoque_service import registrar_movimentacao_manual, transferir_estoque
from app.services.financeiro_operacional import aplicar_acao_fundo, criar_lancamento_financeiro, criar_solicitacao_fundo
from app.services.pedido_service import create_order, update_order
from app.services.recebimento_service import armazenar_recebimento, conferir_recebimento, create_recebimento
from models import (
    AuditoriaEvento,
    EnderecoEstoque,
    Estoque,
    Fornecedor,
    FundoSolicitacao,
    ItemPedido,
    LancamentoFinanceiro,
    Movimentacao,
    Pedido,
    RecebimentoFornecedor,
    Produto,
)


def _criar_estrutura_estoque():
    fornecedor = Fornecedor(nome='Fornecedor Service', ativo=True)
    estoque_origem = Estoque(nome='Origem Service', ativo=True)
    estoque_destino = Estoque(nome='Destino Service', ativo=True)
    db.session.add_all([fornecedor, estoque_origem, estoque_destino])
    db.session.flush()

    endereco_origem = EnderecoEstoque(
        estoque_id=estoque_origem.id,
        nome='Origem A1',
        loja_cd='LJ01',
        setor_zona='deposito',
        tipo_area='recebimento',
        status='ativo',
        tipo_estrutura='rack',
        codigo_armazem='LJ01',
        rua_corredor='01',
        coluna_baia='01',
        nivel_prateleira='01',
        posicao_slot='01',
        lado='LA',
        controle_validade='fifo',
        codigo_localizacao='LJ01-DEP-R01-RK01-N01-V01-LA',
        ativo=True,
    )
    endereco_destino = EnderecoEstoque(
        estoque_id=estoque_destino.id,
        nome='Destino B1',
        loja_cd='LJ02',
        setor_zona='deposito',
        tipo_area='armazenagem',
        status='ativo',
        tipo_estrutura='rack',
        codigo_armazem='LJ02',
        rua_corredor='02',
        coluna_baia='01',
        nivel_prateleira='01',
        posicao_slot='01',
        lado='LB',
        controle_validade='fifo',
        codigo_localizacao='LJ02-DEP-R02-RK01-N01-V01-LB',
        ativo=True,
    )
    db.session.add_all([endereco_origem, endereco_destino])
    db.session.flush()
    return fornecedor, endereco_origem, endereco_destino


def test_create_order_service_creates_items_and_total(db_session, caixa, produto):
    pedido = create_order(
        caixa=caixa,
        itens_payload=[{'produto_id': produto.id, 'quantidade': 2}],
    )
    db.session.commit()

    assert pedido.status == Pedido.STATUS_ABERTO
    assert pedido.total == 20.0
    assert len(pedido.itens) == 1
    assert pedido.itens[0].quantidade == 2


def test_update_order_service_replaces_items_without_route_logic(db_session, caixa, produto):
    pedido = Pedido(caixa_id=caixa.id, status=Pedido.STATUS_ABERTO)
    db.session.add(pedido)
    db.session.flush()
    db.session.add(ItemPedido(pedido_id=pedido.id, produto_id=produto.id, quantidade=1, preco_unitario=produto.preco_venda))
    db.session.flush()

    update_order(
        pedido,
        novo_status=Pedido.STATUS_ABERTO,
        caixa=caixa,
        observacoes='Atualizado pelo service',
        itens_payload=[{'produto_id': produto.id, 'quantidade': 3}],
    )
    db.session.commit()

    assert pedido.observacoes == 'Atualizado pelo service'
    assert pedido.total == 30.0
    assert len(pedido.itens) == 1
    assert pedido.itens[0].quantidade == 3


def test_registrar_movimentacao_manual_service_generates_record(db_session, produto):
    movimentacao = registrar_movimentacao_manual(
        produto=produto,
        tipo=Movimentacao.TIPO_SAIDA,
        quantidade=2,
        motivo='uso_interno',
        observacoes='Teste service',
    )
    db.session.add(movimentacao)
    db.session.commit()

    assert produto.quantidade_estoque == 8
    assert movimentacao.motivo == 'uso_interno'
    assert movimentacao.tipo == Movimentacao.TIPO_SAIDA


def test_transferir_estoque_service_updates_address_and_registers_transfer(db_session, produto):
    _, endereco_origem, endereco_destino = _criar_estrutura_estoque()
    produto.endereco_id = endereco_origem.id
    db.session.commit()

    movimentacao = transferir_estoque(
        produto=produto,
        endereco_origem=endereco_origem,
        endereco_destino=endereco_destino,
        motivo='reposicao_loja',
        observacoes='Transferencia por service',
    )
    db.session.add(movimentacao)
    db.session.commit()

    assert produto.endereco_id == endereco_destino.id
    assert movimentacao.tipo == Movimentacao.TIPO_TRANSFERENCIA
    assert movimentacao.endereco_origem_id == endereco_origem.id


def test_create_recebimento_service_persists_items_and_totals(db_session, produto):
    fornecedor, endereco_origem, _ = _criar_estrutura_estoque()
    recebimento = create_recebimento(
        fornecedor=fornecedor,
        local_recebimento=endereco_origem,
        tipo_recebimento=RecebimentoFornecedor.TIPO_COMPRA_REVENDA,
        itens_processados=[
            {
                'produto_id': produto.id,
                'qtd_recebida': 4,
                'unidade': 'UN',
                'descricao_item': produto.nome,
                'preco_unitario': 5.0,
                'total_item': 20.0,
            }
        ],
        desconto=2.0,
        info_nota='NF-SERVICE-1',
    )
    db.session.commit()

    assert recebimento.subtotal == 20.0
    assert recebimento.total_pagar == 18.0
    assert len(recebimento.itens) == 1


def test_conferir_e_armazenar_recebimento_services_control_flow(db_session, admin_user, produto):
    fornecedor, endereco_origem, endereco_destino = _criar_estrutura_estoque()
    recebimento = create_recebimento(
        fornecedor=fornecedor,
        local_recebimento=endereco_origem,
        tipo_recebimento=RecebimentoFornecedor.TIPO_COMPRA_REVENDA,
        itens_processados=[
            {
                'produto_id': produto.id,
                'qtd_recebida': 5,
                'unidade': 'UN',
                'descricao_item': produto.nome,
                'preco_unitario': 4.0,
                'total_item': 20.0,
            }
        ],
        info_nota='NF-SERVICE-2',
    )
    db.session.flush()

    item = recebimento.itens[0]
    conferir_recebimento(
        recebimento,
        conferencias_por_item={
            item.id: {
                'qtd_recebida': '5',
                'qtd_avaria': '1',
                'lote': 'L001',
                'validade': '2026-12-31',
            }
        },
        actor=admin_user,
    )
    armazenar_recebimento(
        recebimento,
        destinos_por_item={item.id: endereco_destino},
        actor=admin_user,
        categoria_quimico_predicate=lambda _: False,
        tipo_labels={RecebimentoFornecedor.TIPO_COMPRA_REVENDA: 'Compra revenda'},
    )
    db.session.commit()

    db.session.refresh(produto)
    assert recebimento.status == RecebimentoFornecedor.STATUS_CONCLUIDO
    assert produto.quantidade_estoque == 14
    assert Movimentacao.query.filter_by(produto_id=produto.id, motivo='recebimento_fornecedor').count() == 1
    assert AuditoriaEvento.query.filter_by(entidade='recebimento').count() == 2


def test_criar_solicitacao_fundo_service_and_apply_action(db_session, admin_user):
    fundo = criar_solicitacao_fundo(
        tipo=FundoSolicitacao.TIPO_APORTE,
        descricao='Aporte service',
        valor=120.0,
        solicitado_por_id=admin_user.id,
    )
    db.session.flush()

    aplicar_acao_fundo(fundo, acao='aprovar', actor=admin_user)
    db.session.commit()

    assert fundo.status == FundoSolicitacao.STATUS_APROVADA
    assert fundo.aprovado_por_id == admin_user.id


def test_criar_lancamento_financeiro_service_computes_consumo_proprio(db_session, admin_user, produto):
    lancamento = criar_lancamento_financeiro(
        tipo=LancamentoFinanceiro.TIPO_CONSUMO_PROPRIO,
        descricao='Consumo interno service',
        valor=0.0,
        data_competencia=date(2026, 3, 19),
        incluir_contabilidade=True,
        referencia_documento='REQ-123',
        centro_custo='OPERACAO',
        produto=produto,
        quantidade=3,
        criado_por_id=admin_user.id,
    )
    db.session.commit()

    assert lancamento.valor == 12.0
    assert lancamento.produto_id == produto.id
    assert lancamento.quantidade == 3


def test_transferir_estoque_service_blocks_same_stock_transfer(db_session, produto):
    fornecedor = Fornecedor(nome='Fornecedor Same', ativo=True)
    estoque = Estoque(nome='Mesmo Estoque', ativo=True)
    db.session.add_all([fornecedor, estoque])
    db.session.flush()
    endereco_origem = EnderecoEstoque(
        estoque_id=estoque.id,
        nome='Origem',
        loja_cd='LJ01',
        setor_zona='deposito',
        tipo_area='recebimento',
        status='ativo',
        tipo_estrutura='rack',
        codigo_armazem='LJ01',
        rua_corredor='03',
        coluna_baia='01',
        nivel_prateleira='01',
        posicao_slot='01',
        lado='LA',
        controle_validade='fifo',
        codigo_localizacao='LJ01-DEP-R03-RK01-N01-V01-LA',
        ativo=True,
    )
    endereco_destino = EnderecoEstoque(
        estoque_id=estoque.id,
        nome='Destino',
        loja_cd='LJ01',
        setor_zona='deposito',
        tipo_area='armazenagem',
        status='ativo',
        tipo_estrutura='rack',
        codigo_armazem='LJ01',
        rua_corredor='04',
        coluna_baia='01',
        nivel_prateleira='01',
        posicao_slot='01',
        lado='LB',
        controle_validade='fifo',
        codigo_localizacao='LJ01-DEP-R04-RK01-N01-V01-LB',
        ativo=True,
    )
    db.session.add_all([endereco_origem, endereco_destino])
    db.session.flush()
    produto.endereco_id = endereco_origem.id

    with pytest.raises(BusinessRuleError):
        transferir_estoque(
            produto=produto,
            endereco_origem=endereco_origem,
            endereco_destino=endereco_destino,
            motivo='reposicao_loja',
        )
