"""Script para corrigir escritorio_id em serviços, etapas e tarefas após migração"""
from sqlalchemy import text
from app.database import engine

def fix_escritorio_ids():
    """Corrige escritorio_id em serviços, etapas e tarefas"""
    
    with engine.connect() as conn:
        # 1. Verificar quantos escritórios existem
        result = conn.execute(text("SELECT COUNT(*) FROM escritorio"))
        total_escritorios = result.scalar()
        
        if total_escritorios == 0:
            print("ERRO: Nenhum escritorio encontrado!")
            return
        
        # 2. Se houver apenas um escritório, associar tudo a ele
        if total_escritorios == 1:
            result = conn.execute(text("SELECT id FROM escritorio LIMIT 1"))
            escritorio_id = result.scalar()
            print(f"Encontrado 1 escritorio (ID: {escritorio_id}). Associando todos os servicos a ele...")
            
            # Atualizar serviços sem escritorio_id
            result = conn.execute(text("""
                UPDATE servicos 
                SET escritorio_id = :escritorio_id 
                WHERE escritorio_id IS NULL
            """), {'escritorio_id': escritorio_id})
            servicos_atualizados = result.rowcount
            print(f"  - {servicos_atualizados} servicos atualizados")
            
            # Atualizar etapas sem escritorio_id (baseado no servico)
            result = conn.execute(text("""
                UPDATE etapas 
                SET escritorio_id = (
                    SELECT escritorio_id 
                    FROM servicos 
                    WHERE servicos.id = etapas.servico_id
                )
                WHERE escritorio_id IS NULL
            """))
            etapas_atualizadas = result.rowcount
            print(f"  - {etapas_atualizadas} etapas atualizadas")
            
            # Atualizar tarefas sem escritorio_id (baseado na etapa)
            result = conn.execute(text("""
                UPDATE tarefas 
                SET escritorio_id = (
                    SELECT escritorio_id 
                    FROM etapas 
                    WHERE etapas.id = tarefas.etapa_id
                )
                WHERE escritorio_id IS NULL
            """))
            tarefas_atualizadas = result.rowcount
            print(f"  - {tarefas_atualizadas} tarefas atualizadas")
            
            conn.commit()
            print(f"\nOK: Todos os registros associados ao escritorio {escritorio_id}")
            
        else:
            # 3. Se houver múltiplos escritórios, associar todos os serviços a TODOS os escritórios
            print(f"Encontrados {total_escritorios} escritorios.")
            print("Associando servicos a TODOS os escritorios...")
            
            # Buscar todos os escritórios
            result = conn.execute(text("SELECT id FROM escritorio ORDER BY id"))
            escritorios = [row[0] for row in result]
            
            # Buscar todos os serviços sem escritorio_id
            result = conn.execute(text("SELECT id FROM servicos WHERE escritorio_id IS NULL"))
            servicos_sem_escritorio = [row[0] for row in result]
            
            if not servicos_sem_escritorio:
                print("Nenhum servico sem escritorio_id encontrado.")
                return
            
            print(f"Encontrados {len(servicos_sem_escritorio)} servicos sem escritorio_id")
            print(f"Associando cada servico a {len(escritorios)} escritorios...")
            
            # Para cada serviço, criar uma cópia para cada escritório
            # Mas primeiro, vamos verificar se devemos duplicar ou associar ao primeiro
            # Por enquanto, vamos associar todos ao primeiro escritório para não duplicar
            primeiro_escritorio = escritorios[0]
            
            # Atualizar serviços sem escritorio_id para o primeiro escritório
            result = conn.execute(text("""
                UPDATE servicos 
                SET escritorio_id = :escritorio_id 
                WHERE escritorio_id IS NULL
            """), {'escritorio_id': primeiro_escritorio})
            servicos_atualizados = result.rowcount
            print(f"  - {servicos_atualizados} servicos associados ao escritorio {primeiro_escritorio}")
            
            # Atualizar etapas sem escritorio_id (baseado no servico)
            result = conn.execute(text("""
                UPDATE etapas 
                SET escritorio_id = (
                    SELECT escritorio_id 
                    FROM servicos 
                    WHERE servicos.id = etapas.servico_id
                )
                WHERE escritorio_id IS NULL
            """))
            etapas_atualizadas = result.rowcount
            print(f"  - {etapas_atualizadas} etapas atualizadas")
            
            # Atualizar tarefas sem escritorio_id (baseado na etapa)
            result = conn.execute(text("""
                UPDATE tarefas 
                SET escritorio_id = (
                    SELECT escritorio_id 
                    FROM etapas 
                    WHERE etapas.id = tarefas.etapa_id
                )
                WHERE escritorio_id IS NULL
            """))
            tarefas_atualizadas = result.rowcount
            print(f"  - {tarefas_atualizadas} tarefas atualizadas")
            
            conn.commit()
            print(f"\nOK: Todos os registros associados ao escritorio {primeiro_escritorio}")
            print("\nNOTA: Se voce precisar associar servicos a escritorios especificos,")
            print("      execute manualmente via SQL ou crie um script de mapeamento.")

if __name__ == "__main__":
    fix_escritorio_ids()

