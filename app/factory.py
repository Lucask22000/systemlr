import logging
import os

from dotenv import load_dotenv
from flask import Flask

from config import DEV_FALLBACK_SECRET, config
from models import db

from app.extensions import init_extensions


load_dotenv()
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


def create_app(config_name=None, *, register_routes=False, route_contexts=None):
    if config_name is None:
        config_name = (os.environ.get('FLASK_CONFIG') or os.environ.get('APP_ENV') or 'development').strip().lower()
    if config_name not in config:
        config_name = 'default'

    app = Flask(
        __name__,
        template_folder=os.path.join(PROJECT_ROOT, 'templates'),
        static_folder=os.path.join(PROJECT_ROOT, 'static'),
    )
    app.config.from_object(config[config_name])
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config.setdefault('LOGIN_MAX_ATTEMPTS', 5)
    app.config.setdefault('LOGIN_WINDOW_SECONDS', 300)
    app.config.setdefault('LOCAL_AI_ENABLED', os.environ.get('SYSTEMLR_LOCAL_AI_ENABLED', '1') not in {'0', 'false', 'False'})
    app.config.setdefault(
        'LOCAL_AI_AUTO_INSTALL',
        os.environ.get('SYSTEMLR_LOCAL_AI_AUTO_INSTALL', '1') not in {'0', 'false', 'False'}
        and app.config.get('ENV_NAME') != 'testing'
    )
    app.config.setdefault(
        'LOCAL_AI_MODEL_ID',
        os.environ.get('SYSTEMLR_LOCAL_AI_MODEL', 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
    )
    app.config.setdefault(
        'LOCAL_AI_MODEL_CANDIDATES',
        os.environ.get(
            'SYSTEMLR_LOCAL_AI_MODEL_CANDIDATES',
            'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2,intfloat/multilingual-e5-large,sentence-transformers/distiluse-base-multilingual-cased-v2',
        ),
    )
    app.config.setdefault('LOCAL_AI_MAX_HISTORY_MESSAGES', int(os.environ.get('SYSTEMLR_LOCAL_AI_MAX_HISTORY_MESSAGES', '5')))

    app.logger.setLevel(logging.INFO)
    if not app.logger.handlers:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s %(name)s %(message)s',
        )

    if app.config.get('ENV_NAME') == 'production' and app.config.get('SECRET_KEY') == DEV_FALLBACK_SECRET:
        raise RuntimeError('SECRET_KEY insegura em producao. Defina a variavel de ambiente SECRET_KEY.')

    init_extensions(app, db)

    if register_routes:
        route_contexts = route_contexts or {}
        from app import api_routes, auth_routes, dashboard_routes, empresa_routes, rh_routes, services_routes

        auth_routes.register_routes(app, route_contexts.get('auth'))
        dashboard_routes.register_routes(app, route_contexts.get('dashboard'))
        rh_routes.register_routes(app, route_contexts.get('rh'))
        empresa_routes.register_routes(app, route_contexts.get('empresa'))
        services_routes.register_routes(app, route_contexts.get('services'))
        api_routes.register_routes(app, route_contexts.get('api'))

    return app
