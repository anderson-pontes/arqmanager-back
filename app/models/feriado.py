from sqlalchemy import Column, String, Date, Boolean, Integer, ForeignKey
from app.models.base import BaseModel, TimestampMixin


class Feriado(BaseModel, TimestampMixin):
    """Modelo de Feriado"""
    __tablename__ = "feriados"
    __table_args__ = {'extend_existing': True}
    
    data = Column(Date, nullable=False)
    descricao = Column(String(255), nullable=False)
    tipo = Column(String(50))  # nacional, estadual, municipal
    ativo = Column(Boolean, default=True)
    escritorio_id = Column(Integer, ForeignKey('escritorio.id'), nullable=False, index=True)
    
    def __repr__(self):
        return f"<Feriado {self.data} - {self.descricao}>"
