"""add public ecommerce accounts reviews and coupons

Revision ID: f1a2b3c4d5e6
Revises: e8f1a2b3c4d5
Create Date: 2026-03-27 22:15:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = 'f1a2b3c4d5e6'
down_revision = 'e8f1a2b3c4d5'
branch_labels = None
depends_on = None


def _inspector():
    return sa.inspect(op.get_bind())


def _has_table(name):
    return _inspector().has_table(name)


def _columns(name):
    if not _has_table(name):
        return set()
    return {col['name'] for col in _inspector().get_columns(name)}


def _indexes(name):
    if not _has_table(name):
        return set()
    return {idx['name'] for idx in _inspector().get_indexes(name)}


def _create_index_if_missing(table_name, index_name, columns, *, unique=False):
    if index_name not in _indexes(table_name):
        op.create_index(index_name, table_name, columns, unique=unique)


def _add_columns_if_missing(table_name, columns):
    existing = _columns(table_name)
    if not existing:
        return
    for column in columns:
        if column.name in existing:
            continue
        with op.batch_alter_table(table_name, schema=None) as batch_op:
            batch_op.add_column(column)
        existing.add(column.name)


def _create_clientes_enderecos_if_missing():
    if _has_table('clientes_enderecos'):
        return
    op.create_table(
        'clientes_enderecos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('cliente_id', sa.Integer(), nullable=False),
        sa.Column('apelido', sa.String(length=50), nullable=True),
        sa.Column('cep', sa.String(length=12), nullable=False),
        sa.Column('endereco', sa.String(length=180), nullable=False),
        sa.Column('numero', sa.String(length=20), nullable=True),
        sa.Column('complemento', sa.String(length=120), nullable=True),
        sa.Column('bairro', sa.String(length=100), nullable=True),
        sa.Column('cidade', sa.String(length=100), nullable=True),
        sa.Column('estado', sa.String(length=2), nullable=True),
        sa.Column('referencia', sa.String(length=180), nullable=True),
        sa.Column('principal', sa.Boolean(), nullable=True),
        sa.Column('criado_em', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['cliente_id'], ['clientes_publicos.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    _create_index_if_missing('clientes_enderecos', 'ix_clientes_enderecos_cliente_principal', ['cliente_id', 'principal'])


def _create_clientes_favoritos_if_missing():
    if _has_table('clientes_favoritos'):
        return
    op.create_table(
        'clientes_favoritos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('cliente_id', sa.Integer(), nullable=False),
        sa.Column('produto_id', sa.Integer(), nullable=False),
        sa.Column('criado_em', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['cliente_id'], ['clientes_publicos.id']),
        sa.ForeignKeyConstraint(['produto_id'], ['produtos.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('cliente_id', 'produto_id', name='uq_cliente_favorito_produto'),
    )
    _create_index_if_missing('clientes_favoritos', 'ix_clientes_favoritos_cliente_criado', ['cliente_id', 'criado_em'])


def _create_avaliacoes_if_missing():
    if _has_table('avaliacoes_produtos'):
        return
    op.create_table(
        'avaliacoes_produtos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('produto_id', sa.Integer(), nullable=False),
        sa.Column('cliente_id', sa.Integer(), nullable=False),
        sa.Column('nota', sa.Integer(), nullable=False),
        sa.Column('titulo', sa.String(length=100), nullable=True),
        sa.Column('comentario', sa.Text(), nullable=True),
        sa.Column('criado_em', sa.DateTime(), nullable=True),
        sa.Column('aprovada', sa.Boolean(), nullable=True),
        sa.CheckConstraint('nota >= 1 AND nota <= 5', name='ck_avaliacoes_produtos_nota'),
        sa.ForeignKeyConstraint(['cliente_id'], ['clientes_publicos.id']),
        sa.ForeignKeyConstraint(['produto_id'], ['produtos.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('produto_id', 'cliente_id', name='uq_avaliacao_produto_cliente'),
    )
    _create_index_if_missing('avaliacoes_produtos', 'ix_avaliacoes_produtos_produto_aprovada', ['produto_id', 'aprovada'])


def _create_cupons_if_missing():
    if _has_table('cupons'):
        return
    op.create_table(
        'cupons',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('codigo', sa.String(length=50), nullable=False),
        sa.Column('descricao', sa.String(length=180), nullable=True),
        sa.Column('tipo_desconto', sa.String(length=20), nullable=False),
        sa.Column('valor', sa.Float(), nullable=False),
        sa.Column('minimo_compra', sa.Float(), nullable=True),
        sa.Column('produtos_incluidos', sa.Text(), nullable=True),
        sa.Column('categorias_incluidas', sa.Text(), nullable=True),
        sa.Column('primeira_compra', sa.Boolean(), nullable=True),
        sa.Column('data_inicio', sa.Date(), nullable=True),
        sa.Column('data_fim', sa.Date(), nullable=True),
        sa.Column('ativo', sa.Boolean(), nullable=True),
        sa.Column('uso_unico_por_cliente', sa.Boolean(), nullable=True),
        sa.Column('criado_em', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('codigo'),
    )
    _create_index_if_missing('cupons', 'ix_cupons_codigo_ativo', ['codigo', 'ativo'])


def _create_cupons_utilizacoes_if_missing():
    if _has_table('cupons_utilizacoes'):
        return
    op.create_table(
        'cupons_utilizacoes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('cupom_id', sa.Integer(), nullable=False),
        sa.Column('cliente_id', sa.Integer(), nullable=False),
        sa.Column('pedido_id', sa.Integer(), nullable=True),
        sa.Column('criado_em', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['cliente_id'], ['clientes_publicos.id']),
        sa.ForeignKeyConstraint(['cupom_id'], ['cupons.id']),
        sa.ForeignKeyConstraint(['pedido_id'], ['pedidos.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    _create_index_if_missing('cupons_utilizacoes', 'ix_cupons_utilizacoes_cupom_cliente', ['cupom_id', 'cliente_id'])


def upgrade():
    _add_columns_if_missing('clientes_publicos', [
        sa.Column('senha_hash', sa.String(length=255), nullable=True),
        sa.Column('data_cadastro', sa.DateTime(), nullable=True),
        sa.Column('ultimo_acesso', sa.DateTime(), nullable=True),
    ])
    _add_columns_if_missing('pedidos', [
        sa.Column('cliente_publico_id', sa.Integer(), nullable=True),
        sa.Column('codigo_rastreio', sa.String(length=100), nullable=True),
        sa.Column('transportadora', sa.String(length=100), nullable=True),
        sa.Column('data_estimada_entrega', sa.Date(), nullable=True),
    ])

    if _has_table('pedidos') and 'cliente_publico_id' in _columns('pedidos'):
        with op.batch_alter_table('pedidos', schema=None) as batch_op:
            try:
                batch_op.create_foreign_key('fk_pedidos_cliente_publico_id', 'clientes_publicos', ['cliente_publico_id'], ['id'])
            except Exception:
                pass

    _create_clientes_enderecos_if_missing()
    _create_clientes_favoritos_if_missing()
    _create_avaliacoes_if_missing()
    _create_cupons_if_missing()
    _create_cupons_utilizacoes_if_missing()

    _create_index_if_missing('clientes_publicos', 'ix_clientes_publicos_email_celular', ['email', 'celular'])
    _create_index_if_missing('clientes_publicos', 'ix_clientes_publicos_data_cadastro', ['data_cadastro'])
    _create_index_if_missing('pedidos', 'ix_pedidos_cliente_publico_id', ['cliente_publico_id'])


def downgrade():
    pass
