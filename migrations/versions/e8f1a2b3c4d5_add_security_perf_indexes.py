"""add security and performance indexes

Revision ID: e8f1a2b3c4d5
Revises: d4e5f6a7b8c9
Create Date: 2026-03-27 20:10:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = 'e8f1a2b3c4d5'
down_revision = 'd4e5f6a7b8c9'
branch_labels = None
depends_on = None


def _inspector():
    return sa.inspect(op.get_bind())


def _indexes(table_name):
    if not _inspector().has_table(table_name):
        return set()
    return {idx['name'] for idx in _inspector().get_indexes(table_name)}


def _create_index_if_missing(table_name, index_name, columns, *, unique=False):
    if index_name not in _indexes(table_name):
        op.create_index(index_name, table_name, columns, unique=unique)


def upgrade():
    _create_index_if_missing('pedidos', 'ix_pedidos_origem', ['origem'])
    _create_index_if_missing('recebimentos_fornecedor', 'ix_recebimentos_local_recebimento', ['local_recebimento_id'])
    _create_index_if_missing('movimentacoes', 'ix_movimentacoes_tipo', ['tipo'])
    _create_index_if_missing('estoques', 'ix_estoques_codigo_filial', ['codigo_filial'])
    _create_index_if_missing('funcionarios', 'ix_funcionarios_matricula_ativo', ['matricula', 'ativo'])


def downgrade():
    pass
