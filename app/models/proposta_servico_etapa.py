from sqlalchemy import Column, Integer, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel, TimestampMixin


class PropostaServicoEtapa(BaseModel, TimestampMixin):
    """Modelo de Etapa de Proposta"""
    __tablename__ = "proposta_servico_etapa"
    __table_args__ = {'extend_existing': True}
    
    proposta_id = Column(Integer, ForeignKey('propostas.id'), nullable=False)
    etapa_id = Column(Integer, ForeignKey('etapas.id'), nullable=False)
    prazo = Column(Integer)  # Prazo em dias
    data_prevista = Column(Date)
    data_conclusao = Column(Date)
    observacao = Column(Text)
    
    # Relacionamentos
    # proposta = relationship("Proposta", back_populates="etapas")
    # etapa = relationship("Etapa")
    
    def __repr__(self):
        return f"<PropostaServicoEtapa proposta_id={self.proposta_id} etapa_id={self.etapa_id}>"
