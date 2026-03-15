import json
import re
import unicodedata
from urllib.parse import urlparse

from flask import Blueprint, abort, current_app, flash, redirect, render_template, request, session, url_for
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from sqlalchemy import or_

from app.services.utils_service import _normalizar_contato, _to_float
from app.utils.helpers import slugify
from app.utils.validators import validar_cep, validar_email, validar_telefone
from models import Categoria, ClientePublico, EmpresaConfig, Garcom, ItemPedido, Mesa, Pedido, Produto, db
from realtime import publish_alert
from app.utils.payment_config import default_payment_id, load_payment_options, payment_methods_map


CLIENTE_SESSION_KEY = 'qr_clientes'
SITE_CART_SESSION_KEY = 'site_carrinho'
SITE_CUSTOMER_SESSION_KEY = 'site_cliente_cadastro'
PEDIDO_CONFIRMACAO_SALT = 'pedido-site-confirmacao'


def _obter_empresa_config():
    empresa = EmpresaConfig.query.first()
    if not empresa:
        empresa = EmpresaConfig()
        db.session.add(empresa)
        db.session.commit()
    return empresa


def _serializer_confirmacao_pedido():
    return URLSafeTimedSerializer(current_app.config['SECRET_KEY'], salt=PEDIDO_CONFIRMACAO_SALT)


def _gerar_token_confirmacao_pedido(pedido_id):
    return _serializer_confirmacao_pedido().dumps({'pedido_id': int(pedido_id), 'origem': 'site'})


def _token_confirmacao_pedido_valido(pedido_id, token):
    if not token:
        return False
    try:
        payload = _serializer_confirmacao_pedido().loads(token, max_age=60 * 60 * 24 * 15)
    except (BadSignature, SignatureExpired):
        return False
    return payload.get('origem') == 'site' and int(payload.get('pedido_id') or 0) == int(pedido_id)


def _destino_interno_seguro(destino):
    texto = (destino or '').strip()
    if not texto:
        return None
    parsed = urlparse(texto)
    if parsed.scheme or parsed.netloc:
        host_atual = urlparse(request.host_url).netloc
        if parsed.netloc != host_atual:
            return None
        caminho = parsed.path or '/'
        if not caminho.startswith('/'):
            caminho = f'/{caminho}'
        return f'{caminho}?{parsed.query}' if parsed.query else caminho
    if not texto.startswith('/') or texto.startswith('//'):
        return None
    return texto


def _redirect_interno_seguro(destino, fallback):
    return redirect(_destino_interno_seguro(destino) or fallback)


def _slugify(texto):
    return slugify(texto) or 'cliente'


def _atendimento_mesas_ativo():
    empresa = _obter_empresa_config()
    return empresa.atendimento_mesas_ativo is not False


def _ecommerce_site_ativo(empresa=None):
    empresa = empresa or _obter_empresa_config()
    return empresa.ecommerce_ativo is not False


def _redirecionar_loja_inativa():
    if session.get('funcionario_id'):
        return redirect(url_for('boas_vindas'))
    return redirect(url_for('login'))


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
    if not empresa or empresa.atendimento_mesas_ativo is False or not empresa.distribuicao_ativa:
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


def _normalizar_quantidade(valor, minimo=1, maximo=99, default=1):
    try:
        quantidade = int(valor)
    except (TypeError, ValueError):
        quantidade = int(default)
    if quantidade < minimo:
        return minimo
    if quantidade > maximo:
        return maximo
    return quantidade


def _obter_carrinho_site():
    carrinho_bruto = session.get(SITE_CART_SESSION_KEY, {})
    if not isinstance(carrinho_bruto, dict):
        carrinho_bruto = {}

    carrinho = {}
    for produto_id, quantidade in carrinho_bruto.items():
        try:
            produto_int = int(produto_id)
            quantidade_int = int(quantidade)
        except (TypeError, ValueError):
            continue
        if quantidade_int <= 0:
            continue
        carrinho[str(produto_int)] = min(quantidade_int, 99)

    if carrinho != carrinho_bruto:
        session[SITE_CART_SESSION_KEY] = carrinho
        session.modified = True

    return carrinho


def _salvar_carrinho_site(carrinho):
    normalizado = {}
    for produto_id, quantidade in (carrinho or {}).items():
        try:
            produto_int = int(produto_id)
            quantidade_int = int(quantidade)
        except (TypeError, ValueError):
            continue
        if quantidade_int <= 0:
            continue
        normalizado[str(produto_int)] = min(quantidade_int, 99)

    session[SITE_CART_SESSION_KEY] = normalizado
    session.modified = True


def _dados_cliente_padrao():
    return {
        'nome': '',
        'email': '',
        'celular': '',
        'cpf_cnpj': '',
        'cep': '',
        'endereco': '',
        'numero': '',
        'complemento': '',
        'bairro': '',
        'cidade': '',
        'estado': '',
        'referencia': '',
        'observacoes': '',
        'recebe_ofertas': False,
    }


def _obter_cliente_site_sessao():
    dados = session.get(SITE_CUSTOMER_SESSION_KEY, {})
    defaults = _dados_cliente_padrao()
    if not isinstance(dados, dict):
        return defaults

    resultado = dict(defaults)
    for chave in defaults:
        if chave not in dados:
            continue
        if chave == 'recebe_ofertas':
            resultado[chave] = bool(dados.get(chave))
        else:
            resultado[chave] = (dados.get(chave) or '').strip()
    return resultado


def _salvar_cliente_site_sessao(dados):
    defaults = _dados_cliente_padrao()
    payload = {}
    for chave in defaults:
        if chave == 'recebe_ofertas':
            payload[chave] = bool(dados.get(chave))
        else:
            payload[chave] = (dados.get(chave) or '').strip()
    session[SITE_CUSTOMER_SESSION_KEY] = payload
    session.modified = True


def _coletar_dados_cliente_form(form_data):
    dados = {
        'nome': (form_data.get('nome') or '').strip(),
        'email': (form_data.get('email') or '').strip().lower(),
        'celular': (form_data.get('celular') or '').strip(),
        'cpf_cnpj': (form_data.get('cpf_cnpj') or '').strip(),
        'cep': (form_data.get('cep') or '').strip(),
        'endereco': (form_data.get('endereco') or '').strip(),
        'numero': (form_data.get('numero') or '').strip(),
        'complemento': (form_data.get('complemento') or '').strip(),
        'bairro': (form_data.get('bairro') or '').strip(),
        'cidade': (form_data.get('cidade') or '').strip(),
        'estado': (form_data.get('estado') or '').strip().upper(),
        'referencia': (form_data.get('referencia') or '').strip(),
        'observacoes': (form_data.get('observacoes') or '').strip(),
        'recebe_ofertas': (form_data.get('recebe_ofertas') == 'on'),
    }

    erros = []
    if not dados['nome']:
        erros.append('Informe o nome completo.')
    if not validar_email(dados['email']):
        erros.append('Informe um e-mail valido.')
    if not validar_telefone(dados['celular']):
        erros.append('Informe um celular valido com DDD.')
    cep = validar_cep(dados['cep'])
    if not cep:
        erros.append('Informe o CEP.')
    elif cep == '__invalid__':
        erros.append('Informe um CEP valido.')
    if not dados['endereco']:
        erros.append('Informe o endereco.')
    if not dados['numero']:
        erros.append('Informe o numero do endereco.')
    if not dados['bairro']:
        erros.append('Informe o bairro.')
    if not dados['cidade']:
        erros.append('Informe a cidade.')
    if len(dados['estado']) != 2:
        erros.append('Informe o estado com 2 letras.')

    return dados, erros


def _upsert_cliente_publico(dados):
    filtros = []
    email = validar_email(dados.get('email'))
    celular = validar_telefone(dados.get('celular')) or _normalizar_contato(dados.get('celular'))
    cpf_cnpj = _normalizar_contato(dados.get('cpf_cnpj'))

    if email:
        filtros.append(db.func.lower(ClientePublico.email) == email)
    if celular:
        filtros.append(ClientePublico.celular == celular)
    if cpf_cnpj:
        filtros.append(ClientePublico.cpf_cnpj == cpf_cnpj)

    cliente = None
    if filtros:
        cliente = ClientePublico.query.filter(or_(*filtros)).order_by(ClientePublico.atualizado_em.desc()).first()

    if not cliente:
        cliente = ClientePublico()
        db.session.add(cliente)

    cliente.nome = dados.get('nome')
    cliente.email = email
    cliente.celular = celular or (dados.get('celular') or '').strip()
    cliente.cpf_cnpj = cpf_cnpj or None
    cliente.cep = dados.get('cep') or None
    cliente.endereco = dados.get('endereco') or None
    cliente.numero = dados.get('numero') or None
    cliente.complemento = dados.get('complemento') or None
    cliente.bairro = dados.get('bairro') or None
    cliente.cidade = dados.get('cidade') or None
    cliente.estado = dados.get('estado') or None
    cliente.referencia = dados.get('referencia') or None
    cliente.observacoes = dados.get('observacoes') or None
    cliente.recebe_ofertas = bool(dados.get('recebe_ofertas'))
    return cliente


def obter_resumo_carrinho_site():
    carrinho = _obter_carrinho_site()
    if not carrinho:
        return {'itens': [], 'subtotal': 0.0, 'quantidade_itens': 0}

    produto_ids = [int(produto_id) for produto_id in carrinho.keys()]
    produtos = Produto.query.filter(Produto.id.in_(produto_ids)).all()
    produtos_por_id = {produto.id: produto for produto in produtos}

    itens = []
    subtotal = 0.0
    mudou = False
    for produto_id, quantidade in list(carrinho.items()):
        produto = produtos_por_id.get(int(produto_id))
        if not produto or not produto.ativo or not produto.disponivel_para_venda:
            carrinho.pop(produto_id, None)
            mudou = True
            continue

        quantidade_int = _normalizar_quantidade(quantidade, minimo=1, maximo=99, default=1)
        if quantidade_int != quantidade:
            carrinho[produto_id] = quantidade_int
            mudou = True

        total_item = float(produto.preco_venda or 0.0) * quantidade_int
        subtotal += total_item
        itens.append({
            'produto': produto,
            'quantidade': quantidade_int,
            'total_item': total_item,
        })

    if mudou:
        _salvar_carrinho_site(carrinho)

    return {
        'itens': itens,
        'subtotal': round(subtotal, 2),
        'quantidade_itens': sum(item['quantidade'] for item in itens),
    }


def _coletar_pagamento_checkout(form_data, total_pedido, metodos_validos):
    metodo = (form_data.get('metodo_pagamento') or '').strip().lower()
    if metodo not in metodos_validos:
        raise ValueError('Selecione um metodo de pagamento valido.')

    total = float(total_pedido or 0.0)
    valor_pago = total
    troco = 0.0
    detalhes = {}
    if metodo == 'dinheiro':
        valor_recebido = _to_float(form_data.get('valor_recebido'), 0.0)
        if valor_recebido < total:
            raise ValueError('Valor recebido em dinheiro e menor que o total do pedido.')
        valor_pago = valor_recebido
        troco = max(valor_recebido - total, 0.0)
        detalhes['valor_recebido'] = round(valor_recebido, 2)

    return {
        'metodo': metodo,
        'metodo_label': metodos_validos[metodo],
        'valor_pago': round(valor_pago, 2),
        'troco': round(troco, 2),
        'detalhes': detalhes,
    }


def register_public_routes(app):
    bp = Blueprint('public', __name__)

    @bp.route('/cliente/cadastro', methods=['GET', 'POST'])
    def cadastro_cliente_site():
        empresa = _obter_empresa_config()
        if not _ecommerce_site_ativo(empresa):
            return _redirecionar_loja_inativa()
        resumo_carrinho = obter_resumo_carrinho_site()
        cliente_dados = _obter_cliente_site_sessao()
        proximo_seguro = _destino_interno_seguro(request.args.get('proximo'))

        if request.method == 'POST':
            cliente_dados, erros = _coletar_dados_cliente_form(request.form)
            if erros:
                for erro in erros:
                    flash(erro, 'warning')
            else:
                try:
                    _upsert_cliente_publico(cliente_dados)
                    db.session.commit()
                    _salvar_cliente_site_sessao(cliente_dados)
                    flash('Cadastro do cliente salvo com sucesso.', 'success')
                    proximo = (request.form.get('proximo') or '').strip()
                    if proximo:
                        return _redirect_interno_seguro(proximo, url_for('public.checkout_site'))
                    return redirect(url_for('public.checkout_site'))
                except Exception as e:
                    db.session.rollback()
                    flash(f'Nao foi possivel salvar o cadastro: {str(e)}', 'danger')

        return render_template(
            'public/cadastro_cliente.html',
            empresa=empresa,
            resumo_carrinho=resumo_carrinho,
            cliente_dados=cliente_dados,
            proximo_seguro=proximo_seguro,
        )

    @bp.route('/carrinho', methods=['GET'])
    def carrinho_site():
        empresa = _obter_empresa_config()
        if not _ecommerce_site_ativo(empresa):
            return _redirecionar_loja_inativa()
        resumo_carrinho = obter_resumo_carrinho_site()
        ids_no_carrinho = {item['produto'].id for item in resumo_carrinho['itens']}
        query_destaque = Produto.query.filter(
            Produto.ativo.is_(True),
            Produto.status_disponibilidade.in_(Produto.STATUS_DISPONIBILIDADE_ONLINE_EQUIVALENTES)
        )
        if ids_no_carrinho:
            query_destaque = query_destaque.filter(~Produto.id.in_(list(ids_no_carrinho)))
        produtos_destaque = query_destaque.order_by(Produto.atualizado_em.desc()).limit(6).all()

        return render_template(
            'public/carrinho.html',
            empresa=empresa,
            resumo_carrinho=resumo_carrinho,
            produtos_destaque=produtos_destaque,
        )

    @bp.route('/carrinho/adicionar', methods=['POST'])
    def adicionar_item_carrinho_site():
        if not _ecommerce_site_ativo():
            return _redirecionar_loja_inativa()
        destino = _destino_interno_seguro(request.form.get('next')) or _destino_interno_seguro(request.referrer) or url_for('index')
        produto_id = request.form.get('produto_id', type=int)
        quantidade = _normalizar_quantidade(request.form.get('quantidade'), minimo=1, maximo=99, default=1)

        produto = Produto.query.get(produto_id) if produto_id else None
        if not produto or not produto.ativo or not produto.disponivel_para_venda:
            flash('Produto indisponivel para venda no momento.', 'warning')
            return redirect(destino)

        carrinho = _obter_carrinho_site()
        qtd_atual = int(carrinho.get(str(produto.id), 0))
        carrinho[str(produto.id)] = min(qtd_atual + quantidade, 99)
        _salvar_carrinho_site(carrinho)
        flash(f'"{produto.nome}" adicionado ao carrinho.', 'success')
        return redirect(destino)

    @bp.route('/carrinho/atualizar', methods=['POST'])
    def atualizar_carrinho_site():
        if not _ecommerce_site_ativo():
            return _redirecionar_loja_inativa()
        carrinho = _obter_carrinho_site()
        if not carrinho:
            flash('Seu carrinho esta vazio.', 'warning')
            return redirect(url_for('public.carrinho_site'))

        for produto_id in list(carrinho.keys()):
            campo = f'quantidade_{produto_id}'
            if campo not in request.form:
                continue
            quantidade_raw = request.form.get(campo)
            try:
                quantidade = int(quantidade_raw)
            except (TypeError, ValueError):
                quantidade = 1

            if quantidade <= 0:
                carrinho.pop(produto_id, None)
            else:
                carrinho[produto_id] = _normalizar_quantidade(quantidade, minimo=1, maximo=99, default=1)

        _salvar_carrinho_site(carrinho)
        flash('Carrinho atualizado.', 'success')
        return redirect(url_for('public.carrinho_site'))

    @bp.route('/carrinho/remover', methods=['POST'])
    def remover_item_carrinho_site():
        if not _ecommerce_site_ativo():
            return _redirecionar_loja_inativa()
        produto_id = request.form.get('produto_id', type=int)
        carrinho = _obter_carrinho_site()
        if produto_id and str(produto_id) in carrinho:
            carrinho.pop(str(produto_id), None)
            _salvar_carrinho_site(carrinho)
            flash('Item removido do carrinho.', 'success')
        else:
            flash('Item nao encontrado no carrinho.', 'warning')
        return redirect(url_for('public.carrinho_site'))

    @bp.route('/checkout', methods=['GET', 'POST'])
    def checkout_site():
        empresa = _obter_empresa_config()
        if not _ecommerce_site_ativo(empresa):
            return _redirecionar_loja_inativa()
        resumo_carrinho = obter_resumo_carrinho_site()
        if not resumo_carrinho['itens']:
            flash('Adicione itens ao carrinho antes de finalizar.', 'warning')
            return redirect(url_for('public.carrinho_site'))

        payment_options = load_payment_options(empresa.pagamentos_ecommerce_json, 'ecommerce')
        payment_methods = payment_methods_map(empresa.pagamentos_ecommerce_json, 'ecommerce')
        default_payment = default_payment_id(empresa.pagamentos_ecommerce_json, 'ecommerce') or 'pix'
        cliente_dados = _obter_cliente_site_sessao()
        pagamento_selecionado = (request.form.get('metodo_pagamento') or default_payment).strip().lower() if request.method == 'POST' else default_payment
        valor_recebido = (request.form.get('valor_recebido') or '').strip() if request.method == 'POST' else ''

        if request.method == 'POST':
            cliente_dados, erros = _coletar_dados_cliente_form(request.form)
            if erros:
                for erro in erros:
                    flash(erro, 'warning')
            else:
                try:
                    pagamento = _coletar_pagamento_checkout(request.form, resumo_carrinho['subtotal'], payment_methods)
                    cliente_db = _upsert_cliente_publico(cliente_dados)
                    db.session.flush()

                    pedido = Pedido(
                        cliente_nome=cliente_dados.get('nome'),
                        cliente_celular=cliente_dados.get('celular'),
                        status='aberto',
                        origem='site',
                        total=float(resumo_carrinho['subtotal'] or 0.0),
                        metodo_pagamento=pagamento['metodo_label'],
                        valor_pago=pagamento['valor_pago'],
                        estoque_processado=False,
                        financeiro_processado=False,
                    )
                    db.session.add(pedido)
                    db.session.flush()

                    for item in resumo_carrinho['itens']:
                        produto = item['produto']
                        db.session.add(ItemPedido(
                            pedido_id=pedido.id,
                            produto_id=produto.id,
                            quantidade=item['quantidade'],
                            preco_unitario=produto.preco_venda
                        ))

                    pedido.observacoes = json.dumps({
                        'cliente_publico_id': cliente_db.id,
                        'cliente_cadastro': cliente_dados,
                        'pagamento': {
                            'metodo': pagamento['metodo'],
                            'metodo_label': pagamento['metodo_label'],
                            'troco': pagamento['troco'],
                            'detalhes': pagamento['detalhes'],
                        },
                        'origem_checkout': 'home_varejo',
                    }, ensure_ascii=False)

                    db.session.commit()
                    try:
                        publish_alert({
                            'pedido_id': pedido.id,
                            'origem': 'site',
                            'cliente_nome': pedido.cliente_nome,
                            'itens': [
                                {'produto': item['produto'].nome, 'quantidade': item['quantidade']}
                                for item in resumo_carrinho['itens']
                            ],
                            'criado_em': pedido.criado_em.isoformat() if pedido.criado_em else None
                        })
                    except Exception:
                        pass

                    _salvar_cliente_site_sessao(cliente_dados)
                    _salvar_carrinho_site({})
                    token_confirmacao = _gerar_token_confirmacao_pedido(pedido.id)

                    flash(f'Pedido #{pedido.id} recebido com sucesso.', 'success')
                    return redirect(url_for('public.pedido_confirmado_site', pedido_id=pedido.id, token=token_confirmacao))
                except ValueError as e:
                    db.session.rollback()
                    flash(str(e), 'warning')
                except Exception as e:
                    db.session.rollback()
                    flash(f'Nao foi possivel concluir seu pedido: {str(e)}', 'danger')

        return render_template(
            'public/checkout.html',
            empresa=empresa,
            resumo_carrinho=resumo_carrinho,
            cliente_dados=cliente_dados,
            payment_options=payment_options,
            pagamento_selecionado=pagamento_selecionado,
            valor_recebido=valor_recebido,
        )

    @bp.route('/pedido/<int:pedido_id>/confirmado', methods=['GET'])
    def pedido_confirmado_site(pedido_id):
        empresa = _obter_empresa_config()
        if not _ecommerce_site_ativo(empresa):
            return _redirecionar_loja_inativa()
        token = (request.args.get('token') or '').strip()
        if not _token_confirmacao_pedido_valido(pedido_id, token):
            abort(404)
        pedido = Pedido.query.filter_by(id=pedido_id, origem='site').first_or_404()
        detalhes = {}
        if pedido.observacoes:
            try:
                detalhes = json.loads(pedido.observacoes)
            except Exception:
                detalhes = {}

        return render_template(
            'public/pedido_confirmado.html',
            empresa=empresa,
            pedido=pedido,
            detalhes=detalhes,
            resumo_carrinho=obter_resumo_carrinho_site(),
        )

    @bp.route('/m/<token>', methods=['GET'])
    def cardapio_mesa(token):
        if not _atendimento_mesas_ativo():
            abort(404)
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
        if not _atendimento_mesas_ativo():
            abort(404)
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
        if not _atendimento_mesas_ativo():
            abort(404)
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
        if not _atendimento_mesas_ativo():
            abort(404)
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
            cliente_celular=cliente.get('celular'),
            estoque_processado=False,
            financeiro_processado=False
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
