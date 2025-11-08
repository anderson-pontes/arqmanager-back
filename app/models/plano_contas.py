from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel, TimestampMixin


class PlanoContas(BaseModel, TimestampMixin):
    """Modelo de Plano de Contas"""
    __tablename__ = "plano_contas"
    __table_args__ = {'extend_existing': True}
    
    codigo = Column(String(20), nullable=False)
    descricao = Column(String(255), nullable=False)
    tipo = Column(String(50), nullable=False)  # receita, despesa, ativo, passivo
    nivel = Column(Integer, default=1)
    plano_contas_pai_id = Column(Integer, ForeignKey('plano_contas.id'))
    escritorio_id = Column(Integer, ForeignKey('escritorio.id'))
    ativo = Column(Boolean, default=True)
    
    # Relacionamentos
    # plano_contas_pai = relationship("PlanoContas", remote_side=[id])
    # escritorio = relationship("Escritorio")
    
    def __repr__(self):
        return f"<PlanoContas {self.codigo} - {self.descricao}>"
