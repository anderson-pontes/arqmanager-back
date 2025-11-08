"""
Schemas para Movimento Financeiro
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from decimal import Decimal


class MovimentoBase(BaseModel):
    projeto_id: Optional[int] = None
    tipo: int  # 1=Despesa, 2=Receita, etc
    data_entrada: date
    data_efetivacao: Optional[date] = None
    competencia: Optional[date] = None
    descricao: str = Field(..., max_length=255)
    observacao: Optional[str] = Field(None, max_length=255)
    valor: Decimal
    valor_acrescido: Optional[Decimal] = None
    valor_desconto: Optional[Decimal] = None
    valor_resultante: Optional[Decimal] = None
    comprovante: Optional[str] = Field(None, max_length=255)
    extensao: Optional[str] = Field(None, max_length=10)
    codigo_plano_contas: Optional[str] = Field(None, max_length=50)
    ativo: bool = True


class MovimentoCreate(MovimentoBase):
    pass


class MovimentoUpdate(BaseModel):
    projeto_id: Optional[int] = None
    tipo: Optional[int] = None
    data_entrada: Optional[date] = None
    data_efetivacao: Optional[date] = None
    competencia: Optional[date] = None
    descricao: Optional[str] = Field(None, max_length=255)
    observacao: Optional[str] = Field(None, max_length=255)
    valor: Optional[Decimal] = None
    valor_acrescido: Optional[Decimal] = None
    valor_desconto: Optional[Decimal] = None
    valor_resultante: Optional[Decimal] = None
    comprovante: Optional[str] = Field(None, max_length=255)
    extensao: Optional[str] = Field(None, max_length=10)
    codigo_plano_contas: Optional[str] = Field(None, max_length=50)
    ativo: Optional[bool] = None


class MovimentoResponse(MovimentoBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
