import requests

# Login
resp = requests.post("http://localhost:8000/api/v1/auth/login", json={"email": "admin@arqmanager.com", "senha": "admin123"})
print(f"Login: {resp.status_code}")
token = resp.json()["access_token"]

headers = {"Authorization": f"Bearer {token}"}

# Testar clientes
resp = requests.get("http://localhost:8000/api/v1/clientes", headers=headers)
print(f"Clientes: {resp.status_code} - {resp.text[:100]}")

# Testar serviços
resp = requests.get("http://localhost:8000/api/v1/servicos", headers=headers)
print(f"Servicos: {resp.status_code} - {resp.text[:100]}")
