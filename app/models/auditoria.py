"""
Modelo de Auditoria/Logs
Registra todas as ações dos usuários por escritório
"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import BaseModel


class Auditoria(BaseModel):
    """Modelo de Auditoria - Registra ações dos usuários"""
    __tablename__ = "auditoria"
    
    usuario_id = Column(Integer, ForeignKey('colaborador.id'), nullable=False, index=True)
    escritorio_id = Column(Integer, ForeignKey('escritorio.id'), nullable=True, index=True)  # Nullable para ações administrativas
    acao = Column(String(100), nullable=False)  # CREATE, UPDATE, DELETE, VIEW, LOGIN, etc.
    entidade = Column(String(100), nullable=False)  # Cliente, Projeto, Proposta, etc.
    entidade_id = Column(Integer, nullable=True)  # ID da entidade afetada
    descricao = Column(Text)  # Descrição detalhada da ação
    ip_address = Column(String(45))  # IPv4 ou IPv6
    user_agent = Column(String(500))  # User agent do navegador
    dados_anteriores = Column(Text)  # JSON com dados antes da alteração (para UPDATE)
    dados_novos = Column(Text)  # JSON com dados após a alteração (para UPDATE)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    
    def __repr__(self):
        return f"<Auditoria(id={self.id}, usuario_id={self.usuario_id}, acao='{self.acao}', entidade='{self.entidade}')>"










