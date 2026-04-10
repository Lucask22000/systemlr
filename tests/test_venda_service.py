from datetime import date, datetime, timedelta

import pytest

from app import db
from app.exceptions import ValidationError
from app.services.pedido_service import create_order
from app.services.venda_service import VendaService
from models import ItemPedido, LancamentoFinanceiro, Movimentacao, MovimentacaoCaixa, Pedido, Produto


def test_venda_service_processa_venda_rapida_de_forma_atomica(db_session, admin_user, caixa, produto):
    pedido = create_order(
        caixa=caixa,
        itens_payload=[{'produto_id': produto.id, 'quantidade': 8}],
        actor=admin_user,
    )
    db.session.commit()

    payload = VendaService().processar_venda_rapida(
        pedido.id,
        metodo_pagamento='dinheiro',
        valor_pago=100.0,
        actor=admin_user,
    )

    db.session.refresh(produto)
    db.session.refresh(caixa)
    db.session.refresh(pedido)

    assert pedido.status == Pedido.STATUS_FECHADO
    assert pedido.estoque_processado is True
    assert pedido.financeiro_processado is True
    assert produto.quantidade_estoque == 2
    assert caixa.saldo_atual == 180.0
    assert Movimentacao.query.filter_by(pedido_id=pedido.id, tipo=Movimentacao.TIPO_SAIDA).count() == 1
    assert MovimentacaoCaixa.query.filter_by(caixa_id=caixa.id, tipo=MovimentacaoCaixa.TIPO_ENTRADA).count() == 1
    assert LancamentoFinanceiro.query.filter_by(pedido_id=pedido.id, tipo=LancamentoFinanceiro.TIPO_RECEITA).count() == 1
    assert payload['comprovante']['troco'] == 20.0
    assert payload['alerts']
    assert 'abaixo do minimo' in payload['alerts'][0]['message']


def test_venda_service_busca_prioriza_ean_e_sugere_venda_cruzada(db_session, categoria, caixa):
    produto_base = Produto(
        codigo='7891234567895',
        nome='Cafe Torrado',
        categoria_id=categoria.id,
        preco_custo=8.0,
        preco_venda=16.0,
        quantidade_estoque=30,
        quantidade_minima=5,
        ativo=True,
    )
    produto_combo_1 = Produto(
        codigo='7891234567896',
        nome='Filtro de Papel',
        categoria_id=categoria.id,
        preco_custo=2.0,
        preco_venda=6.0,
        quantidade_estoque=40,
        quantidade_minima=5,
        ativo=True,
    )
    produto_combo_2 = Produto(
        codigo='7891234567897',
        nome='Acucar Mascavo',
        categoria_id=categoria.id,
        preco_custo=3.0,
        preco_venda=8.0,
        quantidade_estoque=40,
        quantidade_minima=5,
        ativo=True,
    )
    db.session.add_all([produto_base, produto_combo_1, produto_combo_2])
    db.session.flush()

    for itens in (
        [(produto_base, 1), (produto_combo_1, 1)],
        [(produto_base, 1), (produto_combo_1, 1), (produto_combo_2, 1)],
    ):
        pedido = Pedido(
            caixa_id=caixa.id,
            status=Pedido.STATUS_FECHADO,
            criado_em=datetime.utcnow() - timedelta(days=2),
            fechado_em=datetime.utcnow() - timedelta(days=1),
            total=sum(prod.preco_venda * qtd for prod, qtd in itens),
            estoque_processado=True,
            financeiro_processado=True,
        )
        db.session.add(pedido)
        db.session.flush()
        for prod, qtd in itens:
            db.session.add(
                ItemPedido(
                    pedido_id=pedido.id,
                    produto_id=prod.id,
                    quantidade=qtd,
                    preco_unitario=prod.preco_venda,
                )
            )
    db.session.commit()

    service = VendaService()
    busca = service.buscar_produtos_pdv('7891234567895')
    sugestoes = service.sugerir_venda_cruzada(produto_base.id)

    assert busca
    assert busca[0]['produto_id'] == produto_base.id
    assert busca[0]['score_mode'] == 'barcode_exact'
    assert sugestoes[0]['produto_id'] == produto_combo_1.id
    assert sugestoes[0]['frequencia_compra_conjunta'] == 2


def test_venda_service_calcula_runway_e_margem_real(db_session, caixa, produto):
    pedido = Pedido(
        caixa_id=caixa.id,
        status=Pedido.STATUS_FECHADO,
        criado_em=datetime.utcnow() - timedelta(days=3),
        fechado_em=datetime.utcnow() - timedelta(days=2),
        total=20.0,
        estoque_processado=True,
        financeiro_processado=True,
    )
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
    db.session.commit()

    service = VendaService()
    pedido_carregado = service.carregar_pedido_pdv(pedido.id)
    margem = service.calcular_margem_real_pedido(pedido_carregado, desconto_total=2.0)
    runway = service.calcular_runway_estoque(janela_dias=30, limit=10)
    item_runway = next(item for item in runway if item['produto_id'] == produto.id)

    assert margem['receita_liquida'] == 18.0
    assert margem['custo_total'] == 8.0
    assert margem['lucro_bruto'] == 10.0
    assert margem['margem_percentual'] == 55.56
    assert item_runway['quantidade_vendida_periodo'] == 2
    assert item_runway['media_saida_dia'] > 0
    assert item_runway['dias_ate_ruptura'] is not None


def test_venda_service_ignora_e_bloqueia_produto_vencido(db_session, categoria, caixa):
    produto_vencido = Produto(
        codigo='7891234567800',
        nome='Sanduiche Natural',
        categoria_id=categoria.id,
        preco_custo=5.0,
        preco_venda=11.0,
        quantidade_estoque=6,
        quantidade_minima=1,
        validade=date.today() - timedelta(days=1),
        ativo=True,
    )
    db.session.add(produto_vencido)
    db.session.commit()

    busca = VendaService().buscar_produtos_pdv('Sanduiche')
    assert busca == []

    with pytest.raises(ValidationError):
        create_order(
            caixa=caixa,
            itens_payload=[{'produto_id': produto_vencido.id, 'quantidade': 1}],
        )
