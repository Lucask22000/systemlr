from datetime import datetime

from app import db
from app.services.analytics import calcular_metricas_dashboard
from models import EnderecoEstoque, Estoque, ItemPedido, Pedido


def test_dashboard_analytics_calculates_average_prep_time(db_session, caixa, produto):
    pedido = Pedido(
        caixa_id=caixa.id,
        status=Pedido.STATUS_FECHADO,
        criado_em=datetime(2026, 3, 27, 10, 0, 0),
        fechado_em=datetime(2026, 3, 27, 10, 30, 0),
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
    db.session.commit()

    analytics = calcular_metricas_dashboard(
        datetime(2026, 3, 27, 0, 0, 0),
        datetime(2026, 3, 28, 0, 0, 0),
    )

    assert analytics['tempo_medio_preparo_minutos'] == 30.0


def test_estoque_analytics_endpoint_returns_pareto_and_occupancy(authenticated_client, categoria, produto):
    estoque = Estoque(nome='Estoque KPI', codigo_filial='LJ01', ativo=True)
    endereco = EnderecoEstoque(
        estoque=estoque,
        nome='Endereco KPI',
        loja_cd='LJ01',
        setor_zona='deposito',
        tipo_area='armazenagem',
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
    produto.endereco = endereco
    db.session.add_all([estoque, endereco])
    db.session.commit()

    response = authenticated_client.get('/api/estoque/analytics?periodo=30')
    payload = response.get_json()

    assert response.status_code == 200
    assert payload['success'] is True
    assert 'pareto_produtos' in payload['data']
    assert 'ocupacao_enderecos' in payload['data']


def test_boas_vindas_renders_for_authenticated_user(authenticated_client):
    response = authenticated_client.get('/boas-vindas')

    assert response.status_code == 200
