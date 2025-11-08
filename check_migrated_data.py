#!/usr/bin/env python3
"""
Script para verificar dados migrados no PostgreSQL
"""
from sqlalchemy import create_engine, text
from app.core.config import settings

def check_data():
    """Verifica dados migrados"""
    print("=" * 60)
    print("🔍 VERIFICAÇÃO DE DADOS MIGRADOS - PostgreSQL")
    print("=" * 60)
    
    try:
        engine = create_engine(settings.DATABASE_URL)
        
        with engine.connect() as conn:
            print("\n✅ Conectado ao PostgreSQL\n")
            
            print("📊 Contagem de registros:")
            
            tables = [
                ('status', 'Status'),
                ('cliente', 'Clientes'),
                ('servicos', 'Serviços'),
                ('etapas', 'Etapas'),
                ('propostas', 'Propostas'),
                ('projetos', 'Projetos'),
                ('movimentos', 'Movimentos'),
                ('colaborador', 'Colaboradores')
            ]
            
            total = 0
            for table, label in tables:
                try:
                    result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = result.scalar()
                    total += count
                    print(f"   ✅ {label}: {count} registros")
                except Exception as e:
                    print(f"   ⚠️  {label}: Tabela não existe ou erro")
            
            print(f"\n   📈 Total: {total} registros migrados")
            
            # Verificar alguns dados de exemplo
            print("\n📋 Exemplos de dados:")
            
            # Status
            try:
                result = conn.execute(text("SELECT id, descricao FROM status LIMIT 3"))
                rows = result.fetchall()
                if rows:
                    print("\n   Status:")
                    for row in rows:
                        print(f"      - [{row[0]}] {row[1]}")
            except:
                pass
            
            # Serviços
            try:
                result = conn.execute(text("SELECT id, nome FROM servicos LIMIT 3"))
                rows = result.fetchall()
                if rows:
                    print("\n   Serviços:")
                    for row in rows:
                        print(f"      - [{row[0]}] {row[1]}")
            except:
                pass
            
            # Clientes
            try:
                result = conn.execute(text("SELECT id, nome, tipo_pessoa FROM cliente LIMIT 3"))
                rows = result.fetchall()
                if rows:
                    print("\n   Clientes:")
                    for row in rows:
                        print(f"      - [{row[0]}] {row[1]} ({row[2]})")
            except:
                pass
            
            print("\n" + "=" * 60)
            print("✅ Verificação concluída!")
            print("=" * 60)
            
    except Exception as e:
        print(f"\n❌ Erro ao conectar no PostgreSQL:")
        print(f"   {e}")
        print("\n💡 Verifique:")
        print("   1. PostgreSQL está rodando")
        print("   2. Credenciais no .env estão corretas")
        print("   3. Migrations foram aplicadas: alembic upgrade head")

if __name__ == "__main__":
    check_data()
