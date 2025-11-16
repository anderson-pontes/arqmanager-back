"""
Script para executar a migração do banco de dados
"""
import subprocess
import sys
import os

def run_migration():
    """Executa a migração do Alembic"""
    try:
        # Verificar status atual
        print("📊 Verificando status atual das migrações...")
        result = subprocess.run(
            ["alembic", "current"],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        print(result.stdout)
        if result.stderr:
            print("⚠️ Avisos:", result.stderr)
        
        # Executar migração
        print("\n🚀 Executando migração...")
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        if result.returncode == 0:
            print("✅ Migração executada com sucesso!")
            print(result.stdout)
        else:
            print("❌ Erro ao executar migração:")
            print(result.stderr)
            sys.exit(1)
            
        # Verificar status final
        print("\n📊 Status final:")
        result = subprocess.run(
            ["alembic", "current"],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        print(result.stdout)
        
    except FileNotFoundError:
        print("❌ Erro: Alembic não encontrado. Certifique-se de estar no ambiente virtual.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_migration()










