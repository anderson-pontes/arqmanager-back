"""
Modelo de Status
"""
from sqlalchemy import Column, Integer, String, Boolean
from app.models.base import Base, TimestampMixin


class Status(Base, TimestampMixin):
    __tablename__ = "status"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String(100), nullable=False)
    cor = Column(String(7))  # Cor em hexadecimal
    ativo = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<Status(id={self.id}, descricao='{self.descricao}')>"
