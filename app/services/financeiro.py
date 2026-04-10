from flask import current_app
from sqlalchemy.exc import OperationalError, ProgrammingError

from app import extensions
from app.services.analytics import calcular_metricas_dashboard, construir_metricas_dashboard_vazias
from app.services.utils import _to_float
from app.utils.data import parse_date_range
from models import db


def _parse_date_range(data_inicial_str, data_final_str, default_days=7):
    return parse_date_range(data_inicial_str, data_final_str, default_days=default_days)


def _coletar_dashboard_analytics(inicio_periodo, fim_periodo):
    cache = extensions.cache
    cache_key = f'dashboard:{inicio_periodo.strftime("%Y%m%d")}:{fim_periodo.strftime("%Y%m%d")}'
    if cache is not None:
        dados = cache.get(cache_key)
        if dados is not None:
            return dados
    try:
        dados = calcular_metricas_dashboard(inicio_periodo, fim_periodo)
    except (OperationalError, ProgrammingError):
        current_app.logger.warning('dashboard analytics indisponiveis por schema/banco inconsistente', exc_info=True)
        db.session.rollback()
        dados = construir_metricas_dashboard_vazias(
            inicio_periodo,
            fim_periodo,
            schema_inconsistente=True,
        )
    else:
        if cache is not None:
            cache.set(cache_key, dados, timeout=60)
        return dados

    if cache is not None:
        cache.set(cache_key, dados, timeout=60)
    return dados


def _build_payment_data(metodo_raw, valor_raw, total_pedido, payment_methods, split_raw=None, cliente_crediario=''):
    metodo = (metodo_raw or '').strip().lower()
    if metodo not in payment_methods:
        raise ValueError('Metodo de pagamento invalido.')
    total = float(total_pedido or 0.0)
    metodo_label_base = payment_methods.get(metodo, metodo.replace('_', ' ').title())

    if metodo == 'dividido':
        split_raw = split_raw or {}
        valor_dinheiro = _to_float(split_raw.get('dinheiro'), 0.0) or 0.0
        valor_cartao = _to_float(split_raw.get('cartao'), 0.0) or 0.0
        if valor_dinheiro < 0 or valor_cartao < 0:
            raise ValueError('Valores de pagamento nao podem ser negativos.')
        valor_pago = valor_dinheiro + valor_cartao
        if valor_pago <= 0:
            raise ValueError('Informe ao menos um valor para dinheiro ou cartao.')
        if valor_pago < total:
            raise ValueError('Valor informado insuficiente para finalizar o pedido.')
        metodo_texto = f'{metodo_label_base} (dinheiro: {valor_dinheiro:.2f} | cartao: {valor_cartao:.2f})'
        return metodo_texto, valor_pago

    valor_pago = _to_float(valor_raw, None)
    if valor_pago is None:
        valor_pago = 0.0 if metodo == 'crediario' else float(total_pedido or 0.0)
    if valor_pago < 0:
        raise ValueError('Valor pago nao pode ser negativo.')

    if metodo == 'crediario':
        cliente = (cliente_crediario or '').strip()
        metodo_texto = f'{metodo_label_base} ({cliente})' if cliente else metodo_label_base
    else:
        if metodo == 'dinheiro' and valor_pago < total:
            raise ValueError('Valor recebido insuficiente para finalizar o pedido.')
        metodo_texto = metodo_label_base

    return metodo_texto, valor_pago
