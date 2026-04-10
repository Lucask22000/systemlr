from __future__ import annotations

import json

from models import ProcessoEvento, db


def _json_details(payload):
    data = {key: value for key, value in (payload or {}).items() if value not in (None, '', [], {}, ())}
    if not data:
        return None
    return json.dumps(data, ensure_ascii=False, default=str)


def record_process_event(
    *,
    processo_tipo,
    etapa,
    acao,
    entidade,
    entidade_id,
    actor=None,
    pedido_id=None,
    recebimento_id=None,
    movimentacao_id=None,
    lancamento_financeiro_id=None,
    fundo_solicitacao_id=None,
    detalhes=None,
):
    evento = ProcessoEvento(
        processo_tipo=processo_tipo,
        etapa=etapa,
        acao=acao,
        entidade=entidade,
        entidade_id=entidade_id,
        pedido_id=pedido_id,
        recebimento_id=recebimento_id,
        movimentacao_id=movimentacao_id,
        lancamento_financeiro_id=lancamento_financeiro_id,
        fundo_solicitacao_id=fundo_solicitacao_id,
        funcionario_id=(getattr(actor, 'id', None) if actor else None),
        funcionario_nome=(getattr(actor, 'nome', None) if actor else None),
        detalhes=_json_details(detalhes),
    )
    db.session.add(evento)
    return evento


def build_timeline(*, pedido=None, recebimento=None, fundo=None):
    query = ProcessoEvento.query
    if pedido is not None:
        query = query.filter(ProcessoEvento.pedido_id == pedido.id)
    elif recebimento is not None:
        query = query.filter(ProcessoEvento.recebimento_id == recebimento.id)
    elif fundo is not None:
        query = query.filter(ProcessoEvento.fundo_solicitacao_id == fundo.id)
    else:
        return []

    eventos = query.order_by(ProcessoEvento.criado_em.asc(), ProcessoEvento.id.asc()).all()
    timeline = []
    for evento in eventos:
        try:
            detalhes = json.loads(evento.detalhes) if evento.detalhes else {}
        except Exception:
            detalhes = {'raw': evento.detalhes}
        timeline.append({
            'quando': evento.criado_em,
            'processo_tipo': evento.processo_tipo,
            'etapa': evento.etapa,
            'acao': evento.acao,
            'entidade': evento.entidade,
            'entidade_id': evento.entidade_id,
            'pedido_id': evento.pedido_id,
            'recebimento_id': evento.recebimento_id,
            'movimentacao_id': evento.movimentacao_id,
            'lancamento_financeiro_id': evento.lancamento_financeiro_id,
            'fundo_solicitacao_id': evento.fundo_solicitacao_id,
            'responsavel': evento.funcionario_nome,
            'detalhes': detalhes,
        })
    return timeline
