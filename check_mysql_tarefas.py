"""Script para verificar tarefas no MySQL"""
from sqlalchemy import create_engine, text
from load_mysql_config import load_mysql_url

def check_mysql_tarefas():
    """Verifica tarefas no MySQL"""
    
    mysql_url = load_mysql_url()
    if not mysql_url:
        print("ERRO: Nao foi possivel carregar URL do MySQL")
        return
    
    engine = create_engine(mysql_url)
    
    with engine.connect() as conn:
        # Contar tarefas no MySQL
        result = conn.execute(text("SELECT COUNT(*) FROM servico_microservico"))
        total = result.scalar()
        print(f"Total de tarefas no MySQL: {total}")
        
        # Listar algumas tarefas
        if total > 0:
            print("\nPrimeiras 10 tarefas:")
            result = conn.execute(text("""
                SELECT cod_microservico, cod_etapa, descricao, ordem
                FROM servico_microservico
                ORDER BY cod_etapa, ordem
                LIMIT 10
            """))
            
            for row in result:
                tarefa_id = row[0]
                etapa_id = row[1]
                descricao = row[2] or ''
                ordem = row[3] or 0
                print(f"  Tarefa {tarefa_id}: {descricao[:50]} (Etapa: {etapa_id}, Ordem: {ordem})")
        
        # Verificar quantas etapas têm tarefas
        result = conn.execute(text("""
            SELECT COUNT(DISTINCT cod_etapa) 
            FROM servico_microservico
        """))
        etapas_com_tarefas = result.scalar()
        print(f"\nEtapas com tarefas no MySQL: {etapas_com_tarefas}")

if __name__ == "__main__":
    check_mysql_tarefas()




