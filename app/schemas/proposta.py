"""
Schemas para Proposta
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from decimal import Decimal


class PropostaBase(BaseModel):
    cliente_id: int
    servico_id: int
    status_id: Optional[int] = None
    nome: Optional[str] = Field(None, max_length=255)
    descricao: Optional[str] = None
    identificacao: Optional[str] = Field(None, max_length=255)
    numero_proposta: int
    ano_proposta: int
    data_proposta: Optional[date] = None
    valor_proposta: Optional[Decimal] = None
    valor_avista: Optional[Decimal] = None
    valor_parcela_aprazo: Optional[str] = Field(None, max_length=255)
    forma_pagamento: Optional[str] = Field(None, max_length=200)
    prazo: Optional[str] = Field(None, max_length=200)
    entrega_parcial: str = Field(default="Não", max_length=8)
    visitas_incluidas: Optional[int] = None
    observacao: Optional[str] = None


class PropostaCreate(PropostaBase):
    pass


class PropostaUpdate(BaseModel):
    cliente_id: Optional[int] = None
    servico_id: Optional[int] = None
    status_id: Optional[int] = None
    nome: Optional[str] = Field(None, max_length=255)
    descricao: Optional[str] = None
    identificacao: Optional[str] = Field(None, max_length=255)
    numero_proposta: Optional[int] = None
    ano_proposta: Optional[int] = None
    data_proposta: Optional[date] = None
    valor_proposta: Optional[Decimal] = None
    valor_avista: Optional[Decimal] = None
    valor_parcela_aprazo: Optional[str] = Field(None, max_length=255)
    forma_pagamento: Optional[str] = Field(None, max_length=200)
    prazo: Optional[str] = Field(None, max_length=200)
    entrega_parcial: Optional[str] = Field(None, max_length=8)
    visitas_incluidas: Optional[int] = None
    observacao: Optional[str] = None


class PropostaResponse(PropostaBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
