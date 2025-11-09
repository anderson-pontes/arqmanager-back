from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional
from datetime import date, datetime
from enum import Enum


class TipoPessoaEnum(str, Enum):
    FISICA = "fisica"
    JURIDICA = "juridica"


class ClienteCreate(BaseModel):
    nome: str
    email: Optional[str] = None
    telefone: Optional[str] = None
    cpf_cnpj: Optional[str] = None
    tipo_pessoa: str = "fisica"
    data_nascimento: Optional[date] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None
    observacoes: Optional[str] = None
    ativo: Optional[bool] = True
    
    @validator('tipo_pessoa')
    def normalize_tipo_pessoa(cls, v):
        """Normaliza tipo_pessoa para o formato do banco"""
        if v:
            tipo_map = {
                'fisica': 'Física',
                'juridica': 'Jurídica',
                'Física': 'Física',
                'Jurídica': 'Jurídica'
            }
            return tipo_map.get(v, 'Física')
        return 'Física'


class ClienteUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    cpf_cnpj: Optional[str] = None
    tipo_pessoa: Optional[str] = None
    data_nascimento: Optional[date] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None
    observacoes: Optional[str] = None
    ativo: Optional[bool] = None
    
    @validator('tipo_pessoa')
    def normalize_tipo_pessoa(cls, v):
        """Normaliza tipo_pessoa para o formato do banco"""
        if v:
            tipo_map = {
                'fisica': 'Física',
                'juridica': 'Jurídica',
                'Física': 'Física',
                'Jurídica': 'Jurídica'
            }
            return tipo_map.get(v, v)
        return v


class ClienteResponse(BaseModel):
    id: int
    nome: str
    email: Optional[str] = None
    telefone: Optional[str] = None
    cpf_cnpj: Optional[str] = None
    tipo_pessoa: str
    data_nascimento: Optional[date] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None
    observacoes: Optional[str] = None
    ativo: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
    
    @classmethod
    def from_orm(cls, obj, db=None):
        """Converte modelo do banco para resposta da API com mapeamento de campos"""
        # Processar indicado_por: se for um ID numérico, buscar o nome do cliente
        observacoes = obj.indicado_por
        if observacoes and observacoes.isdigit() and db:
            try:
                from app.models.cliente import Cliente
                indicador_id = int(observacoes)
                indicador = db.query(Cliente).filter(Cliente.id == indicador_id).first()
                if indicador:
                    observacoes = f"Indicado por: {indicador.nome}"
            except:
                pass  # Se der erro, mantém o valor original
        
        return cls(
            id=obj.id,
            nome=obj.nome,
            email=obj.email or None,
            telefone=obj.telefone or None,
            cpf_cnpj=obj.identificacao or None,  # Mapear identificacao -> cpf_cnpj
            tipo_pessoa=cls._normalize_tipo_pessoa(obj.tipo_pessoa),
            data_nascimento=obj.data_nascimento,
            endereco=obj.logradouro or None,  # Mapear logradouro -> endereco
            cidade=obj.cidade or None,
            estado=obj.uf or None,  # Mapear uf -> estado
            cep=obj.cep or None,
            observacoes=observacoes,  # Mapear indicado_por -> observacoes (com nome se for ID)
            ativo=obj.ativo,
            created_at=obj.created_at,
            updated_at=obj.updated_at
        )
    
    @staticmethod
    def _normalize_tipo_pessoa(v):
        """Normaliza tipo_pessoa para lowercase"""
        if v:
            tipo_map = {
                'Física': 'fisica',
                'Jurídica': 'juridica',
                'fisica': 'fisica',
                'juridica': 'juridica'
            }
            return tipo_map.get(v, v.lower() if isinstance(v, str) else v)
        return v
