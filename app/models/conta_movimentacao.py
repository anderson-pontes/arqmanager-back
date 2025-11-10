from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.models.base import BaseModel, TimestampMixin


class ContaMovimentacao(BaseModel, TimestampMixin):
    """Modelo de Movimentação de Conta Bancária"""
    __tablename__ = "conta_movimentacao"
    __table_args__ = {'extend_existing': True}
    
    conta_bancaria_id = Column(Integer, ForeignKey('conta_bancaria.id'), nullable=False)
    data = Column(Date, nullable=False)
    descricao = Column(String(255), nullable=False)
    valor = Column(Numeric(10, 2), nullable=False)
    tipo = Column(String(20), nullable=False)  # receita, despesa
    saldo = Column(Numeric(10, 2))
    movimento_id = Column(Integer, ForeignKey('movimentos.id'))
    escritorio_id = Column(Integer, ForeignKey('escritorio.id'), nullable=False, index=True)
    
    # Relacionamentos
    # conta_bancaria = relationship("ContaBancaria", back_populates="movimentacoes")
    # movimento = relationship("Movimento")
    
    def __repr__(self):
        return f"<ContaMovimentacao {self.descricao} - {self.valor}>"
