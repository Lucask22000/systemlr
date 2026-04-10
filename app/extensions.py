"""Inicializacao centralizada de extensoes Flask."""

import os

from flask import request
from flask_migrate import Migrate

try:
    from flask_wtf.csrf import CSRFProtect
except Exception:  # pragma: no cover - fallback para ambientes sem dependencia instalada
    CSRFProtect = None

try:
    from flask_limiter import Limiter
except Exception:  # pragma: no cover - fallback para ambientes sem dependencia instalada
    Limiter = None

try:
    from flask_caching import Cache
except Exception:  # pragma: no cover - fallback para ambientes sem dependencia instalada
    Cache = None


migrate = Migrate()
csrf = CSRFProtect() if CSRFProtect else None
limiter = None
cache = Cache() if Cache else None


def _client_rate_limit_key():
    if request.access_route:
        return request.access_route[-1]
    return request.remote_addr or 'unknown'


def init_extensions(app, db):
    """Registra extensoes no app."""
    global limiter
    migrate.init_app(app, db)

    if csrf is not None:
        # Mantem a validacao manual legada durante transicao de arquitetura.
        app.config.setdefault('WTF_CSRF_CHECK_DEFAULT', False)
        csrf.init_app(app)

    if Limiter is not None:
        storage_uri = (
            os.environ.get('RATELIMIT_STORAGE_URI')
            or app.config.get('RATELIMIT_STORAGE_URI')
            or 'memory://'
        )
        limiter = Limiter(key_func=_client_rate_limit_key, storage_uri=storage_uri)
        limiter.init_app(app)
    else:
        limiter = None

    if cache is not None:
        cache_type = app.config.get('CACHE_TYPE') or os.environ.get('CACHE_TYPE') or 'SimpleCache'
        cache_default_timeout = int(
            app.config.get('CACHE_DEFAULT_TIMEOUT')
            or os.environ.get('CACHE_DEFAULT_TIMEOUT')
            or 60
        )
        cache_redis_url = app.config.get('CACHE_REDIS_URL') or os.environ.get('CACHE_REDIS_URL')
        cache_config = {
            'CACHE_TYPE': cache_type,
            'CACHE_DEFAULT_TIMEOUT': cache_default_timeout,
        }
        if cache_redis_url:
            cache_config['CACHE_REDIS_URL'] = cache_redis_url
        cache.init_app(app, config=cache_config)
