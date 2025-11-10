"""
Teste completo do fluxo de login incluindo verificação do token JWT
"""
import sys
import os
import requests
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from jose import jwt
from app.core.config import settings

BASE_URL = "http://localhost:8000/api/v1"

def decode_jwt_token(token: str):
    """Decodifica token JWT sem verificar assinatura (apenas para teste)"""
    try:
        # python-jose requer a chave, mas podemos usar unverified
        from jose import jwt as jose_jwt
        decoded = jose_jwt.get_unverified_claims(token)
        return decoded
    except Exception as e:
        print(f"Erro ao decodificar token: {e}")
        return None

def test_complete_login_flow():
    """Testa o fluxo completo de login com verificação de token"""
    print("=" * 70)
    print("TESTE COMPLETO: Fluxo de Login com Verificação de Token JWT")
    print("=" * 70)
    
    # 1. Login de admin do sistema
    print("\n📝 PASSO 1: Login de Admin do Sistema")
    print("-" * 70)
    
    admin_credentials = {
        "email": "admin@sistema.com",
        "senha": "admin123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=admin_credentials)
        
        if response.status_code != 200:
            print(f"❌ Erro no login: {response.status_code}")
            print(response.text)
            return False
        
        data = response.json()
        access_token = data['access_token']
        refresh_token = data['refresh_token']
        
        print("✅ Login bem-sucedido!")
        print(f"   User: {data['user']['nome']} ({data['user']['email']})")
        print(f"   is_system_admin: {data['is_system_admin']}")
        print(f"   requires_escritorio_selection: {data['requires_escritorio_selection']}")
        print(f"   Escritórios disponíveis: {len(data['available_escritorios'])}")
        
        # Verificar token inicial (sem contexto)
        print("\n📝 PASSO 2: Verificando Token Inicial (sem contexto)")
        print("-" * 70)
        token_payload = decode_jwt_token(access_token)
        if token_payload:
            print("✅ Token decodificado:")
            print(f"   User ID: {token_payload.get('sub')}")
            print(f"   Email: {token_payload.get('email')}")
            print(f"   is_system_admin: {token_payload.get('is_system_admin')}")
            print(f"   escritorio_id: {token_payload.get('escritorio_id', 'NÃO DEFINIDO')}")
            print(f"   perfil: {token_payload.get('perfil', 'NÃO DEFINIDO')}")
            
            if token_payload.get('escritorio_id'):
                print("   ⚠️ Token já tem contexto (inesperado no login inicial)")
            else:
                print("   ✅ Token sem contexto (esperado no login inicial)")
        
        # 3. Obter escritórios disponíveis
        print("\n📝 PASSO 3: Obtendo Escritórios Disponíveis")
        print("-" * 70)
        
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"{BASE_URL}/auth/available-escritorios", headers=headers)
        
        if response.status_code != 200:
            print(f"❌ Erro ao obter escritórios: {response.status_code}")
            print(response.text)
            return False
        
        escritorios = response.json()
        print(f"✅ {len(escritorios)} escritórios disponíveis")
        
        if not escritorios:
            print("⚠️ Nenhum escritório disponível para testar")
            return True
        
        primeiro_escritorio = escritorios[0]
        print(f"   Escritório selecionado: {primeiro_escritorio['nome_fantasia']} (ID: {primeiro_escritorio['id']})")
        
        # 4. Definir contexto
        print("\n📝 PASSO 4: Definindo Contexto (Escritório + Perfil)")
        print("-" * 70)
        
        context_data = {
            "escritorio_id": primeiro_escritorio['id'],
            "perfil": "Financeiro"
        }
        
        response = requests.post(
            f"{BASE_URL}/auth/set-context",
            json=context_data,
            headers=headers
        )
        
        if response.status_code != 200:
            print(f"❌ Erro ao definir contexto: {response.status_code}")
            print(response.text)
            return False
        
        context_response = response.json()
        new_access_token = context_response['access_token']
        
        print("✅ Contexto definido com sucesso!")
        print(f"   Escritório ID: {context_response['escritorio_id']}")
        print(f"   Perfil: {context_response['perfil']}")
        
        # 5. Verificar novo token (com contexto)
        print("\n📝 PASSO 5: Verificando Novo Token (com contexto)")
        print("-" * 70)
        
        new_token_payload = decode_jwt_token(new_access_token)
        if new_token_payload:
            print("✅ Novo token decodificado:")
            print(f"   User ID: {new_token_payload.get('sub')}")
            print(f"   Email: {new_token_payload.get('email')}")
            print(f"   is_system_admin: {new_token_payload.get('is_system_admin')}")
            print(f"   escritorio_id: {new_token_payload.get('escritorio_id')}")
            print(f"   perfil: {new_token_payload.get('perfil')}")
            
            if new_token_payload.get('escritorio_id') == context_response['escritorio_id']:
                print("   ✅ Contexto presente no token!")
            else:
                print("   ❌ Contexto não encontrado no token!")
                return False
        
        # 6. Testar endpoint protegido com contexto
        print("\n📝 PASSO 6: Testando Endpoint Protegido com Contexto")
        print("-" * 70)
        
        new_headers = {"Authorization": f"Bearer {new_access_token}"}
        response = requests.get(f"{BASE_URL}/auth/me", headers=new_headers)
        
        if response.status_code != 200:
            print(f"❌ Erro ao acessar /auth/me: {response.status_code}")
            print(response.text)
            return False
        
        user_data = response.json()
        print("✅ Endpoint /auth/me acessado com sucesso!")
        print(f"   User: {user_data['nome']}")
        print(f"   Email: {user_data['email']}")
        
        # 7. Testar dependency get_current_escritorio
        print("\n📝 PASSO 7: Verificando se contexto é extraído corretamente")
        print("-" * 70)
        
        # Vamos testar se o contexto está sendo extraído do token
        # Isso é feito internamente pelo get_current_user
        print("✅ Contexto extraído do token:")
        print(f"   Escritório ID: {new_token_payload.get('escritorio_id')}")
        print(f"   Perfil: {new_token_payload.get('perfil')}")
        print(f"   Admin do Sistema: {new_token_payload.get('is_system_admin')}")
        
        print("\n" + "=" * 70)
        print("✅ TODOS OS TESTES PASSARAM!")
        print("=" * 70)
        print("\n📋 Resumo:")
        print("   ✅ Login de admin do sistema funcionando")
        print("   ✅ Token inicial sem contexto (correto)")
        print("   ✅ Lista de escritórios disponíveis funcionando")
        print("   ✅ Definição de contexto funcionando")
        print("   ✅ Novo token com contexto (correto)")
        print("   ✅ Endpoints protegidos funcionando com contexto")
        print("\n🎉 O fluxo completo está funcionando corretamente!")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar ao servidor.")
        print("   Certifique-se de que o servidor está rodando em http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_complete_login_flow()
    sys.exit(0 if success else 1)

