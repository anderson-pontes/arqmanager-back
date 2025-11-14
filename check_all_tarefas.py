"""Script para verificar todas as tarefas no banco"""
from sqlalchemy import text
from app.database import engine

def check_all_tarefas():
    """Verifica todas as tarefas no banco"""
    
    with engine.connect() as conn:
        # Contar tarefas totais
        result = conn.execute(text("SELECT COUNT(*) FROM tarefas"))
        total_tarefas = result.scalar()
        print(f"Total de tarefas no banco: {total_tarefas}")
        
        # Contar por escritório
        result = conn.execute(text("""
            SELECT escritorio_id, COUNT(*) 
            FROM tarefas 
            GROUP BY escritorio_id
            ORDER BY escritorio_id
        """))
        
        print("\nTarefas por escritorio:")
        for row in result:
            esc_id = row[0] if row[0] else 'NULL'
            count = row[1]
            print(f"  Escritorio {esc_id}: {count} tarefas")
        
        # Verificar tarefas sem escritorio_id
        result = conn.execute(text("SELECT COUNT(*) FROM tarefas WHERE escritorio_id IS NULL"))
        tarefas_sem_escritorio = result.scalar()
        print(f"\nTarefas sem escritorio_id: {tarefas_sem_escritorio}")
        
        # Verificar tarefas do escritório 1
        result = conn.execute(text("SELECT COUNT(*) FROM tarefas WHERE escritorio_id = 1"))
        tarefas_esc_1 = result.scalar()
        print(f"Tarefas do escritorio 1: {tarefas_esc_1}")
        
        # Listar algumas tarefas para verificar
        if total_tarefas > 0:
            print("\nPrimeiras 10 tarefas:")
            result = conn.execute(text("""
                SELECT id, etapa_id, nome, escritorio_id
                FROM tarefas
                ORDER BY id
                LIMIT 10
            """))
            
            for row in result:
                tarefa_id = row[0]
                etapa_id = row[1]
                nome = row[2]
                esc_id = row[3] if row[3] else 'NULL'
                print(f"  Tarefa {tarefa_id}: {nome} (Etapa: {etapa_id}, Escritorio: {esc_id})")
        
        # Verificar etapas do escritório 1
        result = conn.execute(text("""
            SELECT COUNT(*) FROM etapas WHERE escritorio_id = 1
        """))
        etapas_esc_1 = result.scalar()
        print(f"\nEtapas do escritorio 1: {etapas_esc_1}")
        
        # Verificar se há etapas sem tarefas
        result = conn.execute(text("""
            SELECT e.id, e.nome, e.servico_id
            FROM etapas e
            LEFT JOIN tarefas t ON t.etapa_id = e.id
            WHERE e.escritorio_id = 1 AND t.id IS NULL
            LIMIT 5
        """))
        
        etapas_sem_tarefas = list(result)
        if etapas_sem_tarefas:
            print(f"\nPrimeiras 5 etapas sem tarefas no escritorio 1:")
            for etapa in etapas_sem_tarefas:
                print(f"  Etapa {etapa[0]}: {etapa[1]} (Servico: {etapa[2]})")

if __name__ == "__main__":
    check_all_tarefas()

