"""Script para verificar colaboradores migrados"""
from sqlalchemy import text
from app.database import engine

def check_colaboradores_migrados():
    """Verifica colaboradores migrados"""
    
    with engine.connect() as conn:
        # Contar colaboradores
        result = conn.execute(text("SELECT COUNT(*) FROM colaborador"))
        total = result.scalar()
        print(f"Total de colaboradores no PostgreSQL: {total}")
        
        # Contar relacionamentos
        result = conn.execute(text("SELECT COUNT(*) FROM colaborador_escritorio"))
        total_rel = result.scalar()
        print(f"Total de relacionamentos colaborador-escritorio: {total_rel}")
        
        # Listar colaboradores por escritório
        result = conn.execute(text("""
            SELECT 
                e.id as escritorio_id,
                e.nome_fantasia,
                COUNT(DISTINCT ce.colaborador_id) as total_colaboradores
            FROM escritorio e
            LEFT JOIN colaborador_escritorio ce ON ce.escritorio_id = e.id
            GROUP BY e.id, e.nome_fantasia
            ORDER BY e.id
        """))
        
        print("\nColaboradores por escritorio:")
        for row in result:
            esc_id = row[0]
            esc_nome = row[1]
            total_colab = row[2]
            print(f"  Escritorio {esc_id} ({esc_nome}): {total_colab} colaboradores")
        
        # Listar alguns colaboradores
        if total > 0:
            print("\nPrimeiros 10 colaboradores:")
            result = conn.execute(text("""
                SELECT id, nome, email, cpf, ativo
                FROM colaborador
                ORDER BY id
                LIMIT 10
            """))
            
            for row in result:
                colab_id = row[0]
                nome = row[1]
                email = row[2] or ''
                cpf = row[3] or ''
                ativo = row[4]
                print(f"  Colaborador {colab_id}: {nome} ({email}) - CPF: {cpf} - Ativo: {ativo}")

if __name__ == "__main__":
    check_colaboradores_migrados()





