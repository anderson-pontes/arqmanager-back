"""Script para testar listagem de colaboradores"""
from sqlalchemy import text
from app.database import engine
from app.models.user import User, user_escritorio
from app.repositories.user import UserRepository
from app.services.user import UserService
from app.database import SessionLocal

def test_list_colaboradores():
    """Testa a listagem de colaboradores do escritório 1"""
    
    db = SessionLocal()
    try:
        service = UserService(db)
        
        # Testar listagem
        print("Testando listagem de colaboradores do escritorio 1...")
        colaboradores = service.get_all(escritorio_id=1, skip=0, limit=20)
        
        print(f"\nTotal retornado: {len(colaboradores)}")
        
        if len(colaboradores) > 0:
            print("\nPrimeiros colaboradores:")
            for colab in colaboradores[:5]:
                print(f"  - {colab.nome} ({colab.email}) - Perfil: {colab.perfil}")
        else:
            print("\nNenhum colaborador retornado!")
            
            # Verificar diretamente no banco
            print("\nVerificando diretamente no banco...")
            result = db.execute(text("""
                SELECT u.id, u.nome, u.email, u.perfil
                FROM colaborador u
                JOIN colaborador_escritorio ce ON ce.colaborador_id = u.id
                WHERE ce.escritorio_id = 1
                LIMIT 5
            """))
            
            print("Colaboradores encontrados no banco:")
            for row in result:
                print(f"  - ID {row[0]}: {row[1]} ({row[2]}) - Perfil: {row[3]}")
        
        # Testar contagem
        print("\nTestando contagem...")
        total = service.count(escritorio_id=1)
        print(f"Total de colaboradores: {total}")
        
    finally:
        db.close()

if __name__ == "__main__":
    test_list_colaboradores()




