from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from app.models.base import BaseModel, TimestampMixin


class FormaPagamento(BaseModel, TimestampMixin):
    """Modelo de Forma de Pagamento"""
    __tablename__ = "forma_pagamento"
    __table_args__ = {'extend_existing': True}
    
    descricao = Column(String(255), nullable=False)
    ativo = Column(Boolean, default=True)
    escritorio_id = Column(Integer, ForeignKey('escritorio.id'), nullable=False, index=True)
    
    def __repr__(self):
        return f"<FormaPagamento {self.descricao}>"
