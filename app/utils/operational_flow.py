from __future__ import annotations

from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from flask import request, url_for


RETURN_PARAM_NAMES = ('return_to', 'next')
ORIGIN_PARAM_NAMES = ('origem', 'origin')
CONTEXT_PARAM_NAMES = ('contexto', 'context')
CONTEXT_KEY_PARAM_NAMES = ('context_key', 'storage_key')


def _first_value(source, names):
    for name in names:
        value = source.get(name)
        if value is None:
            continue
        text = str(value).strip()
        if text:
            return text
    return None


def is_safe_local_url(target: str | None) -> bool:
    if not target:
        return False
    parsed = urlparse(str(target).strip())
    return not parsed.scheme and not parsed.netloc and (parsed.path or '').startswith('/')


def get_flow_metadata(*, default_origin=None, default_context=None, default_context_key=None):
    return {
        'return_to': _first_value(request.values, RETURN_PARAM_NAMES),
        'origem': _first_value(request.values, ORIGIN_PARAM_NAMES) or default_origin,
        'contexto': _first_value(request.values, CONTEXT_PARAM_NAMES) or default_context,
        'context_key': _first_value(request.values, CONTEXT_KEY_PARAM_NAMES) or default_context_key,
    }


def get_return_url(default_endpoint: str, *, default_params=None) -> str:
    return_to = _first_value(request.values, RETURN_PARAM_NAMES)
    if is_safe_local_url(return_to):
        return return_to
    return url_for(default_endpoint, **(default_params or {}))


def append_query_params(url: str, **params) -> str:
    parsed = urlparse(url)
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    for key, value in params.items():
        if value is None or value == '':
            query.pop(key, None)
            continue
        query[key] = str(value)
    return urlunparse(parsed._replace(query=urlencode(query, doseq=True)))


def build_related_create_url(
    endpoint: str,
    *,
    return_to: str | None,
    origem: str | None = None,
    contexto: str | None = None,
    context_key: str | None = None,
    **extra_params,
) -> str:
    params = {}
    if is_safe_local_url(return_to):
        params['return_to'] = return_to
    if origem:
        params['origem'] = origem
    if contexto:
        params['contexto'] = contexto
    if context_key:
        params['context_key'] = context_key
    params.update({key: value for key, value in extra_params.items() if value not in (None, '')})
    return url_for(endpoint, **params)


def build_related_return_url(
    default_endpoint: str,
    *,
    entity: str | None = None,
    entity_id: int | str | None = None,
    default_params=None,
    extra_params=None,
) -> str:
    target = get_return_url(default_endpoint, default_params=default_params)
    metadata = get_flow_metadata()
    params = {
        'origem': metadata.get('origem'),
        'contexto': metadata.get('contexto'),
        'context_key': metadata.get('context_key'),
    }
    if entity:
        params['flow_entity'] = entity
    if entity_id not in (None, ''):
        params['flow_entity_id'] = entity_id
    if extra_params:
        params.update(extra_params)
    return append_query_params(target, **params)
