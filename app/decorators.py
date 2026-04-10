from functools import wraps

from flask import flash, redirect, session, url_for

from app import extensions
from models import Funcionario
from security import is_json_request, json_response


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'funcionario_id' not in session:
            if is_json_request():
                return json_response(False, 'Você precisa fazer login.', status=401, code='auth_required')
            flash('Você precisa fazer login para acessar esta página.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


def require_role(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'funcionario_id' not in session:
                if is_json_request():
                    return json_response(False, 'Você precisa fazer login.', status=401, code='auth_required')
                flash('Você precisa fazer login.', 'warning')
                return redirect(url_for('login'))

            funcionario = Funcionario.query.get(session['funcionario_id'])
            if not funcionario or not funcionario.ativo:
                session.clear()
                if is_json_request():
                    return json_response(False, 'Funcionario inativo ou removido.', status=403, code='forbidden')
                flash('Funcionario inativo ou removido.', 'danger')
                return redirect(url_for('login'))

            if funcionario.role not in roles:
                if is_json_request():
                    return json_response(False, 'Sem permissao para executar esta operacao.', status=403, code='forbidden')
                flash('Você não tem permissão para acessar esta página.', 'danger')
                return redirect(url_for('dashboard'))

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def _limit(rule, *args, **kwargs):
    def decorator(func):
        if extensions.limiter is None:
            return func
        return extensions.limiter.limit(rule, *args, **kwargs)(func)

    return decorator
