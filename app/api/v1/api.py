from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, clientes, servicos, status, projetos, propostas, movimentos, colaboradores, escritorios, admin, tarefas

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
api_router.include_router(colaboradores.router, prefix="/colaboradores", tags=["Colaboradores"])
api_router.include_router(clientes.router, prefix="/clientes", tags=["Clientes"])
api_router.include_router(servicos.router, prefix="/servicos", tags=["Serviços"])
api_router.include_router(tarefas.router, prefix="/tarefas", tags=["Tarefas"])
api_router.include_router(status.router, prefix="/status", tags=["Status"])
api_router.include_router(projetos.router, prefix="/projetos", tags=["Projetos"])
api_router.include_router(propostas.router, prefix="/propostas", tags=["Propostas"])
api_router.include_router(movimentos.router, prefix="/movimentos", tags=["Financeiro"])
api_router.include_router(escritorios.router, prefix="/escritorios", tags=["Escritórios"])
api_router.include_router(admin.router, prefix="/admin", tags=["Administração"])
