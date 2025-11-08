"""
Modelo de Serviço
"""
from sqlalchemy import Column, Integer, String, Numeric, Boolean, Text
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin


class Servico(Base, TimestampMixin):
    __tablename__ = "servicos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(500), nullable=False, index=True)
    descricao = Column(Text)  # desc_documento no MySQL
    descricao_contrato = Column(Text)  # Para compatibilidade futura
    valor_base = Column(Numeric(10, 2))
    unidade = Column(String(50))  # m², unidade, hora, etc.
    codigo_plano_contas = Column(String(50))  # Código do plano de contas
    ativo = Column(Boolean, default=True)
    
    # Relacionamentos
    etapas = relationship("Etapa", back_populates="servico", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Servico(id={self.id}, nome='{self.nome}')>"
