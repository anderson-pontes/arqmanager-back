from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.models.base import BaseModel, TimestampMixin


class ProjetoArquivamento(BaseModel, TimestampMixin):
    """Modelo de Arquivamento de Projeto"""
    __tablename__ = "projeto_arquivamento"
    __table_args__ = {'extend_existing': True}
    
    projeto_id = Column(Integer, ForeignKey('projetos.id'), nullable=False)
    data_arquivamento = Column(Date, nullable=False)
    motivo = Column(String(255))
    observacao = Column(Text)
    ativo = Column(Boolean, default=True)
    
    # Relacionamentos
    # projeto = relationship("Projeto")
    
    def __repr__(self):
        return f"<ProjetoArquivamento projeto_id={self.projeto_id}>"
