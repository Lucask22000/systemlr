"""initial schema baseline

Revision ID: 37aef055a863
Revises:
Create Date: 2026-03-03 00:29:44.759624

"""

from alembic import op


# revision identifiers, used by Alembic.
revision = '37aef055a863'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Cria o schema base a partir do metadata atual.

    O projeto iniciou migrations depois de o banco ja existir, entao a migration
    inicial anterior so aplicava ajustes incrementais sobre tabelas preexistentes.
    Em banco vazio isso deixava `flask db upgrade` inutilizavel. Aqui a migration
    inicial passa a criar o schema completo com `checkfirst=True`, servindo como
    baseline formal para novos ambientes.
    """
    bind = op.get_bind()
    from models import db

    db.metadata.create_all(bind=bind, checkfirst=True)


def downgrade():
    pass
