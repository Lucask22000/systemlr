import os
import re
import uuid

from flask import current_app
from PIL import Image

try:
    import magic
except Exception:  # pragma: no cover - fallback quando python-magic nao estiver disponivel
    magic = None

from app.exceptions import BusinessRuleError, ValidationError
from app.services.operational_rules import validate_stock_movement_payload, validate_stock_transfer_payload
from app.services.traceability import record_process_event
from app.services.transaction import atomic_transaction
from app.utils.helpers import sem_acentos
from app.utils.validators import normalizar_codigo_barras
from models import EmpresaConfig, Movimentacao, Produto, db


ALLOWED_IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp', '.gif'}
ALLOWED_IMAGE_MIME_TYPES = {'image/jpeg', 'image/png', 'image/webp', 'image/gif'}
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


def registrar_movimentacao_manual(
    *,
    produto,
    tipo,
    quantidade,
    motivo,
    recebimento_fornecedor=False,
    fornecedor=None,
    valor_compra=None,
    info_nota=None,
    observacoes=None,
    movimentacao_model=Movimentacao,
    failure_hook=None,
    actor=None,
    pedido_id=None,
    recebimento_id=None,
):
    with atomic_transaction():
        motivo_normalizado = validate_stock_movement_payload(
            tipo=tipo,
            quantidade=quantidade,
            motivo=motivo,
            recebimento_fornecedor=recebimento_fornecedor,
        )
        aplicar_movimentacao_estoque(produto, tipo, quantidade, movimentacao_model=movimentacao_model)
        if failure_hook:
            failure_hook('after_stock')

        movimentacao = movimentacao_model(
            produto_id=produto.id,
            pedido_id=pedido_id,
            recebimento_id=recebimento_id,
            fornecedor_id=(fornecedor.id if fornecedor else None),
            tipo=tipo,
            quantidade=quantidade,
            valor_compra=valor_compra,
            info_nota=info_nota,
            motivo=motivo_normalizado,
            observacoes=observacoes,
            endereco_origem_id=(produto.endereco_id if tipo == movimentacao_model.TIPO_SAIDA else None),
            endereco_destino_id=(produto.endereco_id if tipo == movimentacao_model.TIPO_ENTRADA else None),
        )
        db.session.add(movimentacao)
        db.session.flush()
        record_process_event(
            processo_tipo='estoque',
            etapa='movimentacao',
            acao='movimentacao_manual_registrada',
            entidade='movimentacao',
            entidade_id=movimentacao.id,
            pedido_id=pedido_id,
            recebimento_id=recebimento_id,
            movimentacao_id=movimentacao.id,
            actor=actor,
            detalhes={
                'produto_id': produto.id,
                'tipo': tipo,
                'quantidade': quantidade,
                'motivo': motivo_normalizado,
            },
        )
    return movimentacao


def transferir_estoque(
    *,
    produto,
    endereco_origem,
    endereco_destino,
    motivo,
    observacoes=None,
    allow_same_stock=False,
    movimentacao_model=Movimentacao,
    failure_hook=None,
    actor=None,
):
    with atomic_transaction():
        validate_stock_transfer_payload(
            produto=produto,
            endereco_origem=endereco_origem,
            endereco_destino=endereco_destino,
            motivo=motivo,
        )
        if (
            not allow_same_stock
            and endereco_origem.estoque_id
            and endereco_destino.estoque_id
            and endereco_origem.estoque_id == endereco_destino.estoque_id
        ):
            raise BusinessRuleError(
                'Esta tela e exclusiva para transferencias entre lojas/CDs. '
                'Para ajustes internos use Entradas e Saidas Internas ou Enderecos Inteligentes.'
            )

        produto.endereco_id = endereco_destino.id
        if failure_hook:
            failure_hook('after_address')
        movimentacao = movimentacao_model(
            produto_id=produto.id,
            tipo=movimentacao_model.TIPO_TRANSFERENCIA,
            quantidade=max(int(produto.quantidade_estoque or 0), 0),
            motivo=(motivo or '').strip(),
            observacoes=observacoes,
            endereco_origem_id=(endereco_origem.id if endereco_origem else None),
            endereco_destino_id=endereco_destino.id,
        )
        db.session.add(movimentacao)
        db.session.flush()
        record_process_event(
            processo_tipo='estoque',
            etapa='transferencia',
            acao='transferencia_registrada',
            entidade='movimentacao',
            entidade_id=movimentacao.id,
            movimentacao_id=movimentacao.id,
            actor=actor,
            detalhes={
                'produto_id': produto.id,
                'endereco_origem_id': endereco_origem.id if endereco_origem else None,
                'endereco_destino_id': endereco_destino.id,
                'quantidade': movimentacao.quantidade,
                'motivo': movimentacao.motivo,
            },
        )
    return movimentacao


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
        header = stream.read(2048)
        stream.seek(0)
        if magic is not None:
            mime_type = magic.from_buffer(header, mime=True)
            if mime_type not in ALLOWED_IMAGE_MIME_TYPES:
                return False
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
