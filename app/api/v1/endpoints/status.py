"""
Endpoints de Status
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.deps import get_current_user
from app.repositories.status_repository import StatusRepository
from app.schemas.projeto import StatusCreate, StatusUpdate, StatusResponse

router = APIRouter()


@router.get("", response_model=List[StatusResponse])
def listar_status(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    ativo: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Lista todos os status"""
    repo = StatusRepository(db)
    return repo.get_all(skip, limit, ativo)


@router.post("", response_model=StatusResponse, status_code=status.HTTP_201_CREATED)
def criar_status(
    status_data: StatusCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Cria um novo status"""
    repo = StatusRepository(db)
    return repo.create(status_data)


@router.get("/{status_id}", response_model=StatusResponse)
def obter_status(
    status_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Obtém um status por ID"""
    repo = StatusRepository(db)
    status_obj = repo.get_by_id(status_id)
    
    if not status_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Status não encontrado"
        )
    
    return status_obj


@router.put("/{status_id}", response_model=StatusResponse)
def atualizar_status(
    status_id: int,
    status_data: StatusUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Atualiza um status"""
    repo = StatusRepository(db)
    status_obj = repo.update(status_id, status_data)
    
    if not status_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Status não encontrado"
        )
    
    return status_obj


@router.delete("/{status_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_status(
    status_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Deleta um status"""
    repo = StatusRepository(db)
    
    if not repo.delete(status_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Status não encontrado"
        )
