"""add_dados_bancarios_to_colaborador_escritorio

Revision ID: 4ca297d39855
Revises: dc96143c0d06
Create Date: 2025-11-15 23:57:39.174698

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ca297d39855'
down_revision = 'dc96143c0d06'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Verificar se as colunas já existem antes de adicionar
    # Adicionar coluna banco se não existir
    op.execute("""
        DO $$ 
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'colaborador_escritorio' 
                AND column_name = 'banco'
            ) THEN
                ALTER TABLE colaborador_escritorio 
                ADD COLUMN banco VARCHAR(100);
            END IF;
        END $$;
    """)
    
    # Adicionar coluna agencia se não existir
    op.execute("""
        DO $$ 
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'colaborador_escritorio' 
                AND column_name = 'agencia'
            ) THEN
                ALTER TABLE colaborador_escritorio 
                ADD COLUMN agencia VARCHAR(30);
            END IF;
        END $$;
    """)
    
    # Adicionar coluna tipo_conta se não existir
    op.execute("""
        DO $$ 
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'colaborador_escritorio' 
                AND column_name = 'tipo_conta'
            ) THEN
                ALTER TABLE colaborador_escritorio 
                ADD COLUMN tipo_conta VARCHAR(20);
            END IF;
        END $$;
    """)
    
    # Adicionar coluna conta se não existir
    op.execute("""
        DO $$ 
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'colaborador_escritorio' 
                AND column_name = 'conta'
            ) THEN
                ALTER TABLE colaborador_escritorio 
                ADD COLUMN conta VARCHAR(20);
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
                AND column_name = 'banco'
            ) THEN
                ALTER TABLE colaborador_escritorio DROP COLUMN banco;
            END IF;
        END $$;
    """)
    
    op.execute("""
        DO $$ 
        BEGIN
            IF EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'colaborador_escritorio' 
                AND column_name = 'agencia'
            ) THEN
                ALTER TABLE colaborador_escritorio DROP COLUMN agencia;
            END IF;
        END $$;
    """)
    
    op.execute("""
        DO $$ 
        BEGIN
            IF EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'colaborador_escritorio' 
                AND column_name = 'tipo_conta'
            ) THEN
                ALTER TABLE colaborador_escritorio DROP COLUMN tipo_conta;
            END IF;
        END $$;
    """)
    
    op.execute("""
        DO $$ 
        BEGIN
            IF EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'colaborador_escritorio' 
                AND column_name = 'conta'
            ) THEN
                ALTER TABLE colaborador_escritorio DROP COLUMN conta;
            END IF;
        END $$;
    """)
