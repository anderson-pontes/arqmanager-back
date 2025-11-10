"""make cpf optional

Revision ID: make_cpf_optional
Revises: a1b2c3d4e5f6
Create Date: 2025-01-09

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'make_cpf_optional'
down_revision = 'a1b2c3d4e5f6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Tornar CPF nullable
    # PostgreSQL permite múltiplos NULLs em colunas unique
    op.alter_column('colaborador', 'cpf',
                    nullable=True,
                    existing_type=sa.String(14),
                    existing_nullable=False)


def downgrade() -> None:
    # Reverter: tornar CPF obrigatório novamente
    # Primeiro, definir um CPF padrão para registros NULL (se houver)
    op.execute("""
        UPDATE colaborador 
        SET cpf = '00000000000' || id::text 
        WHERE cpf IS NULL
    """)
    
    op.alter_column('colaborador', 'cpf',
                    nullable=False,
                    existing_type=sa.String(14),
                    existing_nullable=True)

