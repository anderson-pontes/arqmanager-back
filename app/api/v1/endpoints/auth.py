from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.auth import AuthService
from app.schemas.user import UserLogin, UserWithToken, UserResponse
from app.api.deps import get_current_user

router = APIRouter()


@router.post("/login", response_model=UserWithToken)
def login(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Endpoint de login
    
    Retorna:
    - user: Dados do usuário
    - access_token: Token de acesso (30 min)
    - refresh_token: Token de refresh (7 dias)
    - requires_escritorio_selection: Se precisa selecionar escritório
    """
    service = AuthService(db)
    return service.login(credentials)


@router.post("/refresh")
def refresh_token(
    refresh_token: str = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    """
    Gera novo access token a partir do refresh token
    """
    service = AuthService(db)
    return service.refresh_token(refresh_token)


@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retorna informações do usuário autenticado
    """
    service = AuthService(db)
    return service.get_current_user(current_user["id"])


@router.post("/logout")
def logout(current_user: dict = Depends(get_current_user)):
    """
    Endpoint de logout
    
    Nota: Como usamos JWT stateless, o logout é feito no frontend
    removendo o token. Este endpoint serve apenas para validar
    que o usuário está autenticado.
    """
    return {"message": "Logout realizado com sucesso"}
