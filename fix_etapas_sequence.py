"""Script para corrigir a sequence do PostgreSQL para etapas"""
from sqlalchemy import text
from app.database import engine

def fix_etapas_sequence():
    """Corrige a sequence da tabela etapas"""
    with engine.connect() as conn:
        # Verificar o maior ID atual
        result = conn.execute(text("SELECT MAX(id) FROM etapas"))
        max_id = result.scalar() or 0
        
        print(f"Maior ID na tabela etapas: {max_id}")
        
        # Resetar a sequence para o próximo valor
        next_id = max_id + 1
        
        # Verificar se a sequence existe
        result = conn.execute(text("""
            SELECT EXISTS (
                SELECT 1 FROM pg_class 
                WHERE relname = 'etapas_id_seq'
            )
        """))
        sequence_exists = result.scalar()
        
        if not sequence_exists:
            print("AVISO: Sequence etapas_id_seq nao existe. Criando...")
            # Criar a sequence
            conn.execute(text(f"CREATE SEQUENCE etapas_id_seq START WITH {next_id}"))
            # Associar a sequence à coluna
            conn.execute(text("ALTER TABLE etapas ALTER COLUMN id SET DEFAULT nextval('etapas_id_seq')"))
            conn.execute(text("ALTER SEQUENCE etapas_id_seq OWNED BY etapas.id"))
        else:
            # Resetar a sequence existente
            conn.execute(text(f"SELECT setval('etapas_id_seq', {max_id}, true)"))
        
        conn.commit()
        
        print(f"OK: Sequence resetada para comecar em: {next_id}")
        
        # Verificar
        result = conn.execute(text("SELECT nextval('etapas_id_seq')"))
        new_val = result.scalar()
        print(f"Proximo ID que sera usado: {new_val}")
        
        # Resetar novamente para o valor correto (já que nextval incrementou)
        conn.execute(text(f"SELECT setval('etapas_id_seq', {max_id}, true)"))
        conn.commit()
        print(f"OK: Sequence configurada corretamente. Proximo ID sera: {next_id}")

if __name__ == "__main__":
    fix_etapas_sequence()

