from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
