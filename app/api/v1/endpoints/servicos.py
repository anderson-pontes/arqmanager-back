"""
Endpoints de Serviços
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.deps import get_current_user
from app.repositories.servico_repository import ServicoRepository
from app.repositories.etapa_repository import EtapaRepository
from app.schemas.servico import (
    ServicoCreate, ServicoUpdate, ServicoResponse,
    EtapaCreate, EtapaUpdate, EtapaResponse
)

router = APIRouter()


@router.get("", response_model=List[ServicoResponse])
def listar_servicos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    ativo: Optional[bool] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Lista todos os serviços"""
    repo = ServicoRepository(db)
    
    if search:
        return repo.search(search, skip, limit)
    
    return repo.get_all(skip, limit, ativo)


@router.post("", response_model=ServicoResponse, status_code=status.HTTP_201_CREATED)
def criar_servico(
    servico: ServicoCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Cria um novo serviço"""
    repo = ServicoRepository(db)
    return repo.create(servico)


@router.get("/stats/count")
def contar_servicos(
    ativo: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Retorna a contagem de serviços"""
    repo = ServicoRepository(db)
    return {"total": repo.count(ativo)}


@router.get("/{servico_id}", response_model=ServicoResponse)
def obter_servico(
    servico_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Obtém um serviço por ID"""
    repo = ServicoRepository(db)
    servico = repo.get_by_id(servico_id)
    
    if not servico:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Serviço não encontrado"
        )
    
    return servico


@router.put("/{servico_id}", response_model=ServicoResponse)
def atualizar_servico(
    servico_id: int,
    servico_data: ServicoUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Atualiza um serviço"""
    repo = ServicoRepository(db)
    servico = repo.update(servico_id, servico_data)
    
    if not servico:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Serviço não encontrado"
        )
    
    return servico


@router.delete("/{servico_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_servico(
    servico_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Deleta um serviço"""
    repo = ServicoRepository(db)
    
    if not repo.delete(servico_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Serviço não encontrado"
        )


# Endpoints de Etapas
@router.get("/{servico_id}/etapas", response_model=List[EtapaResponse])
def listar_etapas(
    servico_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Lista todas as etapas de um serviço"""
    # Verificar se serviço existe
    servico_repo = ServicoRepository(db)
    if not servico_repo.get_by_id(servico_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Serviço não encontrado"
        )
    
    repo = EtapaRepository(db)
    return repo.get_by_servico(servico_id)


@router.post("/{servico_id}/etapas", response_model=EtapaResponse, status_code=status.HTTP_201_CREATED)
def criar_etapa(
    servico_id: int,
    etapa: EtapaCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Cria uma nova etapa para um serviço"""
    # Verificar se serviço existe
    servico_repo = ServicoRepository(db)
    if not servico_repo.get_by_id(servico_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Serviço não encontrado"
        )
    
    repo = EtapaRepository(db)
    return repo.create(servico_id, etapa)


@router.put("/{servico_id}/etapas/{etapa_id}", response_model=EtapaResponse)
def atualizar_etapa(
    servico_id: int,
    etapa_id: int,
    etapa_data: EtapaUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Atualiza uma etapa"""
    repo = EtapaRepository(db)
    etapa = repo.get_by_id(etapa_id)
    
    if not etapa or etapa.servico_id != servico_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Etapa não encontrada"
        )
    
    return repo.update(etapa_id, etapa_data)


@router.delete("/{servico_id}/etapas/{etapa_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_etapa(
    servico_id: int,
    etapa_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Deleta uma etapa"""
    repo = EtapaRepository(db)
    etapa = repo.get_by_id(etapa_id)
    
    if not etapa or etapa.servico_id != servico_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Etapa não encontrada"
        )
    
    repo.delete(etapa_id)
