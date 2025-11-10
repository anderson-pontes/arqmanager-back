"""Add is_system_admin to colaborador

Revision ID: a1b2c3d4e5f6
Revises: 1274f715ef8d
Create Date: 2025-01-09 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = 'create_remaining_manual'  # Última migração: create_remaining_manual (head atual)
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Adicionar coluna is_system_admin na tabela colaborador
    op.add_column(
        'colaborador',
        sa.Column(
            'is_system_admin',
            sa.Boolean(),
            nullable=False,
            server_default='false'
        )
    )


def downgrade() -> None:
    # Remover coluna is_system_admin
    op.drop_column('colaborador', 'is_system_admin')

