"""Add projetos, status and projeto_colaborador tables

Revision ID: d378fe72e1a1
Revises: 94bed1fe2f8a
Create Date: 2025-11-08 14:39:12.004969

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'd378fe72e1a1'
down_revision = '94bed1fe2f8a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Criar tabela status
    op.create_table('status',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('descricao', sa.String(length=100), nullable=False),
        sa.Column('cor', sa.String(length=7), nullable=True),
        sa.Column('ativo', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_status_id'), 'status', ['id'], unique=False)
    
    # Criar tabela projetos
    op.create_table('projetos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('cliente_id', sa.Integer(), nullable=False),
        sa.Column('servico_id', sa.Integer(), nullable=False),
        sa.Column('proposta_id', sa.Integer(), nullable=True),
        sa.Column('status_id', sa.Integer(), nullable=True),
        sa.Column('descricao', sa.Text(), nullable=False),
        sa.Column('numero_projeto', sa.Integer(), nullable=True),
        sa.Column('ano_projeto', sa.Integer(), nullable=True),
        sa.Column('data_inicio', sa.Date(), nullable=False),
        sa.Column('data_previsao_fim', sa.Date(), nullable=True),
        sa.Column('data_fim', sa.Date(), nullable=True),
        sa.Column('metragem', sa.Numeric(precision=8, scale=2), nullable=True),
        sa.Column('valor_contrato', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('saldo_contrato', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('observacao', sa.String(length=255), nullable=True),
        sa.Column('observacao_contrato', sa.Text(), nullable=True),
        sa.Column('cod_contratado', sa.String(length=20), nullable=True),
        sa.Column('ativo', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['cliente_id'], ['cliente.id'], ),
        sa.ForeignKeyConstraint(['servico_id'], ['servicos.id'], ),
        sa.ForeignKeyConstraint(['status_id'], ['status.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_projetos_id'), 'projetos', ['id'], unique=False)
    
    # Criar tabela projeto_colaborador
    op.create_table('projeto_colaborador',
        sa.Column('projeto_id', sa.Integer(), nullable=False),
        sa.Column('colaborador_id', sa.Integer(), nullable=False),
        sa.Column('funcao', sa.String(length=100), nullable=True),
        sa.Column('ativo', sa.Boolean(), nullable=True, server_default='true'),
        sa.ForeignKeyConstraint(['colaborador_id'], ['colaborador.id'], ),
        sa.ForeignKeyConstraint(['projeto_id'], ['projetos.id'], ),
        sa.PrimaryKeyConstraint('projeto_id', 'colaborador_id')
    )


def downgrade() -> None:
    # Remover tabelas
    op.drop_table('projeto_colaborador')
    op.drop_index(op.f('ix_projetos_id'), table_name='projetos')
    op.drop_table('projetos')
    op.drop_index(op.f('ix_status_id'), table_name='status')
    op.drop_table('status')
