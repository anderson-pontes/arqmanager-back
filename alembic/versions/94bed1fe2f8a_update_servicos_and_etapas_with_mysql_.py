"""Update servicos and etapas with MySQL fields

Revision ID: 94bed1fe2f8a
Revises: 7cec4802024b
Create Date: 2025-11-08 14:31:41.661296

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '94bed1fe2f8a'
down_revision = '7cec4802024b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Adicionar novos campos em servicos
    op.add_column('servicos', sa.Column('descricao_contrato', sa.Text(), nullable=True))
    op.add_column('servicos', sa.Column('codigo_plano_contas', sa.String(length=50), nullable=True))
    
    # Alterar tamanho do campo nome em servicos
    op.alter_column('servicos', 'nome', type_=sa.String(length=500), existing_type=sa.String(length=200))
    
    # Alterar tamanho do campo nome em etapas
    op.alter_column('etapas', 'nome', type_=sa.String(length=500), existing_type=sa.String(length=200))


def downgrade() -> None:
    # Remover novos campos
    op.drop_column('servicos', 'codigo_plano_contas')
    op.drop_column('servicos', 'descricao_contrato')
    
    # Reverter tamanho dos campos
    op.alter_column('servicos', 'nome', type_=sa.String(length=200), existing_type=sa.String(length=500))
    op.alter_column('etapas', 'nome', type_=sa.String(length=200), existing_type=sa.String(length=500))
