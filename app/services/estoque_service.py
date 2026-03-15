from app.services.estoque import (
    _delete_image_file,
    _normalizar_codigo_barras,
    _save_product_image,
    aplicar_movimentacao_estoque,
    categoria_parece_quimico,
)


normalizar_codigo_barras = _normalizar_codigo_barras
save_product_image = _save_product_image
delete_image_file = _delete_image_file


__all__ = [
    'aplicar_movimentacao_estoque',
    'categoria_parece_quimico',
    '_normalizar_codigo_barras',
    '_save_product_image',
    '_delete_image_file',
    'normalizar_codigo_barras',
    'save_product_image',
    'delete_image_file',
]
