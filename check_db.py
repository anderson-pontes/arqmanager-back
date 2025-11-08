"""
Script para verificar conexão com banco e tabelas
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.database import engine, SessionLocal
from app.models.user import User, Escritorio
from sqlalchemy import inspect

def check_database():
    print("🔍 Verificando banco de dados...\n")
    
    try:
        # Testar conexão
        with engine.connect() as conn:
            print("✅ Conexão com banco OK!")
        
        # Verificar tabelas
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        print(f"\n📋 Tabelas encontradas ({len(tables)}):")
        for table in tables:
            print(f"   - {table}")
        
        # Verificar se tabelas necessárias existem
        required_tables = ['colaborador', 'escritorio', 'colaborador_escritorio']
        missing_tables = [t for t in required_tables if t not in tables]
        
        if missing_tables:
            print(f"\n❌ Tabelas faltando: {missing_tables}")
            print("\n💡 Execute:")
            print("   python create_migration.py")
            print("   alembic revision --autogenerate -m 'Initial migration'")
            print("   alembic upgrade head")
            return False
        
        print("\n✅ Todas as tabelas necessárias existem!")
        
        # Contar registros
        db = SessionLocal()
        try:
            user_count = db.query(User).count()
            esc_count = db.query(Escritorio).count()
            
            print(f"\n📊 Registros:")
            print(f"   Usuários: {user_count}")
            print(f"   Escritórios: {esc_count}")
            
            if user_count == 0:
                print("\n⚠️  Nenhum usuário cadastrado!")
                print("💡 Execute: python create_admin.py")
        finally:
            db.close()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    check_database()
