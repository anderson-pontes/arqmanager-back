"""Add propostas table

Revision ID: 1274f715ef8d
Revises: d378fe72e1a1
Create Date: 2025-11-08 14:50:12.004969

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '1274f715ef8d'
down_revision = 'd378fe72e1a1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Criar tabela propostas
    op.create_table('propostas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('cliente_id', sa.Integer(), nullable=False),
        sa.Column('servico_id', sa.Integer(), nullable=False),
        sa.Column('status_id', sa.Integer(), nullable=True),
        sa.Column('nome', sa.String(length=255), nullable=True),
        sa.Column('descricao', sa.Text(), nullable=True),
        sa.Column('identificacao', sa.String(length=255), nullable=True),
        sa.Column('numero_proposta', sa.Integer(), nullable=False),
        sa.Column('ano_proposta', sa.Integer(), nullable=False),
        sa.Column('data_proposta', sa.Date(), nullable=True),
        sa.Column('valor_proposta', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('valor_avista', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('valor_parcela_aprazo', sa.String(length=255), nullable=True),
        sa.Column('forma_pagamento', sa.String(length=200), nullable=True),
        sa.Column('prazo', sa.String(length=200), nullable=True),
        sa.Column('entrega_parcial', sa.String(length=8), nullable=True, server_default='Não'),
        sa.Column('visitas_incluidas', sa.Integer(), nullable=True),
        sa.Column('observacao', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['cliente_id'], ['cliente.id'], ),
        sa.ForeignKeyConstraint(['servico_id'], ['servicos.id'], ),
        sa.ForeignKeyConstraint(['status_id'], ['status.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_propostas_id'), 'propostas', ['id'], unique=False)


def downgrade() -> None:
    # Remover tabela
    op.drop_index(op.f('ix_propostas_id'), table_name='propostas')
    op.drop_table('propostas')
