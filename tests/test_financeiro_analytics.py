from datetime import datetime

from sqlalchemy.exc import OperationalError

from app.helpers import _coletar_dashboard_analytics
from app.services.analytics import calcular_metricas_dashboard
from models import ItemPedido, LancamentoFinanceiro, Pedido
from app import db


def test_dashboard_operational_result_excludes_non_pnl_financial_movements(db_session, produto, caixa):
    pedido = Pedido(
        caixa_id=caixa.id,
        status=Pedido.STATUS_FECHADO,
        fechado_em=datetime(2026, 3, 27, 12, 0, 0),
        criado_em=datetime(2026, 3, 27, 11, 0, 0),
        total=20.0,
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

    db.session.add_all([
        LancamentoFinanceiro(
            tipo=LancamentoFinanceiro.TIPO_DESPESA,
            categoria='pagamento_fornecedor',
            descricao='Pagamento de fornecedor',
            valor=8.0,
            data_competencia=datetime(2026, 3, 27).date(),
        ),
        LancamentoFinanceiro(
            tipo=LancamentoFinanceiro.TIPO_DESPESA,
            categoria='sangria',
            descricao='Sangria do caixa',
            valor=5.0,
            data_competencia=datetime(2026, 3, 27).date(),
        ),
        LancamentoFinanceiro(
            tipo=LancamentoFinanceiro.TIPO_DESPESA,
            categoria='energia',
            descricao='Conta de energia',
            valor=3.0,
            data_competencia=datetime(2026, 3, 27).date(),
        ),
    ])
    db.session.commit()

    analytics = calcular_metricas_dashboard(
        datetime(2026, 3, 27, 0, 0, 0),
        datetime(2026, 3, 28, 0, 0, 0),
    )

    assert analytics['faturamento_periodo'] == 20.0
    assert analytics['cmv_periodo'] == 8.0
    assert analytics['lucro_bruto_periodo'] == 12.0
    assert analytics['despesas_operacionais_periodo'] == 3.0
    assert analytics['movimentacoes_financeiras_excluidas_periodo'] == 13.0
    assert analytics['resultado_operacional_periodo'] == 9.0
    assert analytics['margem_operacional_pct'] == 45.0


def test_dashboard_analytics_returns_safe_fallback_on_schema_mismatch(app_ctx, monkeypatch):
    def _raise_schema_mismatch(*_args, **_kwargs):
        raise OperationalError(
            'SELECT',
            {},
            Exception('no such column: pedidos.cliente_publico_id'),
        )

    monkeypatch.setattr('app.helpers.calcular_metricas_dashboard', _raise_schema_mismatch)

    analytics = _coletar_dashboard_analytics(
        datetime(2026, 3, 27, 0, 0, 0),
        datetime(2026, 3, 28, 0, 0, 0),
    )

    assert analytics['pedidos_periodo_total'] == 0
    assert analytics['faturamento_periodo'] == 0.0
    assert analytics['metodo_mais_usado'] == 'nao informado'
    assert analytics['alertas']
    assert analytics['alertas'][0]['titulo'] == 'Analytics temporariamente indisponivel'
