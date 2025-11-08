from jose import jwt, JWTError
from app.core.config import settings
from app.core.security import create_access_token

token = create_access_token({'sub': 1, 'email': 'test@test.com'})
print(f"Token: {token[:50]}...")

try:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    print(f"Payload OK: {payload}")
except JWTError as e:
    print(f"Erro JWT: {e}")
except Exception as e:
    print(f"Erro: {e}")
