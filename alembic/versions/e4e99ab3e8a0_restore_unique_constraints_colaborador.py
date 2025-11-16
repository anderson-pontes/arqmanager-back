"""restore_unique_constraints_colaborador

Revision ID: e4e99ab3e8a0
Revises: d5988f9a8662
Create Date: 2025-11-14 21:59:58.206693

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4e99ab3e8a0'
down_revision = 'd5988f9a8662'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Restaurar índices únicos de email e CPF na tabela colaborador
    # Email e CPF devem ser únicos no sistema (não por escritório)
    
    # Remover índices não-únicos existentes
    op.drop_index('ix_colaborador_email', table_name='colaborador', if_exists=True)
    op.drop_index('ix_colaborador_cpf', table_name='colaborador', if_exists=True)
    
    # Recriar índices únicos
    op.create_index('ix_colaborador_email', 'colaborador', ['email'], unique=True)
    op.create_index('ix_colaborador_cpf', 'colaborador', ['cpf'], unique=True)


def downgrade() -> None:
    # Reverter: remover índices únicos e recriar como não-únicos
    op.drop_index('ix_colaborador_email', table_name='colaborador', if_exists=True)
    op.drop_index('ix_colaborador_cpf', table_name='colaborador', if_exists=True)
    op.create_index('ix_colaborador_email', 'colaborador', ['email'], unique=False)
    op.create_index('ix_colaborador_cpf', 'colaborador', ['cpf'], unique=False)
