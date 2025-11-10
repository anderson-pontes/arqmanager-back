from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from app.database import get_db
from app.services.cliente import ClienteService
from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse
from app.api.deps import get_current_user, get_current_escritorio

router = APIRouter()


class ClienteListResponse(BaseModel):
    """Schema de resposta paginada"""
    items: List[ClienteResponse]
    total: int
    skip: int
    limit: int


@router.get("/test")
def test_clientes():
    """Endpoint de teste simples"""
    return {"message": "Endpoint de clientes funcionando!", "total": 135}


@router.get("/", response_model=ClienteListResponse)
def list_clientes(
    skip: int = Query(0, ge=0, description="Número de registros a pular"),
    limit: int = Query(20, ge=1, le=100, description="Número de registros por página"),
    ativo: Optional[bool] = None,
    tipo_pessoa: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """
    Lista todos os clientes com paginação, isolados por escritório
    
    Parâmetros:
    - skip: Número de registros a pular (padrão: 0)
    - limit: Número de registros por página (padrão: 20, máx: 100)
    - ativo: Filtrar por status (True/False)
    - tipo_pessoa: Filtrar por tipo (Física/Jurídica)
    - search: Buscar por nome, email, CPF/CNPJ ou cidade
    
    Retorna:
    - items: Lista de clientes
    - total: Total de clientes no banco
    - skip: Offset usado
    - limit: Limite usado
    """
    service = ClienteService(db)
    clientes = service.get_all(escritorio_id, skip=skip, limit=limit, ativo=ativo, tipo_pessoa=tipo_pessoa, search=search)
    total = service.count(escritorio_id, ativo=ativo, tipo_pessoa=tipo_pessoa, search=search)
    
    return {
        "items": clientes,
        "total": total,
        "skip": skip,
        "limit": limit
    }


@router.post("/", response_model=ClienteResponse, status_code=201)
def create_cliente(
    cliente: ClienteCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """
    Cria um novo cliente, vinculado ao escritório
    
    Validações:
    - Email único no escritório
    - CPF/CNPJ único no escritório
    - CPF: 11 dígitos para Pessoa Física
    - CNPJ: 14 dígitos para Pessoa Jurídica
    """
    service = ClienteService(db)
    return service.create(cliente, escritorio_id)


@router.get("/{cliente_id}", response_model=ClienteResponse)
def get_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """
    Busca um cliente por ID, garantindo que pertence ao escritório
    """
    service = ClienteService(db)
    return service.get_by_id(cliente_id, escritorio_id)


@router.put("/{cliente_id}", response_model=ClienteResponse)
def update_cliente(
    cliente_id: int,
    cliente: ClienteUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """
    Atualiza um cliente, garantindo que pertence ao escritório
    """
    service = ClienteService(db)
    return service.update(cliente_id, cliente, escritorio_id)


@router.delete("/{cliente_id}", status_code=204)
def delete_cliente(
    cliente_id: int,
    permanent: bool = Query(False, description="Se True, exclui permanentemente do banco"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """
    Remove um cliente, garantindo que pertence ao escritório
    
    Parâmetros:
    - permanent: False = Soft delete (marca como inativo)
    - permanent: True = Hard delete (remove do banco permanentemente)
    """
    service = ClienteService(db)
    service.delete(cliente_id, escritorio_id, permanent=permanent)


@router.get("/stats/count")
def count_clientes(
    ativo: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """
    Retorna total de clientes cadastrados, isolados por escritório
    
    Parâmetros:
    - ativo: Contar apenas ativos (True) ou inativos (False), ou todos (None)
    """
    service = ClienteService(db)
    return {
        "total": service.count(escritorio_id, ativo=ativo),
        "ativo": ativo
    }
