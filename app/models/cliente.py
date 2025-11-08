from sqlalchemy import Column, Integer, String, Boolean, Date
from sqlalchemy.orm import relationship
from app.models.base import BaseModel, TimestampMixin


class Cliente(BaseModel, TimestampMixin):
    """Modelo de Cliente"""
    __tablename__ = "cliente"
    
    nome = Column(String(255), nullable=False, index=True)
    razao_social = Column(String(255))
    email = Column(String(255), nullable=False, index=True)
    identificacao = Column(String(20), unique=True, nullable=False, index=True)  # CPF ou CNPJ
    tipo_pessoa = Column(String(20), nullable=False)  # "Física" ou "Jurídica"
    telefone = Column(String(20), nullable=False)
    whatsapp = Column(String(20))
    data_nascimento = Column(Date)
    ativo = Column(Boolean, default=True)
    
    # Endereço
    logradouro = Column(String(255))
    numero = Column(String(20))
    complemento = Column(String(100))
    bairro = Column(String(100))
    cidade = Column(String(100))
    uf = Column(String(2))
    cep = Column(String(10))
    
    # Inscrições (para PJ)
    inscricao_estadual = Column(String(20))
    inscricao_municipal = Column(String(20))
    
    # Indicação
    indicado_por = Column(String(255))
    
    # Relacionamentos
    # projetos = relationship("Projeto", back_populates="cliente")
    # propostas = relationship("Proposta", back_populates="cliente")
    
    def __repr__(self):
        return f"<Cliente {self.nome} ({self.identificacao})>"
