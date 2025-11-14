"""Add tarefas table

Revision ID: add_tarefas_table
Revises: 94bed1fe2f8a
Create Date: 2025-01-XX XX:XX:XX.XXXXXX

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_tarefas_table'
down_revision = '45561ebf7912'  # Aponta para a última migration (add_auditoria_table)
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Criar tabela de tarefas
    op.create_table('tarefas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('etapa_id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(length=500), nullable=False),
        sa.Column('ordem', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('cor', sa.String(length=50), nullable=True),
        sa.Column('tem_prazo', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('precisa_detalhamento', sa.Boolean(), nullable=True, server_default='false'),
        sa.Column('escritorio_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['etapa_id'], ['etapas.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['escritorio_id'], ['escritorio.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tarefas_id'), 'tarefas', ['id'], unique=False)
    op.create_index(op.f('ix_tarefas_etapa_id'), 'tarefas', ['etapa_id'], unique=False)
    op.create_index(op.f('ix_tarefas_escritorio_id'), 'tarefas', ['escritorio_id'], unique=False)


def downgrade() -> None:
    # Remover tabela de tarefas
    op.drop_index(op.f('ix_tarefas_escritorio_id'), table_name='tarefas')
    op.drop_index(op.f('ix_tarefas_etapa_id'), table_name='tarefas')
    op.drop_index(op.f('ix_tarefas_id'), table_name='tarefas')
    op.drop_table('tarefas')


