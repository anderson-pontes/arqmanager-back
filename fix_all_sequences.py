"""Script para corrigir todas as sequences do PostgreSQL após migração"""
from sqlalchemy import text
from app.database import engine

def fix_all_sequences():
    """Corrige todas as sequences após migração"""
    tables = [
        ('escritorio', 'escritorio_id_seq'),
        ('servicos', 'servicos_id_seq'),
        ('etapas', 'etapas_id_seq'),
        ('tarefas', 'tarefas_id_seq'),
        ('colaborador', 'colaborador_id_seq'),
    ]
    
    with engine.connect() as conn:
        for table_name, sequence_name in tables:
            try:
                # Verificar o maior ID atual
                result = conn.execute(text(f"SELECT MAX(id) FROM {table_name}"))
                max_id = result.scalar() or 0
                
                if max_id == 0:
                    print(f"AVISO: Tabela {table_name} esta vazia, pulando...")
                    continue
                
                next_id = max_id + 1
                
                # Verificar se a sequence existe
                result = conn.execute(text("""
                    SELECT EXISTS (
                        SELECT 1 FROM pg_class 
                        WHERE relname = :seq_name
                    )
                """), {'seq_name': sequence_name})
                sequence_exists = result.scalar()
                
                if not sequence_exists:
                    print(f"AVISO: Sequence {sequence_name} nao existe. Criando...")
                    # Criar a sequence
                    conn.execute(text(f"CREATE SEQUENCE {sequence_name} START WITH {next_id}"))
                    # Associar a sequence à coluna
                    conn.execute(text(f"ALTER TABLE {table_name} ALTER COLUMN id SET DEFAULT nextval('{sequence_name}')"))
                    conn.execute(text(f"ALTER SEQUENCE {sequence_name} OWNED BY {table_name}.id"))
                else:
                    # Resetar a sequence existente
                    conn.execute(text(f"SELECT setval('{sequence_name}', {max_id}, true)"))
                
                conn.commit()
                
                print(f"OK: {table_name}: Sequence resetada para comecar em {next_id}")
                
            except Exception as e:
                print(f"ERRO ao corrigir sequence de {table_name}: {e}")
                conn.rollback()
        
        print("\nOK: Todas as sequences foram corrigidas!")

if __name__ == "__main__":
    fix_all_sequences()

