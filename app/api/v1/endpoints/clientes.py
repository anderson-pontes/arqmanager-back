from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from app.database import get_db
from app.services.cliente import ClienteService
from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse
from app.api.deps import get_current_user

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
    current_user: dict = Depends(get_current_user)
):
    """
    Lista todos os clientes com paginação
    
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
    clientes = service.get_all(skip=skip, limit=limit, ativo=ativo, tipo_pessoa=tipo_pessoa, search=search)
    total = service.count(ativo=ativo, tipo_pessoa=tipo_pessoa, search=search)  # ✅ Passa search para count
    
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
    current_user: dict = Depends(get_current_user)
):
    """
    Cria um novo cliente
    
    Validações:
    - Email único
    - CPF/CNPJ único
    - CPF: 11 dígitos para Pessoa Física
    - CNPJ: 14 dígitos para Pessoa Jurídica
    """
    service = ClienteService(db)
    return service.create(cliente)


@router.get("/{cliente_id}", response_model=ClienteResponse)
def get_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Busca um cliente por ID
    """
    service = ClienteService(db)
    return service.get_by_id(cliente_id)


@router.put("/{cliente_id}", response_model=ClienteResponse)
def update_cliente(
    cliente_id: int,
    cliente: ClienteUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Atualiza um cliente
    """
    service = ClienteService(db)
    return service.update(cliente_id, cliente)


@router.delete("/{cliente_id}", status_code=204)
def delete_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Remove um cliente (soft delete)
    """
    service = ClienteService(db)
    service.delete(cliente_id)


@router.get("/stats/count")
def count_clientes(
    ativo: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Retorna total de clientes cadastrados
    
    Parâmetros:
    - ativo: Contar apenas ativos (True) ou inativos (False), ou todos (None)
    """
    service = ClienteService(db)
    return {
        "total": service.count(ativo),
        "ativo": ativo
    }
