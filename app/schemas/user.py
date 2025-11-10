from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import date, datetime
from enum import Enum


class PerfilEnum(str, Enum):
    ADMIN = "Admin"
    GERENTE = "Gerente"
    COLABORADOR = "Colaborador"


class TipoColaboradorEnum(str, Enum):
    GERAL = "Geral"
    TERCEIRIZADO = "Terceirizado"


# Escritorio Schemas
class EscritorioBase(BaseModel):
    nome_fantasia: str
    razao_social: str
    documento: str
    email: EmailStr
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    cor: str = "#6366f1"


class EscritorioCreate(EscritorioBase):
    pass


class EscritorioUpdate(BaseModel):
    nome_fantasia: Optional[str] = None
    razao_social: Optional[str] = None
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    cor: Optional[str] = None


class EscritorioResponse(EscritorioBase):
    id: int
    ativo: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# User Schemas
class UserBase(BaseModel):
    nome: str
    email: EmailStr
    cpf: Optional[str] = None  # CPF agora é opcional
    telefone: Optional[str] = None
    data_nascimento: Optional[date] = None
    perfil: PerfilEnum = PerfilEnum.COLABORADOR
    tipo: TipoColaboradorEnum = TipoColaboradorEnum.GERAL
    
    @validator('cpf')
    def validate_cpf(cls, v):
        # Se CPF for fornecido, validar
        if v is None or v == '' or (isinstance(v, str) and not v.strip()):
            return None
        # Remove caracteres não numéricos
        cpf_clean = ''.join(filter(str.isdigit, str(v)))
        if len(cpf_clean) != 11:
            raise ValueError('CPF deve ter 11 dígitos')
        return cpf_clean


class UserCreate(UserBase):
    senha: str
    tipo_pix: Optional[str] = None
    chave_pix: Optional[str] = None
    is_system_admin: Optional[bool] = False  # NOVO
    
    @validator('senha')
    def validate_senha(cls, v):
        if len(v) < 6:
            raise ValueError('Senha deve ter no mínimo 6 caracteres')
        return v


class UserUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None
    data_nascimento: Optional[date] = None
    perfil: Optional[PerfilEnum] = None
    tipo: Optional[TipoColaboradorEnum] = None
    foto: Optional[str] = None
    ativo: Optional[bool] = None
    tipo_pix: Optional[str] = None
    chave_pix: Optional[str] = None
    senha: Optional[str] = None
    
    @validator('senha')
    def validate_senha(cls, v):
        if v is not None and len(v) < 6:
            raise ValueError('Senha deve ter no mínimo 6 caracteres')
        return v


class UserResponse(UserBase):
    id: int
    ativo: bool
    foto: Optional[str] = None
    ultimo_acesso: Optional[date] = None
    tipo_pix: Optional[str] = None
    chave_pix: Optional[str] = None
    is_system_admin: bool = False  # NOVO
    created_at: datetime
    updated_at: datetime
    escritorios: List[EscritorioResponse] = []
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    senha: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None
    email: Optional[str] = None


class EscritorioContextInfo(BaseModel):
    """Informações de escritório disponível"""
    id: int
    nome_fantasia: str
    razao_social: str
    cor: str
    perfil: Optional[str] = None  # Perfil do usuário neste escritório (se aplicável)


class SetContextRequest(BaseModel):
    """Request para definir contexto de escritório e perfil"""
    escritorio_id: Optional[int] = None  # None para área administrativa
    perfil: Optional[str] = None  # None para área administrativa


class SetContextResponse(BaseModel):
    """Response após definir contexto"""
    access_token: str
    escritorio_id: Optional[int] = None
    perfil: Optional[str] = None
    is_admin_mode: bool = False  # True quando está em modo administrativo


class UserWithToken(BaseModel):
    user: UserResponse
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    requires_escritorio_selection: bool = False
    is_system_admin: bool = False  # NOVO
    available_escritorios: List[EscritorioContextInfo] = []  # NOVO
