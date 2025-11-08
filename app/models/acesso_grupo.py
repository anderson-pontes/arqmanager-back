from sqlalchemy import Column, String, Boolean
from app.models.base import BaseModel, TimestampMixin


class AcessoGrupo(BaseModel, TimestampMixin):
    """Modelo de Grupo de Acesso"""
    __tablename__ = "acesso_grupo"
    __table_args__ = {'extend_existing': True}
    
    descricao = Column(String(255), nullable=False)
    ativo = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<AcessoGrupo {self.descricao}>"
