"""
Script simplificado para criar usuário admin
"""
import sys
import os
from datetime import date

sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash


def create_admin():
    db = SessionLocal()
    
    try:
        # Verificar se já existe admin
        existing = db.query(User).filter(User.email == "admin@arqmanager.com").first()
        if existing:
            print("❌ Usuário admin já existe!")
            print(f"\n📧 Email: {existing.email}")
            print("🔑 Senha: admin123 (se não foi alterada)")
            return
        
        # Criar usuário admin
        admin = User(
            nome="Administrador",
            email="admin@arqmanager.com",
            senha=get_password_hash("admin123"),
            cpf="00000000000",
            telefone="(00) 00000-0000",
            data_nascimento=date(1990, 1, 1),
            perfil="Admin",
            tipo="Geral",
            ativo=True
        )
        db.add(admin)
        db.commit()
        
        print("=" * 60)
        print("✅ USUÁRIO ADMIN CRIADO COM SUCESSO!")
        print("=" * 60)
        print("\n📧 Email: admin@arqmanager.com")
        print("🔑 Senha: admin123")
        print("\n⚠️  IMPORTANTE: Altere a senha após o primeiro login!")
        print("\n💡 Acesse: http://localhost:8000/docs")
        print("=" * 60)
        
    except Exception as e:
        db.rollback()
        print(f"❌ Erro ao criar admin: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    create_admin()
