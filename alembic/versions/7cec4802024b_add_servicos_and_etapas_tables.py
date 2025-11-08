"""Add servicos and etapas tables

Revision ID: 7cec4802024b
Revises: create_clientes_002
Create Date: 2025-11-08 14:07:49.422989

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7cec4802024b'
down_revision = 'create_clientes_002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Criar tabela de serviços
    op.create_table('servicos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(length=200), nullable=False),
        sa.Column('descricao', sa.Text(), nullable=True),
        sa.Column('valor_base', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('unidade', sa.String(length=50), nullable=True),
        sa.Column('ativo', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_servicos_id'), 'servicos', ['id'], unique=False)
    op.create_index(op.f('ix_servicos_nome'), 'servicos', ['nome'], unique=False)
    
    # Criar tabela de etapas
    op.create_table('etapas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('servico_id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(length=200), nullable=False),
        sa.Column('descricao', sa.Text(), nullable=True),
        sa.Column('ordem', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('obrigatoria', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['servico_id'], ['servicos.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_etapas_id'), 'etapas', ['id'], unique=False)


def downgrade() -> None:
    # Remover tabelas
    op.drop_index(op.f('ix_etapas_id'), table_name='etapas')
    op.drop_table('etapas')
    op.drop_index(op.f('ix_servicos_nome'), table_name='servicos')
    op.drop_index(op.f('ix_servicos_id'), table_name='servicos')
    op.drop_table('servicos')
