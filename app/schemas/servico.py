"""
Schemas para Serviço
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class EtapaBase(BaseModel):
    nome: str = Field(..., max_length=500)
    descricao: Optional[str] = None
    descricao_contrato: Optional[str] = None  # HTML/rich text para contrato
    ordem: int = 0
    obrigatoria: bool = True


class EtapaCreate(EtapaBase):
    pass


class EtapaUpdate(BaseModel):
    nome: Optional[str] = Field(None, max_length=500)
    descricao: Optional[str] = None
    descricao_contrato: Optional[str] = None  # HTML/rich text para contrato
    ordem: Optional[int] = None
    obrigatoria: Optional[bool] = None


class EtapaResponse(EtapaBase):
    id: int
    servico_id: int
    escritorio_id: int
    created_at: datetime
    updated_at: datetime
    tarefas: List["TarefaResponse"] = []

    class Config:
        from_attributes = True


class ServicoBase(BaseModel):
    nome: str = Field(..., max_length=500)
    descricao: Optional[str] = None
    descricao_contrato: Optional[str] = None
    valor_base: Optional[Decimal] = None
    unidade: Optional[str] = Field(None, max_length=50)
    codigo_plano_contas: Optional[str] = Field(None, max_length=50)
    ativo: bool = True


class ServicoCreate(ServicoBase):
    etapas: Optional[List[EtapaCreate]] = []


class ServicoUpdate(BaseModel):
    nome: Optional[str] = Field(None, max_length=500)
    descricao: Optional[str] = None
    descricao_contrato: Optional[str] = None
    valor_base: Optional[Decimal] = None
    unidade: Optional[str] = Field(None, max_length=50)
    codigo_plano_contas: Optional[str] = Field(None, max_length=50)
    ativo: Optional[bool] = None


class ServicoResponse(ServicoBase):
    id: int
    escritorio_id: int
    created_at: datetime
    updated_at: datetime
    etapas: List[EtapaResponse] = []

    class Config:
        from_attributes = True


# Schemas de Tarefa
class TarefaBase(BaseModel):
    nome: str = Field(..., max_length=500)
    ordem: int = 0
    cor: Optional[str] = Field(None, max_length=50)
    tem_prazo: bool = True
    precisa_detalhamento: bool = False


class TarefaCreate(TarefaBase):
    pass


class TarefaUpdate(BaseModel):
    nome: Optional[str] = Field(None, max_length=500)
    ordem: Optional[int] = None
    cor: Optional[str] = Field(None, max_length=50)
    tem_prazo: Optional[bool] = None
    precisa_detalhamento: Optional[bool] = None


class TarefaResponse(TarefaBase):
    id: int
    etapa_id: int
    escritorio_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ReordenarEtapasRequest(BaseModel):
    """Request para reordenar etapas em lote"""
    etapa_ids: List[int] = Field(..., description="Lista de IDs das etapas na nova ordem")


class ReordenarTarefasRequest(BaseModel):
    """Request para reordenar tarefas em lote"""
    tarefa_ids: List[int] = Field(..., description="Lista de IDs das tarefas na nova ordem")
