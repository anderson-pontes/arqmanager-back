"""
Teste de todos os cenários de login
"""
import sys
import os
import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from jose import jwt as jose_jwt

BASE_URL = "http://localhost:8000/api/v1"

def decode_token(token: str):
    """Decodifica token sem verificar"""
    try:
        return jose_jwt.get_unverified_claims(token)
    except:
        return None

def test_scenario(name: str, email: str, senha: str):
    """Testa um cenário de login"""
    print(f"\n{'='*70}")
    print(f"TESTE: {name}")
    print(f"{'='*70}")
    
    try:
        # Login
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": email, "senha": senha}
        )
        
        if response.status_code != 200:
            print(f"❌ Login falhou: {response.status_code}")
            print(response.text)
            return False
        
        data = response.json()
        token = data['access_token']
        payload = decode_token(token)
        
        print(f"✅ Login bem-sucedido!")
        print(f"   User: {data['user']['nome']}")
        print(f"   is_system_admin: {data['is_system_admin']}")
        print(f"   requires_escritorio_selection: {data['requires_escritorio_selection']}")
        print(f"   Escritórios disponíveis: {len(data['available_escritorios'])}")
        print(f"   Token tem contexto: {'escritorio_id' in payload if payload else 'N/A'}")
        
        # Se precisa selecionar, testar set-context
        if data['requires_escritorio_selection'] and data['available_escritorios']:
            print(f"\n   Testando set-context...")
            esc = data['available_escritorios'][0]
            perfil = esc.get('perfil') or 'Colaborador'
            
            headers = {"Authorization": f"Bearer {token}"}
            context_response = requests.post(
                f"{BASE_URL}/auth/set-context",
                json={"escritorio_id": esc['id'], "perfil": perfil},
                headers=headers
            )
            
            if context_response.status_code == 200:
                new_token = context_response.json()['access_token']
                new_payload = decode_token(new_token)
                print(f"   ✅ Contexto definido!")
                print(f"      Escritório ID: {new_payload.get('escritorio_id')}")
                print(f"      Perfil: {new_payload.get('perfil')}")
            else:
                print(f"   ❌ Erro ao definir contexto: {context_response.text}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Executa todos os testes"""
    print("="*70)
    print("TESTE COMPLETO: Todos os Cenários de Login")
    print("="*70)
    
    results = []
    
    # Teste 1: Admin do sistema
    results.append((
        "Admin do Sistema",
        test_scenario(
            "Admin do Sistema",
            "admin@sistema.com",
            "admin123"
        )
    ))
    
    # Teste 2: Verificar se há usuários comuns no banco
    print(f"\n{'='*70}")
    print("Buscando usuários comuns para teste...")
    print(f"{'='*70}")
    
    try:
        # Tentar fazer login com alguns emails comuns
        # (Isso depende dos dados no banco)
        print("⚠️ Para testar usuário comum, você precisa ter um usuário cadastrado")
        print("   que não seja admin do sistema e tenha pelo menos 1 escritório vinculado")
    except:
        pass
    
    # Resumo
    print(f"\n{'='*70}")
    print("RESUMO DOS TESTES")
    print(f"{'='*70}")
    
    for name, success in results:
        status = "✅ PASSOU" if success else "❌ FALHOU"
        print(f"{status}: {name}")
    
    all_passed = all(result[1] for result in results)
    
    print(f"\n{'='*70}")
    if all_passed:
        print("✅ TODOS OS TESTES PASSARAM!")
    else:
        print("❌ ALGUNS TESTES FALHARAM")
    print(f"{'='*70}")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)











