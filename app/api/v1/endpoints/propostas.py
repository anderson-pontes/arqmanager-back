"""
Endpoints de Propostas
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.deps import get_current_user
from app.repositories.proposta_repository import PropostaRepository
from app.schemas.proposta import PropostaCreate, PropostaUpdate, PropostaResponse

router = APIRouter()


@router.get("", response_model=List[PropostaResponse])
def listar_propostas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    cliente_id: Optional[int] = None,
    status_id: Optional[int] = None,
    ano: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Lista todas as propostas"""
    repo = PropostaRepository(db)
    
    if search:
        return repo.search(search, skip, limit)
    
    return repo.get_all(skip, limit, cliente_id, status_id, ano)


@router.post("", response_model=PropostaResponse, status_code=status.HTTP_201_CREATED)
def criar_proposta(
    proposta: PropostaCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Cria uma nova proposta"""
    repo = PropostaRepository(db)
    return repo.create(proposta)


@router.get("/stats/count")
def contar_propostas(
    cliente_id: Optional[int] = None,
    status_id: Optional[int] = None,
    ano: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Retorna a contagem de propostas"""
    repo = PropostaRepository(db)
    return {"total": repo.count(cliente_id, status_id, ano)}


@router.get("/proximo-numero/{ano}")
def obter_proximo_numero(
    ano: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Retorna o próximo número de proposta para o ano"""
    repo = PropostaRepository(db)
    return {"numero": repo.get_proximo_numero(ano)}


@router.get("/{proposta_id}", response_model=PropostaResponse)
def obter_proposta(
    proposta_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Obtém uma proposta por ID"""
    repo = PropostaRepository(db)
    proposta = repo.get_by_id(proposta_id)
    
    if not proposta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proposta não encontrada"
        )
    
    return proposta


@router.put("/{proposta_id}", response_model=PropostaResponse)
def atualizar_proposta(
    proposta_id: int,
    proposta_data: PropostaUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Atualiza uma proposta"""
    repo = PropostaRepository(db)
    proposta = repo.update(proposta_id, proposta_data)
    
    if not proposta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proposta não encontrada"
        )
    
    return proposta


@router.delete("/{proposta_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_proposta(
    proposta_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Deleta uma proposta"""
    repo = PropostaRepository(db)
    
    if not repo.delete(proposta_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proposta não encontrada"
        )
