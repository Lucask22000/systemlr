"""add local_recebimento to recebimentos

Revision ID: 7f4d9a1c2b10
Revises: 37aef055a863
Create Date: 2026-03-18 17:30:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = '7f4d9a1c2b10'
down_revision = '37aef055a863'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if not inspector.has_table('recebimentos_fornecedor'):
        return

    colunas = {col['name'] for col in inspector.get_columns('recebimentos_fornecedor')}
    if 'local_recebimento_id' in colunas:
        return

    with op.batch_alter_table('recebimentos_fornecedor', schema=None) as batch_op:
        batch_op.add_column(sa.Column('local_recebimento_id', sa.Integer(), nullable=True))


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if not inspector.has_table('recebimentos_fornecedor'):
        return

    colunas = {col['name'] for col in inspector.get_columns('recebimentos_fornecedor')}
    if 'local_recebimento_id' not in colunas:
        return

    with op.batch_alter_table('recebimentos_fornecedor', schema=None) as batch_op:
        batch_op.drop_column('local_recebimento_id')
