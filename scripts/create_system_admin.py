"""
Script para criar um administrador do sistema
Uso: python scripts/create_system_admin.py
"""
import sys
import os

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate
from app.core.security import get_password_hash


def create_system_admin():
    """Cria um administrador do sistema"""
    db: Session = SessionLocal()
    
    try:
        user_repo = UserRepository(db)
        
        print("=" * 50)
        print("Criação de Administrador do Sistema")
        print("=" * 50)
        
        # Solicitar dados
        nome = input("Nome completo: ").strip()
        email = input("Email: ").strip()
        cpf = input("CPF (apenas números): ").strip().replace(".", "").replace("-", "")
        senha = input("Senha (mínimo 6 caracteres): ").strip()
        
        if len(senha) < 6:
            print("❌ Erro: Senha deve ter no mínimo 6 caracteres")
            return
        
        # Verificar se email já existe
        existing_user = user_repo.get_by_email(email)
        if existing_user:
            print(f"❌ Erro: Email {email} já está cadastrado")
            return
        
        # Verificar se CPF já existe
        existing_cpf = user_repo.get_by_cpf(cpf)
        if existing_cpf:
            print(f"❌ Erro: CPF {cpf} já está cadastrado")
            return
        
        # Criar usuário admin do sistema
        admin_data = UserCreate(
            nome=nome,
            email=email,
            cpf=cpf,
            senha=senha,
            perfil="Admin",
            is_system_admin=True
        )
        
        admin = user_repo.create(admin_data)
        
        print("\n✅ Administrador do sistema criado com sucesso!")
        print(f"   ID: {admin.id}")
        print(f"   Nome: {admin.nome}")
        print(f"   Email: {admin.email}")
        print(f"   Perfil: {admin.perfil}")
        print(f"   Admin do Sistema: {admin.is_system_admin}")
        
    except Exception as e:
        print(f"\n❌ Erro ao criar administrador: {str(e)}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_system_admin()












