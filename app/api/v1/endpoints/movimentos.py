"""
Endpoints de Movimentos Financeiros
"""
from typing import List, Optional
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.deps import get_current_user
from app.repositories.movimento_repository import MovimentoRepository
from app.schemas.movimento import MovimentoCreate, MovimentoUpdate, MovimentoResponse

router = APIRouter()


@router.get("", response_model=List[MovimentoResponse])
def listar_movimentos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    tipo: Optional[int] = None,
    projeto_id: Optional[int] = None,
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    ativo: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Lista todos os movimentos financeiros"""
    repo = MovimentoRepository(db)
    return repo.get_all(skip, limit, tipo, projeto_id, data_inicio, data_fim, ativo)


@router.post("", response_model=MovimentoResponse, status_code=status.HTTP_201_CREATED)
def criar_movimento(
    movimento: MovimentoCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Cria um novo movimento financeiro"""
    repo = MovimentoRepository(db)
    return repo.create(movimento)


@router.get("/resumo")
def obter_resumo(
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    tipo: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Retorna resumo financeiro"""
    repo = MovimentoRepository(db)
    return repo.get_resumo(data_inicio, data_fim, tipo)


@router.get("/mes/{ano}/{mes}", response_model=List[MovimentoResponse])
def obter_por_mes(
    ano: int,
    mes: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Retorna movimentos de um mês específico"""
    repo = MovimentoRepository(db)
    return repo.get_por_mes(ano, mes)


@router.get("/{movimento_id}", response_model=MovimentoResponse)
def obter_movimento(
    movimento_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Obtém um movimento por ID"""
    repo = MovimentoRepository(db)
    movimento = repo.get_by_id(movimento_id)
    
    if not movimento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movimento não encontrado"
        )
    
    return movimento


@router.put("/{movimento_id}", response_model=MovimentoResponse)
def atualizar_movimento(
    movimento_id: int,
    movimento_data: MovimentoUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Atualiza um movimento"""
    repo = MovimentoRepository(db)
    movimento = repo.update(movimento_id, movimento_data)
    
    if not movimento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movimento não encontrado"
        )
    
    return movimento


@router.delete("/{movimento_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_movimento(
    movimento_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Deleta um movimento"""
    repo = MovimentoRepository(db)
    
    if not repo.delete(movimento_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movimento não encontrado"
        )
