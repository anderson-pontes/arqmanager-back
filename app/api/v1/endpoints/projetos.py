"""
Endpoints de Projetos
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.deps import get_current_user, get_current_escritorio
from app.repositories.projeto_repository import ProjetoRepository
from app.schemas.projeto import (
    ProjetoCreate, ProjetoUpdate, ProjetoResponse,
    ProjetoColaboradorCreate
)

router = APIRouter()


@router.get("", response_model=List[ProjetoResponse])
def listar_projetos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    ativo: Optional[bool] = None,
    cliente_id: Optional[int] = None,
    status_id: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """Lista todos os projetos, isolados por escritório"""
    repo = ProjetoRepository(db)
    
    if search:
        return repo.search(escritorio_id, search, skip, limit)
    
    return repo.get_all(escritorio_id, skip, limit, ativo, cliente_id, status_id)


@router.post("", response_model=ProjetoResponse, status_code=status.HTTP_201_CREATED)
def criar_projeto(
    projeto: ProjetoCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """Cria um novo projeto, vinculado ao escritório"""
    repo = ProjetoRepository(db)
    return repo.create(projeto, escritorio_id)


@router.get("/stats/count")
def contar_projetos(
    ativo: Optional[bool] = None,
    cliente_id: Optional[int] = None,
    status_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """Retorna a contagem de projetos, isolados por escritório"""
    repo = ProjetoRepository(db)
    return {"total": repo.count(escritorio_id, ativo, cliente_id, status_id)}


@router.get("/{projeto_id}", response_model=ProjetoResponse)
def obter_projeto(
    projeto_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """Obtém um projeto por ID, garantindo que pertence ao escritório"""
    repo = ProjetoRepository(db)
    projeto = repo.get_by_id(projeto_id, escritorio_id)
    
    if not projeto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeto não encontrado"
        )
    
    return projeto


@router.put("/{projeto_id}", response_model=ProjetoResponse)
def atualizar_projeto(
    projeto_id: int,
    projeto_data: ProjetoUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """Atualiza um projeto, garantindo que pertence ao escritório"""
    repo = ProjetoRepository(db)
    projeto = repo.update(projeto_id, projeto_data, escritorio_id)
    
    if not projeto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeto não encontrado"
        )
    
    return projeto


@router.delete("/{projeto_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_projeto(
    projeto_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """Deleta um projeto, garantindo que pertence ao escritório"""
    repo = ProjetoRepository(db)
    
    if not repo.delete(projeto_id, escritorio_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeto não encontrado"
        )


# Endpoints de Colaboradores do Projeto
@router.post("/{projeto_id}/colaboradores", status_code=status.HTTP_201_CREATED)
def adicionar_colaborador(
    projeto_id: int,
    colaborador_data: ProjetoColaboradorCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """Adiciona um colaborador ao projeto, garantindo que pertence ao escritório"""
    repo = ProjetoRepository(db)
    colab = repo.add_colaborador(
        projeto_id, 
        colaborador_data.colaborador_id,
        escritorio_id,
        colaborador_data.funcao
    )
    
    if not colab:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeto não encontrado"
        )
    
    return {"message": "Colaborador adicionado com sucesso"}


@router.delete("/{projeto_id}/colaboradores/{colaborador_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_colaborador(
    projeto_id: int,
    colaborador_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """Remove um colaborador do projeto, garantindo que pertence ao escritório"""
    repo = ProjetoRepository(db)
    
    if not repo.remove_colaborador(projeto_id, colaborador_id, escritorio_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Colaborador não encontrado no projeto"
        )
