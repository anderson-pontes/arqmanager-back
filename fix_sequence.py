"""Script para corrigir a sequence do PostgreSQL"""
from sqlalchemy import text
from app.database import engine

def fix_sequence():
    """Corrige a sequence da tabela cliente"""
    with engine.connect() as conn:
        # Verificar o maior ID atual
        result = conn.execute(text("SELECT MAX(id) FROM cliente"))
        max_id = result.scalar() or 0
        
        print(f"Maior ID na tabela cliente: {max_id}")
        
        # Resetar a sequence para o próximo valor
        next_id = max_id + 1
        conn.execute(text(f"ALTER SEQUENCE cliente_id_seq RESTART WITH {next_id}"))
        conn.commit()
        
        print(f"✅ Sequence resetada para começar em: {next_id}")
        
        # Verificar
        result = conn.execute(text("SELECT nextval('cliente_id_seq')"))
        new_val = result.scalar()
        print(f"Próximo ID que será usado: {new_val}")

if __name__ == "__main__":
    fix_sequence()
