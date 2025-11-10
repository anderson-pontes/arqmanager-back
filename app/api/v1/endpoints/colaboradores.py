"""
Endpoints de Colaboradores
Alias para /users para manter compatibilidade com frontend
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.services.user import UserService
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.api.deps import get_current_user

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
def list_colaboradores(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    ativo: Optional[bool] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Lista todos os colaboradores
    
    Filtros:
    - ativo: Filtrar por status (True/False)
    - search: Buscar por nome, email ou CPF
    """
    service = UserService(db)
    return service.get_all(skip=skip, limit=limit, ativo=ativo, search=search)


@router.post("/", response_model=UserResponse, status_code=201)
def create_colaborador(
    colaborador: UserCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Cria um novo colaborador
    """
    service = UserService(db)
    return service.create(colaborador)


@router.get("/{colaborador_id}", response_model=UserResponse)
def get_colaborador(
    colaborador_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Busca um colaborador por ID
    """
    service = UserService(db)
    return service.get_by_id(colaborador_id)


@router.put("/{colaborador_id}", response_model=UserResponse)
def update_colaborador(
    colaborador_id: int,
    colaborador: UserUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Atualiza um colaborador
    """
    service = UserService(db)
    return service.update(colaborador_id, colaborador)


@router.delete("/{colaborador_id}", status_code=204)
def delete_colaborador(
    colaborador_id: int,
    permanent: bool = Query(False, description="Se True, remove permanentemente. Se False, soft delete (marca como inativo)"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Remove um colaborador
    
    Parâmetros:
    - permanent: False = Soft delete (marca como inativo)
    - permanent: True = Hard delete (remove do banco permanentemente)
    """
    service = UserService(db)
    service.delete(colaborador_id, permanent=permanent)


@router.get("/stats/count")
def count_colaboradores(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Retorna total de colaboradores cadastrados
    """
    service = UserService(db)
    return {"total": service.count()}

