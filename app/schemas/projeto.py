"""
Schemas para Projeto
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal


# Status
class StatusBase(BaseModel):
    descricao: str = Field(..., max_length=100)
    cor: Optional[str] = Field(None, max_length=7)
    ativo: bool = True


class StatusCreate(StatusBase):
    pass


class StatusUpdate(BaseModel):
    descricao: Optional[str] = Field(None, max_length=100)
    cor: Optional[str] = Field(None, max_length=7)
    ativo: Optional[bool] = None


class StatusResponse(StatusBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Projeto Colaborador
class ProjetoColaboradorBase(BaseModel):
    colaborador_id: int
    funcao: Optional[str] = Field(None, max_length=100)
    ativo: bool = True


class ProjetoColaboradorCreate(ProjetoColaboradorBase):
    pass


class ProjetoColaboradorResponse(ProjetoColaboradorBase):
    projeto_id: int

    class Config:
        from_attributes = True


# Projeto
class ProjetoBase(BaseModel):
    cliente_id: int
    servico_id: int
    status_id: Optional[int] = None
    descricao: str
    numero_projeto: Optional[int] = None
    ano_projeto: Optional[int] = None
    data_inicio: date
    data_previsao_fim: Optional[date] = None
    data_fim: Optional[date] = None
    metragem: Optional[Decimal] = None
    valor_contrato: Optional[Decimal] = None
    saldo_contrato: Optional[Decimal] = None
    observacao: Optional[str] = Field(None, max_length=255)
    observacao_contrato: Optional[str] = None
    cod_contratado: Optional[str] = Field(None, max_length=20)
    ativo: bool = True


class ProjetoCreate(ProjetoBase):
    colaboradores: Optional[List[ProjetoColaboradorCreate]] = []


class ProjetoUpdate(BaseModel):
    cliente_id: Optional[int] = None
    servico_id: Optional[int] = None
    status_id: Optional[int] = None
    descricao: Optional[str] = None
    numero_projeto: Optional[int] = None
    ano_projeto: Optional[int] = None
    data_inicio: Optional[date] = None
    data_previsao_fim: Optional[date] = None
    data_fim: Optional[date] = None
    metragem: Optional[Decimal] = None
    valor_contrato: Optional[Decimal] = None
    saldo_contrato: Optional[Decimal] = None
    observacao: Optional[str] = Field(None, max_length=255)
    observacao_contrato: Optional[str] = None
    cod_contratado: Optional[str] = Field(None, max_length=20)
    ativo: Optional[bool] = None


class ProjetoResponse(ProjetoBase):
    id: int
    proposta_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    colaboradores: List[ProjetoColaboradorResponse] = []

    class Config:
        from_attributes = True
