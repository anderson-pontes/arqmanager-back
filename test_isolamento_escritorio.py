"""
Script de teste para validar isolamento por escritório
Cria múltiplos escritórios e verifica que os dados estão isolados
"""
import sys
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import Escritorio, User
from app.models.cliente import Cliente
from app.models.projeto import Projeto
from app.models.status import Status
from app.models.servico import Servico
from app.core.security import get_password_hash
from sqlalchemy import text


def criar_escritorio_teste(db: Session, nome: str, email: str) -> Escritorio:
    """Cria um escritório de teste"""
    escritorio = Escritorio(
        nome_fantasia=nome,
        razao_social=f"{nome} LTDA",
        email=email,
        cor="#6366f1",
        ativo=True
    )
    db.add(escritorio)
    db.flush()
    return escritorio


def criar_admin_escritorio(db: Session, escritorio_id: int, nome: str, email: str) -> User:
    """Cria um admin para o escritório"""
    admin = User(
        nome=nome,
        email=email,
        senha=get_password_hash("123456"),
        perfil="Admin",
        is_system_admin=False,
        ativo=True
    )
    db.add(admin)
    db.flush()
    
    # Vincular admin ao escritório
    db.execute(
        text("""
            INSERT INTO colaborador_escritorio (colaborador_id, escritorio_id, perfil, ativo)
            VALUES (:user_id, :escritorio_id, 'Admin', true)
        """),
        {"user_id": admin.id, "escritorio_id": escritorio_id}
    )
    
    return admin


def criar_cliente_teste(db: Session, escritorio_id: int, nome: str, email: str, identificacao: str) -> Cliente:
    """Cria um cliente de teste"""
    cliente = Cliente(
        nome=nome,
        email=email,
        identificacao=identificacao,
        tipo_pessoa="Física",
        telefone="11999999999",
        ativo=True,
        escritorio_id=escritorio_id
    )
    db.add(cliente)
    db.flush()
    return cliente


def criar_status_teste(db: Session, escritorio_id: int, descricao: str) -> Status:
    """Cria um status de teste"""
    status = Status(
        descricao=descricao,
        cor="#3b82f6",
        ativo=True,
        escritorio_id=escritorio_id
    )
    db.add(status)
    db.flush()
    return status


def testar_isolamento():
    """Testa o isolamento entre escritórios"""
    import time
    db: Session = SessionLocal()
    
    try:
        timestamp = int(time.time())
        print("=" * 60)
        print("TESTE DE ISOLAMENTO POR ESCRITÓRIO")
        print("=" * 60)
        
        # Criar dois escritórios
        print("\n1. Criando escritórios de teste...")
        escritorio1 = criar_escritorio_teste(db, f"Escritório A {timestamp}", f"escritorio_a_{timestamp}@test.com")
        escritorio2 = criar_escritorio_teste(db, f"Escritório B {timestamp}", f"escritorio_b_{timestamp}@test.com")
        db.commit()
        print(f"   ✓ Escritório 1 criado: ID {escritorio1.id} - {escritorio1.nome_fantasia}")
        print(f"   ✓ Escritório 2 criado: ID {escritorio2.id} - {escritorio2.nome_fantasia}")
        
        # Criar admins
        print("\n2. Criando administradores...")
        admin1 = criar_admin_escritorio(db, escritorio1.id, f"Admin A {timestamp}", f"admin_a_{timestamp}@test.com")
        admin2 = criar_admin_escritorio(db, escritorio2.id, f"Admin B {timestamp}", f"admin_b_{timestamp}@test.com")
        db.commit()
        print(f"   ✓ Admin 1 criado: ID {admin1.id} - {admin1.email}")
        print(f"   ✓ Admin 2 criado: ID {admin2.id} - {admin2.email}")
        
        # Criar clientes para cada escritório
        print("\n3. Criando clientes...")
        cliente1 = criar_cliente_teste(db, escritorio1.id, f"Cliente A1 {timestamp}", f"cliente_a1_{timestamp}@test.com", f"1111111{timestamp % 10000:04d}")
        cliente2 = criar_cliente_teste(db, escritorio1.id, f"Cliente A2 {timestamp}", f"cliente_a2_{timestamp}@test.com", f"2222222{timestamp % 10000:04d}")
        cliente3 = criar_cliente_teste(db, escritorio2.id, f"Cliente B1 {timestamp}", f"cliente_b1_{timestamp}@test.com", f"3333333{timestamp % 10000:04d}")
        db.commit()
        print(f"   ✓ Cliente 1 (Escritório A): ID {cliente1.id} - {cliente1.nome}")
        print(f"   ✓ Cliente 2 (Escritório A): ID {cliente2.id} - {cliente2.nome}")
        print(f"   ✓ Cliente 3 (Escritório B): ID {cliente3.id} - {cliente3.nome}")
        
        # Criar status para cada escritório
        print("\n4. Criando status...")
        status1 = criar_status_teste(db, escritorio1.id, "Status A1")
        status2 = criar_status_teste(db, escritorio1.id, "Status A2")
        status3 = criar_status_teste(db, escritorio2.id, "Status B1")
        db.commit()
        print(f"   ✓ Status 1 (Escritório A): ID {status1.id} - {status1.descricao}")
        print(f"   ✓ Status 2 (Escritório A): ID {status2.id} - {status2.descricao}")
        print(f"   ✓ Status 3 (Escritório B): ID {status3.id} - {status3.descricao}")
        
        # Testar isolamento - verificar que escritório 1 só vê seus dados
        print("\n5. Testando isolamento...")
        
        clientes_escritorio1 = db.query(Cliente).filter(Cliente.escritorio_id == escritorio1.id).all()
        clientes_escritorio2 = db.query(Cliente).filter(Cliente.escritorio_id == escritorio2.id).all()
        
        print(f"\n   Clientes do Escritório 1: {len(clientes_escritorio1)}")
        for c in clientes_escritorio1:
            print(f"      - {c.nome} (ID: {c.id})")
        
        print(f"\n   Clientes do Escritório 2: {len(clientes_escritorio2)}")
        for c in clientes_escritorio2:
            print(f"      - {c.nome} (ID: {c.id})")
        
        status_escritorio1 = db.query(Status).filter(Status.escritorio_id == escritorio1.id).all()
        status_escritorio2 = db.query(Status).filter(Status.escritorio_id == escritorio2.id).all()
        
        print(f"\n   Status do Escritório 1: {len(status_escritorio1)}")
        for s in status_escritorio1:
            print(f"      - {s.descricao} (ID: {s.id})")
        
        print(f"\n   Status do Escritório 2: {len(status_escritorio2)}")
        for s in status_escritorio2:
            print(f"      - {s.descricao} (ID: {s.id})")
        
        # Validações
        print("\n6. Validações...")
        erros = []
        
        # Verificar que escritório 1 tem 2 clientes
        if len(clientes_escritorio1) != 2:
            erros.append(f"Escritório 1 deveria ter 2 clientes, mas tem {len(clientes_escritorio1)}")
        
        # Verificar que escritório 2 tem 1 cliente
        if len(clientes_escritorio2) != 1:
            erros.append(f"Escritório 2 deveria ter 1 cliente, mas tem {len(clientes_escritorio2)}")
        
        # Verificar que escritório 1 tem 2 status
        if len(status_escritorio1) != 2:
            erros.append(f"Escritório 1 deveria ter 2 status, mas tem {len(status_escritorio1)}")
        
        # Verificar que escritório 2 tem 1 status
        if len(status_escritorio2) != 1:
            erros.append(f"Escritório 2 deveria ter 1 status, mas tem {len(status_escritorio2)}")
        
        # Verificar que não há clientes sem escritorio_id
        clientes_sem_escritorio = db.query(Cliente).filter(Cliente.escritorio_id.is_(None)).count()
        if clientes_sem_escritorio > 0:
            erros.append(f"Existem {clientes_sem_escritorio} clientes sem escritorio_id")
        
        if erros:
            print("\n   ❌ ERROS ENCONTRADOS:")
            for erro in erros:
                print(f"      - {erro}")
            return False
        else:
            print("\n   ✅ TODOS OS TESTES PASSARAM!")
            print("   ✓ Isolamento entre escritórios está funcionando corretamente")
            return True
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        return False
    finally:
        db.close()


if __name__ == "__main__":
    sucesso = testar_isolamento()
    sys.exit(0 if sucesso else 1)

