"""
Teste específico para verificar se o perfil escolhido pelo admin é aplicado
"""
import sys
import os
import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from jose import jwt as jose_jwt

BASE_URL = "http://localhost:8000/api/v1"

def decode_token(token: str):
    try:
        return jose_jwt.get_unverified_claims(token)
    except:
        return None

def test_perfil_selection():
    """Testa se o admin pode escolher qualquer perfil"""
    print("="*70)
    print("TESTE: Seleção de Perfil pelo Admin do Sistema")
    print("="*70)
    
    # Login
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": "admin@sistema.com", "senha": "admin123"}
    )
    
    if response.status_code != 200:
        print(f"❌ Login falhou")
        return False
    
    data = response.json()
    token = data['access_token']
    headers = {"Authorization": f"Bearer {token}"}
    
    # Obter escritórios
    esc_response = requests.get(f"{BASE_URL}/auth/available-escritorios", headers=headers)
    escritorios = esc_response.json()
    
    if not escritorios:
        print("❌ Nenhum escritório disponível")
        return False
    
    escritorio_id = escritorios[0]['id']
    
    # Testar diferentes perfis
    perfis_para_testar = ["Admin", "Gerente", "Financeiro", "Técnico", "Colaborador"]
    
    print(f"\nEscritório selecionado: {escritorios[0]['nome_fantasia']} (ID: {escritorio_id})")
    print(f"\nTestando diferentes perfis:\n")
    
    for perfil in perfis_para_testar:
        print(f"  Testando perfil: {perfil}")
        
        context_response = requests.post(
            f"{BASE_URL}/auth/set-context",
            json={"escritorio_id": escritorio_id, "perfil": perfil},
            headers=headers
        )
        
        if context_response.status_code == 200:
            new_token = context_response.json()['access_token']
            payload = decode_token(new_token)
            
            perfil_no_token = payload.get('perfil') if payload else None
            
            if perfil_no_token == perfil:
                print(f"    ✅ Perfil '{perfil}' aplicado corretamente no token")
            else:
                print(f"    ⚠️ Perfil esperado: '{perfil}', mas token tem: '{perfil_no_token}'")
        else:
            print(f"    ❌ Erro: {context_response.status_code} - {context_response.text}")
    
    print(f"\n{'='*70}")
    print("✅ Teste concluído!")
    print(f"{'='*70}")
    
    return True

if __name__ == "__main__":
    test_perfil_selection()












