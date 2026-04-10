import os
from datetime import timedelta

try:
    import redis
except Exception:  # pragma: no cover - redis e opcional no bootstrap local
    redis = None

DEV_FALLBACK_SECRET = 'dev-secret-key-change-in-production'


class Config:
    """Configuracao base da aplicacao."""

    SQLALCHEMY_DATABASE_URI = 'sqlite:///estoque.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', DEV_FALLBACK_SECRET)
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = False
    PREFERRED_URL_SCHEME = 'http'
    ENV_NAME = 'base'
    CACHE_TYPE = os.environ.get('CACHE_TYPE', 'SimpleCache')
    CACHE_DEFAULT_TIMEOUT = int(os.environ.get('CACHE_DEFAULT_TIMEOUT', '60'))
    CACHE_REDIS_URL = os.environ.get('CACHE_REDIS_URL')
    RATELIMIT_STORAGE_URI = os.environ.get('RATELIMIT_STORAGE_URI', 'memory://')
    REDIS_URL = os.environ.get('REDIS_URL')
    SESSION_TYPE = 'redis' if REDIS_URL else 'filesystem'
    SESSION_REDIS = redis.from_url(REDIS_URL) if (REDIS_URL and redis is not None) else None


class DevelopmentConfig(Config):
    """Configuracao de desenvolvimento."""

    DEBUG = True
    TESTING = False
    ENV_NAME = 'development'


class ProductionConfig(Config):
    """Configuracao de producao."""

    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    PREFERRED_URL_SCHEME = 'https'
    ENV_NAME = 'production'


class TestingConfig(Config):
    """Configuracao de testes."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    ENV_NAME = 'testing'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
}
