"""add_logo_field_to_escritorio

Revision ID: add_logo_escritorio
Revises: 6f82149aa95a
Create Date: 2025-01-20 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_logo_escritorio'
down_revision = '6f82149aa95a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Adicionar campo logo na tabela escritorio
    op.add_column('escritorio', sa.Column('logo', sa.String(500), nullable=True))


def downgrade() -> None:
    # Remover campo logo da tabela escritorio
    op.drop_column('escritorio', 'logo')



