"""add escritorio address fields

Revision ID: add_escritorio_address
Revises: make_cpf_optional
Create Date: 2025-01-15 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_escritorio_address'
down_revision = 'make_cpf_optional'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Tornar documento (CNPJ) opcional
    op.alter_column('escritorio', 'documento',
                    nullable=True,
                    existing_type=sa.String(20),
                    existing_nullable=False)
    
    # Adicionar campo CPF
    op.add_column('escritorio', sa.Column('cpf', sa.String(14), nullable=True))
    op.create_index(op.f('ix_escritorio_cpf'), 'escritorio', ['cpf'], unique=True)
    
    # Adicionar campos de endereço separados
    op.add_column('escritorio', sa.Column('logradouro', sa.String(255), nullable=True))
    op.add_column('escritorio', sa.Column('numero', sa.String(20), nullable=True))
    op.add_column('escritorio', sa.Column('complemento', sa.String(100), nullable=True))
    op.add_column('escritorio', sa.Column('bairro', sa.String(100), nullable=True))
    op.add_column('escritorio', sa.Column('cidade', sa.String(100), nullable=True))
    op.add_column('escritorio', sa.Column('uf', sa.String(2), nullable=True))
    op.add_column('escritorio', sa.Column('cep', sa.String(10), nullable=True))


def downgrade() -> None:
    # Remover campos de endereço
    op.drop_column('escritorio', 'cep')
    op.drop_column('escritorio', 'uf')
    op.drop_column('escritorio', 'cidade')
    op.drop_column('escritorio', 'bairro')
    op.drop_column('escritorio', 'complemento')
    op.drop_column('escritorio', 'numero')
    op.drop_column('escritorio', 'logradouro')
    
    # Remover campo CPF
    op.drop_index(op.f('ix_escritorio_cpf'), table_name='escritorio')
    op.drop_column('escritorio', 'cpf')
    
    # Tornar documento obrigatório novamente (preencher com valores padrão se necessário)
    op.execute("""
        UPDATE escritorio 
        SET documento = '00000000000000' || id::text 
        WHERE documento IS NULL
    """)
    op.alter_column('escritorio', 'documento',
                    nullable=False,
                    existing_type=sa.String(20),
                    existing_nullable=True)










