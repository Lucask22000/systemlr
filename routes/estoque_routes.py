from datetime import datetime, timedelta
import os
import re
import unicodedata
import uuid

from sqlalchemy.orm import load_only, selectinload
from app import extensions

from flask import render_template, request, redirect, url_for, flash, jsonify, session

from app.exceptions import AppError, ValidationError
from app.utils.helpers import sem_acentos
from app.utils.validators import normalizar_codigo_barras
from models import (
    AlmoxarifadoAtribuicao,
    db,
    Categoria,
    EnderecoEstoque,
    Estoque,
    Produto,
    Movimentacao,
    Fornecedor,
    RecebimentoFornecedor,
    RecebimentoItem,
    EmpresaConfig,
    Funcionario,
    Pedido,
    ItemPedido,
    EquipamentoMovimentacao,
    ManutencaoEquipamento,
)
from utils.endereco_codigo import (
    CONTROLE_VALIDADE_VALIDOS,
    RESTRICOES_VALIDAS,
    SETORES_ZONA_VALIDOS,
    STATUS_ENDERECO_VALIDOS,
    TEMPERATURA_VALIDOS,
    TIPOS_AREA_VALIDOS,
    gerar_codigo_localizacao_supermercado,
    validar_endereco_supermercado_payload,
)

# pillow serÃ¡ usado para redimensionar/comprimir imagens
from PIL import Image

ALLOWED_IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp', '.gif'}
DEFAULT_PRODUCT_IMAGE = 'img/placeholders/imgindisponivel.png'


def register_estoque_routes(app, login_required, require_role, aplicar_movimentacao_estoque, sincronizar_matriculas_funcionarios=None):
    estoque_write_roles = ('admin', 'gerente', 'caixa', 'operador')
    endereco_context = {
        'setores_zona_validos': SETORES_ZONA_VALIDOS,
        'tipos_area_validos': TIPOS_AREA_VALIDOS,
        'status_endereco_validos': STATUS_ENDERECO_VALIDOS,
        'controle_validade_validos': CONTROLE_VALIDADE_VALIDOS,
        'temperatura_validos': TEMPERATURA_VALIDOS,
        'restricoes_validas': RESTRICOES_VALIDAS,
    }
    STATUS_DISPONIBILIDADE_LABELS = {
        Produto.STATUS_DISPONIVEL_ONLINE: 'Online',
        Produto.STATUS_DISPONIVEL_OFF: 'Off',
    }
    TIPOS_MOVIMENTACAO_PRODUTO = {
        'manual': 'Manual',
        'carrinho': 'Carrinho',
        'paleteira': 'Paleteira',
        'empilhadeira': 'Empilhadeira',
    }
    recebimento_status_labels = {
        RecebimentoFornecedor.STATUS_CRIADO: 'Criado',
        RecebimentoFornecedor.STATUS_AGUARDANDO_ARMAZENAGEM: 'Aguardando armazenagem',
        RecebimentoFornecedor.STATUS_CONCLUIDO: 'Concluido',
        RecebimentoFornecedor.STATUS_CANCELADO: 'Cancelado',
    }
    recebimento_tipo_labels = {
        RecebimentoFornecedor.TIPO_COMPRA_REVENDA: 'Compra para revenda',
        RecebimentoFornecedor.TIPO_USO_CONSUMO: 'Uso e consumo operacional',
        RecebimentoFornecedor.TIPO_BONIFICACAO: 'Bonificacao do fornecedor',
        RecebimentoFornecedor.TIPO_CONSIGNADO: 'Consignado',
        RecebimentoFornecedor.TIPO_RETORNO_INDUSTRIALIZACAO: 'Retorno de industrializacao',
    }
    recebimento_tipos_fornecedor_opcional = {
        RecebimentoFornecedor.TIPO_USO_CONSUMO,
    }
    almoxarifado_destino_labels = {
        AlmoxarifadoAtribuicao.DESTINO_FUNCIONARIO: 'Funcionario',
        AlmoxarifadoAtribuicao.DESTINO_SETOR: 'Setor',
    }
    motivos_movimentacao_interna = [
        'ajuste_inventario',
        'acerto_estoque',
        'consumo_operacional',
        'perda_validade',
        'avaria_quebra',
        'devolucao_cliente',
        'demonstracao_deguste',
        'uso_interno',
    ]
    motivos_transferencia = [
        'reposicao_loja',
        'abastecimento_filial',
        'transferencia_centro_distribuicao',
        'remanejamento_operacional',
    ]
    fornecedor_padrao_recebimento_nome = 'Origem interna / fornecedor nao informado'

    def _normalizar_status_disponibilidade(valor):
        return Produto.normalizar_status_disponibilidade(valor)

    def _normalizar_tipo_movimentacao(valor):
        tipo = (valor or 'manual').strip().lower()
        if tipo not in TIPOS_MOVIMENTACAO_PRODUTO:
            return 'manual'
        return tipo

    def _obter_empresa_config_estoque():
        empresa = EmpresaConfig.query.first()
        if not empresa:
            empresa = EmpresaConfig()
            db.session.add(empresa)
            db.session.commit()
        return empresa

    def _reposicao_loja_fisica_ativa(empresa=None):
        empresa = empresa or _obter_empresa_config_estoque()
        return empresa.reposicao_loja_fisica_ativa is not False

    def _emissao_etiqueta_loja_ativa(empresa=None):
        empresa = empresa or _obter_empresa_config_estoque()
        return empresa.emissao_etiqueta_loja_ativa is not False

    def _emissao_etiqueta_endereco_ativa(empresa=None):
        empresa = empresa or _obter_empresa_config_estoque()
        return empresa.emissao_etiqueta_endereco_ativa is not False

    def _normalizar_codigo_barras(valor):
        return normalizar_codigo_barras(valor)

    def _sem_acentos(texto):
        return sem_acentos(texto)

    def _categoria_parece_quimico(produto):
        categoria_nome = ''
        if getattr(produto, 'categoria', None):
            categoria_nome = produto.categoria.nome or ''
        texto = _sem_acentos(categoria_nome).strip().lower()
        return bool(texto and re.search(r'quim', texto))

    def _parse_data_filtro(valor):
        texto = (valor or '').strip()
        if not texto:
            return None
        try:
            return datetime.strptime(texto, '%Y-%m-%d')
        except ValueError:
            return None

    def _tipo_recebimento_exige_fornecedor(tipo_recebimento):
        tipo_normalizado = (tipo_recebimento or '').strip().lower()
        return (
            tipo_normalizado in RecebimentoFornecedor.TIPOS_VALIDOS
            and tipo_normalizado not in recebimento_tipos_fornecedor_opcional
        )

    def _obter_fornecedor_padrao_recebimento():
        fornecedor = Fornecedor.query.filter(
            db.func.lower(Fornecedor.nome) == fornecedor_padrao_recebimento_nome.lower()
        ).first()
        if fornecedor:
            return fornecedor
        fornecedor = Fornecedor(
            nome=fornecedor_padrao_recebimento_nome,
            contato='Cadastro automatico',
            observacoes_gerais='Usado quando o tipo de recebimento nao exige fornecedor informado.',
            tipo_produtos_fornece='Origem interna e consumo operacional',
            ativo=True,
        )
        db.session.add(fornecedor)
        db.session.flush()
        return fornecedor

    def _resolver_funcionario_por_matricula_ou_nome(texto_busca='', funcionario_id=None):
        if funcionario_id:
            funcionario = Funcionario.query.filter_by(id=funcionario_id, ativo=True).first()
            if funcionario:
                return funcionario

        texto = (texto_busca or '').strip()
        if not texto:
            return None

        matricula = texto.upper()
        funcionario = Funcionario.query.filter(
            Funcionario.ativo.is_(True),
            db.func.lower(Funcionario.matricula) == matricula.lower(),
        ).first()
        if funcionario:
            return funcionario

        return Funcionario.query.filter(
            Funcionario.ativo.is_(True),
            db.func.lower(Funcionario.nome) == texto.lower(),
        ).order_by(Funcionario.nome.asc()).first()

    def _listar_setores_almoxarifado():
        departamentos = {
            (nome or '').strip()
            for nome, in db.session.query(Funcionario.departamento).filter(Funcionario.departamento.isnot(None)).all()
            if (nome or '').strip()
        }
        times = {
            (nome or '').strip()
            for nome, in db.session.query(Funcionario.time_nome).filter(Funcionario.time_nome.isnot(None)).all()
            if (nome or '').strip()
        }
        return sorted(departamentos.union(times))

    def _aplicar_filtros_produtos(
        query,
        *,
        categoria_id=None,
        busca='',
        status_disponibilidade='',
        estoque_id=None,
        endereco_id=None,
        fornecedor_id=None,
        fora_picking='',
        status_ativo='',
        ruptura='',
    ):
        if categoria_id:
            query = query.filter(Produto.categoria_id == categoria_id)
        if busca:
            termo = f'%{busca}%'
            query = query.filter(
                db.or_(
                    Produto.nome.ilike(termo),
                    Produto.codigo.ilike(termo),
                    Produto.descricao.ilike(termo),
                )
            )
        ativo = (status_ativo or '').strip().lower()
        if ativo == 'ativos':
            query = query.filter(Produto.ativo.is_(True))
        elif ativo == 'inativos':
            query = query.filter(Produto.ativo.is_(False))
        status = (status_disponibilidade or '').strip().lower()
        if status in Produto.STATUS_DISPONIBILIDADE_ONLINE_EQUIVALENTES:
            query = query.filter(Produto.status_disponibilidade.in_(Produto.STATUS_DISPONIBILIDADE_ONLINE_EQUIVALENTES))
        elif status in Produto.STATUS_DISPONIBILIDADE_OFF_EQUIVALENTES:
            query = query.filter(Produto.status_disponibilidade.in_(Produto.STATUS_DISPONIBILIDADE_OFF_EQUIVALENTES))
        if endereco_id:
            query = query.filter(Produto.endereco_id == endereco_id)
        if fornecedor_id:
            query = query.filter(Produto.fornecedor_id == fornecedor_id)
        fora = (fora_picking or '').strip().lower()
        if fora == 'sim':
            query = query.filter(Produto.fora_picking.is_(True))
        elif fora == 'nao':
            query = query.filter(db.or_(Produto.fora_picking.is_(False), Produto.fora_picking.is_(None)))
        ruptura = (ruptura or '').strip().lower()
        if ruptura == 'sim':
            query = query.filter(Produto.quantidade_estoque < Produto.quantidade_minima)
        elif ruptura == 'nao':
            query = query.filter(Produto.quantidade_estoque >= Produto.quantidade_minima)
        if estoque_id:
            query = query.join(EnderecoEstoque, Produto.endereco_id == EnderecoEstoque.id).filter(
                EnderecoEstoque.estoque_id == estoque_id
            )
        return query

    def _funcionario_logado_estoque():
        funcionario_id = session.get('funcionario_id')
        if not funcionario_id:
            return None
        return Funcionario.query.get(funcionario_id)

    def _estoques_permitidos_ids_base(funcionario=None):
        funcionario = funcionario or _funcionario_logado_estoque()
        if not funcionario or funcionario.role == 'admin' or not getattr(funcionario, 'restricao_estoques_ativa', False):
            return None
        ids = set()
        if getattr(funcionario, 'estoque_principal_id', None):
            ids.add(funcionario.estoque_principal_id)
        for estoque in getattr(funcionario, 'estoques_permitidos', []) or []:
            if getattr(estoque, 'id', None):
                ids.add(estoque.id)
        return ids

    def _estoque_contexto_selecionado_id(funcionario=None):
        funcionario = funcionario or _funcionario_logado_estoque()
        valor = session.get('estoque_contexto_id')
        if valor in (None, '', 'all'):
            return None
        try:
            estoque_id = int(valor)
        except (TypeError, ValueError):
            session.pop('estoque_contexto_id', None)
            return None

        ids_base = _estoques_permitidos_ids_base(funcionario)
        query = Estoque.query.filter(Estoque.id == estoque_id, Estoque.ativo.is_(True))
        if ids_base is not None:
            if estoque_id not in ids_base:
                session.pop('estoque_contexto_id', None)
                return None
            query = query.filter(Estoque.id.in_(ids_base))
        if not query.with_entities(Estoque.id).first():
            session.pop('estoque_contexto_id', None)
            return None
        return estoque_id

    def _estoques_permitidos_ids(funcionario=None):
        funcionario = funcionario or _funcionario_logado_estoque()
        ids_base = _estoques_permitidos_ids_base(funcionario)
        estoque_contexto_id = _estoque_contexto_selecionado_id(funcionario)
        if estoque_contexto_id:
            return {estoque_contexto_id}
        return ids_base

    def _estoque_query_permitida(funcionario=None):
        query = Estoque.query
        ids = _estoques_permitidos_ids(funcionario)
        if ids is None:
            return query
        if not ids:
            return query.filter(Estoque.id == -1)
        return query.filter(Estoque.id.in_(ids))

    def _endereco_query_permitida(funcionario=None):
        query = EnderecoEstoque.query
        ids = _estoques_permitidos_ids(funcionario)
        if ids is None:
            return query
        if not ids:
            return query.filter(EnderecoEstoque.id == -1)
        return query.filter(EnderecoEstoque.estoque_id.in_(ids))

    def _produto_query_permitida(query, funcionario=None):
        ids = _estoques_permitidos_ids(funcionario)
        if ids is None:
            return query
        if not ids:
            return query.filter(Produto.endereco_id.is_(None))
        return query.filter(
            db.or_(
                Produto.endereco_id.is_(None),
                Produto.endereco.has(EnderecoEstoque.estoque_id.in_(ids)),
            )
        )

    def _movimentacao_query_permitida(query, funcionario=None):
        ids = _estoques_permitidos_ids(funcionario)
        if ids is None:
            return query
        if not ids:
            return query.filter(Movimentacao.id == -1)
        return query.filter(
            Movimentacao.produto.has(
                db.or_(
                    Produto.endereco_id.is_(None),
                    Produto.endereco.has(EnderecoEstoque.estoque_id.in_(ids)),
                )
            )
        )

    def _carregar_estoque_permitido(estoque_id, funcionario=None, *, apenas_ativo=False):
        if not estoque_id:
            return None
        query = _estoque_query_permitida(funcionario)
        if apenas_ativo:
            query = query.filter(Estoque.ativo.is_(True))
        return query.filter(Estoque.id == estoque_id).first()

    def _carregar_endereco_permitido(endereco_id, funcionario=None, *, apenas_ativo=False):
        if not endereco_id:
            return None
        query = _endereco_query_permitida(funcionario)
        if apenas_ativo:
            query = query.filter(EnderecoEstoque.ativo.is_(True))
        return query.filter(EnderecoEstoque.id == endereco_id).first()

    def _produto_em_estoque_permitido(produto, funcionario=None):
        ids = _estoques_permitidos_ids(funcionario)
        if ids is None or not produto:
            return True
        if not getattr(produto, 'endereco_id', None):
            return True
        endereco = getattr(produto, 'endereco', None) or EnderecoEstoque.query.get(produto.endereco_id)
        return bool(endereco and endereco.estoque_id in ids)
    def _is_allowed_image(filename):
        _, ext = os.path.splitext(filename.lower())
        return ext in ALLOWED_IMAGE_EXTENSIONS

    def _is_valid_image_content(file_storage):
        if not file_storage:
            return False
        stream = getattr(file_storage, 'stream', None)
        if stream is None:
            return False
        try:
            stream.seek(0)
            img = Image.open(stream)
            img.verify()
            stream.seek(0)
            return True
        except Exception:
            try:
                stream.seek(0)
            except Exception:
                pass
            return False

    def _optimize_image_file(absolute_path):
        try:
            img = Image.open(absolute_path)
            max_size = (800, 800)
            resample = getattr(Image, 'Resampling', Image).LANCZOS
            img.thumbnail(max_size, resample)
            save_kwargs = {'optimize': True}
            if img.format and img.format.lower() in ['jpeg', 'jpg']:
                save_kwargs['quality'] = 85
            img.save(absolute_path, **save_kwargs)
        except Exception:
            pass

    def _delete_image_file(relative_path):
        if not relative_path:
            return
        caminho_rel = str(relative_path).replace('\\', '/')
        if caminho_rel == DEFAULT_PRODUCT_IMAGE:
            return
        caminho_padrao_config = None
        try:
            empresa_cfg = EmpresaConfig.query.first()
            caminho_padrao_config = (empresa_cfg.ecom_produto_placeholder_path or '').strip().replace('\\', '/') if empresa_cfg else ''
        except Exception:
            caminho_padrao_config = None
        if caminho_padrao_config and caminho_rel == caminho_padrao_config:
            return

        image_path = os.path.normpath(os.path.join(app.static_folder, relative_path))
        static_root = os.path.normpath(app.static_folder)
        if os.path.commonpath([image_path, static_root]) != static_root:
            return

        if os.path.exists(image_path):
            os.remove(image_path)

    def _save_product_image(file_storage, product_name):
        if not file_storage or not file_storage.filename:
            return None, None
        if not _is_allowed_image(file_storage.filename):
            return None, 'Formato de imagem invalido. Use PNG, JPG, JPEG, WEBP ou GIF.'
        if not _is_valid_image_content(file_storage):
            return None, 'Arquivo enviado nao corresponde a uma imagem valida.'

        _, ext = os.path.splitext(file_storage.filename.lower())
        image_name = f'{uuid.uuid4().hex}{ext}'
        relative_dir = os.path.join('uploads', 'produtos')
        absolute_dir = os.path.join(app.static_folder, relative_dir)
        os.makedirs(absolute_dir, exist_ok=True)
        relative_path = os.path.join(relative_dir, image_name).replace('\\', '/')
        absolute_path = os.path.join(app.static_folder, relative_path)

        file_storage.save(absolute_path)
        _optimize_image_file(absolute_path)
        return relative_path, None

    def _imagem_padrao_produto():
        try:
            empresa_cfg = EmpresaConfig.query.first()
            caminho_cfg = (empresa_cfg.ecom_produto_placeholder_path or '').strip().replace('\\', '/') if empresa_cfg else ''
            if caminho_cfg:
                return caminho_cfg
        except Exception:
            pass
        return DEFAULT_PRODUCT_IMAGE

    def _normalizar_imagem_produto(path):
        texto = (path or '').strip().replace('\\', '/')
        return texto or _imagem_padrao_produto()

    def _preencher_imagem_padrao_produtos():
        try:
            atualizados = Produto.query.filter(
                db.or_(Produto.imagem_path.is_(None), Produto.imagem_path == '')
            ).update(
                {Produto.imagem_path: _imagem_padrao_produto()},
                synchronize_session=False
            )
            if atualizados:
                db.session.commit()
        except Exception:
            db.session.rollback()

    def _save_category_image(file_storage, category_name):
        if not file_storage or not file_storage.filename:
            return None, None
        if not _is_allowed_image(file_storage.filename):
            return None, 'Formato de imagem invalido. Use PNG, JPG, JPEG, WEBP ou GIF.'
        if not _is_valid_image_content(file_storage):
            return None, 'Arquivo enviado nao corresponde a uma imagem valida.'

        _, ext = os.path.splitext(file_storage.filename.lower())
        image_name = f'{uuid.uuid4().hex}{ext}'
        relative_dir = os.path.join('uploads', 'categorias')
        absolute_dir = os.path.join(app.static_folder, relative_dir)
        os.makedirs(absolute_dir, exist_ok=True)
        relative_path = os.path.join(relative_dir, image_name).replace('\\', '/')
        absolute_path = os.path.join(app.static_folder, relative_path)

        file_storage.save(absolute_path)
        _optimize_image_file(absolute_path)
        return relative_path, None

    with app.app_context():
        _preencher_imagem_padrao_produtos()

    @app.route('/produtos')
    @login_required
    def listar_produtos():
        funcionario_logado = _funcionario_logado_estoque()
        page = max(request.args.get('page', 1, type=int), 1)
        per_page = min(max(request.args.get('per_page', 25, type=int), 1), 100)
        categoria_id = request.args.get('categoria_id', type=int)
        busca = (request.args.get('busca') or '').strip()
        status_disponibilidade = (request.args.get('status_disponibilidade') or '').strip().lower()
        estoque_id = request.args.get('estoque_id', type=int)
        endereco_id = request.args.get('endereco_id', type=int)
        fornecedor_id = request.args.get('fornecedor_id', type=int)
        fora_picking = (request.args.get('fora_picking') or '').strip().lower()
        status_ativo = (request.args.get('status_ativo') or '').strip().lower()
        ruptura = (request.args.get('ruptura') or '').strip().lower()
        ordenar = (request.args.get('ordenar') or 'nome_asc').strip().lower()

        ordenacoes_produto = {
            'nome_asc': (Produto.nome.asc(), Produto.id.asc()),
            'nome_desc': (Produto.nome.desc(), Produto.id.desc()),
            'codigo_asc': (Produto.codigo.asc(), Produto.id.asc()),
            'estoque_menor': (Produto.quantidade_estoque.asc(), Produto.nome.asc()),
            'estoque_maior': (Produto.quantidade_estoque.desc(), Produto.nome.asc()),
            'recentes': (Produto.criado_em.desc(), Produto.id.desc()),
            'atualizados': (Produto.atualizado_em.desc(), Produto.id.desc()),
        }
        if ordenar not in ordenacoes_produto:
            ordenar = 'nome_asc'

        if estoque_id and not _carregar_estoque_permitido(estoque_id, funcionario_logado):
            flash('Você não possui acesso ao estoque selecionado.', 'warning')
            return redirect(url_for('listar_produtos'))
        if endereco_id and not _carregar_endereco_permitido(endereco_id, funcionario_logado):
            flash('Você não possui acesso ao endereço selecionado.', 'warning')
            return redirect(url_for('listar_produtos'))

        query = _aplicar_filtros_produtos(
            _produto_query_permitida(Produto.query, funcionario_logado),
            categoria_id=categoria_id,
            busca=busca,
            status_disponibilidade=status_disponibilidade,
            estoque_id=estoque_id,
            endereco_id=endereco_id,
            fornecedor_id=fornecedor_id,
            fora_picking=fora_picking,
            status_ativo=status_ativo,
            ruptura=ruptura,
        ).options(
            load_only(
                Produto.id,
                Produto.codigo,
                Produto.nome,
                Produto.imagem_path,
                Produto.categoria_id,
                Produto.fornecedor_id,
                Produto.endereco_id,
                Produto.preco_venda,
                Produto.quantidade_estoque,
                Produto.quantidade_minima,
                Produto.status_disponibilidade,
                Produto.tipo_movimentacao,
                Produto.fora_picking,
                Produto.ativo,
                Produto.criado_em,
                Produto.atualizado_em,
            ),
            selectinload(Produto.categoria).load_only(Categoria.id, Categoria.nome),
            selectinload(Produto.endereco).load_only(EnderecoEstoque.id, EnderecoEstoque.nome),
            selectinload(Produto.fornecedor).load_only(Fornecedor.id, Fornecedor.nome),
        )

        pagination = query.order_by(*ordenacoes_produto[ordenar]).paginate(page=page, per_page=per_page, error_out=False)
        produtos = pagination.items
        categorias = Categoria.query.order_by(Categoria.nome.asc()).all()
        estoques = _estoque_query_permitida(funcionario_logado).filter_by(ativo=True).order_by(Estoque.nome.asc()).all()
        if estoque_id:
            enderecos = _endereco_query_permitida(funcionario_logado).filter_by(
                ativo=True,
                estoque_id=estoque_id,
            ).order_by(EnderecoEstoque.nome.asc()).all()
        else:
            enderecos = []
        fornecedores = Fornecedor.query.filter(
            Fornecedor.ativo.is_(True),
            db.func.lower(Fornecedor.nome) != fornecedor_padrao_recebimento_nome.lower(),
        ).order_by(Fornecedor.nome.asc()).all()
        filtros_labels = []
        if busca:
            filtros_labels.append(f'Busca: {busca}')
        categoria_obj = next((cat for cat in categorias if cat.id == categoria_id), None)
        if categoria_obj:
            filtros_labels.append(f'Categoria: {categoria_obj.nome}')
        estoque_obj = next((estoque for estoque in estoques if estoque.id == estoque_id), None)
        if estoque_obj:
            filtros_labels.append(f'Estoque: {estoque_obj.nome}')
        endereco_obj = next((endereco for endereco in enderecos if endereco.id == endereco_id), None)
        if endereco_obj:
            filtros_labels.append(f'Endereco: {endereco_obj.nome}')
        fornecedor_obj = next((fornecedor for fornecedor in fornecedores if fornecedor.id == fornecedor_id), None)
        if fornecedor_obj:
            filtros_labels.append(f'Fornecedor: {fornecedor_obj.nome}')
        if status_disponibilidade:
            filtros_labels.append(f'Disponibilidade: {STATUS_DISPONIBILIDADE_LABELS.get(status_disponibilidade, status_disponibilidade)}')
        if status_ativo == 'ativos':
            filtros_labels.append('Somente ativos')
        elif status_ativo == 'inativos':
            filtros_labels.append('Somente inativos')
        if fora_picking == 'sim':
            filtros_labels.append('Fora de picking')
        elif fora_picking == 'nao':
            filtros_labels.append('Em picking')
        if ruptura == 'sim':
            filtros_labels.append('Somente ruptura')
        elif ruptura == 'nao':
            filtros_labels.append('Sem ruptura')

        total_resultados = pagination.total
        inicio_resultados = ((page - 1) * per_page) + 1 if total_resultados else 0
        fim_resultados = inicio_resultados + len(produtos) - 1 if total_resultados else 0
        return render_template(
            'estoque/produtos/produtos.html',
            produtos=produtos,
            pagination=pagination,
            per_page=per_page,
            per_page_options=(25, 50, 100),
            categorias=categorias,
            enderecos=enderecos,
            estoques=estoques,
            fornecedores=fornecedores,
            categoria_selecionada=categoria_id,
            busca=busca,
            filtros_labels=filtros_labels,
            ordenar=ordenar,
            ordenacoes_disponiveis={
                'nome_asc': 'Nome A-Z',
                'nome_desc': 'Nome Z-A',
                'codigo_asc': 'Codigo',
                'estoque_menor': 'Menor estoque',
                'estoque_maior': 'Maior estoque',
                'recentes': 'Mais recentes',
                'atualizados': 'Atualizados por ultimo',
            },
            resumo_lista={
                'total_resultados': total_resultados,
                'inicio_resultados': inicio_resultados,
                'fim_resultados': fim_resultados,
                'pagina_atual': pagination.page,
                'total_paginas': pagination.pages,
                'filtros_ativos': len(filtros_labels),
            },
            filtros={
                'status_disponibilidade': status_disponibilidade,
                'estoque_id': estoque_id,
                'endereco_id': endereco_id,
                'fornecedor_id': fornecedor_id,
                'fora_picking': fora_picking,
                'status_ativo': status_ativo,
                'ruptura': ruptura,
            },
            status_disponibilidade_labels=STATUS_DISPONIBILIDADE_LABELS,
            tipos_movimentacao_produto=TIPOS_MOVIMENTACAO_PRODUTO,
            query_params=request.args.to_dict()
        )

    @app.route('/produtos/etiquetas-loja')
    @login_required
    def imprimir_etiquetas_loja():
        empresa = _obter_empresa_config_estoque()
        if not _emissao_etiqueta_loja_ativa(empresa):
            flash('A emissao de etiquetas de loja esta desativada na configuracao da empresa.', 'warning')
            return redirect(url_for('listar_produtos'))

        funcionario_logado = _funcionario_logado_estoque()
        categoria_id = request.args.get('categoria_id', type=int)
        estoque_id = request.args.get('estoque_id', type=int)
        somente_em_venda = (request.args.get('somente_em_venda') or 'sim').strip().lower()
        busca = (request.args.get('busca') or '').strip()

        if estoque_id and not _carregar_estoque_permitido(estoque_id, funcionario_logado):
            flash('Voce nao possui acesso ao estoque selecionado para etiquetas de loja.', 'warning')
            return redirect(url_for('listar_produtos'))

        query = _produto_query_permitida(
            Produto.query.options(
                selectinload(Produto.categoria),
                selectinload(Produto.endereco),
            ),
            funcionario_logado,
        ).filter(Produto.ativo.is_(True))

        if categoria_id:
            query = query.filter(Produto.categoria_id == categoria_id)
        if estoque_id:
            query = query.filter(Produto.estoque_id == estoque_id)
        if somente_em_venda == 'sim':
            query = query.filter(Produto.quantidade_estoque > 0)
        if busca:
            termo = f'%{busca}%'
            query = query.filter(
                db.or_(
                    Produto.nome.ilike(termo),
                    Produto.codigo.ilike(termo),
                    Produto.descricao.ilike(termo),
                )
            )

        produtos = query.order_by(Produto.nome.asc()).limit(180).all()
        categorias = Categoria.query.order_by(Categoria.nome.asc()).all()
        estoques = _estoque_query_permitida(funcionario_logado).order_by(Estoque.nome.asc()).all()

        return render_template(
            'estoque/produtos/etiquetas_loja.html',
            empresa=empresa,
            produtos=produtos,
            categorias=categorias,
            estoques=estoques,
            filtros={
                'categoria_id': categoria_id,
                'estoque_id': estoque_id,
                'somente_em_venda': somente_em_venda,
                'busca': busca,
            },
        )

    @app.route('/produtos/enderecos/armazenar-todos', methods=['POST'])
    @require_role(*estoque_write_roles)
    def armazenar_todos_produtos_enderecos():
        funcionario_logado = _funcionario_logado_estoque()
        try:
            estoque_id = request.form.get('estoque_id', type=int)
            apenas_sem_endereco = (request.form.get('apenas_sem_endereco') == 'on')
            categoria_id = request.form.get('categoria_id', type=int)
            busca = (request.form.get('busca') or '').strip()
            status_disponibilidade = (request.form.get('status_disponibilidade') or '').strip().lower()
            filtro_estoque_id = request.form.get('filtro_estoque_id', type=int)
            filtro_endereco_id = request.form.get('filtro_endereco_id', type=int)

            if not estoque_id:
                flash('Selecione um estoque para distribuir os produtos.', 'error')
                return redirect(url_for(
                    'listar_produtos',
                    categoria_id=categoria_id or '',
                    busca=busca,
                    status_disponibilidade=status_disponibilidade,
                    estoque_id=filtro_estoque_id or '',
                    endereco_id=filtro_endereco_id or '',
                ))

            estoque = _carregar_estoque_permitido(estoque_id, funcionario_logado)
            if not estoque:
                flash('Estoque informado nao existe ou nao esta liberado para este colaborador.', 'error')
                return redirect(url_for(
                    'listar_produtos',
                    categoria_id=categoria_id or '',
                    busca=busca,
                    status_disponibilidade=status_disponibilidade,
                    estoque_id=filtro_estoque_id or '',
                    endereco_id=filtro_endereco_id or '',
                ))

            if filtro_estoque_id and not _carregar_estoque_permitido(filtro_estoque_id, funcionario_logado):
                flash('Filtro de estoque fora da sua alçada.', 'error')
                return redirect(url_for('listar_produtos'))
            if filtro_endereco_id and not _carregar_endereco_permitido(filtro_endereco_id, funcionario_logado):
                flash('Filtro de endereço fora da sua alçada.', 'error')
                return redirect(url_for('listar_produtos'))

            enderecos = _endereco_query_permitida(funcionario_logado).filter_by(
                estoque_id=estoque.id,
                ativo=True
            ).order_by(EnderecoEstoque.id.asc()).all()
            if not enderecos:
                flash('Este estoque nao possui enderecos ativos para armazenamento.', 'warning')
                return redirect(url_for(
                    'listar_produtos',
                    categoria_id=categoria_id or '',
                    busca=busca,
                    status_disponibilidade=status_disponibilidade,
                    estoque_id=filtro_estoque_id or '',
                    endereco_id=filtro_endereco_id or '',
                ))

            query = _aplicar_filtros_produtos(
                _produto_query_permitida(Produto.query.order_by(Produto.id.asc()), funcionario_logado),
                categoria_id=categoria_id,
                busca=busca,
                status_disponibilidade=status_disponibilidade,
                estoque_id=filtro_estoque_id,
                endereco_id=filtro_endereco_id,
            )
            if apenas_sem_endereco:
                query = query.filter(Produto.endereco_id.is_(None))

            produtos = query.all()
            if not produtos:
                flash('Nenhum produto encontrado para armazenar com os filtros selecionados.', 'warning')
                return redirect(url_for(
                    'listar_produtos',
                    categoria_id=categoria_id or '',
                    busca=busca,
                    status_disponibilidade=status_disponibilidade,
                    estoque_id=filtro_estoque_id or '',
                    endereco_id=filtro_endereco_id or '',
                ))

            total_enderecos = len(enderecos)
            for idx, produto in enumerate(produtos):
                destino = enderecos[idx % total_enderecos]
                produto.endereco_id = destino.id

            db.session.commit()
            msg_regra = 'sem endereco' if apenas_sem_endereco else 'filtrados'
            flash(
                f'{len(produtos)} produto(s) armazenado(s) em {total_enderecos} endereco(s) do estoque "{estoque.nome}" (criterio: {msg_regra}).',
                'success'
            )
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao armazenar produtos nos enderecos: {str(e)}', 'error')

        return redirect(url_for(
            'listar_produtos',
            categoria_id=request.form.get('categoria_id') or '',
            busca=(request.form.get('busca') or '').strip(),
            status_disponibilidade=(request.form.get('status_disponibilidade') or '').strip().lower(),
            estoque_id=request.form.get('filtro_estoque_id') or '',
            endereco_id=request.form.get('filtro_endereco_id') or '',
        ))

    @app.route('/produtos/novo', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def novo_produto():
        funcionario_logado = _funcionario_logado_estoque()
        if request.method == 'POST':
            nova_imagem_path = None
            try:
                categoria_id = request.form.get('categoria_id', type=int)
                fornecedor_id = request.form.get('fornecedor_id', type=int)
                categoria = Categoria.query.get(categoria_id)
                if not categoria:
                    flash('Categoria invalida', 'error')
                    return redirect(url_for('novo_produto'))
                fornecedor = Fornecedor.query.get(fornecedor_id) if fornecedor_id else None
                if not fornecedor:
                    flash('Fornecedor invalido. Selecione um fornecedor para o produto.', 'error')
                    return redirect(url_for('novo_produto'))

                endereco_id = request.form.get('endereco_id', type=int) or None
                if endereco_id and not _carregar_endereco_permitido(endereco_id, funcionario_logado, apenas_ativo=True):
                    flash('Endereco invalido ou fora dos estoques permitidos.', 'error')
                    return redirect(url_for('novo_produto'))

                codigo_barras, erro_codigo = _normalizar_codigo_barras(request.form.get('codigo'))
                if erro_codigo:
                    flash(erro_codigo, 'error')
                    return redirect(url_for('novo_produto'))

                nova_imagem_path, erro_imagem = _save_product_image(
                    request.files.get('imagem'),
                    request.form.get('nome')
                )
                if erro_imagem:
                    flash(erro_imagem, 'error')
                    return redirect(url_for('novo_produto'))

                produto = Produto(
                    codigo=codigo_barras,
                    nome=request.form.get('nome'),
                    descricao=request.form.get('descricao'),
                    imagem_path=_normalizar_imagem_produto(nova_imagem_path),
                    categoria_id=categoria_id,
                    fornecedor_id=fornecedor.id,
                    endereco_id=endereco_id,
                    preco_custo=float(request.form.get('preco_custo', 0)),
                    preco_venda=float(request.form.get('preco_venda', 0)),
                    quantidade_estoque=int(request.form.get('quantidade_estoque', 0)),
                    quantidade_minima=int(request.form.get('quantidade_minima', 5)),
                    status_disponibilidade=_normalizar_status_disponibilidade(request.form.get('status_disponibilidade')),
                    tipo_movimentacao=_normalizar_tipo_movimentacao(request.form.get('tipo_movimentacao')),
                    fora_picking=(request.form.get('fora_picking') == 'on'),
                    prioridade_reabastecimento=request.form.get('prioridade_reabastecimento', type=int),
                    servico_montagem_disponivel=(request.form.get('servico_montagem_disponivel') == 'on'),
                    servico_instalacao_disponivel=(request.form.get('servico_instalacao_disponivel') == 'on'),
                )
                db.session.add(produto)
                db.session.commit()
                flash(f'Produto "{produto.nome}" criado com sucesso!', 'success')
                return redirect(url_for('listar_produtos'))
            except Exception as e:
                db.session.rollback()
                if nova_imagem_path:
                    _delete_image_file(nova_imagem_path)
                flash(f'Erro ao criar produto: {str(e)}', 'error')

        categorias = Categoria.query.all()
        fornecedores = Fornecedor.query.filter(
            Fornecedor.ativo.is_(True),
            db.func.lower(Fornecedor.nome) != fornecedor_padrao_recebimento_nome.lower(),
        ).order_by(Fornecedor.nome.asc()).all()
        enderecos = _endereco_query_permitida(funcionario_logado).filter_by(ativo=True).order_by(EnderecoEstoque.nome.asc()).all()
        return render_template(
            'estoque/produtos/novo_produto.html',
            categorias=categorias,
            fornecedores=fornecedores,
            enderecos=enderecos,
            status_disponibilidade_labels=STATUS_DISPONIBILIDADE_LABELS,
            tipos_movimentacao_produto=TIPOS_MOVIMENTACAO_PRODUTO,
            codigos_existentes=[c[0] for c in db.session.query(Produto.codigo).all()]
        )

    @app.route('/produtos/<int:produto_id>/editar', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def editar_produto(produto_id):
        funcionario_logado = _funcionario_logado_estoque()
        produto = Produto.query.get_or_404(produto_id)
        if not _produto_em_estoque_permitido(produto, funcionario_logado):
            flash('Você não possui acesso ao estoque deste produto.', 'danger')
            return redirect(url_for('listar_produtos'))
        if request.method == 'POST':
            nova_imagem_path = None
            imagem_anterior = produto.imagem_path
            try:
                fornecedor_id = request.form.get('fornecedor_id', type=int)
                fornecedor = Fornecedor.query.get(fornecedor_id) if fornecedor_id else None
                if not fornecedor:
                    flash('Fornecedor invalido. Selecione um fornecedor para o produto.', 'error')
                    return redirect(url_for('editar_produto', produto_id=produto_id))
                endereco_id = request.form.get('endereco_id', type=int) or None
                if endereco_id and not _carregar_endereco_permitido(endereco_id, funcionario_logado, apenas_ativo=True):
                    flash('Endereco invalido ou fora dos estoques permitidos.', 'error')
                    return redirect(url_for('editar_produto', produto_id=produto_id))
                produto.nome = request.form.get('nome')
                produto.descricao = request.form.get('descricao')
                produto.categoria_id = int(request.form.get('categoria_id'))
                produto.fornecedor_id = fornecedor.id
                produto.endereco_id = endereco_id
                preco_custo_raw = request.form.get('preco_custo')
                if preco_custo_raw is not None and str(preco_custo_raw).strip() != '':
                    produto.preco_custo = float(preco_custo_raw)

                preco_venda_raw = request.form.get('preco_venda')
                if preco_venda_raw is not None and str(preco_venda_raw).strip() != '':
                    produto.preco_venda = float(preco_venda_raw)
                produto.quantidade_minima = int(request.form.get('quantidade_minima', 5))
                produto.status_disponibilidade = _normalizar_status_disponibilidade(request.form.get('status_disponibilidade'))
                produto.tipo_movimentacao = _normalizar_tipo_movimentacao(request.form.get('tipo_movimentacao'))
                produto.fora_picking = (request.form.get('fora_picking') == 'on')
                produto.prioridade_reabastecimento = request.form.get('prioridade_reabastecimento', type=int)
                produto.servico_montagem_disponivel = (request.form.get('servico_montagem_disponivel') == 'on')
                produto.servico_instalacao_disponivel = (request.form.get('servico_instalacao_disponivel') == 'on')

                remover_imagem = request.form.get('remover_imagem') == 'on'
                arquivo_imagem = request.files.get('imagem')

                if arquivo_imagem and arquivo_imagem.filename:
                    nova_imagem_path, erro_imagem = _save_product_image(arquivo_imagem, produto.nome)
                    if erro_imagem:
                        flash(erro_imagem, 'error')
                        return redirect(url_for('editar_produto', produto_id=produto_id))
                    produto.imagem_path = nova_imagem_path
                elif remover_imagem:
                    produto.imagem_path = _imagem_padrao_produto()

                produto.imagem_path = _normalizar_imagem_produto(produto.imagem_path)

                db.session.commit()

                if nova_imagem_path and imagem_anterior and imagem_anterior != nova_imagem_path:
                    _delete_image_file(imagem_anterior)
                if remover_imagem and imagem_anterior:
                    _delete_image_file(imagem_anterior)

                flash(f'Produto "{produto.nome}" atualizado com sucesso!', 'success')
                return redirect(url_for('listar_produtos'))
            except Exception as e:
                db.session.rollback()
                if nova_imagem_path:
                    _delete_image_file(nova_imagem_path)
                flash(f'Erro ao atualizar produto: {str(e)}', 'error')

        categorias = Categoria.query.all()
        fornecedores = Fornecedor.query.filter(
            Fornecedor.ativo.is_(True),
            db.func.lower(Fornecedor.nome) != fornecedor_padrao_recebimento_nome.lower(),
        ).order_by(Fornecedor.nome.asc()).all()
        enderecos = _endereco_query_permitida(funcionario_logado).filter_by(ativo=True).order_by(EnderecoEstoque.nome.asc()).all()
        return render_template(
            'estoque/produtos/editar_produto.html',
            produto=produto,
            categorias=categorias,
            fornecedores=fornecedores,
            enderecos=enderecos,
            status_disponibilidade_labels=STATUS_DISPONIBILIDADE_LABELS,
            tipos_movimentacao_produto=TIPOS_MOVIMENTACAO_PRODUTO,
            codigos_existentes=[c[0] for c in db.session.query(Produto.codigo).filter(Produto.id != produto.id).all()]
        )

    @app.route('/produtos/<int:produto_id>')
    @login_required
    def visualizar_produto(produto_id):
        funcionario_logado = _funcionario_logado_estoque()
        produto = Produto.query.get_or_404(produto_id)
        if not _produto_em_estoque_permitido(produto, funcionario_logado):
            flash('Você não possui acesso ao estoque deste produto.', 'danger')
            return redirect(url_for('listar_produtos'))
        movimentacoes = Movimentacao.query.filter_by(produto_id=produto_id).order_by(
            Movimentacao.criado_em.desc()
        ).all()
        return render_template('estoque/produtos/visualizar_produto.html', produto=produto, movimentacoes=movimentacoes)

    @app.route('/produtos/<int:produto_id>/deletar', methods=['POST'])
    @require_role(*estoque_write_roles)
    def deletar_produto(produto_id):
        funcionario_logado = _funcionario_logado_estoque()
        produto = Produto.query.get_or_404(produto_id)
        if not _produto_em_estoque_permitido(produto, funcionario_logado):
            flash('Você não possui acesso ao estoque deste produto.', 'danger')
            return redirect(url_for('listar_produtos'))
        imagem_produto = produto.imagem_path
        try:
            db.session.delete(produto)
            db.session.commit()
            if imagem_produto:
                _delete_image_file(imagem_produto)
            flash(f'Produto "{produto.nome}" deletado com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao deletar produto: {str(e)}', 'error')
        return redirect(url_for('listar_produtos'))

    @app.route('/produtos/<int:produto_id>/marcar-fora-picking', methods=['POST'])
    @require_role(*estoque_write_roles)
    def marcar_produto_fora_picking(produto_id):
        funcionario_logado = _funcionario_logado_estoque()
        produto = Produto.query.get_or_404(produto_id)
        if not _produto_em_estoque_permitido(produto, funcionario_logado):
            flash('Você não possui acesso ao estoque deste produto.', 'danger')
            return redirect(request.referrer or url_for('listar_produtos'))
        try:
            produto.fora_picking = True
            db.session.commit()
            flash(f'Produto "{produto.nome}" marcado como fora de picking.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao marcar fora de picking: {str(e)}', 'error')
        return redirect(request.referrer or url_for('listar_produtos'))

    @app.route('/produtos/<int:produto_id>/baixar-para-picking', methods=['POST'])
    @require_role(*estoque_write_roles)
    def baixar_produto_para_picking(produto_id):
        funcionario_logado = _funcionario_logado_estoque()
        produto = Produto.query.get_or_404(produto_id)
        if not _produto_em_estoque_permitido(produto, funcionario_logado):
            flash('Você não possui acesso ao estoque deste produto.', 'danger')
            return redirect(request.referrer or url_for('listar_produtos'))
        try:
            produto.fora_picking = False
            produto.ultima_baixa_picking_em = datetime.utcnow()
            db.session.commit()
            flash(f'Produto "{produto.nome}" baixado para fluxo de picking.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao baixar produto para picking: {str(e)}', 'error')
        return redirect(request.referrer or url_for('listar_produtos'))

    @app.route('/estoque/enderecos-inteligentes')
    @login_required
    def enderecos_inteligentes():
        empresa = _obter_empresa_config_estoque()
        funcionario_logado = _funcionario_logado_estoque()
        dias = request.args.get('dias', type=int) or 30
        if dias not in {7, 15, 30, 60, 90}:
            dias = 30
        data_limite = datetime.utcnow() - timedelta(days=dias)

        mais_vendidos = db.session.query(
            ItemPedido.produto_id,
            db.func.sum(ItemPedido.quantidade).label('qtd_vendida'),
        ).join(
            Pedido, Pedido.id == ItemPedido.pedido_id
        ).filter(
            Pedido.criado_em >= data_limite,
            Pedido.status != Pedido.STATUS_CANCELADO,
        ).group_by(
            ItemPedido.produto_id
        ).order_by(
            db.desc('qtd_vendida')
        ).limit(40).all()

        produtos_ids = [item.produto_id for item in mais_vendidos]
        produtos_map = {
            p.id: p for p in _produto_query_permitida(Produto.query, funcionario_logado).options(
                selectinload(Produto.endereco),
                selectinload(Produto.categoria),
            ).filter(Produto.id.in_(produtos_ids)).all()
        } if produtos_ids else {}

        ranking = []
        for item in mais_vendidos:
            produto = produtos_map.get(item.produto_id)
            if not produto:
                continue
            endereco = produto.endereco
            em_area_picking = bool(endereco and (endereco.tipo_area or '').lower() in {'picking', 'box_expedicao'})
            ranking.append({
                'produto': produto,
                'qtd_vendida': int(item.qtd_vendida or 0),
                'em_area_picking': em_area_picking,
            })

        enderecos_picking = _endereco_query_permitida(funcionario_logado).filter(
            EnderecoEstoque.ativo.is_(True),
            EnderecoEstoque.status == 'ativo',
            EnderecoEstoque.tipo_area.in_(['picking', 'box_expedicao', 'expedicao'])
        ).order_by(
            db.case((EnderecoEstoque.tipo_area == 'box_expedicao', 0), else_=1),
            EnderecoEstoque.prioridade_picking.asc().nullslast(),
            EnderecoEstoque.nome.asc()
        ).all()

        fora_picking = _produto_query_permitida(Produto.query, funcionario_logado).options(
            selectinload(Produto.endereco),
            selectinload(Produto.categoria),
        ).filter(
            Produto.ativo.is_(True),
            Produto.fora_picking.is_(True),
        ).order_by(
            db.case((Produto.prioridade_reabastecimento.is_(None), 1), else_=0),
            Produto.prioridade_reabastecimento.asc(),
            Produto.nome.asc()
        ).limit(120).all()

        return render_template(
            'estoque/enderecos/enderecos_inteligentes.html',
            empresa=empresa,
            dias=dias,
            ranking=ranking,
            enderecos_picking=enderecos_picking,
            fora_picking=fora_picking,
            reposicao_loja_ativa=_reposicao_loja_fisica_ativa(empresa),
            etiquetas_loja_ativas=_emissao_etiqueta_loja_ativa(empresa),
            etiquetas_endereco_ativas=_emissao_etiqueta_endereco_ativa(empresa),
            tipos_movimentacao_produto=TIPOS_MOVIMENTACAO_PRODUTO,
        )

    @app.route('/produtos/<int:produto_id>/enderecar-inteligente', methods=['POST'])
    @require_role(*estoque_write_roles)
    def enderecar_produto_inteligente(produto_id):
        funcionario_logado = _funcionario_logado_estoque()
        produto = Produto.query.get_or_404(produto_id)
        if not _produto_em_estoque_permitido(produto, funcionario_logado):
            flash('Você não possui acesso ao estoque deste produto.', 'danger')
            return redirect(request.referrer or url_for('enderecos_inteligentes'))
        try:
            endereco_id = request.form.get('endereco_id', type=int)
            endereco = _carregar_endereco_permitido(endereco_id, funcionario_logado, apenas_ativo=True) if endereco_id else None
            if not endereco:
                flash('Endereco inteligente invalido ou inativo.', 'error')
                return redirect(request.referrer or url_for('enderecos_inteligentes'))
            produto.endereco_id = endereco.id
            produto.fora_picking = False
            produto.ultima_baixa_picking_em = datetime.utcnow()
            db.session.commit()
            flash(f'Produto "{produto.nome}" direcionado para "{endereco.nome}" com sucesso.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao enderecar produto: {str(e)}', 'error')
        return redirect(request.referrer or url_for('enderecos_inteligentes'))

    @app.route('/estoque/equipamentos')
    @login_required
    def listar_equipamentos_movimentacao():
        status = (request.args.get('status') or '').strip().lower()
        tipo = (request.args.get('tipo') or '').strip().lower()
        busca = (request.args.get('busca') or '').strip()

        query = EquipamentoMovimentacao.query
        if status in EquipamentoMovimentacao.STATUS_VALIDOS:
            query = query.filter(EquipamentoMovimentacao.status == status)
        if tipo in EquipamentoMovimentacao.TIPOS_VALIDOS:
            query = query.filter(EquipamentoMovimentacao.tipo == tipo)
        if busca:
            termo = f'%{busca}%'
            query = query.filter(
                db.or_(
                    EquipamentoMovimentacao.codigo.ilike(termo),
                    EquipamentoMovimentacao.nome.ilike(termo),
                    EquipamentoMovimentacao.placa.ilike(termo),
                    EquipamentoMovimentacao.bateria_codigo.ilike(termo),
                )
            )

        equipamentos = query.order_by(
            db.case((EquipamentoMovimentacao.status == EquipamentoMovimentacao.STATUS_OPERACIONAL, 0), else_=1),
            EquipamentoMovimentacao.nome.asc(),
        ).all()
        return render_template(
            'estoque/equipamentos/equipamentos.html',
            equipamentos=equipamentos,
            filtros={'status': status, 'tipo': tipo, 'busca': busca},
            tipos_validos=EquipamentoMovimentacao.TIPOS_VALIDOS,
            status_validos=EquipamentoMovimentacao.STATUS_VALIDOS,
        )

    @app.route('/estoque/equipamentos/novo', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def novo_equipamento_movimentacao():
        if request.method == 'POST':
            try:
                codigo = (request.form.get('codigo') or '').strip().upper()
                nome = (request.form.get('nome') or '').strip()
                tipo = (request.form.get('tipo') or '').strip().lower()
                status = (request.form.get('status') or '').strip().lower()
                if not codigo or not nome:
                    flash('Codigo e nome do equipamento sao obrigatorios.', 'error')
                    return redirect(url_for('novo_equipamento_movimentacao'))
                if tipo not in EquipamentoMovimentacao.TIPOS_VALIDOS:
                    tipo = EquipamentoMovimentacao.TIPO_EMPILHADEIRA
                if status not in EquipamentoMovimentacao.STATUS_VALIDOS:
                    status = EquipamentoMovimentacao.STATUS_OPERACIONAL

                proxima_manutencao_em = None
                data_txt = (request.form.get('proxima_manutencao_em') or '').strip()
                if data_txt:
                    try:
                        proxima_manutencao_em = datetime.strptime(data_txt, '%Y-%m-%d').date()
                    except ValueError:
                        flash('Data de proxima manutencao invalida.', 'error')
                        return redirect(url_for('novo_equipamento_movimentacao'))

                equipamento = EquipamentoMovimentacao(
                    codigo=codigo,
                    nome=nome,
                    tipo=tipo,
                    placa=(request.form.get('placa') or '').strip().upper() or None,
                    capacidade_kg=request.form.get('capacidade_kg', type=float),
                    bateria_codigo=(request.form.get('bateria_codigo') or '').strip().upper() or None,
                    bateria_nivel=request.form.get('bateria_nivel', type=int),
                    status=status,
                    proxima_manutencao_em=proxima_manutencao_em,
                    observacoes=(request.form.get('observacoes') or '').strip() or None,
                    ativo=(request.form.get('ativo') == 'on'),
                )
                db.session.add(equipamento)
                db.session.commit()
                flash(f'Equipamento "{equipamento.nome}" cadastrado com sucesso.', 'success')
                return redirect(url_for('listar_equipamentos_movimentacao'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao cadastrar equipamento: {str(e)}', 'error')

        return render_template(
            'estoque/equipamentos/novo_equipamento.html',
            tipos_validos=EquipamentoMovimentacao.TIPOS_VALIDOS,
            status_validos=EquipamentoMovimentacao.STATUS_VALIDOS,
        )

    @app.route('/estoque/equipamentos/<int:equipamento_id>/editar', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def editar_equipamento_movimentacao(equipamento_id):
        equipamento = EquipamentoMovimentacao.query.get_or_404(equipamento_id)
        if request.method == 'POST':
            try:
                if request.form.get('acao') == 'nova_manutencao':
                    descricao = (request.form.get('descricao_manutencao') or '').strip()
                    if not descricao:
                        flash('Descricao da manutencao e obrigatoria.', 'error')
                        return redirect(url_for('editar_equipamento_movimentacao', equipamento_id=equipamento.id))
                    tipo_manut = (request.form.get('tipo_manutencao') or 'preventiva').strip().lower()
                    if tipo_manut not in {'preventiva', 'corretiva'}:
                        tipo_manut = 'preventiva'
                    realizado_em = None
                    realizado_txt = (request.form.get('realizado_em') or '').strip()
                    if realizado_txt:
                        realizado_em = datetime.strptime(realizado_txt, '%Y-%m-%d').date()
                    proxima_em = None
                    proxima_txt = (request.form.get('proxima_em') or '').strip()
                    if proxima_txt:
                        proxima_em = datetime.strptime(proxima_txt, '%Y-%m-%d').date()
                    manutencao = ManutencaoEquipamento(
                        equipamento_id=equipamento.id,
                        tipo=tipo_manut,
                        descricao=descricao,
                        custo=request.form.get('custo_manutencao', type=float),
                        realizado_em=realizado_em,
                        proxima_em=proxima_em,
                        responsavel=(request.form.get('responsavel_manutencao') or '').strip() or None,
                    )
                    db.session.add(manutencao)
                    if proxima_em:
                        equipamento.proxima_manutencao_em = proxima_em
                    equipamento.status = EquipamentoMovimentacao.STATUS_MANUTENCAO if tipo_manut == 'corretiva' else equipamento.status
                    db.session.commit()
                    flash('Manutencao registrada com sucesso.', 'success')
                    return redirect(url_for('editar_equipamento_movimentacao', equipamento_id=equipamento.id))

                equipamento.codigo = (request.form.get('codigo') or '').strip().upper()
                equipamento.nome = (request.form.get('nome') or '').strip()
                tipo = (request.form.get('tipo') or '').strip().lower()
                status = (request.form.get('status') or '').strip().lower()
                if tipo in EquipamentoMovimentacao.TIPOS_VALIDOS:
                    equipamento.tipo = tipo
                if status in EquipamentoMovimentacao.STATUS_VALIDOS:
                    equipamento.status = status
                equipamento.placa = (request.form.get('placa') or '').strip().upper() or None
                equipamento.capacidade_kg = request.form.get('capacidade_kg', type=float)
                equipamento.bateria_codigo = (request.form.get('bateria_codigo') or '').strip().upper() or None
                equipamento.bateria_nivel = request.form.get('bateria_nivel', type=int)
                equipamento.observacoes = (request.form.get('observacoes') or '').strip() or None
                equipamento.ativo = (request.form.get('ativo') == 'on')
                data_txt = (request.form.get('proxima_manutencao_em') or '').strip()
                equipamento.proxima_manutencao_em = datetime.strptime(data_txt, '%Y-%m-%d').date() if data_txt else None

                if not equipamento.codigo or not equipamento.nome:
                    flash('Codigo e nome do equipamento sao obrigatorios.', 'error')
                    return redirect(url_for('editar_equipamento_movimentacao', equipamento_id=equipamento.id))

                db.session.commit()
                flash('Equipamento atualizado com sucesso.', 'success')
                return redirect(url_for('listar_equipamentos_movimentacao'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao atualizar equipamento: {str(e)}', 'error')

        manutencoes = ManutencaoEquipamento.query.filter_by(
            equipamento_id=equipamento.id
        ).order_by(
            ManutencaoEquipamento.criado_em.desc()
        ).all()
        return render_template(
            'estoque/equipamentos/editar_equipamento.html',
            equipamento=equipamento,
            manutencoes=manutencoes,
            tipos_validos=EquipamentoMovimentacao.TIPOS_VALIDOS,
            status_validos=EquipamentoMovimentacao.STATUS_VALIDOS,
        )

    @app.route('/categorias')
    @login_required
    def listar_categorias():
        categorias = Categoria.query.all()
        return render_template('estoque/categorias/categorias.html', categorias=categorias)

    @app.route('/categorias/nova', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def nova_categoria():
        if request.method == 'POST':
            nova_imagem_path = None
            try:
                nome_categoria = request.form.get('nome')
                nova_imagem_path, erro_imagem = _save_category_image(
                    request.files.get('imagem'),
                    nome_categoria
                )
                if erro_imagem:
                    flash(erro_imagem, 'error')
                    return redirect(url_for('nova_categoria'))

                categoria = Categoria(
                    nome=nome_categoria,
                    descricao=request.form.get('descricao'),
                    imagem_path=nova_imagem_path
                )
                db.session.add(categoria)
                db.session.commit()
                flash(f'Categoria "{categoria.nome}" criada com sucesso!', 'success')
                return redirect(url_for('listar_categorias'))
            except Exception as e:
                db.session.rollback()
                if nova_imagem_path:
                    _delete_image_file(nova_imagem_path)
                flash(f'Erro ao criar categoria: {str(e)}', 'error')
        return render_template('estoque/categorias/nova_categoria.html')

    @app.route('/categorias/<int:categoria_id>/editar', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def editar_categoria(categoria_id):
        categoria = Categoria.query.get_or_404(categoria_id)
        if request.method == 'POST':
            nova_imagem_path = None
            imagem_anterior = categoria.imagem_path
            try:
                categoria.nome = request.form.get('nome')
                categoria.descricao = request.form.get('descricao')
                remover_imagem = request.form.get('remover_imagem') == 'on'
                arquivo_imagem = request.files.get('imagem')

                if arquivo_imagem and arquivo_imagem.filename:
                    nova_imagem_path, erro_imagem = _save_category_image(arquivo_imagem, categoria.nome)
                    if erro_imagem:
                        flash(erro_imagem, 'error')
                        return redirect(url_for('editar_categoria', categoria_id=categoria_id))
                    categoria.imagem_path = nova_imagem_path
                elif remover_imagem:
                    categoria.imagem_path = None

                db.session.commit()

                if nova_imagem_path and imagem_anterior and imagem_anterior != nova_imagem_path:
                    _delete_image_file(imagem_anterior)
                if remover_imagem and imagem_anterior:
                    _delete_image_file(imagem_anterior)

                flash(f'Categoria "{categoria.nome}" atualizada com sucesso!', 'success')
                return redirect(url_for('listar_categorias'))
            except Exception as e:
                db.session.rollback()
                if nova_imagem_path:
                    _delete_image_file(nova_imagem_path)
                flash(f'Erro ao atualizar categoria: {str(e)}', 'error')
        return render_template('estoque/categorias/editar_categoria.html', categoria=categoria)

    @app.route('/categorias/<int:categoria_id>/deletar', methods=['POST'])
    @require_role(*estoque_write_roles)
    def deletar_categoria(categoria_id):
        categoria = Categoria.query.get_or_404(categoria_id)
        imagem_categoria = categoria.imagem_path
        try:
            db.session.delete(categoria)
            db.session.commit()
            if imagem_categoria:
                _delete_image_file(imagem_categoria)
            flash(f'Categoria "{categoria.nome}" deletada com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao deletar categoria: {str(e)}', 'error')
        return redirect(url_for('listar_categorias'))

    @app.route('/fornecedores')
    @login_required
    def listar_fornecedores():
        page = max(request.args.get('page', 1, type=int), 1)
        per_page = min(max(request.args.get('per_page', 25, type=int), 1), 100)
        busca = (request.args.get('busca') or '').strip()
        status = (request.args.get('status') or '').strip().lower()

        query = Fornecedor.query
        if busca:
            termo = f'%{busca}%'
            query = query.filter(
                db.or_(
                    Fornecedor.nome.ilike(termo),
                    Fornecedor.documento.ilike(termo),
                    Fornecedor.contato.ilike(termo),
                    Fornecedor.telefone.ilike(termo),
                    Fornecedor.email.ilike(termo),
                    Fornecedor.endereco_cidade.ilike(termo),
                    Fornecedor.tipo_produtos_fornece.ilike(termo),
                )
            )
        if status == 'ativo':
            query = query.filter(Fornecedor.ativo.is_(True))
        elif status == 'inativo':
            query = query.filter(Fornecedor.ativo.is_(False))

        pagination = query.order_by(Fornecedor.nome.asc()).paginate(page=page, per_page=per_page, error_out=False)
        return render_template(
            'estoque/fornecedores/fornecedores.html',
            fornecedores=pagination.items,
            pagination=pagination,
            per_page=per_page,
            filtros={'busca': busca, 'status': status},
            query_params=request.args.to_dict(),
        )

    @app.route('/fornecedores/<int:fornecedor_id>')
    @login_required
    def detalhes_fornecedor(fornecedor_id):
        fornecedor = Fornecedor.query.get_or_404(fornecedor_id)
        recebimentos = RecebimentoFornecedor.query.filter_by(
            fornecedor_id=fornecedor.id
        ).order_by(
            RecebimentoFornecedor.criado_em.desc()
        ).limit(20).all()
        movimentacoes = Movimentacao.query.filter_by(
            fornecedor_id=fornecedor.id
        ).order_by(
            Movimentacao.criado_em.desc()
        ).limit(20).all()
        return render_template(
            'estoque/fornecedores/detalhes_fornecedor.html',
            fornecedor=fornecedor,
            recebimentos=recebimentos,
            movimentacoes=movimentacoes,
        )

    @app.route('/fornecedores/novo', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def novo_fornecedor():
        if request.method == 'POST':
            try:
                fornecedor = Fornecedor(
                    nome=request.form.get('nome', '').strip(),
                    documento=request.form.get('documento', '').strip() or None,
                    contato=request.form.get('contato', '').strip() or None,
                    telefone=request.form.get('telefone', '').strip() or None,
                    email=request.form.get('email', '').strip() or None,
                    endereco_rua=request.form.get('endereco_rua', '').strip() or None,
                    endereco_numero=request.form.get('endereco_numero', '').strip() or None,
                    endereco_bairro=request.form.get('endereco_bairro', '').strip() or None,
                    endereco_cidade=request.form.get('endereco_cidade', '').strip() or None,
                    tipo_produtos_fornece=request.form.get('tipo_produtos_fornece', '').strip() or None,
                    observacoes_gerais=request.form.get('observacoes_gerais', '').strip() or None,
                    ativo=(request.form.get('ativo') == 'on')
                )
                if not fornecedor.nome:
                    flash('Nome do fornecedor e obrigatorio.', 'error')
                    return redirect(url_for('novo_fornecedor'))
                db.session.add(fornecedor)
                db.session.commit()
                flash(f'Fornecedor "{fornecedor.nome}" cadastrado com sucesso!', 'success')
                return redirect(url_for('listar_fornecedores'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao cadastrar fornecedor: {str(e)}', 'error')
        return render_template('estoque/fornecedores/novo_fornecedor.html')

    @app.route('/fornecedores/<int:fornecedor_id>/editar', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def editar_fornecedor(fornecedor_id):
        fornecedor = Fornecedor.query.get_or_404(fornecedor_id)
        if request.method == 'POST':
            try:
                nome = request.form.get('nome', '').strip()
                if not nome:
                    flash('Nome do fornecedor e obrigatorio.', 'error')
                    return redirect(url_for('editar_fornecedor', fornecedor_id=fornecedor_id))
                fornecedor.nome = nome
                fornecedor.documento = request.form.get('documento', '').strip() or None
                fornecedor.contato = request.form.get('contato', '').strip() or None
                fornecedor.telefone = request.form.get('telefone', '').strip() or None
                fornecedor.email = request.form.get('email', '').strip() or None
                fornecedor.endereco_rua = request.form.get('endereco_rua', '').strip() or None
                fornecedor.endereco_numero = request.form.get('endereco_numero', '').strip() or None
                fornecedor.endereco_bairro = request.form.get('endereco_bairro', '').strip() or None
                fornecedor.endereco_cidade = request.form.get('endereco_cidade', '').strip() or None
                fornecedor.tipo_produtos_fornece = request.form.get('tipo_produtos_fornece', '').strip() or None
                fornecedor.observacoes_gerais = request.form.get('observacoes_gerais', '').strip() or None
                fornecedor.ativo = (request.form.get('ativo') == 'on')
                db.session.commit()
                flash(f'Fornecedor "{fornecedor.nome}" atualizado com sucesso!', 'success')
                return redirect(url_for('listar_fornecedores'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao atualizar fornecedor: {str(e)}', 'error')
        return render_template('estoque/fornecedores/editar_fornecedor.html', fornecedor=fornecedor)

    @app.route('/fornecedores/<int:fornecedor_id>/deletar', methods=['POST'])
    @require_role(*estoque_write_roles)
    def deletar_fornecedor(fornecedor_id):
        fornecedor = Fornecedor.query.get_or_404(fornecedor_id)
        try:
            db.session.delete(fornecedor)
            db.session.commit()
            flash(f'Fornecedor "{fornecedor.nome}" removido com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao remover fornecedor: {str(e)}', 'error')
        return redirect(url_for('listar_fornecedores'))

    @app.route('/estoque/recebimentos')
    @login_required
    def listar_recebimentos_fornecedor():
        page = max(request.args.get('page', 1, type=int), 1)
        per_page = min(max(request.args.get('per_page', 20, type=int), 1), 100)
        status = (request.args.get('status') or '').strip().lower()
        tipo_recebimento = (request.args.get('tipo_recebimento') or '').strip().lower()
        fornecedor_id = request.args.get('fornecedor_id', type=int)
        busca = (request.args.get('busca') or '').strip()
        data_inicio_txt = (request.args.get('data_inicio') or '').strip()
        data_fim_txt = (request.args.get('data_fim') or '').strip()
        data_inicio = _parse_data_filtro(data_inicio_txt)
        data_fim = _parse_data_filtro(data_fim_txt)

        query = RecebimentoFornecedor.query
        if status in RecebimentoFornecedor.STATUS_VALIDOS:
            query = query.filter(RecebimentoFornecedor.status == status)
        if tipo_recebimento in RecebimentoFornecedor.TIPOS_VALIDOS:
            query = query.filter(RecebimentoFornecedor.tipo_recebimento == tipo_recebimento)
        if fornecedor_id:
            query = query.filter(RecebimentoFornecedor.fornecedor_id == fornecedor_id)
        if data_inicio:
            query = query.filter(RecebimentoFornecedor.criado_em >= data_inicio)
        if data_fim:
            query = query.filter(RecebimentoFornecedor.criado_em < (data_fim + timedelta(days=1)))
        if busca:
            termo = f'%{busca}%'
            query = query.outerjoin(Fornecedor, Fornecedor.id == RecebimentoFornecedor.fornecedor_id).outerjoin(
                Funcionario, Funcionario.id == RecebimentoFornecedor.recebedor_funcionario_id
            ).outerjoin(
                RecebimentoItem, RecebimentoItem.recebimento_id == RecebimentoFornecedor.id
            ).outerjoin(
                Produto, Produto.id == RecebimentoItem.produto_id
            ).filter(
                db.or_(
                    Fornecedor.nome.ilike(termo),
                    Funcionario.nome.ilike(termo),
                    Funcionario.matricula.ilike(termo),
                    RecebimentoFornecedor.info_nota.ilike(termo),
                    RecebimentoFornecedor.observacoes.ilike(termo),
                    RecebimentoFornecedor.recebedor_nome.ilike(termo),
                    Produto.nome.ilike(termo),
                    Produto.codigo.ilike(termo),
                    db.cast(RecebimentoFornecedor.id, db.String).ilike(termo),
                )
            ).distinct()

        recebimentos = query.options(
            load_only(
                RecebimentoFornecedor.id,
                RecebimentoFornecedor.fornecedor_id,
                RecebimentoFornecedor.tipo_recebimento,
                RecebimentoFornecedor.info_nota,
                RecebimentoFornecedor.subtotal,
                RecebimentoFornecedor.total_pagar,
                RecebimentoFornecedor.status,
                RecebimentoFornecedor.recebedor_funcionario_id,
                RecebimentoFornecedor.recebedor_nome,
                RecebimentoFornecedor.criado_em,
                RecebimentoFornecedor.conferido_em,
            ),
            selectinload(RecebimentoFornecedor.fornecedor),
            selectinload(RecebimentoFornecedor.recebedor_funcionario),
            selectinload(RecebimentoFornecedor.itens).selectinload(RecebimentoItem.produto),
        ).order_by(RecebimentoFornecedor.criado_em.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False,
        )
        pendencias_armazenagem = RecebimentoFornecedor.query.filter_by(
            status=RecebimentoFornecedor.STATUS_AGUARDANDO_ARMAZENAGEM
        ).count()
        recebimento_armazenagem_mais_antigo = RecebimentoFornecedor.query.filter_by(
            status=RecebimentoFornecedor.STATUS_AGUARDANDO_ARMAZENAGEM
        ).order_by(
            RecebimentoFornecedor.conferido_em.asc(),
            RecebimentoFornecedor.criado_em.asc(),
        ).first()
        fornecedores = Fornecedor.query.filter(
            Fornecedor.ativo.is_(True),
            db.func.lower(Fornecedor.nome) != fornecedor_padrao_recebimento_nome.lower(),
        ).order_by(Fornecedor.nome.asc()).all()
        return render_template(
            'estoque/recebimentos/recebimentos.html',
            recebimentos=recebimentos.items,
            pagination=recebimentos,
            per_page=per_page,
            fornecedores=fornecedores,
            pendencias_armazenagem=pendencias_armazenagem,
            recebimento_armazenagem_mais_antigo=recebimento_armazenagem_mais_antigo,
            status_labels=recebimento_status_labels,
            tipo_labels=recebimento_tipo_labels,
            filtros={
                'status': status,
                'tipo_recebimento': tipo_recebimento,
                'fornecedor_id': fornecedor_id,
                'busca': busca,
                'data_inicio': data_inicio_txt,
                'data_fim': data_fim_txt,
            },
            query_params=request.args.to_dict(),
        )

    @app.route('/estoque/recebimentos/novo', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def novo_recebimento_fornecedor():
        funcionario_logado = _funcionario_logado_estoque()
        fornecedores = Fornecedor.query.filter(
            Fornecedor.ativo.is_(True),
            db.func.lower(Fornecedor.nome) != fornecedor_padrao_recebimento_nome.lower(),
        ).order_by(Fornecedor.nome.asc()).all()
        produtos = _produto_query_permitida(Produto.query.filter_by(ativo=True), funcionario_logado).order_by(Produto.nome.asc()).all()
        funcionarios_recebimento = Funcionario.query.filter_by(ativo=True).options(
            load_only(
                Funcionario.id,
                Funcionario.nome,
                Funcionario.matricula,
                Funcionario.numero_cadastro,
                Funcionario.departamento,
            )
        ).order_by(Funcionario.nome.asc()).all()

        if request.method == 'POST':
            try:
                fornecedor_id = request.form.get('fornecedor_id', type=int)
                tipo_recebimento = (request.form.get('tipo_recebimento') or '').strip().lower()
                fornecedor = Fornecedor.query.get(fornecedor_id) if fornecedor_id else None
                if tipo_recebimento not in RecebimentoFornecedor.TIPOS_VALIDOS:
                    flash('Selecione um tipo de recebimento valido.', 'error')
                    return redirect(url_for('novo_recebimento_fornecedor'))
                if fornecedor_id and not fornecedor:
                    flash('Selecione um fornecedor valido.', 'error')
                    return redirect(url_for('novo_recebimento_fornecedor'))
                if _tipo_recebimento_exige_fornecedor(tipo_recebimento) and not fornecedor:
                    flash('Este tipo de recebimento exige fornecedor informado.', 'error')
                    return redirect(url_for('novo_recebimento_fornecedor'))
                if not fornecedor:
                    fornecedor = _obter_fornecedor_padrao_recebimento()

                recebedor_funcionario = _resolver_funcionario_por_matricula_ou_nome(
                    texto_busca=(request.form.get('recebedor_busca') or request.form.get('recebedor_nome') or '').strip(),
                    funcionario_id=request.form.get('recebedor_funcionario_id', type=int),
                )
                recebedor_nome = (
                    recebedor_funcionario.nome
                    if recebedor_funcionario
                    else (request.form.get('recebedor_nome') or request.form.get('recebedor_busca') or '').strip() or None
                )

                produto_ids = request.form.getlist('produto_id[]') or request.form.getlist('produto_id')
                quantidades = request.form.getlist('qtd_recebida[]') or request.form.getlist('qtd_recebida')
                unidades = request.form.getlist('unidade[]') or request.form.getlist('unidade')
                descricoes_itens = request.form.getlist('descricao_item[]') or request.form.getlist('descricao_item')
                precos_unitarios = request.form.getlist('preco_unitario[]') or request.form.getlist('preco_unitario')
                if not produto_ids:
                    flash('Informe ao menos um item no recebimento.', 'error')
                    return redirect(url_for('novo_recebimento_fornecedor'))

                data_entrega = None
                data_entrega_txt = (request.form.get('data_entrega') or '').strip()
                if data_entrega_txt:
                    try:
                        data_entrega = datetime.strptime(data_entrega_txt, '%Y-%m-%d').date()
                    except ValueError:
                        flash('Data de entrega invalida.', 'error')
                        return redirect(url_for('novo_recebimento_fornecedor'))

                subtotal = 0.0
                desconto_raw = (request.form.get('desconto') or '').strip()
                if desconto_raw:
                    try:
                        desconto = float(desconto_raw.replace(',', '.'))
                    except ValueError:
                        flash('Desconto invalido.', 'error')
                        return redirect(url_for('novo_recebimento_fornecedor'))
                else:
                    desconto = 0.0
                if desconto < 0:
                    flash('Desconto nao pode ser negativo.', 'error')
                    return redirect(url_for('novo_recebimento_fornecedor'))

                itens_processados = []
                for idx, raw_produto_id in enumerate(produto_ids):
                    texto_produto_id = str(raw_produto_id or '').strip()
                    if not texto_produto_id:
                        continue
                    try:
                        produto_id = int(texto_produto_id)
                    except ValueError:
                        flash('Produto invalido em um dos itens.', 'error')
                        return redirect(url_for('novo_recebimento_fornecedor'))

                    produto = Produto.query.get(produto_id)
                    if not produto or not produto.ativo:
                        flash('Um dos produtos informados nao existe ou esta inativo.', 'error')
                        return redirect(url_for('novo_recebimento_fornecedor'))
                    if not _produto_em_estoque_permitido(produto, funcionario_logado):
                        flash(f'Voce nao possui acesso ao estoque do produto "{produto.nome}".', 'error')
                        return redirect(url_for('novo_recebimento_fornecedor'))

                    raw_qtd = quantidades[idx] if idx < len(quantidades) else '0'
                    try:
                        qtd_recebida = int(str(raw_qtd or '0').strip() or '0')
                    except ValueError:
                        flash(f'Quantidade invalida para o produto "{produto.nome}".', 'error')
                        return redirect(url_for('novo_recebimento_fornecedor'))
                    if qtd_recebida < 0:
                        flash(f'Quantidade recebida nao pode ser negativa para o produto "{produto.nome}".', 'error')
                        return redirect(url_for('novo_recebimento_fornecedor'))

                    unidade = (unidades[idx] if idx < len(unidades) else '').strip().upper() or 'UN'
                    descricao_item = (descricoes_itens[idx] if idx < len(descricoes_itens) else '').strip() or produto.nome
                    raw_preco = (precos_unitarios[idx] if idx < len(precos_unitarios) else '').strip()
                    if raw_preco:
                        try:
                            preco_unitario = float(raw_preco.replace(',', '.'))
                        except ValueError:
                            flash(f'Preco unitario invalido para o produto "{produto.nome}".', 'error')
                            return redirect(url_for('novo_recebimento_fornecedor'))
                    else:
                        preco_unitario = float(produto.preco_custo or 0.0)
                    if preco_unitario < 0:
                        flash(f'Preco unitario nao pode ser negativo para o produto "{produto.nome}".', 'error')
                        return redirect(url_for('novo_recebimento_fornecedor'))

                    total_item = float(qtd_recebida) * float(preco_unitario)
                    subtotal += total_item
                    itens_processados.append({
                        'produto_id': produto_id,
                        'qtd_recebida': qtd_recebida,
                        'unidade': unidade,
                        'descricao_item': descricao_item,
                        'preco_unitario': preco_unitario,
                        'total_item': total_item,
                    })

                if not itens_processados:
                    flash('Informe ao menos um item valido no recebimento.', 'error')
                    return redirect(url_for('novo_recebimento_fornecedor'))

                total_pagar = max(subtotal - desconto, 0.0)

                recebimento = RecebimentoFornecedor(
                    fornecedor_id=fornecedor.id,
                    tipo_recebimento=tipo_recebimento,
                    fornecedor_documento=(request.form.get('fornecedor_documento') or '').strip() or None,
                    data_entrega=data_entrega,
                    info_nota=(request.form.get('info_nota') or '').strip() or None,
                    subtotal=subtotal,
                    desconto=desconto,
                    total_pagar=total_pagar,
                    observacoes=(request.form.get('observacoes') or '').strip() or None,
                    recebedor_funcionario_id=(recebedor_funcionario.id if recebedor_funcionario else None),
                    recebedor_nome=recebedor_nome,
                    recebedor_assinatura=(request.form.get('recebedor_assinatura') or '').strip() or None,
                    entregador_nome=(request.form.get('entregador_nome') or '').strip() or None,
                    entregador_assinatura=(request.form.get('entregador_assinatura') or '').strip() or None,
                    status=RecebimentoFornecedor.STATUS_CRIADO,
                )
                ir_para_armazenagem = (request.form.get('ir_para_armazenagem') == 'on')
                if ir_para_armazenagem:
                    recebimento.status = RecebimentoFornecedor.STATUS_AGUARDANDO_ARMAZENAGEM
                    recebimento.conferido_em = datetime.utcnow()
                db.session.add(recebimento)
                db.session.flush()

                for item in itens_processados:
                    db.session.add(
                        RecebimentoItem(
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

                db.session.commit()
                if ir_para_armazenagem:
                    flash('Recebimento criado. Direcionando para armazenagem em enderecos ativos.', 'success')
                    return redirect(url_for('armazenar_recebimento_fornecedor', recebimento_id=recebimento.id))
                flash('Recebimento criado com sucesso. Agora confira os itens.', 'success')
                return redirect(url_for('conferir_recebimento_fornecedor', recebimento_id=recebimento.id))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao criar recebimento: {str(e)}', 'error')

        return render_template(
            'estoque/recebimentos/novo_recebimento.html',
            fornecedores=fornecedores,
            produtos=produtos,
            funcionarios_recebimento=funcionarios_recebimento,
            tipo_labels=recebimento_tipo_labels,
            tipo_recebimento_padrao=RecebimentoFornecedor.TIPO_COMPRA_REVENDA,
            tipos_fornecedor_opcional=sorted(recebimento_tipos_fornecedor_opcional),
        )

    @app.route('/estoque/recebimentos/<int:recebimento_id>/conferir', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def conferir_recebimento_fornecedor(recebimento_id):
        recebimento = RecebimentoFornecedor.query.options(
            selectinload(RecebimentoFornecedor.fornecedor),
            selectinload(RecebimentoFornecedor.recebedor_funcionario),
            selectinload(RecebimentoFornecedor.itens).selectinload(RecebimentoItem.produto),
        ).get_or_404(recebimento_id)

        if recebimento.status in {RecebimentoFornecedor.STATUS_CANCELADO, RecebimentoFornecedor.STATUS_CONCLUIDO}:
            flash('Nao e possivel conferir um recebimento cancelado ou concluido.', 'warning')
            return redirect(url_for('listar_recebimentos_fornecedor'))

        if request.method == 'POST':
            try:
                for item in recebimento.itens:
                    prefix = f'item_{item.id}_'
                    raw_qtd_recebida = request.form.get(f'{prefix}qtd_recebida', '0')
                    raw_qtd_avaria = request.form.get(f'{prefix}qtd_avaria', '0')
                    lote = (request.form.get(f'{prefix}lote') or '').strip() or None
                    validade_texto = (request.form.get(f'{prefix}validade') or '').strip()

                    try:
                        qtd_recebida = int(str(raw_qtd_recebida or '0').strip() or '0')
                    except ValueError:
                        raise ValueError(f'Quantidade recebida invalida para o produto "{item.produto.nome}".')
                    try:
                        qtd_avaria = int(str(raw_qtd_avaria or '0').strip() or '0')
                    except ValueError:
                        raise ValueError(f'Quantidade avariada invalida para o produto "{item.produto.nome}".')

                    if qtd_recebida < 0:
                        raise ValueError(f'Quantidade recebida nao pode ser negativa para o produto "{item.produto.nome}".')
                    if qtd_avaria < 0:
                        raise ValueError(f'Quantidade avariada nao pode ser negativa para o produto "{item.produto.nome}".')
                    if qtd_avaria > qtd_recebida:
                        raise ValueError(f'Avaria nao pode ser maior que recebimento no produto "{item.produto.nome}".')

                    validade = None
                    if validade_texto:
                        try:
                            validade = datetime.strptime(validade_texto, '%Y-%m-%d').date()
                        except ValueError:
                            raise ValueError(f'Data de validade invalida para o produto "{item.produto.nome}".')

                    item.qtd_recebida = qtd_recebida
                    item.qtd_avaria = qtd_avaria
                    item.lote = lote
                    item.validade = validade

                recebimento.status = RecebimentoFornecedor.STATUS_AGUARDANDO_ARMAZENAGEM
                recebimento.conferido_em = datetime.utcnow()
                db.session.commit()
                flash('Conferencia salva. Proximo passo: armazenagem (put-away).', 'success')
                return redirect(url_for('armazenar_recebimento_fornecedor', recebimento_id=recebimento.id))
            except ValueError as e:
                db.session.rollback()
                flash(str(e), 'error')
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao conferir recebimento: {str(e)}', 'error')

        return render_template(
            'estoque/recebimentos/conferir_recebimento.html',
            recebimento=recebimento,
            status_labels=recebimento_status_labels,
            tipo_labels=recebimento_tipo_labels,
        )

    @app.route('/estoque/recebimentos/<int:recebimento_id>/armazenar', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def armazenar_recebimento_fornecedor(recebimento_id):
        funcionario_logado = _funcionario_logado_estoque()
        recebimento = RecebimentoFornecedor.query.options(
            selectinload(RecebimentoFornecedor.fornecedor),
            selectinload(RecebimentoFornecedor.recebedor_funcionario),
            selectinload(RecebimentoFornecedor.itens).selectinload(RecebimentoItem.produto).selectinload(Produto.categoria),
        ).get_or_404(recebimento_id)

        if recebimento.status == RecebimentoFornecedor.STATUS_CANCELADO:
            flash('Recebimento cancelado. Armazenagem nao permitida.', 'warning')
            return redirect(url_for('listar_recebimentos_fornecedor'))
        if recebimento.status == RecebimentoFornecedor.STATUS_CONCLUIDO:
            flash('Recebimento ja concluido.', 'info')
            return redirect(url_for('listar_recebimentos_fornecedor'))
        if recebimento.status == RecebimentoFornecedor.STATUS_CRIADO:
            flash('Conclua a conferencia antes da armazenagem.', 'warning')
            return redirect(url_for('conferir_recebimento_fornecedor', recebimento_id=recebimento.id))

        enderecos_ativos = _endereco_query_permitida(funcionario_logado).filter(EnderecoEstoque.status == 'ativo').order_by(EnderecoEstoque.nome.asc()).all()
        enderecos_por_id = {endereco.id: endereco for endereco in enderecos_ativos}

        if request.method == 'POST':
            try:
                if not enderecos_ativos:
                    flash('Nao existem enderecos ativos para armazenagem.', 'error')
                    return redirect(url_for('armazenar_recebimento_fornecedor', recebimento_id=recebimento.id))

                erros = []
                destinos_por_item = {}
                for item in recebimento.itens:
                    endereco_destino_id = request.form.get(f'endereco_destino_{item.id}', type=int)
                    if not endereco_destino_id:
                        erros.append(f'Informe o endereco destino para "{item.produto.nome}".')
                        continue
                    endereco_destino = enderecos_por_id.get(endereco_destino_id)
                    if not endereco_destino:
                        erros.append(f'Endereco destino invalido/inativo para "{item.produto.nome}".')
                        continue
                    if item.qtd_liquida > 0 and (endereco_destino.controle_validade or 'nenhum') == 'fefo' and not item.validade:
                        erros.append(f'Endereco "{endereco_destino.nome}" exige FEFO. Informe validade para "{item.produto.nome}".')
                    restricoes = {parte.strip().lower() for parte in (endereco_destino.restricoes or '').split(',') if parte.strip()}
                    if 'alimentos' in restricoes and _categoria_parece_quimico(item.produto):
                        erros.append(
                            f'Produto "{item.produto.nome}" (categoria quimica) nao pode ser armazenado no endereco de alimentos "{endereco_destino.nome}".'
                        )
                    destinos_por_item[item.id] = endereco_destino

                if erros:
                    for erro in erros:
                        flash(erro, 'error')
                    return redirect(url_for('armazenar_recebimento_fornecedor', recebimento_id=recebimento.id))

                for item in recebimento.itens:
                    endereco_destino = destinos_por_item[item.id]
                    item.endereco_destino_id = endereco_destino.id
                    quantidade_entrada = item.qtd_liquida
                    if quantidade_entrada <= 0:
                        continue

                    aplicar_movimentacao_estoque(item.produto, Movimentacao.TIPO_ENTRADA, quantidade_entrada)

                    item.produto.endereco_id = endereco_destino.id
                    tipo_recebimento_label = recebimento_tipo_labels.get(
                        recebimento.tipo_recebimento,
                        recebimento.tipo_recebimento or 'Recebimento'
                    )
                    tipo_recebimento_slug = (
                        recebimento.tipo_recebimento
                        if recebimento.tipo_recebimento in RecebimentoFornecedor.TIPOS_VALIDOS
                        else 'compra_revenda'
                    )
                    observacoes_mov = f'Recebimento #{recebimento.id} | Tipo: {tipo_recebimento_label}'
                    if item.lote:
                        observacoes_mov += f' | Lote: {item.lote}'
                    if item.validade:
                        observacoes_mov += f' | Validade: {item.validade.strftime("%d/%m/%Y")}'
                    if item.qtd_avaria:
                        observacoes_mov += f' | Avaria: {item.qtd_avaria}'

                    movimentacao = Movimentacao(
                        produto_id=item.produto_id,
                        fornecedor_id=recebimento.fornecedor_id,
                        endereco_destino_id=endereco_destino.id,
                        tipo=Movimentacao.TIPO_ENTRADA,
                        quantidade=quantidade_entrada,
                        info_nota=recebimento.info_nota,
                        motivo=f'recebimento_{tipo_recebimento_slug}',
                        observacoes=observacoes_mov,
                    )
                    db.session.add(movimentacao)

                recebimento.status = RecebimentoFornecedor.STATUS_CONCLUIDO
                recebimento.armazenado_em = datetime.utcnow()
                db.session.commit()
                flash('Armazenagem concluida. Estoque atualizado com sucesso.', 'success')
                return redirect(url_for('listar_recebimentos_fornecedor'))
            except AppError as e:
                db.session.rollback()
                flash(str(e), 'error')
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao concluir armazenagem: {str(e)}', 'error')

        return render_template(
            'estoque/recebimentos/armazenar_recebimento.html',
            recebimento=recebimento,
            enderecos_ativos=enderecos_ativos,
            status_labels=recebimento_status_labels,
            tipo_labels=recebimento_tipo_labels,
        )

    @app.route('/estoque/recebimentos/<int:recebimento_id>/cancelar', methods=['POST'])
    @require_role(*estoque_write_roles)
    def cancelar_recebimento_fornecedor(recebimento_id):
        recebimento = RecebimentoFornecedor.query.get_or_404(recebimento_id)
        try:
            if recebimento.status == RecebimentoFornecedor.STATUS_CONCLUIDO:
                flash('Recebimento concluido nao pode ser cancelado.', 'error')
                return redirect(url_for('listar_recebimentos_fornecedor'))
            if recebimento.status == RecebimentoFornecedor.STATUS_CANCELADO:
                flash('Recebimento ja esta cancelado.', 'info')
                return redirect(url_for('listar_recebimentos_fornecedor'))
            recebimento.status = RecebimentoFornecedor.STATUS_CANCELADO
            db.session.commit()
            flash('Recebimento cancelado com sucesso.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao cancelar recebimento: {str(e)}', 'error')
        return redirect(url_for('listar_recebimentos_fornecedor'))

    @app.route('/estoque/almoxarifado')
    @login_required
    def listar_almoxarifado():
        funcionario_logado = _funcionario_logado_estoque()
        page = max(request.args.get('page', 1, type=int), 1)
        per_page = min(max(request.args.get('per_page', 20, type=int), 1), 100)
        busca = (request.args.get('busca') or '').strip()
        destino_tipo = (request.args.get('destino_tipo') or '').strip().lower()
        funcionario_id = request.args.get('funcionario_id', type=int)
        setor = (request.args.get('setor') or '').strip()

        query = AlmoxarifadoAtribuicao.query.join(Produto, Produto.id == AlmoxarifadoAtribuicao.produto_id)
        ids_estoques = _estoques_permitidos_ids(funcionario_logado)
        if ids_estoques is not None:
            if not ids_estoques:
                query = query.filter(Produto.endereco_id.is_(None))
            else:
                query = query.filter(
                    db.or_(
                        Produto.endereco_id.is_(None),
                        Produto.endereco.has(EnderecoEstoque.estoque_id.in_(ids_estoques)),
                    )
                )
        if destino_tipo in AlmoxarifadoAtribuicao.DESTINOS_VALIDOS:
            query = query.filter(AlmoxarifadoAtribuicao.destino_tipo == destino_tipo)
        if funcionario_id:
            query = query.filter(AlmoxarifadoAtribuicao.funcionario_id == funcionario_id)
        if setor:
            query = query.filter(AlmoxarifadoAtribuicao.setor_destino == setor)
        if busca:
            termo = f'%{busca}%'
            query = query.outerjoin(Funcionario, Funcionario.id == AlmoxarifadoAtribuicao.funcionario_id).filter(
                db.or_(
                    Produto.nome.ilike(termo),
                    Produto.codigo.ilike(termo),
                    AlmoxarifadoAtribuicao.nome_destino.ilike(termo),
                    AlmoxarifadoAtribuicao.matricula_referencia.ilike(termo),
                    AlmoxarifadoAtribuicao.setor_destino.ilike(termo),
                    Funcionario.nome.ilike(termo),
                )
            ).distinct()

        atribuicoes = query.options(
            selectinload(AlmoxarifadoAtribuicao.produto),
            selectinload(AlmoxarifadoAtribuicao.funcionario),
            selectinload(AlmoxarifadoAtribuicao.registrado_por),
        ).order_by(AlmoxarifadoAtribuicao.criado_em.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False,
        )
        funcionarios_ativos = Funcionario.query.filter_by(ativo=True).options(
            load_only(Funcionario.id, Funcionario.nome, Funcionario.matricula)
        ).order_by(Funcionario.nome.asc()).all()

        return render_template(
            'estoque/almoxarifado/almoxarifado.html',
            atribuicoes=atribuicoes.items,
            pagination=atribuicoes,
            per_page=per_page,
            funcionarios_ativos=funcionarios_ativos,
            setores_disponiveis=_listar_setores_almoxarifado(),
            destino_labels=almoxarifado_destino_labels,
            filtros={
                'busca': busca,
                'destino_tipo': destino_tipo,
                'funcionario_id': funcionario_id,
                'setor': setor,
            },
            query_params=request.args.to_dict(),
        )

    @app.route('/estoque/almoxarifado/nova', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def nova_atribuicao_almoxarifado():
        funcionario_logado = _funcionario_logado_estoque()
        produtos = _produto_query_permitida(Produto.query.filter_by(ativo=True), funcionario_logado).order_by(Produto.nome.asc()).all()
        funcionarios_ativos = Funcionario.query.filter_by(ativo=True).options(
            load_only(
                Funcionario.id,
                Funcionario.nome,
                Funcionario.matricula,
                Funcionario.numero_cadastro,
                Funcionario.departamento,
            )
        ).order_by(Funcionario.nome.asc()).all()
        setores_disponiveis = _listar_setores_almoxarifado()

        if request.method == 'POST':
            try:
                produto_id = request.form.get('produto_id', type=int)
                quantidade = request.form.get('quantidade', type=int)
                destino_tipo = (request.form.get('destino_tipo') or '').strip().lower()
                setor_destino = (request.form.get('setor_destino') or '').strip() or None
                observacoes = (request.form.get('observacoes') or '').strip() or None
                funcionario_destino = None

                produto = Produto.query.get(produto_id) if produto_id else None
                if not produto or not produto.ativo:
                    flash('Selecione um produto valido para o almoxarifado.', 'error')
                    return redirect(url_for('nova_atribuicao_almoxarifado'))
                if not _produto_em_estoque_permitido(produto, funcionario_logado):
                    flash('Voce nao possui acesso ao estoque desse produto.', 'error')
                    return redirect(url_for('nova_atribuicao_almoxarifado'))
                if not quantidade or quantidade <= 0:
                    flash('Informe uma quantidade maior que zero.', 'error')
                    return redirect(url_for('nova_atribuicao_almoxarifado'))
                if destino_tipo not in AlmoxarifadoAtribuicao.DESTINOS_VALIDOS:
                    flash('Selecione um destino valido para a atribuicao.', 'error')
                    return redirect(url_for('nova_atribuicao_almoxarifado'))

                if destino_tipo == AlmoxarifadoAtribuicao.DESTINO_FUNCIONARIO:
                    funcionario_destino = _resolver_funcionario_por_matricula_ou_nome(
                        texto_busca=(request.form.get('funcionario_busca') or '').strip(),
                        funcionario_id=request.form.get('funcionario_destino_id', type=int),
                    )
                    if not funcionario_destino:
                        flash('Selecione um funcionario valido por matricula ou nome.', 'error')
                        return redirect(url_for('nova_atribuicao_almoxarifado'))
                else:
                    if not setor_destino:
                        flash('Informe o setor que recebera o produto.', 'error')
                        return redirect(url_for('nova_atribuicao_almoxarifado'))

                aplicar_movimentacao_estoque(produto, Movimentacao.TIPO_SAIDA, quantidade)

                nome_destino = funcionario_destino.nome if funcionario_destino else setor_destino
                matricula_referencia = funcionario_destino.matricula if funcionario_destino else None
                descricao_movimentacao = f'Almoxarifado | Destino: {nome_destino}'
                if matricula_referencia:
                    descricao_movimentacao += f' | Matricula: {matricula_referencia}'
                if observacoes:
                    descricao_movimentacao += f' | Obs: {observacoes}'

                db.session.add(
                    AlmoxarifadoAtribuicao(
                        produto_id=produto.id,
                        funcionario_id=(funcionario_destino.id if funcionario_destino else None),
                        registrado_por_id=(funcionario_logado.id if funcionario_logado else None),
                        destino_tipo=destino_tipo,
                        nome_destino=nome_destino,
                        setor_destino=setor_destino,
                        matricula_referencia=matricula_referencia,
                        quantidade=quantidade,
                        observacoes=observacoes,
                    )
                )
                db.session.add(
                    Movimentacao(
                        produto_id=produto.id,
                        endereco_origem_id=produto.endereco_id,
                        tipo=Movimentacao.TIPO_SAIDA,
                        quantidade=quantidade,
                        motivo=f'almoxarifado_{destino_tipo}',
                        observacoes=descricao_movimentacao,
                    )
                )
                db.session.commit()
                flash('Atribuicao registrada no almoxarifado com baixa de estoque.', 'success')
                return redirect(url_for('listar_almoxarifado'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao registrar atribuicao do almoxarifado: {str(e)}', 'error')

        return render_template(
            'estoque/almoxarifado/nova_atribuicao.html',
            produtos=produtos,
            funcionarios_ativos=funcionarios_ativos,
            setores_disponiveis=setores_disponiveis,
            destino_labels=almoxarifado_destino_labels,
        )

    @app.route('/enderecos-estoque')
    @login_required
    def listar_enderecos_estoque():
        funcionario_logado = _funcionario_logado_estoque()
        page = max(request.args.get('page', 1, type=int), 1)
        per_page = min(max(request.args.get('per_page', 25, type=int), 1), 100)
        estoque_id = request.args.get('estoque_id', type=int)
        setor_zona = (request.args.get('setor_zona') or '').strip().lower()
        busca = (request.args.get('busca') or '').strip()
        status = (request.args.get('status') or '').strip().lower()

        if estoque_id and not _carregar_estoque_permitido(estoque_id, funcionario_logado):
            flash('Você não possui acesso ao estoque selecionado.', 'warning')
            return redirect(url_for('listar_enderecos_estoque'))

        query = _endereco_query_permitida(funcionario_logado)
        if estoque_id:
            query = query.filter(EnderecoEstoque.estoque_id == estoque_id)
        if setor_zona in SETORES_ZONA_VALIDOS:
            query = query.filter(EnderecoEstoque.setor_zona == setor_zona)
        if busca:
            termo = f'%{busca}%'
            query = query.filter(
                db.or_(
                    EnderecoEstoque.nome.ilike(termo),
                    EnderecoEstoque.codigo_localizacao.ilike(termo),
                    EnderecoEstoque.loja_cd.ilike(termo),
                    EnderecoEstoque.setor_zona.ilike(termo),
                    EnderecoEstoque.tipo_produto_reservado.ilike(termo),
                    EnderecoEstoque.rua.ilike(termo),
                    EnderecoEstoque.bairro.ilike(termo),
                    EnderecoEstoque.cidade.ilike(termo),
                )
            )
        if status in STATUS_ENDERECO_VALIDOS:
            query = query.filter(EnderecoEstoque.status == status)
        elif status == 'ativo':
            query = query.filter(EnderecoEstoque.ativo.is_(True))
        elif status == 'inativo':
            query = query.filter(EnderecoEstoque.ativo.is_(False))

        pagination = query.options(
            load_only(
                EnderecoEstoque.id,
                EnderecoEstoque.estoque_id,
                EnderecoEstoque.nome,
                EnderecoEstoque.codigo_localizacao,
                EnderecoEstoque.loja_cd,
                EnderecoEstoque.setor_zona,
                EnderecoEstoque.tipo_area,
                EnderecoEstoque.status,
                EnderecoEstoque.ativo,
            ),
            selectinload(EnderecoEstoque.estoque).load_only(Estoque.id, Estoque.nome),
        ).order_by(EnderecoEstoque.nome.asc()).paginate(page=page, per_page=per_page, error_out=False)
        enderecos = pagination.items
        estoques = _estoque_query_permitida(funcionario_logado).order_by(Estoque.nome.asc()).all()
        enderecos_stats = {}
        ids_endereco = [endereco.id for endereco in enderecos]
        if ids_endereco:
            stats_raw = db.session.query(
                Produto.endereco_id.label('endereco_id'),
                db.func.count(Produto.id).label('produtos'),
                db.func.sum(Produto.quantidade_estoque).label('unidades'),
                db.func.sum(Produto.quantidade_estoque * Produto.preco_custo).label('valor_total'),
            ).filter(
                Produto.endereco_id.in_(ids_endereco)
            ).group_by(
                Produto.endereco_id
            ).all()
            enderecos_stats = {
                int(item.endereco_id): {
                    'produtos': int(item.produtos or 0),
                    'unidades': int(item.unidades or 0),
                    'valor_total': float(item.valor_total or 0.0),
                }
                for item in stats_raw
            }
        return render_template(
            'estoque/enderecos/enderecos.html',
            enderecos=enderecos,
            estoques=estoques,
            enderecos_stats=enderecos_stats,
            pagination=pagination,
            per_page=per_page,
            filtros={
                'estoque_id': estoque_id,
                'setor_zona': setor_zona,
                'busca': busca,
                'status': status,
            },
            **endereco_context,
        )

    @app.route('/enderecos-estoque/<int:endereco_id>/detalhes')
    @login_required
    def detalhes_endereco_estoque(endereco_id):
        funcionario_logado = _funcionario_logado_estoque()
        endereco = _carregar_endereco_permitido(endereco_id, funcionario_logado)
        if not endereco:
            flash('Você não possui acesso a este endereço.', 'danger')
            return redirect(url_for('listar_enderecos_estoque'))
        produtos = _produto_query_permitida(Produto.query.filter_by(endereco_id=endereco.id), funcionario_logado).order_by(Produto.nome.asc()).all()
        total_unidades = sum(int(produto.quantidade_estoque or 0) for produto in produtos)
        valor_total = sum(float(produto.quantidade_estoque or 0) * float(produto.preco_custo or 0) for produto in produtos)
        return render_template(
            'estoque/enderecos/detalhes_endereco.html',
            endereco=endereco,
            produtos=produtos,
            total_unidades=total_unidades,
            valor_total=valor_total,
        )

    @app.route('/enderecos-estoque/<int:endereco_id>/etiqueta')
    @login_required
    def imprimir_etiqueta_endereco_estoque(endereco_id):
        empresa = _obter_empresa_config_estoque()
        if not _emissao_etiqueta_endereco_ativa(empresa):
            flash('A emissao de etiquetas de enderecos de estoque esta desativada na configuracao da empresa.', 'warning')
            return redirect(url_for('listar_enderecos_estoque'))
        funcionario_logado = _funcionario_logado_estoque()
        endereco = _carregar_endereco_permitido(endereco_id, funcionario_logado)
        if not endereco:
            flash('Você não possui acesso a este endereço.', 'danger')
            return redirect(url_for('listar_enderecos_estoque'))
        return render_template(
            'estoque/enderecos/etiquetas_enderecos.html',
            empresa=empresa,
            enderecos=[endereco],
            titulo='Etiqueta de Endereco',
        )

    @app.route('/enderecos-estoque/etiquetas')
    @login_required
    def imprimir_etiquetas_enderecos_estoque():
        empresa = _obter_empresa_config_estoque()
        if not _emissao_etiqueta_endereco_ativa(empresa):
            flash('A emissao de etiquetas de enderecos de estoque esta desativada na configuracao da empresa.', 'warning')
            return redirect(url_for('listar_enderecos_estoque'))
        funcionario_logado = _funcionario_logado_estoque()
        estoque_id = request.args.get('estoque_id', type=int)
        if estoque_id and not _carregar_estoque_permitido(estoque_id, funcionario_logado):
            flash('Você não possui acesso ao estoque selecionado.', 'warning')
            return redirect(url_for('listar_enderecos_estoque'))
        query = _endereco_query_permitida(funcionario_logado)
        if estoque_id:
            query = query.filter(EnderecoEstoque.estoque_id == estoque_id)
        enderecos = query.filter(EnderecoEstoque.ativo.is_(True)).order_by(EnderecoEstoque.nome.asc()).all()
        if not enderecos:
            flash('Nenhum endereco ativo encontrado para imprimir etiquetas.', 'warning')
            return redirect(url_for('listar_enderecos_estoque', estoque_id=estoque_id or ''))
        return render_template(
            'estoque/enderecos/etiquetas_enderecos.html',
            empresa=empresa,
            enderecos=enderecos,
            titulo='Etiquetas de Enderecos',
        )

    @app.route('/estoques')
    @login_required
    def listar_estoques():
        funcionario_logado = _funcionario_logado_estoque()
        page = max(request.args.get('page', 1, type=int), 1)
        per_page = min(max(request.args.get('per_page', 20, type=int), 1), 100)
        busca = (request.args.get('busca') or '').strip()
        status = (request.args.get('status') or '').strip().lower()

        query = _estoque_query_permitida(funcionario_logado)
        if busca:
            termo = f'%{busca}%'
            query = query.filter(
                db.or_(
                    Estoque.nome.ilike(termo),
                    Estoque.codigo_filial.ilike(termo),
                    Estoque.descricao.ilike(termo),
                )
            )
        if status == 'ativo':
            query = query.filter(Estoque.ativo.is_(True))
        elif status == 'inativo':
            query = query.filter(Estoque.ativo.is_(False))

        pagination = query.order_by(Estoque.nome.asc()).paginate(page=page, per_page=per_page, error_out=False)
        estoques = pagination.items
        return render_template(
            'estoque/estoques/estoques.html',
            estoques=estoques,
            pagination=pagination,
            per_page=per_page,
            filtros={
                'busca': busca,
                'status': status,
            }
        )

    @app.route('/estoques/novo', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def novo_estoque():
        if request.method == 'POST':
            try:
                nome = (request.form.get('nome') or '').strip()
                codigo_filial = re.sub(r'[^A-Z0-9]+', '', (request.form.get('codigo_filial') or '').strip().upper()) or None
                descricao = (request.form.get('descricao') or '').strip() or None
                ativo = (request.form.get('ativo') == 'on')

                if not nome:
                    flash('Nome do estoque e obrigatorio.', 'error')
                    return redirect(url_for('novo_estoque'))
                if codigo_filial and Estoque.query.filter(db.func.lower(Estoque.codigo_filial) == codigo_filial.lower()).first():
                    flash('Codigo de filial ja utilizado por outro estoque.', 'error')
                    return redirect(url_for('novo_estoque'))

                estoque = Estoque(nome=nome, codigo_filial=codigo_filial, descricao=descricao, ativo=ativo)
                db.session.add(estoque)
                db.session.commit()
                if sincronizar_matriculas_funcionarios:
                    sincronizar_matriculas_funcionarios()
                flash(f'Estoque "{estoque.nome}" criado com sucesso!', 'success')
                return redirect(url_for('listar_estoques'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao criar estoque: {str(e)}', 'error')
        return render_template('estoque/estoques/novo_estoque.html')

    @app.route('/estoques/<int:estoque_id>/editar', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def editar_estoque(estoque_id):
        funcionario_logado = _funcionario_logado_estoque()
        estoque = _carregar_estoque_permitido(estoque_id, funcionario_logado)
        if not estoque:
            flash('Você não possui acesso a este estoque.', 'danger')
            return redirect(url_for('listar_estoques'))
        if request.method == 'POST':
            try:
                nome = (request.form.get('nome') or '').strip()
                codigo_filial = re.sub(r'[^A-Z0-9]+', '', (request.form.get('codigo_filial') or '').strip().upper()) or None
                descricao = (request.form.get('descricao') or '').strip() or None
                ativo = (request.form.get('ativo') == 'on')
                if not nome:
                    flash('Nome do estoque e obrigatorio.', 'error')
                    return redirect(url_for('editar_estoque', estoque_id=estoque.id))
                duplicado = Estoque.query.filter(
                    db.func.lower(Estoque.codigo_filial) == (codigo_filial.lower() if codigo_filial else ''),
                    Estoque.id != estoque.id,
                ).first() if codigo_filial else None
                if duplicado:
                    flash('Codigo de filial ja utilizado por outro estoque.', 'error')
                    return redirect(url_for('editar_estoque', estoque_id=estoque.id))

                estoque.nome = nome
                estoque.codigo_filial = codigo_filial
                estoque.descricao = descricao
                estoque.ativo = ativo
                db.session.commit()
                if sincronizar_matriculas_funcionarios:
                    sincronizar_matriculas_funcionarios()
                flash('Estoque atualizado com sucesso!', 'success')
                return redirect(url_for('listar_estoques'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao atualizar estoque: {str(e)}', 'error')
        return render_template('estoque/estoques/editar_estoque.html', estoque=estoque)

    @app.route('/estoques/<int:estoque_id>/deletar', methods=['POST'])
    @require_role(*estoque_write_roles)
    def deletar_estoque(estoque_id):
        funcionario_logado = _funcionario_logado_estoque()
        estoque = _carregar_estoque_permitido(estoque_id, funcionario_logado)
        if not estoque:
            flash('Você não possui acesso a este estoque.', 'danger')
            return redirect(url_for('listar_estoques'))
        try:
            if EnderecoEstoque.query.filter_by(estoque_id=estoque.id).count() > 0:
                flash('Nao e possivel excluir estoque com enderecos vinculados.', 'error')
                return redirect(url_for('listar_estoques'))
            if Funcionario.query.filter(
                db.or_(
                    Funcionario.estoque_principal_id == estoque.id,
                    Funcionario.estoques_permitidos.any(Estoque.id == estoque.id),
                )
            ).count() > 0:
                flash('Nao e possivel excluir estoque vinculado a colaboradores.', 'error')
                return redirect(url_for('listar_estoques'))
            db.session.delete(estoque)
            db.session.commit()
            flash('Estoque removido com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao remover estoque: {str(e)}', 'error')
        return redirect(url_for('listar_estoques'))

    @app.route('/enderecos-estoque/novo', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def novo_endereco_estoque():
        funcionario_logado = _funcionario_logado_estoque()
        estoques_ativos = _estoque_query_permitida(funcionario_logado).filter_by(ativo=True).order_by(Estoque.nome.asc()).all()
        categorias = Categoria.query.order_by(Categoria.nome.asc()).all()
        if request.method == 'POST':
            try:
                estoque_id = request.form.get('estoque_id', type=int) or None
                categoria_reservada_id = request.form.get('tipo_produto_reservado_categoria_id', type=int)
                nome = (request.form.get('nome') or '').strip()
                cadastrar_lote_rack = (request.form.get('cadastrar_lote_rack') == 'on')
                payload_validacao = request.form.copy()
                tipo_estrutura_form = (request.form.get('tipo_estrutura') or '').strip().lower()
                if cadastrar_lote_rack and tipo_estrutura_form == 'rack':
                    # Permite lote mesmo quando nivel/vao unitarios nao forem informados.
                    nivel_inicial_tmp = request.form.get('lote_nivel_inicial', type=int)
                    vao_inicial_tmp = request.form.get('lote_vao_inicial', type=int)
                    if not payload_validacao.get('nivel_prateleira') and nivel_inicial_tmp is not None:
                        payload_validacao['nivel_prateleira'] = str(nivel_inicial_tmp)
                    if not payload_validacao.get('posicao_slot') and vao_inicial_tmp is not None:
                        payload_validacao['posicao_slot'] = str(vao_inicial_tmp)

                comp = validar_endereco_supermercado_payload(payload_validacao)
                codigo_localizacao = comp['codigo_localizacao']
                if not nome:
                    flash('Nome do endereco e obrigatorio.', 'error')
                    return redirect(url_for('novo_endereco_estoque'))
                if not estoque_id:
                    flash('Selecione um estoque para o endereco.', 'error')
                    return redirect(url_for('novo_endereco_estoque'))
                estoque = _carregar_estoque_permitido(estoque_id, funcionario_logado, apenas_ativo=True)
                if not estoque:
                    flash('Estoque informado e invalido ou nao esta liberado para este colaborador.', 'error')
                    return redirect(url_for('novo_endereco_estoque'))
                categoria_reservada = None
                if categoria_reservada_id:
                    categoria_reservada = Categoria.query.get(categoria_reservada_id)
                    if not categoria_reservada:
                        flash('Categoria de produto reservado invalida.', 'error')
                        return redirect(url_for('novo_endereco_estoque'))
                tipo_produto_reservado_valor = (
                    categoria_reservada.nome
                    if categoria_reservada
                    else (comp.get('tipo_produto_reservado') or None)
                )

                # Cadastro em lote de endereco apenas para estrutura rack
                if cadastrar_lote_rack and comp['tipo_estrutura'] == 'rack':
                    nivel_inicial = request.form.get('lote_nivel_inicial', type=int)
                    nivel_final = request.form.get('lote_nivel_final', type=int)
                    vao_inicial = request.form.get('lote_vao_inicial', type=int)
                    vao_final = request.form.get('lote_vao_final', type=int)
                    if None in (nivel_inicial, nivel_final, vao_inicial, vao_final):
                        flash('Preencha nivel inicial/final e vao inicial/final para cadastro em lote.', 'error')
                        return redirect(url_for('novo_endereco_estoque'))
                    if nivel_inicial < 0 or vao_inicial < 1:
                        flash('Intervalo invalido. Nivel deve iniciar em 0+ e vao em 1+.', 'error')
                        return redirect(url_for('novo_endereco_estoque'))
                    if nivel_final < nivel_inicial or vao_final < vao_inicial:
                        flash('Intervalo invalido. Valores finais devem ser maiores ou iguais aos iniciais.', 'error')
                        return redirect(url_for('novo_endereco_estoque'))

                    combinacoes = []
                    for nivel in range(nivel_inicial, nivel_final + 1):
                        for vao in range(vao_inicial, vao_final + 1):
                            combinacoes.append((nivel, vao))
                    if not combinacoes:
                        flash('Nenhuma combinacao valida para gerar enderecos.', 'error')
                        return redirect(url_for('novo_endereco_estoque'))
                    if len(combinacoes) > 400:
                        flash('Limite excedido. Gere no maximo 400 enderecos por lote.', 'error')
                        return redirect(url_for('novo_endereco_estoque'))

                    codigos_gerados = []
                    nomes_gerados = []
                    for nivel, vao in combinacoes:
                        codigos_gerados.append(
                            gerar_codigo_localizacao_supermercado(
                                loja_cd=comp['loja_cd'],
                                setor_zona=comp['setor_zona'],
                                tipo_estrutura='rack',
                                rua_corredor=comp['rua_corredor'],
                                rack_estante=comp['coluna_baia'],
                                nivel_prateleira=str(nivel),
                                posicao_slot=str(vao),
                                lado=comp['lado'],
                            )
                        )
                        nomes_gerados.append(f'{nome} N{nivel:02d} V{vao:02d}')

                    duplicado_codigo = EnderecoEstoque.query.filter(
                        EnderecoEstoque.codigo_localizacao.in_(codigos_gerados)
                    ).first()
                    if duplicado_codigo:
                        flash(
                            f'Ja existe endereco com codigo "{duplicado_codigo.codigo_localizacao}". '
                            'Ajuste o intervalo informado.',
                            'error'
                        )
                        return redirect(url_for('novo_endereco_estoque'))

                    duplicado_nome = EnderecoEstoque.query.filter(
                        EnderecoEstoque.nome.in_(nomes_gerados)
                    ).first()
                    if duplicado_nome:
                        flash(
                            f'Ja existe endereco com nome "{duplicado_nome.nome}". '
                            'Use outro nome base para o lote.',
                            'error'
                        )
                        return redirect(url_for('novo_endereco_estoque'))

                    novos_enderecos = []
                    for idx, (nivel, vao) in enumerate(combinacoes):
                        novos_enderecos.append(
                            EnderecoEstoque(
                                estoque_id=estoque.id,
                                nome=nomes_gerados[idx],
                                codigo_localizacao=codigos_gerados[idx],
                                loja_cd=comp['loja_cd'],
                                setor_zona=comp['setor_zona'],
                                tipo_area=comp['tipo_area'],
                                status=comp['status'],
                                descricao=comp['descricao'],
                                observacoes=comp['observacoes'],
                                tipo_estrutura='rack',
                                codigo_armazem=comp['codigo_armazem'],
                                rua_corredor=comp['rua_corredor'],
                                coluna_baia=comp['coluna_baia'],
                                nivel_prateleira=f'{nivel:02d}',
                                posicao_slot=f'{vao:02d}',
                                lado=comp['lado'],
                                ponto_local=None,
                                permite_fracionado=comp['permite_fracionado'],
                                permite_mistura_sku=comp['permite_mistura_sku'],
                                permite_mistura_lote=comp['permite_mistura_lote'],
                                controle_validade=comp['controle_validade'],
                                temperatura=comp['temperatura'],
                                restricoes=comp['restricoes'],
                                capacidade_caixas=comp['capacidade_caixas'],
                                capacidade_fardos=comp['capacidade_fardos'],
                                capacidade_unidades=comp['capacidade_unidades'],
                                capacidade_pallets=comp['capacidade_pallets'],
                                peso_max_kg=comp['peso_max_kg'],
                                volume_max_m3=comp['volume_max_m3'],
                                prioridade_picking=comp['prioridade_picking'],
                                tipo_produto_reservado=tipo_produto_reservado_valor,
                                sku_produto=comp['sku_produto'],
                                data_alocacao=datetime.utcnow(),
                                tipo_endereco=comp['tipo_endereco'],
                                rua=(request.form.get('rua') or '').strip() or None,
                                numero=(request.form.get('numero') or '').strip() or None,
                                bairro=(request.form.get('bairro') or '').strip() or None,
                                cidade=(request.form.get('cidade') or '').strip() or None,
                                estado=((request.form.get('estado') or '').strip().upper() or None),
                                cep=(request.form.get('cep') or '').strip() or None,
                                complemento=(request.form.get('complemento') or '').strip() or None,
                                ativo=(comp['status'] != 'bloqueado')
                            )
                        )
                    db.session.add_all(novos_enderecos)
                    db.session.commit()
                    flash(f'{len(novos_enderecos)} enderecos cadastrados com sucesso para o rack/estante.', 'success')
                    return redirect(url_for('listar_enderecos_estoque'))

                if codigo_localizacao and EnderecoEstoque.query.filter_by(codigo_localizacao=codigo_localizacao).first():
                    flash(f'Codigo de localizacao "{codigo_localizacao}" ja cadastrado.', 'error')
                    return redirect(url_for('novo_endereco_estoque'))
                if comp['tipo_estrutura'] == 'rack':
                    duplicado = EnderecoEstoque.query.filter_by(
                        codigo_armazem=comp['codigo_armazem'],
                        rua_corredor=comp['rua_corredor'],
                        coluna_baia=comp['coluna_baia'],
                        nivel_prateleira=comp['nivel_prateleira'],
                        posicao_slot=comp['posicao_slot'],
                    ).first()
                    if duplicado:
                        flash('Ja existe um endereco com os mesmos componentes (armazem/corredor/baia/nivel/slot).', 'error')
                        return redirect(url_for('novo_endereco_estoque'))

                endereco = EnderecoEstoque(
                    estoque_id=estoque.id,
                    nome=nome,
                    codigo_localizacao=codigo_localizacao,
                    loja_cd=comp['loja_cd'],
                    setor_zona=comp['setor_zona'],
                    tipo_area=comp['tipo_area'],
                    status=comp['status'],
                    descricao=comp['descricao'],
                    observacoes=comp['observacoes'],
                    tipo_estrutura=comp['tipo_estrutura'],
                    codigo_armazem=comp['codigo_armazem'],
                    rua_corredor=comp['rua_corredor'],
                    coluna_baia=comp['coluna_baia'],
                    nivel_prateleira=comp['nivel_prateleira'],
                    posicao_slot=comp['posicao_slot'],
                    lado=comp['lado'],
                    ponto_local=comp['ponto_local'],
                    permite_fracionado=comp['permite_fracionado'],
                    permite_mistura_sku=comp['permite_mistura_sku'],
                    permite_mistura_lote=comp['permite_mistura_lote'],
                    controle_validade=comp['controle_validade'],
                    temperatura=comp['temperatura'],
                    restricoes=comp['restricoes'],
                    capacidade_caixas=comp['capacidade_caixas'],
                    capacidade_fardos=comp['capacidade_fardos'],
                    capacidade_unidades=comp['capacidade_unidades'],
                    capacidade_pallets=comp['capacidade_pallets'],
                    peso_max_kg=comp['peso_max_kg'],
                    volume_max_m3=comp['volume_max_m3'],
                    prioridade_picking=comp['prioridade_picking'],
                    tipo_produto_reservado=tipo_produto_reservado_valor,
                    sku_produto=comp['sku_produto'],
                    data_alocacao=datetime.utcnow(),
                    tipo_endereco=comp['tipo_endereco'],
                    rua=(request.form.get('rua') or '').strip() or None,
                    numero=(request.form.get('numero') or '').strip() or None,
                    bairro=(request.form.get('bairro') or '').strip() or None,
                    cidade=(request.form.get('cidade') or '').strip() or None,
                    estado=((request.form.get('estado') or '').strip().upper() or None),
                    cep=(request.form.get('cep') or '').strip() or None,
                    complemento=(request.form.get('complemento') or '').strip() or None,
                    ativo=(comp['status'] != 'bloqueado')
                )
                db.session.add(endereco)
                db.session.commit()
                flash(f'Endereco "{endereco.nome}" cadastrado com sucesso!', 'success')
                return redirect(url_for('listar_enderecos_estoque'))
            except ValueError as e:
                db.session.rollback()
                flash(str(e), 'error')
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao cadastrar endereco: {str(e)}', 'error')
        return render_template(
            'estoque/enderecos/novo_endereco.html',
            estoques=estoques_ativos,
            categorias=categorias,
            **endereco_context
        )

    @app.route('/enderecos-estoque/<int:endereco_id>/editar', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def editar_endereco_estoque(endereco_id):
        funcionario_logado = _funcionario_logado_estoque()
        endereco = _carregar_endereco_permitido(endereco_id, funcionario_logado)
        if not endereco:
            flash('Você não possui acesso a este endereço.', 'danger')
            return redirect(url_for('listar_enderecos_estoque'))
        estoques_ativos = _estoque_query_permitida(funcionario_logado).filter_by(ativo=True).order_by(Estoque.nome.asc()).all()
        categorias = Categoria.query.order_by(Categoria.nome.asc()).all()
        if request.method == 'POST':
            try:
                estoque_id = request.form.get('estoque_id', type=int) or None
                categoria_reservada_id = request.form.get('tipo_produto_reservado_categoria_id', type=int)
                nome = (request.form.get('nome') or '').strip()
                comp = validar_endereco_supermercado_payload(request.form)
                codigo_localizacao = comp['codigo_localizacao']
                if not nome:
                    flash('Nome do endereco e obrigatorio.', 'error')
                    return redirect(url_for('editar_endereco_estoque', endereco_id=endereco_id))
                if not estoque_id:
                    flash('Selecione um estoque para o endereco.', 'error')
                    return redirect(url_for('editar_endereco_estoque', endereco_id=endereco_id))
                estoque = _carregar_estoque_permitido(estoque_id, funcionario_logado, apenas_ativo=True)
                if not estoque:
                    flash('Estoque informado e invalido ou nao esta liberado para este colaborador.', 'error')
                    return redirect(url_for('editar_endereco_estoque', endereco_id=endereco_id))
                if not categoria_reservada_id:
                    flash('Selecione uma categoria para o tipo de produto reservado.', 'error')
                    return redirect(url_for('editar_endereco_estoque', endereco_id=endereco_id))
                categoria_reservada = Categoria.query.get(categoria_reservada_id)
                if not categoria_reservada:
                    flash('Categoria de produto reservado invalida.', 'error')
                    return redirect(url_for('editar_endereco_estoque', endereco_id=endereco_id))
                if codigo_localizacao:
                    endereco_existente = EnderecoEstoque.query.filter_by(codigo_localizacao=codigo_localizacao).first()
                    if endereco_existente and endereco_existente.id != endereco.id:
                        flash(f'Codigo de localizacao "{codigo_localizacao}" ja cadastrado.', 'error')
                        return redirect(url_for('editar_endereco_estoque', endereco_id=endereco_id))
                if comp['tipo_estrutura'] == 'rack':
                    duplicado = EnderecoEstoque.query.filter_by(
                        codigo_armazem=comp['codigo_armazem'],
                        rua_corredor=comp['rua_corredor'],
                        coluna_baia=comp['coluna_baia'],
                        nivel_prateleira=comp['nivel_prateleira'],
                        posicao_slot=comp['posicao_slot'],
                    ).first()
                    if duplicado and duplicado.id != endereco.id:
                        flash('Ja existe um endereco com os mesmos componentes (armazem/corredor/baia/nivel/slot).', 'error')
                        return redirect(url_for('editar_endereco_estoque', endereco_id=endereco_id))

                endereco.estoque_id = estoque.id
                endereco.nome = nome
                endereco.codigo_localizacao = codigo_localizacao
                endereco.loja_cd = comp['loja_cd']
                endereco.setor_zona = comp['setor_zona']
                endereco.tipo_area = comp['tipo_area']
                endereco.status = comp['status']
                endereco.descricao = comp['descricao']
                endereco.observacoes = comp['observacoes']
                endereco.tipo_estrutura = comp['tipo_estrutura']
                endereco.codigo_armazem = comp['codigo_armazem']
                endereco.rua_corredor = comp['rua_corredor']
                endereco.coluna_baia = comp['coluna_baia']
                endereco.nivel_prateleira = comp['nivel_prateleira']
                endereco.posicao_slot = comp['posicao_slot']
                endereco.lado = comp['lado']
                endereco.ponto_local = comp['ponto_local']
                endereco.permite_fracionado = comp['permite_fracionado']
                endereco.permite_mistura_sku = comp['permite_mistura_sku']
                endereco.permite_mistura_lote = comp['permite_mistura_lote']
                endereco.controle_validade = comp['controle_validade']
                endereco.temperatura = comp['temperatura']
                endereco.restricoes = comp['restricoes']
                endereco.capacidade_caixas = comp['capacidade_caixas']
                endereco.capacidade_fardos = comp['capacidade_fardos']
                endereco.capacidade_unidades = comp['capacidade_unidades']
                endereco.capacidade_pallets = comp['capacidade_pallets']
                endereco.peso_max_kg = comp['peso_max_kg']
                endereco.volume_max_m3 = comp['volume_max_m3']
                endereco.prioridade_picking = comp['prioridade_picking']
                endereco.tipo_produto_reservado = categoria_reservada.nome
                endereco.sku_produto = comp['sku_produto']
                endereco.tipo_endereco = comp['tipo_endereco']
                endereco.rua = (request.form.get('rua') or '').strip() or None
                endereco.numero = (request.form.get('numero') or '').strip() or None
                endereco.bairro = (request.form.get('bairro') or '').strip() or None
                endereco.cidade = (request.form.get('cidade') or '').strip() or None
                endereco.estado = ((request.form.get('estado') or '').strip().upper() or None)
                endereco.cep = (request.form.get('cep') or '').strip() or None
                endereco.complemento = (request.form.get('complemento') or '').strip() or None
                endereco.ativo = (comp['status'] != 'bloqueado')
                db.session.commit()
                flash('Endereco atualizado com sucesso!', 'success')
                return redirect(url_for('listar_enderecos_estoque'))
            except ValueError as e:
                db.session.rollback()
                flash(str(e), 'error')
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao atualizar endereco: {str(e)}', 'error')
        return render_template(
            'estoque/enderecos/editar_endereco.html',
            endereco=endereco,
            estoques=estoques_ativos,
            categorias=categorias,
            **endereco_context
        )

    @app.route('/enderecos-estoque/<int:endereco_id>/deletar', methods=['POST'])
    @require_role(*estoque_write_roles)
    def deletar_endereco_estoque(endereco_id):
        funcionario_logado = _funcionario_logado_estoque()
        endereco = _carregar_endereco_permitido(endereco_id, funcionario_logado)
        if not endereco:
            flash('Você não possui acesso a este endereço.', 'danger')
            return redirect(url_for('listar_enderecos_estoque'))
        try:
            Produto.query.filter_by(endereco_id=endereco.id).update({'endereco_id': None})
            db.session.delete(endereco)
            db.session.commit()
            flash('Endereco removido com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao remover endereco: {str(e)}', 'error')
        return redirect(url_for('listar_enderecos_estoque'))

    @app.route('/movimentacoes/rapido/<int:produto_id>', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def movimentacao_rapida(produto_id):
        funcionario_logado = _funcionario_logado_estoque()
        produto = Produto.query.get_or_404(produto_id)
        if not _produto_em_estoque_permitido(produto, funcionario_logado):
            flash('Você não possui acesso ao estoque deste produto.', 'danger')
            return redirect(url_for('listar_movimentacoes'))
        if request.method == 'POST':
            try:
                tipo = request.form.get('tipo')
                quantidade = int(request.form.get('quantidade'))
                fornecedor_id = request.form.get('fornecedor_id', type=int)
                recebimento_fornecedor = (request.form.get('recebimento_fornecedor') == 'on')

                if tipo not in {Movimentacao.TIPO_ENTRADA, Movimentacao.TIPO_SAIDA}:
                    flash('Tipo de movimentacao invalido.', 'error')
                    return redirect(url_for('movimentacao_rapida', produto_id=produto_id))

                aplicar_movimentacao_estoque(produto, tipo, quantidade)

                fornecedor = None
                if tipo == Movimentacao.TIPO_ENTRADA and fornecedor_id:
                    fornecedor = Fornecedor.query.get(fornecedor_id)
                    if not fornecedor:
                        flash('Fornecedor invalido.', 'error')
                        return redirect(url_for('movimentacao_rapida', produto_id=produto_id))
                if tipo == Movimentacao.TIPO_ENTRADA and recebimento_fornecedor and not fornecedor:
                    flash('No recebimento de fornecedor, selecione o fornecedor.', 'error')
                    return redirect(url_for('movimentacao_rapida', produto_id=produto_id))

                motivo = request.form.get('motivo')
                if tipo == Movimentacao.TIPO_ENTRADA and recebimento_fornecedor and not motivo:
                    motivo = 'recebimento_fornecedor'

                movimentacao = Movimentacao(
                    produto_id=produto_id,
                    fornecedor_id=(fornecedor.id if fornecedor else None),
                    tipo=tipo,
                    quantidade=quantidade,
                    valor_compra=request.form.get('valor_compra', type=float),
                    info_nota=request.form.get('info_nota'),
                    motivo=motivo,
                    observacoes=request.form.get('observacoes'),
                    endereco_origem_id=(produto.endereco_id if tipo == Movimentacao.TIPO_SAIDA else None),
                    endereco_destino_id=(produto.endereco_id if tipo == Movimentacao.TIPO_ENTRADA else None),
                )
                db.session.add(movimentacao)
                db.session.commit()
                flash('Movimentacao registrada com sucesso!', 'success')
                return redirect(url_for('listar_movimentacoes'))
            except AppError as e:
                db.session.rollback()
                flash(str(e), 'error')
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao registrar movimentacao: {str(e)}', 'error')

        return render_template(
            'estoque/movimentacoes/movimentacao_rapida.html',
            produto=produto,
            motivos_sugeridos=motivos_movimentacao_interna,
        )

    @app.route('/movimentacoes')
    @login_required
    def listar_movimentacoes():
        funcionario_logado = _funcionario_logado_estoque()
        page = max(request.args.get('page', 1, type=int), 1)
        per_page = min(max(request.args.get('per_page', 25, type=int), 1), 100)
        produto_id = request.args.get('produto_id', type=int)
        status = (request.args.get('status') or request.args.get('tipo') or '').strip().lower()
        busca = (request.args.get('busca') or '').strip()
        data_inicio_txt = (request.args.get('data_inicio') or '').strip()
        data_fim_txt = (request.args.get('data_fim') or '').strip()
        data_inicio = _parse_data_filtro(data_inicio_txt)
        data_fim = _parse_data_filtro(data_fim_txt)

        query = _movimentacao_query_permitida(Movimentacao.query, funcionario_logado).filter(
            Movimentacao.tipo.in_([Movimentacao.TIPO_ENTRADA, Movimentacao.TIPO_SAIDA])
        )
        if produto_id:
            query = query.filter_by(produto_id=produto_id)
        if status and status in [Movimentacao.TIPO_ENTRADA, Movimentacao.TIPO_SAIDA]:
            query = query.filter_by(tipo=status)
        if data_inicio:
            query = query.filter(Movimentacao.criado_em >= data_inicio)
        if data_fim:
            query = query.filter(Movimentacao.criado_em < (data_fim + timedelta(days=1)))
        if busca:
            termo = f'%{busca}%'
            query = query.join(Produto, Produto.id == Movimentacao.produto_id).outerjoin(
                Fornecedor, Fornecedor.id == Movimentacao.fornecedor_id
            ).filter(
                db.or_(
                    Produto.nome.ilike(termo),
                    Produto.codigo.ilike(termo),
                    Movimentacao.motivo.ilike(termo),
                    Movimentacao.info_nota.ilike(termo),
                    Movimentacao.observacoes.ilike(termo),
                    Fornecedor.nome.ilike(termo),
                )
            )

        movimentacoes = query.options(
            load_only(
                Movimentacao.id,
                Movimentacao.produto_id,
                Movimentacao.fornecedor_id,
                Movimentacao.tipo,
                Movimentacao.quantidade,
                Movimentacao.valor_compra,
                Movimentacao.info_nota,
                Movimentacao.motivo,
                Movimentacao.observacoes,
                Movimentacao.criado_em,
            ),
            selectinload(Movimentacao.produto).load_only(
                Produto.id,
                Produto.nome,
                Produto.codigo,
                Produto.endereco_id,
            ),
            selectinload(Movimentacao.fornecedor).load_only(
                Fornecedor.id,
                Fornecedor.nome,
            )
        ).order_by(Movimentacao.criado_em.desc()).paginate(page=page, per_page=per_page, error_out=False)
        produtos = _produto_query_permitida(Produto.query, funcionario_logado).all()
        return render_template(
            'estoque/movimentacoes/movimentacoes.html',
            movimentacoes=movimentacoes.items,
            pagination=movimentacoes,
            per_page=per_page,
            produtos=produtos,
            produto_selecionado=produto_id,
            status_selecionado=status,
            busca=busca,
            data_inicio=data_inicio_txt,
            data_fim=data_fim_txt,
            query_params=request.args.to_dict()
        )

    @app.route('/movimentacoes/nova', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def nova_movimentacao():
        funcionario_logado = _funcionario_logado_estoque()
        if request.method == 'POST':
            try:
                produto_id = int(request.form.get('produto_id'))
                tipo = request.form.get('tipo')
                quantidade = int(request.form.get('quantidade'))
                fornecedor_id = request.form.get('fornecedor_id', type=int)
                recebimento_fornecedor = (request.form.get('recebimento_fornecedor') == 'on')

                if tipo not in {Movimentacao.TIPO_ENTRADA, Movimentacao.TIPO_SAIDA}:
                    flash('Tipo de movimentacao invalido.', 'error')
                    return redirect(url_for('nova_movimentacao'))

                produto = Produto.query.get(produto_id)
                if not produto:
                    flash('Produto nao encontrado', 'error')
                    return redirect(url_for('nova_movimentacao'))
                if not _produto_em_estoque_permitido(produto, funcionario_logado):
                    flash('Você não possui acesso ao estoque deste produto.', 'danger')
                    return redirect(url_for('nova_movimentacao'))

                aplicar_movimentacao_estoque(produto, tipo, quantidade)

                fornecedor = None
                if tipo == Movimentacao.TIPO_ENTRADA and fornecedor_id:
                    fornecedor = Fornecedor.query.get(fornecedor_id)
                    if not fornecedor:
                        flash('Fornecedor invalido.', 'error')
                        return redirect(url_for('nova_movimentacao'))
                if tipo == Movimentacao.TIPO_ENTRADA and recebimento_fornecedor and not fornecedor:
                    flash('No recebimento de fornecedor, selecione o fornecedor.', 'error')
                    return redirect(url_for('nova_movimentacao'))

                motivo = request.form.get('motivo')
                if tipo == Movimentacao.TIPO_ENTRADA and recebimento_fornecedor and not motivo:
                    motivo = 'recebimento_fornecedor'

                movimentacao = Movimentacao(
                    produto_id=produto_id,
                    fornecedor_id=(fornecedor.id if fornecedor else None),
                    tipo=tipo,
                    quantidade=quantidade,
                    valor_compra=request.form.get('valor_compra', type=float),
                    info_nota=request.form.get('info_nota'),
                    motivo=motivo,
                    observacoes=request.form.get('observacoes'),
                    endereco_origem_id=(produto.endereco_id if tipo == Movimentacao.TIPO_SAIDA else None),
                    endereco_destino_id=(produto.endereco_id if tipo == Movimentacao.TIPO_ENTRADA else None),
                )
                db.session.add(movimentacao)
                db.session.commit()
                flash('Movimentacao registrada com sucesso!', 'success')
                return redirect(url_for('listar_movimentacoes'))
            except AppError as e:
                db.session.rollback()
                flash(str(e), 'error')
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao registrar movimentacao: {str(e)}', 'error')

        produtos = _produto_query_permitida(Produto.query.filter_by(ativo=True), funcionario_logado).all()
        return render_template(
            'estoque/movimentacoes/nova_movimentacao.html',
            produtos=produtos,
            motivos_sugeridos=motivos_movimentacao_interna,
        )

    @app.route('/movimentacoes/transferencias')
    @login_required
    def listar_transferencias_estoque():
        funcionario_logado = _funcionario_logado_estoque()
        page = max(request.args.get('page', 1, type=int), 1)
        per_page = min(max(request.args.get('per_page', 25, type=int), 1), 100)
        produto_id = request.args.get('produto_id', type=int)
        busca = (request.args.get('busca') or '').strip()
        data_inicio_txt = (request.args.get('data_inicio') or '').strip()
        data_fim_txt = (request.args.get('data_fim') or '').strip()
        data_inicio = _parse_data_filtro(data_inicio_txt)
        data_fim = _parse_data_filtro(data_fim_txt)

        query = _movimentacao_query_permitida(Movimentacao.query, funcionario_logado).filter(
            Movimentacao.tipo == Movimentacao.TIPO_TRANSFERENCIA
        )
        if produto_id:
            query = query.filter(Movimentacao.produto_id == produto_id)
        if data_inicio:
            query = query.filter(Movimentacao.criado_em >= data_inicio)
        if data_fim:
            query = query.filter(Movimentacao.criado_em < (data_fim + timedelta(days=1)))
        if busca:
            termo = f'%{busca}%'
            query = query.join(Produto, Produto.id == Movimentacao.produto_id).filter(
                db.or_(
                    Produto.nome.ilike(termo),
                    Produto.codigo.ilike(termo),
                    Movimentacao.motivo.ilike(termo),
                    Movimentacao.observacoes.ilike(termo),
                )
            )

        transferencias = query.options(
            selectinload(Movimentacao.produto),
            selectinload(Movimentacao.endereco_origem).selectinload(EnderecoEstoque.estoque),
            selectinload(Movimentacao.endereco_destino).selectinload(EnderecoEstoque.estoque),
        ).order_by(Movimentacao.criado_em.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False,
        )
        produtos = _produto_query_permitida(Produto.query, funcionario_logado).order_by(Produto.nome.asc()).all()
        return render_template(
            'estoque/movimentacoes/transferencias.html',
            transferencias=transferencias.items,
            pagination=transferencias,
            per_page=per_page,
            produtos=produtos,
            produto_selecionado=produto_id,
            busca=busca,
            data_inicio=data_inicio_txt,
            data_fim=data_fim_txt,
            query_params=request.args.to_dict(),
        )

    @app.route('/movimentacoes/transferencia', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def transferir_armazenamento():
        funcionario_logado = _funcionario_logado_estoque()
        if request.method == 'POST':
            try:
                produto_id = request.form.get('produto_id', type=int)
                endereco_destino_id = request.form.get('endereco_destino_id', type=int)
                motivo = (request.form.get('motivo') or '').strip() or 'transferencia_armazenamento'
                observacoes = (request.form.get('observacoes') or '').strip() or None

                produto = Produto.query.get(produto_id)
                if not produto:
                    flash('Produto nao encontrado.', 'error')
                    return redirect(url_for('transferir_armazenamento'))
                if not _produto_em_estoque_permitido(produto, funcionario_logado):
                    flash('Você não possui acesso ao estoque deste produto.', 'danger')
                    return redirect(url_for('transferir_armazenamento'))
                if not produto.endereco_id:
                    flash('Produto sem endereco de origem para transferencia.', 'error')
                    return redirect(url_for('transferir_armazenamento'))

                endereco_origem = _carregar_endereco_permitido(produto.endereco_id, funcionario_logado)
                endereco_destino = _carregar_endereco_permitido(endereco_destino_id, funcionario_logado, apenas_ativo=True)
                if not endereco_destino:
                    flash('Endereco de destino invalido.', 'error')
                    return redirect(url_for('transferir_armazenamento'))
                if not endereco_origem:
                    flash('Origem da transferencia nao localizada.', 'error')
                    return redirect(url_for('transferir_armazenamento'))
                if endereco_origem and endereco_origem.id == endereco_destino.id:
                    flash('Origem e destino nao podem ser iguais.', 'error')
                    return redirect(url_for('transferir_armazenamento'))
                if (
                    endereco_origem.estoque_id
                    and endereco_destino.estoque_id
                    and endereco_origem.estoque_id == endereco_destino.estoque_id
                ):
                    flash(
                        'Esta tela e exclusiva para transferencias entre lojas/CDs. '
                        'Para ajustes internos use Entradas e Saidas Internas ou Enderecos Inteligentes.',
                        'warning'
                    )
                    return redirect(url_for('transferir_armazenamento'))

                produto.endereco_id = endereco_destino.id
                movimentacao = Movimentacao(
                    produto_id=produto.id,
                    tipo=Movimentacao.TIPO_TRANSFERENCIA,
                    quantidade=max(int(produto.quantidade_estoque or 0), 0),
                    motivo=motivo,
                    observacoes=observacoes,
                    endereco_origem_id=(endereco_origem.id if endereco_origem else None),
                    endereco_destino_id=endereco_destino.id,
                )
                db.session.add(movimentacao)
                db.session.commit()
                flash(
                    f'Transferencia concluida: produto "{produto.nome}" movido para "{endereco_destino.nome}".',
                    'success'
                )
                return redirect(url_for('listar_transferencias_estoque'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao transferir armazenamento: {str(e)}', 'error')

        produtos = _produto_query_permitida(
            Produto.query.options(
                selectinload(Produto.endereco).selectinload(EnderecoEstoque.estoque),
                selectinload(Produto.categoria),
            ).filter(
                Produto.ativo.is_(True),
                Produto.endereco_id.isnot(None)
            ),
            funcionario_logado,
        ).order_by(Produto.nome.asc()).all()
        enderecos = _endereco_query_permitida(funcionario_logado).options(
            selectinload(EnderecoEstoque.estoque),
        ).filter_by(ativo=True).order_by(EnderecoEstoque.nome.asc()).all()
        return render_template(
            'estoque/movimentacoes/transferencia_armazenamento.html',
            produtos=produtos,
            enderecos=enderecos,
            motivos_sugeridos=motivos_transferencia,
        )

    @app.route('/api/estoque/analytics')
    @login_required
    def analytics_estoque_api():
        funcionario_logado = _funcionario_logado_estoque()
        periodo = request.args.get('periodo', type=int) or 30
        if periodo not in {7, 30, 90}:
            periodo = 30
        cache = extensions.cache
        funcionario_id = getattr(funcionario_logado, 'id', 'anon')
        cache_key = f'analytics:estoque:{funcionario_id}:{periodo}'
        if cache is not None:
            cached_payload = cache.get(cache_key)
            if cached_payload is not None:
                return jsonify(cached_payload)

        data_limite = datetime.utcnow() - timedelta(days=periodo)
        movimentos_raw = _movimentacao_query_permitida(db.session.query(
            db.func.date(Movimentacao.criado_em).label('dia'),
            Movimentacao.tipo.label('tipo'),
            db.func.sum(Movimentacao.quantidade).label('quantidade')
        ), funcionario_logado).filter(
            Movimentacao.criado_em >= data_limite
        ).group_by(
            db.func.date(Movimentacao.criado_em),
            Movimentacao.tipo
        ).order_by(db.func.date(Movimentacao.criado_em).asc()).all()

        entradas_por_dia = {}
        saidas_por_dia = {}
        for item in movimentos_raw:
            dia = str(item.dia)
            qtd = int(item.quantidade or 0)
            if item.tipo == Movimentacao.TIPO_ENTRADA:
                entradas_por_dia[dia] = entradas_por_dia.get(dia, 0) + qtd
            elif item.tipo == Movimentacao.TIPO_SAIDA:
                saidas_por_dia[dia] = saidas_por_dia.get(dia, 0) + qtd

        dias = []
        for i in range(periodo):
            dia = (datetime.utcnow() - timedelta(days=(periodo - i - 1))).date()
            key = str(dia)
            dias.append({
                'dia': key,
                'entradas': entradas_por_dia.get(key, 0),
                'saidas': saidas_por_dia.get(key, 0),
            })

        valor_categoria_raw = _produto_query_permitida(db.session.query(
            Categoria.nome.label('categoria_nome'),
            db.func.sum(Produto.quantidade_estoque * Produto.preco_custo).label('valor_total')
        ).join(Produto, Produto.categoria_id == Categoria.id), funcionario_logado).filter(
            Produto.ativo == True
        ).group_by(Categoria.id, Categoria.nome).order_by(db.desc('valor_total')).all()

        payload = {
            'success': True,
            'message': 'Analytics de estoque carregado com sucesso.',
            'data': {
                'periodo_dias': periodo,
                'movimentacao_diaria': dias,
                'valor_por_categoria': [
                    {
                        'categoria': item.categoria_nome,
                        'valor_total': float(item.valor_total or 0)
                    }
                    for item in valor_categoria_raw
                ],
                'produtos_em_falta': _produto_query_permitida(Produto.query, funcionario_logado).filter(
                    Produto.quantidade_estoque < Produto.quantidade_minima,
                    Produto.ativo == True
                ).count(),
                'produtos_sem_estoque': _produto_query_permitida(Produto.query, funcionario_logado).filter(
                    Produto.ativo == True,
                    Produto.quantidade_estoque <= 0
                ).count()
            }
        }
        if cache is not None:
            cache.set(cache_key, payload, timeout=120)
        return jsonify(payload)

    @app.route('/relatorios')
    @login_required
    def relatorios():
        empresa = _obter_empresa_config_estoque()
        funcionario_logado = _funcionario_logado_estoque()
        total_produtos = _produto_query_permitida(Produto.query, funcionario_logado).count()
        produtos_ativos = _produto_query_permitida(Produto.query, funcionario_logado).filter_by(ativo=True).count()
        produtos_inativos = _produto_query_permitida(Produto.query, funcionario_logado).filter_by(ativo=False).count()
        total_unidades = _produto_query_permitida(
            db.session.query(db.func.sum(Produto.quantidade_estoque)),
            funcionario_logado,
        ).scalar() or 0

        produtos_em_falta = _produto_query_permitida(Produto.query, funcionario_logado).filter(
            Produto.quantidade_estoque < Produto.quantidade_minima,
            Produto.ativo == True
        ).all()
        produtos_sem_estoque = _produto_query_permitida(Produto.query, funcionario_logado).filter(
            Produto.ativo == True,
            Produto.quantidade_estoque <= 0
        ).count()

        valor_total = _produto_query_permitida(db.session.query(
            db.func.sum(Produto.quantidade_estoque * Produto.preco_custo)
        ), funcionario_logado).scalar() or 0
        custo_medio_estoque = (valor_total / total_unidades) if total_unidades else 0

        produtos_maior_valor = _produto_query_permitida(db.session.query(
            Produto,
            (Produto.quantidade_estoque * Produto.preco_custo).label('valor_total')
        ), funcionario_logado).order_by(db.desc('valor_total')).limit(10).all()

        data_limite = datetime.utcnow() - timedelta(days=30)
        movimentacoes_mes = _movimentacao_query_permitida(Movimentacao.query, funcionario_logado).filter(Movimentacao.criado_em >= data_limite).count()
        entradas_mes = _movimentacao_query_permitida(Movimentacao.query, funcionario_logado).filter(
            Movimentacao.criado_em >= data_limite,
            Movimentacao.tipo == Movimentacao.TIPO_ENTRADA
        ).count()
        saidas_mes = _movimentacao_query_permitida(Movimentacao.query, funcionario_logado).filter(
            Movimentacao.criado_em >= data_limite,
            Movimentacao.tipo == Movimentacao.TIPO_SAIDA
        ).count()
        saldo_movimentacao_mes = int(entradas_mes or 0) - int(saidas_mes or 0)

        data_sem_giro = datetime.utcnow() - timedelta(days=60)
        produtos_sem_giro = _produto_query_permitida(Produto.query, funcionario_logado).filter(
            Produto.ativo == True,
            ~Produto.movimentacoes.any(Movimentacao.criado_em >= data_sem_giro)
        ).order_by(Produto.nome.asc()).limit(10).all()

        valor_por_categoria = _produto_query_permitida(db.session.query(
            Categoria.nome.label('categoria_nome'),
            db.func.sum(Produto.quantidade_estoque * Produto.preco_custo).label('valor_total'),
            db.func.sum(Produto.quantidade_estoque).label('qtd_total'),
            db.func.count(Produto.id).label('produtos')
        ).join(Produto, Produto.categoria_id == Categoria.id), funcionario_logado).filter(
            Produto.ativo == True
        ).group_by(Categoria.id, Categoria.nome).order_by(
            db.desc('valor_total')
        ).all()

        valor_por_endereco = _endereco_query_permitida(funcionario_logado).with_entities(
            EnderecoEstoque.nome.label('endereco_nome'),
            db.func.count(Produto.id).label('produtos'),
            db.func.sum(Produto.quantidade_estoque).label('qtd_total'),
            db.func.sum(Produto.quantidade_estoque * Produto.preco_custo).label('valor_total')
        ).join(Produto, Produto.endereco_id == EnderecoEstoque.id).filter(
            Produto.ativo == True
        ).group_by(EnderecoEstoque.id, EnderecoEstoque.nome).order_by(
            db.desc('valor_total')
        ).all()

        total_enderecos_ativos = _endereco_query_permitida(funcionario_logado).filter_by(ativo=True).count()
        enderecos_ocupados = _endereco_query_permitida(funcionario_logado).with_entities(EnderecoEstoque.id).join(
            Produto, Produto.endereco_id == EnderecoEstoque.id
        ).filter(
            EnderecoEstoque.ativo == True,
            Produto.ativo == True
        ).distinct().count()
        taxa_ocupacao_enderecos = (
            (enderecos_ocupados / total_enderecos_ativos) * 100.0
            if total_enderecos_ativos > 0 else 0.0
        )

        produtos_ativos_total = max(int(produtos_ativos or 0), 1)
        taxa_reposicao_necessaria = (len(produtos_em_falta) / produtos_ativos_total) * 100.0

        produtos_sem_endereco = _produto_query_permitida(Produto.query, funcionario_logado).filter(
            Produto.ativo == True,
            Produto.endereco_id.is_(None)
        ).count()
        produtos_fora_picking = _produto_query_permitida(Produto.query, funcionario_logado).filter(
            Produto.ativo == True,
            Produto.fora_picking.is_(True)
        ).count()
        produtos_risco_ruptura = _produto_query_permitida(Produto.query, funcionario_logado).filter(
            Produto.ativo == True,
            Produto.quantidade_minima > 0,
            Produto.quantidade_estoque <= 0
        ).count()

        risco_operacional_score = 0
        risco_operacional_score += min(int(taxa_reposicao_necessaria // 5), 8)
        risco_operacional_score += min(int((produtos_sem_endereco / produtos_ativos_total) * 10), 5)
        risco_operacional_score += min(int((produtos_fora_picking / produtos_ativos_total) * 10), 4)
        risco_operacional_score += min(int((produtos_risco_ruptura / produtos_ativos_total) * 12), 8)
        risco_operacional_score = min(risco_operacional_score, 25)

        dicas_estoque_inteligente = []
        if taxa_ocupacao_enderecos > 90:
            dicas_estoque_inteligente.append(
                'Ocupacao alta de enderecos. Priorize consolidacao de SKUs e abertura de novos slots de picking.'
            )
        elif taxa_ocupacao_enderecos < 55 and total_enderecos_ativos > 0:
            dicas_estoque_inteligente.append(
                'Ocupacao baixa de enderecos. Reorganize para reduzir deslocamento operacional e concentrar picking.'
            )

        if taxa_reposicao_necessaria >= 18:
            dicas_estoque_inteligente.append(
                'Reposicao elevada. Programe janelas fixas de reabastecimento e revise minimo por curva ABC.'
            )

        if produtos_sem_endereco > 0:
            dicas_estoque_inteligente.append(
                f'{produtos_sem_endereco} produto(s) sem endereco. Enderece para evitar ruptura e retrabalho no coletor.'
            )

        if produtos_fora_picking > 0:
            dicas_estoque_inteligente.append(
                f'{produtos_fora_picking} produto(s) fora de picking. Use "enderecos inteligentes" para baixar ao fluxo.'
            )

        if produtos_sem_giro:
            dicas_estoque_inteligente.append(
                'Existem produtos sem giro em 60 dias. Reavalie ponto de estocagem, promocao ou descontinuidade.'
            )

        if saldo_movimentacao_mes < 0:
            dicas_estoque_inteligente.append(
                'Saidas maiores que entradas no periodo. Reforce compras e agenda de recebimento para itens criticos.'
            )

        if not dicas_estoque_inteligente:
            dicas_estoque_inteligente.append(
                'Operacao equilibrada. Mantenha rotina de reposicao preventiva e revisao semanal por endereco.'
            )

        return render_template(
            'estoque/relatorios/relatorios.html',
            empresa=empresa,
            total_produtos=total_produtos,
            produtos_ativos=produtos_ativos,
            produtos_inativos=produtos_inativos,
            total_unidades=total_unidades,
            produtos_em_falta=produtos_em_falta,
            produtos_sem_estoque=produtos_sem_estoque,
            valor_total_estoque=f'{valor_total:.2f}',
            custo_medio_estoque=f'{custo_medio_estoque:.2f}',
            produtos_maior_valor=produtos_maior_valor,
            movimentacoes_mes=movimentacoes_mes,
            entradas_mes=entradas_mes,
            saidas_mes=saidas_mes,
            saldo_movimentacao_mes=saldo_movimentacao_mes,
            produtos_sem_giro=produtos_sem_giro,
            valor_por_categoria=valor_por_categoria,
            valor_por_endereco=valor_por_endereco,
            total_enderecos_ativos=total_enderecos_ativos,
            enderecos_ocupados=enderecos_ocupados,
            taxa_ocupacao_enderecos=taxa_ocupacao_enderecos,
            taxa_reposicao_necessaria=taxa_reposicao_necessaria,
            produtos_sem_endereco=produtos_sem_endereco,
            produtos_fora_picking=produtos_fora_picking,
            produtos_risco_ruptura=produtos_risco_ruptura,
            risco_operacional_score=risco_operacional_score,
            dicas_estoque_inteligente=dicas_estoque_inteligente,
        )

