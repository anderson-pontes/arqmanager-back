"""
Endpoints de Tarefas
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.deps import get_current_user, get_current_escritorio
from app.services.tarefa_service import TarefaService
from app.schemas.servico import (
    TarefaCreate, TarefaUpdate, TarefaResponse
)

router = APIRouter()


@router.get("", response_model=List[TarefaResponse])
def listar_tarefas(
    etapa_id: Optional[int] = Query(None, description="Filtrar por etapa"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: Optional[str] = Query(None, description="Buscar por nome"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """Lista todas as tarefas, opcionalmente filtradas por etapa"""
    service = TarefaService(db)
    
    if search:
        return service.buscar_tarefas(escritorio_id, search, etapa_id, skip, limit)
    
    return service.listar_tarefas(escritorio_id, etapa_id, skip, limit)


@router.get("/stats/count")
def contar_tarefas(
    etapa_id: Optional[int] = Query(None, description="Filtrar por etapa"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """Retorna a contagem de tarefas, opcionalmente filtradas por etapa"""
    service = TarefaService(db)
    return {"total": service.contar_tarefas(escritorio_id, etapa_id)}


@router.get("/{tarefa_id}", response_model=TarefaResponse)
def obter_tarefa(
    tarefa_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """Obtém uma tarefa por ID, garantindo que pertence ao escritório"""
    service = TarefaService(db)
    return service.obter_tarefa(tarefa_id, escritorio_id)


@router.post("", response_model=TarefaResponse, status_code=status.HTTP_201_CREATED)
def criar_tarefa(
    tarefa: TarefaCreate,
    etapa_id: int = Query(..., description="ID da etapa"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """Cria uma nova tarefa, vinculada à etapa e ao escritório
    
    Nota: Para criar tarefa dentro de uma etapa específica de um serviço,
    use o endpoint: POST /servicos/{servico_id}/etapas/{etapa_id}/tarefas
    """
    service = TarefaService(db)
    return service.criar_tarefa(etapa_id, tarefa, escritorio_id)


@router.put("/{tarefa_id}", response_model=TarefaResponse)
def atualizar_tarefa(
    tarefa_id: int,
    tarefa_data: TarefaUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """Atualiza uma tarefa, garantindo que pertence ao escritório"""
    service = TarefaService(db)
    return service.atualizar_tarefa(tarefa_id, tarefa_data, escritorio_id)


@router.delete("/{tarefa_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_tarefa(
    tarefa_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """Deleta uma tarefa, garantindo que pertence ao escritório"""
    service = TarefaService(db)
    service.deletar_tarefa(tarefa_id, escritorio_id)

