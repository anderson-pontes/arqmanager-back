"""
Endpoints de Serviços
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.deps import get_current_user, get_current_escritorio
from app.services.servico_service import ServicoService
from app.services.etapa_service import EtapaService
from app.services.tarefa_service import TarefaService
from app.schemas.servico import (
    ServicoCreate, ServicoUpdate, ServicoResponse,
    EtapaCreate, EtapaUpdate, EtapaResponse,
    TarefaCreate, TarefaUpdate, TarefaResponse,
    ReordenarEtapasRequest, ReordenarTarefasRequest
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
    service = ServicoService(db)
    return service.listar_servicos(escritorio_id, skip, limit, ativo, search)


@router.get("/hierarquia", response_model=List[ServicoResponse])
def listar_servicos_hierarquia(
    ativo: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """Lista todos os serviços com etapas e tarefas aninhadas (hierarquia completa)"""
    service = ServicoService(db)
    return service.listar_servicos_hierarquia(escritorio_id, ativo)


@router.post("", response_model=ServicoResponse, status_code=status.HTTP_201_CREATED)
def criar_servico(
    servico: ServicoCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """Cria um novo serviço, vinculado ao escritório"""
    service = ServicoService(db)
    return service.criar_servico(servico, escritorio_id)


@router.get("/stats/count")
def contar_servicos(
    ativo: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """Retorna a contagem de serviços, isolados por escritório"""
    service = ServicoService(db)
    return {"total": service.contar_servicos(escritorio_id, ativo)}


@router.get("/{servico_id}", response_model=ServicoResponse)
def obter_servico(
    servico_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """Obtém um serviço por ID, garantindo que pertence ao escritório"""
    service = ServicoService(db)
    return service.obter_servico(servico_id, escritorio_id)


@router.put("/{servico_id}", response_model=ServicoResponse)
def atualizar_servico(
    servico_id: int,
    servico_data: ServicoUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """Atualiza um serviço, garantindo que pertence ao escritório"""
    service = ServicoService(db)
    return service.atualizar_servico(servico_id, servico_data, escritorio_id)


@router.delete("/{servico_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_servico(
    servico_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """Deleta um serviço, garantindo que pertence ao escritório"""
    service = ServicoService(db)
    service.deletar_servico(servico_id, escritorio_id)


# Endpoints de Etapas
@router.get("/{servico_id}/etapas", response_model=List[EtapaResponse])
def listar_etapas(
    servico_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """Lista todas as etapas de um serviço, garantindo que pertence ao escritório"""
    service = EtapaService(db)
    return service.listar_etapas_por_servico(servico_id, escritorio_id)


@router.post("/{servico_id}/etapas", response_model=EtapaResponse, status_code=status.HTTP_201_CREATED)
def criar_etapa(
    servico_id: int,
    etapa: EtapaCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """Cria uma nova etapa para um serviço, garantindo que pertence ao escritório"""
    service = EtapaService(db)
    return service.criar_etapa(servico_id, etapa, escritorio_id)


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
    service = EtapaService(db)
    etapa = service.obter_etapa(etapa_id, escritorio_id)
    
    if etapa.servico_id != servico_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Etapa não pertence ao serviço informado"
        )
    
    return service.atualizar_etapa(etapa_id, etapa_data, escritorio_id)


@router.delete("/{servico_id}/etapas/{etapa_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_etapa(
    servico_id: int,
    etapa_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """Deleta uma etapa, garantindo que pertence ao escritório"""
    service = EtapaService(db)
    etapa = service.obter_etapa(etapa_id, escritorio_id)
    
    if etapa.servico_id != servico_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Etapa não pertence ao serviço informado"
        )
    
    service.deletar_etapa(etapa_id, escritorio_id)


@router.put("/{servico_id}/etapas/reordenar", response_model=List[EtapaResponse])
def reordenar_etapas(
    servico_id: int,
    request: ReordenarEtapasRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """Reordena etapas de um serviço em lote"""
    service = EtapaService(db)
    return service.reordenar_etapas(servico_id, request.etapa_ids, escritorio_id)


# Endpoints de Tarefas
@router.get("/{servico_id}/etapas/{etapa_id}/tarefas", response_model=List[TarefaResponse])
def listar_tarefas_por_etapa(
    servico_id: int,
    etapa_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """Lista todas as tarefas de uma etapa"""
    # Validar se etapa pertence ao serviço
    etapa_service = EtapaService(db)
    etapa = etapa_service.obter_etapa(etapa_id, escritorio_id)
    
    if etapa.servico_id != servico_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Etapa não pertence ao serviço informado"
        )
    
    tarefa_service = TarefaService(db)
    return tarefa_service.listar_tarefas_por_etapa(etapa_id, escritorio_id)


@router.post("/{servico_id}/etapas/{etapa_id}/tarefas", response_model=TarefaResponse, status_code=status.HTTP_201_CREATED)
def criar_tarefa_por_etapa(
    servico_id: int,
    etapa_id: int,
    tarefa: TarefaCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """Cria uma nova tarefa para uma etapa"""
    # Validar se etapa pertence ao serviço
    etapa_service = EtapaService(db)
    etapa = etapa_service.obter_etapa(etapa_id, escritorio_id)
    
    if etapa.servico_id != servico_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Etapa não pertence ao serviço informado"
        )
    
    tarefa_service = TarefaService(db)
    return tarefa_service.criar_tarefa(etapa_id, tarefa, escritorio_id)


@router.put("/{servico_id}/etapas/{etapa_id}/tarefas/{tarefa_id}", response_model=TarefaResponse)
def atualizar_tarefa_por_etapa(
    servico_id: int,
    etapa_id: int,
    tarefa_id: int,
    tarefa_data: TarefaUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """Atualiza uma tarefa de uma etapa"""
    # Validar se etapa pertence ao serviço
    etapa_service = EtapaService(db)
    etapa = etapa_service.obter_etapa(etapa_id, escritorio_id)
    
    if etapa.servico_id != servico_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Etapa não pertence ao serviço informado"
        )
    
    # Validar se tarefa pertence à etapa
    tarefa_service = TarefaService(db)
    tarefa = tarefa_service.obter_tarefa(tarefa_id, escritorio_id)
    
    if tarefa.etapa_id != etapa_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tarefa não pertence à etapa informada"
        )
    
    return tarefa_service.atualizar_tarefa(tarefa_id, tarefa_data, escritorio_id)


@router.delete("/{servico_id}/etapas/{etapa_id}/tarefas/{tarefa_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_tarefa_por_etapa(
    servico_id: int,
    etapa_id: int,
    tarefa_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """Deleta uma tarefa de uma etapa"""
    # Validar se etapa pertence ao serviço
    etapa_service = EtapaService(db)
    etapa = etapa_service.obter_etapa(etapa_id, escritorio_id)
    
    if etapa.servico_id != servico_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Etapa não pertence ao serviço informado"
        )
    
    # Validar se tarefa pertence à etapa
    tarefa_service = TarefaService(db)
    tarefa = tarefa_service.obter_tarefa(tarefa_id, escritorio_id)
    
    if tarefa.etapa_id != etapa_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tarefa não pertence à etapa informada"
        )
    
    tarefa_service.deletar_tarefa(tarefa_id, escritorio_id)


@router.put("/{servico_id}/etapas/{etapa_id}/tarefas/reordenar", response_model=List[TarefaResponse])
def reordenar_tarefas(
    servico_id: int,
    etapa_id: int,
    request: ReordenarTarefasRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """Reordena tarefas de uma etapa em lote"""
    # Validar se etapa pertence ao serviço
    etapa_service = EtapaService(db)
    etapa = etapa_service.obter_etapa(etapa_id, escritorio_id)
    
    if etapa.servico_id != servico_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Etapa não pertence ao serviço informado"
        )
    
    tarefa_service = TarefaService(db)
    return tarefa_service.reordenar_tarefas(etapa_id, request.tarefa_ids, escritorio_id)
