from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.services.user import UserService
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.api.deps import get_current_user

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    ativo: Optional[bool] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Lista todos os usuários/colaboradores
    
    Filtros:
    - ativo: Filtrar por status (True/False)
    - search: Buscar por nome, email ou CPF
    """
    service = UserService(db)
    return service.get_all(skip=skip, limit=limit, ativo=ativo, search=search)


@router.post("/", response_model=UserResponse, status_code=201)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Cria um novo usuário/colaborador
    """
    service = UserService(db)
    return service.create(user)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Busca um usuário por ID
    """
    service = UserService(db)
    return service.get_by_id(user_id)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Atualiza um usuário
    """
    service = UserService(db)
    return service.update(user_id, user)


@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Remove um usuário (soft delete)
    """
    service = UserService(db)
    service.delete(user_id)


@router.get("/stats/count")
def count_users(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Retorna total de usuários cadastrados
    """
    service = UserService(db)
    return {"total": service.count()}
