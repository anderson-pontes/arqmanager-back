#!/usr/bin/env python3
"""
Script para analisar views não migradas e determinar prioridade
"""
from sqlalchemy import create_engine, text

MYSQL_URL = "mysql+pymysql://root:xpto1661WIN@localhost:3306/dbarqmanager"

def analyze_views():
    """Analisa todas as views não migradas"""
    engine = create_engine(MYSQL_URL)
    
    # Views não migradas
    views = [
        'v_aniversariantes',
        'v_ata',
        'v_contas_escritorio',
        'v_data',
        'v_email_enviado',
        'v_extrato_conta',
        'v_extrato_conta_consolidado',
        'v_extrato_conta_consolidado_ano',
        'v_feriados',
        'v_financeiro_projeto',
        'v_indicacao',
        'v_mes',
        'v_permissao',
        'v_plano_contas',
        'v_previsto_realizado',
        'v_projeto_arquivamento',
        'v_projeto_rrt',
        'v_proposta_microservico',
        'v_proposta_servico_etapa',
        'v_rrt_projeto',
        'v_template_email_whatsapp'
    ]
    
    print("=" * 80)
    print("🔍 ANÁLISE DE VIEWS NÃO MIGRADAS")
    print("=" * 80)
    
    with engine.connect() as conn:
        for view_name in views:
            print(f"\n{'='*80}")
            print(f"📊 VIEW: {view_name}")
            print('='*80)
            
            try:
                # Contar registros
                result = conn.execute(text(f"SELECT COUNT(*) FROM {view_name}"))
                count = result.scalar()
                
                # Pegar primeiras colunas
                result = conn.execute(text(f"SELECT * FROM {view_name} LIMIT 1"))
                row = result.fetchone()
                
                if row:
                    columns = result.keys()
                    print(f"📈 Registros: {count}")
                    print(f"📋 Colunas ({len(columns)}):")
                    for i, col in enumerate(columns[:10]):  # Primeiras 10 colunas
                        print(f"   - {col}")
                    if len(columns) > 10:
                        print(f"   ... e mais {len(columns) - 10} colunas")
                    
                    # Mostrar exemplo de dados
                    print(f"\n💡 Exemplo de dados:")
                    for i, (col, val) in enumerate(zip(columns[:5], row[:5])):
                        print(f"   {col}: {str(val)[:50]}")
                else:
                    print(f"⚠️  View vazia")
                    
            except Exception as e:
                print(f"❌ Erro: {str(e)[:100]}")
    
    print("\n" + "=" * 80)
    print("📊 CLASSIFICAÇÃO POR PRIORIDADE")
    print("=" * 80)
    
    print("\n🔴 PRIORIDADE ALTA (Essenciais):")
    print("   1. v_financeiro_projeto - Financeiro por projeto")
    print("   2. v_extrato_conta - Extrato bancário")
    print("   3. v_plano_contas - Plano de contas")
    print("   4. v_proposta_servico_etapa - Etapas das propostas")
    print("   5. v_previsto_realizado - Análise financeira")
    
    print("\n🟡 PRIORIDADE MÉDIA (Úteis):")
    print("   6. v_projeto_arquivamento - Projetos arquivados")
    print("   7. v_permissao - Permissões de usuários")
    print("   8. v_feriados - Feriados para cálculo")
    print("   9. v_indicacao - Indicações de clientes")
    print("   10. v_aniversariantes - Aniversariantes do mês")
    
    print("\n🟢 PRIORIDADE BAIXA (Opcionais):")
    print("   11. v_email_enviado - Histórico de emails")
    print("   12. v_ata - Atas de reunião")
    print("   13. v_data - Datas auxiliares")
    print("   14. v_mes - Meses do ano")
    print("   15. v_contas_escritorio - Contas por escritório")
    print("   16. v_extrato_conta_consolidado - Extrato consolidado")
    print("   17. v_extrato_conta_consolidado_ano - Extrato anual")
    print("   18. v_projeto_rrt - RRT dos projetos")
    print("   19. v_proposta_microservico - Microserviços (não usado)")
    print("   20. v_rrt_projeto - RRT por projeto")
    print("   21. v_template_email_whatsapp - Templates")

if __name__ == "__main__":
    analyze_views()
