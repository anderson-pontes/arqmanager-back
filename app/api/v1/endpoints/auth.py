from fastapi import APIRouter, Depends, Body, File, UploadFile
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.auth import AuthService
from app.schemas.user import (
    UserLogin, UserWithToken, UserResponse,
    SetContextRequest, SetContextResponse,
    EscritorioContextInfo, ChangePasswordRequest, UpdateProfileRequest
)
from app.api.deps import get_current_user
from app.utils.upload import save_upload_file
from typing import List

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
    - is_system_admin: Se é admin do sistema
    - available_escritorios: Lista de escritórios disponíveis
    """
    service = AuthService(db)
    return service.login(credentials)


@router.post("/set-context", response_model=SetContextResponse)
def set_context(
    context: SetContextRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Define o contexto de escritório e perfil para o usuário
    Retorna novo access_token com contexto incluído
    
    Se escritorio_id for None, define contexto de área administrativa (apenas para admin do sistema)
    """
    service = AuthService(db)
    result = service.set_context(
        current_user["id"],
        context.escritorio_id,
        context.perfil
    )
    return SetContextResponse(**result)


@router.get("/available-escritorios", response_model=List[EscritorioContextInfo])
def get_available_escritorios(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retorna lista de escritórios disponíveis para o usuário
    """
    service = AuthService(db)
    return service.get_available_escritorios(current_user["id"])


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


@router.post("/change-password")
def change_password(
    password_data: ChangePasswordRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Altera a senha do usuário logado
    """
    service = AuthService(db)
    service.change_password(
        current_user["id"],
        password_data.senha_atual,
        password_data.senha_nova
    )
    return {"message": "Senha alterada com sucesso"}


@router.get("/me/perfis")
def get_user_perfis(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retorna todos os perfis do usuário logado em todos os escritórios
    """
    service = AuthService(db)
    perfis = service.get_user_perfis(current_user["id"])
    return perfis


@router.put("/me", response_model=UserResponse)
def update_profile(
    profile_data: UpdateProfileRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Atualiza dados do perfil do usuário logado (telefone)
    """
    service = AuthService(db)
    updated_user = service.update_profile(
        current_user["id"],
        profile_data.telefone
    )
    return updated_user


@router.post("/me/foto", response_model=UserResponse)
async def upload_profile_photo(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Faz upload de foto de perfil do usuário logado
    """
    try:
        # Salvar arquivo
        file_path = save_upload_file(file, subdirectory="colaboradores")
        print(f"Arquivo salvo em: {file_path}")
        
        # Atualizar foto no banco
        service = AuthService(db)
        updated_user = service.update_profile_photo(current_user["id"], file_path)
        
        # Log para debug
        print(f"Usuário atualizado - Foto: {updated_user.foto}")
        if hasattr(updated_user, 'model_dump'):
            print(f"UserResponse serializado: {updated_user.model_dump()}")
        
        return updated_user
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao fazer upload da foto: {str(e)}"
        )
