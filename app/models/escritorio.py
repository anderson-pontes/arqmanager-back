from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.models.base import BaseModel, TimestampMixin


class Escritorio(BaseModel, TimestampMixin):
    """Modelo de Escritório/Empresa"""
    __tablename__ = "escritorio"
    __table_args__ = {'extend_existing': True}
    __table_args__ = {'extend_existing': True}
    
    nome = Column(String(255), nullable=False)
    razao_social = Column(String(255))
    cnpj = Column(String(20), unique=True)
    email = Column(String(255))
    telefone = Column(String(20))
    
    # Endereço
    logradouro = Column(String(255))
    numero = Column(String(20))
    complemento = Column(String(100))
    bairro = Column(String(100))
    cidade = Column(String(100))
    uf = Column(String(2))
    cep = Column(String(10))
    
    ativo = Column(Boolean, default=True)
    
    # Relacionamentos
    # colaboradores = relationship("ColaboradorEscritorio", back_populates="escritorio")
    # contas_bancarias = relationship("ContaBancaria", back_populates="escritorio")
    
    def __repr__(self):
        return f"<Escritorio {self.nome}>"
