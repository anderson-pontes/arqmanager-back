"""add_descricao_contrato_to_etapas

Revision ID: f2c0bdbb29c7
Revises: add_tarefas_table
Create Date: 2025-11-13 23:45:47.428794

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2c0bdbb29c7'
down_revision = 'add_tarefas_table'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Adicionar coluna descricao_contrato na tabela etapas
    op.add_column('etapas', sa.Column('descricao_contrato', sa.Text(), nullable=True))


def downgrade() -> None:
    # Remover coluna descricao_contrato
    op.drop_column('etapas', 'descricao_contrato')
