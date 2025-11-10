from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.escritorio import EscritorioService
from app.repositories.user import EscritorioRepository, UserRepository
from app.schemas.user import (
    EscritorioCreate, 
    EscritorioResponse, 
    EscritorioUpdate,
    UserCreate, 
    UserResponse
)
from app.api.deps import require_system_admin
from typing import Dict, List, Optional

router = APIRouter()


@router.get("/", response_model=List[EscritorioResponse])
def list_escritorios(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    ativo: Optional[bool] = None,
    current_user: dict = Depends(require_system_admin),
    db: Session = Depends(get_db)
):
    """Lista todos os escritórios (apenas admin do sistema)"""
    repo = EscritorioRepository(db)
    escritorios = repo.get_all(skip=skip, limit=limit, ativo=ativo)
    return [EscritorioResponse.from_orm(e) for e in escritorios]


@router.get("/{escritorio_id}", response_model=EscritorioResponse)
def get_escritorio(
    escritorio_id: int,
    current_user: dict = Depends(require_system_admin),
    db: Session = Depends(get_db)
):
    """Busca escritório por ID (apenas admin do sistema)"""
    service = EscritorioService(db)
    escritorio = service.get_by_id(escritorio_id)
    return EscritorioResponse.from_orm(escritorio)


@router.post("/", response_model=Dict)
def create_escritorio_with_admin(
    escritorio_data: EscritorioCreate,
    admin_data: UserCreate,
    current_user: dict = Depends(require_system_admin),
    db: Session = Depends(get_db)
):
    """
    Cria um novo escritório e automaticamente cria um administrador do escritório
    Apenas administradores do sistema podem criar escritórios
    """
    service = EscritorioService(db)
    result = service.create_with_admin(escritorio_data, admin_data)
    
    return {
        "escritorio": EscritorioResponse.from_orm(result["escritorio"]),
        "admin": {
            "id": result["admin"].id,
            "nome": result["admin"].nome,
            "email": result["admin"].email
        }
    }


@router.put("/{escritorio_id}", response_model=EscritorioResponse)
def update_escritorio(
    escritorio_id: int,
    escritorio_data: EscritorioUpdate,
    current_user: dict = Depends(require_system_admin),
    db: Session = Depends(get_db)
):
    """Atualiza um escritório (apenas admin do sistema)"""
    repo = EscritorioRepository(db)
    escritorio = repo.get_by_id(escritorio_id)
    
    if not escritorio:
        raise HTTPException(status_code=404, detail="Escritório não encontrado")
    
    update_data = escritorio_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(escritorio, field, value)
    
    db.commit()
    db.refresh(escritorio)
    
    return EscritorioResponse.from_orm(escritorio)


@router.delete("/{escritorio_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_escritorio(
    escritorio_id: int,
    current_user: dict = Depends(require_system_admin),
    db: Session = Depends(get_db)
):
    """Desativa um escritório (soft delete) (apenas admin do sistema)"""
    repo = EscritorioRepository(db)
    escritorio = repo.get_by_id(escritorio_id)
    
    if not escritorio:
        raise HTTPException(status_code=404, detail="Escritório não encontrado")
    
    escritorio.ativo = False
    db.commit()
    
    return None

