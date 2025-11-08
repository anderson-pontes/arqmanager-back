"""create remaining tables manual

Revision ID: create_remaining_manual
Revises: 65e216e25051
Create Date: 2025-01-08

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'create_remaining_manual'
down_revision = '65e216e25051'
branch_labels = None
depends_on = None


def upgrade():
    # Escritório
    op.execute("""
        CREATE TABLE IF NOT EXISTS escritorio (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            razao_social VARCHAR(255),
            cnpj VARCHAR(20) UNIQUE,
            email VARCHAR(255),
            telefone VARCHAR(20),
            logradouro VARCHAR(255),
            numero VARCHAR(20),
            complemento VARCHAR(100),
            bairro VARCHAR(100),
            cidade VARCHAR(100),
            uf VARCHAR(2),
            cep VARCHAR(10),
            ativo BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        )
    """)
    
    # Colaborador Escritório
    op.execute("""
        CREATE TABLE IF NOT EXISTS colaborador_escritorio (
            id SERIAL PRIMARY KEY,
            colaborador_id INTEGER NOT NULL REFERENCES colaborador(id),
            escritorio_id INTEGER NOT NULL REFERENCES escritorio(id),
            tipo INTEGER,
            socio BOOLEAN DEFAULT FALSE,
            pix_tipo VARCHAR(50),
            pix_chave VARCHAR(255),
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        )
    """)
    
    # Forma de Pagamento
    op.execute("""
        CREATE TABLE IF NOT EXISTS forma_pagamento (
            id SERIAL PRIMARY KEY,
            descricao VARCHAR(255) NOT NULL,
            ativo BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        )
    """)
    
    # Projeto Pagamento
    op.execute("""
        CREATE TABLE IF NOT EXISTS projeto_pagamento (
            id SERIAL PRIMARY KEY,
            projeto_id INTEGER NOT NULL REFERENCES projetos(id),
            forma_pagamento_id INTEGER REFERENCES forma_pagamento(id),
            valor NUMERIC(10, 2) NOT NULL,
            valor_recebido NUMERIC(10, 2),
            data_prevista DATE,
            data_recebimento DATE,
            observacao TEXT,
            ativo BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        )
    """)
    
    # Proposta Serviço Etapa
    op.execute("""
        CREATE TABLE IF NOT EXISTS proposta_servico_etapa (
            id SERIAL PRIMARY KEY,
            proposta_id INTEGER NOT NULL REFERENCES propostas(id),
            etapa_id INTEGER NOT NULL REFERENCES etapas(id),
            prazo INTEGER,
            data_prevista DATE,
            data_conclusao DATE,
            observacao TEXT,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        )
    """)
    
    # Conta Bancária
    op.execute("""
        CREATE TABLE IF NOT EXISTS conta_bancaria (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            banco VARCHAR(255),
            agencia VARCHAR(20),
            conta VARCHAR(20),
            tipo VARCHAR(50),
            saldo_inicial NUMERIC(10, 2) DEFAULT 0,
            escritorio_id INTEGER REFERENCES escritorio(id),
            ativo BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        )
    """)
    
    # Conta Movimentação
    op.execute("""
        CREATE TABLE IF NOT EXISTS conta_movimentacao (
            id SERIAL PRIMARY KEY,
            conta_bancaria_id INTEGER NOT NULL REFERENCES conta_bancaria(id),
            data DATE NOT NULL,
            descricao VARCHAR(255) NOT NULL,
            valor NUMERIC(10, 2) NOT NULL,
            tipo VARCHAR(20) NOT NULL,
            saldo NUMERIC(10, 2),
            movimento_id INTEGER REFERENCES movimentos(id),
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        )
    """)
    
    # Plano de Contas
    op.execute("""
        CREATE TABLE IF NOT EXISTS plano_contas (
            id SERIAL PRIMARY KEY,
            codigo VARCHAR(20) NOT NULL,
            descricao VARCHAR(255) NOT NULL,
            tipo VARCHAR(50) NOT NULL,
            nivel INTEGER DEFAULT 1,
            plano_contas_pai_id INTEGER REFERENCES plano_contas(id),
            escritorio_id INTEGER REFERENCES escritorio(id),
            ativo BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        )
    """)
    
    # Feriados
    op.execute("""
        CREATE TABLE IF NOT EXISTS feriados (
            id SERIAL PRIMARY KEY,
            data DATE NOT NULL,
            descricao VARCHAR(255) NOT NULL,
            tipo VARCHAR(50),
            ativo BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        )
    """)
    
    # Indicação
    op.execute("""
        CREATE TABLE IF NOT EXISTS indicacao (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            telefone VARCHAR(20),
            email VARCHAR(255),
            observacao TEXT,
            ativo BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        )
    """)
    
    # Projeto Documento
    op.execute("""
        CREATE TABLE IF NOT EXISTS projeto_documento (
            id SERIAL PRIMARY KEY,
            projeto_id INTEGER NOT NULL REFERENCES projetos(id),
            tipo_documento_id INTEGER,
            nome VARCHAR(255) NOT NULL,
            arquivo VARCHAR(500),
            extensao VARCHAR(10),
            observacao TEXT,
            ativo BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        )
    """)
    
    # Acesso Grupo
    op.execute("""
        CREATE TABLE IF NOT EXISTS acesso_grupo (
            id SERIAL PRIMARY KEY,
            descricao VARCHAR(255) NOT NULL,
            ativo BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        )
    """)
    
    # Projeto Arquivamento
    op.execute("""
        CREATE TABLE IF NOT EXISTS projeto_arquivamento (
            id SERIAL PRIMARY KEY,
            projeto_id INTEGER NOT NULL REFERENCES projetos(id),
            data_arquivamento DATE NOT NULL,
            motivo VARCHAR(255),
            observacao TEXT,
            ativo BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        )
    """)


def downgrade():
    op.drop_table('projeto_arquivamento')
    op.drop_table('acesso_grupo')
    op.drop_table('projeto_documento')
    op.drop_table('indicacao')
    op.drop_table('feriados')
    op.drop_table('plano_contas')
    op.drop_table('conta_movimentacao')
    op.drop_table('conta_bancaria')
    op.drop_table('proposta_servico_etapa')
    op.drop_table('projeto_pagamento')
    op.drop_table('forma_pagamento')
    op.drop_table('colaborador_escritorio')
    op.drop_table('escritorio')
