from datetime import datetime

from app.exceptions import BusinessRuleError, ValidationError
from app.services.estoque_service import aplicar_movimentacao_estoque
from app.services.traceability import record_process_event
from app.services.transaction import atomic_transaction
from app.services.workflow import RecebimentoStatus, transition_recebimento_status
from models import Movimentacao, RecebimentoFornecedor, RecebimentoItem, db


def create_recebimento(
    *,
    fornecedor,
    local_recebimento,
    tipo_recebimento,
    itens_processados,
    fornecedor_documento=None,
    data_entrega=None,
    info_nota=None,
    desconto=0.0,
    observacoes=None,
    recebedor_funcionario=None,
    recebedor_nome=None,
    recebedor_assinatura=None,
    entregador_nome=None,
    entregador_assinatura=None,
    ir_para_armazenagem=False,
    actor=None,
    recebimento_model=RecebimentoFornecedor,
    item_model=RecebimentoItem,
    failure_hook=None,
):
    if tipo_recebimento not in recebimento_model.TIPOS_VALIDOS:
        raise ValidationError('Selecione um tipo de recebimento valido.')
    if not local_recebimento:
        raise ValidationError('Defina um local de recebimento ativo e valido antes de concluir.')
    if not itens_processados:
        raise ValidationError('Informe ao menos um item valido no recebimento.')

    subtotal = sum(float(item['total_item']) for item in itens_processados)
    desconto = float(desconto or 0.0)
    if desconto < 0:
        raise ValidationError('Desconto nao pode ser negativo.')
    total_pagar = max(subtotal - desconto, 0.0)

    with atomic_transaction():
        recebimento = recebimento_model(
            fornecedor_id=getattr(fornecedor, 'id', None),
            local_recebimento_id=local_recebimento.id,
            tipo_recebimento=tipo_recebimento,
            fornecedor_documento=fornecedor_documento or getattr(fornecedor, 'documento', None) or None,
            data_entrega=data_entrega,
            info_nota=info_nota,
            subtotal=subtotal,
            desconto=desconto,
            total_pagar=total_pagar,
            observacoes=observacoes,
            recebedor_funcionario_id=(recebedor_funcionario.id if recebedor_funcionario else None),
            recebedor_nome=recebedor_nome,
            recebedor_assinatura=recebedor_assinatura,
            entregador_nome=entregador_nome,
            entregador_assinatura=entregador_assinatura,
            status=recebimento_model.STATUS_CRIADO,
        )
        db.session.add(recebimento)
        db.session.flush()

        for item in itens_processados:
            db.session.add(
                item_model(
                    recebimento_id=recebimento.id,
                    produto_id=item['produto_id'],
                    qtd_recebida=item['qtd_recebida'],
                    unidade=item['unidade'],
                    descricao_item=item['descricao_item'],
                    preco_unitario=item['preco_unitario'],
                    total_item=item['total_item'],
                    qtd_avaria=0,
                )
            )
        if failure_hook:
            failure_hook('after_items')

        if ir_para_armazenagem:
            transition_recebimento_status(
                recebimento,
                RecebimentoStatus.AGUARDANDO_ARMAZENAGEM,
                actor=actor,
                detalhes='Recebimento criado com envio direto para armazenagem.',
            )

        record_process_event(
            processo_tipo='recebimento',
            etapa='criacao',
            acao='recebimento_criado',
            entidade='recebimento',
            entidade_id=recebimento.id,
            recebimento_id=recebimento.id,
            actor=actor,
            detalhes={
                'status': recebimento.status,
                'fornecedor_id': recebimento.fornecedor_id,
                'local_recebimento_id': recebimento.local_recebimento_id,
                'info_nota': recebimento.info_nota,
            },
        )

    return recebimento


def conferir_recebimento(recebimento, *, conferencias_por_item, actor=None, failure_hook=None):
    with atomic_transaction():
        if recebimento.status in {RecebimentoFornecedor.STATUS_CANCELADO, RecebimentoFornecedor.STATUS_CONCLUIDO}:
            raise BusinessRuleError('Nao e possivel conferir um recebimento cancelado ou concluido.')

        for item in recebimento.itens:
            dados = conferencias_por_item.get(item.id) or {}
            qtd_recebida = int(dados.get('qtd_recebida', 0))
            qtd_avaria = int(dados.get('qtd_avaria', 0))
            lote = dados.get('lote')
            validade_texto = (dados.get('validade') or '').strip()

            if qtd_recebida < 0:
                raise ValidationError(f'Quantidade recebida nao pode ser negativa para o produto "{item.produto.nome}".')
            if qtd_avaria < 0:
                raise ValidationError(f'Quantidade avariada nao pode ser negativa para o produto "{item.produto.nome}".')
            if qtd_avaria > qtd_recebida:
                raise ValidationError(f'Avaria nao pode ser maior que recebimento no produto "{item.produto.nome}".')

            validade = None
            if validade_texto:
                try:
                    validade = datetime.strptime(validade_texto, '%Y-%m-%d').date()
                except ValueError as exc:
                    raise ValidationError(f'Data de validade invalida para o produto "{item.produto.nome}".') from exc

            item.qtd_recebida = qtd_recebida
            item.qtd_avaria = qtd_avaria
            item.lote = lote
            item.validade = validade

        if failure_hook:
            failure_hook('after_conference')

        transition_recebimento_status(
            recebimento,
            RecebimentoStatus.AGUARDANDO_ARMAZENAGEM,
            actor=actor,
            detalhes='Conferencia de recebimento concluida.',
        )
        record_process_event(
            processo_tipo='recebimento',
            etapa='conferencia',
            acao='recebimento_conferido',
            entidade='recebimento',
            entidade_id=recebimento.id,
            recebimento_id=recebimento.id,
            actor=actor,
            detalhes={
                'status': recebimento.status,
                'itens': len(recebimento.itens),
            },
        )
    return recebimento


def armazenar_recebimento(
    recebimento,
    *,
    destinos_por_item,
    actor=None,
    categoria_quimico_predicate,
    tipo_labels,
    movimentacao_model=Movimentacao,
    failure_hook=None,
):
    with atomic_transaction():
        if recebimento.status == RecebimentoFornecedor.STATUS_CANCELADO:
            raise BusinessRuleError('Recebimento cancelado. Armazenagem nao permitida.')
        if recebimento.status == RecebimentoFornecedor.STATUS_CONCLUIDO:
            raise BusinessRuleError('Recebimento ja concluido.')
        if recebimento.status == RecebimentoFornecedor.STATUS_CRIADO:
            raise BusinessRuleError('Conclua a conferencia antes da armazenagem.')

        for item in recebimento.itens:
            endereco_destino = destinos_por_item.get(item.id)
            if not endereco_destino:
                raise ValidationError(f'Informe o endereco destino para "{item.produto.nome}".')
            if item.qtd_liquida > 0 and (endereco_destino.controle_validade or 'nenhum') == 'fefo' and not item.validade:
                raise ValidationError(
                    f'Endereco "{endereco_destino.nome}" exige FEFO. Informe validade para "{item.produto.nome}".'
                )
            restricoes = {parte.strip().lower() for parte in (endereco_destino.restricoes or '').split(',') if parte.strip()}
            if 'alimentos' in restricoes and categoria_quimico_predicate(item.produto):
                raise ValidationError(
                    f'Produto "{item.produto.nome}" (categoria quimica) nao pode ser armazenado no endereco de alimentos "{endereco_destino.nome}".'
                )

        for item in recebimento.itens:
            endereco_destino = destinos_por_item[item.id]
            item.endereco_destino_id = endereco_destino.id
            quantidade_entrada = item.qtd_liquida
            if quantidade_entrada <= 0:
                continue

            aplicar_movimentacao_estoque(item.produto, movimentacao_model.TIPO_ENTRADA, quantidade_entrada)
            item.produto.endereco_id = endereco_destino.id

            tipo_recebimento_label = tipo_labels.get(recebimento.tipo_recebimento, recebimento.tipo_recebimento or 'Recebimento')
            observacoes_mov = f'Recebimento #{recebimento.id} | Tipo: {tipo_recebimento_label}'
            if item.lote:
                observacoes_mov += f' | Lote: {item.lote}'
            if item.validade:
                observacoes_mov += f' | Validade: {item.validade.strftime("%d/%m/%Y")}'
            if item.qtd_avaria:
                observacoes_mov += f' | Avaria: {item.qtd_avaria}'

            movimentacao = movimentacao_model(
                    produto_id=item.produto_id,
                    recebimento_id=recebimento.id,
                    fornecedor_id=recebimento.fornecedor_id,
                    endereco_destino_id=endereco_destino.id,
                    tipo=movimentacao_model.TIPO_ENTRADA,
                    quantidade=quantidade_entrada,
                    info_nota=recebimento.info_nota,
                    motivo='recebimento_fornecedor',
                    observacoes=observacoes_mov,
            )
            db.session.add(movimentacao)
            db.session.flush()
            record_process_event(
                processo_tipo='recebimento',
                etapa='armazenagem',
                acao='movimentacao_estoque_gerada',
                entidade='movimentacao',
                entidade_id=movimentacao.id,
                recebimento_id=recebimento.id,
                movimentacao_id=movimentacao.id,
                actor=actor,
                detalhes={
                    'produto_id': item.produto_id,
                    'quantidade': quantidade_entrada,
                    'endereco_destino_id': endereco_destino.id,
                },
            )
            if failure_hook:
                failure_hook('after_item_stock')

        transition_recebimento_status(
            recebimento,
            RecebimentoStatus.CONCLUIDO,
            actor=actor,
            detalhes='Armazenagem concluida e saldo atualizado.',
        )
        record_process_event(
            processo_tipo='recebimento',
            etapa='armazenagem',
            acao='recebimento_armazenado',
            entidade='recebimento',
            entidade_id=recebimento.id,
            recebimento_id=recebimento.id,
            actor=actor,
            detalhes={
                'status': recebimento.status,
                'armazenado_em': recebimento.armazenado_em,
            },
        )
    return recebimento
