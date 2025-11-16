"""
Script para verificar se a migração foi aplicada corretamente
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import inspect
from app.database import engine
from app.models.user import User

def verify_migration():
    """Verifica se a coluna is_system_admin foi criada"""
    try:
        inspector = inspect(engine)
        columns = [col['name'] for col in inspector.get_columns('colaborador')]
        
        if 'is_system_admin' in columns:
            print("✅ Coluna 'is_system_admin' encontrada na tabela 'colaborador'")
            
            # Verificar tipo e default
            for col in inspector.get_columns('colaborador'):
                if col['name'] == 'is_system_admin':
                    print(f"   Tipo: {col['type']}")
                    print(f"   Nullable: {col['nullable']}")
                    print(f"   Default: {col['default']}")
            return True
        else:
            print("❌ Coluna 'is_system_admin' NÃO encontrada!")
            print(f"Colunas existentes: {', '.join(columns)}")
            return False
    except Exception as e:
        print(f"❌ Erro ao verificar migração: {str(e)}")
        return False

if __name__ == "__main__":
    verify_migration()










