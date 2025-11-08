import requests

# Login
response = requests.post(
    "http://localhost:8000/api/v1/auth/login",
    json={"email": "admin@arqmanager.com", "senha": "admin123"}
)

token = response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Testar clientes (funciona)
response1 = requests.get("http://localhost:8000/api/v1/clientes", headers=headers)
print(f"Clientes Status: {response1.status_code}")

# Testar serviços (não funciona)
response2 = requests.get("http://localhost:8000/api/v1/servicos", headers=headers)
print(f"Servicos Status: {response2.status_code}")
print(f"Response: {response2.text}")
