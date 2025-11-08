#!/usr/bin/env python3
"""
Script para criar as views restantes mais importantes no PostgreSQL
"""
from sqlalchemy import create_engine, text
from app.core.config import settings

def create_remaining_views():
    """Cria as views restantes prioritárias"""
    engine = create_engine(settings.DATABASE_URL)
    
    views = {
        # PRIORIDADE ALTA
        
        'v_financeiro_projeto': """
            CREATE OR REPLACE VIEW v_financeiro_projeto AS
            SELECT 
                pp.id as cod_projeto_pagamento,
                pp.projeto_id as cod_projeto,
                p.numero_projeto,
                p.ano_projeto,
                p.ano_projeto || '/' || LPAD(p.numero_projeto::text, 3, '0') as numero_projeto_formatado,
                p.descricao as projeto_descricao,
                c.nome as cliente_nome,
                pp.forma_pagamento_id as cod_forma_pagamento,
                fp.descricao as forma_pagamento_descricao,
                pp.valor,
                COALESCE(pp.valor_recebido, pp.valor) as valor_recebido,
                TO_CHAR(pp.valor, 'FM999G999G999D00') as valor_formatado,
                TO_CHAR(COALESCE(pp.valor_recebido, pp.valor), 'FM999G999G999D00') as valor_recebido_formatado,
                pp.data_prevista,
                TO_CHAR(pp.data_prevista, 'DD/MM/YYYY') as data_prevista_formatada,
                pp.data_recebimento,
                TO_CHAR(pp.data_recebimento, 'DD/MM/YYYY') as data_recebimento_formatada,
                CASE 
                    WHEN pp.data_recebimento IS NOT NULL THEN 'Recebido'
                    WHEN pp.data_prevista < CURRENT_DATE THEN 'Atrasado'
                    ELSE 'A Receber'
                END as status_pagamento,
                pp.observacao,
                pp.ativo,
                p.valor_contrato,
                p.saldo_contrato,
                TO_CHAR(p.valor_contrato, 'FM999G999G999D00') as valor_contrato_formatado,
                TO_CHAR(p.saldo_contrato, 'FM999G999G999D00') as saldo_contrato_formatado
            FROM projeto_pagamento pp
            LEFT JOIN projetos p ON pp.projeto_id = p.id
            LEFT JOIN cliente c ON p.cliente_id = c.id
            LEFT JOIN forma_pagamento fp ON pp.forma_pagamento_id = fp.id
            WHERE pp.ativo = true
        """,
        
        'v_extrato_conta': """
            CREATE OR REPLACE VIEW v_extrato_conta AS
            SELECT 
                cm.id as cod_conta_movimentacao,
                cm.conta_bancaria_id as cod_conta_bancaria,
                cb.nome as conta_nome,
                cb.banco,
                cm.data,
                TO_CHAR(cm.data, 'DD/MM/YYYY') as data_formatada,
                EXTRACT(YEAR FROM cm.data) as ano,
                EXTRACT(MONTH FROM cm.data) as mes,
                TO_CHAR(cm.data, 'MM/YYYY') as mes_ano,
                cm.descricao,
                cm.tipo,
                CASE cm.tipo
                    WHEN 'receita' THEN 'Receita'
                    WHEN 'despesa' THEN 'Despesa'
                    ELSE 'Não definido'
                END as tipo_formatado,
                cm.valor,
                TO_CHAR(cm.valor, 'FM999G999G999D00') as valor_formatado,
                cm.saldo,
                TO_CHAR(cm.saldo, 'FM999G999G999D00') as saldo_formatado,
                cm.movimento_id as cod_movimento,
                m.descricao as movimento_descricao,
                cb.escritorio_id
            FROM conta_movimentacao cm
            LEFT JOIN conta_bancaria cb ON cm.conta_bancaria_id = cb.id
            LEFT JOIN movimentos m ON cm.movimento_id = m.id
            ORDER BY cm.data DESC, cm.id DESC
        """,
        
        'v_plano_contas': """
            CREATE OR REPLACE VIEW v_plano_contas AS
            SELECT 
                pc.id as cod_plano_contas,
                pc.codigo,
                pc.descricao,
                pc.tipo,
                CASE pc.tipo
                    WHEN 'receita' THEN 'Receita'
                    WHEN 'despesa' THEN 'Despesa'
                    WHEN 'ativo' THEN 'Ativo'
                    WHEN 'passivo' THEN 'Passivo'
                    ELSE 'Não definido'
                END as tipo_formatado,
                pc.nivel,
                pc.plano_contas_pai_id as cod_plano_contas_pai,
                pp.codigo as codigo_pai,
                pp.descricao as descricao_pai,
                pc.escritorio_id,
                pc.ativo,
                pc.created_at,
                pc.updated_at
            FROM plano_contas pc
            LEFT JOIN plano_contas pp ON pc.plano_contas_pai_id = pp.id
            WHERE pc.ativo = true
            ORDER BY pc.codigo
        """,
        
        'v_proposta_servico_etapa': """
            CREATE OR REPLACE VIEW v_proposta_servico_etapa AS
            SELECT 
                pse.id as cod_proposta_servico_etapa,
                pse.proposta_id as cod_proposta,
                pr.numero_proposta,
                pr.ano_proposta,
                pr.ano_proposta || '/' || LPAD(pr.numero_proposta::text, 3, '0') as numero_proposta_formatado,
                pr.nome as proposta_nome,
                pse.etapa_id as cod_servico_etapa,
                e.nome as etapa_descricao,
                e.descricao as etapa_descricao_contrato,
                e.ordem as etapa_ordem,
                pse.prazo,
                pse.data_prevista,
                TO_CHAR(pse.data_prevista, 'DD/MM/YYYY') as data_prevista_formatada,
                pse.data_conclusao,
                TO_CHAR(pse.data_conclusao, 'DD/MM/YYYY') as data_conclusao_formatada,
                CASE 
                    WHEN pse.data_conclusao IS NOT NULL THEN 'Concluída'
                    WHEN pse.data_prevista < CURRENT_DATE THEN 'Atrasada'
                    ELSE 'Em Andamento'
                END as status_etapa,
                pse.observacao,
                pr.cliente_id as cod_cliente,
                c.nome as cliente_nome
            FROM proposta_servico_etapa pse
            LEFT JOIN propostas pr ON pse.proposta_id = pr.id
            LEFT JOIN etapas e ON pse.etapa_id = e.id
            LEFT JOIN cliente c ON pr.cliente_id = c.id
            ORDER BY pr.ano_proposta DESC, pr.numero_proposta DESC, e.ordem
        """,
        
        'v_previsto_realizado': """
            CREATE OR REPLACE VIEW v_previsto_realizado AS
            SELECT 
                EXTRACT(YEAR FROM m.competencia) as ano,
                EXTRACT(MONTH FROM m.competencia) as mes,
                TO_CHAR(m.competencia, 'MM/YYYY') as mes_ano,
                m.tipo,
                CASE m.tipo
                    WHEN 1 THEN 'Receita'
                    WHEN 2 THEN 'Despesa'
                    ELSE 'Não definido'
                END as tipo_formatado,
                SUM(CASE WHEN m.data_efetivacao IS NULL THEN m.valor ELSE 0 END) as valor_previsto,
                SUM(CASE WHEN m.data_efetivacao IS NOT NULL THEN m.valor ELSE 0 END) as valor_realizado,
                TO_CHAR(SUM(CASE WHEN m.data_efetivacao IS NULL THEN m.valor ELSE 0 END), 'FM999G999G999D00') as valor_previsto_formatado,
                TO_CHAR(SUM(CASE WHEN m.data_efetivacao IS NOT NULL THEN m.valor ELSE 0 END), 'FM999G999G999D00') as valor_realizado_formatado
            FROM movimentos m
            WHERE m.ativo = true
            GROUP BY EXTRACT(YEAR FROM m.competencia), EXTRACT(MONTH FROM m.competencia), m.competencia, m.tipo
            ORDER BY ano DESC, mes DESC, m.tipo
        """,
        
        # PRIORIDADE MÉDIA
        
        'v_feriados': """
            CREATE OR REPLACE VIEW v_feriados AS
            SELECT 
                f.id as cod_feriado,
                f.data,
                TO_CHAR(f.data, 'DD/MM/YYYY') as data_formatada,
                EXTRACT(DAY FROM f.data) as dia,
                EXTRACT(MONTH FROM f.data) as mes,
                EXTRACT(YEAR FROM f.data) as ano,
                TO_CHAR(f.data, 'Day') as dia_semana,
                f.descricao,
                f.tipo,
                CASE f.tipo
                    WHEN 'nacional' THEN 'Nacional'
                    WHEN 'estadual' THEN 'Estadual'
                    WHEN 'municipal' THEN 'Municipal'
                    ELSE 'Não definido'
                END as tipo_formatado,
                f.ativo
            FROM feriados f
            WHERE f.ativo = true
            ORDER BY f.data
        """,
        
        'v_indicacao': """
            CREATE OR REPLACE VIEW v_indicacao AS
            SELECT 
                i.id as cod_indicacao,
                i.nome,
                i.telefone,
                i.email,
                i.observacao,
                i.ativo,
                i.created_at as data_cadastro,
                TO_CHAR(i.created_at, 'DD/MM/YYYY') as data_cadastro_formatada,
                -- Verificar se virou cliente
                CASE 
                    WHEN EXISTS (
                        SELECT 1 FROM cliente c 
                        WHERE c.nome ILIKE '%' || i.nome || '%' 
                        OR c.telefone = i.telefone 
                        OR c.email = i.email
                    ) THEN 'Sim'
                    ELSE 'Não'
                END as virou_cliente
            FROM indicacao i
            WHERE i.ativo = true
            ORDER BY i.created_at DESC
        """,
        
        'v_aniversariantes': """
            CREATE OR REPLACE VIEW v_aniversariantes AS
            SELECT 
                c.id as cod_cliente,
                c.nome,
                c.email,
                c.telefone,
                c.whatsapp,
                c.data_nascimento,
                TO_CHAR(c.data_nascimento, 'DD/MM/YYYY') as data_nascimento_formatada,
                EXTRACT(DAY FROM c.data_nascimento) as dia_nascimento,
                EXTRACT(MONTH FROM c.data_nascimento) as mes_nascimento,
                EXTRACT(YEAR FROM AGE(c.data_nascimento)) as idade,
                TO_CHAR(c.data_nascimento, 'DD/MM') as dia_mes,
                -- Próximo aniversário
                CASE 
                    WHEN EXTRACT(MONTH FROM c.data_nascimento) = EXTRACT(MONTH FROM CURRENT_DATE)
                         AND EXTRACT(DAY FROM c.data_nascimento) >= EXTRACT(DAY FROM CURRENT_DATE)
                    THEN MAKE_DATE(EXTRACT(YEAR FROM CURRENT_DATE)::int, 
                                   EXTRACT(MONTH FROM c.data_nascimento)::int, 
                                   EXTRACT(DAY FROM c.data_nascimento)::int)
                    WHEN EXTRACT(MONTH FROM c.data_nascimento) > EXTRACT(MONTH FROM CURRENT_DATE)
                    THEN MAKE_DATE(EXTRACT(YEAR FROM CURRENT_DATE)::int, 
                                   EXTRACT(MONTH FROM c.data_nascimento)::int, 
                                   EXTRACT(DAY FROM c.data_nascimento)::int)
                    ELSE MAKE_DATE((EXTRACT(YEAR FROM CURRENT_DATE) + 1)::int, 
                                   EXTRACT(MONTH FROM c.data_nascimento)::int, 
                                   EXTRACT(DAY FROM c.data_nascimento)::int)
                END as proximo_aniversario,
                c.tipo_pessoa,
                c.ativo
            FROM cliente c
            WHERE c.ativo = true 
            AND c.data_nascimento IS NOT NULL
            ORDER BY mes_nascimento, dia_nascimento
        """,
        
        'v_permissao': """
            CREATE OR REPLACE VIEW v_permissao AS
            SELECT 
                apg.id as cod_permissao,
                apg.grupo_id as cod_grupo,
                ag.descricao as grupo_descricao,
                apg.modulo_transacao_id as cod_modulo_transacao,
                amt.descricao as modulo_transacao_descricao,
                amt.modulo as modulo_nome,
                amt.transacao as transacao_nome,
                apg.permitir,
                CASE apg.permitir
                    WHEN true THEN 'Permitido'
                    ELSE 'Negado'
                END as permissao_formatada,
                apg.created_at,
                apg.updated_at
            FROM acesso_permissao_grupo apg
            LEFT JOIN acesso_grupo ag ON apg.grupo_id = ag.id
            LEFT JOIN acesso_modulo_transacao amt ON apg.modulo_transacao_id = amt.id
            WHERE ag.ativo = true
            ORDER BY ag.descricao, amt.modulo, amt.transacao
        """,
        
        'v_projeto_arquivamento': """
            CREATE OR REPLACE VIEW v_projeto_arquivamento AS
            SELECT 
                pa.id as cod_projeto_arquivamento,
                pa.projeto_id as cod_projeto,
                p.numero_projeto,
                p.ano_projeto,
                p.ano_projeto || '/' || LPAD(p.numero_projeto::text, 3, '0') as numero_projeto_formatado,
                p.descricao as projeto_descricao,
                c.nome as cliente_nome,
                pa.data_arquivamento,
                TO_CHAR(pa.data_arquivamento, 'DD/MM/YYYY') as data_arquivamento_formatada,
                pa.motivo,
                pa.observacao,
                pa.ativo
            FROM projeto_arquivamento pa
            LEFT JOIN projetos p ON pa.projeto_id = p.id
            LEFT JOIN cliente c ON p.cliente_id = c.id
            WHERE pa.ativo = true
            ORDER BY pa.data_arquivamento DESC
        """
    }
    
    print("=" * 70)
    print("🔄 CRIANDO VIEWS RESTANTES NO POSTGRESQL")
    print("=" * 70)
    
    created = 0
    errors = 0
    
    with engine.connect() as conn:
        for view_name, view_sql in views.items():
            try:
                print(f"\n📊 Criando view: {view_name}")
                conn.execute(text(view_sql))
                conn.commit()
                print(f"   ✅ View {view_name} criada com sucesso!")
                created += 1
            except Exception as e:
                print(f"   ❌ Erro ao criar {view_name}: {str(e)[:150]}")
                conn.rollback()
                errors += 1
    
    print("\n" + "=" * 70)
    print("📊 RESUMO")
    print("=" * 70)
    print(f"\n✅ Views criadas: {created}")
    print(f"❌ Erros: {errors}")
    
    if created > 0:
        print(f"\n📋 Views disponíveis agora:")
        print("   PRIORIDADE ALTA:")
        print("   ✅ v_financeiro_projeto - Financeiro por projeto")
        print("   ✅ v_extrato_conta - Extrato bancário")
        print("   ✅ v_plano_contas - Plano de contas")
        print("   ✅ v_proposta_servico_etapa - Etapas das propostas")
        print("   ✅ v_previsto_realizado - Análise financeira")
        print("\n   PRIORIDADE MÉDIA:")
        print("   ✅ v_feriados - Feriados")
        print("   ✅ v_indicacao - Indicações")
        print("   ✅ v_aniversariantes - Aniversariantes")
        print("   ✅ v_permissao - Permissões")
        print("   ✅ v_projeto_arquivamento - Projetos arquivados")
    
    print("\n💡 Para testar:")
    print("   python test_views.py")

if __name__ == "__main__":
    create_remaining_views()
