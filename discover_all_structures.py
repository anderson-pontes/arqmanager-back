#!/usr/bin/env python3
"""
Script para descobrir TODAS as estruturas das tabelas MySQL
e gerar um relatório completo
"""
from sqlalchemy import create_engine, text

MYSQL_URL = "mysql+pymysql://root:xpto1661WIN@localhost:3306/dbarqmanager"

def main():
    engine = create_engine(MYSQL_URL)
    
    tables = [
        'escritorio',
        'colaborador_escritorio',
        'forma_pagamento',
        'projeto_pagamento',
        'proposta_servico_etapa',
        'conta_bancaria',
        'conta_movimentacao',
        'plano_contas',
        'feriados',
        'indicacao',
        'projeto_documento',
        'acesso_grupo',
        'projeto_arquivamento',
    ]
    
    print("=" * 80)
    print("📊 ESTRUTURAS DAS TABELAS MYSQL")
    print("=" * 80)
    
    with engine.connect() as conn:
        for table in tables:
            print(f"\n{'='*80}")
            print(f"📋 Tabela: {table}")
            print('='*80)
            
            try:
                result = conn.execute(text(f"DESCRIBE {table}"))
                print(f"\n{'Campo':<30} {'Tipo':<20} {'Null':<5} {'Key':<5}")
                print("-" * 80)
                for row in result:
                    print(f"{row[0]:<30} {row[1]:<20} {row[2]:<5} {row[3]:<5}")
                
                # Contar registros
                result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = result.scalar()
                print(f"\n📊 Total de registros: {count}")
                
            except Exception as e:
                print(f"❌ Erro: {e}")
    
    print("\n" + "=" * 80)
    print("✅ Análise concluída!")
    print("=" * 80)

if __name__ == "__main__":
    main()
