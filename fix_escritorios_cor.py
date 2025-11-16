"""Script para corrigir campo cor dos escritórios"""
from sqlalchemy import text
from app.database import engine

def fix_escritorios_cor():
    """Corrige campo cor dos escritórios que estão NULL"""
    
    with engine.connect() as conn:
        # Atualizar escritórios com cor NULL
        result = conn.execute(text("""
            UPDATE escritorio 
            SET cor = '#6366f1'
            WHERE cor IS NULL OR cor = ''
        """))
        
        updated = result.rowcount
        print(f"Atualizados {updated} escritorios com cor padrao")
        
        conn.commit()
        print("OK: Cores dos escritorios corrigidas!")

if __name__ == "__main__":
    fix_escritorios_cor()




