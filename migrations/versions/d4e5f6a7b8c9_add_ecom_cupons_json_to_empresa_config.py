"""add ecom cupons json to empresa config

Revision ID: d4e5f6a7b8c9
Revises: b1c2d3e4f5a6
Create Date: 2026-03-24 00:10:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = 'd4e5f6a7b8c9'
down_revision = 'b1c2d3e4f5a6'
branch_labels = None
depends_on = None


def upgrade():
    inspector = sa.inspect(op.get_bind())
    if not inspector.has_table('empresa_config'):
        return

    colunas = {col['name'] for col in inspector.get_columns('empresa_config')}
    if 'ecom_cupons_json' in colunas:
        return

    with op.batch_alter_table('empresa_config', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ecom_cupons_json', sa.Text(), nullable=True))


def downgrade():
    inspector = sa.inspect(op.get_bind())
    if not inspector.has_table('empresa_config'):
        return

    colunas = {col['name'] for col in inspector.get_columns('empresa_config')}
    if 'ecom_cupons_json' not in colunas:
        return

    with op.batch_alter_table('empresa_config', schema=None) as batch_op:
        batch_op.drop_column('ecom_cupons_json')
