"""add ecom card bg to empresa config

Revision ID: b1c2d3e4f5a6
Revises: c9d89c3f41a2
Create Date: 2026-03-24 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = 'b1c2d3e4f5a6'
down_revision = 'c9d89c3f41a2'
branch_labels = None
depends_on = None


def upgrade():
    inspector = sa.inspect(op.get_bind())
    if not inspector.has_table('empresa_config'):
        return

    colunas = {col['name'] for col in inspector.get_columns('empresa_config')}
    if 'ecom_card_bg' in colunas:
        return

    with op.batch_alter_table('empresa_config', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('ecom_card_bg', sa.String(length=20), nullable=True, server_default='#ffffff')
        )


def downgrade():
    inspector = sa.inspect(op.get_bind())
    if not inspector.has_table('empresa_config'):
        return

    colunas = {col['name'] for col in inspector.get_columns('empresa_config')}
    if 'ecom_card_bg' not in colunas:
        return

    with op.batch_alter_table('empresa_config', schema=None) as batch_op:
        batch_op.drop_column('ecom_card_bg')
