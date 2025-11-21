"""add_socio_pix_to_colaborador_escritorio

Revision ID: dc96143c0d06
Revises: 6f82149aa95a
Create Date: 2025-11-15 23:31:33.466318

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc96143c0d06'
down_revision = '6f82149aa95a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Verificar se as colunas já existem antes de adicionar
    # Adicionar coluna socio se não existir
    op.execute("""
        DO $$ 
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'colaborador_escritorio' 
                AND column_name = 'socio'
            ) THEN
                ALTER TABLE colaborador_escritorio 
                ADD COLUMN socio BOOLEAN DEFAULT FALSE;
            END IF;
        END $$;
    """)
    
    # Adicionar coluna pix_tipo se não existir
    op.execute("""
        DO $$ 
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'colaborador_escritorio' 
                AND column_name = 'pix_tipo'
            ) THEN
                ALTER TABLE colaborador_escritorio 
                ADD COLUMN pix_tipo VARCHAR(50);
            END IF;
        END $$;
    """)
    
    # Adicionar coluna pix_chave se não existir
    op.execute("""
        DO $$ 
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'colaborador_escritorio' 
                AND column_name = 'pix_chave'
            ) THEN
                ALTER TABLE colaborador_escritorio 
                ADD COLUMN pix_chave VARCHAR(255);
            END IF;
        END $$;
    """)


def downgrade() -> None:
    # Remover colunas se existirem
    op.execute("""
        DO $$ 
        BEGIN
            IF EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'colaborador_escritorio' 
                AND column_name = 'socio'
            ) THEN
                ALTER TABLE colaborador_escritorio DROP COLUMN socio;
            END IF;
        END $$;
    """)
    
    op.execute("""
        DO $$ 
        BEGIN
            IF EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'colaborador_escritorio' 
                AND column_name = 'pix_tipo'
            ) THEN
                ALTER TABLE colaborador_escritorio DROP COLUMN pix_tipo;
            END IF;
        END $$;
    """)
    
    op.execute("""
        DO $$ 
        BEGIN
            IF EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'colaborador_escritorio' 
                AND column_name = 'pix_chave'
            ) THEN
                ALTER TABLE colaborador_escritorio DROP COLUMN pix_chave;
            END IF;
        END $$;
    """)
