"""
Script para verificar e criar/atualizar administrador do sistema
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate
from app.core.security import get_password_hash


def check_and_create_admin():
    """Verifica se existe admin do sistema, caso contrário cria ou atualiza"""
    db: Session = SessionLocal()
    
    try:
        user_repo = UserRepository(db)
        
        print("=" * 60)
        print("Verificação e Criação de Administrador do Sistema")
        print("=" * 60)
        
        # Verificar se já existe admin do sistema
        from app.models.user import User
        existing_admin = db.query(User).filter(
            User.is_system_admin == True,
            User.ativo == True
        ).first()
        
        if existing_admin:
            print(f"\n✅ Já existe um administrador do sistema:")
            print(f"   ID: {existing_admin.id}")
            print(f"   Nome: {existing_admin.nome}")
            print(f"   Email: {existing_admin.email}")
            print(f"   Perfil: {existing_admin.perfil}")
            print(f"   Admin do Sistema: {existing_admin.is_system_admin}")
            return existing_admin
        
        # Verificar se existe usuário com email admin@sistema.com
        admin_email = "admin@sistema.com"
        existing_user = user_repo.get_by_email(admin_email)
        
        if existing_user:
            print(f"\n📝 Usuário encontrado com email {admin_email}")
            print(f"   Atualizando para administrador do sistema...")
            
            # Atualizar para admin do sistema
            existing_user.is_system_admin = True
            existing_user.perfil = "Admin"
            db.commit()
            db.refresh(existing_user)
            
            print(f"\n✅ Usuário atualizado com sucesso!")
            print(f"   ID: {existing_user.id}")
            print(f"   Nome: {existing_user.nome}")
            print(f"   Email: {existing_user.email}")
            print(f"   Perfil: {existing_user.perfil}")
            print(f"   Admin do Sistema: {existing_user.is_system_admin}")
            return existing_user
        
        # Criar novo admin do sistema
        print(f"\n📝 Criando novo administrador do sistema...")
        
        admin_data = UserCreate(
            nome="Administrador do Sistema",
            email=admin_email,
            cpf="99999999999",  # CPF diferente
            senha="admin123",
            perfil="Admin",
            is_system_admin=True
        )
        
        admin = user_repo.create(admin_data)
        
        print(f"\n✅ Administrador do sistema criado com sucesso!")
        print(f"   ID: {admin.id}")
        print(f"   Nome: {admin.nome}")
        print(f"   Email: {admin.email}")
        print(f"   CPF: {admin.cpf}")
        print(f"   Perfil: {admin.perfil}")
        print(f"   Admin do Sistema: {admin.is_system_admin}")
        print(f"\n⚠️  Credenciais padrão:")
        print(f"   Email: {admin_email}")
        print(f"   Senha: admin123")
        print(f"   ⚠️  IMPORTANTE: Altere a senha após o primeiro login!")
        
        return admin
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()
        db.rollback()
        return None
    finally:
        db.close()


if __name__ == "__main__":
    check_and_create_admin()







