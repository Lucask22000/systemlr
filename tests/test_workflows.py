import pytest

from app.exceptions import BusinessRuleError, ValidationError
from app.services.workflow import (
    ExpedicaoStatus,
    FundoStatus,
    RecebimentoStatus,
    transition_expedicao_status,
    transition_fundo_status,
    transition_pedido_status,
    transition_recebimento_status,
)
from models import (
    AuditoriaEvento,
    Caixa,
    EnderecoEstoque,
    Estoque,
    Fornecedor,
    FundoSolicitacao,
    ItemPedido,
    Pedido,
    RecebimentoFornecedor,
    RecebimentoItem,
    db,
)


def _criar_caixa_aberto():
    caixa = Caixa(
        nome='Caixa Workflow',
        saldo_inicial=50.0,
        saldo_atual=50.0,
        aberto=True,
    )
    db.session.add(caixa)
    db.session.flush()
    return caixa


def _criar_recebimento_basico(produto):
    fornecedor = Fornecedor(nome='Fornecedor Workflow', ativo=True)
    estoque = Estoque(nome='CD Workflow', ativo=True)
    db.session.add_all([fornecedor, estoque])
    db.session.flush()

    endereco = EnderecoEstoque(
        estoque_id=estoque.id,
        nome='Endereco Workflow',
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
    db.session.add(endereco)
    db.session.flush()

    recebimento = RecebimentoFornecedor(
        fornecedor_id=fornecedor.id,
        local_recebimento_id=endereco.id,
        tipo_recebimento=RecebimentoFornecedor.TIPO_COMPRA_REVENDA,
        status=RecebimentoFornecedor.STATUS_CRIADO,
    )
    db.session.add(recebimento)
    db.session.flush()

    item = RecebimentoItem(
        recebimento_id=recebimento.id,
        produto_id=produto.id,
        qtd_recebida=5,
        qtd_avaria=1,
        unidade='UN',
        descricao_item=produto.nome,
        preco_unitario=produto.preco_custo,
        total_item=20.0,
    )
    db.session.add(item)
    db.session.flush()
    return recebimento, item, endereco


def test_pedido_state_machine_blocks_invalid_reopen_after_close(db_session, admin_user, produto):
    caixa = _criar_caixa_aberto()
    pedido = Pedido(caixa_id=caixa.id, status=Pedido.STATUS_ABERTO, estoque_processado=False, financeiro_processado=False)
    db.session.add(pedido)
    db.session.flush()
    db.session.add(
        ItemPedido(
            pedido_id=pedido.id,
            produto_id=produto.id,
            quantidade=2,
            preco_unitario=produto.preco_venda,
        )
    )
    pedido.total = 20.0

    transition_pedido_status(pedido, Pedido.STATUS_FECHADO, actor=admin_user, on_fechamento=lambda item: None)
    db.session.commit()

    with pytest.raises(BusinessRuleError):
        transition_pedido_status(pedido, Pedido.STATUS_ABERTO, actor=admin_user, on_fechamento=lambda item: None)


def test_recebimento_state_machine_requires_destination_before_conclusion(db_session, admin_user, produto):
    recebimento, item, _ = _criar_recebimento_basico(produto)

    transition_recebimento_status(recebimento, RecebimentoStatus.AGUARDANDO_ARMAZENAGEM, actor=admin_user)
    db.session.commit()

    with pytest.raises(BusinessRuleError):
        transition_recebimento_status(recebimento, RecebimentoStatus.CONCLUIDO, actor=admin_user)

    assert AuditoriaEvento.query.filter_by(entidade='recebimento').count() == 1
    assert item.endereco_destino_id is None


def test_expedicao_state_machine_blocks_dispatch_before_separation(db_session, admin_user):
    pedido = Pedido(status=Pedido.STATUS_ABERTO, origem='site')
    db.session.add(pedido)
    db.session.flush()

    with pytest.raises(BusinessRuleError):
        transition_expedicao_status(
            pedido,
            ExpedicaoStatus.EM_ROTA,
            actor=admin_user,
            enabled=True,
            allowed_origins={'site'},
        )


def test_expedicao_state_machine_marks_order_as_delivered(db_session, admin_user):
    pedido = Pedido(status=Pedido.STATUS_ABERTO, origem='site')
    db.session.add(pedido)
    db.session.flush()

    transition_expedicao_status(
        pedido,
        ExpedicaoStatus.SEPARADO,
        actor=admin_user,
        enabled=True,
        allowed_origins={'site'},
        metadata={'rota_entrega': 'Rota 1'},
    )
    transition_expedicao_status(
        pedido,
        ExpedicaoStatus.EM_ROTA,
        actor=admin_user,
        enabled=True,
        allowed_origins={'site'},
    )
    transition_expedicao_status(
        pedido,
        ExpedicaoStatus.ENTREGUE,
        actor=admin_user,
        enabled=True,
        allowed_origins={'site'},
    )
    db.session.commit()

    assert pedido.status == Pedido.STATUS_ENTREGUE
    assert pedido.separacao_entrega_concluida is True
    assert pedido.saiu_para_entrega_em is not None
    assert pedido.entrega_concluida_em is not None
    assert AuditoriaEvento.query.filter_by(entidade='expedicao').count() == 3


def test_fundo_state_machine_requires_rejection_reason_and_generates_lancamento(db_session, admin_user):
    fundo = FundoSolicitacao(
        tipo=FundoSolicitacao.TIPO_APORTE,
        descricao='Aporte emergencial',
        valor=150.0,
        status=FundoSolicitacao.STATUS_SOLICITADA,
        solicitado_por_id=admin_user.id,
    )
    db.session.add(fundo)
    db.session.flush()

    with pytest.raises(ValidationError):
        transition_fundo_status(fundo, FundoStatus.REJEITADA, actor=admin_user, motivo_rejeicao='')

    transition_fundo_status(fundo, FundoStatus.APROVADA, actor=admin_user)
    transition_fundo_status(fundo, FundoStatus.LIBERADA, actor=admin_user)
    db.session.commit()

    assert fundo.status == FundoSolicitacao.STATUS_LIBERADA
    assert fundo.lancamento_financeiro_id is not None
    assert AuditoriaEvento.query.filter_by(entidade='fundo').count() == 2
