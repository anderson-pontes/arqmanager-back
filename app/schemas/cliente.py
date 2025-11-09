from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import date, datetime
from enum import Enum


class TipoPessoaEnum(str, Enum):
    FISICA = "Física"
    JURIDICA = "Jurídica"


class EnderecoBase(BaseModel):
    logradouro: str
    numero: str
    complemento: Optional[str] = None
    bairro: str
    cidade: str
    uf: str
    cep: str
    
    @validator('uf')
    def validate_uf(cls, v):
        if len(v) != 2:
            raise ValueError('UF deve ter 2 caracteres')
        return v.upper()
    
    @validator('cep')
    def validate_cep(cls, v):
        # Remove caracteres não numéricos
        cep = ''.join(filter(str.isdigit, v))
        if len(cep) != 8:
            raise ValueError('CEP deve ter 8 dígitos')
        return cep


class ClienteBase(BaseModel):
    nome: str
    razao_social: Optional[str] = None
    email: EmailStr
    identificacao: str
    tipo_pessoa: TipoPessoaEnum
    telefone: str
    whatsapp: Optional[str] = None
    data_nascimento: Optional[date] = None
    logradouro: Optional[str] = None  # ✅ Opcional
    numero: Optional[str] = None  # ✅ Opcional
    complemento: Optional[str] = None
    bairro: Optional[str] = None  # ✅ Opcional
    cidade: Optional[str] = None  # ✅ Opcional
    uf: Optional[str] = None  # ✅ Opcional
    cep: Optional[str] = None  # ✅ Opcional
    inscricao_estadual: Optional[str] = None
    inscricao_municipal: Optional[str] = None
    indicado_por: Optional[str] = None
    
    @validator('identificacao')
    def validate_identificacao(cls, v, values):
        # Remove caracteres não numéricos
        doc = ''.join(filter(str.isdigit, v))
        
        tipo = values.get('tipo_pessoa')
        if tipo == TipoPessoaEnum.FISICA:
            if len(doc) != 11:
                raise ValueError('CPF deve ter 11 dígitos')
        elif tipo == TipoPessoaEnum.JURIDICA:
            if len(doc) != 14:
                raise ValueError('CNPJ deve ter 14 dígitos')
        
        return doc
    
    @validator('uf')
    def validate_uf(cls, v):
        if v and len(v) != 2:  # ✅ Só valida se não for None
            raise ValueError('UF deve ter 2 caracteres')
        return v.upper() if v else None
    
    @validator('cep')
    def validate_cep(cls, v):
        if not v:  # ✅ Se for None, retorna None
            return None
        cep = ''.join(filter(str.isdigit, v))
        if len(cep) != 8:
            raise ValueError('CEP deve ter 8 dígitos')
        return cep


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    nome: Optional[str] = None
    razao_social: Optional[str] = None
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None
    whatsapp: Optional[str] = None
    data_nascimento: Optional[date] = None
    logradouro: Optional[str] = None
    numero: Optional[str] = None
    complemento: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None
    cep: Optional[str] = None
    inscricao_estadual: Optional[str] = None
    inscricao_municipal: Optional[str] = None
    indicado_por: Optional[str] = None
    ativo: Optional[bool] = None


class ClienteResponse(BaseModel):
    id: int
    nome: str
    razao_social: Optional[str] = None
    email: str
    identificacao: str
    tipo_pessoa: str  # ✅ String simples, sem Enum
    telefone: str
    whatsapp: Optional[str] = None
    data_nascimento: Optional[date] = None
    logradouro: Optional[str] = None
    numero: Optional[str] = None
    complemento: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None
    cep: Optional[str] = None
    inscricao_estadual: Optional[str] = None
    inscricao_municipal: Optional[str] = None
    indicado_por: Optional[str] = None
    ativo: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
