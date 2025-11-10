"""Teste do endpoint de criação de admin"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

# Primeiro, fazer login como admin do sistema
login_response = requests.post(
    f"{BASE_URL}/auth/login",
    json={"email": "admin@sistema.com", "senha": "admin123"}
)

if login_response.status_code != 200:
    print(f"❌ Erro no login: {login_response.status_code}")
    print(login_response.text)
    exit(1)

token = login_response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Testar criação de admin sem CPF
print("\n1️⃣ Testando criação de admin SEM CPF")
print("-" * 60)

data_sem_cpf = {
    "nome": "Admin Teste",
    "email": "adminteste@teste.com",
    "senha": "teste123"
}

response = requests.post(
    f"{BASE_URL}/admin/system-admin",
    json=data_sem_cpf,
    headers=headers
)

print(f"Status: {response.status_code}")
print(f"Response: {response.text}")

if response.status_code == 200:
    print("✅ Admin criado com sucesso!")
else:
    print(f"❌ Erro: {response.status_code}")
    try:
        error_detail = response.json()
        print(f"Detalhes: {json.dumps(error_detail, indent=2)}")
    except:
        print(f"Resposta: {response.text}")

# Testar criação de admin COM CPF
print("\n2️⃣ Testando criação de admin COM CPF")
print("-" * 60)

data_com_cpf = {
    "nome": "Admin Teste 2",
    "email": "adminteste2@teste.com",
    "senha": "teste123",
    "cpf": "12345678901"
}

response2 = requests.post(
    f"{BASE_URL}/admin/system-admin",
    json=data_com_cpf,
    headers=headers
)

print(f"Status: {response2.status_code}")
print(f"Response: {response2.text}")

if response2.status_code == 200:
    print("✅ Admin criado com sucesso!")
else:
    print(f"❌ Erro: {response2.status_code}")
    try:
        error_detail = response2.json()
        print(f"Detalhes: {json.dumps(error_detail, indent=2)}")
    except:
        print(f"Resposta: {response2.text}")

