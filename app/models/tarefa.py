"""
Modelo de Tarefa (Microserviço)
"""
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin


class Tarefa(Base, TimestampMixin):
    __tablename__ = "tarefas"

    id = Column(Integer, primary_key=True, index=True)
    etapa_id = Column(Integer, ForeignKey("etapas.id", ondelete="CASCADE"), nullable=False, index=True)
    nome = Column(String(500), nullable=False)  # descricao no MySQL
    ordem = Column(Integer, default=0)
    cor = Column(String(50))  # Hex color (ex: #FF5733)
    tem_prazo = Column(Boolean, default=True)  # prazo no MySQL
    precisa_detalhamento = Column(Boolean, default=False)  # detalhe no MySQL
    escritorio_id = Column(Integer, ForeignKey("escritorio.id"), nullable=False, index=True)
    
    # Relacionamentos
    etapa = relationship("Etapa", back_populates="tarefas")
    
    def __repr__(self):
        return f"<Tarefa(id={self.id}, nome='{self.nome}', etapa_id={self.etapa_id})>"


