"""
Script para testar autenticação completa
"""
import sys
sys.path.insert(0, '.')

from app.database import SessionLocal
from app.models.user import User
from app.core.security import verify_password, get_password_hash, create_access_token, decode_token
from datetime import timedelta

db = SessionLocal()

print("=" * 60)
print("TESTE COMPLETO DE AUTENTICAÇÃO")
print("=" * 60)

# 1. Verificar usuário
print("\n1. VERIFICANDO USUÁRIO")
print("-" * 60)
admin = db.query(User).filter(User.email == "admin@arqmanager.com").first()

if not admin:
    print("❌ Usuário não encontrado! Criando...")
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
    db.refresh(admin)
    print("✅ Usuário criado!")
else:
    print(f"✅ Usuário encontrado: {admin.nome}")

print(f"   ID: {admin.id}")
print(f"   Email: {admin.email}")
print(f"   Ativo: {admin.ativo}")
print(f"   Perfil: {admin.perfil}")

# 2. Testar senha
print("\n2. TESTANDO SENHA")
print("-" * 60)
senha_correta = verify_password("admin123", admin.senha)
print(f"Senha 'admin123': {'✅ CORRETA' if senha_correta else '❌ INCORRETA'}")

if not senha_correta:
    print("Atualizando senha...")
    admin.senha = get_password_hash("admin123")
    db.commit()
    print("✅ Senha atualizada!")

# 3. Criar token
print("\n3. CRIANDO TOKEN")
print("-" * 60)
token_data = {
    "sub": str(admin.id),
    "email": admin.email
}
access_token = create_access_token(token_data, expires_delta=timedelta(minutes=30))
print(f"Token criado: {access_token[:50]}...")

# 4. Decodificar token
print("\n4. DECODIFICANDO TOKEN")
print("-" * 60)
payload = decode_token(access_token)
if payload:
    print("✅ Token válido!")
    print(f"   sub: {payload.get('sub')}")
    print(f"   email: {payload.get('email')}")
    print(f"   type: {payload.get('type')}")
    print(f"   exp: {payload.get('exp')}")
else:
    print("❌ Token inválido!")

# 5. Simular validação do get_current_user
print("\n5. SIMULANDO VALIDAÇÃO")
print("-" * 60)

if payload is None:
    print("❌ Token inválido")
elif payload.get("type") != "access":
    print(f"❌ Tipo de token inválido: {payload.get('type')}")
else:
    user_id_str = payload.get("sub")
    if user_id_str is None:
        print("❌ Sub não encontrado no token")
    else:
        try:
            user_id = int(user_id_str)
            print(f"✅ User ID extraído: {user_id}")
            
            # Buscar usuário
            user = db.query(User).filter(User.id == user_id).first()
            if user is None:
                print(f"❌ Usuário {user_id} não encontrado no banco")
            elif not user.ativo:
                print(f"❌ Usuário {user_id} está inativo")
            else:
                print(f"✅ Usuário validado: {user.nome}")
                print(f"   ID: {user.id}")
                print(f"   Email: {user.email}")
                print(f"   Perfil: {user.perfil}")
        except (ValueError, TypeError) as e:
            print(f"❌ Erro ao converter user_id: {e}")

print("\n" + "=" * 60)
print("TOKEN PARA USAR NO SWAGGER:")
print("=" * 60)
print(access_token)
print("\n⚠️ COPIE O TOKEN ACIMA (SEM ASPAS) E COLE NO SWAGGER")

db.close()
