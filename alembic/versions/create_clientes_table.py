"""Create clientes table

Revision ID: create_clientes_002
Revises: create_tables_001
Create Date: 2025-01-08 00:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'create_clientes_002'
down_revision = 'create_tables_001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Criar tabela cliente
    op.create_table(
        'cliente',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('nome', sa.String(length=255), nullable=False),
        sa.Column('razao_social', sa.String(length=255), nullable=True),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('identificacao', sa.String(length=20), nullable=False),
        sa.Column('tipo_pessoa', sa.String(length=20), nullable=False),
        sa.Column('telefone', sa.String(length=20), nullable=False),
        sa.Column('whatsapp', sa.String(length=20), nullable=True),
        sa.Column('data_nascimento', sa.Date(), nullable=True),
        sa.Column('ativo', sa.Boolean(), nullable=True, default=True),
        sa.Column('logradouro', sa.String(length=255), nullable=True),
        sa.Column('numero', sa.String(length=20), nullable=True),
        sa.Column('complemento', sa.String(length=100), nullable=True),
        sa.Column('bairro', sa.String(length=100), nullable=True),
        sa.Column('cidade', sa.String(length=100), nullable=True),
        sa.Column('uf', sa.String(length=2), nullable=True),
        sa.Column('cep', sa.String(length=10), nullable=True),
        sa.Column('inscricao_estadual', sa.String(length=20), nullable=True),
        sa.Column('inscricao_municipal', sa.String(length=20), nullable=True),
        sa.Column('indicado_por', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cliente_id'), 'cliente', ['id'], unique=False)
    op.create_index(op.f('ix_cliente_nome'), 'cliente', ['nome'], unique=False)
    op.create_index(op.f('ix_cliente_email'), 'cliente', ['email'], unique=False)
    op.create_index(op.f('ix_cliente_identificacao'), 'cliente', ['identificacao'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_cliente_identificacao'), table_name='cliente')
    op.drop_index(op.f('ix_cliente_email'), table_name='cliente')
    op.drop_index(op.f('ix_cliente_nome'), table_name='cliente')
    op.drop_index(op.f('ix_cliente_id'), table_name='cliente')
    op.drop_table('cliente')
