"""
Endpoints de Status
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.deps import get_current_user, get_current_escritorio
from app.repositories.status_repository import StatusRepository
from app.schemas.projeto import StatusCreate, StatusUpdate, StatusResponse

router = APIRouter()


@router.get("", response_model=List[StatusResponse])
def listar_status(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    ativo: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """Lista todos os status, isolados por escritório"""
    repo = StatusRepository(db)
    return repo.get_all(escritorio_id, skip, limit, ativo)


@router.post("", response_model=StatusResponse, status_code=status.HTTP_201_CREATED)
def criar_status(
    status_data: StatusCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """Cria um novo status, vinculado ao escritório"""
    repo = StatusRepository(db)
    return repo.create(status_data, escritorio_id)


@router.get("/{status_id}", response_model=StatusResponse)
def obter_status(
    status_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """Obtém um status por ID, garantindo que pertence ao escritório"""
    repo = StatusRepository(db)
    status_obj = repo.get_by_id(status_id, escritorio_id)
    
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
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """Atualiza um status, garantindo que pertence ao escritório"""
    repo = StatusRepository(db)
    status_obj = repo.update(status_id, status_data, escritorio_id)
    
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
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """Deleta um status, garantindo que pertence ao escritório"""
    repo = StatusRepository(db)
    
    if not repo.delete(status_id, escritorio_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Status não encontrado"
        )
