from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.models.base import BaseModel, TimestampMixin


class ProjetoDocumento(BaseModel, TimestampMixin):
    """Modelo de Documento de Projeto"""
    __tablename__ = "projeto_documento"
    __table_args__ = {'extend_existing': True}
    
    projeto_id = Column(Integer, ForeignKey('projetos.id'), nullable=False)
    tipo_documento_id = Column(Integer)  # Referência para arquivo_tipo
    nome = Column(String(255), nullable=False)
    arquivo = Column(String(500))  # Caminho do arquivo
    extensao = Column(String(10))
    observacao = Column(Text)
    ativo = Column(Boolean, default=True)
    
    # Relacionamentos
    # projeto = relationship("Projeto", back_populates="documentos")
    
    def __repr__(self):
        return f"<ProjetoDocumento {self.nome}>"
