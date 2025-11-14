"""
Script para criar um administrador do sistema automaticamente
Uso: python scripts/create_system_admin_auto.py [--nome NOME] [--email EMAIL] [--cpf CPF] [--senha SENHA]
"""
import sys
import os
import argparse

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate
from app.core.security import get_password_hash


def create_system_admin(nome: str, email: str, cpf: str, senha: str):
    """Cria um administrador do sistema"""
    db: Session = SessionLocal()
    
    try:
        user_repo = UserRepository(db)
        
        print("=" * 50)
        print("Criação de Administrador do Sistema")
        print("=" * 50)
        print(f"Nome: {nome}")
        print(f"Email: {email}")
        print(f"CPF: {cpf}")
        print("=" * 50)
        
        # Validar senha
        if len(senha) < 6:
            print("❌ Erro: Senha deve ter no mínimo 6 caracteres")
            return False
        
        # Limpar CPF
        cpf_limpo = cpf.replace(".", "").replace("-", "").strip()
        
        if len(cpf_limpo) != 11:
            print("❌ Erro: CPF deve ter 11 dígitos")
            return False
        
        # Verificar se email já existe
        existing_user = user_repo.get_by_email(email)
        if existing_user:
            print(f"❌ Erro: Email {email} já está cadastrado")
            if existing_user.is_system_admin:
                print(f"   Este usuário já é um administrador do sistema!")
            return False
        
        # Verificar se CPF já existe
        existing_cpf = user_repo.get_by_cpf(cpf_limpo)
        if existing_cpf:
            print(f"❌ Erro: CPF {cpf_limpo} já está cadastrado")
            return False
        
        # Criar usuário admin do sistema
        admin_data = UserCreate(
            nome=nome,
            email=email,
            cpf=cpf_limpo,
            senha=senha,
            perfil="Admin",
            is_system_admin=True
        )
        
        admin = user_repo.create(admin_data)
        
        print("\n✅ Administrador do sistema criado com sucesso!")
        print(f"   ID: {admin.id}")
        print(f"   Nome: {admin.nome}")
        print(f"   Email: {admin.email}")
        print(f"   CPF: {admin.cpf}")
        print(f"   Perfil: {admin.perfil}")
        print(f"   Admin do Sistema: {admin.is_system_admin}")
        print("\n" + "=" * 50)
        print("⚠️  IMPORTANTE: Guarde estas credenciais com segurança!")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erro ao criar administrador: {str(e)}")
        import traceback
        traceback.print_exc()
        db.rollback()
        return False
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Criar administrador do sistema')
    parser.add_argument('--nome', type=str, help='Nome completo do administrador', default='Administrador do Sistema')
    parser.add_argument('--email', type=str, help='Email do administrador', required=True)
    parser.add_argument('--cpf', type=str, help='CPF do administrador (apenas números)', required=True)
    parser.add_argument('--senha', type=str, help='Senha do administrador (mínimo 6 caracteres)', required=True)
    
    args = parser.parse_args()
    
    success = create_system_admin(
        nome=args.nome,
        email=args.email,
        cpf=args.cpf,
        senha=args.senha
    )
    
    sys.exit(0 if success else 1)







