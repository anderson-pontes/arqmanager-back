from sqlalchemy import Column, String, Boolean, Text, Integer, ForeignKey
from app.models.base import BaseModel, TimestampMixin


class Indicacao(BaseModel, TimestampMixin):
    """Modelo de Indicação de Cliente"""
    __tablename__ = "indicacao"
    __table_args__ = {'extend_existing': True}
    
    nome = Column(String(255), nullable=False)
    telefone = Column(String(20))
    email = Column(String(255))
    observacao = Column(Text)
    ativo = Column(Boolean, default=True)
    escritorio_id = Column(Integer, ForeignKey('escritorio.id'), nullable=False, index=True)
    
    def __repr__(self):
        return f"<Indicacao {self.nome}>"
