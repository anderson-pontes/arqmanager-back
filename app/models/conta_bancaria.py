from sqlalchemy import Column, Integer, String, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel, TimestampMixin


class ContaBancaria(BaseModel, TimestampMixin):
    """Modelo de Conta Bancária"""
    __tablename__ = "conta_bancaria"
    __table_args__ = {'extend_existing': True}
    
    nome = Column(String(255), nullable=False)
    banco = Column(String(255))
    agencia = Column(String(20))
    conta = Column(String(20))
    tipo = Column(String(50))  # corrente, poupanca, etc
    saldo_inicial = Column(Numeric(10, 2), default=0)
    escritorio_id = Column(Integer, ForeignKey('escritorio.id'))
    ativo = Column(Boolean, default=True)
    
    # Relacionamentos
    # escritorio = relationship("Escritorio", back_populates="contas_bancarias")
    # movimentacoes = relationship("ContaMovimentacao", back_populates="conta_bancaria")
    
    def __repr__(self):
        return f"<ContaBancaria {self.nome} - {self.banco}>"
