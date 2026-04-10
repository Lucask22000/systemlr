import pytest

from app.services.estoque_service import registrar_movimentacao_manual, transferir_estoque
from app.services.financeiro_operacional import aplicar_acao_fundo, criar_lancamento_financeiro
from app.services.pedido import _processar_fechamento_pedido
from app.services.recebimento_service import armazenar_recebimento, conferir_recebimento, create_recebimento
from models import (
    AuditoriaEvento,
    Caixa,
    EnderecoEstoque,
    Estoque,
    Fornecedor,
    FundoSolicitacao,
    ItemPedido,
    LancamentoFinanceiro,
    Movimentacao,
    MovimentacaoCaixa,
    Pedido,
    RecebimentoFornecedor,
    RecebimentoItem,
    db,
)


def _setup_enderecos():
    fornecedor = Fornecedor(nome='Fornecedor TX', ativo=True)
    estoque_a = Estoque(nome='Estoque A', ativo=True)
    estoque_b = Estoque(nome='Estoque B', ativo=True)
    db.session.add_all([fornecedor, estoque_a, estoque_b])
    db.session.flush()

    origem = EnderecoEstoque(
        estoque_id=estoque_a.id,
        nome='Origem TX',
        loja_cd='LJ01',
        setor_zona='deposito',
        tipo_area='recebimento',
        status='ativo',
        tipo_estrutura='rack',
        codigo_armazem='LJ01',
        rua_corredor='10',
        coluna_baia='01',
        nivel_prateleira='01',
        posicao_slot='01',
        lado='LA',
        controle_validade='fifo',
        codigo_localizacao='LJ01-DEP-R10-RK01-N01-V01-LA',
        ativo=True,
    )
    destino = EnderecoEstoque(
        estoque_id=estoque_b.id,
        nome='Destino TX',
        loja_cd='LJ02',
        setor_zona='deposito',
        tipo_area='armazenagem',
        status='ativo',
        tipo_estrutura='rack',
        codigo_armazem='LJ02',
        rua_corredor='11',
        coluna_baia='01',
        nivel_prateleira='01',
        posicao_slot='01',
        lado='LB',
        controle_validade='fifo',
        codigo_localizacao='LJ02-DEP-R11-RK01-N01-V01-LB',
        ativo=True,
    )
    db.session.add_all([origem, destino])
    db.session.flush()
    return fornecedor, origem, destino


def test_finalizacao_pedido_rollback_sem_efeito_parcial(db_session, produto, caixa):
    pedido = Pedido(
        caixa_id=caixa.id,
        status=Pedido.STATUS_ABERTO,
        total=20.0,
        estoque_processado=False,
        financeiro_processado=False,
    )
    db.session.add(pedido)
    db.session.flush()
    db.session.add(ItemPedido(pedido_id=pedido.id, produto_id=produto.id, quantidade=2, preco_unitario=produto.preco_venda))
    db.session.commit()

    with pytest.raises(RuntimeError):
        _processar_fechamento_pedido(pedido, failure_hook=lambda etapa: (_ for _ in ()).throw(RuntimeError('falha tx')))

    db.session.refresh(produto)
    db.session.refresh(pedido)
    db.session.refresh(caixa)
    assert produto.quantidade_estoque == 10
    assert pedido.estoque_processado is False
    assert pedido.financeiro_processado is False
    assert Movimentacao.query.count() == 0
    assert MovimentacaoCaixa.query.count() == 0
    assert caixa.saldo_atual == caixa.saldo_inicial


def test_baixa_estoque_rollback_em_falha(db_session, produto):
    with pytest.raises(RuntimeError):
        registrar_movimentacao_manual(
            produto=produto,
            tipo=Movimentacao.TIPO_SAIDA,
            quantidade=3,
            motivo='uso_interno',
            failure_hook=lambda etapa: (_ for _ in ()).throw(RuntimeError('falha tx')),
        )

    db.session.refresh(produto)
    assert produto.quantidade_estoque == 10
    assert Movimentacao.query.count() == 0


def test_recebimento_armazenagem_rollback_sem_efeito_parcial(db_session, admin_user, produto):
    fornecedor, origem, destino = _setup_enderecos()
    recebimento = create_recebimento(
        fornecedor=fornecedor,
        local_recebimento=origem,
        tipo_recebimento=RecebimentoFornecedor.TIPO_COMPRA_REVENDA,
        itens_processados=[
            {
                'produto_id': produto.id,
                'qtd_recebida': 4,
                'unidade': 'UN',
                'descricao_item': produto.nome,
                'preco_unitario': 4.0,
                'total_item': 16.0,
            }
        ],
        info_nota='NF-TX-001',
    )
    db.session.flush()
    item = recebimento.itens[0]
    conferir_recebimento(
        recebimento,
        conferencias_por_item={item.id: {'qtd_recebida': '4', 'qtd_avaria': '1', 'validade': '2027-01-01'}},
        actor=admin_user,
    )
    db.session.commit()

    with pytest.raises(RuntimeError):
        armazenar_recebimento(
            recebimento,
            destinos_por_item={item.id: destino},
            actor=admin_user,
            categoria_quimico_predicate=lambda _: False,
            tipo_labels={RecebimentoFornecedor.TIPO_COMPRA_REVENDA: 'Compra'},
            failure_hook=lambda etapa: (_ for _ in ()).throw(RuntimeError('falha tx')),
        )

    db.session.refresh(produto)
    db.session.refresh(recebimento)
    db.session.refresh(item)
    assert produto.quantidade_estoque == 10
    assert produto.endereco_id is None
    assert item.endereco_destino_id is None
    assert recebimento.status == RecebimentoFornecedor.STATUS_AGUARDANDO_ARMAZENAGEM
    assert Movimentacao.query.count() == 0
    assert AuditoriaEvento.query.filter_by(entidade='recebimento').count() == 1


def test_transferencia_rollback_sem_mudar_endereco(db_session, produto):
    _, origem, destino = _setup_enderecos()
    produto.endereco_id = origem.id
    db.session.commit()

    with pytest.raises(RuntimeError):
        transferir_estoque(
            produto=produto,
            endereco_origem=origem,
            endereco_destino=destino,
            motivo='reposicao_loja',
            failure_hook=lambda etapa: (_ for _ in ()).throw(RuntimeError('falha tx')),
        )

    db.session.refresh(produto)
    assert produto.endereco_id == origem.id
    assert Movimentacao.query.count() == 0


def test_liberacao_fundo_rollback_sem_lancamento_parcial(db_session, admin_user):
    fundo = FundoSolicitacao(
        tipo=FundoSolicitacao.TIPO_APORTE,
        descricao='Fundo TX',
        valor=200.0,
        status=FundoSolicitacao.STATUS_APROVADA,
        solicitado_por_id=admin_user.id,
        aprovado_por_id=admin_user.id,
    )
    db.session.add(fundo)
    db.session.commit()

    with pytest.raises(RuntimeError):
        aplicar_acao_fundo(
            fundo,
            acao='liberar',
            actor=admin_user,
            failure_hook=lambda etapa: (_ for _ in ()).throw(RuntimeError('falha tx')),
        )

    db.session.refresh(fundo)
    assert fundo.status == FundoSolicitacao.STATUS_APROVADA
    assert fundo.lancamento_financeiro_id is None
    assert LancamentoFinanceiro.query.count() == 0
    assert AuditoriaEvento.query.filter_by(entidade='fundo').count() == 0


def test_lancamento_financeiro_vinculado_rollback_sem_registro(db_session, admin_user, produto):
    with pytest.raises(RuntimeError):
        criar_lancamento_financeiro(
            tipo=LancamentoFinanceiro.TIPO_CONSUMO_PROPRIO,
            descricao='Consumo TX',
            valor=0.0,
            referencia_documento='REQ-TX',
            centro_custo='OPERACAO',
            produto=produto,
            quantidade=2,
            criado_por_id=admin_user.id,
            failure_hook=lambda etapa: (_ for _ in ()).throw(RuntimeError('falha tx')),
        )

    assert LancamentoFinanceiro.query.count() == 0
