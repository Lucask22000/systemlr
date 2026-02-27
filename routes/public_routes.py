from flask import Blueprint, render_template, request, redirect, url_for, flash

from models import Produto, Mesa, Pedido, ItemPedido, db
from realtime import publish_alert


def register_public_routes(app):
    bp = Blueprint('public', __name__)

    @bp.route('/m/<token>', methods=['GET'])
    def cardapio_mesa(token):
        mesa = Mesa.query.filter_by(qr_token=token).first_or_404()
        produtos = Produto.query.filter_by(ativo=True).order_by(Produto.nome.asc()).all()
        return render_template('public/cardapio.html', mesa=mesa, produtos=produtos)

    @bp.route('/m/<token>/pedido', methods=['POST'])
    def enviar_pedido_qr(token):
        mesa = Mesa.query.filter_by(qr_token=token).first_or_404()
        itens = []
        for key, value in request.form.items():
            if not key.startswith('produto_'):
                continue
            try:
                produto_id = int(key.split('_')[1])
                quantidade = int(value)
            except Exception:
                continue
            if quantidade <= 0:
                continue
            itens.append((produto_id, quantidade))

        if not itens:
            flash('Nenhum item selecionado.', 'warning')
            return redirect(url_for('public.cardapio_mesa', token=token))

        pedido = Pedido(mesa_id=mesa.id, status='aberto', origem='qr')
        db.session.add(pedido)
        total = 0
        for produto_id, quantidade in itens:
            prod = Produto.query.get(produto_id)
            if not prod:
                continue
            item = ItemPedido(
                pedido=pedido,
                produto_id=prod.id,
                quantidade=quantidade,
                preco_unitario=prod.preco_venda
            )
            total += quantidade * prod.preco_venda
            db.session.add(item)
        pedido.total = total
        mesa.status = 'ocupada'
        db.session.commit()

        publish_alert({
            'mesa': mesa.numero,
            'pedido_id': pedido.id,
            'itens': [{'produto': Produto.query.get(pid).nome, 'quantidade': qty} for pid, qty in itens],
            'criado_em': pedido.criado_em.isoformat()
        })

        return render_template('public/pedido_enviado.html', mesa=mesa, pedido=pedido)

    app.register_blueprint(bp)
