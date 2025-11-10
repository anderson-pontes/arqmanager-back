"""add_auditoria_table

Revision ID: 45561ebf7912
Revises: 06f4fa27b50f
Create Date: 2025-11-10 15:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45561ebf7912'
down_revision = '06f4fa27b50f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Cria tabela de auditoria para rastrear ações dos usuários por escritório
    """
    op.create_table(
        'auditoria',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('usuario_id', sa.Integer(), nullable=False),
        sa.Column('escritorio_id', sa.Integer(), nullable=True),
        sa.Column('acao', sa.String(length=100), nullable=False),
        sa.Column('entidade', sa.String(length=100), nullable=False),
        sa.Column('entidade_id', sa.Integer(), nullable=True),
        sa.Column('descricao', sa.Text(), nullable=True),
        sa.Column('ip_address', sa.String(length=45), nullable=True),
        sa.Column('user_agent', sa.String(length=500), nullable=True),
        sa.Column('dados_anteriores', sa.Text(), nullable=True),
        sa.Column('dados_novos', sa.Text(), nullable=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['usuario_id'], ['colaborador.id'], ),
        sa.ForeignKeyConstraint(['escritorio_id'], ['escritorio.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_auditoria_id'), 'auditoria', ['id'], unique=False)
    op.create_index(op.f('ix_auditoria_usuario_id'), 'auditoria', ['usuario_id'], unique=False)
    op.create_index(op.f('ix_auditoria_escritorio_id'), 'auditoria', ['escritorio_id'], unique=False)
    op.create_index(op.f('ix_auditoria_timestamp'), 'auditoria', ['timestamp'], unique=False)


def downgrade() -> None:
    """
    Remove tabela de auditoria
    """
    op.drop_index(op.f('ix_auditoria_timestamp'), table_name='auditoria')
    op.drop_index(op.f('ix_auditoria_escritorio_id'), table_name='auditoria')
    op.drop_index(op.f('ix_auditoria_usuario_id'), table_name='auditoria')
    op.drop_index(op.f('ix_auditoria_id'), table_name='auditoria')
    op.drop_table('auditoria')
