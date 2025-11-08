from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel, TimestampMixin


class ColaboradorEscritorio(BaseModel, TimestampMixin):
    """Modelo de relacionamento Colaborador-Escritório"""
    __tablename__ = "colaborador_escritorio"
    __table_args__ = {'extend_existing': True}
    
    colaborador_id = Column(Integer, ForeignKey('colaborador.id'), nullable=False, index=True)
    escritorio_id = Column(Integer, ForeignKey('escritorio.id'), nullable=False, index=True)
    tipo = Column(Integer)  # 1=Geral, 2=Terceirizado
    socio = Column(Boolean, default=False)
    pix_tipo = Column(String(50))
    pix_chave = Column(String(255))
    
    # Relacionamentos
    # colaborador = relationship("Colaborador", back_populates="escritorios")
    # escritorio = relationship("Escritorio", back_populates="colaboradores")
    
    def __repr__(self):
        return f"<ColaboradorEscritorio colaborador_id={self.colaborador_id} escritorio_id={self.escritorio_id}>"
