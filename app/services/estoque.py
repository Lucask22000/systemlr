import os
import re
import uuid

from flask import current_app
from PIL import Image

from app.exceptions import BusinessRuleError, ValidationError
from app.utils.helpers import sem_acentos
from app.utils.validators import normalizar_codigo_barras
from models import EmpresaConfig, Movimentacao, Produto


ALLOWED_IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp', '.gif'}
DEFAULT_PRODUCT_IMAGE = 'img/placeholders/imgindisponivel.png'


def aplicar_movimentacao_estoque(produto, tipo, quantidade, *, tipos_validos=None, movimentacao_model=Movimentacao):
    tipos_validos = set(tipos_validos or {
        movimentacao_model.TIPO_ENTRADA,
        movimentacao_model.TIPO_SAIDA,
        movimentacao_model.TIPO_TRANSFERENCIA,
    })
    if tipo not in tipos_validos:
        return 'Tipo de movimentação inválido'

    if quantidade <= 0:
        return 'Quantidade deve ser maior que 0'

    if tipo == movimentacao_model.TIPO_ENTRADA:
        produto.quantidade_estoque += quantidade
        return None

    if produto.quantidade_estoque < quantidade:
        return 'Quantidade em estoque insuficiente'

    produto.quantidade_estoque -= quantidade
    return None


def _normalizar_codigo_barras(valor):
    return normalizar_codigo_barras(valor)


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

    image_path = os.path.normpath(os.path.join(current_app.static_folder, relative_path))
    static_root = os.path.normpath(current_app.static_folder)
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
    absolute_dir = os.path.join(current_app.static_folder, relative_dir)
    os.makedirs(absolute_dir, exist_ok=True)
    relative_path = os.path.join(relative_dir, image_name).replace('\\', '/')
    absolute_path = os.path.join(current_app.static_folder, relative_path)

    file_storage.save(absolute_path)
    _optimize_image_file(absolute_path)
    return relative_path, None


def categoria_parece_quimico(produto):
    categoria_nome = ''
    if getattr(produto, 'categoria', None):
        categoria_nome = produto.categoria.nome or ''
    texto = sem_acentos(categoria_nome).strip().lower()
    return bool(texto and re.search(r'quim', texto))


def aplicar_movimentacao_estoque(produto, tipo, quantidade, *, tipos_validos=None, movimentacao_model=Movimentacao):
    tipos_validos = set(tipos_validos or {
        movimentacao_model.TIPO_ENTRADA,
        movimentacao_model.TIPO_SAIDA,
        movimentacao_model.TIPO_TRANSFERENCIA,
    })
    if tipo not in tipos_validos:
        raise ValidationError('Tipo de movimentacao invalido.')

    if quantidade <= 0:
        raise ValidationError('Quantidade deve ser maior que 0.')

    if tipo == movimentacao_model.TIPO_ENTRADA:
        produto.quantidade_estoque += quantidade
        return None

    if produto.quantidade_estoque < quantidade:
        raise BusinessRuleError('Quantidade em estoque insuficiente.')

    produto.quantidade_estoque -= quantidade
    return None
