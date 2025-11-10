"""add_escritorio_id_isolation

Revision ID: 06f4fa27b50f
Revises: add_escritorio_address
Create Date: 2025-11-10 14:38:45.613319

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06f4fa27b50f'
down_revision = 'add_escritorio_address'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Adiciona escritorio_id em todas as tabelas que precisam de isolamento por escritório.
    Inicialmente nullable para permitir migração de dados existentes.
    """
    
    # Cliente - precisa de isolamento
    op.add_column('cliente', sa.Column('escritorio_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_cliente_escritorio', 'cliente', 'escritorio', ['escritorio_id'], ['id'])
    op.create_index(op.f('ix_cliente_escritorio_id'), 'cliente', ['escritorio_id'])
    
    # Projetos - precisa de isolamento
    op.add_column('projetos', sa.Column('escritorio_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_projetos_escritorio', 'projetos', 'escritorio', ['escritorio_id'], ['id'])
    op.create_index(op.f('ix_projetos_escritorio_id'), 'projetos', ['escritorio_id'])
    
    # Propostas - precisa de isolamento
    op.add_column('propostas', sa.Column('escritorio_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_propostas_escritorio', 'propostas', 'escritorio', ['escritorio_id'], ['id'])
    op.create_index(op.f('ix_propostas_escritorio_id'), 'propostas', ['escritorio_id'])
    
    # Movimentos - precisa de isolamento direto (além de via projeto)
    op.add_column('movimentos', sa.Column('escritorio_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_movimentos_escritorio', 'movimentos', 'escritorio', ['escritorio_id'], ['id'])
    op.create_index(op.f('ix_movimentos_escritorio_id'), 'movimentos', ['escritorio_id'])
    
    # Serviços - precisa de isolamento
    op.add_column('servicos', sa.Column('escritorio_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_servicos_escritorio', 'servicos', 'escritorio', ['escritorio_id'], ['id'])
    op.create_index(op.f('ix_servicos_escritorio_id'), 'servicos', ['escritorio_id'])
    
    # Etapas - precisa de isolamento (via serviço, mas também direto para facilitar queries)
    op.add_column('etapas', sa.Column('escritorio_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_etapas_escritorio', 'etapas', 'escritorio', ['escritorio_id'], ['id'])
    op.create_index(op.f('ix_etapas_escritorio_id'), 'etapas', ['escritorio_id'])
    
    # Status - precisa de isolamento
    op.add_column('status', sa.Column('escritorio_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_status_escritorio', 'status', 'escritorio', ['escritorio_id'], ['id'])
    op.create_index(op.f('ix_status_escritorio_id'), 'status', ['escritorio_id'])
    
    # Forma de Pagamento - precisa de isolamento
    op.add_column('forma_pagamento', sa.Column('escritorio_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_forma_pagamento_escritorio', 'forma_pagamento', 'escritorio', ['escritorio_id'], ['id'])
    op.create_index(op.f('ix_forma_pagamento_escritorio_id'), 'forma_pagamento', ['escritorio_id'])
    
    # Feriados - precisa de isolamento
    op.add_column('feriados', sa.Column('escritorio_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_feriados_escritorio', 'feriados', 'escritorio', ['escritorio_id'], ['id'])
    op.create_index(op.f('ix_feriados_escritorio_id'), 'feriados', ['escritorio_id'])
    
    # Indicação - precisa de isolamento
    op.add_column('indicacao', sa.Column('escritorio_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_indicacao_escritorio', 'indicacao', 'escritorio', ['escritorio_id'], ['id'])
    op.create_index(op.f('ix_indicacao_escritorio_id'), 'indicacao', ['escritorio_id'])
    
    # Projeto Colaborador - precisa de isolamento direto (além de via projeto)
    op.add_column('projeto_colaborador', sa.Column('escritorio_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_projeto_colaborador_escritorio', 'projeto_colaborador', 'escritorio', ['escritorio_id'], ['id'])
    op.create_index(op.f('ix_projeto_colaborador_escritorio_id'), 'projeto_colaborador', ['escritorio_id'])
    
    # Projeto Pagamento - precisa de isolamento direto (além de via projeto)
    op.add_column('projeto_pagamento', sa.Column('escritorio_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_projeto_pagamento_escritorio', 'projeto_pagamento', 'escritorio', ['escritorio_id'], ['id'])
    op.create_index(op.f('ix_projeto_pagamento_escritorio_id'), 'projeto_pagamento', ['escritorio_id'])
    
    # Projeto Documento - precisa de isolamento direto (além de via projeto)
    op.add_column('projeto_documento', sa.Column('escritorio_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_projeto_documento_escritorio', 'projeto_documento', 'escritorio', ['escritorio_id'], ['id'])
    op.create_index(op.f('ix_projeto_documento_escritorio_id'), 'projeto_documento', ['escritorio_id'])
    
    # Proposta Servico Etapa - precisa de isolamento direto (além de via proposta)
    op.add_column('proposta_servico_etapa', sa.Column('escritorio_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_proposta_servico_etapa_escritorio', 'proposta_servico_etapa', 'escritorio', ['escritorio_id'], ['id'])
    op.create_index(op.f('ix_proposta_servico_etapa_escritorio_id'), 'proposta_servico_etapa', ['escritorio_id'])
    
    # Conta Movimentação - precisa de isolamento direto (além de via conta_bancaria)
    op.add_column('conta_movimentacao', sa.Column('escritorio_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_conta_movimentacao_escritorio', 'conta_movimentacao', 'escritorio', ['escritorio_id'], ['id'])
    op.create_index(op.f('ix_conta_movimentacao_escritorio_id'), 'conta_movimentacao', ['escritorio_id'])
    
    # Preencher escritorio_id baseado em relacionamentos existentes
    # Para projetos, propostas e movimentos, podemos inferir do cliente ou projeto
    # Para outros, vamos deixar NULL inicialmente e preencher via seeds ou manualmente
    
    # Preencher escritorio_id em projetos baseado no cliente (se cliente tiver escritorio_id)
    op.execute("""
        UPDATE projetos p
        SET escritorio_id = (
            SELECT c.escritorio_id 
            FROM cliente c 
            WHERE c.id = p.cliente_id 
            LIMIT 1
        )
        WHERE p.escritorio_id IS NULL
    """)
    
    # Preencher escritorio_id em propostas baseado no cliente
    op.execute("""
        UPDATE propostas pr
        SET escritorio_id = (
            SELECT c.escritorio_id 
            FROM cliente c 
            WHERE c.id = pr.cliente_id 
            LIMIT 1
        )
        WHERE pr.escritorio_id IS NULL
    """)
    
    # Preencher escritorio_id em movimentos baseado no projeto
    op.execute("""
        UPDATE movimentos m
        SET escritorio_id = (
            SELECT p.escritorio_id 
            FROM projetos p 
            WHERE p.id = m.projeto_id 
            LIMIT 1
        )
        WHERE m.escritorio_id IS NULL AND m.projeto_id IS NOT NULL
    """)
    
    # Preencher escritorio_id em etapas baseado no serviço
    op.execute("""
        UPDATE etapas e
        SET escritorio_id = (
            SELECT s.escritorio_id 
            FROM servicos s 
            WHERE s.id = e.servico_id 
            LIMIT 1
        )
        WHERE e.escritorio_id IS NULL
    """)
    
    # Preencher escritorio_id em projeto_colaborador baseado no projeto
    op.execute("""
        UPDATE projeto_colaborador pc
        SET escritorio_id = (
            SELECT p.escritorio_id 
            FROM projetos p 
            WHERE p.id = pc.projeto_id 
            LIMIT 1
        )
        WHERE pc.escritorio_id IS NULL
    """)
    
    # Preencher escritorio_id em projeto_pagamento baseado no projeto
    op.execute("""
        UPDATE projeto_pagamento pp
        SET escritorio_id = (
            SELECT p.escritorio_id 
            FROM projetos p 
            WHERE p.id = pp.projeto_id 
            LIMIT 1
        )
        WHERE pp.escritorio_id IS NULL
    """)
    
    # Preencher escritorio_id em projeto_documento baseado no projeto
    op.execute("""
        UPDATE projeto_documento pd
        SET escritorio_id = (
            SELECT p.escritorio_id 
            FROM projetos p 
            WHERE p.id = pd.projeto_id 
            LIMIT 1
        )
        WHERE pd.escritorio_id IS NULL
    """)
    
    # Preencher escritorio_id em proposta_servico_etapa baseado na proposta
    op.execute("""
        UPDATE proposta_servico_etapa pse
        SET escritorio_id = (
            SELECT pr.escritorio_id 
            FROM propostas pr 
            WHERE pr.id = pse.proposta_id 
            LIMIT 1
        )
        WHERE pse.escritorio_id IS NULL
    """)
    
    # Preencher escritorio_id em conta_movimentacao baseado na conta_bancaria
    op.execute("""
        UPDATE conta_movimentacao cm
        SET escritorio_id = (
            SELECT cb.escritorio_id 
            FROM conta_bancaria cb 
            WHERE cb.id = cm.conta_bancaria_id 
            LIMIT 1
        )
        WHERE cm.escritorio_id IS NULL
    """)
    
    # NOTA: Os campos escritorio_id foram criados como nullable para permitir migração.
    # Após garantir que todos os dados foram migrados, execute uma migration adicional
    # para tornar esses campos NOT NULL. Por enquanto, mantemos nullable para permitir
    # criação de novos escritórios sem dados históricos.


def downgrade() -> None:
    """
    Remove escritorio_id de todas as tabelas
    """
    # Remover índices e foreign keys primeiro
    op.drop_index(op.f('ix_conta_movimentacao_escritorio_id'), table_name='conta_movimentacao')
    op.drop_constraint('fk_conta_movimentacao_escritorio', 'conta_movimentacao', type_='foreignkey')
    op.drop_column('conta_movimentacao', 'escritorio_id')
    
    op.drop_index(op.f('ix_proposta_servico_etapa_escritorio_id'), table_name='proposta_servico_etapa')
    op.drop_constraint('fk_proposta_servico_etapa_escritorio', 'proposta_servico_etapa', type_='foreignkey')
    op.drop_column('proposta_servico_etapa', 'escritorio_id')
    
    op.drop_index(op.f('ix_projeto_documento_escritorio_id'), table_name='projeto_documento')
    op.drop_constraint('fk_projeto_documento_escritorio', 'projeto_documento', type_='foreignkey')
    op.drop_column('projeto_documento', 'escritorio_id')
    
    op.drop_index(op.f('ix_projeto_pagamento_escritorio_id'), table_name='projeto_pagamento')
    op.drop_constraint('fk_projeto_pagamento_escritorio', 'projeto_pagamento', type_='foreignkey')
    op.drop_column('projeto_pagamento', 'escritorio_id')
    
    op.drop_index(op.f('ix_projeto_colaborador_escritorio_id'), table_name='projeto_colaborador')
    op.drop_constraint('fk_projeto_colaborador_escritorio', 'projeto_colaborador', type_='foreignkey')
    op.drop_column('projeto_colaborador', 'escritorio_id')
    
    op.drop_index(op.f('ix_indicacao_escritorio_id'), table_name='indicacao')
    op.drop_constraint('fk_indicacao_escritorio', 'indicacao', type_='foreignkey')
    op.drop_column('indicacao', 'escritorio_id')
    
    op.drop_index(op.f('ix_feriados_escritorio_id'), table_name='feriados')
    op.drop_constraint('fk_feriados_escritorio', 'feriados', type_='foreignkey')
    op.drop_column('feriados', 'escritorio_id')
    
    op.drop_index(op.f('ix_forma_pagamento_escritorio_id'), table_name='forma_pagamento')
    op.drop_constraint('fk_forma_pagamento_escritorio', 'forma_pagamento', type_='foreignkey')
    op.drop_column('forma_pagamento', 'escritorio_id')
    
    op.drop_index(op.f('ix_status_escritorio_id'), table_name='status')
    op.drop_constraint('fk_status_escritorio', 'status', type_='foreignkey')
    op.drop_column('status', 'escritorio_id')
    
    op.drop_index(op.f('ix_etapas_escritorio_id'), table_name='etapas')
    op.drop_constraint('fk_etapas_escritorio', 'etapas', type_='foreignkey')
    op.drop_column('etapas', 'escritorio_id')
    
    op.drop_index(op.f('ix_servicos_escritorio_id'), table_name='servicos')
    op.drop_constraint('fk_servicos_escritorio', 'servicos', type_='foreignkey')
    op.drop_column('servicos', 'escritorio_id')
    
    op.drop_index(op.f('ix_movimentos_escritorio_id'), table_name='movimentos')
    op.drop_constraint('fk_movimentos_escritorio', 'movimentos', type_='foreignkey')
    op.drop_column('movimentos', 'escritorio_id')
    
    op.drop_index(op.f('ix_propostas_escritorio_id'), table_name='propostas')
    op.drop_constraint('fk_propostas_escritorio', 'propostas', type_='foreignkey')
    op.drop_column('propostas', 'escritorio_id')
    
    op.drop_index(op.f('ix_projetos_escritorio_id'), table_name='projetos')
    op.drop_constraint('fk_projetos_escritorio', 'projetos', type_='foreignkey')
    op.drop_column('projetos', 'escritorio_id')
    
    op.drop_index(op.f('ix_cliente_escritorio_id'), table_name='cliente')
    op.drop_constraint('fk_cliente_escritorio', 'cliente', type_='foreignkey')
    op.drop_column('cliente', 'escritorio_id')
