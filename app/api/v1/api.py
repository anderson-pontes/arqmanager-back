from fastapi import APIRouter
from app.api.v1.endpoints import auth, users

api_router = APIRouter()

# Health check
@api_router.get("/health", tags=["health"])
def health_check():
    """Endpoint de health check"""
    return {
        "status": "ok",
        "message": "ARQManager API is running"
    }

# Incluir routers dos módulos
api_router.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
api_router.include_router(users.router, prefix="/users", tags=["Usuários"])
# api_router.include_router(clientes.router, prefix="/clientes", tags=["clientes"])
