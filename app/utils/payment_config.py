import json
import re


DEFAULT_PDV_PAYMENT_OPTIONS = [
    {'id': 'dinheiro', 'label': 'Dinheiro', 'descricao': 'Recebimento em especie com troco.'},
    {'id': 'cartao', 'label': 'Cartao', 'descricao': 'Cartao de credito ou debito no caixa.'},
    {'id': 'pix', 'label': 'Pix', 'descricao': 'Transferencia instantanea por QR Code.'},
    {'id': 'crediario', 'label': 'Crediario', 'descricao': 'Venda no crediario da loja.'},
    {'id': 'dividido', 'label': 'Dividido', 'descricao': 'Divide o pagamento entre dinheiro e cartao.'},
]

DEFAULT_ECOMMERCE_PAYMENT_OPTIONS = [
    {'id': 'pix', 'label': 'Pix', 'descricao': 'Confirmacao imediata da compra.'},
    {'id': 'cartao_credito', 'label': 'Cartao de credito', 'descricao': 'Pagamento em credito na retirada ou entrega.'},
    {'id': 'cartao_debito', 'label': 'Cartao de debito', 'descricao': 'Pagamento em debito na retirada ou entrega.'},
    {'id': 'dinheiro', 'label': 'Dinheiro', 'descricao': 'Informe o valor para troco.'},
    {'id': 'vale_alimentacao', 'label': 'Vale-alimentacao', 'descricao': 'Aceite de beneficios e convenios alimentares.'},
]


def _slugify(value):
    texto = (value or '').strip().lower()
    texto = re.sub(r'[^a-z0-9]+', '_', texto)
    return texto.strip('_')


def _normalize_text(value):
    return re.sub(r'[^a-z0-9]+', '', (value or '').strip().lower())


def _load_json_list(raw_value):
    if not raw_value:
        return []
    try:
        data = json.loads(raw_value)
    except Exception:
        return []
    return data if isinstance(data, list) else []


def _payment_defaults(channel):
    if channel == 'pdv':
        return DEFAULT_PDV_PAYMENT_OPTIONS
    return DEFAULT_ECOMMERCE_PAYMENT_OPTIONS


def load_payment_options(raw_value, channel):
    defaults = _payment_defaults(channel)
    source = _load_json_list(raw_value)
    items = source if source else defaults

    options = []
    seen = set()
    for item in items:
        if isinstance(item, dict):
            payment_id = _slugify(item.get('id') or item.get('codigo') or item.get('label'))
            label = (item.get('label') or item.get('nome') or '').strip()
            description = (item.get('descricao') or item.get('description') or '').strip()
            active = item.get('ativo', True) is not False
        else:
            parts = [part.strip() for part in str(item or '').split('|')]
            payment_id = _slugify(parts[0] if parts else '')
            label = parts[1] if len(parts) > 1 else ''
            description = parts[2] if len(parts) > 2 else ''
            active = True
        if not payment_id or payment_id in seen or not active:
            continue
        seen.add(payment_id)
        if not label:
            label = payment_id.replace('_', ' ').title()
        options.append({
            'id': payment_id,
            'label': label,
            'descricao': description,
            'requires_cash_amount': payment_id == 'dinheiro',
            'supports_split': payment_id == 'dividido',
            'supports_credit_account': payment_id == 'crediario',
        })

    return options or [dict(item) for item in defaults]


def payment_options_to_text(raw_value, channel):
    options = load_payment_options(raw_value, channel)
    lines = []
    for item in options:
        lines.append(' | '.join([
            item.get('id') or '',
            item.get('label') or '',
            item.get('descricao') or '',
        ]).rstrip())
    return '\n'.join(lines)


def payment_text_to_json(text, channel):
    defaults_by_id = {item['id']: item for item in _payment_defaults(channel)}
    options = []
    seen = set()
    for line in (text or '').splitlines():
        parts = [part.strip() for part in line.split('|')]
        payment_id = _slugify(parts[0] if parts else '')
        if not payment_id or payment_id in seen:
            continue
        seen.add(payment_id)
        default = defaults_by_id.get(payment_id, {})
        label = parts[1] if len(parts) > 1 and parts[1] else default.get('label') or payment_id.replace('_', ' ').title()
        description = parts[2] if len(parts) > 2 and parts[2] else default.get('descricao') or ''
        options.append({
            'id': payment_id,
            'label': label,
            'descricao': description,
            'ativo': True,
        })
    return json.dumps(options, ensure_ascii=False) if options else None


def payment_methods_map(raw_value, channel):
    return {item['id']: item['label'] for item in load_payment_options(raw_value, channel)}


def default_payment_id(raw_value, channel):
    options = load_payment_options(raw_value, channel)
    return options[0]['id'] if options else None


def infer_payment_method_id(stored_value, options):
    raw_text = (stored_value or '').strip().lower()
    raw_key = _normalize_text(raw_text)
    if not raw_key:
        return ''
    for item in options:
        option_id = (item.get('id') or '').strip().lower()
        option_label = _normalize_text(item.get('label'))
        if option_id and option_id in raw_text:
            return option_id
        if option_label and option_label in raw_key:
            return option_id
    return ''


def load_api_integrations(raw_value):
    items = []
    for item in _load_json_list(raw_value):
        if not isinstance(item, dict):
            continue
        integration_id = _slugify(item.get('id') or item.get('nome') or item.get('provider'))
        if not integration_id:
            continue
        items.append({
            'id': integration_id,
            'nome': (item.get('nome') or '').strip(),
            'provider': (item.get('provider') or '').strip(),
            'ambiente': (item.get('ambiente') or '').strip(),
            'base_url': (item.get('base_url') or '').strip(),
            'chave_publica': (item.get('chave_publica') or '').strip(),
            'token_secreto': (item.get('token_secreto') or '').strip(),
            'webhook_url': (item.get('webhook_url') or '').strip(),
        })
    return items


def api_integrations_to_text(raw_value):
    lines = []
    for item in load_api_integrations(raw_value):
        lines.append(' | '.join([
            item.get('id') or '',
            item.get('nome') or '',
            item.get('provider') or '',
            item.get('ambiente') or '',
            item.get('base_url') or '',
            item.get('chave_publica') or '',
            item.get('token_secreto') or '',
            item.get('webhook_url') or '',
        ]).rstrip())
    return '\n'.join(lines)


def api_integrations_text_to_json(text):
    items = []
    seen = set()
    for line in (text or '').splitlines():
        parts = [part.strip() for part in line.split('|')]
        integration_id = _slugify(parts[0] if parts else '')
        if not integration_id or integration_id in seen:
            continue
        seen.add(integration_id)
        items.append({
            'id': integration_id,
            'nome': parts[1] if len(parts) > 1 else '',
            'provider': parts[2] if len(parts) > 2 else '',
            'ambiente': parts[3] if len(parts) > 3 else '',
            'base_url': parts[4] if len(parts) > 4 else '',
            'chave_publica': parts[5] if len(parts) > 5 else '',
            'token_secreto': parts[6] if len(parts) > 6 else '',
            'webhook_url': parts[7] if len(parts) > 7 else '',
        })
    return json.dumps(items, ensure_ascii=False) if items else None
