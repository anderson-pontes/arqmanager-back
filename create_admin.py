"""
Script para criar usuário admin inicial
Execute: python create_admin.py
"""
import sys
import os
from datetime import date

sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal
from app.models.user import User, Escritorio
from app.core.security import get_password_hash


def create_admin():
    db = SessionLocal()
    
    try:
        # Verificar se já existe admin
        existing = db.query(User).filter(User.email == "admin@arqmanager.com").first()
        if existing:
            print("❌ Usuário admin já existe!")
            return
        
        # Criar escritório padrão
        escritorio = Escritorio(
            nome_fantasia="ARQManager",
            razao_social="ARQManager Ltda",
            documento="00000000000000",
            email="contato@arqmanager.com",
            telefone="(00) 00000-0000",
            endereco="Endereço do escritório",
            cor="#6366f1"
        )
        db.add(escritorio)
        db.flush()
        
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
        db.flush()
        
        # Associar admin ao escritório
        admin.escritorios.append(escritorio)
        
        db.commit()
        
        print("✅ Usuário admin criado com sucesso!")
        print("\n📧 Email: admin@arqmanager.com")
        print("🔑 Senha: admin123")
        print("\n⚠️  IMPORTANTE: Altere a senha após o primeiro login!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Erro ao criar admin: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    create_admin()
