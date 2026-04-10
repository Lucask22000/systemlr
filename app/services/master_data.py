import re

from app.exceptions import ValidationError
from app.utils.payment_config import payment_text_to_json


ALLOWED_COST_CENTERS = {
    'administrativo',
    'estoque',
    'financeiro',
    'logistica',
    'manutencao',
    'operacao',
    'rh',
    'tecnologia',
    'vendas',
}

ALLOWED_MOVEMENT_REASONS = {
    'entrada': {
        'acerto_estoque',
        'devolucao_cliente',
        'inventario_ajuste',
        'producao_interna',
        'recebimento_fornecedor',
        'retorno_almoxarifado',
    },
    'saida': {
        'acerto_estoque',
        'almoxarifado_funcionario',
        'almoxarifado_setor',
        'avaria_quebra',
        'consumo_operacional',
        'perda_validade',
        'uso_interno',
        'venda',
    },
    'transferencia': {
        'abastecimento_filial',
        'redistribuicao_cd',
        'reposicao_loja',
        'transferencia_operacional',
    },
}

ALLOWED_CANCEL_REASONS = {
    'avaria',
    'cliente_desistiu',
    'duplicidade',
    'erro_cadastro',
    'falta_estoque',
    'operacao_cancelada',
    'pagamento_nao_aprovado',
}


def _normalize_slug(value):
    texto = (value or '').strip().lower()
    texto = re.sub(r'[^a-z0-9]+', '_', texto)
    return texto.strip('_')


def _validate_email(value, *, field_label):
    texto = (value or '').strip()
    if texto and '@' not in texto:
        raise ValidationError(f'{field_label} invalido.')
    return texto or None


def validate_supplier_payload(
    *,
    nome,
    documento=None,
    telefone=None,
    email=None,
    endereco_cidade=None,
    tipo_produtos_fornece=None,
    ativo=True,
):
    nome = (nome or '').strip()
    if not nome:
        raise ValidationError('Nome do fornecedor e obrigatorio.')
    email = _validate_email(email, field_label='Email do fornecedor')
    if not ativo:
        return
    if not (documento or '').strip() and not (telefone or '').strip() and not email:
        raise ValidationError('Fornecedor ativo exige ao menos um contato principal: documento, telefone ou email.')
    if not (endereco_cidade or '').strip():
        raise ValidationError('Fornecedor ativo exige cidade informada.')
    if not (tipo_produtos_fornece or '').strip():
        raise ValidationError('Fornecedor ativo exige tipo de produto/servico informado.')


def validate_employee_payload(
    *,
    nome,
    email,
    role,
    cargo,
    departamento,
    ativo=True,
    controle_acesso_ativo=False,
    perfil_acesso_id=None,
    restricao_estoques_ativa=False,
    estoque_principal_id=None,
):
    if not (nome or '').strip():
        raise ValidationError('Nome do funcionario e obrigatorio.')
    if not (email or '').strip():
        raise ValidationError('Email do funcionario e obrigatorio.')
    _validate_email(email, field_label='Email do funcionario')
    if not ativo:
        return
    if not (role or '').strip():
        raise ValidationError('Funcionario ativo exige perfil de acesso operacional.')
    if not (cargo or '').strip():
        raise ValidationError('Funcionario ativo exige cargo informado.')
    if not (departamento or '').strip():
        raise ValidationError('Funcionario ativo exige departamento informado.')
    if controle_acesso_ativo and not perfil_acesso_id:
        raise ValidationError('Controle de acesso ativo exige perfil de acesso vinculado.')
    if restricao_estoques_ativa and not estoque_principal_id:
        raise ValidationError('Funcionario com restricao de estoques exige estoque principal.')


def validate_stock_master_payload(*, nome, codigo_filial, ativo=True):
    if not (nome or '').strip():
        raise ValidationError('Nome do estoque e obrigatorio.')
    if ativo and not (codigo_filial or '').strip():
        raise ValidationError('Estoque/filial ativo exige codigo de filial.')


def normalize_cost_center(value, *, required=False):
    texto = _normalize_slug(value)
    if required and not texto:
        raise ValidationError('Centro de custo e obrigatorio.')
    if texto and texto not in ALLOWED_COST_CENTERS:
        raise ValidationError('Centro de custo invalido. Use um centro de custo padronizado.')
    return texto or None


def validate_movement_reason_classified(reason, *, tipo):
    motivo = _normalize_slug(reason)
    if not motivo:
        raise ValidationError('Motivo de movimentacao e obrigatorio.')
    permitidos = ALLOWED_MOVEMENT_REASONS.get(tipo, set())
    if motivo not in permitidos:
        raise ValidationError('Motivo de movimentacao invalido. Use um motivo padronizado.')
    return motivo


def validate_cancel_reason_classified(reason, *, entity_label='registro'):
    texto = (reason or '').strip()
    if not texto:
        raise ValidationError(f'Informe o motivo do cancelamento de {entity_label}.')
    motivo = _normalize_slug(texto)
    if motivo in ALLOWED_CANCEL_REASONS:
        return motivo
    if len(texto) < 8:
        raise ValidationError(f'Motivo do cancelamento de {entity_label} muito curto. Detalhe melhor ou use um motivo padronizado.')
    return texto


def validate_payment_options_configuration(text, *, channel):
    linhas = [linha.strip() for linha in (text or '').splitlines() if linha.strip()]
    if not linhas:
        return None

    vistos = set()
    for linha in linhas:
        partes = [parte.strip() for parte in linha.split('|')]
        payment_id = _normalize_slug(partes[0] if partes else '')
        label = partes[1] if len(partes) > 1 else ''
        if not payment_id:
            raise ValidationError('Forma de pagamento invalida: informe um identificador.')
        if not label:
            raise ValidationError('Forma de pagamento invalida: informe o nome exibido.')
        if payment_id in vistos:
            raise ValidationError('Forma de pagamento duplicada na configuracao.')
        vistos.add(payment_id)
    return payment_text_to_json(text, channel)
