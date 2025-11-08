"""
Modelo de Etapa
"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin


class Etapa(Base, TimestampMixin):
    __tablename__ = "etapas"

    id = Column(Integer, primary_key=True, index=True)
    servico_id = Column(Integer, ForeignKey("servicos.id"), nullable=False)
    nome = Column(String(200), nullable=False)
    descricao = Column(Text)
    ordem = Column(Integer, default=0)
    obrigatoria = Column(Boolean, default=True)
    
    # Relacionamentos
    servico = relationship("Servico", back_populates="etapas")
    
    def __repr__(self):
        return f"<Etapa(id={self.id}, nome='{self.nome}', servico_id={self.servico_id})>"
