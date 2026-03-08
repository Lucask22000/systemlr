from datetime import datetime, timedelta
import os
import re
import unicodedata
import uuid

from sqlalchemy.orm import selectinload

from flask import render_template, request, redirect, url_for, flash, jsonify

from models import (
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
DEFAULT_PRODUCT_IMAGE = 'img/placeholders/produto-sem-foto.svg'


def register_estoque_routes(app, login_required, require_role, aplicar_movimentacao_estoque):
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
    recebimento_status_labels = {
        RecebimentoFornecedor.STATUS_CRIADO: 'Criado',
        RecebimentoFornecedor.STATUS_AGUARDANDO_ARMAZENAGEM: 'Aguardando armazenagem',
        RecebimentoFornecedor.STATUS_CONCLUIDO: 'Concluido',
        RecebimentoFornecedor.STATUS_CANCELADO: 'Cancelado',
    }

    def _normalizar_status_disponibilidade(valor):
        return Produto.normalizar_status_disponibilidade(valor)

    def _sem_acentos(texto):
        base = unicodedata.normalize('NFKD', str(texto or ''))
        return ''.join(c for c in base if not unicodedata.combining(c))

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

    def _aplicar_filtros_produtos(
        query,
        *,
        categoria_id=None,
        busca='',
        status_disponibilidade='',
        estoque_id=None,
        endereco_id=None,
        fornecedor_id=None,
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
        status = (status_disponibilidade or '').strip().lower()
        if status in Produto.STATUS_DISPONIBILIDADE_ONLINE_EQUIVALENTES:
            query = query.filter(Produto.status_disponibilidade.in_(Produto.STATUS_DISPONIBILIDADE_ONLINE_EQUIVALENTES))
        elif status in Produto.STATUS_DISPONIBILIDADE_OFF_EQUIVALENTES:
            query = query.filter(Produto.status_disponibilidade.in_(Produto.STATUS_DISPONIBILIDADE_OFF_EQUIVALENTES))
        if endereco_id:
            query = query.filter(Produto.endereco_id == endereco_id)
        if fornecedor_id:
            query = query.filter(Produto.fornecedor_id == fornecedor_id)
        if estoque_id:
            query = query.join(EnderecoEstoque, Produto.endereco_id == EnderecoEstoque.id).filter(
                EnderecoEstoque.estoque_id == estoque_id
            )
        return query
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
        page = max(request.args.get('page', 1, type=int), 1)
        per_page = min(max(request.args.get('per_page', 20, type=int), 1), 100)
        categoria_id = request.args.get('categoria_id', type=int)
        busca = (request.args.get('busca') or '').strip()
        status_disponibilidade = (request.args.get('status_disponibilidade') or '').strip().lower()
        estoque_id = request.args.get('estoque_id', type=int)
        endereco_id = request.args.get('endereco_id', type=int)
        fornecedor_id = request.args.get('fornecedor_id', type=int)

        query = _aplicar_filtros_produtos(
            Produto.query,
            categoria_id=categoria_id,
            busca=busca,
            status_disponibilidade=status_disponibilidade,
            estoque_id=estoque_id,
            endereco_id=endereco_id,
            fornecedor_id=fornecedor_id,
        ).options(
            selectinload(Produto.categoria),
            selectinload(Produto.endereco),
            selectinload(Produto.fornecedor),
        )

        pagination = query.order_by(Produto.nome.asc()).paginate(page=page, per_page=per_page, error_out=False)
        produtos = pagination.items
        categorias = Categoria.query.order_by(Categoria.nome.asc()).all()
        enderecos = EnderecoEstoque.query.filter_by(ativo=True).order_by(EnderecoEstoque.nome.asc()).all()
        estoques = Estoque.query.filter_by(ativo=True).order_by(Estoque.nome.asc()).all()
        fornecedores = Fornecedor.query.filter_by(ativo=True).order_by(Fornecedor.nome.asc()).all()
        return render_template(
            'estoque/produtos/produtos.html',
            produtos=produtos,
            pagination=pagination,
            per_page=per_page,
            categorias=categorias,
            enderecos=enderecos,
            estoques=estoques,
            fornecedores=fornecedores,
            categoria_selecionada=categoria_id,
            busca=busca,
            filtros={
                'status_disponibilidade': status_disponibilidade,
                'estoque_id': estoque_id,
                'endereco_id': endereco_id,
                'fornecedor_id': fornecedor_id,
            },
            status_disponibilidade_labels=STATUS_DISPONIBILIDADE_LABELS,
            query_params=request.args.to_dict()
        )

    @app.route('/produtos/enderecos/armazenar-todos', methods=['POST'])
    @require_role(*estoque_write_roles)
    def armazenar_todos_produtos_enderecos():
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

            estoque = Estoque.query.get(estoque_id)
            if not estoque:
                flash('Estoque informado nao existe.', 'error')
                return redirect(url_for(
                    'listar_produtos',
                    categoria_id=categoria_id or '',
                    busca=busca,
                    status_disponibilidade=status_disponibilidade,
                    estoque_id=filtro_estoque_id or '',
                    endereco_id=filtro_endereco_id or '',
                ))

            enderecos = EnderecoEstoque.query.filter_by(
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
                Produto.query.order_by(Produto.id.asc()),
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

                codigo_raw = (request.form.get('codigo') or '').strip()
                codigo_barras = re.sub(r'\D', '', codigo_raw)
                if len(codigo_barras) not in {8, 12, 13, 14}:
                    flash('Codigo/SKU deve ser um codigo de barras numerico (8, 12, 13 ou 14 digitos).', 'error')
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
                    endereco_id=request.form.get('endereco_id', type=int) or None,
                    preco_custo=float(request.form.get('preco_custo', 0)),
                    preco_venda=float(request.form.get('preco_venda', 0)),
                    quantidade_estoque=int(request.form.get('quantidade_estoque', 0)),
                    quantidade_minima=int(request.form.get('quantidade_minima', 5)),
                    status_disponibilidade=_normalizar_status_disponibilidade(request.form.get('status_disponibilidade'))
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
        fornecedores = Fornecedor.query.filter_by(ativo=True).order_by(Fornecedor.nome.asc()).all()
        enderecos = EnderecoEstoque.query.filter_by(ativo=True).order_by(EnderecoEstoque.nome.asc()).all()
        return render_template(
            'estoque/produtos/novo_produto.html',
            categorias=categorias,
            fornecedores=fornecedores,
            enderecos=enderecos,
            status_disponibilidade_labels=STATUS_DISPONIBILIDADE_LABELS,
            codigos_existentes=[c[0] for c in db.session.query(Produto.codigo).all()]
        )

    @app.route('/produtos/<int:produto_id>/editar', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def editar_produto(produto_id):
        produto = Produto.query.get_or_404(produto_id)
        if request.method == 'POST':
            nova_imagem_path = None
            imagem_anterior = produto.imagem_path
            try:
                fornecedor_id = request.form.get('fornecedor_id', type=int)
                fornecedor = Fornecedor.query.get(fornecedor_id) if fornecedor_id else None
                if not fornecedor:
                    flash('Fornecedor invalido. Selecione um fornecedor para o produto.', 'error')
                    return redirect(url_for('editar_produto', produto_id=produto_id))
                produto.nome = request.form.get('nome')
                produto.descricao = request.form.get('descricao')
                produto.categoria_id = int(request.form.get('categoria_id'))
                produto.fornecedor_id = fornecedor.id
                produto.endereco_id = request.form.get('endereco_id', type=int) or None
                preco_custo_raw = request.form.get('preco_custo')
                if preco_custo_raw is not None and str(preco_custo_raw).strip() != '':
                    produto.preco_custo = float(preco_custo_raw)

                preco_venda_raw = request.form.get('preco_venda')
                if preco_venda_raw is not None and str(preco_venda_raw).strip() != '':
                    produto.preco_venda = float(preco_venda_raw)
                produto.quantidade_minima = int(request.form.get('quantidade_minima', 5))
                produto.status_disponibilidade = _normalizar_status_disponibilidade(request.form.get('status_disponibilidade'))

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
        fornecedores = Fornecedor.query.filter_by(ativo=True).order_by(Fornecedor.nome.asc()).all()
        enderecos = EnderecoEstoque.query.filter_by(ativo=True).order_by(EnderecoEstoque.nome.asc()).all()
        return render_template(
            'estoque/produtos/editar_produto.html',
            produto=produto,
            categorias=categorias,
            fornecedores=fornecedores,
            enderecos=enderecos,
            status_disponibilidade_labels=STATUS_DISPONIBILIDADE_LABELS,
            codigos_existentes=[c[0] for c in db.session.query(Produto.codigo).filter(Produto.id != produto.id).all()]
        )

    @app.route('/produtos/<int:produto_id>')
    @login_required
    def visualizar_produto(produto_id):
        produto = Produto.query.get_or_404(produto_id)
        movimentacoes = Movimentacao.query.filter_by(produto_id=produto_id).order_by(
            Movimentacao.criado_em.desc()
        ).all()
        return render_template('estoque/produtos/visualizar_produto.html', produto=produto, movimentacoes=movimentacoes)

    @app.route('/produtos/<int:produto_id>/deletar', methods=['POST'])
    @require_role(*estoque_write_roles)
    def deletar_produto(produto_id):
        produto = Produto.query.get_or_404(produto_id)
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
        fornecedor_id = request.args.get('fornecedor_id', type=int)
        busca = (request.args.get('busca') or '').strip()
        data_inicio_txt = (request.args.get('data_inicio') or '').strip()
        data_fim_txt = (request.args.get('data_fim') or '').strip()
        data_inicio = _parse_data_filtro(data_inicio_txt)
        data_fim = _parse_data_filtro(data_fim_txt)

        query = RecebimentoFornecedor.query
        if status in RecebimentoFornecedor.STATUS_VALIDOS:
            query = query.filter(RecebimentoFornecedor.status == status)
        if fornecedor_id:
            query = query.filter(RecebimentoFornecedor.fornecedor_id == fornecedor_id)
        if data_inicio:
            query = query.filter(RecebimentoFornecedor.criado_em >= data_inicio)
        if data_fim:
            query = query.filter(RecebimentoFornecedor.criado_em < (data_fim + timedelta(days=1)))
        if busca:
            termo = f'%{busca}%'
            query = query.outerjoin(Fornecedor, Fornecedor.id == RecebimentoFornecedor.fornecedor_id).outerjoin(
                RecebimentoItem, RecebimentoItem.recebimento_id == RecebimentoFornecedor.id
            ).outerjoin(
                Produto, Produto.id == RecebimentoItem.produto_id
            ).filter(
                db.or_(
                    Fornecedor.nome.ilike(termo),
                    RecebimentoFornecedor.info_nota.ilike(termo),
                    RecebimentoFornecedor.observacoes.ilike(termo),
                    Produto.nome.ilike(termo),
                    Produto.codigo.ilike(termo),
                    db.cast(RecebimentoFornecedor.id, db.String).ilike(termo),
                )
            ).distinct()

        recebimentos = query.options(
            selectinload(RecebimentoFornecedor.fornecedor),
            selectinload(RecebimentoFornecedor.itens).selectinload(RecebimentoItem.produto),
        ).order_by(RecebimentoFornecedor.criado_em.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False,
        )
        fornecedores = Fornecedor.query.filter_by(ativo=True).order_by(Fornecedor.nome.asc()).all()
        return render_template(
            'estoque/recebimentos/recebimentos.html',
            recebimentos=recebimentos.items,
            pagination=recebimentos,
            per_page=per_page,
            fornecedores=fornecedores,
            status_labels=recebimento_status_labels,
            filtros={
                'status': status,
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
        fornecedores = Fornecedor.query.filter_by(ativo=True).order_by(Fornecedor.nome.asc()).all()
        produtos = Produto.query.filter_by(ativo=True).order_by(Produto.nome.asc()).all()

        if request.method == 'POST':
            try:
                fornecedor_id = request.form.get('fornecedor_id', type=int)
                fornecedor = Fornecedor.query.get(fornecedor_id) if fornecedor_id else None
                if not fornecedor:
                    flash('Selecione um fornecedor valido.', 'error')
                    return redirect(url_for('novo_recebimento_fornecedor'))

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
                    fornecedor_documento=(request.form.get('fornecedor_documento') or '').strip() or None,
                    data_entrega=data_entrega,
                    info_nota=(request.form.get('info_nota') or '').strip() or None,
                    subtotal=subtotal,
                    desconto=desconto,
                    total_pagar=total_pagar,
                    observacoes=(request.form.get('observacoes') or '').strip() or None,
                    recebedor_nome=(request.form.get('recebedor_nome') or '').strip() or None,
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
        )

    @app.route('/estoque/recebimentos/<int:recebimento_id>/conferir', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def conferir_recebimento_fornecedor(recebimento_id):
        recebimento = RecebimentoFornecedor.query.options(
            selectinload(RecebimentoFornecedor.fornecedor),
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
        )

    @app.route('/estoque/recebimentos/<int:recebimento_id>/armazenar', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def armazenar_recebimento_fornecedor(recebimento_id):
        recebimento = RecebimentoFornecedor.query.options(
            selectinload(RecebimentoFornecedor.fornecedor),
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

        enderecos_ativos = EnderecoEstoque.query.filter(EnderecoEstoque.status == 'ativo').order_by(EnderecoEstoque.nome.asc()).all()
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

                    erro_mov = aplicar_movimentacao_estoque(item.produto, Movimentacao.TIPO_ENTRADA, quantidade_entrada)
                    if erro_mov:
                        raise ValueError(f'Falha ao aplicar entrada de "{item.produto.nome}": {erro_mov}')

                    item.produto.endereco_id = endereco_destino.id
                    observacoes_mov = f'Recebimento #{recebimento.id}'
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
                        motivo='recebimento_fornecedor',
                        observacoes=observacoes_mov,
                    )
                    db.session.add(movimentacao)

                recebimento.status = RecebimentoFornecedor.STATUS_CONCLUIDO
                recebimento.armazenado_em = datetime.utcnow()
                db.session.commit()
                flash('Armazenagem concluida. Estoque atualizado com sucesso.', 'success')
                return redirect(url_for('listar_recebimentos_fornecedor'))
            except ValueError as e:
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

    @app.route('/enderecos-estoque')
    @login_required
    def listar_enderecos_estoque():
        page = max(request.args.get('page', 1, type=int), 1)
        per_page = min(max(request.args.get('per_page', 25, type=int), 1), 100)
        estoque_id = request.args.get('estoque_id', type=int)
        setor_zona = (request.args.get('setor_zona') or '').strip().lower()
        busca = (request.args.get('busca') or '').strip()
        status = (request.args.get('status') or '').strip().lower()

        query = EnderecoEstoque.query
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

        pagination = query.order_by(EnderecoEstoque.nome.asc()).paginate(page=page, per_page=per_page, error_out=False)
        enderecos = pagination.items
        estoques = Estoque.query.order_by(Estoque.nome.asc()).all()
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
        endereco = EnderecoEstoque.query.get_or_404(endereco_id)
        produtos = Produto.query.filter_by(endereco_id=endereco.id).order_by(Produto.nome.asc()).all()
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
        endereco = EnderecoEstoque.query.get_or_404(endereco_id)
        return render_template(
            'estoque/enderecos/etiquetas_enderecos.html',
            enderecos=[endereco],
            titulo='Etiqueta de Endereco',
        )

    @app.route('/enderecos-estoque/etiquetas')
    @login_required
    def imprimir_etiquetas_enderecos_estoque():
        estoque_id = request.args.get('estoque_id', type=int)
        query = EnderecoEstoque.query
        if estoque_id:
            query = query.filter(EnderecoEstoque.estoque_id == estoque_id)
        enderecos = query.filter(EnderecoEstoque.ativo.is_(True)).order_by(EnderecoEstoque.nome.asc()).all()
        if not enderecos:
            flash('Nenhum endereco ativo encontrado para imprimir etiquetas.', 'warning')
            return redirect(url_for('listar_enderecos_estoque', estoque_id=estoque_id or ''))
        return render_template(
            'estoque/enderecos/etiquetas_enderecos.html',
            enderecos=enderecos,
            titulo='Etiquetas de Enderecos',
        )

    @app.route('/estoques')
    @login_required
    def listar_estoques():
        page = max(request.args.get('page', 1, type=int), 1)
        per_page = min(max(request.args.get('per_page', 20, type=int), 1), 100)
        busca = (request.args.get('busca') or '').strip()
        status = (request.args.get('status') or '').strip().lower()

        query = Estoque.query
        if busca:
            termo = f'%{busca}%'
            query = query.filter(
                db.or_(
                    Estoque.nome.ilike(termo),
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
                descricao = (request.form.get('descricao') or '').strip() or None
                ativo = (request.form.get('ativo') == 'on')

                if not nome:
                    flash('Nome do estoque e obrigatorio.', 'error')
                    return redirect(url_for('novo_estoque'))

                estoque = Estoque(nome=nome, descricao=descricao, ativo=ativo)
                db.session.add(estoque)
                db.session.commit()
                flash(f'Estoque "{estoque.nome}" criado com sucesso!', 'success')
                return redirect(url_for('listar_estoques'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao criar estoque: {str(e)}', 'error')
        return render_template('estoque/estoques/novo_estoque.html')

    @app.route('/estoques/<int:estoque_id>/editar', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def editar_estoque(estoque_id):
        estoque = Estoque.query.get_or_404(estoque_id)
        if request.method == 'POST':
            try:
                nome = (request.form.get('nome') or '').strip()
                descricao = (request.form.get('descricao') or '').strip() or None
                ativo = (request.form.get('ativo') == 'on')
                if not nome:
                    flash('Nome do estoque e obrigatorio.', 'error')
                    return redirect(url_for('editar_estoque', estoque_id=estoque.id))

                estoque.nome = nome
                estoque.descricao = descricao
                estoque.ativo = ativo
                db.session.commit()
                flash('Estoque atualizado com sucesso!', 'success')
                return redirect(url_for('listar_estoques'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao atualizar estoque: {str(e)}', 'error')
        return render_template('estoque/estoques/editar_estoque.html', estoque=estoque)

    @app.route('/estoques/<int:estoque_id>/deletar', methods=['POST'])
    @require_role(*estoque_write_roles)
    def deletar_estoque(estoque_id):
        estoque = Estoque.query.get_or_404(estoque_id)
        try:
            if EnderecoEstoque.query.filter_by(estoque_id=estoque.id).count() > 0:
                flash('Nao e possivel excluir estoque com enderecos vinculados.', 'error')
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
        estoques_ativos = Estoque.query.filter_by(ativo=True).order_by(Estoque.nome.asc()).all()
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
                estoque = Estoque.query.get(estoque_id)
                if not estoque:
                    flash('Estoque informado e invalido.', 'error')
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
        endereco = EnderecoEstoque.query.get_or_404(endereco_id)
        estoques_ativos = Estoque.query.filter_by(ativo=True).order_by(Estoque.nome.asc()).all()
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
                estoque = Estoque.query.get(estoque_id)
                if not estoque:
                    flash('Estoque informado e invalido.', 'error')
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
        endereco = EnderecoEstoque.query.get_or_404(endereco_id)
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
        produto = Produto.query.get_or_404(produto_id)
        if request.method == 'POST':
            try:
                tipo = request.form.get('tipo')
                quantidade = int(request.form.get('quantidade'))
                fornecedor_id = request.form.get('fornecedor_id', type=int)
                recebimento_fornecedor = (request.form.get('recebimento_fornecedor') == 'on')

                if tipo not in {Movimentacao.TIPO_ENTRADA, Movimentacao.TIPO_SAIDA}:
                    flash('Tipo de movimentacao invalido.', 'error')
                    return redirect(url_for('movimentacao_rapida', produto_id=produto_id))

                erro = aplicar_movimentacao_estoque(produto, tipo, quantidade)
                if erro:
                    flash(erro, 'error')
                    return redirect(url_for('movimentacao_rapida', produto_id=produto_id))

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
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao registrar movimentacao: {str(e)}', 'error')

        fornecedores = Fornecedor.query.filter_by(ativo=True).order_by(Fornecedor.nome.asc()).all()
        return render_template('estoque/movimentacoes/movimentacao_rapida.html', produto=produto, fornecedores=fornecedores)

    @app.route('/movimentacoes')
    @login_required
    def listar_movimentacoes():
        page = max(request.args.get('page', 1, type=int), 1)
        per_page = min(max(request.args.get('per_page', 25, type=int), 1), 100)
        produto_id = request.args.get('produto_id', type=int)
        status = (request.args.get('status') or request.args.get('tipo') or '').strip().lower()
        fornecedor_id = request.args.get('fornecedor_id', type=int)
        busca = (request.args.get('busca') or '').strip()
        data_inicio_txt = (request.args.get('data_inicio') or '').strip()
        data_fim_txt = (request.args.get('data_fim') or '').strip()
        data_inicio = _parse_data_filtro(data_inicio_txt)
        data_fim = _parse_data_filtro(data_fim_txt)

        query = Movimentacao.query
        if produto_id:
            query = query.filter_by(produto_id=produto_id)
        if status and status in [Movimentacao.TIPO_ENTRADA, Movimentacao.TIPO_SAIDA, Movimentacao.TIPO_TRANSFERENCIA]:
            query = query.filter_by(tipo=status)
        if fornecedor_id:
            query = query.filter(Movimentacao.fornecedor_id == fornecedor_id)
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
            selectinload(Movimentacao.produto),
            selectinload(Movimentacao.fornecedor)
        ).order_by(Movimentacao.criado_em.desc()).paginate(page=page, per_page=per_page, error_out=False)
        produtos = Produto.query.all()
        fornecedores = Fornecedor.query.filter_by(ativo=True).order_by(Fornecedor.nome.asc()).all()
        return render_template(
            'estoque/movimentacoes/movimentacoes.html',
            movimentacoes=movimentacoes.items,
            pagination=movimentacoes,
            per_page=per_page,
            produtos=produtos,
            fornecedores=fornecedores,
            produto_selecionado=produto_id,
            fornecedor_selecionado=fornecedor_id,
            status_selecionado=status,
            busca=busca,
            data_inicio=data_inicio_txt,
            data_fim=data_fim_txt,
            tipos_movimentacao=Movimentacao.TIPOS,
            query_params=request.args.to_dict()
        )

    @app.route('/movimentacoes/nova', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def nova_movimentacao():
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

                erro = aplicar_movimentacao_estoque(produto, tipo, quantidade)
                if erro:
                    flash(erro, 'error')
                    return redirect(url_for('nova_movimentacao'))

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
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao registrar movimentacao: {str(e)}', 'error')

        produtos = Produto.query.filter_by(ativo=True).all()
        fornecedores = Fornecedor.query.filter_by(ativo=True).order_by(Fornecedor.nome.asc()).all()
        return render_template('estoque/movimentacoes/nova_movimentacao.html', produtos=produtos, fornecedores=fornecedores)

    @app.route('/movimentacoes/transferencia', methods=['GET', 'POST'])
    @require_role(*estoque_write_roles)
    def transferir_armazenamento():
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
                if not produto.endereco_id:
                    flash('Produto sem endereco de origem para transferencia.', 'error')
                    return redirect(url_for('transferir_armazenamento'))

                endereco_origem = EnderecoEstoque.query.get(produto.endereco_id)
                endereco_destino = EnderecoEstoque.query.filter_by(id=endereco_destino_id, ativo=True).first()
                if not endereco_destino:
                    flash('Endereco de destino invalido.', 'error')
                    return redirect(url_for('transferir_armazenamento'))
                if endereco_origem and endereco_origem.id == endereco_destino.id:
                    flash('Origem e destino nao podem ser iguais.', 'error')
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
                return redirect(url_for('listar_movimentacoes'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao transferir armazenamento: {str(e)}', 'error')

        produtos = Produto.query.filter(
            Produto.ativo.is_(True),
            Produto.endereco_id.isnot(None)
        ).order_by(Produto.nome.asc()).all()
        enderecos = EnderecoEstoque.query.filter_by(ativo=True).order_by(EnderecoEstoque.nome.asc()).all()
        return render_template(
            'estoque/movimentacoes/transferencia_armazenamento.html',
            produtos=produtos,
            enderecos=enderecos
        )

    @app.route('/api/estoque/analytics')
    @login_required
    def analytics_estoque_api():
        periodo = request.args.get('periodo', type=int) or 30
        if periodo not in {7, 30, 90}:
            periodo = 30

        data_limite = datetime.utcnow() - timedelta(days=periodo)
        movimentos_raw = db.session.query(
            db.func.date(Movimentacao.criado_em).label('dia'),
            Movimentacao.tipo.label('tipo'),
            db.func.sum(Movimentacao.quantidade).label('quantidade')
        ).filter(
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

        valor_categoria_raw = db.session.query(
            Categoria.nome.label('categoria_nome'),
            db.func.sum(Produto.quantidade_estoque * Produto.preco_custo).label('valor_total')
        ).join(Produto, Produto.categoria_id == Categoria.id).filter(
            Produto.ativo == True
        ).group_by(Categoria.id, Categoria.nome).order_by(db.desc('valor_total')).all()

        return jsonify({
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
                'produtos_em_falta': Produto.query.filter(
                    Produto.quantidade_estoque < Produto.quantidade_minima,
                    Produto.ativo == True
                ).count(),
                'produtos_sem_estoque': Produto.query.filter(
                    Produto.ativo == True,
                    Produto.quantidade_estoque <= 0
                ).count()
            }
        })

    @app.route('/relatorios')
    @login_required
    def relatorios():
        total_produtos = Produto.query.count()
        produtos_ativos = Produto.query.filter_by(ativo=True).count()
        produtos_inativos = Produto.query.filter_by(ativo=False).count()
        total_unidades = db.session.query(db.func.sum(Produto.quantidade_estoque)).scalar() or 0

        produtos_em_falta = Produto.query.filter(
            Produto.quantidade_estoque < Produto.quantidade_minima,
            Produto.ativo == True
        ).all()
        produtos_sem_estoque = Produto.query.filter(
            Produto.ativo == True,
            Produto.quantidade_estoque <= 0
        ).count()

        valor_total = db.session.query(
            db.func.sum(Produto.quantidade_estoque * Produto.preco_custo)
        ).scalar() or 0
        custo_medio_estoque = (valor_total / total_unidades) if total_unidades else 0

        produtos_maior_valor = db.session.query(
            Produto,
            (Produto.quantidade_estoque * Produto.preco_custo).label('valor_total')
        ).order_by(db.desc('valor_total')).limit(10).all()

        data_limite = datetime.utcnow() - timedelta(days=30)
        movimentacoes_mes = Movimentacao.query.filter(Movimentacao.criado_em >= data_limite).count()
        entradas_mes = Movimentacao.query.filter(
            Movimentacao.criado_em >= data_limite,
            Movimentacao.tipo == Movimentacao.TIPO_ENTRADA
        ).count()
        saidas_mes = Movimentacao.query.filter(
            Movimentacao.criado_em >= data_limite,
            Movimentacao.tipo == Movimentacao.TIPO_SAIDA
        ).count()

        data_sem_giro = datetime.utcnow() - timedelta(days=60)
        produtos_sem_giro = Produto.query.filter(
            Produto.ativo == True,
            ~Produto.movimentacoes.any(Movimentacao.criado_em >= data_sem_giro)
        ).order_by(Produto.nome.asc()).limit(10).all()

        valor_por_categoria = db.session.query(
            Categoria.nome.label('categoria_nome'),
            db.func.sum(Produto.quantidade_estoque * Produto.preco_custo).label('valor_total'),
            db.func.sum(Produto.quantidade_estoque).label('qtd_total'),
            db.func.count(Produto.id).label('produtos')
        ).join(Produto, Produto.categoria_id == Categoria.id).filter(
            Produto.ativo == True
        ).group_by(Categoria.id, Categoria.nome).order_by(
            db.desc('valor_total')
        ).all()

        valor_por_endereco = db.session.query(
            EnderecoEstoque.nome.label('endereco_nome'),
            db.func.count(Produto.id).label('produtos'),
            db.func.sum(Produto.quantidade_estoque).label('qtd_total'),
            db.func.sum(Produto.quantidade_estoque * Produto.preco_custo).label('valor_total')
        ).join(Produto, Produto.endereco_id == EnderecoEstoque.id).filter(
            Produto.ativo == True
        ).group_by(EnderecoEstoque.id, EnderecoEstoque.nome).order_by(
            db.desc('valor_total')
        ).all()

        return render_template(
            'estoque/relatorios/relatorios.html',
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
            produtos_sem_giro=produtos_sem_giro,
            valor_por_categoria=valor_por_categoria,
            valor_por_endereco=valor_por_endereco
        )

