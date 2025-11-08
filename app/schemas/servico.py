"""
Schemas para Serviço
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class EtapaBase(BaseModel):
    nome: str = Field(..., max_length=200)
    descricao: Optional[str] = None
    ordem: int = 0
    obrigatoria: bool = True


class EtapaCreate(EtapaBase):
    pass


class EtapaUpdate(BaseModel):
    nome: Optional[str] = Field(None, max_length=200)
    descricao: Optional[str] = None
    ordem: Optional[int] = None
    obrigatoria: Optional[bool] = None


class EtapaResponse(EtapaBase):
    id: int
    servico_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ServicoBase(BaseModel):
    nome: str = Field(..., max_length=200)
    descricao: Optional[str] = None
    valor_base: Optional[Decimal] = None
    unidade: Optional[str] = Field(None, max_length=50)
    ativo: bool = True


class ServicoCreate(ServicoBase):
    etapas: Optional[List[EtapaCreate]] = []


class ServicoUpdate(BaseModel):
    nome: Optional[str] = Field(None, max_length=200)
    descricao: Optional[str] = None
    valor_base: Optional[Decimal] = None
    unidade: Optional[str] = Field(None, max_length=50)
    ativo: Optional[bool] = None


class ServicoResponse(ServicoBase):
    id: int
    created_at: datetime
    updated_at: datetime
    etapas: List[EtapaResponse] = []

    class Config:
        from_attributes = True
