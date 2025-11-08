"""Add movimentos table

Revision ID: 65e216e25051
Revises: 1274f715ef8d
Create Date: 2025-11-08 14:52:23.748015

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65e216e25051'
down_revision = '1274f715ef8d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Criar tabela movimentos
    op.create_table('movimentos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('projeto_id', sa.Integer(), nullable=True),
        sa.Column('tipo', sa.Integer(), nullable=False),
        sa.Column('data_entrada', sa.Date(), nullable=False),
        sa.Column('data_efetivacao', sa.Date(), nullable=True),
        sa.Column('competencia', sa.Date(), nullable=True),
        sa.Column('descricao', sa.String(length=255), nullable=False),
        sa.Column('observacao', sa.String(length=255), nullable=True),
        sa.Column('valor', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('valor_acrescido', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('valor_desconto', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('valor_resultante', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('comprovante', sa.String(length=255), nullable=True),
        sa.Column('extensao', sa.String(length=10), nullable=True),
        sa.Column('codigo_plano_contas', sa.String(length=50), nullable=True),
        sa.Column('ativo', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['projeto_id'], ['projetos.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_movimentos_id'), 'movimentos', ['id'], unique=False)
    op.create_index('ix_movimentos_data_entrada', 'movimentos', ['data_entrada'], unique=False)
    op.create_index('ix_movimentos_tipo', 'movimentos', ['tipo'], unique=False)


def downgrade() -> None:
    # Remover tabela
    op.drop_index('ix_movimentos_tipo', table_name='movimentos')
    op.drop_index('ix_movimentos_data_entrada', table_name='movimentos')
    op.drop_index(op.f('ix_movimentos_id'), table_name='movimentos')
    op.drop_table('movimentos')
