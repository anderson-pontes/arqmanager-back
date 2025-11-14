"""Script para corrigir a sequence do PostgreSQL para tarefas"""
from sqlalchemy import text
from app.database import engine

def fix_tarefas_sequence():
    """Corrige a sequence da tabela tarefas"""
    with engine.connect() as conn:
        # Verificar o maior ID atual
        result = conn.execute(text("SELECT MAX(id) FROM tarefas"))
        max_id = result.scalar() or 0
        
        print(f"Maior ID na tabela tarefas: {max_id}")
        
        # Resetar a sequence para o próximo valor
        next_id = max_id + 1
        
        # Verificar se a sequence existe
        result = conn.execute(text("""
            SELECT EXISTS (
                SELECT 1 FROM pg_class 
                WHERE relname = 'tarefas_id_seq'
            )
        """))
        sequence_exists = result.scalar()
        
        if not sequence_exists:
            print("AVISO: Sequence tarefas_id_seq nao existe. Criando...")
            # Criar a sequence
            conn.execute(text(f"CREATE SEQUENCE tarefas_id_seq START WITH {next_id}"))
            # Associar a sequence à coluna
            conn.execute(text("ALTER TABLE tarefas ALTER COLUMN id SET DEFAULT nextval('tarefas_id_seq')"))
            conn.execute(text("ALTER SEQUENCE tarefas_id_seq OWNED BY tarefas.id"))
        else:
            # Resetar a sequence existente (só se max_id > 0)
            if max_id > 0:
                conn.execute(text(f"SELECT setval('tarefas_id_seq', {max_id}, true)"))
            else:
                # Se não há registros, garantir que a sequence comece em 1
                conn.execute(text("SELECT setval('tarefas_id_seq', 1, false)"))
        
        conn.commit()
        
        print(f"OK: Sequence resetada para comecar em: {next_id}")
        
        # Verificar
        result = conn.execute(text("SELECT nextval('tarefas_id_seq')"))
        new_val = result.scalar()
        print(f"Proximo ID que sera usado: {new_val}")
        
        # Resetar novamente para o valor correto (já que nextval incrementou)
        if max_id > 0:
            conn.execute(text(f"SELECT setval('tarefas_id_seq', {max_id}, true)"))
        else:
            conn.execute(text("SELECT setval('tarefas_id_seq', 1, false)"))
        conn.commit()
        print(f"OK: Sequence configurada corretamente. Proximo ID sera: {next_id}")

if __name__ == "__main__":
    fix_tarefas_sequence()

