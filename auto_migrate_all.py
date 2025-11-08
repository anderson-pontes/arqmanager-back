#!/usr/bin/env python3
"""
Script automático que descobre a estrutura das tabelas MySQL e migra tudo
"""
import sys
from sqlalchemy import create_engine, text
from app.core.config import settings

MYSQL_URL = "mysql+pymysql://root:xpto1661WIN@localhost:3306/dbarqmanager"

def get_table_structure(mysql_conn, table_name):
    """Obtém a estrutura de uma tabela"""
    result = mysql_conn.execute(text(f"DESCRIBE {table_name}"))
    columns = []
    for row in result:
        columns.append({
            'name': row[0],
            'type': row[1],
            'null': row[2],
            'key': row[3],
            'default': row[4]
        })
    return columns

def migrate_table_auto(mysql_engine, pg_engine, mysql_table, pg_table, where_clause=""):
    """Migra uma tabela automaticamente descobrindo sua estrutura"""
    print(f"\n📋 Migrando {mysql_table} → {pg_table}...")
    
    with mysql_engine.connect() as mysql_conn:
        # Descobrir estrutura
        columns = get_table_structure(mysql_conn, mysql_table)
        column_names = [col['name'] for col in columns]
        
        print(f"   📊 {len(columns)} colunas encontradas")
        
        # Construir SELECT
        select_sql = f"SELECT {', '.join(column_names)} FROM {mysql_table}"
        if where_clause:
            select_sql += f" WHERE {where_clause}"
        
        try:
            result = mysql_conn.execute(text(select_sql))
        except Exception as e:
            print(f"   ❌ Erro ao ler dados: {str(e)[:100]}")
            return 0, 0
        
        count = 0
        errors = 0
        
        for row in result:
            try:
                # Criar dict de dados
                data = {col: row[i] for i, col in enumerate(column_names)}
                
                # Construir INSERT dinâmico
                cols_str = ', '.join(column_names)
                placeholders = ', '.join([f":{col}" for col in column_names])
                
                insert_sql = f"""
                    INSERT INTO {pg_table} ({cols_str}, created_at, updated_at)
                    VALUES ({placeholders}, NOW(), NOW())
                    ON CONFLICT (id) DO NOTHING
                """
                
                with pg_engine.connect() as pg_conn:
                    pg_conn.execute(text(insert_sql), data)
                    pg_conn.commit()
                count += 1
                
                if count % 100 == 0:
                    print(f"   ⏳ {count} registros migrados...")
                    
            except Exception as e:
                errors += 1
                if errors <= 3:
                    print(f"   ⚠️  Erro no registro {count + errors}: {str(e)[:100]}")
        
        print(f"   ✅ {count} registros migrados ({errors} erros)")
        return count, errors

def main():
    """Função principal"""
    print("=" * 70)
    print("🔄 MIGRAÇÃO AUTOMÁTICA COMPLETA - MySQL → PostgreSQL")
    print("=" * 70)
    
    mysql_engine = create_engine(MYSQL_URL)
    pg_engine = create_engine(settings.DATABASE_URL)
    
    # Tabelas a migrar (MySQL → PostgreSQL)
    tables_to_migrate = [
        # (mysql_table, pg_table, where_clause)
        ('escritorio', 'escritorio', 'id_escritorio > 0'),
        ('colaborador_escritorio', 'colaborador_escritorio', ''),
        ('forma_pagamento', 'forma_pagamento', 'ativo = 1'),
        ('projeto_pagamento', 'projeto_pagamento', ''),
        ('proposta_servico_etapa', 'proposta_servico_etapa', ''),
        ('conta_bancaria', 'conta_bancaria', 'ativo = 1'),
        ('conta_movimentacao', 'conta_movimentacao', ''),
        ('plano_contas', 'plano_contas', 'ativo = 1'),
        ('feriados', 'feriados', 'ativo = 1'),
        ('indicacao', 'indicacao', 'ativo = 1'),
        ('projeto_documento', 'projeto_documento', 'ativo = 1'),
        ('acesso_grupo', 'acesso_grupo', 'ativo = 1'),
        ('projeto_arquivamento', 'projeto_arquivamento', 'ativo = 1'),
    ]
    
    total_migrated = 0
    total_errors = 0
    
    for mysql_table, pg_table, where_clause in tables_to_migrate:
        try:
            count, errors = migrate_table_auto(
                mysql_engine, pg_engine, 
                mysql_table, pg_table, 
                where_clause
            )
            total_migrated += count
            total_errors += errors
        except Exception as e:
            print(f"   ❌ Erro fatal: {str(e)[:150]}")
            total_errors += 1
    
    print("\n" + "=" * 70)
    print("📊 RESUMO FINAL")
    print("=" * 70)
    print(f"\n✅ Total migrado: {total_migrated} registros")
    print(f"⚠️  Total de erros: {total_errors}")
    
    if total_migrated > 0:
        print("\n🎉 Migração concluída!")
        print("\n💡 Próximos passos:")
        print("   1. Verificar dados: python check_migrated_data.py")
        print("   2. Criar views restantes: python create_remaining_views.py")
        print("   3. Testar API: uvicorn app.main:app --reload")
    
    mysql_engine.dispose()
    pg_engine.dispose()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Migração cancelada pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
