"""Utilitarios para mensagens amigaveis e padronizadas ao usuario."""

FLASH_CATEGORY_BY_KIND = {
    'Erro': 'danger',
    'Sucesso': 'success',
    'Aviso': 'warning',
}

DEFAULT_ACTIONS_BY_CODE = {
    'auth_required': 'Faca login com um usuario autorizado para continuar.',
    'forbidden': 'Use um perfil com permissao para concluir esta acao.',
    'bad_request': 'Revise os dados informados e tente novamente.',
    'validation_error': 'Corrija os campos destacados e tente novamente.',
    'business_rule': 'Revise o status atual do registro antes de continuar.',
    'not_found': 'Atualize a tela e tente novamente.',
    'csrf_invalid': 'Recarregue a pagina e envie a operacao novamente.',
    'assistant_disabled': 'Use os atalhos da tela atual ou tente novamente mais tarde.',
    'assistant_question_required': 'Preencha o campo de pergunta antes de enviar.',
    'assistant_question_too_long': 'Resuma a pergunta e envie novamente.',
    'assistant_feedback_response_required': 'Abra uma resposta valida antes de avaliar.',
    'assistant_feedback_vote_required': 'Escolha like ou dislike para registrar o feedback.',
    'assistant_feedback_save_failed': 'Tente salvar o feedback novamente em alguns instantes.',
    'app_error': 'Tente novamente em alguns instantes.',
    'internal_error': 'Tente novamente em alguns instantes.',
}


def _clean_text(value):
    return ' '.join(str(value or '').strip().split())


def ensure_sentence(value):
    text = _clean_text(value)
    if not text:
        return ''
    if text[-1] not in '.!?':
        text += '.'
    return text


def resolve_action(*, code=None, status_code=None, action=None):
    if action:
        return ensure_sentence(action)
    if code and code in DEFAULT_ACTIONS_BY_CODE:
        return ensure_sentence(DEFAULT_ACTIONS_BY_CODE[code])
    if status_code == 403:
        return ensure_sentence(DEFAULT_ACTIONS_BY_CODE['forbidden'])
    if status_code == 400:
        return ensure_sentence(DEFAULT_ACTIONS_BY_CODE['validation_error'])
    if status_code == 404:
        return ensure_sentence(DEFAULT_ACTIONS_BY_CODE['not_found'])
    return ensure_sentence(DEFAULT_ACTIONS_BY_CODE['app_error'])


def build_flash_message(kind, message, action=None):
    message_text = ensure_sentence(message)
    action_text = ensure_sentence(action)
    parts = [f'{kind}: {message_text}']
    if action_text:
        parts.append(f'Acao: {action_text}')
    return ' '.join(parts)


def flash_category_for_status(status_code):
    if status_code and status_code < 400:
        return FLASH_CATEGORY_BY_KIND['Sucesso']
    if status_code == 403:
        return FLASH_CATEGORY_BY_KIND['Aviso']
    return FLASH_CATEGORY_BY_KIND['Erro']
