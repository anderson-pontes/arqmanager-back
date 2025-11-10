"""
Script para atualizar usuário existente para administrador do sistema
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.repositories.user import UserRepository
from app.models.user import User


def fix_admin():
    """Atualiza o usuário admin@sistema.com para ser admin do sistema"""
    db: Session = SessionLocal()
    
    try:
        user_repo = UserRepository(db)
        
        print("=" * 60)
        print("Atualizando Administrador do Sistema")
        print("=" * 60)
        
        # Buscar usuário por email
        admin_email = "admin@sistema.com"
        user = user_repo.get_by_email(admin_email)
        
        if not user:
            print(f"❌ Usuário com email {admin_email} não encontrado")
            return False
        
        print(f"\n📝 Usuário encontrado:")
        print(f"   ID: {user.id}")
        print(f"   Nome: {user.nome}")
        print(f"   Email: {user.email}")
        print(f"   Perfil atual: {user.perfil}")
        print(f"   Admin do Sistema atual: {user.is_system_admin}")
        
        # Atualizar
        user.is_system_admin = True
        user.perfil = "Admin"
        
        db.commit()
        db.refresh(user)
        
        print(f"\n✅ Usuário atualizado com sucesso!")
        print(f"   ID: {user.id}")
        print(f"   Nome: {user.nome}")
        print(f"   Email: {user.email}")
        print(f"   Perfil: {user.perfil}")
        print(f"   Admin do Sistema: {user.is_system_admin}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()
        db.rollback()
        return False
    finally:
        db.close()


if __name__ == "__main__":
    fix_admin()

