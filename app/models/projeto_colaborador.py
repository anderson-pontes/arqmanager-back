"""
Modelo de Projeto Colaborador (relacionamento N:N)
"""
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base


class ProjetoColaborador(Base):
    __tablename__ = "projeto_colaborador"

    projeto_id = Column(Integer, ForeignKey("projetos.id"), primary_key=True)
    colaborador_id = Column(Integer, ForeignKey("colaborador.id"), primary_key=True)
    funcao = Column(String(100))  # Função do colaborador no projeto
    ativo = Column(Boolean, default=True)
    
    # Relacionamentos
    projeto = relationship("Projeto", back_populates="colaboradores")
    colaborador = relationship("User", backref="projetos")
    
    def __repr__(self):
        return f"<ProjetoColaborador(projeto_id={self.projeto_id}, colaborador_id={self.colaborador_id})>"
