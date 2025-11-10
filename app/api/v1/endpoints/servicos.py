"""
Endpoints de Serviços
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.deps import get_current_user, get_current_escritorio
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
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """Lista todos os serviços, isolados por escritório"""
    repo = ServicoRepository(db)
    
    if search:
        return repo.search(escritorio_id, search, skip, limit)
    
    return repo.get_all(escritorio_id, skip, limit, ativo)


@router.post("", response_model=ServicoResponse, status_code=status.HTTP_201_CREATED)
def criar_servico(
    servico: ServicoCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """Cria um novo serviço, vinculado ao escritório"""
    repo = ServicoRepository(db)
    return repo.create(servico, escritorio_id)


@router.get("/stats/count")
def contar_servicos(
    ativo: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """Retorna a contagem de serviços, isolados por escritório"""
    repo = ServicoRepository(db)
    return {"total": repo.count(escritorio_id, ativo)}


@router.get("/{servico_id}", response_model=ServicoResponse)
def obter_servico(
    servico_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """Obtém um serviço por ID, garantindo que pertence ao escritório"""
    repo = ServicoRepository(db)
    servico = repo.get_by_id(servico_id, escritorio_id)
    
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
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """Atualiza um serviço, garantindo que pertence ao escritório"""
    repo = ServicoRepository(db)
    servico = repo.update(servico_id, servico_data, escritorio_id)
    
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
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """Deleta um serviço, garantindo que pertence ao escritório"""
    repo = ServicoRepository(db)
    
    if not repo.delete(servico_id, escritorio_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Serviço não encontrado"
        )


# Endpoints de Etapas
@router.get("/{servico_id}/etapas", response_model=List[EtapaResponse])
def listar_etapas(
    servico_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """Lista todas as etapas de um serviço, garantindo que pertence ao escritório"""
    # Verificar se serviço existe e pertence ao escritório
    servico_repo = ServicoRepository(db)
    if not servico_repo.get_by_id(servico_id, escritorio_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Serviço não encontrado"
        )
    
    repo = EtapaRepository(db)
    return repo.get_by_servico(servico_id, escritorio_id)


@router.post("/{servico_id}/etapas", response_model=EtapaResponse, status_code=status.HTTP_201_CREATED)
def criar_etapa(
    servico_id: int,
    etapa: EtapaCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """Cria uma nova etapa para um serviço, garantindo que pertence ao escritório"""
    # Verificar se serviço existe e pertence ao escritório
    servico_repo = ServicoRepository(db)
    if not servico_repo.get_by_id(servico_id, escritorio_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Serviço não encontrado"
        )
    
    repo = EtapaRepository(db)
    return repo.create(servico_id, etapa, escritorio_id)


@router.put("/{servico_id}/etapas/{etapa_id}", response_model=EtapaResponse)
def atualizar_etapa(
    servico_id: int,
    etapa_id: int,
    etapa_data: EtapaUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """Atualiza uma etapa, garantindo que pertence ao escritório"""
    repo = EtapaRepository(db)
    etapa = repo.get_by_id(etapa_id, escritorio_id)
    
    if not etapa or etapa.servico_id != servico_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Etapa não encontrada"
        )
    
    return repo.update(etapa_id, etapa_data, escritorio_id)


@router.delete("/{servico_id}/etapas/{etapa_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_etapa(
    servico_id: int,
    etapa_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """Deleta uma etapa, garantindo que pertence ao escritório"""
    repo = EtapaRepository(db)
    etapa = repo.get_by_id(etapa_id, escritorio_id)
    
    if not etapa or etapa.servico_id != servico_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Etapa não encontrada"
        )
    
    repo.delete(etapa_id, escritorio_id)
