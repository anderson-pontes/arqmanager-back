"""
Endpoints de Projetos
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.deps import get_current_user
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
    current_user: dict = Depends(get_current_user)
):
    """Lista todos os projetos"""
    repo = ProjetoRepository(db)
    
    if search:
        return repo.search(search, skip, limit)
    
    return repo.get_all(skip, limit, ativo, cliente_id, status_id)


@router.post("", response_model=ProjetoResponse, status_code=status.HTTP_201_CREATED)
def criar_projeto(
    projeto: ProjetoCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Cria um novo projeto"""
    repo = ProjetoRepository(db)
    return repo.create(projeto)


@router.get("/stats/count")
def contar_projetos(
    ativo: Optional[bool] = None,
    cliente_id: Optional[int] = None,
    status_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Retorna a contagem de projetos"""
    repo = ProjetoRepository(db)
    return {"total": repo.count(ativo, cliente_id, status_id)}


@router.get("/{projeto_id}", response_model=ProjetoResponse)
def obter_projeto(
    projeto_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Obtém um projeto por ID"""
    repo = ProjetoRepository(db)
    projeto = repo.get_by_id(projeto_id)
    
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
    current_user: dict = Depends(get_current_user)
):
    """Atualiza um projeto"""
    repo = ProjetoRepository(db)
    projeto = repo.update(projeto_id, projeto_data)
    
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
    current_user: dict = Depends(get_current_user)
):
    """Deleta um projeto"""
    repo = ProjetoRepository(db)
    
    if not repo.delete(projeto_id):
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
    current_user: dict = Depends(get_current_user)
):
    """Adiciona um colaborador ao projeto"""
    repo = ProjetoRepository(db)
    colab = repo.add_colaborador(
        projeto_id, 
        colaborador_data.colaborador_id,
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
    current_user: dict = Depends(get_current_user)
):
    """Remove um colaborador do projeto"""
    repo = ProjetoRepository(db)
    
    if not repo.remove_colaborador(projeto_id, colaborador_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Colaborador não encontrado no projeto"
        )
