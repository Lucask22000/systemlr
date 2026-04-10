import secrets
from functools import wraps
from typing import Iterable, Optional, Tuple

from flask import abort, jsonify, request, session

CSRF_SESSION_KEY = '_csrf_token'
CSRF_HEADER_CANDIDATES = ('X-CSRF-Token', 'X-CSRFToken')
SAFE_METHODS = {'GET', 'HEAD', 'OPTIONS', 'TRACE'}


def json_response(success, message, *, status=200, data=None, code=None, fields=None, action=None):
    payload = {
        'success': bool(success),
        'message': message,
        'code': code or ('ok' if success else 'request_failed'),
        'fields': fields or {},
    }
    if data is not None:
        payload['data'] = data
    if action:
        payload['action'] = action
    return jsonify(payload), status


def is_json_request() -> bool:
    if request.path.startswith('/api/'):
        return True
    accepts = request.headers.get('Accept', '')
    return 'application/json' in accepts.lower()


def ensure_csrf_token() -> str:
    token = session.get(CSRF_SESSION_KEY)
    if not token:
        token = secrets.token_urlsafe(32)
        session[CSRF_SESSION_KEY] = token
        session.modified = True
    return token


def csrf_input_tag() -> str:
    token = ensure_csrf_token()
    return f'<input type="hidden" name="csrf_token" value="{token}">'


def _extract_request_csrf_token() -> Optional[str]:
    for header_name in CSRF_HEADER_CANDIDATES:
        header_token = request.headers.get(header_name)
        if header_token:
            return header_token

    form_token = request.form.get('csrf_token')
    if form_token:
        return form_token

    json_payload = request.get_json(silent=True) or {}
    json_token = json_payload.get('csrf_token') if isinstance(json_payload, dict) else None
    if json_token:
        return json_token

    return None


def validate_csrf_request() -> Tuple[bool, str]:
    expected_token = session.get(CSRF_SESSION_KEY)
    if not expected_token:
        return False, 'Sessao sem token CSRF valido. Recarregue a pagina e tente novamente.'

    informed_token = _extract_request_csrf_token()
    if not informed_token:
        return False, 'Token CSRF ausente.'

    if not secrets.compare_digest(str(expected_token), str(informed_token)):
        return False, 'Token CSRF invalido.'

    return True, ''


def csrf_protect_request(*, exempt_endpoints: Optional[Iterable[str]] = None):
    if request.method in SAFE_METHODS:
        return None

    endpoint = request.endpoint or ''
    if endpoint.startswith('static'):
        return None

    # Rotas publicas sensiveis como login/registro nao devem ser isentas por padrao.
    if exempt_endpoints and endpoint in set(exempt_endpoints):
        return None

    ok, reason = validate_csrf_request()
    if ok:
        return None

    if is_json_request():
        return json_response(False, reason, status=400, code='csrf_invalid')

    abort(400, description=reason)


def role_required(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            role = (session.get('funcionario_role') or '').strip().lower()
            if role not in roles:
                if is_json_request():
                    return json_response(False, 'Sem permissao para executar esta operacao.', status=403, code='forbidden')
                abort(403)
            return fn(*args, **kwargs)

        return wrapper

    return decorator
