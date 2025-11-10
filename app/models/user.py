from sqlalchemy import Column, Integer, String, Boolean, Date, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel, TimestampMixin


# Tabela de associação User <-> Escritorio
user_escritorio = Table(
    'colaborador_escritorio',
    BaseModel.metadata,
    Column('colaborador_id', Integer, ForeignKey('colaborador.id'), primary_key=True),
    Column('escritorio_id', Integer, ForeignKey('escritorio.id'), primary_key=True),
    Column('perfil', String(50)),
    Column('ativo', Boolean, default=True)
)


class Escritorio(BaseModel, TimestampMixin):
    """Modelo de Escritório"""
    __tablename__ = "escritorio"
    
    nome_fantasia = Column(String(255), nullable=False)
    razao_social = Column(String(255), nullable=False)
    documento = Column(String(20), unique=True, nullable=True, index=True)  # CNPJ agora opcional
    cpf = Column(String(14), unique=True, nullable=True, index=True)  # CPF opcional
    email = Column(String(255), nullable=False)
    telefone = Column(String(20))
    # Endereço completo (mantido para compatibilidade)
    endereco = Column(String(500))
    # Campos de endereço separados
    logradouro = Column(String(255))  # Rua/Avenida
    numero = Column(String(20))  # Número
    complemento = Column(String(100))  # Complemento
    bairro = Column(String(100))  # Bairro
    cidade = Column(String(100))  # Cidade
    uf = Column(String(2))  # Estado (UF)
    cep = Column(String(10))  # CEP
    cor = Column(String(7), default="#6366f1")
    dias_uteis = Column(Boolean, default=True)
    prazo_arquiva_proposta = Column(Integer, default=30)
    observacao_proposta_padrao = Column(String(1000))
    observacao_contrato_padrao = Column(String(1000))
    ativo = Column(Boolean, default=True)
    
    # Relacionamentos
    colaboradores = relationship("User", secondary=user_escritorio, back_populates="escritorios")


class User(BaseModel, TimestampMixin):
    """Modelo de Usuário/Colaborador"""
    __tablename__ = "colaborador"
    
    nome = Column(String(255), nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    senha = Column(String(255), nullable=False)  # Hash da senha
    cpf = Column(String(14), unique=True, nullable=True, index=True)  # CPF agora é opcional
    telefone = Column(String(20))
    data_nascimento = Column(Date)
    perfil = Column(String(50), default="Colaborador")  # Admin, Gerente, Colaborador
    tipo = Column(String(20), default="Geral")  # Geral, Terceirizado
    ativo = Column(Boolean, default=True)
    foto = Column(String(500))
    ultimo_acesso = Column(Date)
    is_system_admin = Column(Boolean, default=False)  # Admin do sistema
    
    # PIX (opcional)
    tipo_pix = Column(String(20))
    chave_pix = Column(String(100))
    
    # Relacionamentos
    escritorios = relationship("Escritorio", secondary=user_escritorio, back_populates="colaboradores")
    
    def __repr__(self):
        return f"<User {self.nome} ({self.email})>"
