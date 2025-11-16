"""
Script para testar o fluxo completo de login
"""
import sys
import os
import requests
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

BASE_URL = "http://localhost:8000/api/v1"

def test_login_flow():
    """Testa o fluxo completo de login"""
    print("=" * 60)
    print("TESTE: Fluxo Completo de Login")
    print("=" * 60)
    
    # 1. Testar login de admin do sistema
    print("\n1️⃣ Testando login de ADMIN DO SISTEMA")
    print("-" * 60)
    
    admin_credentials = {
        "email": "admin@sistema.com",
        "senha": "admin123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=admin_credentials)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Login bem-sucedido!")
            print(f"   User ID: {data['user']['id']}")
            print(f"   Nome: {data['user']['nome']}")
            print(f"   Email: {data['user']['email']}")
            print(f"   Perfil: {data['user']['perfil']}")
            print(f"   is_system_admin: {data['is_system_admin']}")
            print(f"   requires_escritorio_selection: {data['requires_escritorio_selection']}")
            print(f"   Escritórios disponíveis: {len(data['available_escritorios'])}")
            
            if data['available_escritorios']:
                print("\n   Escritórios disponíveis:")
                for esc in data['available_escritorios'][:3]:  # Mostrar apenas 3 primeiros
                    print(f"      - {esc['nome_fantasia']} (ID: {esc['id']})")
            
            access_token = data['access_token']
            refresh_token = data['refresh_token']
            
            # 2. Testar endpoint de escritórios disponíveis
            print("\n2️⃣ Testando GET /auth/available-escritorios")
            print("-" * 60)
            
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(f"{BASE_URL}/auth/available-escritorios", headers=headers)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                escritorios = response.json()
                print(f"✅ {len(escritorios)} escritórios disponíveis")
                if escritorios:
                    print(f"   Primeiro escritório: {escritorios[0]['nome_fantasia']}")
            
            # 3. Testar definição de contexto
            if data['available_escritorios']:
                print("\n3️⃣ Testando POST /auth/set-context")
                print("-" * 60)
                
                primeiro_escritorio = data['available_escritorios'][0]
                context_data = {
                    "escritorio_id": primeiro_escritorio['id'],
                    "perfil": "Financeiro"  # Admin pode escolher qualquer perfil
                }
                
                response = requests.post(
                    f"{BASE_URL}/auth/set-context",
                    json=context_data,
                    headers=headers
                )
                print(f"Status Code: {response.status_code}")
                
                if response.status_code == 200:
                    context_response = response.json()
                    print("✅ Contexto definido com sucesso!")
                    print(f"   Escritório ID: {context_response['escritorio_id']}")
                    print(f"   Perfil: {context_response['perfil']}")
                    print(f"   Novo access_token gerado")
                    
                    new_token = context_response['access_token']
                    
                    # 4. Testar endpoint protegido com contexto
                    print("\n4️⃣ Testando endpoint protegido com contexto")
                    print("-" * 60)
                    
                    new_headers = {"Authorization": f"Bearer {new_token}"}
                    response = requests.get(f"{BASE_URL}/auth/me", headers=new_headers)
                    print(f"Status Code: {response.status_code}")
                    
                    if response.status_code == 200:
                        user_data = response.json()
                        print("✅ Endpoint /auth/me funcionando com contexto!")
                        print(f"   User: {user_data['nome']}")
                else:
                    print(f"❌ Erro ao definir contexto: {response.text}")
            else:
                print("⚠️ Nenhum escritório disponível para testar contexto")
            
        else:
            print(f"❌ Erro no login: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar ao servidor.")
        print("   Certifique-se de que o servidor está rodando em http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "=" * 60)
    print("✅ Teste concluído!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    test_login_flow()










