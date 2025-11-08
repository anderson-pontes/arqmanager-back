"""
Modelo de Movimento Financeiro
"""
from sqlalchemy import Column, Integer, String, Date, Numeric, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin


class Movimento(Base, TimestampMixin):
    __tablename__ = "movimentos"

    id = Column(Integer, primary_key=True, index=True)
    projeto_id = Column(Integer, ForeignKey("projetos.id"), nullable=True)
    
    # Tipo: 1=Despesa, 2=Receita, 3=Transferência, etc
    tipo = Column(Integer, nullable=False)  # cod_despesa_receita_tipo
    
    # Datas
    data_entrada = Column(Date, nullable=False)
    data_efetivacao = Column(Date)
    competencia = Column(Date)
    
    # Descrição
    descricao = Column(String(255), nullable=False)
    observacao = Column(String(255))
    
    # Valores
    valor = Column(Numeric(15, 2), nullable=False)
    valor_acrescido = Column(Numeric(15, 2))  # Juros
    valor_desconto = Column(Numeric(15, 2))  # Desconto
    valor_resultante = Column(Numeric(15, 2))  # Valor final
    
    # Comprovante
    comprovante = Column(String(255))  # Path do arquivo
    extensao = Column(String(10))
    
    # Plano de contas
    codigo_plano_contas = Column(String(50))
    
    # Controle
    ativo = Column(Boolean, default=True)
    
    # Relacionamentos
    projeto = relationship("Projeto", backref="movimentos")
    
    def __repr__(self):
        return f"<Movimento(id={self.id}, descricao='{self.descricao}', valor={self.valor})>"
