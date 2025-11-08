#!/usr/bin/env python3
"""
Script para verificar todos os objetos do banco MySQL
(views, procedures, functions, triggers)
"""
from sqlalchemy import create_engine, text

MYSQL_URL = "mysql+pymysql://root:xpto1661WIN@localhost:3306/dbarqmanager"

def check_all_objects():
    """Verifica todos os objetos do banco"""
    engine = create_engine(MYSQL_URL)
    
    print("=" * 70)
    print("🔍 ANÁLISE COMPLETA DO BANCO MYSQL")
    print("=" * 70)
    
    with engine.connect() as conn:
        # 1. VIEWS
        print("\n📊 VIEWS:")
        print("-" * 70)
        result = conn.execute(text("SHOW FULL TABLES WHERE Table_type = 'VIEW'"))
        views = [row[0] for row in result]
        print(f"Total: {len(views)} views")
        
        migrated_views = ['v_cliente', 'v_projeto', 'v_proposta', 'v_movimento', 'v_servico_etapa', 'v_colaborador']
        
        print("\n✅ Views já migradas (6):")
        for view in migrated_views:
            print(f"   ✅ {view}")
        
        print(f"\n⚠️  Views NÃO migradas ({len(views) - len(migrated_views)}):")
        for view in views:
            if view not in migrated_views:
                print(f"   ⚠️  {view}")
        
        # 2. STORED PROCEDURES
        print("\n\n🔧 STORED PROCEDURES:")
        print("-" * 70)
        result = conn.execute(text("SHOW PROCEDURE STATUS WHERE Db = 'dbarqmanager'"))
        procedures = [row[1] for row in result]
        print(f"Total: {len(procedures)} procedures")
        
        if procedures:
            for proc in procedures:
                print(f"   📌 {proc}")
                # Mostrar definição
                try:
                    result = conn.execute(text(f"SHOW CREATE PROCEDURE {proc}"))
                    definition = result.fetchone()
                    if definition:
                        print(f"      Definição: {definition[2][:100]}...")
                except:
                    pass
        else:
            print("   ✅ Nenhuma procedure encontrada")
        
        # 3. FUNCTIONS
        print("\n\n⚙️  FUNCTIONS:")
        print("-" * 70)
        result = conn.execute(text("SHOW FUNCTION STATUS WHERE Db = 'dbarqmanager'"))
        functions = [row[1] for row in result]
        print(f"Total: {len(functions)} functions")
        
        if functions:
            for func in functions:
                print(f"   📌 {func}")
        else:
            print("   ✅ Nenhuma function encontrada")
        
        # 4. TRIGGERS
        print("\n\n⚡ TRIGGERS:")
        print("-" * 70)
        result = conn.execute(text("SHOW TRIGGERS"))
        triggers = [row[0] for row in result]
        print(f"Total: {len(triggers)} triggers")
        
        if triggers:
            for trigger in triggers:
                print(f"   📌 {trigger}")
        else:
            print("   ✅ Nenhum trigger encontrado")
        
        # 5. TABELAS
        print("\n\n📋 TABELAS:")
        print("-" * 70)
        result = conn.execute(text("SHOW FULL TABLES WHERE Table_type = 'BASE TABLE'"))
        tables = [row[0] for row in result]
        print(f"Total: {len(tables)} tabelas")
        
        migrated_tables = ['status', 'cliente', 'servico', 'servico_etapa', 'proposta', 'projeto', 'movimento', 'colaborador']
        
        print("\n✅ Tabelas principais migradas (8):")
        for table in migrated_tables:
            if table in tables:
                print(f"   ✅ {table}")
        
        print(f"\n⚠️  Tabelas NÃO migradas ({len(tables) - len(migrated_tables)}):")
        not_migrated = []
        for table in tables:
            if table not in migrated_tables:
                not_migrated.append(table)
                # Contar registros
                try:
                    result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = result.scalar()
                    print(f"   ⚠️  {table} ({count} registros)")
                except:
                    print(f"   ⚠️  {table}")
        
        # RESUMO
        print("\n\n" + "=" * 70)
        print("📊 RESUMO DA ANÁLISE")
        print("=" * 70)
        print(f"\n✅ Objetos Migrados:")
        print(f"   - 6 views principais")
        print(f"   - 8 tabelas principais")
        print(f"   - 1.485 registros de dados")
        
        print(f"\n⚠️  Objetos NÃO Migrados:")
        print(f"   - {len(views) - 6} views secundárias")
        print(f"   - {len(procedures)} stored procedures")
        print(f"   - {len(functions)} functions")
        print(f"   - {len(triggers)} triggers")
        print(f"   - {len(not_migrated)} tabelas auxiliares")
        
        print("\n💡 RECOMENDAÇÕES:")
        print("-" * 70)
        
        if len(procedures) > 0:
            print("⚠️  PROCEDURES: Precisam ser reescritas em Python/FastAPI")
            print("   - Lógica de negócio deve estar nos services")
            print("   - Não use procedures no PostgreSQL")
        
        if len(functions) > 0:
            print("⚠️  FUNCTIONS: Reescrever como funções Python")
            print("   - Use helpers/utils no código")
        
        if len(triggers) > 0:
            print("⚠️  TRIGGERS: Avaliar necessidade")
            print("   - Prefira lógica explícita nos services")
            print("   - Use eventos do SQLAlchemy se necessário")
        
        if len(not_migrated) > 10:
            print("⚠️  TABELAS: Muitas tabelas não migradas")
            print("   - Verifique quais são essenciais")
            print("   - Migre conforme necessidade")
        
        print("\n✅ PRÓXIMOS PASSOS:")
        print("-" * 70)
        print("1. Revisar views não migradas e criar conforme necessidade")
        print("2. Converter procedures em services Python")
        print("3. Avaliar tabelas auxiliares importantes")
        print("4. Testar API com dados migrados")
        print("5. Ajustar endpoints conforme necessário")

if __name__ == "__main__":
    check_all_objects()
