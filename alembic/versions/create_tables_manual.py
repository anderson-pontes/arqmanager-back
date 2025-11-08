"""Create tables manually

Revision ID: create_tables_001
Revises: 78d7cf7f2ecc
Create Date: 2025-01-08 00:10:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'create_tables_001'
down_revision = '78d7cf7f2ecc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Criar tabela escritorio
    op.create_table(
        'escritorio',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('nome_fantasia', sa.String(length=255), nullable=False),
        sa.Column('razao_social', sa.String(length=255), nullable=False),
        sa.Column('documento', sa.String(length=20), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('telefone', sa.String(length=20), nullable=True),
        sa.Column('endereco', sa.String(length=500), nullable=True),
        sa.Column('cor', sa.String(length=7), nullable=True),
        sa.Column('dias_uteis', sa.Boolean(), nullable=True),
        sa.Column('prazo_arquiva_proposta', sa.Integer(), nullable=True),
        sa.Column('observacao_proposta_padrao', sa.String(length=1000), nullable=True),
        sa.Column('observacao_contrato_padrao', sa.String(length=1000), nullable=True),
        sa.Column('ativo', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_escritorio_documento'), 'escritorio', ['documento'], unique=True)
    op.create_index(op.f('ix_escritorio_id'), 'escritorio', ['id'], unique=False)
    
    # Criar tabela colaborador
    op.create_table(
        'colaborador',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('nome', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('senha', sa.String(length=255), nullable=False),
        sa.Column('cpf', sa.String(length=14), nullable=False),
        sa.Column('telefone', sa.String(length=20), nullable=True),
        sa.Column('data_nascimento', sa.Date(), nullable=True),
        sa.Column('perfil', sa.String(length=50), nullable=True),
        sa.Column('tipo', sa.String(length=20), nullable=True),
        sa.Column('ativo', sa.Boolean(), nullable=True),
        sa.Column('foto', sa.String(length=500), nullable=True),
        sa.Column('ultimo_acesso', sa.Date(), nullable=True),
        sa.Column('tipo_pix', sa.String(length=20), nullable=True),
        sa.Column('chave_pix', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_colaborador_cpf'), 'colaborador', ['cpf'], unique=True)
    op.create_index(op.f('ix_colaborador_email'), 'colaborador', ['email'], unique=True)
    op.create_index(op.f('ix_colaborador_id'), 'colaborador', ['id'], unique=False)
    op.create_index(op.f('ix_colaborador_nome'), 'colaborador', ['nome'], unique=False)
    
    # Criar tabela de associação colaborador_escritorio
    op.create_table(
        'colaborador_escritorio',
        sa.Column('colaborador_id', sa.Integer(), nullable=False),
        sa.Column('escritorio_id', sa.Integer(), nullable=False),
        sa.Column('perfil', sa.String(length=50), nullable=True),
        sa.Column('ativo', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['colaborador_id'], ['colaborador.id'], ),
        sa.ForeignKeyConstraint(['escritorio_id'], ['escritorio.id'], ),
        sa.PrimaryKeyConstraint('colaborador_id', 'escritorio_id')
    )


def downgrade() -> None:
    op.drop_table('colaborador_escritorio')
    op.drop_index(op.f('ix_colaborador_nome'), table_name='colaborador')
    op.drop_index(op.f('ix_colaborador_id'), table_name='colaborador')
    op.drop_index(op.f('ix_colaborador_email'), table_name='colaborador')
    op.drop_index(op.f('ix_colaborador_cpf'), table_name='colaborador')
    op.drop_table('colaborador')
    op.drop_index(op.f('ix_escritorio_id'), table_name='escritorio')
    op.drop_index(op.f('ix_escritorio_documento'), table_name='escritorio')
    op.drop_table('escritorio')
