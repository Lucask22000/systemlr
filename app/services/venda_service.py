from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta

from sqlalchemy import case, func, inspect as sa_inspect
from sqlalchemy.orm import aliased, joinedload

from app.exceptions import BusinessRuleError, NotFound, ValidationError
from app.services.traceability import record_process_event
from app.services.transaction import atomic_transaction
from app.utils.validators import normalizar_codigo_barras
from models import (
    Caixa,
    Categoria,
    ItemPedido,
    LancamentoFinanceiro,
    Movimentacao,
    MovimentacaoCaixa,
    Pedido,
    Produto,
    db,
)


class VendaService:
    """Orquestra o fluxo do PDV sem deixar regra de negocio nas rotas."""

    def __init__(self, session=None):
        self.session = session or db.session

    def carregar_pedido_pdv(self, pedido_id):
        query = (
            self.session.query(Pedido)
            .options(
                joinedload(Pedido.caixa),
                joinedload(Pedido.mesa),
                joinedload(Pedido.garcom),
                joinedload(Pedido.itens)
                .joinedload(ItemPedido.produto)
                .joinedload(Produto.categoria),
            )
            .filter(Pedido.id == pedido_id)
        )
        pedido = query.first()
        if not pedido:
            raise NotFound('Pedido nao encontrado.')
        return pedido

    def buscar_produtos_pdv(self, termo, *, limit=12):
        termo = (termo or '').strip()
        if not termo:
            return []

        termo_lower = termo.lower()
        query = self.session.query(Produto).options(joinedload(Produto.categoria)).filter(
            Produto.ativo.is_(True),
            Produto.filtro_nao_vencidos(),
        )

        codigo_normalizado, codigo_erro = normalizar_codigo_barras(termo)
        codigo_busca = codigo_normalizado if not codigo_erro else None
        if not codigo_busca and termo.isdigit():
            codigo_busca = termo

        if codigo_busca:
            match = (
                query.filter(Produto.codigo == codigo_busca)
                .order_by(Produto.nome.asc())
                .limit(limit)
                .all()
            )
            if match:
                return [self._serializar_produto_busca(produto, score='barcode_exact') for produto in match]

        dialect = (self.session.bind.dialect.name if self.session.bind else '').lower()
        prefix = f'{termo}%'
        contains = f'%{termo}%'
        rank = case(
            (func.lower(Produto.nome) == termo_lower, 0),
            (func.lower(Produto.codigo) == termo_lower, 1),
            (Produto.nome.ilike(prefix), 2),
            (Produto.nome.ilike(contains), 3),
            else_=4,
        )
        filtered = query.filter(
            db.or_(
                Produto.nome.ilike(contains),
                Produto.codigo.ilike(contains),
            )
        )

        if dialect == 'postgresql' and len(termo) >= 3:
            similarity = func.similarity(func.lower(Produto.nome), termo_lower)
            produtos = (
                filtered.order_by(rank.asc(), similarity.desc(), Produto.nome.asc())
                .limit(limit)
                .all()
            )
            return [self._serializar_produto_busca(produto, score='trigram') for produto in produtos]

        produtos = filtered.order_by(rank.asc(), Produto.nome.asc()).limit(limit).all()
        return [self._serializar_produto_busca(produto, score='ilike_ranked') for produto in produtos]

    def processar_venda_rapida(
        self,
        pedido_ref,
        *,
        metodo_pagamento=None,
        valor_pago=None,
        desconto_total=0.0,
        incluir_contabilidade=False,
        actor=None,
        commit=True,
        failure_hook=None,
    ):
        pedido = self._resolver_pedido_para_fechamento(pedido_ref)
        pedido, lancamento = self._finalizar_pedido(
            pedido,
            metodo_pagamento=metodo_pagamento,
            valor_pago=valor_pago,
            incluir_contabilidade=incluir_contabilidade,
            actor=actor,
            failure_hook=failure_hook,
        )
        if commit:
            self.session.commit()
            self.session.refresh(pedido)
        else:
            self.session.flush()

        desconto_total = float(desconto_total or 0.0)
        margem = self.calcular_margem_real_pedido(pedido, desconto_total=desconto_total)
        alertas = self._montar_alertas_pos_venda(pedido)
        venda_cruzada = []
        if pedido.itens:
            venda_cruzada = self.sugerir_venda_cruzada(pedido.itens[0].produto_id, limit=3)

        return {
            'pedido_id': pedido.id,
            'status': pedido.status,
            'metodo_pagamento': pedido.metodo_pagamento,
            'valor_pago': float(pedido.valor_pago or 0.0) if pedido.valor_pago is not None else None,
            'total': float(pedido.total or 0.0),
            'comprovante': self.gerar_talao_payload(pedido),
            'margin': margem,
            'alerts': alertas,
            'cross_sell': venda_cruzada,
            'lancamento_financeiro_id': getattr(lancamento, 'id', None),
        }

    def _resolver_pedido_para_fechamento(self, pedido_ref):
        """Aceita id ou instancia de pedido sem perder alteracoes pendentes em memoria."""
        if isinstance(pedido_ref, Pedido):
            estado = sa_inspect(pedido_ref)
            if estado.session is self.session:
                return pedido_ref
            pedido_id = getattr(pedido_ref, 'id', None)
            if pedido_id is None:
                raise NotFound('Pedido nao encontrado.')
            return self.carregar_pedido_pdv(pedido_id)
        return self.carregar_pedido_pdv(pedido_ref)

    def _finalizar_pedido(
        self,
        pedido,
        *,
        metodo_pagamento=None,
        valor_pago=None,
        incluir_contabilidade=False,
        actor=None,
        failure_hook=None,
    ):
        status_atual = (pedido.status or Pedido.STATUS_ABERTO).strip().lower()
        if status_atual in Pedido.STATUS_IMUTAVEIS:
            raise BusinessRuleError(f'Pedido ja esta {pedido.status}.')
        if not pedido.itens:
            raise ValidationError('Pedido sem itens nao pode ser finalizado.')

        with atomic_transaction(self.session):
            itens_por_produto = self._agrupar_itens_por_produto(pedido.itens)
            produtos = self._carregar_produtos_para_fechamento(list(itens_por_produto.keys()))
            self._validar_estoque(produtos, itens_por_produto)
            self._aplicar_baixa_estoque(pedido, produtos, itens_por_produto, actor=actor)
            if failure_hook:
                failure_hook('after_stock')
            self._aplicar_financeiro_caixa(pedido, actor=actor)
            if failure_hook:
                failure_hook('after_cash')
            lancamento = next(
                (
                    item for item in (getattr(pedido, 'lancamentos_financeiros', None) or [])
                    if item.tipo == LancamentoFinanceiro.TIPO_RECEITA and (item.categoria or '').strip().lower() == 'pdv'
                ),
                None,
            )
            if lancamento is None:
                lancamento = self._criar_lancamento_financeiro_pdv(
                    pedido,
                    actor=actor,
                    incluir_contabilidade=incluir_contabilidade,
                )

            if metodo_pagamento:
                pedido.metodo_pagamento = metodo_pagamento
            if valor_pago is not None:
                pedido.valor_pago = float(valor_pago)

            pedido.status = Pedido.STATUS_FECHADO
            pedido.fechado_em = datetime.utcnow()
            pedido.estoque_processado = True
            pedido.financeiro_processado = True
            if pedido.mesa:
                pedido.mesa.status = 'livre'

            record_process_event(
                processo_tipo='pedido_venda',
                etapa='fechamento',
                acao='pedido_fechado',
                entidade='pedido',
                entidade_id=pedido.id,
                pedido_id=pedido.id,
                actor=actor,
                detalhes={
                    'status': pedido.status,
                    'metodo_pagamento': pedido.metodo_pagamento,
                    'total': float(pedido.total or 0.0),
                    'fechado_em': pedido.fechado_em,
                    'lancamento_financeiro_id': lancamento.id,
                },
            )
        return pedido, lancamento

    def calcular_runway_estoque(self, *, janela_dias=30, limit=50):
        inicio = datetime.utcnow() - timedelta(days=max(int(janela_dias or 30), 1))
        dias = float(max(int(janela_dias or 30), 1))
        quantidade_vendida = func.coalesce(func.sum(ItemPedido.quantidade), 0)
        media_diaria = quantidade_vendida / dias
        dias_estoque = case(
            (quantidade_vendida > 0, Produto.quantidade_estoque / media_diaria),
            else_=None,
        )

        rows = (
            self.session.query(
                Produto.id.label('produto_id'),
                Produto.nome.label('produto_nome'),
                Produto.codigo.label('codigo'),
                Categoria.nome.label('categoria'),
                Produto.quantidade_estoque.label('estoque_atual'),
                Produto.quantidade_minima.label('estoque_minimo'),
                quantidade_vendida.label('quantidade_vendida'),
                func.round(media_diaria, 2).label('media_diaria'),
                func.round(dias_estoque, 1).label('dias_runway'),
            )
            .outerjoin(Categoria, Categoria.id == Produto.categoria_id)
            .outerjoin(ItemPedido, ItemPedido.produto_id == Produto.id)
            .outerjoin(
                Pedido,
                db.and_(
                    Pedido.id == ItemPedido.pedido_id,
                    Pedido.status == Pedido.STATUS_FECHADO,
                    Pedido.fechado_em >= inicio,
                ),
            )
            .filter(Produto.ativo.is_(True))
            .group_by(
                Produto.id,
                Produto.nome,
                Produto.codigo,
                Categoria.nome,
                Produto.quantidade_estoque,
                Produto.quantidade_minima,
            )
            .order_by(dias_estoque.asc().nullsfirst(), Produto.nome.asc())
            .limit(limit)
            .all()
        )

        return [
            {
                'produto_id': row.produto_id,
                'produto': row.produto_nome,
                'codigo': row.codigo,
                'categoria': row.categoria,
                'estoque_atual': int(row.estoque_atual or 0),
                'estoque_minimo': int(row.estoque_minimo or 0),
                'quantidade_vendida_periodo': int(row.quantidade_vendida or 0),
                'media_saida_dia': float(row.media_diaria or 0.0),
                'dias_ate_ruptura': float(row.dias_runway) if row.dias_runway is not None else None,
                'abaixo_minimo': int(row.estoque_atual or 0) <= int(row.estoque_minimo or 0),
            }
            for row in rows
        ]

    def calcular_margem_real_pedido(self, pedido, *, desconto_total=0.0):
        desconto_total = float(desconto_total or 0.0)
        subtotal = float(sum((item.quantidade or 0) * (item.preco_unitario or 0) for item in pedido.itens))
        if subtotal <= 0:
            return {
                'subtotal_bruto': 0.0,
                'desconto_rateado': desconto_total,
                'receita_liquida': 0.0,
                'custo_total': 0.0,
                'lucro_bruto': 0.0,
                'margem_percentual': 0.0,
                'itens': [],
            }

        itens = []
        custo_total = 0.0
        receita_liquida = 0.0
        for item in pedido.itens:
            produto = item.produto
            linha_bruta = float((item.quantidade or 0) * (item.preco_unitario or 0))
            desconto_rateado = round((linha_bruta / subtotal) * desconto_total, 2) if desconto_total else 0.0
            linha_liquida = max(round(linha_bruta - desconto_rateado, 2), 0.0)
            custo_linha = round(float((produto.preco_custo if produto else 0.0) or 0.0) * float(item.quantidade or 0), 2)
            lucro_linha = round(linha_liquida - custo_linha, 2)
            margem_pct = round((lucro_linha / linha_liquida) * 100, 2) if linha_liquida else 0.0
            custo_total += custo_linha
            receita_liquida += linha_liquida
            itens.append(
                {
                    'produto_id': item.produto_id,
                    'produto': produto.nome if produto else f'Produto {item.produto_id}',
                    'categoria': produto.categoria.nome if produto and produto.categoria else None,
                    'quantidade': int(item.quantidade or 0),
                    'preco_unitario': float(item.preco_unitario or 0.0),
                    'desconto_rateado': desconto_rateado,
                    'receita_liquida': linha_liquida,
                    'custo_medio': float((produto.preco_custo if produto else 0.0) or 0.0),
                    'custo_total': custo_linha,
                    'lucro_bruto': lucro_linha,
                    'margem_percentual': margem_pct,
                }
            )

        lucro_total = round(receita_liquida - custo_total, 2)
        margem_total = round((lucro_total / receita_liquida) * 100, 2) if receita_liquida else 0.0
        return {
            'subtotal_bruto': round(subtotal, 2),
            'desconto_rateado': round(desconto_total, 2),
            'receita_liquida': round(receita_liquida, 2),
            'custo_total': round(custo_total, 2),
            'lucro_bruto': lucro_total,
            'margem_percentual': margem_total,
            'itens': itens,
        }

    def sugerir_venda_cruzada(self, produto_id, *, limit=3, janela_dias=90):
        inicio = datetime.utcnow() - timedelta(days=max(int(janela_dias or 90), 1))
        base_item = aliased(ItemPedido)
        combo_item = aliased(ItemPedido)

        rows = (
            self.session.query(
                combo_item.produto_id.label('produto_id'),
                Produto.nome.label('produto_nome'),
                Produto.codigo.label('codigo'),
                Categoria.nome.label('categoria'),
                func.count(func.distinct(combo_item.pedido_id)).label('frequencia'),
            )
            .join(base_item, db.and_(
                base_item.pedido_id == combo_item.pedido_id,
                base_item.produto_id == produto_id,
                combo_item.produto_id != produto_id,
            ))
            .join(Pedido, Pedido.id == combo_item.pedido_id)
            .join(Produto, Produto.id == combo_item.produto_id)
            .outerjoin(Categoria, Categoria.id == Produto.categoria_id)
            .filter(
                Pedido.status == Pedido.STATUS_FECHADO,
                Pedido.fechado_em >= inicio,
            )
            .group_by(combo_item.produto_id, Produto.nome, Produto.codigo, Categoria.nome)
            .order_by(func.count(func.distinct(combo_item.pedido_id)).desc(), Produto.nome.asc())
            .limit(limit)
            .all()
        )

        return [
            {
                'produto_id': row.produto_id,
                'produto': row.produto_nome,
                'codigo': row.codigo,
                'categoria': row.categoria,
                'frequencia_compra_conjunta': int(row.frequencia or 0),
            }
            for row in rows
        ]

    def consolidar_itens_lote(self, itens_payload):
        consolidado = defaultdict(int)
        for item in itens_payload or []:
            produto_id = item.get('produto_id')
            quantidade = item.get('quantidade', 0)
            try:
                produto_id = int(produto_id)
                quantidade = int(quantidade)
            except (TypeError, ValueError):
                raise ValidationError('Item invalido para processamento em lote.')
            if quantidade <= 0:
                raise ValidationError('Quantidade deve ser maior que zero.')
            consolidado[produto_id] += quantidade
        return dict(consolidado)

    def gerar_talao_payload(self, pedido):
        troco = 0.0
        if pedido.valor_pago is not None:
            troco = round(max(float(pedido.valor_pago or 0.0) - float(pedido.total or 0.0), 0.0), 2)
        return {
            'pedido_id': pedido.id,
            'emitido_em': pedido.fechado_em.isoformat() if pedido.fechado_em else datetime.utcnow().isoformat(),
            'caixa': pedido.caixa.nome if pedido.caixa else None,
            'metodo_pagamento': pedido.metodo_pagamento,
            'total': float(pedido.total or 0.0),
            'valor_pago': float(pedido.valor_pago or 0.0) if pedido.valor_pago is not None else None,
            'troco': troco,
            'itens': [
                {
                    'produto_id': item.produto_id,
                    'produto': item.produto.nome if item.produto else f'Produto {item.produto_id}',
                    'categoria': item.produto.categoria.nome if item.produto and item.produto.categoria else None,
                    'quantidade': int(item.quantidade or 0),
                    'preco_unitario': float(item.preco_unitario or 0.0),
                    'subtotal': float((item.quantidade or 0) * (item.preco_unitario or 0.0)),
                }
                for item in pedido.itens
            ],
        }

    def _agrupar_itens_por_produto(self, itens):
        agregados = defaultdict(int)
        for item in itens:
            agregados[item.produto_id] += int(item.quantidade or 0)
        return dict(agregados)

    def _carregar_produtos_para_fechamento(self, produto_ids):
        query = (
            self.session.query(Produto)
            .options(joinedload(Produto.categoria))
            .filter(Produto.id.in_(produto_ids))
            .order_by(Produto.id.asc())
        )
        if self.session.bind and self.session.bind.dialect.name == 'postgresql':
            query = query.with_for_update()
        return {produto.id: produto for produto in query.all()}

    def _validar_estoque(self, produtos, itens_por_produto):
        for produto_id, quantidade in itens_por_produto.items():
            produto = produtos.get(produto_id)
            if not produto:
                raise NotFound(f'Produto {produto_id} nao encontrado.')
            if not produto.ativo:
                raise BusinessRuleError(f'Produto "{produto.nome}" esta inativo.')
            if produto.vencido:
                raise BusinessRuleError(f'Produto "{produto.nome}" esta vencido e nao pode ser vendido.')
            if produto.quantidade_estoque < quantidade:
                raise BusinessRuleError(f'Estoque insuficiente para "{produto.nome}".')

    def _aplicar_baixa_estoque(self, pedido, produtos, itens_por_produto, *, actor=None):
        if pedido.estoque_processado:
            return
        for produto_id, quantidade in itens_por_produto.items():
            produto = produtos[produto_id]
            produto.quantidade_estoque -= quantidade
            movimentacao = Movimentacao(
                produto_id=produto.id,
                pedido_id=pedido.id,
                tipo=Movimentacao.TIPO_SAIDA,
                quantidade=quantidade,
                motivo='venda',
                observacoes=f'Pedido {pedido.id} fechado pelo PDV',
            )
            self.session.add(movimentacao)
            self.session.flush()
            record_process_event(
                processo_tipo='pedido_venda',
                etapa='estoque',
                acao='movimentacao_estoque_gerada',
                entidade='movimentacao',
                entidade_id=movimentacao.id,
                pedido_id=pedido.id,
                actor=actor,
                detalhes={
                    'produto_id': produto.id,
                    'quantidade': quantidade,
                    'tipo': Movimentacao.TIPO_SAIDA,
                },
            )

    def _aplicar_financeiro_caixa(self, pedido, *, actor=None):
        if pedido.financeiro_processado:
            return
        caixa = pedido.caixa or (self.session.get(Caixa, pedido.caixa_id) if pedido.caixa_id else None)
        if not caixa:
            raise NotFound('Caixa do pedido nao encontrada.')
        if not caixa.aberto:
            raise BusinessRuleError('Caixa do pedido esta fechada.')

        valor = float(pedido.total or 0.0)
        caixa.saldo_atual = float(caixa.saldo_atual or 0.0) + valor
        self.session.add(
            MovimentacaoCaixa(
                caixa_id=caixa.id,
                tipo=MovimentacaoCaixa.TIPO_ENTRADA,
                valor=valor,
                descricao=f'Fechamento do pedido #{pedido.id}',
            )
        )
        record_process_event(
            processo_tipo='pedido_venda',
            etapa='financeiro',
            acao='caixa_atualizado',
            entidade='pedido',
            entidade_id=pedido.id,
            pedido_id=pedido.id,
            actor=actor,
            detalhes={
                'caixa_id': caixa.id,
                'valor': valor,
            },
        )

    def _criar_lancamento_financeiro_pdv(self, pedido, *, actor=None, incluir_contabilidade=False):
        referencia = f'PDV-{pedido.id}'
        lancamento = LancamentoFinanceiro(
            tipo=LancamentoFinanceiro.TIPO_RECEITA,
            categoria='pdv',
            descricao=f'Receita do pedido #{pedido.id}',
            valor=float(pedido.total or 0.0),
            data_competencia=(pedido.fechado_em or datetime.utcnow()).date(),
            incluir_contabilidade=bool(incluir_contabilidade),
            referencia_documento=referencia,
            centro_custo='PDV',
            pedido_id=pedido.id,
        )
        self.session.add(lancamento)
        self.session.flush()
        record_process_event(
            processo_tipo='financeiro_operacional',
            etapa='lancamento',
            acao='lancamento_pdv_gerado',
            entidade='lancamento_financeiro',
            entidade_id=lancamento.id,
            pedido_id=pedido.id,
            lancamento_financeiro_id=lancamento.id,
            actor=actor,
            detalhes={'valor': lancamento.valor, 'categoria': lancamento.categoria},
        )
        return lancamento

    def _montar_alertas_pos_venda(self, pedido):
        alertas = []
        for item in pedido.itens:
            produto = item.produto
            if not produto:
                continue
            estoque_restante = int(produto.quantidade_estoque or 0)
            if estoque_restante <= int(produto.quantidade_minima or 0):
                alertas.append(
                    {
                        'type': 'low_stock',
                        'product_id': produto.id,
                        'message': (
                            f'O produto {produto.nome} foi adicionado. '
                            f'Aviso: O stock deste item esta abaixo do minimo '
                            f'(Restam {estoque_restante} un).'
                        ),
                    }
                )
        return alertas

    def _serializar_produto_busca(self, produto, *, score):
        return {
            'produto_id': produto.id,
            'codigo': produto.codigo,
            'nome': produto.nome,
            'categoria': produto.categoria.nome if produto.categoria else None,
            'preco_venda': float(produto.preco_venda or 0.0),
            'preco_custo': float(produto.preco_custo or 0.0),
            'quantidade_estoque': int(produto.quantidade_estoque or 0),
            'quantidade_minima': int(produto.quantidade_minima or 0),
            'score_mode': score,
        }


def processar_venda_rapida(pedido_id, **kwargs):
    return VendaService().processar_venda_rapida(pedido_id, **kwargs)


def buscar_produtos_pdv(termo, *, limit=12):
    return VendaService().buscar_produtos_pdv(termo, limit=limit)


def calcular_runway_estoque(*, janela_dias=30, limit=50):
    return VendaService().calcular_runway_estoque(janela_dias=janela_dias, limit=limit)


def sugerir_venda_cruzada(produto_id, *, limit=3, janela_dias=90):
    return VendaService().sugerir_venda_cruzada(produto_id, limit=limit, janela_dias=janela_dias)
