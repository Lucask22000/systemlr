from collections import deque
from datetime import datetime

from flask import current_app, request, session

from app import extensions
from app.services.financeiro_service import calcular_metricas_dashboard, parse_date_range
from models import Funcionario


_failed_login_attempts = {}


def get_funcionario_logado():
    if 'funcionario_id' in session:
        return Funcionario.query.get(session['funcionario_id'])
    return None


def _normalizar_texto(valor):
    return (valor or '').strip().lower()


def _client_ip():
    if request.access_route:
        return request.access_route[-1]
    return request.remote_addr or 'unknown'


def _purge_old_attempts(attempts):
    now = datetime.utcnow()
    login_window_seconds = int(current_app.config.get('LOGIN_WINDOW_SECONDS', 300))
    while attempts and (now - attempts[0]).total_seconds() > login_window_seconds:
        attempts.popleft()


def _is_login_rate_limited(ip_addr):
    attempts = _failed_login_attempts.get(ip_addr)
    if not attempts:
        return False
    _purge_old_attempts(attempts)
    return len(attempts) >= int(current_app.config.get('LOGIN_MAX_ATTEMPTS', 5))


def _register_login_attempt(ip_addr, success):
    attempts = _failed_login_attempts.setdefault(ip_addr, deque())
    _purge_old_attempts(attempts)
    if success:
        attempts.clear()
    else:
        attempts.append(datetime.utcnow())


def _parse_date_range(data_inicial_str, data_final_str, default_days=7):
    return parse_date_range(data_inicial_str, data_final_str, default_days=default_days)


def _coletar_dashboard_analytics(inicio_periodo, fim_periodo):
    cache = extensions.cache
    cache_key = f'dashboard:{inicio_periodo.strftime("%Y%m%d")}:{fim_periodo.strftime("%Y%m%d")}'
    if cache is not None:
        dados = cache.get(cache_key)
        if dados is not None:
            return dados
    dados = calcular_metricas_dashboard(inicio_periodo, fim_periodo)
    if cache is not None:
        cache.set(cache_key, dados, timeout=60)
    return dados
