from __future__ import annotations

import json
from datetime import datetime

from flask import has_request_context, request

from app.exceptions import BusinessRuleError, PermissionDenied, ValidationError
from app.services.operational_rules import require_cancel_reason
from app.services.traceability import record_process_event
from app.services.transaction import atomic_transaction
from models import AuditoriaEvento, FundoSolicitacao, LancamentoFinanceiro, Pedido, RecebimentoFornecedor, db


class PedidoStatus:
    ABERTO = Pedido.STATUS_ABERTO
    EM_PREPARO = Pedido.STATUS_EM_PREPARO
    ENTREGUE = Pedido.STATUS_ENTREGUE
    FECHADO = Pedido.STATUS_FECHADO
    CANCELADO = Pedido.STATUS_CANCELADO
    VALIDOS = {
        ABERTO,
        EM_PREPARO,
        ENTREGUE,
        FECHADO,
        CANCELADO,
    }
    TRANSICOES = Pedido.TRANSICOES_PERMITIDAS


class RecebimentoStatus:
    CRIADO = RecebimentoFornecedor.STATUS_CRIADO
    AGUARDANDO_ARMAZENAGEM = RecebimentoFornecedor.STATUS_AGUARDANDO_ARMAZENAGEM
    CONCLUIDO = RecebimentoFornecedor.STATUS_CONCLUIDO
    CANCELADO = RecebimentoFornecedor.STATUS_CANCELADO
    VALIDOS = {
        CRIADO,
        AGUARDANDO_ARMAZENAGEM,
        CONCLUIDO,
        CANCELADO,
    }
    TRANSICOES = {
        CRIADO: {AGUARDANDO_ARMAZENAGEM, CANCELADO},
        AGUARDANDO_ARMAZENAGEM: {CONCLUIDO, CANCELADO},
        CONCLUIDO: set(),
        CANCELADO: set(),
    }


class ExpedicaoStatus:
    PENDENTE_SEPARACAO = 'pendente_separacao'
    SEPARADO = 'separado'
    EM_ROTA = 'em_rota'
    ENTREGUE = 'entregue'
    VALIDOS = {
        PENDENTE_SEPARACAO,
        SEPARADO,
        EM_ROTA,
        ENTREGUE,
    }
    TRANSICOES = {
        PENDENTE_SEPARACAO: {SEPARADO},
        SEPARADO: {PENDENTE_SEPARACAO, EM_ROTA},
        EM_ROTA: {SEPARADO, ENTREGUE},
        ENTREGUE: set(),
    }


class FundoStatus:
    SOLICITADA = FundoSolicitacao.STATUS_SOLICITADA
    APROVADA = FundoSolicitacao.STATUS_APROVADA
    REJEITADA = FundoSolicitacao.STATUS_REJEITADA
    LIBERADA = FundoSolicitacao.STATUS_LIBERADA
    CANCELADA = FundoSolicitacao.STATUS_CANCELADA
    VALIDOS = {
        SOLICITADA,
        APROVADA,
        REJEITADA,
        LIBERADA,
        CANCELADA,
    }
    TRANSICOES = {
        SOLICITADA: {APROVADA, REJEITADA, CANCELADA},
        APROVADA: {LIBERADA, CANCELADA},
        REJEITADA: set(),
        LIBERADA: set(),
        CANCELADA: set(),
    }


def _normalizar_status(status, validos, *, default=None):
    valor = (status or default or '').strip().lower()
    if valor not in validos:
        raise ValidationError('Status informado e invalido.')
    return valor


def _detalhes_json(**payload):
    dados = {chave: valor for chave, valor in payload.items() if valor not in (None, '', [], {}, ())}
    if not dados:
        return ''
    return json.dumps(dados, ensure_ascii=False, default=str)


def _registrar_auditoria_transicao(*, entidade, entidade_id, transicao, actor=None, detalhes=None):
    evento = AuditoriaEvento(
        funcionario_id=(getattr(actor, 'id', None) if actor else None),
        funcionario_nome=(getattr(actor, 'nome', None) if actor else None),
        funcionario_email=(getattr(actor, 'email', None) if actor else None),
        funcionario_role=(getattr(actor, 'role', None) if actor else None),
        metodo=(request.method if has_request_context() else 'SYSTEM'),
        endpoint=(request.endpoint if has_request_context() else 'workflow.transition'),
        rota=(request.path if has_request_context() else f'workflow://{entidade}/{entidade_id}'),
        acao=f'transicao_{entidade}',
        entidade=entidade,
        detalhes=_detalhes_json(id=entidade_id, transicao=transicao, detalhes=detalhes),
        status_code=None,
        ip=((request.headers.get('X-Forwarded-For') or request.remote_addr) if has_request_context() else 'system'),
    )
    db.session.add(evento)


def _validar_transicao(status_atual, status_destino, transicoes, *, entidade_nome):
    if status_destino == status_atual:
        return status_atual
    permitidos = transicoes.get(status_atual, set())
    if status_destino not in permitidos:
        raise BusinessRuleError(
            f'Transicao invalida de {entidade_nome}: {status_atual} -> {status_destino}.'
        )
    return status_destino


def transition_pedido_status(
    pedido,
    novo_status,
    *,
    actor=None,
    on_fechamento=None,
    detalhes=None,
    require_delivery_separation=False,
):
    status_atual = _normalizar_status(getattr(pedido, 'status', None), PedidoStatus.VALIDOS, default=PedidoStatus.ABERTO)
    status_destino = _normalizar_status(novo_status, PedidoStatus.VALIDOS, default=status_atual)

    if status_atual in {PedidoStatus.FECHADO, PedidoStatus.CANCELADO} and status_destino != status_atual:
        raise BusinessRuleError(f'Pedido {status_atual} e imutavel.')

    _validar_transicao(status_atual, status_destino, PedidoStatus.TRANSICOES, entidade_nome='pedido')

    if status_destino == PedidoStatus.ENTREGUE and require_delivery_separation and not pedido.separacao_entrega_concluida:
        raise BusinessRuleError('Pedido nao pode ir para entrega sem separacao concluida.')

    if status_destino == PedidoStatus.FECHADO and status_atual != PedidoStatus.FECHADO:
        if on_fechamento is None:
            raise BusinessRuleError('Fluxo de fechamento nao configurado para o pedido.')
        on_fechamento(pedido)
    elif status_destino == PedidoStatus.CANCELADO and status_atual != PedidoStatus.CANCELADO:
        motivo = require_cancel_reason(detalhes, entity_label='pedido')
        pedido.fechado_em = datetime.utcnow()
        pedido.observacoes = '\n'.join(item for item in [pedido.observacoes, f'Cancelamento: {motivo}'] if item)
        if pedido.mesa:
            pedido.mesa.status = 'livre'
    elif pedido.mesa and status_destino in {PedidoStatus.ABERTO, PedidoStatus.EM_PREPARO, PedidoStatus.ENTREGUE}:
        pedido.mesa.status = 'ocupada'

    pedido.status = status_destino
    _registrar_auditoria_transicao(
        entidade='pedido',
        entidade_id=pedido.id,
        transicao=f'{status_atual}->{status_destino}',
        actor=actor,
        detalhes=detalhes,
    )
    record_process_event(
        processo_tipo='pedido_venda',
        etapa='status',
        acao='status_alterado',
        entidade='pedido',
        entidade_id=pedido.id,
        pedido_id=pedido.id,
        actor=actor,
        detalhes={
            'de': status_atual,
            'para': status_destino,
            'observacao': detalhes,
        },
    )
    return pedido.status


def _validar_itens_recebimento(recebimento):
    if not recebimento.itens:
        raise BusinessRuleError('Recebimento sem itens nao pode avancar no fluxo.')


def transition_recebimento_status(recebimento, novo_status, *, actor=None, detalhes=None):
    status_atual = _normalizar_status(recebimento.status, RecebimentoStatus.VALIDOS, default=RecebimentoStatus.CRIADO)
    status_destino = _normalizar_status(novo_status, RecebimentoStatus.VALIDOS, default=status_atual)
    _validar_transicao(status_atual, status_destino, RecebimentoStatus.TRANSICOES, entidade_nome='recebimento')
    _validar_itens_recebimento(recebimento)

    if status_destino == RecebimentoStatus.AGUARDANDO_ARMAZENAGEM:
        for item in recebimento.itens:
            if (item.qtd_recebida or 0) < 0:
                raise BusinessRuleError(f'Quantidade recebida invalida para "{item.produto.nome}".')
            if (item.qtd_avaria or 0) < 0:
                raise BusinessRuleError(f'Quantidade avariada invalida para "{item.produto.nome}".')
            if (item.qtd_avaria or 0) > (item.qtd_recebida or 0):
                raise BusinessRuleError(f'Avaria maior que quantidade recebida para "{item.produto.nome}".')
        recebimento.conferido_em = recebimento.conferido_em or datetime.utcnow()

    if status_destino == RecebimentoStatus.CONCLUIDO:
        for item in recebimento.itens:
            if (item.qtd_liquida or 0) > 0 and not item.endereco_destino_id:
                raise BusinessRuleError(f'Endereco destino obrigatorio para "{item.produto.nome}".')
        recebimento.armazenado_em = recebimento.armazenado_em or datetime.utcnow()

    if status_destino == RecebimentoStatus.CANCELADO:
        motivo = require_cancel_reason(detalhes, entity_label='recebimento')
        recebimento.observacoes = '\n'.join(item for item in [recebimento.observacoes, f'Cancelamento: {motivo}'] if item)

    recebimento.status = status_destino
    _registrar_auditoria_transicao(
        entidade='recebimento',
        entidade_id=recebimento.id,
        transicao=f'{status_atual}->{status_destino}',
        actor=actor,
        detalhes=detalhes,
    )
    record_process_event(
        processo_tipo='recebimento',
        etapa='status',
        acao='status_alterado',
        entidade='recebimento',
        entidade_id=recebimento.id,
        recebimento_id=recebimento.id,
        actor=actor,
        detalhes={
            'de': status_atual,
            'para': status_destino,
            'observacao': detalhes,
        },
    )
    return recebimento.status


def get_expedicao_status(pedido):
    if pedido.entrega_concluida_em:
        return ExpedicaoStatus.ENTREGUE
    if pedido.saiu_para_entrega_em:
        return ExpedicaoStatus.EM_ROTA
    if pedido.separacao_entrega_concluida:
        return ExpedicaoStatus.SEPARADO
    return ExpedicaoStatus.PENDENTE_SEPARACAO


def transition_expedicao_status(
    pedido,
    novo_status,
    *,
    actor=None,
    enabled=True,
    allowed_origins=None,
    detalhes=None,
    metadata=None,
):
    if not enabled:
        raise BusinessRuleError('Separacao/expedicao de entrega esta desativada na configuracao da empresa.')

    if allowed_origins and (pedido.origem or '').strip().lower() not in {item.strip().lower() for item in allowed_origins if item}:
        raise BusinessRuleError('Pedido fora da fila configurada para separacao de entrega.')

    if pedido.status in {Pedido.STATUS_CANCELADO, Pedido.STATUS_FECHADO}:
        raise BusinessRuleError('Pedido fora da fila operacional de expedicao.')

    status_atual = get_expedicao_status(pedido)
    status_destino = _normalizar_status(novo_status, ExpedicaoStatus.VALIDOS, default=status_atual)
    _validar_transicao(status_atual, status_destino, ExpedicaoStatus.TRANSICOES, entidade_nome='expedicao')

    metadata = metadata or {}
    if status_destino == ExpedicaoStatus.SEPARADO:
        pedido.rota_entrega = metadata.get('rota_entrega', pedido.rota_entrega)
        pedido.ordem_rota = metadata.get('ordem_rota', pedido.ordem_rota)
        pedido.local_saida = metadata.get('local_saida', pedido.local_saida)
        pedido.veiculo_tipo = metadata.get('veiculo_tipo', pedido.veiculo_tipo)
        pedido.veiculo_placa = metadata.get('veiculo_placa', pedido.veiculo_placa)
        pedido.motorista_nome = metadata.get('motorista_nome', pedido.motorista_nome)
        pedido.empresa_terceirizada = metadata.get('empresa_terceirizada', pedido.empresa_terceirizada)
        pedido.nota_fiscal_numero = metadata.get('nota_fiscal_numero', pedido.nota_fiscal_numero)
        pedido.nota_fiscal_chave = metadata.get('nota_fiscal_chave', pedido.nota_fiscal_chave)
        if metadata.get('nota_fiscal_emitida'):
            pedido.nota_fiscal_emitida_em = pedido.nota_fiscal_emitida_em or datetime.utcnow()
        pedido.separacao_entrega_concluida = True
        pedido.separacao_entrega_em = pedido.separacao_entrega_em or datetime.utcnow()

    elif status_destino == ExpedicaoStatus.PENDENTE_SEPARACAO:
        pedido.separacao_entrega_concluida = False
        pedido.separacao_entrega_em = None
        pedido.saiu_para_entrega_em = None
        pedido.entrega_concluida_em = None

    elif status_destino == ExpedicaoStatus.EM_ROTA:
        if not pedido.separacao_entrega_concluida:
            raise BusinessRuleError('Pedido nao esta separado para despacho.')
        pedido.saiu_para_entrega_em = pedido.saiu_para_entrega_em or datetime.utcnow()

    elif status_destino == ExpedicaoStatus.ENTREGUE:
        if not pedido.separacao_entrega_concluida:
            raise BusinessRuleError('Pedido nao esta separado para entrega.')
        pedido.saiu_para_entrega_em = pedido.saiu_para_entrega_em or datetime.utcnow()
        pedido.entrega_concluida_em = pedido.entrega_concluida_em or datetime.utcnow()
        transition_pedido_status(
            pedido,
            PedidoStatus.ENTREGUE,
            actor=actor,
            detalhes='Entrega confirmada no fluxo de expedicao.',
        )

    _registrar_auditoria_transicao(
        entidade='expedicao',
        entidade_id=pedido.id,
        transicao=f'{status_atual}->{status_destino}',
        actor=actor,
        detalhes=detalhes,
    )
    record_process_event(
        processo_tipo='expedicao',
        etapa='expedicao',
        acao=f'expedicao_{status_destino}',
        entidade='pedido',
        entidade_id=pedido.id,
        pedido_id=pedido.id,
        actor=actor,
        detalhes={
            'de': status_atual,
            'para': status_destino,
            'metadata': metadata,
            'observacao': detalhes,
        },
    )
    return status_destino


def transition_fundo_status(
    fundo,
    novo_status,
    *,
    actor=None,
    motivo_rejeicao=None,
    detalhes=None,
    failure_hook=None,
):
    with atomic_transaction():
        status_atual = _normalizar_status(fundo.status, FundoStatus.VALIDOS, default=FundoStatus.SOLICITADA)
        status_destino = _normalizar_status(novo_status, FundoStatus.VALIDOS, default=status_atual)
        _validar_transicao(status_atual, status_destino, FundoStatus.TRANSICOES, entidade_nome='fundo')

        role = (getattr(actor, 'role', '') or '').strip().lower()

        if status_destino in {FundoStatus.APROVADA, FundoStatus.REJEITADA, FundoStatus.LIBERADA} and role not in {'admin', 'gerente'}:
            raise PermissionDenied('Somente admin/gerente pode alterar esta etapa da solicitacao.')

        lancamento_id = fundo.lancamento_financeiro_id
        if status_destino == FundoStatus.APROVADA:
            fundo.aprovado_por_id = getattr(actor, 'id', None)
            fundo.aprovado_em = fundo.aprovado_em or datetime.utcnow()
            fundo.motivo_rejeicao = None

        elif status_destino == FundoStatus.REJEITADA:
            motivo_rejeicao = (motivo_rejeicao or '').strip()
            if not motivo_rejeicao:
                raise ValidationError('Informe o motivo da rejeicao.')
            fundo.aprovado_por_id = getattr(actor, 'id', None)
            fundo.aprovado_em = datetime.utcnow()
            fundo.motivo_rejeicao = motivo_rejeicao

        elif status_destino == FundoStatus.LIBERADA:
            if fundo.lancamento_financeiro_id:
                raise BusinessRuleError('Solicitacao ja possui lancamento financeiro vinculado.')
            tipo_lanc = (
                LancamentoFinanceiro.TIPO_RECEITA
                if fundo.tipo == FundoSolicitacao.TIPO_APORTE
                else LancamentoFinanceiro.TIPO_DESPESA
            )
            lancamento = LancamentoFinanceiro(
                tipo=tipo_lanc,
                categoria=fundo.categoria or 'liberacao_fundos',
                descricao=f'Liberacao de fundo #{fundo.id} - {fundo.descricao}',
                valor=float(fundo.valor or 0.0),
                data_competencia=datetime.utcnow().date(),
                incluir_contabilidade=True,
                referencia_documento=fundo.referencia_documento,
                centro_custo=fundo.centro_custo,
                criado_por_id=getattr(actor, 'id', None),
            )
            db.session.add(lancamento)
            db.session.flush()
            if failure_hook:
                failure_hook('after_lancamento')
            if not fundo.aprovado_por_id:
                fundo.aprovado_por_id = getattr(actor, 'id', None)
                fundo.aprovado_em = fundo.aprovado_em or datetime.utcnow()
            fundo.liberado_por_id = getattr(actor, 'id', None)
            fundo.liberado_em = datetime.utcnow()
            fundo.lancamento_financeiro_id = lancamento.id
            lancamento_id = lancamento.id
            fundo.motivo_rejeicao = None

        fundo.status = status_destino
        _registrar_auditoria_transicao(
            entidade='fundo',
            entidade_id=fundo.id,
            transicao=f'{status_atual}->{status_destino}',
            actor=actor,
            detalhes=detalhes,
        )
        record_process_event(
            processo_tipo='financeiro_operacional',
            etapa='fundos',
            acao=f'fundo_{status_destino}',
            entidade='fundo',
            entidade_id=fundo.id,
            fundo_solicitacao_id=fundo.id,
            lancamento_financeiro_id=lancamento_id,
            actor=actor,
            detalhes={
                'de': status_atual,
                'para': status_destino,
                'observacao': detalhes,
            },
        )
        return fundo.status
