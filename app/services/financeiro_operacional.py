from datetime import datetime

from app.exceptions import ValidationError
from app.services.operational_rules import validate_financial_entry_payload
from app.services.transaction import atomic_transaction
from app.services.workflow import FundoStatus, transition_fundo_status
from models import FundoSolicitacao, LancamentoFinanceiro, db


def criar_solicitacao_fundo(
    *,
    tipo,
    descricao,
    valor,
    solicitado_por_id=None,
    categoria=None,
    centro_custo=None,
    referencia_documento=None,
    fundo_model=FundoSolicitacao,
):
    tipo_normalizado = (tipo or '').strip().lower()
    descricao = (descricao or '').strip()
    valor = float(valor or 0.0)

    if tipo_normalizado not in fundo_model.TIPOS_VALIDOS:
        raise ValidationError('Tipo de fundo invalido.')
    if not descricao:
        raise ValidationError('Descricao da solicitacao e obrigatoria.')
    if valor <= 0:
        raise ValidationError('Valor deve ser maior que zero.')

    fundo = fundo_model(
        tipo=tipo_normalizado,
        descricao=descricao,
        categoria=(categoria or '').strip() or None,
        valor=valor,
        centro_custo=(centro_custo or '').strip() or None,
        referencia_documento=(referencia_documento or '').strip() or None,
        status=fundo_model.STATUS_SOLICITADA,
        solicitado_por_id=solicitado_por_id,
    )
    db.session.add(fundo)
    return fundo


def aplicar_acao_fundo(fundo, *, acao, actor=None, motivo_rejeicao=None, failure_hook=None):
    with atomic_transaction():
        acao = (acao or '').strip().lower()
        if acao == 'aprovar':
            return transition_fundo_status(
                fundo,
                FundoStatus.APROVADA,
                actor=actor,
                detalhes='Aprovacao de solicitacao de fundo.',
            )
        if acao == 'rejeitar':
            return transition_fundo_status(
                fundo,
                FundoStatus.REJEITADA,
                actor=actor,
                motivo_rejeicao=motivo_rejeicao,
                detalhes='Rejeicao de solicitacao de fundo.',
            )
        if acao == 'liberar':
            return transition_fundo_status(
                fundo,
                FundoStatus.LIBERADA,
                actor=actor,
                detalhes='Liberacao operacional de fundo com geracao de lancamento.',
                failure_hook=failure_hook,
            )
        raise ValidationError('Acao de fundo invalida.')


def criar_lancamento_financeiro(
    *,
    tipo,
    descricao,
    valor,
    data_competencia=None,
    incluir_contabilidade=False,
    referencia_documento=None,
    centro_custo=None,
    categoria=None,
    produto=None,
    produto_id=None,
    quantidade=None,
    criado_por_id=None,
    lancamento_model=LancamentoFinanceiro,
    failure_hook=None,
):
    with atomic_transaction():
        tipo = (tipo or '').strip().lower()
        descricao = (descricao or '').strip()
        categoria = (categoria or '').strip() or None
        referencia_documento = (referencia_documento or '').strip() or None
        centro_custo = (centro_custo or '').strip() or None
        valor = float(valor or 0.0)
        quantidade = float(quantidade) if quantidade not in {None, ''} else None
        data_competencia = data_competencia or datetime.utcnow().date()

        if tipo not in lancamento_model.TIPOS:
            raise ValidationError('Tipo de lancamento invalido.')
        if not descricao:
            raise ValidationError('Descricao e obrigatoria.')

        if tipo == lancamento_model.TIPO_CONSUMO_PROPRIO:
            if not produto:
                raise ValidationError('Selecione um produto para consumo proprio.')
            if not quantidade or quantidade <= 0:
                raise ValidationError('Informe quantidade valida para consumo proprio.')
            valor = round((produto.preco_custo or 0) * quantidade, 2)
        elif tipo in {lancamento_model.TIPO_DESPESA, lancamento_model.TIPO_RECEITA}:
            if valor <= 0:
                raise ValidationError('Valor deve ser maior que zero.')
        elif tipo == lancamento_model.TIPO_AJUSTE and valor == 0:
            raise ValidationError('Ajuste deve ter valor diferente de zero.')

        validate_financial_entry_payload(
            tipo=tipo,
            referencia_documento=referencia_documento,
            centro_custo=centro_custo,
        )

        lancamento = lancamento_model(
            tipo=tipo,
            categoria=categoria,
            descricao=descricao,
            valor=valor,
            data_competencia=data_competencia,
            incluir_contabilidade=bool(incluir_contabilidade),
            referencia_documento=referencia_documento,
            centro_custo=centro_custo,
            produto_id=(produto.id if produto else produto_id),
            quantidade=quantidade if quantidade and quantidade > 0 else None,
            criado_por_id=criado_por_id,
        )
        db.session.add(lancamento)
        if failure_hook:
            failure_hook('after_lancamento')
    return lancamento
