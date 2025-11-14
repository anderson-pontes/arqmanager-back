"""Script para testar o endpoint de colaboradores"""
from sqlalchemy import text
from app.database import engine
from app.models.user import User
from app.schemas.user import UserResponse

def test_colaboradores():
    """Testa a listagem de colaboradores"""
    
    with engine.connect() as conn:
        # Testar query básica
        result = conn.execute(text("""
            SELECT u.id, u.nome, u.email, u.cpf, u.ativo
            FROM colaborador u
            JOIN colaborador_escritorio ce ON ce.colaborador_id = u.id
            WHERE ce.escritorio_id = 1
            LIMIT 5
        """))
        
        print("Colaboradores do escritorio 1:")
        for row in result:
            print(f"  ID: {row[0]}, Nome: {row[1]}, Email: {row[2]}, CPF: {row[3]}, Ativo: {row[4]}")
        
        # Verificar se há problemas com CPF NULL
        result = conn.execute(text("""
            SELECT COUNT(*) FROM colaborador WHERE cpf IS NULL
        """))
        null_cpf_count = result.scalar()
        print(f"\nColaboradores com CPF NULL: {null_cpf_count}")
        
        # Verificar se há problemas com perfil
        result = conn.execute(text("""
            SELECT DISTINCT perfil FROM colaborador
        """))
        perfis = [row[0] for row in result]
        print(f"Perfis encontrados: {perfis}")
        
        # Verificar relacionamentos
        result = conn.execute(text("""
            SELECT COUNT(*) FROM colaborador_escritorio WHERE escritorio_id = 1
        """))
        rel_count = result.scalar()
        print(f"Relacionamentos com escritorio 1: {rel_count}")

if __name__ == "__main__":
    test_colaboradores()

