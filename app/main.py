from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.core.config import settings
from app.api.v1.api import api_router

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API para gestão de escritórios de arquitetura",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configurar esquema de autenticação no Swagger
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="API para gestão de escritórios de arquitetura",
        routes=app.routes,
    )
    
    # Adicionar esquema de segurança Bearer
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Insira o token JWT obtido no endpoint /api/v1/auth/login"
        }
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ TEMPORÁRIO - aceita qualquer origem
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1")


@app.get("/", tags=["root"])
def root():
    """Root endpoint"""
    return {
        "message": "ARQManager API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/api/v1/health"
    }


@app.get("/test-cors", tags=["test"])
def test_cors():
    """Endpoint de teste para CORS (sem autenticação)"""
    return {
        "message": "CORS está funcionando!",
        "origin": "http://localhost:5173"
    }


@app.on_event("startup")
async def startup_event():
    """Evento executado ao iniciar a aplicação"""
    print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} iniciado!")
    print(f"📚 Documentação: http://{settings.HOST}:{settings.PORT}/docs")
    print(f"🔧 Ambiente: {settings.ENVIRONMENT}")


@app.on_event("shutdown")
async def shutdown_event():
    """Evento executado ao encerrar a aplicação"""
    print("👋 Encerrando aplicação...")
