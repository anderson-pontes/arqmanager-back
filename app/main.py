from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from pathlib import Path
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

# Configure CORS - DEVE SER O PRIMEIRO MIDDLEWARE
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Aceita qualquer origem (desenvolvimento)
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# Handler para erros de validação
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handler customizado para erros de validação do Pydantic"""
    errors = exc.errors()
    error_messages = []
    
    for error in errors:
        field = ".".join(str(loc) for loc in error.get("loc", []))
        message = error.get("msg", "Erro de validação")
        error_messages.append(f"{field}: {message}")
    
    response = JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "; ".join(error_messages),
            "errors": errors
        }
    )
    # Adicionar headers CORS manualmente
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, PATCH, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

# Handler para erros gerais (500)
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handler para erros não tratados"""
    import traceback
    error_detail = str(exc) if settings.ENVIRONMENT == "development" else "Erro interno do servidor"
    print(f"Erro não tratado: {exc}")
    print(traceback.format_exc())
    
    response = JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": error_detail}
    )
    # Adicionar headers CORS manualmente - CRÍTICO para evitar erro CORS
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, PATCH, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

# Include API router
app.include_router(api_router, prefix="/api/v1")

# Servir arquivos estáticos de upload
upload_dir = Path(settings.UPLOAD_DIR)
upload_dir.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(upload_dir)), name="uploads")


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
