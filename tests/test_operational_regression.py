import pytest

from app import db
from app.exceptions import BusinessRuleError
from app.services.estoque_service import transferir_estoque
from app.services.financeiro_operacional import aplicar_acao_fundo
from app.services.pedido import _processar_fechamento_pedido, create_order
from app.services.recebimento_service import armazenar_recebimento, create_recebimento
from app.services.workflow import ExpedicaoStatus, transition_expedicao_status, transition_pedido_status
from models import (
    Caixa,
    EnderecoEstoque,
    Estoque,
    Fornecedor,
    FundoSolicitacao,
    Funcionario,
    ItemPedido,
    Movimentacao,
    MovimentacaoCaixa,
    Pedido,
    PermissaoAcesso,
    ProcessoEvento,
    Produto,
    RecebimentoFornecedor,
)


def _create_supplier_and_addresses():
    fornecedor = Fornecedor(
        nome='Fornecedor Regressao',
        documento='12345678000199',
        telefone='65999999999',
        endereco_cidade='Cuiaba',
        tipo_produtos_fornece='mercearia',
        ativo=True,
    )
    estoque_origem = Estoque(nome='CD Origem', codigo_filial='CD01', ativo=True)
    estoque_destino = Estoque(nome='Loja Destino', codigo_filial='LJ01', ativo=True)
    db.session.add_all([fornecedor, estoque_origem, estoque_destino])
    db.session.flush()

    endereco_origem = EnderecoEstoque(
        estoque_id=estoque_origem.id,
        nome='Dock Origem',
        loja_cd='CD01',
        setor_zona='deposito',
        tipo_area='recebimento',
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
    endereco_destino = EnderecoEstoque(
        estoque_id=estoque_destino.id,
        nome='Box Destino',
        loja_cd='LJ01',
        setor_zona='deposito',
        tipo_area='armazenagem',
        status='ativo',
        tipo_estrutura='rack',
        codigo_armazem='LJ01',
        rua_corredor='02',
        coluna_baia='01',
        nivel_prateleira='01',
        posicao_slot='01',
        lado='LB',
        controle_validade='fifo',
        codigo_localizacao='LJ01-DEP-R02-RK01-N01-V01-LB',
        ativo=True,
    )
    db.session.add_all([endereco_origem, endereco_destino])
    db.session.commit()
    return fornecedor, endereco_origem, endereco_destino


def _login_as(client, usuario, csrf_token):
    with client.session_transaction() as sess:
        sess['funcionario_id'] = usuario.id
        sess['funcionario_nome'] = usuario.nome
        sess['funcionario_role'] = usuario.role
        sess['_csrf_token'] = csrf_token


class TestPedidosRegressao:
    def test_pedido_finalizado_nao_pode_ser_alterado(self, authenticated_client, produto, caixa, csrf_token):
        pedido = Pedido(
            caixa_id=caixa.id,
            status=Pedido.STATUS_FECHADO,
            total=10.0,
            estoque_processado=True,
            financeiro_processado=True,
        )
        db.session.add(pedido)
        db.session.flush()
        db.session.add(
            ItemPedido(
                pedido_id=pedido.id,
                produto_id=produto.id,
                quantidade=1,
                preco_unitario=produto.preco_venda,
            )
        )
        db.session.commit()

        response = authenticated_client.post(
            f'/pedidos/{pedido.id}/editar',
            data={
                'status': Pedido.STATUS_FECHADO,
                'observacoes': 'tentativa de alteracao',
                'item_count': 1,
                'produto_0': produto.id,
                'quantidade_0': 3,
                'csrf_token': csrf_token,
            },
        )

        assert response.status_code == 302
        db.session.refresh(pedido)
        assert pedido.observacoes != 'tentativa de alteracao'
        assert pedido.total == 10.0

    def test_pedido_cancelado_nao_gera_baixa_indevida_de_estoque(self, db_session, admin_user, produto, caixa):
        pedido = create_order(
            caixa=caixa,
            itens_payload=[{'produto_id': produto.id, 'quantidade': 2}],
            actor=admin_user,
        )
        db.session.commit()

        transition_pedido_status(
            pedido,
            Pedido.STATUS_CANCELADO,
            actor=admin_user,
            detalhes='cliente desistiu',
        )
        db.session.commit()

        db.session.refresh(produto)
        db.session.refresh(pedido)
        assert pedido.status == Pedido.STATUS_CANCELADO
        assert produto.quantidade_estoque == 10
        assert Movimentacao.query.filter_by(pedido_id=pedido.id).count() == 0

    def test_pedido_nao_pode_ser_entregue_sem_separacao(self, db_session, admin_user, produto, caixa):
        pedido = create_order(
            caixa=caixa,
            itens_payload=[{'produto_id': produto.id, 'quantidade': 1}],
            actor=admin_user,
        )
        pedido.origem = 'site'
        db.session.commit()

        with pytest.raises(BusinessRuleError):
            transition_expedicao_status(
                pedido,
                ExpedicaoStatus.ENTREGUE,
                actor=admin_user,
                enabled=True,
            )

        db.session.refresh(pedido)
        assert pedido.separacao_entrega_concluida in (False, None)
        assert pedido.entrega_concluida_em is None


class TestEstoqueRegressao:
    def test_estoque_nao_pode_ficar_negativo(self, authenticated_client, produto, csrf_token):
        response = authenticated_client.post(
            '/movimentacoes/nova',
            data={
                'produto_id': produto.id,
                'tipo': 'saida',
                'quantidade': produto.quantidade_estoque + 1,
                'motivo': 'uso_interno',
                'csrf_token': csrf_token,
            },
        )

        assert response.status_code == 302
        db.session.refresh(produto)
        assert produto.quantidade_estoque == 10

    def test_transferencia_entre_estoques_mantem_integridade_do_saldo_atual(self, db_session, admin_user, produto):
        _, endereco_origem, endereco_destino = _create_supplier_and_addresses()
        produto.endereco_id = endereco_origem.id
        produto.quantidade_estoque = 10
        db.session.commit()

        movimentacao = transferir_estoque(
            produto=produto,
            endereco_origem=endereco_origem,
            endereco_destino=endereco_destino,
            motivo='reposicao_loja',
            actor=admin_user,
        )
        db.session.commit()

        db.session.refresh(produto)
        assert produto.quantidade_estoque == 10
        assert produto.endereco_id == endereco_destino.id
        assert movimentacao.quantidade == 10
        assert movimentacao.endereco_origem_id == endereco_origem.id
        assert movimentacao.endereco_destino_id == endereco_destino.id


class TestRecebimentoRegressao:
    def test_recebimento_nao_pode_ser_armazenado_sem_conferencia(self, db_session, admin_user, produto):
        fornecedor, endereco_origem, endereco_destino = _create_supplier_and_addresses()
        recebimento = create_recebimento(
            fornecedor=fornecedor,
            local_recebimento=endereco_origem,
            tipo_recebimento=RecebimentoFornecedor.TIPO_COMPRA_REVENDA,
            itens_processados=[
                {
                    'produto_id': produto.id,
                    'qtd_recebida': 3,
                    'unidade': 'UN',
                    'descricao_item': produto.nome,
                    'preco_unitario': 4.0,
                    'total_item': 12.0,
                }
            ],
            info_nota='NF-REG-001',
        )
        db.session.commit()

        with pytest.raises(BusinessRuleError):
            armazenar_recebimento(
                recebimento,
                destinos_por_item={recebimento.itens[0].id: endereco_destino},
                actor=admin_user,
                categoria_quimico_predicate=lambda _: False,
                tipo_labels={RecebimentoFornecedor.TIPO_COMPRA_REVENDA: 'Compra'},
            )

        db.session.refresh(recebimento)
        db.session.refresh(produto)
        assert recebimento.status == RecebimentoFornecedor.STATUS_CRIADO
        assert produto.quantidade_estoque == 10


class TestPermissoesRegressao:
    def test_perfil_sem_permissao_nao_acessa_acao_critica(self, client, db_session, caixa, produto, csrf_token):
        usuario = Funcionario(
            nome='Gerente Restrito',
            email='gerente-restrito@test.local',
            role='gerente',
            ativo=True,
            controle_acesso_ativo=True,
        )
        usuario.set_password('123456')
        db.session.add(usuario)
        db.session.flush()
        db.session.add(PermissaoAcesso(funcionario_id=usuario.id, pagina='inicio'))
        db.session.commit()

        _login_as(client, usuario, csrf_token)

        response = client.post(
            '/api/pedidos/criar',
            json={
                'caixa_id': caixa.id,
                'itens': [{'produto_id': produto.id, 'quantidade': 1}],
            },
            headers={'X-CSRF-Token': csrf_token},
        )

        assert response.status_code == 403
        payload = response.get_json()
        assert payload['success'] is False
        assert payload['code'] == 'forbidden'


class TestFinanceiroRegressao:
    def test_solicitacao_rejeitada_nao_pode_ser_liberada(self, db_session, admin_user):
        fundo = FundoSolicitacao(
            tipo=FundoSolicitacao.TIPO_APORTE,
            descricao='Solicitacao rejeitada',
            valor=100.0,
            status=FundoSolicitacao.STATUS_REJEITADA,
            solicitado_por_id=admin_user.id,
            aprovado_por_id=admin_user.id,
            motivo_rejeicao='valor fora da politica',
        )
        db.session.add(fundo)
        db.session.commit()

        with pytest.raises(BusinessRuleError):
            aplicar_acao_fundo(fundo, acao='liberar', actor=admin_user)

        db.session.refresh(fundo)
        assert fundo.status == FundoSolicitacao.STATUS_REJEITADA
        assert fundo.lancamento_financeiro_id is None


class TestTransacoesRegressao:
    def test_erro_no_meio_do_fechamento_gera_rollback_completo(self, db_session, admin_user, produto, caixa):
        pedido = create_order(
            caixa=caixa,
            itens_payload=[{'produto_id': produto.id, 'quantidade': 2}],
            actor=admin_user,
        )
        db.session.commit()

        with pytest.raises(RuntimeError):
            _processar_fechamento_pedido(
                pedido,
                actor=admin_user,
                failure_hook=lambda etapa: (_ for _ in ()).throw(RuntimeError(f'falha em {etapa}')),
            )

        db.session.refresh(produto)
        db.session.refresh(caixa)
        db.session.refresh(pedido)
        assert produto.quantidade_estoque == 10
        assert caixa.saldo_atual == caixa.saldo_inicial
        assert pedido.estoque_processado is False
        assert pedido.financeiro_processado is False
        assert Movimentacao.query.filter_by(pedido_id=pedido.id).count() == 0
        assert MovimentacaoCaixa.query.count() == 0
        assert ProcessoEvento.query.filter_by(pedido_id=pedido.id).count() == 1
