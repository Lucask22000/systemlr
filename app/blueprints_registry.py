"""Centraliza o registro de modulos de rotas.

Mantem compatibilidade com os registradores legados baseados em app.route.
"""

from app.api_routes import register_routes as register_api_routes
from app.auth_routes import register_routes as register_auth_routes
from routes.estoque_routes import register_estoque_routes
from routes.public_routes import register_public_routes
from routes.vendas_routes import register_vendas_routes


def register_auth_module(app, context):
    """Registra as rotas de autenticacao."""
    register_auth_routes(app, context)


def register_domain_modules(
    app,
    *,
    login_required,
    require_role,
    aplicar_movimentacao_estoque,
    sincronizar_matriculas_funcionarios,
):
    """Registra modulos de dominio mantidos fora de app/__init__.py."""
    register_estoque_routes(
        app,
        login_required,
        require_role,
        aplicar_movimentacao_estoque,
        sincronizar_matriculas_funcionarios,
    )
    register_vendas_routes(app, login_required, require_role)
    register_public_routes(app)


def register_api_module(app, context):
    """Registra endpoints de API."""
    register_api_routes(app, context)
