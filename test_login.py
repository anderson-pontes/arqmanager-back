import requests
import json

response = requests.post(
    "http://localhost:8000/api/v1/auth/login",
    json={"email": "admin@arqmanager.com", "senha": "admin123"}
)

print(f"Status: {response.status_code}")
print(f"Response: {response.text}")
if response.status_code == 200:
    data = response.json()
    print(f"Token: {data.get('access_token', 'N/A')}")
