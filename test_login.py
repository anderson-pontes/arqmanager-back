"""
Script para testar login e debug
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal
from app.models.user import User
from app.core.security import verify_password, get_password_hash

def test_login():
    db = SessionLocal()
    
    try:
        # Buscar usuário admin
        user = db.query(User).filter(User.email == "admin@arqmanager.com").first()
        
        if not user:
            print("❌ Usuário não encontrado!")
            print("Execute: python create_admin.py")
            return
        
        print("✅ Usuário encontrado!")
        print(f"   ID: {user.id}")
        print(f"   Nome: {user.nome}")
        print(f"   Email: {user.email}")
        print(f"   Ativo: {user.ativo}")
        print(f"   Perfil: {user.perfil}")
        
        # Testar senha
        senha_teste = "admin123"
        senha_correta = verify_password(senha_teste, user.senha)
        
        print(f"\n🔑 Teste de senha:")
        print(f"   Senha testada: {senha_teste}")
        print(f"   Senha correta: {senha_correta}")
        
        if not senha_correta:
            print("\n⚠️  Senha incorreta! Atualizando...")
            user.senha = get_password_hash(senha_teste)
            db.commit()
            print("✅ Senha atualizada!")
        
        # Verificar escritórios
        print(f"\n🏢 Escritórios: {len(user.escritorios)}")
        for esc in user.escritorios:
            print(f"   - {esc.nome_fantasia}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_login()
