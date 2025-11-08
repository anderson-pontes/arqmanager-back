from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func
from app.database import Base


class TimestampMixin:
    """Mixin para adicionar timestamps automáticos"""
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class BaseModel(Base):
    """Modelo base abstrato"""
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
