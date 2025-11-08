"""
Modelo de Proposta
"""
from sqlalchemy import Column, Integer, String, Text, Date, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin


class Proposta(Base, TimestampMixin):
    __tablename__ = "propostas"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("cliente.id"), nullable=False)
    servico_id = Column(Integer, ForeignKey("servicos.id"), nullable=False)
    status_id = Column(Integer, ForeignKey("status.id"), nullable=True)
    
    # Informações básicas
    nome = Column(String(255))
    descricao = Column(Text)
    identificacao = Column(String(255))  # Identificação do projeto
    numero_proposta = Column(Integer, nullable=False)
    ano_proposta = Column(Integer, nullable=False)
    
    # Datas
    data_proposta = Column(Date)
    
    # Valores
    valor_proposta = Column(Numeric(15, 2))
    valor_avista = Column(Numeric(15, 2))
    valor_parcela_aprazo = Column(String(255))  # Descrição das parcelas
    
    # Pagamento
    forma_pagamento = Column(String(200))
    prazo = Column(String(200))
    entrega_parcial = Column(String(8), default="Não")
    
    # Detalhes
    visitas_incluidas = Column(Integer)
    observacao = Column(Text)
    
    # Relacionamentos
    cliente = relationship("Cliente", backref="propostas")
    servico = relationship("Servico", backref="propostas")
    status = relationship("Status", backref="propostas")
    
    def __repr__(self):
        return f"<Proposta(id={self.id}, nome='{self.nome}')>"
