import json
import re
import unicodedata
from datetime import datetime
from functools import wraps
from urllib.parse import urlencode, urlparse

from flask import Blueprint, abort, current_app, flash, redirect, render_template, request, session, url_for
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from sqlalchemy import and_, func, or_
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import OperationalError, ProgrammingError

from app.exceptions import AppError, BusinessRuleError
from app.services.transaction import atomic_transaction
from app.services.utils_service import _normalizar_contato, _to_float
from app.utils.helpers import slugify
from app.utils.validators import validar_cep, validar_email, validar_telefone
from models import (
    AvaliacaoProduto,
    Categoria,
    ClienteEndereco,
    ClienteFavorito,
    ClientePublico,
    Cupom,
    CupomUtilizacao,
    EmpresaConfig,
    Fornecedor,
    Garcom,
    ItemPedido,
    Mesa,
    Pedido,
    Produto,
    db,
)
from realtime import publish_alert
from app.utils.payment_config import default_payment_id, load_payment_options, payment_methods_map


CLIENTE_SESSION_KEY = 'qr_clientes'
SITE_CART_SESSION_KEY = 'site_carrinho'
SITE_CUSTOMER_SESSION_KEY = 'site_cliente_cadastro'
SITE_PUBLIC_CLIENT_SESSION_KEY = 'site_cliente_id'
SITE_PUBLIC_COUPON_SESSION_KEY = 'site_cupom'
PEDIDO_CONFIRMACAO_SALT = 'pedido-site-confirmacao'


def _schema_has_table(table_name):
    try:
        return db.inspect(db.engine).has_table(table_name)
    except Exception:
        return False


def _schema_has_columns(table_name, expected_columns):
    try:
        if not _schema_has_table(table_name):
            return False
        columns = {col['name'] for col in db.inspect(db.engine).get_columns(table_name)}
        return set(expected_columns).issubset(columns)
    except Exception:
        return False


def _public_accounts_ready():
    return _schema_has_columns('clientes_publicos', {'senha_hash', 'data_cadastro', 'ultimo_acesso'})


def _reviews_ready():
    return _schema_has_table('avaliacoes_produtos')


def _coupons_ready():
    return _schema_has_table('cupons')


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


def _cliente_para_sessao(cliente, endereco=None):
    endereco = endereco or (cliente.endereco_principal if cliente else None)
    dados = _dados_cliente_padrao()
    if not cliente:
        return dados

    dados.update({
        'nome': (cliente.nome or '').strip(),
        'email': (cliente.email or '').strip(),
        'celular': (cliente.celular or '').strip(),
        'cpf_cnpj': (cliente.cpf_cnpj or '').strip(),
        'observacoes': (cliente.observacoes or '').strip(),
        'recebe_ofertas': bool(cliente.recebe_ofertas),
    })
    if endereco:
        dados.update({
            'cep': (endereco.cep or '').strip(),
            'endereco': (endereco.endereco or '').strip(),
            'numero': (endereco.numero or '').strip(),
            'complemento': (endereco.complemento or '').strip(),
            'bairro': (endereco.bairro or '').strip(),
            'cidade': (endereco.cidade or '').strip(),
            'estado': (endereco.estado or '').strip(),
            'referencia': (endereco.referencia or '').strip(),
        })
    else:
        dados.update({
            'cep': (cliente.cep or '').strip(),
            'endereco': (cliente.endereco or '').strip(),
            'numero': (cliente.numero or '').strip(),
            'complemento': (cliente.complemento or '').strip(),
            'bairro': (cliente.bairro or '').strip(),
            'cidade': (cliente.cidade or '').strip(),
            'estado': (cliente.estado or '').strip(),
            'referencia': (cliente.referencia or '').strip(),
        })
    return dados


def _obter_cliente_publico_logado():
    cliente_id = session.get(SITE_PUBLIC_CLIENT_SESSION_KEY)
    if not cliente_id:
        return None
    query = ClientePublico.query
    if _schema_has_table('clientes_enderecos'):
        query = query.options(selectinload(ClientePublico.enderecos))
    if _schema_has_table('clientes_favoritos'):
        query = query.options(selectinload(ClientePublico.favoritos).selectinload(ClienteFavorito.produto))
    return query.get(cliente_id)


def _salvar_cliente_publico_logado(cliente):
    if not cliente:
        session.pop(SITE_PUBLIC_CLIENT_SESSION_KEY, None)
    else:
        session[SITE_PUBLIC_CLIENT_SESSION_KEY] = int(cliente.id)
        _salvar_cliente_site_sessao(_cliente_para_sessao(cliente))
    session.modified = True


def _limpar_sessao_cliente_publico():
    session.pop(SITE_PUBLIC_CLIENT_SESSION_KEY, None)
    session.modified = True


def cliente_login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if not _obter_cliente_publico_logado():
            flash('Faça login para acessar sua conta.', 'warning')
            return redirect(url_for('public.cliente_login_site', next=request.full_path if request.query_string else request.path))
        return view(*args, **kwargs)
    return wrapper


def _coletar_dados_endereco_form(form_data):
    dados = {
        'apelido': (form_data.get('apelido') or '').strip(),
        'cep': (form_data.get('cep') or '').strip(),
        'endereco': (form_data.get('endereco') or '').strip(),
        'numero': (form_data.get('numero') or '').strip(),
        'complemento': (form_data.get('complemento') or '').strip(),
        'bairro': (form_data.get('bairro') or '').strip(),
        'cidade': (form_data.get('cidade') or '').strip(),
        'estado': (form_data.get('estado') or '').strip().upper(),
        'referencia': (form_data.get('referencia') or '').strip(),
        'principal': (form_data.get('principal') == 'on'),
    }
    erros = []
    cep = validar_cep(dados['cep'])
    if not cep:
        erros.append('Informe o CEP do endereço.')
    elif cep == '__invalid__':
        erros.append('Informe um CEP válido.')
    else:
        dados['cep'] = cep
    if not dados['endereco']:
        erros.append('Informe o endereço.')
    if not dados['numero']:
        erros.append('Informe o número do endereço.')
    if not dados['bairro']:
        erros.append('Informe o bairro.')
    if not dados['cidade']:
        erros.append('Informe a cidade.')
    if len(dados['estado']) != 2:
        erros.append('Informe o estado com 2 letras.')
    return dados, erros


def _salvar_endereco_cliente(cliente, dados, endereco=None):
    if endereco is None:
        endereco = ClienteEndereco(cliente=cliente)
        db.session.add(endereco)
    if dados.get('principal'):
        ClienteEndereco.query.filter_by(cliente_id=cliente.id, principal=True).update({'principal': False})
    endereco.apelido = dados.get('apelido') or None
    endereco.cep = dados.get('cep')
    endereco.endereco = dados.get('endereco')
    endereco.numero = dados.get('numero') or None
    endereco.complemento = dados.get('complemento') or None
    endereco.bairro = dados.get('bairro') or None
    endereco.cidade = dados.get('cidade') or None
    endereco.estado = dados.get('estado') or None
    endereco.referencia = dados.get('referencia') or None
    endereco.principal = bool(dados.get('principal'))
    if not cliente.enderecos:
        endereco.principal = True
    return endereco


def _upsert_endereco_principal_cliente(cliente, dados, apelido='Principal'):
    if not cliente:
        return None
    endereco = cliente.endereco_principal
    payload = {
        'apelido': apelido,
        'cep': dados.get('cep'),
        'endereco': dados.get('endereco'),
        'numero': dados.get('numero'),
        'complemento': dados.get('complemento'),
        'bairro': dados.get('bairro'),
        'cidade': dados.get('cidade'),
        'estado': dados.get('estado'),
        'referencia': dados.get('referencia'),
        'principal': True,
    }
    return _salvar_endereco_cliente(cliente, payload, endereco=endereco)


def _parse_json_ids(raw_value):
    if not raw_value:
        return set()
    try:
        values = json.loads(raw_value)
    except Exception:
        return set()
    resultado = set()
    for value in values or []:
        try:
            resultado.add(int(value))
        except (TypeError, ValueError):
            continue
    return resultado


def _base_query_produtos_publicos():
    query = Produto.query.options(
        selectinload(Produto.categoria),
        selectinload(Produto.fornecedor),
    )
    if _schema_has_table('avaliacoes_produtos'):
        query = query.options(selectinload(Produto.avaliacoes))
    return query.filter(
        Produto.ativo.is_(True),
        Produto.filtro_nao_vencidos(),
        Produto.status_disponibilidade.in_(Produto.STATUS_DISPONIBILIDADE_ONLINE_EQUIVALENTES),
    )


def _aplicar_filtros_produtos(query, params):
    busca = (params.get('busca') or '').strip()
    categoria_id = params.get('categoria_id', type=int)
    fornecedor_id = params.get('fornecedor_id', type=int)
    preco_min = params.get('preco_min', type=float)
    preco_max = params.get('preco_max', type=float)
    avaliacao_min = params.get('avaliacao_min', type=float)
    ordenar = (params.get('ordenar') or 'recentes').strip().lower()

    if categoria_id:
        query = query.filter(Produto.categoria_id == categoria_id)
    if fornecedor_id:
        query = query.filter(Produto.fornecedor_id == fornecedor_id)
    if preco_min is not None:
        query = query.filter(Produto.preco_venda >= preco_min)
    if preco_max is not None:
        query = query.filter(Produto.preco_venda <= preco_max)
    if busca:
        termo = f'%{busca}%'
        query = query.filter(
            or_(
                Produto.nome.ilike(termo),
                Produto.codigo.ilike(termo),
                Produto.descricao.ilike(termo),
            )
        )

    usa_avaliacao = bool(avaliacao_min) or ordenar == 'melhor_avaliacao'
    if usa_avaliacao:
        query = query.outerjoin(
            AvaliacaoProduto,
            and_(
                AvaliacaoProduto.produto_id == Produto.id,
                AvaliacaoProduto.aprovada.is_(True),
            )
        ).group_by(Produto.id)
        if avaliacao_min:
            query = query.having(func.coalesce(func.avg(AvaliacaoProduto.nota), 0) >= avaliacao_min)

    if ordenar == 'preco_asc':
        query = query.order_by(Produto.preco_venda.asc(), Produto.nome.asc())
    elif ordenar == 'preco_desc':
        query = query.order_by(Produto.preco_venda.desc(), Produto.nome.asc())
    elif ordenar == 'melhor_avaliacao':
        query = query.order_by(func.coalesce(func.avg(AvaliacaoProduto.nota), 0).desc(), Produto.nome.asc())
    else:
        query = query.order_by(Produto.atualizado_em.desc(), Produto.criado_em.desc())
    return query


def _cliente_ja_comprou_produto(cliente, produto_id):
    if not cliente or not produto_id:
        return False
    if not _schema_has_table('pedidos') or not _schema_has_table('itens_pedido'):
        return False
    return db.session.query(Pedido.id).join(ItemPedido, ItemPedido.pedido_id == Pedido.id).filter(
        Pedido.cliente_publico_id == cliente.id,
        Pedido.status.in_(['entregue', 'fechado']),
        ItemPedido.produto_id == produto_id,
    ).first() is not None


def _carregar_cupom_por_codigo(codigo):
    codigo_limpo = (codigo or '').strip().upper()
    if not codigo_limpo:
        return None
    if not _schema_has_table('cupons'):
        return None
    return Cupom.query.filter(func.upper(Cupom.codigo) == codigo_limpo).first()


def _cupom_pode_ser_usado(cupom, cliente, itens, subtotal):
    hoje = datetime.utcnow().date()
    if not cupom or not cupom.ativo:
        return False, 'Cupom inválido ou indisponível no momento.', []
    if cupom.data_inicio and cupom.data_inicio > hoje:
        return False, 'Este cupom ainda não está vigente.', []
    if cupom.data_fim and cupom.data_fim < hoje:
        return False, 'Este cupom expirou.', []
    if cupom.minimo_compra and float(subtotal or 0) < float(cupom.minimo_compra or 0):
        return False, f'Este cupom exige compra mínima de R$ {float(cupom.minimo_compra):.2f}.', []
    if cupom.primeira_compra:
        if not cliente:
            return False, 'Faça login para usar cupom de primeira compra.', []
        possui_pedido = Pedido.query.filter(
            Pedido.cliente_publico_id == cliente.id,
            Pedido.status != Pedido.STATUS_CANCELADO,
        ).count() > 0
        if possui_pedido:
            return False, 'Este cupom é válido apenas na primeira compra.', []
    if cupom.uso_unico_por_cliente and cliente and _schema_has_table('cupons_utilizacoes'):
        uso_existente = CupomUtilizacao.query.filter_by(cupom_id=cupom.id, cliente_id=cliente.id).first()
        if uso_existente:
            return False, 'Este cupom já foi utilizado na sua conta.', []

    produtos_ids = _parse_json_ids(cupom.produtos_incluidos)
    categorias_ids = _parse_json_ids(cupom.categorias_incluidas)
    itens_elegiveis = []
    for item in itens:
        produto = item['produto']
        if produtos_ids and produto.id not in produtos_ids:
            continue
        if categorias_ids and produto.categoria_id not in categorias_ids:
            continue
        itens_elegiveis.append(item)
    if (produtos_ids or categorias_ids) and not itens_elegiveis:
        return False, 'Os produtos do carrinho não atendem às regras deste cupom.', []
    return True, '', (itens_elegiveis or list(itens))


def _calcular_desconto_cupom(cupom, itens_elegiveis):
    subtotal_elegivel = sum(float(item['total_item'] or 0) for item in itens_elegiveis)
    if subtotal_elegivel <= 0:
        return 0.0
    if cupom.tipo_desconto == 'percentual':
        return round(subtotal_elegivel * (float(cupom.valor or 0) / 100.0), 2)
    if cupom.tipo_desconto == 'fixo':
        return round(min(float(cupom.valor or 0), subtotal_elegivel), 2)
    if cupom.tipo_desconto == 'frete':
        return 0.0
    return 0.0


def _obter_cupom_sessao():
    dados = session.get(SITE_PUBLIC_COUPON_SESSION_KEY)
    return dados if isinstance(dados, dict) else {}


def _salvar_cupom_sessao(cupom):
    session[SITE_PUBLIC_COUPON_SESSION_KEY] = {
        'codigo': (cupom.codigo or '').strip().upper(),
    }
    session.modified = True


def _limpar_cupom_sessao():
    session.pop(SITE_PUBLIC_COUPON_SESSION_KEY, None)
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


def _upsert_cliente_publico(dados, senha=None, cliente=None):
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

    if cliente is None and filtros:
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
    if senha:
        cliente.set_password(senha)
    if not cliente.data_cadastro:
        cliente.data_cadastro = datetime.utcnow()
    return cliente


def obter_resumo_carrinho_site(cliente=None):
    carrinho = _obter_carrinho_site()
    if not carrinho:
        return {
            'itens': [],
            'subtotal': 0.0,
            'desconto': 0.0,
            'total': 0.0,
            'quantidade_itens': 0,
            'cupom': None,
        }

    produto_ids = [int(produto_id) for produto_id in carrinho.keys()]
    produtos = Produto.query.options(
        selectinload(Produto.categoria),
        selectinload(Produto.fornecedor),
        selectinload(Produto.avaliacoes),
    ).filter(Produto.id.in_(produto_ids)).all()
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

    subtotal = round(subtotal, 2)
    desconto = 0.0
    cupom_resumo = None
    cupom_codigo = (_obter_cupom_sessao().get('codigo') or '').strip().upper()
    if cupom_codigo and itens:
        cupom = _carregar_cupom_por_codigo(cupom_codigo)
        valido, mensagem, itens_elegiveis = _cupom_pode_ser_usado(cupom, cliente, itens, subtotal)
        if valido:
            desconto = min(_calcular_desconto_cupom(cupom, itens_elegiveis), subtotal)
            cupom_resumo = {
                'codigo': cupom.codigo,
                'descricao': cupom.descricao,
                'tipo': cupom.tipo_desconto,
                'desconto': round(desconto, 2),
            }
        else:
            _limpar_cupom_sessao()

    return {
        'itens': itens,
        'subtotal': subtotal,
        'desconto': round(desconto, 2),
        'total': round(max(subtotal - desconto, 0.0), 2),
        'quantidade_itens': sum(item['quantidade'] for item in itens),
        'cupom': cupom_resumo,
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

    @bp.route('/cliente/login', methods=['GET', 'POST'])
    def cliente_login_site():
        empresa = _obter_empresa_config()
        if not _ecommerce_site_ativo(empresa):
            return _redirecionar_loja_inativa()
        if not _public_accounts_ready():
            flash('A área do cliente está em atualização. Execute as migrações do e-commerce para ativar este recurso.', 'warning')
            return redirect(url_for('index'))
        if _obter_cliente_publico_logado():
            return redirect(url_for('public.cliente_dashboard'))

        next_dest = _destino_interno_seguro(request.args.get('next') or request.form.get('next'))
        if request.method == 'POST':
            email = validar_email((request.form.get('email') or '').strip().lower())
            senha = (request.form.get('senha') or '').strip()
            if not email or not senha:
                flash('Informe e-mail e senha para entrar.', 'warning')
            else:
                cliente = ClientePublico.query.filter(func.lower(ClientePublico.email) == email).first()
                if not cliente or not cliente.check_password(senha):
                    flash('E-mail ou senha inválidos.', 'danger')
                elif not cliente.senha_hash:
                    flash('Sua conta ainda não possui senha. Atualize seu cadastro para ativar o acesso.', 'warning')
                else:
                    cliente.ultimo_acesso = datetime.utcnow()
                    db.session.commit()
                    _salvar_cliente_publico_logado(cliente)
                    flash(f'Bem-vindo de volta, {cliente.nome}.', 'success')
                    return redirect(next_dest or url_for('public.cliente_dashboard'))

        return render_template(
            'public/cliente_login.html',
            empresa=empresa,
            resumo_carrinho=obter_resumo_carrinho_site(),
            next_dest=next_dest,
        )

    @bp.route('/cliente/logout', methods=['GET', 'POST'])
    def cliente_logout_site():
        cliente = _obter_cliente_publico_logado()
        if cliente:
            flash(f'Até logo, {cliente.nome}.', 'info')
        _limpar_sessao_cliente_publico()
        return redirect(url_for('index'))

    @bp.route('/cliente/cadastro', methods=['GET', 'POST'])
    def cadastro_cliente_site():
        empresa = _obter_empresa_config()
        if not _ecommerce_site_ativo(empresa):
            return _redirecionar_loja_inativa()
        if not _public_accounts_ready():
            flash('O cadastro completo de clientes depende das migrações do e-commerce. Atualize o banco para continuar.', 'warning')
            return redirect(url_for('index'))
        cliente_logado = _obter_cliente_publico_logado()
        resumo_carrinho = obter_resumo_carrinho_site(cliente_logado)
        cliente_dados = _cliente_para_sessao(cliente_logado) if cliente_logado else _obter_cliente_site_sessao()
        proximo_seguro = _destino_interno_seguro(request.args.get('proximo'))

        if request.method == 'POST':
            cliente_dados, erros = _coletar_dados_cliente_form(request.form)
            senha = (request.form.get('senha') or '').strip()
            confirmar_senha = (request.form.get('confirmar_senha') or '').strip()
            if not cliente_logado:
                if len(senha) < 6:
                    erros.append('Crie uma senha com pelo menos 6 caracteres.')
                if senha != confirmar_senha:
                    erros.append('A confirmação da senha não confere.')
            if erros:
                for erro in erros:
                    flash(erro, 'warning')
            else:
                try:
                    cliente = cliente_logado or _upsert_cliente_publico(cliente_dados, senha=senha)
                    if cliente_logado:
                        cliente = _upsert_cliente_publico(cliente_dados, senha=senha if senha else None, cliente=cliente_logado)
                    endereco_principal = _upsert_endereco_principal_cliente(cliente, cliente_dados)
                    db.session.commit()
                    _salvar_cliente_publico_logado(cliente)
                    _salvar_cliente_site_sessao(_cliente_para_sessao(cliente, endereco_principal))
                    flash('Conta do cliente salva com sucesso.', 'success')
                    proximo = (request.form.get('proximo') or '').strip()
                    if proximo:
                        return _redirect_interno_seguro(proximo, url_for('public.checkout_site'))
                    return redirect(url_for('public.cliente_dashboard'))
                except Exception:
                    db.session.rollback()
                    flash('Não foi possível salvar sua conta agora.', 'danger')

        return render_template(
            'public/cadastro_cliente.html',
            empresa=empresa,
            resumo_carrinho=resumo_carrinho,
            cliente_dados=cliente_dados,
            proximo_seguro=proximo_seguro,
            cliente_logado=cliente_logado,
        )

    @bp.route('/cliente')
    @cliente_login_required
    def cliente_dashboard():
        if not _public_accounts_ready():
            flash('A área do cliente ainda não está disponível neste banco.', 'warning')
            return redirect(url_for('index'))
        cliente = _obter_cliente_publico_logado()
        pedidos = Pedido.query.options(
            selectinload(Pedido.itens).selectinload(ItemPedido.produto)
        ).filter_by(cliente_publico_id=cliente.id).order_by(Pedido.criado_em.desc()).limit(5).all()
        favoritos = ClienteFavorito.query.options(
            selectinload(ClienteFavorito.produto).selectinload(Produto.categoria)
        ).filter_by(cliente_id=cliente.id).order_by(ClienteFavorito.criado_em.desc()).limit(8).all()
        avaliacoes = AvaliacaoProduto.query.options(
            selectinload(AvaliacaoProduto.produto)
        ).filter_by(cliente_id=cliente.id).order_by(AvaliacaoProduto.criado_em.desc()).limit(5).all()
        return render_template(
            'cliente/dashboard.html',
            cliente=cliente,
            pedidos=pedidos,
            favoritos=favoritos,
            avaliacoes=avaliacoes,
            resumo_carrinho=obter_resumo_carrinho_site(cliente),
        )

    @bp.route('/cliente/pedidos')
    @cliente_login_required
    def cliente_pedidos():
        if not _public_accounts_ready():
            flash('A área do cliente ainda não está disponível neste banco.', 'warning')
            return redirect(url_for('index'))
        cliente = _obter_cliente_publico_logado()
        pedidos = Pedido.query.options(
            selectinload(Pedido.itens).selectinload(ItemPedido.produto)
        ).filter_by(cliente_publico_id=cliente.id).order_by(Pedido.criado_em.desc()).all()
        return render_template(
            'cliente/pedidos.html',
            cliente=cliente,
            pedidos=pedidos,
            resumo_carrinho=obter_resumo_carrinho_site(cliente),
        )

    @bp.route('/cliente/perfil', methods=['GET', 'POST'])
    @cliente_login_required
    def cliente_perfil():
        if not _public_accounts_ready():
            flash('A área do cliente ainda não está disponível neste banco.', 'warning')
            return redirect(url_for('index'))
        cliente = _obter_cliente_publico_logado()
        if request.method == 'POST':
            cliente_dados, erros = _coletar_dados_cliente_form(request.form)
            nova_senha = (request.form.get('senha') or '').strip()
            confirmar_senha = (request.form.get('confirmar_senha') or '').strip()
            if nova_senha:
                if len(nova_senha) < 6:
                    erros.append('A nova senha deve ter pelo menos 6 caracteres.')
                if nova_senha != confirmar_senha:
                    erros.append('A confirmação da nova senha não confere.')
            if erros:
                for erro in erros:
                    flash(erro, 'warning')
            else:
                try:
                    cliente = _upsert_cliente_publico(cliente_dados, senha=nova_senha if nova_senha else None, cliente=cliente)
                    endereco_principal = _upsert_endereco_principal_cliente(cliente, cliente_dados)
                    db.session.commit()
                    _salvar_cliente_publico_logado(cliente)
                    _salvar_cliente_site_sessao(_cliente_para_sessao(cliente, endereco_principal))
                    flash('Perfil atualizado com sucesso.', 'success')
                    return redirect(url_for('public.cliente_perfil'))
                except Exception:
                    db.session.rollback()
                    flash('Não foi possível atualizar seu perfil.', 'danger')
        return render_template(
            'cliente/editar_perfil.html',
            cliente=cliente,
            cliente_dados=_cliente_para_sessao(cliente),
            resumo_carrinho=obter_resumo_carrinho_site(cliente),
        )

    @bp.route('/cliente/enderecos', methods=['GET', 'POST'])
    @cliente_login_required
    def cliente_enderecos():
        if not _schema_has_table('clientes_enderecos'):
            flash('Os endereços salvos ainda não estão disponíveis neste banco.', 'warning')
            return redirect(url_for('public.cliente_dashboard'))
        cliente = _obter_cliente_publico_logado()
        if request.method == 'POST':
            endereco_id = request.form.get('endereco_id', type=int)
            dados_endereco, erros = _coletar_dados_endereco_form(request.form)
            if erros:
                for erro in erros:
                    flash(erro, 'warning')
            else:
                try:
                    endereco = None
                    if endereco_id:
                        endereco = ClienteEndereco.query.filter_by(id=endereco_id, cliente_id=cliente.id).first_or_404()
                    _salvar_endereco_cliente(cliente, dados_endereco, endereco=endereco)
                    db.session.commit()
                    _salvar_cliente_site_sessao(_cliente_para_sessao(cliente))
                    flash('Endereço salvo com sucesso.', 'success')
                    return redirect(url_for('public.cliente_enderecos'))
                except Exception:
                    db.session.rollback()
                    flash('Não foi possível salvar o endereço.', 'danger')

        return render_template(
            'cliente/enderecos.html',
            cliente=cliente,
            enderecos=sorted(cliente.enderecos, key=lambda item: (not item.principal, item.id)),
            resumo_carrinho=obter_resumo_carrinho_site(cliente),
        )

    @bp.route('/cliente/enderecos/<int:id>/deletar', methods=['POST'])
    @cliente_login_required
    def cliente_endereco_deletar(id):
        if not _schema_has_table('clientes_enderecos'):
            flash('Os endereços salvos ainda não estão disponíveis neste banco.', 'warning')
            return redirect(url_for('public.cliente_dashboard'))
        cliente = _obter_cliente_publico_logado()
        endereco = ClienteEndereco.query.filter_by(id=id, cliente_id=cliente.id).first_or_404()
        try:
            principal = bool(endereco.principal)
            db.session.delete(endereco)
            db.session.flush()
            if principal and cliente.enderecos:
                cliente.enderecos[0].principal = True
            db.session.commit()
            flash('Endereço removido com sucesso.', 'success')
        except Exception:
            db.session.rollback()
            flash('Não foi possível remover o endereço.', 'danger')
        return redirect(url_for('public.cliente_enderecos'))

    @bp.route('/cliente/favoritos')
    @cliente_login_required
    def cliente_favoritos():
        if not _schema_has_table('clientes_favoritos'):
            flash('Os favoritos ainda não estão disponíveis neste banco.', 'warning')
            return redirect(url_for('public.cliente_dashboard'))
        cliente = _obter_cliente_publico_logado()
        favoritos = ClienteFavorito.query.options(
            selectinload(ClienteFavorito.produto).selectinload(Produto.categoria),
            selectinload(ClienteFavorito.produto).selectinload(Produto.fornecedor),
        ).filter_by(cliente_id=cliente.id).order_by(ClienteFavorito.criado_em.desc()).all()
        return render_template(
            'cliente/favoritos.html',
            cliente=cliente,
            favoritos=favoritos,
            resumo_carrinho=obter_resumo_carrinho_site(cliente),
        )

    @bp.route('/cliente/favoritos/adicionar/<int:produto_id>', methods=['POST'])
    @cliente_login_required
    def cliente_favorito_adicionar(produto_id):
        if not _schema_has_table('clientes_favoritos'):
            flash('Os favoritos ainda não estão disponíveis neste banco.', 'warning')
            return redirect(_destino_interno_seguro(request.form.get('next') or request.referrer) or url_for('index'))
        cliente = _obter_cliente_publico_logado()
        produto = Produto.query.get_or_404(produto_id)
        favorito = ClienteFavorito.query.filter_by(cliente_id=cliente.id, produto_id=produto.id).first()
        if not favorito:
            db.session.add(ClienteFavorito(cliente_id=cliente.id, produto_id=produto.id))
            db.session.commit()
            flash(f'"{produto.nome}" foi adicionado aos favoritos.', 'success')
        else:
            flash(f'"{produto.nome}" já está nos seus favoritos.', 'info')
        return redirect(_destino_interno_seguro(request.form.get('next') or request.referrer) or url_for('public.cliente_favoritos'))

    @bp.route('/cliente/favoritos/remover/<int:produto_id>', methods=['POST'])
    @cliente_login_required
    def cliente_favorito_remover(produto_id):
        if not _schema_has_table('clientes_favoritos'):
            flash('Os favoritos ainda não estão disponíveis neste banco.', 'warning')
            return redirect(_destino_interno_seguro(request.form.get('next') or request.referrer) or url_for('index'))
        cliente = _obter_cliente_publico_logado()
        favorito = ClienteFavorito.query.filter_by(cliente_id=cliente.id, produto_id=produto_id).first()
        if favorito:
            db.session.delete(favorito)
            db.session.commit()
            flash('Produto removido dos favoritos.', 'success')
        else:
            flash('Favorito não encontrado.', 'warning')
        return redirect(_destino_interno_seguro(request.form.get('next') or request.referrer) or url_for('public.cliente_favoritos'))

    @bp.route('/carrinho', methods=['GET'])
    def carrinho_site():
        empresa = _obter_empresa_config()
        if not _ecommerce_site_ativo(empresa):
            return _redirecionar_loja_inativa()
        cliente = _obter_cliente_publico_logado()
        resumo_carrinho = obter_resumo_carrinho_site(cliente)
        ids_no_carrinho = {item['produto'].id for item in resumo_carrinho['itens']}
        query_destaque = Produto.query.filter(
            Produto.ativo.is_(True),
            Produto.filtro_nao_vencidos(),
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
            cliente_publico=cliente,
        )

    @bp.route('/carrinho/cupom', methods=['POST'])
    def aplicar_cupom_carrinho_site():
        if not _ecommerce_site_ativo():
            return _redirecionar_loja_inativa()
        if not _coupons_ready():
            flash('Os cupons avançados ainda não estão disponíveis neste banco.', 'warning')
            return redirect(url_for('public.carrinho_site'))
        cliente = _obter_cliente_publico_logado()
        resumo_carrinho = obter_resumo_carrinho_site(cliente)
        if not resumo_carrinho['itens']:
            flash('Adicione itens ao carrinho antes de aplicar um cupom.', 'warning')
            return redirect(url_for('public.carrinho_site'))

        codigo = (request.form.get('codigo_cupom') or '').strip().upper()
        if not codigo:
            _limpar_cupom_sessao()
            flash('Cupom removido do carrinho.', 'info')
            return redirect(url_for('public.carrinho_site'))

        cupom = _carregar_cupom_por_codigo(codigo)
        valido, mensagem, _ = _cupom_pode_ser_usado(cupom, cliente, resumo_carrinho['itens'], resumo_carrinho['subtotal'])
        if not valido:
            flash(mensagem, 'warning')
        else:
            _salvar_cupom_sessao(cupom)
            flash(f'Cupom "{cupom.codigo}" aplicado com sucesso.', 'success')
        return redirect(url_for('public.carrinho_site'))

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
        cliente_logado = _obter_cliente_publico_logado()
        resumo_carrinho = obter_resumo_carrinho_site(cliente_logado)
        if not resumo_carrinho['itens']:
            flash('Adicione itens ao carrinho antes de finalizar.', 'warning')
            return redirect(url_for('public.carrinho_site'))

        payment_options = load_payment_options(empresa.pagamentos_ecommerce_json, 'ecommerce')
        payment_methods = payment_methods_map(empresa.pagamentos_ecommerce_json, 'ecommerce')
        default_payment = default_payment_id(empresa.pagamentos_ecommerce_json, 'ecommerce') or 'pix'
        cliente_dados = _cliente_para_sessao(cliente_logado) if cliente_logado else _obter_cliente_site_sessao()
        enderecos_salvos = sorted((cliente_logado.enderecos if cliente_logado else []), key=lambda item: (not item.principal, item.id))
        pagamento_selecionado = (request.form.get('metodo_pagamento') or default_payment).strip().lower() if request.method == 'POST' else default_payment
        valor_recebido = (request.form.get('valor_recebido') or '').strip() if request.method == 'POST' else ''

        if request.method == 'POST':
            endereco_id = request.form.get('endereco_id', type=int)
            if cliente_logado and endereco_id:
                endereco_escolhido = ClienteEndereco.query.filter_by(id=endereco_id, cliente_id=cliente_logado.id).first()
                if endereco_escolhido:
                    cliente_dados = _cliente_para_sessao(cliente_logado, endereco_escolhido)
                    cliente_dados['observacoes'] = (request.form.get('observacoes') or cliente_dados.get('observacoes') or '').strip()
                    cliente_dados['recebe_ofertas'] = (request.form.get('recebe_ofertas') == 'on') or cliente_dados.get('recebe_ofertas')
                    erros = []
                else:
                    cliente_dados, erros = _coletar_dados_cliente_form(request.form)
            else:
                cliente_dados, erros = _coletar_dados_cliente_form(request.form)
            if erros:
                for erro in erros:
                    flash(erro, 'warning')
            else:
                try:
                    pagamento = _coletar_pagamento_checkout(request.form, resumo_carrinho['total'], payment_methods)
                    with atomic_transaction(db.session):
                        itens_checkout = []
                        for item in resumo_carrinho['itens']:
                            produto = Produto.query.get(item['produto'].id)
                            qtd_solicitada = item['quantidade']
                            if not produto or not produto.ativo:
                                raise BusinessRuleError(
                                    'Um dos produtos do carrinho nao esta mais disponivel. Atualize a pagina e tente novamente.'
                                )
                            if produto.vencido:
                                raise BusinessRuleError(f'O produto {produto.nome} esta vencido e nao pode ser vendido.')
                            if produto.quantidade_estoque < qtd_solicitada:
                                raise BusinessRuleError(
                                    f'Estoque insuficiente para {produto.nome}. Disponivel: {produto.quantidade_estoque}'
                                )
                            itens_checkout.append((produto, qtd_solicitada))

                        cliente_db = cliente_logado or _upsert_cliente_publico(cliente_dados)
                        if cliente_logado:
                            cliente_db = _upsert_cliente_publico(cliente_dados, cliente=cliente_logado)
                        endereco_principal = _upsert_endereco_principal_cliente(cliente_db, cliente_dados)
                        db.session.flush()

                        pedido = Pedido(
                            cliente_publico_id=cliente_db.id,
                            cliente_nome=cliente_dados.get('nome'),
                            cliente_celular=cliente_dados.get('celular'),
                            status='aberto',
                            origem='site',
                            total=float(resumo_carrinho['total'] or 0.0),
                            metodo_pagamento=pagamento['metodo_label'],
                            valor_pago=pagamento['valor_pago'],
                            estoque_processado=False,
                            financeiro_processado=False,
                        )
                        db.session.add(pedido)
                        db.session.flush()

                        for produto, quantidade in itens_checkout:
                            db.session.add(ItemPedido(
                                pedido_id=pedido.id,
                                produto_id=produto.id,
                                quantidade=quantidade,
                                preco_unitario=produto.preco_venda
                            ))

                        cupom_resumo = resumo_carrinho.get('cupom') or {}
                        cupom = _carregar_cupom_por_codigo(cupom_resumo.get('codigo')) if cupom_resumo else None
                        pedido.observacoes = json.dumps({
                            'cliente_publico_id': cliente_db.id,
                            'cliente_cadastro': cliente_dados,
                            'cliente_endereco_id': endereco_principal.id if endereco_principal else None,
                            'pagamento': {
                                'metodo': pagamento['metodo'],
                                'metodo_label': pagamento['metodo_label'],
                                'troco': pagamento['troco'],
                                'detalhes': pagamento['detalhes'],
                            },
                            'cupom': cupom_resumo,
                            'origem_checkout': 'home_varejo',
                        }, ensure_ascii=False)

                        if cupom and cliente_db:
                            db.session.add(CupomUtilizacao(
                                cupom_id=cupom.id,
                                cliente_id=cliente_db.id,
                                pedido=pedido,
                            ))

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

                    _salvar_cliente_publico_logado(cliente_db)
                    _salvar_cliente_site_sessao(_cliente_para_sessao(cliente_db, endereco_principal))
                    _salvar_carrinho_site({})
                    _limpar_cupom_sessao()
                    token_confirmacao = _gerar_token_confirmacao_pedido(pedido.id)

                    flash(f'Pedido #{pedido.id} recebido com sucesso.', 'success')
                    return redirect(url_for('public.pedido_confirmado_site', pedido_id=pedido.id, token=token_confirmacao))
                except AppError as e:
                    db.session.rollback()
                    flash(str(e), 'warning')
                except ValueError as e:
                    db.session.rollback()
                    flash(str(e), 'warning')
                except Exception:
                    db.session.rollback()
                    flash('Não foi possível concluir seu pedido agora.', 'danger')

        return render_template(
            'public/checkout.html',
            empresa=empresa,
            resumo_carrinho=resumo_carrinho,
            cliente_dados=cliente_dados,
            cliente_publico=cliente_logado,
            enderecos_salvos=enderecos_salvos,
            payment_options=payment_options,
            pagamento_selecionado=pagamento_selecionado,
            valor_recebido=valor_recebido,
        )

    @bp.route('/loja/produtos', methods=['GET'])
    def listar_produtos_site():
        empresa = _obter_empresa_config()
        if not _ecommerce_site_ativo(empresa):
            return _redirecionar_loja_inativa()
        cliente = _obter_cliente_publico_logado()
        page = request.args.get('page', 1, type=int)
        query = _aplicar_filtros_produtos(_base_query_produtos_publicos(), request.args)
        paginacao = query.paginate(page=page, per_page=12, error_out=False)
        categorias = Categoria.query.order_by(Categoria.nome.asc()).all()
        fornecedores = Fornecedor.query.order_by(Fornecedor.nome.asc()).all()
        favoritos_ids = {
            favorito.produto_id for favorito in (cliente.favoritos if cliente else [])
        }
        filtros_atuais = request.args.to_dict(flat=True)
        prev_url = None
        next_url = None
        if paginacao.has_prev:
            filtros_prev = dict(filtros_atuais)
            filtros_prev['page'] = paginacao.prev_num
            prev_url = f"{url_for('public.listar_produtos_site')}?{urlencode(filtros_prev)}"
        if paginacao.has_next:
            filtros_next = dict(filtros_atuais)
            filtros_next['page'] = paginacao.next_num
            next_url = f"{url_for('public.listar_produtos_site')}?{urlencode(filtros_next)}"
        return render_template(
            'public/produtos.html',
            empresa=empresa,
            paginacao=paginacao,
            produtos=paginacao.items,
            categorias=categorias,
            fornecedores=fornecedores,
            favoritos_ids=favoritos_ids,
            prev_url=prev_url,
            next_url=next_url,
            resumo_carrinho=obter_resumo_carrinho_site(cliente),
        )

    @bp.route('/loja/produto/<int:produto_id>', methods=['GET'])
    def produto_detalhe_site(produto_id):
        empresa = _obter_empresa_config()
        if not _ecommerce_site_ativo(empresa):
            return _redirecionar_loja_inativa()
        cliente = _obter_cliente_publico_logado()
        produto_query = Produto.query.options(
            selectinload(Produto.categoria),
            selectinload(Produto.fornecedor),
        )
        if _reviews_ready():
            produto_query = produto_query.options(selectinload(Produto.avaliacoes).selectinload(AvaliacaoProduto.cliente))
        produto = produto_query.filter(
            Produto.id == produto_id,
            Produto.ativo.is_(True),
            Produto.filtro_nao_vencidos(),
            Produto.status_disponibilidade.in_(Produto.STATUS_DISPONIBILIDADE_ONLINE_EQUIVALENTES),
        ).first_or_404()
        avaliacao_cliente = None
        if cliente and _reviews_ready():
            avaliacao_cliente = AvaliacaoProduto.query.filter_by(produto_id=produto.id, cliente_id=cliente.id).first()
        relacionados = Produto.query.options(selectinload(Produto.categoria)).filter(
            Produto.id != produto.id,
            Produto.ativo.is_(True),
            Produto.filtro_nao_vencidos(),
            Produto.categoria_id == produto.categoria_id,
            Produto.status_disponibilidade.in_(Produto.STATUS_DISPONIBILIDADE_ONLINE_EQUIVALENTES),
        ).limit(4).all()
        return render_template(
            'public/produto.html',
            empresa=empresa,
            produto=produto,
            avaliacoes=([item for item in produto.avaliacoes if item.aprovada] if _reviews_ready() else []),
            avaliacao_cliente=avaliacao_cliente,
            cliente_publico=cliente,
            relacionados=relacionados,
            resumo_carrinho=obter_resumo_carrinho_site(cliente),
        )

    @bp.route('/loja/produto/<int:produto_id>/avaliar', methods=['GET', 'POST'])
    @cliente_login_required
    def produto_avaliar_site(produto_id):
        if not _reviews_ready():
            flash('As avaliações ainda não estão disponíveis neste banco.', 'warning')
            return redirect(url_for('public.produto_detalhe_site', produto_id=produto_id))
        cliente = _obter_cliente_publico_logado()
        produto = Produto.query.get_or_404(produto_id)
        if not _cliente_ja_comprou_produto(cliente, produto.id):
            flash('Você só pode avaliar produtos já comprados na sua conta.', 'warning')
            return redirect(url_for('public.produto_detalhe_site', produto_id=produto.id))

        avaliacao = AvaliacaoProduto.query.filter_by(produto_id=produto.id, cliente_id=cliente.id).first()
        if request.method == 'POST':
            nota = request.form.get('nota', type=int)
            titulo = (request.form.get('titulo') or '').strip()
            comentario = (request.form.get('comentario') or '').strip()
            if nota not in {1, 2, 3, 4, 5}:
                flash('Selecione uma nota entre 1 e 5 estrelas.', 'warning')
            else:
                try:
                    if not avaliacao:
                        avaliacao = AvaliacaoProduto(produto_id=produto.id, cliente_id=cliente.id)
                        db.session.add(avaliacao)
                    avaliacao.nota = nota
                    avaliacao.titulo = titulo or None
                    avaliacao.comentario = comentario or None
                    avaliacao.aprovada = True
                    db.session.commit()
                    flash('Sua avaliação foi salva com sucesso.', 'success')
                    return redirect(url_for('public.produto_detalhe_site', produto_id=produto.id))
                except Exception:
                    db.session.rollback()
                    flash('Não foi possível salvar sua avaliação.', 'danger')

        return render_template(
            'cliente/avaliar_produto.html',
            cliente=cliente,
            produto=produto,
            avaliacao=avaliacao,
            resumo_carrinho=obter_resumo_carrinho_site(cliente),
        )

    @bp.route('/loja/produto/<int:produto_id>/avaliacoes', methods=['GET'])
    def produto_avaliacoes_site(produto_id):
        empresa = _obter_empresa_config()
        if not _reviews_ready():
            flash('As avaliações ainda não estão disponíveis neste banco.', 'warning')
            return redirect(url_for('public.produto_detalhe_site', produto_id=produto_id))
        produto = Produto.query.options(
            selectinload(Produto.avaliacoes).selectinload(AvaliacaoProduto.cliente)
        ).get_or_404(produto_id)
        return render_template(
            'public/produto_avaliacoes.html',
            empresa=empresa,
            produto=produto,
            avaliacoes=[item for item in produto.avaliacoes if item.aprovada],
            resumo_carrinho=obter_resumo_carrinho_site(_obter_cliente_publico_logado()),
        )

    @bp.route('/cliente/avaliacoes')
    @cliente_login_required
    def cliente_avaliacoes():
        if not _reviews_ready():
            flash('As avaliações ainda não estão disponíveis neste banco.', 'warning')
            return redirect(url_for('public.cliente_dashboard'))
        cliente = _obter_cliente_publico_logado()
        avaliacoes = AvaliacaoProduto.query.options(
            selectinload(AvaliacaoProduto.produto)
        ).filter_by(cliente_id=cliente.id).order_by(AvaliacaoProduto.criado_em.desc()).all()
        return render_template(
            'cliente/avaliacoes.html',
            cliente=cliente,
            avaliacoes=avaliacoes,
            resumo_carrinho=obter_resumo_carrinho_site(cliente),
        )

    @bp.route('/cliente/avaliacoes/<int:id>/remover', methods=['POST'])
    @cliente_login_required
    def cliente_avaliacao_remover(id):
        if not _reviews_ready():
            flash('As avaliações ainda não estão disponíveis neste banco.', 'warning')
            return redirect(url_for('public.cliente_dashboard'))
        cliente = _obter_cliente_publico_logado()
        avaliacao = AvaliacaoProduto.query.filter_by(id=id, cliente_id=cliente.id).first_or_404()
        try:
            db.session.delete(avaliacao)
            db.session.commit()
            flash('Avaliação removida com sucesso.', 'success')
        except Exception:
            db.session.rollback()
            flash('Não foi possível remover a avaliação.', 'danger')
        return redirect(url_for('public.cliente_avaliacoes'))

    @bp.route('/pedido/<int:pedido_id>/confirmado', methods=['GET'])
    def pedido_confirmado_site(pedido_id):
        empresa = _obter_empresa_config()
        if not _ecommerce_site_ativo(empresa):
            return _redirecionar_loja_inativa()
        cliente = _obter_cliente_publico_logado()
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
            cliente_publico=cliente,
            resumo_carrinho=obter_resumo_carrinho_site(cliente),
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
