import requests

# Login
response = requests.post(
    "http://localhost:8000/api/v1/auth/login",
    json={"email": "admin@arqmanager.com", "senha": "admin123"}
)

print(f"Login Status: {response.status_code}")
token = response.json()["access_token"]
print(f"Token: {token[:50]}...")

# Testar endpoint
headers = {"Authorization": f"Bearer {token}"}
response2 = requests.get("http://localhost:8000/api/v1/servicos", headers=headers)
print(f"\nServicos Status: {response2.status_code}")
print(f"Response: {response2.text}")
