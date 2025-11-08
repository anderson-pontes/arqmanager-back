#!/usr/bin/env python3
"""
Script para criar views no PostgreSQL adaptadas do MySQL
"""
from sqlalchemy import create_engine, text
from app.core.config import settings

def create_views():
    """Cria views no PostgreSQL"""
    engine = create_engine(settings.DATABASE_URL)
    
    views = {
        'v_cliente': """
            CREATE OR REPLACE VIEW v_cliente AS
            SELECT 
                id as cod_cliente,
                nome,
                tipo_pessoa as cod_tipo_pessoa,
                CASE tipo_pessoa
                    WHEN 'PF' THEN 'Pessoa Física'
                    WHEN 'PJ' THEN 'Pessoa Jurídica'
                    ELSE 'Não definida'
                END as cod_tipo_pessoa_formatado,
                identificacao,
                REGEXP_REPLACE(identificacao, '[./-]', '', 'g') as identificacao_sem_mascara,
                email,
                cep,
                logradouro,
                numero,
                complemento,
                bairro,
                cidade,
                uf,
                telefone,
                whatsapp,
                data_nascimento,
                TO_CHAR(data_nascimento, 'DD/MM/YYYY') as data_nascimento_formatada,
                razao_social,
                inscricao_estadual,
                inscricao_municipal,
                indicado_por,
                ativo,
                created_at,
                updated_at
            FROM cliente
            WHERE ativo = true
        """,
        
        'v_projeto': """
            CREATE OR REPLACE VIEW v_projeto AS
            SELECT 
                p.id as cod_projeto,
                p.numero_projeto,
                p.ano_projeto,
                p.ano_projeto || '/' || LPAD(p.numero_projeto::text, 3, '0') as numero_projeto_formatado,
                p.descricao,
                p.data_inicio,
                TO_CHAR(p.data_inicio, 'DD/MM/YYYY') as data_inicio_formatada,
                p.data_previsao_fim,
                TO_CHAR(p.data_previsao_fim, 'DD/MM/YYYY') as data_previsao_fim_formatada,
                p.data_fim,
                TO_CHAR(p.data_fim, 'DD/MM/YYYY') as data_fim_formatada,
                p.metragem,
                TO_CHAR(p.metragem, 'FM999G999D00') as metragem_formatada,
                p.valor_contrato,
                TO_CHAR(p.valor_contrato, 'FM999G999G999D00') as valor_contrato_formatado,
                p.saldo_contrato,
                TO_CHAR(p.saldo_contrato, 'FM999G999G999D00') as saldo_contrato_formatado,
                p.observacao,
                p.observacao_contrato,
                p.ativo,
                p.cliente_id as cod_cliente,
                c.nome as cliente_nome,
                c.email as cliente_email,
                c.whatsapp as cliente_whatsapp,
                p.servico_id as cod_servico,
                s.nome as servico_nome,
                p.status_id as cod_status,
                st.descricao as status_descricao,
                st.cor as status_cor,
                p.proposta_id as cod_proposta,
                p.cod_contratado,
                p.created_at,
                p.updated_at
            FROM projetos p
            LEFT JOIN cliente c ON p.cliente_id = c.id
            LEFT JOIN servicos s ON p.servico_id = s.id
            LEFT JOIN status st ON p.status_id = st.id
            WHERE p.ativo = true
        """,
        
        'v_proposta': """
            CREATE OR REPLACE VIEW v_proposta AS
            SELECT 
                p.id as cod_proposta,
                p.numero_proposta,
                p.ano_proposta,
                p.ano_proposta || '/' || LPAD(p.numero_proposta::text, 3, '0') as numero_proposta_formatada,
                p.nome,
                p.descricao,
                p.identificacao,
                p.data_proposta,
                TO_CHAR(p.data_proposta, 'DD/MM/YYYY') as data_proposta_formatada,
                p.valor_proposta,
                CASE 
                    WHEN p.valor_proposta IS NOT NULL THEN TO_CHAR(p.valor_proposta::numeric, 'FM999G999G999D00')
                    ELSE NULL
                END as valor_proposta_formatado,
                p.valor_avista,
                CASE 
                    WHEN p.valor_avista IS NOT NULL THEN TO_CHAR(p.valor_avista::numeric, 'FM999G999G999D00')
                    ELSE NULL
                END as valor_avista_formatado,
                p.valor_parcela_aprazo,
                p.valor_parcela_aprazo as valor_parcela_aprazo_formatado,
                p.forma_pagamento,
                p.prazo,
                p.entrega_parcial,
                p.visitas_incluidas,
                p.observacao,
                p.cliente_id as cod_cliente,
                c.nome as cliente_nome,
                c.email as cliente_email,
                c.telefone as cliente_telefone,
                c.whatsapp as cliente_whatsapp,
                p.servico_id as cod_servico,
                s.nome as servico_nome,
                s.descricao as servico_descricao,
                p.status_id as cod_status,
                st.descricao as status_descricao,
                st.cor as status_cor,
                p.created_at,
                p.updated_at
            FROM propostas p
            LEFT JOIN cliente c ON p.cliente_id = c.id
            LEFT JOIN servicos s ON p.servico_id = s.id
            LEFT JOIN status st ON p.status_id = st.id
        """,
        
        'v_movimento': """
            CREATE OR REPLACE VIEW v_movimento AS
            SELECT 
                m.id as cod_movimento,
                m.tipo as cod_despesa_receita_tipo,
                CASE m.tipo
                    WHEN 1 THEN 'Receita'
                    WHEN 2 THEN 'Despesa'
                    ELSE 'Não definido'
                END as tipo_formatado,
                m.descricao,
                m.observacao,
                m.data_entrada,
                TO_CHAR(m.data_entrada, 'DD/MM/YYYY') as data_entrada_formatada,
                m.data_efetivacao,
                TO_CHAR(m.data_efetivacao, 'DD/MM/YYYY') as data_efetivacao_formatada,
                m.competencia,
                TO_CHAR(m.competencia, 'MM/YYYY') as competencia_formatada,
                m.valor,
                TO_CHAR(m.valor, 'FM999G999G999D00') as valor_formatado,
                m.valor_acrescido,
                TO_CHAR(m.valor_acrescido, 'FM999G999G999D00') as valor_acrescido_formatado,
                m.valor_desconto,
                TO_CHAR(m.valor_desconto, 'FM999G999G999D00') as valor_desconto_formatado,
                m.valor_resultante,
                TO_CHAR(m.valor_resultante, 'FM999G999G999D00') as valor_resultante_formatado,
                m.comprovante,
                m.extensao,
                m.codigo_plano_contas,
                m.ativo,
                m.projeto_id as cod_projeto,
                p.numero_projeto,
                p.ano_projeto,
                p.descricao as projeto_descricao,
                m.created_at,
                m.updated_at
            FROM movimentos m
            LEFT JOIN projetos p ON m.projeto_id = p.id
            WHERE m.ativo = true
        """,
        
        'v_servico_etapa': """
            CREATE OR REPLACE VIEW v_servico_etapa AS
            SELECT 
                e.id as cod_servico_etapa,
                e.servico_id as cod_servico,
                s.nome as servico_nome,
                s.descricao as servico_descricao,
                e.nome as eta_descricao,
                e.descricao as descricao_contrato,
                e.ordem,
                e.obrigatoria as exibir,
                e.created_at,
                e.updated_at
            FROM etapas e
            LEFT JOIN servicos s ON e.servico_id = s.id
            ORDER BY e.servico_id, e.ordem
        """,
        
        'v_colaborador': """
            CREATE OR REPLACE VIEW v_colaborador AS
            SELECT 
                c.id as cod_colaborador,
                c.nome,
                c.email,
                c.cpf,
                c.data_nascimento,
                TO_CHAR(c.data_nascimento, 'DD/MM/YYYY') as data_nascimento_formatada,
                c.telefone,
                c.foto,
                c.ativo,
                c.created_at,
                c.updated_at
            FROM colaborador c
            WHERE c.ativo = true
        """
    }
    
    print("=" * 60)
    print("🔄 CRIANDO VIEWS NO POSTGRESQL")
    print("=" * 60)
    
    with engine.connect() as conn:
        for view_name, view_sql in views.items():
            try:
                print(f"\n📊 Criando view: {view_name}")
                conn.execute(text(view_sql))
                conn.commit()
                print(f"✅ View {view_name} criada com sucesso!")
            except Exception as e:
                print(f"❌ Erro ao criar {view_name}: {e}")
                conn.rollback()
    
    print("\n" + "=" * 60)
    print("🎉 PROCESSO CONCLUÍDO!")
    print("=" * 60)
    print(f"\n✅ {len(views)} views criadas:")
    for view_name in views.keys():
        print(f"   - {view_name}")
    
    print("\n💡 Para testar as views:")
    print("   SELECT * FROM v_cliente LIMIT 5;")
    print("   SELECT * FROM v_projeto LIMIT 5;")
    print("   SELECT * FROM v_proposta LIMIT 5;")

def drop_views():
    """Remove todas as views criadas"""
    engine = create_engine(settings.DATABASE_URL)
    
    views = [
        'v_cliente',
        'v_projeto',
        'v_proposta',
        'v_movimento',
        'v_servico_etapa',
        'v_colaborador'
    ]
    
    print("=" * 60)
    print("🗑️  REMOVENDO VIEWS DO POSTGRESQL")
    print("=" * 60)
    
    with engine.connect() as conn:
        for view_name in views:
            try:
                print(f"\n🗑️  Removendo view: {view_name}")
                conn.execute(text(f"DROP VIEW IF EXISTS {view_name} CASCADE"))
                conn.commit()
                print(f"✅ View {view_name} removida!")
            except Exception as e:
                print(f"❌ Erro ao remover {view_name}: {e}")
                conn.rollback()

def list_views():
    """Lista views existentes no PostgreSQL"""
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT table_name 
            FROM information_schema.views 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """))
        
        views = [row[0] for row in result]
        
        print("=" * 60)
        print(f"📋 VIEWS NO POSTGRESQL ({len(views)})")
        print("=" * 60)
        
        if views:
            for view in views:
                print(f"   ✅ {view}")
        else:
            print("   ⚠️  Nenhuma view encontrada")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'drop':
            drop_views()
        elif sys.argv[1] == 'list':
            list_views()
        else:
            print("Uso: python create_views.py [drop|list]")
    else:
        create_views()
