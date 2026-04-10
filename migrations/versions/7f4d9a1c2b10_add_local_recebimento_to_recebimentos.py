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
    with op.batch_alter_table('recebimentos_fornecedor', schema=None) as batch_op:
        batch_op.add_column(sa.Column('local_recebimento_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            'fk_recebimentos_fornecedor_local_recebimento_id',
            'enderecos_estoque',
            ['local_recebimento_id'],
            ['id'],
        )


def downgrade():
    with op.batch_alter_table('recebimentos_fornecedor', schema=None) as batch_op:
        batch_op.drop_constraint('fk_recebimentos_fornecedor_local_recebimento_id', type_='foreignkey')
        batch_op.drop_column('local_recebimento_id')
