"""
Script para verificar se o usuário admin existe
"""
import sys
sys.path.insert(0, '.')

from app.database import SessionLocal
from app.models.user import User
from app.core.security import verify_password, get_password_hash

db = SessionLocal()

print("=" * 60)
print("VERIFICANDO USUÁRIO ADMIN")
print("=" * 60)

# Buscar admin
admin = db.query(User).filter(User.email == "admin@arqmanager.com").first()

if admin:
    print(f"✅ Usuário encontrado!")
    print(f"ID: {admin.id}")
    print(f"Nome: {admin.nome}")
    print(f"Email: {admin.email}")
    print(f"CPF: {admin.cpf}")
    print(f"Perfil: {admin.perfil}")
    print(f"Ativo: {admin.ativo}")
    print(f"Senha Hash: {admin.senha[:50]}...")
    
    # Testar senha
    print("\n" + "=" * 60)
    print("TESTANDO SENHA")
    print("=" * 60)
    
    senha_correta = verify_password("admin123", admin.senha)
    print(f"Senha 'admin123' está correta: {senha_correta}")
    
    if not senha_correta:
        print("\n⚠️ SENHA INCORRETA! Atualizando...")
        admin.senha = get_password_hash("admin123")
        db.commit()
        print("✅ Senha atualizada para 'admin123'")
else:
    print("❌ Usuário admin NÃO encontrado!")
    print("\nCriando usuário admin...")
    
    admin = User(
        nome="Administrador",
        email="admin@arqmanager.com",
        senha=get_password_hash("admin123"),
        cpf="00000000000",
        perfil="Admin",
        ativo=True
    )
    db.add(admin)
    db.commit()
    print("✅ Usuário admin criado!")
    print(f"Email: admin@arqmanager.com")
    print(f"Senha: admin123")

db.close()
