import re
import unicodedata

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from models import Categoria, EmpresaConfig, Garcom, ItemPedido, Mesa, Pedido, Produto, db
from realtime import publish_alert


CLIENTE_SESSION_KEY = 'qr_clientes'


def _obter_empresa_config():
    empresa = EmpresaConfig.query.first()
    if not empresa:
        empresa = EmpresaConfig()
        db.session.add(empresa)
        db.session.commit()
    return empresa


def _slugify(texto):
    normalizado = unicodedata.normalize('NFKD', (texto or '').strip())
    ascii_texto = normalizado.encode('ascii', 'ignore').decode('ascii').lower()
    ascii_texto = re.sub(r'[^a-z0-9]+', '-', ascii_texto).strip('-')
    return ascii_texto or 'cliente'


def _status_legivel(status):
    labels = {
        'aberto': 'Aberto',
        'em_preparo': 'Em preparo',
        'entregue': 'Entregue',
        'fechado': 'Venda concluida',
        'cancelado': 'Cancelado'
    }
    return labels.get(status, status)


def _atribuir_garcom_automatico(empresa):
    if not empresa or not empresa.distribuicao_ativa:
        return None

    garcons_ativos = Garcom.query.filter_by(ativo=True).order_by(Garcom.nome.asc()).all()
    if not garcons_ativos:
        return None

    modo = (empresa.modo_distribuicao_pedidos or 'round_robin').lower()
    if modo == 'manual':
        return None

    if modo == 'menos_pedidos':
        candidatos = []
        for garcom in garcons_ativos:
            em_andamento = Pedido.query.filter(
                Pedido.garcom_id == garcom.id,
                Pedido.status.in_(['aberto', 'em_preparo'])
            ).count()
            candidatos.append((em_andamento, garcom.id))
        candidatos.sort(key=lambda item: (item[0], item[1]))
        return candidatos[0][1] if candidatos else None

    ids = [g.id for g in garcons_ativos]
    if empresa.ultimo_garcom_id in ids:
        idx = ids.index(empresa.ultimo_garcom_id)
        proximo_idx = (idx + 1) % len(ids)
    else:
        proximo_idx = 0

    escolhido_id = ids[proximo_idx]
    empresa.ultimo_garcom_id = escolhido_id
    db.session.flush()
    return escolhido_id


def _obter_cliente_qr(token):
    clientes = session.get(CLIENTE_SESSION_KEY, {})
    return clientes.get(token)


def _remover_cliente_qr(token):
    clientes = dict(session.get(CLIENTE_SESSION_KEY, {}))
    if token in clientes:
        clientes.pop(token, None)
        session[CLIENTE_SESSION_KEY] = clientes
        session.modified = True


def _salvar_cliente_qr(token, mesa_id, nome, celular):
    clientes = dict(session.get(CLIENTE_SESSION_KEY, {}))
    clientes[token] = {
        'mesa_id': mesa_id,
        'nome': nome,
        'celular': celular,
        'slug': _slugify(nome)
    }
    session[CLIENTE_SESSION_KEY] = clientes
    session.modified = True


def _obter_cliente_por_mesa_slug(mesa, cliente_slug):
    clientes = session.get(CLIENTE_SESSION_KEY, {})
    mesa_id = mesa.id
    slug_informado = (cliente_slug or '').strip().lower()

    for token, dados in clientes.items():
        if not isinstance(dados, dict):
            continue
        if dados.get('mesa_id') != mesa_id:
            continue
        slug_salvo = (dados.get('slug') or _slugify(dados.get('nome') or '')).lower()
        if slug_salvo == slug_informado:
            dados = dict(dados)
            dados['token'] = token
            dados['slug'] = slug_salvo
            return dados
    return None


def _categorias_com_produtos():
    categorias = Categoria.query.order_by(Categoria.nome.asc()).all()
    resultado = []
    for categoria in categorias:
        produtos = Produto.query.filter_by(categoria_id=categoria.id, ativo=True).order_by(Produto.nome.asc()).all()
        if not produtos:
            continue
        resultado.append({
            'categoria': categoria,
            'produtos': produtos
        })
    return resultado


def _listar_pedidos_cliente(mesa_id, cliente):
    if not cliente:
        return []

    pedidos = Pedido.query.filter_by(
        mesa_id=mesa_id,
        origem='qr',
        cliente_nome=cliente.get('nome'),
        cliente_celular=cliente.get('celular')
    ).order_by(Pedido.criado_em.desc()).all()

    for pedido in pedidos:
        pedido.status_label = _status_legivel(pedido.status)
    return pedidos


def register_public_routes(app):
    bp = Blueprint('public', __name__)

    @bp.route('/m/<token>', methods=['GET'])
    def cardapio_mesa(token):
        mesa = Mesa.query.filter_by(qr_token=token).first_or_404()
        empresa = _obter_empresa_config()
        cliente = _obter_cliente_qr(token)

        if not cliente:
            return render_template('public/abrir_comanda.html', mesa=mesa, empresa=empresa)

        # Compatibilidade com sessoes antigas (sem mesa_id/slug) e dados incompletos.
        cliente_nome = (cliente.get('nome') or '').strip() if isinstance(cliente, dict) else ''
        cliente_celular = (cliente.get('celular') or '').strip() if isinstance(cliente, dict) else ''
        if not cliente_nome or not cliente_celular:
            _remover_cliente_qr(token)
            return render_template('public/abrir_comanda.html', mesa=mesa, empresa=empresa)

        if not isinstance(cliente, dict) or cliente.get('mesa_id') != mesa.id or not cliente.get('slug'):
            _salvar_cliente_qr(token, mesa.id, cliente_nome, cliente_celular)
            cliente = _obter_cliente_qr(token)

        return redirect(
            url_for(
                'public.comanda_cliente',
                mesa_numero=mesa.numero,
                cliente_slug=cliente.get('slug') or _slugify(cliente.get('nome') or '')
            )
        )

    @bp.route('/m/<token>/abrir-comanda', methods=['POST'])
    def abrir_comanda_qr(token):
        mesa = Mesa.query.filter_by(qr_token=token).first_or_404()
        nome = (request.form.get('cliente_nome') or '').strip()
        celular = (request.form.get('cliente_celular') or '').strip()

        if not nome or not celular:
            flash('Informe seu nome e celular para abrir a comanda.', 'warning')
            empresa = _obter_empresa_config()
            return render_template('public/abrir_comanda.html', mesa=mesa, empresa=empresa)

        _salvar_cliente_qr(token, mesa.id, nome, celular)
        return redirect(url_for('public.comanda_cliente', mesa_numero=mesa.numero, cliente_slug=_slugify(nome)))

    @bp.route('/comanda/<mesa_numero>/<cliente_slug>', methods=['GET'])
    def comanda_cliente(mesa_numero, cliente_slug):
        mesa = Mesa.query.filter_by(numero=mesa_numero).first_or_404()
        empresa = _obter_empresa_config()
        cliente = _obter_cliente_por_mesa_slug(mesa, cliente_slug)

        if not cliente:
            flash('Abra a comanda informando nome e celular.', 'warning')
            return redirect(url_for('public.cardapio_mesa', token=mesa.qr_token))

        slug_canonico = cliente.get('slug') or _slugify(cliente.get('nome') or '')
        if slug_canonico != (cliente_slug or '').lower():
            return redirect(url_for('public.comanda_cliente', mesa_numero=mesa.numero, cliente_slug=slug_canonico))

        qtd_max = (empresa.cardapio_qtd_maxima if empresa and empresa.cardapio_qtd_maxima else 20)
        if qtd_max <= 0:
            qtd_max = 20

        return render_template(
            'public/cardapio.html',
            mesa=mesa,
            empresa=empresa,
            qtd_max=qtd_max,
            cliente_nome=cliente.get('nome'),
            cliente_celular=cliente.get('celular'),
            cliente_slug=slug_canonico,
            categorias_cardapio=_categorias_com_produtos(),
            pedidos_cliente=_listar_pedidos_cliente(mesa.id, cliente)
        )

    @bp.route('/comanda/<mesa_numero>/<cliente_slug>/pedido', methods=['POST'])
    def enviar_pedido_qr(mesa_numero, cliente_slug):
        mesa = Mesa.query.filter_by(numero=mesa_numero).first_or_404()
        empresa = _obter_empresa_config()
        cliente = _obter_cliente_por_mesa_slug(mesa, cliente_slug)

        if not cliente:
            flash('Abra a comanda informando nome e celular.', 'warning')
            return redirect(url_for('public.cardapio_mesa', token=mesa.qr_token))

        qtd_max = (empresa.cardapio_qtd_maxima if empresa and empresa.cardapio_qtd_maxima else 20)
        if qtd_max <= 0:
            qtd_max = 20

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
            if quantidade > qtd_max:
                quantidade = qtd_max
            itens.append((produto_id, quantidade))

        if not itens:
            flash('Nenhum item selecionado.', 'warning')
            return redirect(url_for('public.comanda_cliente', mesa_numero=mesa.numero, cliente_slug=cliente.get('slug')))

        pedido = Pedido(
            mesa_id=mesa.id,
            status='aberto',
            origem='qr',
            cliente_nome=cliente.get('nome'),
            cliente_celular=cliente.get('celular')
        )
        db.session.add(pedido)

        pedido.garcom_id = _atribuir_garcom_automatico(empresa)

        total = 0
        itens_alerta = []
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
            itens_alerta.append({'produto': prod.nome, 'quantidade': quantidade})
            db.session.add(item)
        pedido.total = total
        mesa.status = 'ocupada'
        db.session.commit()

        publish_alert({
            'mesa': mesa.numero,
            'pedido_id': pedido.id,
            'cliente_nome': pedido.cliente_nome,
            'garcom': (pedido.garcom.nome if pedido.garcom else None),
            'itens': itens_alerta,
            'criado_em': pedido.criado_em.isoformat()
        })

        flash(f'Pedido #{pedido.id} enviado com sucesso.', 'success')
        return redirect(url_for('public.comanda_cliente', mesa_numero=mesa.numero, cliente_slug=cliente.get('slug')))

    app.register_blueprint(bp)
