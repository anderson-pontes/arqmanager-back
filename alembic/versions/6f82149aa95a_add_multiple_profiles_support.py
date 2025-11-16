"""add_multiple_profiles_support

Revision ID: 6f82149aa95a
Revises: e4e99ab3e8a0
Create Date: 2025-11-14 23:28:15.594917

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f82149aa95a'
down_revision = 'e4e99ab3e8a0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Criar tabela para múltiplos perfis por colaborador-escritório
    op.create_table(
        'colaborador_escritorio_perfil',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('colaborador_id', sa.Integer(), nullable=False),
        sa.Column('escritorio_id', sa.Integer(), nullable=False),
        sa.Column('perfil', sa.String(50), nullable=False),
        sa.Column('ativo', sa.Boolean(), default=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['colaborador_id'], ['colaborador.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['escritorio_id'], ['escritorio.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Criar índices para melhor performance (sem unique ainda)
    op.create_index('ix_colaborador_escritorio_perfil_colab', 'colaborador_escritorio_perfil', ['colaborador_id'])
    op.create_index('ix_colaborador_escritorio_perfil_esc', 'colaborador_escritorio_perfil', ['escritorio_id'])
    
    # Migrar dados existentes da tabela colaborador_escritorio para a nova tabela
    # Usar DISTINCT para evitar duplicatas antes de criar a constraint única
    op.execute("""
        INSERT INTO colaborador_escritorio_perfil (colaborador_id, escritorio_id, perfil, ativo, created_at, updated_at)
        SELECT DISTINCT
            colaborador_id,
            escritorio_id,
            COALESCE(perfil, 'Produção') as perfil,
            COALESCE(ativo, true) as ativo,
            NOW() as created_at,
            NOW() as updated_at
        FROM colaborador_escritorio
        WHERE perfil IS NOT NULL
    """)
    
    # Agora criar o índice único após migrar os dados
    op.create_index(
        'ix_colaborador_escritorio_perfil_unique',
        'colaborador_escritorio_perfil',
        ['colaborador_id', 'escritorio_id', 'perfil'],
        unique=True
    )


def downgrade() -> None:
    # Remover índices
    op.drop_index('ix_colaborador_escritorio_perfil_esc', table_name='colaborador_escritorio_perfil')
    op.drop_index('ix_colaborador_escritorio_perfil_colab', table_name='colaborador_escritorio_perfil')
    op.drop_index('ix_colaborador_escritorio_perfil_unique', table_name='colaborador_escritorio_perfil')
    
    # Remover tabela
    op.drop_table('colaborador_escritorio_perfil')
