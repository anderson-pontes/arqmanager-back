"""remove_unique_constraints_from_colaborador

Revision ID: d5988f9a8662
Revises: f2c0bdbb29c7
Create Date: 2025-11-14 21:39:44.774116

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd5988f9a8662'
down_revision = 'f2c0bdbb29c7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Remover índices únicos de email e CPF da tabela colaborador
    # A validação de unicidade agora é feita por escritório na aplicação
    op.drop_index('ix_colaborador_email', table_name='colaborador')
    op.drop_index('ix_colaborador_cpf', table_name='colaborador')
    
    # Recriar os índices sem a constraint unique para manter performance nas buscas
    op.create_index('ix_colaborador_email', 'colaborador', ['email'], unique=False)
    op.create_index('ix_colaborador_cpf', 'colaborador', ['cpf'], unique=False)


def downgrade() -> None:
    # Reverter: recriar índices únicos
    op.drop_index('ix_colaborador_email', table_name='colaborador')
    op.drop_index('ix_colaborador_cpf', table_name='colaborador')
    op.create_index('ix_colaborador_email', 'colaborador', ['email'], unique=True)
    op.create_index('ix_colaborador_cpf', 'colaborador', ['cpf'], unique=True)
