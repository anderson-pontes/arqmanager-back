from sqlalchemy import Column, Integer, String, Numeric, Date, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.models.base import BaseModel, TimestampMixin


class ProjetoPagamento(BaseModel, TimestampMixin):
    """Modelo de Pagamento de Projeto"""
    __tablename__ = "projeto_pagamento"
    __table_args__ = {'extend_existing': True}
    
    projeto_id = Column(Integer, ForeignKey('projetos.id'), nullable=False)
    forma_pagamento_id = Column(Integer, ForeignKey('forma_pagamento.id'))
    valor = Column(Numeric(10, 2), nullable=False)
    valor_recebido = Column(Numeric(10, 2))
    data_prevista = Column(Date)
    data_recebimento = Column(Date)
    observacao = Column(Text)
    ativo = Column(Boolean, default=True)
    escritorio_id = Column(Integer, ForeignKey('escritorio.id'), nullable=False, index=True)
    
    # Relacionamentos
    # projeto = relationship("Projeto", back_populates="pagamentos")
    # forma_pagamento = relationship("FormaPagamento")
    
    def __repr__(self):
        return f"<ProjetoPagamento projeto_id={self.projeto_id} valor={self.valor}>"
