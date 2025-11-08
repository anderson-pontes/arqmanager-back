"""
Modelo de Projeto
"""
from sqlalchemy import Column, Integer, String, Text, Date, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin


class Projeto(Base, TimestampMixin):
    __tablename__ = "projetos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("cliente.id"), nullable=False)
    servico_id = Column(Integer, ForeignKey("servicos.id"), nullable=False)
    proposta_id = Column(Integer, nullable=True)  # FK para proposta (fase futura)
    status_id = Column(Integer, ForeignKey("status.id"), nullable=True)
    
    # Informações básicas
    descricao = Column(Text, nullable=False)
    numero_projeto = Column(Integer)
    ano_projeto = Column(Integer)
    
    # Datas
    data_inicio = Column(Date, nullable=False)
    data_previsao_fim = Column(Date)
    data_fim = Column(Date)
    
    # Valores e medidas
    metragem = Column(Numeric(8, 2))
    valor_contrato = Column(Numeric(15, 2))
    saldo_contrato = Column(Numeric(15, 2))
    
    # Observações
    observacao = Column(String(255))
    observacao_contrato = Column(Text)
    
    # Controle
    cod_contratado = Column(String(20))  # Código do contratado
    ativo = Column(Boolean, default=True)
    
    # Relacionamentos
    cliente = relationship("Cliente", backref="projetos")
    servico = relationship("Servico", backref="projetos")
    status = relationship("Status", backref="projetos")
    colaboradores = relationship("ProjetoColaborador", back_populates="projeto", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Projeto(id={self.id}, descricao='{self.descricao[:30]}...')>"
