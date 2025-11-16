"""
Serviço de Auditoria
Registra ações dos usuários por escritório
"""
from sqlalchemy.orm import Session
from app.models.auditoria import Auditoria
from typing import Optional, Dict, Any
import json
from datetime import datetime


class AuditoriaService:
    """Serviço para registrar ações de auditoria"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def registrar(
        self,
        usuario_id: int,
        acao: str,
        entidade: str,
        escritorio_id: Optional[int] = None,
        entidade_id: Optional[int] = None,
        descricao: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        dados_anteriores: Optional[Dict[str, Any]] = None,
        dados_novos: Optional[Dict[str, Any]] = None
    ) -> Auditoria:
        """
        Registra uma ação de auditoria
        
        Args:
            usuario_id: ID do usuário que realizou a ação
            acao: Tipo de ação (CREATE, UPDATE, DELETE, VIEW, LOGIN, etc.)
            entidade: Nome da entidade (Cliente, Projeto, Proposta, etc.)
            escritorio_id: ID do escritório (None para ações administrativas)
            entidade_id: ID da entidade afetada
            descricao: Descrição detalhada da ação
            ip_address: Endereço IP do usuário
            user_agent: User agent do navegador
            dados_anteriores: Dados antes da alteração (para UPDATE)
            dados_novos: Dados após a alteração (para UPDATE)
        
        Returns:
            Auditoria criada
        """
        auditoria = Auditoria(
            usuario_id=usuario_id,
            escritorio_id=escritorio_id,
            acao=acao,
            entidade=entidade,
            entidade_id=entidade_id,
            descricao=descricao,
            ip_address=ip_address,
            user_agent=user_agent,
            dados_anteriores=json.dumps(dados_anteriores, default=str) if dados_anteriores else None,
            dados_novos=json.dumps(dados_novos, default=str) if dados_novos else None
        )
        
        self.db.add(auditoria)
        self.db.commit()
        self.db.refresh(auditoria)
        return auditoria
    
    def registrar_criacao(
        self,
        usuario_id: int,
        entidade: str,
        entidade_id: int,
        escritorio_id: Optional[int] = None,
        descricao: Optional[str] = None,
        dados_novos: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> Auditoria:
        """Registra criação de uma entidade"""
        return self.registrar(
            usuario_id=usuario_id,
            acao="CREATE",
            entidade=entidade,
            entidade_id=entidade_id,
            escritorio_id=escritorio_id,
            descricao=descricao or f"Criado {entidade} #{entidade_id}",
            dados_novos=dados_novos,
            ip_address=ip_address,
            user_agent=user_agent
        )
    
    def registrar_atualizacao(
        self,
        usuario_id: int,
        entidade: str,
        entidade_id: int,
        escritorio_id: Optional[int] = None,
        descricao: Optional[str] = None,
        dados_anteriores: Optional[Dict[str, Any]] = None,
        dados_novos: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> Auditoria:
        """Registra atualização de uma entidade"""
        return self.registrar(
            usuario_id=usuario_id,
            acao="UPDATE",
            entidade=entidade,
            entidade_id=entidade_id,
            escritorio_id=escritorio_id,
            descricao=descricao or f"Atualizado {entidade} #{entidade_id}",
            dados_anteriores=dados_anteriores,
            dados_novos=dados_novos,
            ip_address=ip_address,
            user_agent=user_agent
        )
    
    def registrar_exclusao(
        self,
        usuario_id: int,
        entidade: str,
        entidade_id: int,
        escritorio_id: Optional[int] = None,
        descricao: Optional[str] = None,
        dados_anteriores: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> Auditoria:
        """Registra exclusão de uma entidade"""
        return self.registrar(
            usuario_id=usuario_id,
            acao="DELETE",
            entidade=entidade,
            entidade_id=entidade_id,
            escritorio_id=escritorio_id,
            descricao=descricao or f"Excluído {entidade} #{entidade_id}",
            dados_anteriores=dados_anteriores,
            ip_address=ip_address,
            user_agent=user_agent
        )
    
    def registrar_visualizacao(
        self,
        usuario_id: int,
        entidade: str,
        entidade_id: int,
        escritorio_id: Optional[int] = None,
        descricao: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> Auditoria:
        """Registra visualização de uma entidade"""
        return self.registrar(
            usuario_id=usuario_id,
            acao="VIEW",
            entidade=entidade,
            entidade_id=entidade_id,
            escritorio_id=escritorio_id,
            descricao=descricao or f"Visualizado {entidade} #{entidade_id}",
            ip_address=ip_address,
            user_agent=user_agent
        )
    
    def registrar_login(
        self,
        usuario_id: int,
        escritorio_id: Optional[int] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> Auditoria:
        """Registra login do usuário"""
        return self.registrar(
            usuario_id=usuario_id,
            acao="LOGIN",
            entidade="User",
            entidade_id=usuario_id,
            escritorio_id=escritorio_id,
            descricao=f"Login realizado",
            ip_address=ip_address,
            user_agent=user_agent
        )
    
    def registrar_mudanca_contexto(
        self,
        usuario_id: int,
        escritorio_id: Optional[int] = None,
        perfil: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> Auditoria:
        """Registra mudança de contexto (escritório/perfil)"""
        contexto = f"Escritório #{escritorio_id}" if escritorio_id else "Modo Administrativo"
        if perfil:
            contexto += f" - Perfil: {perfil}"
        
        return self.registrar(
            usuario_id=usuario_id,
            acao="CONTEXT_CHANGE",
            entidade="Context",
            escritorio_id=escritorio_id,
            descricao=f"Mudança de contexto: {contexto}",
            ip_address=ip_address,
            user_agent=user_agent
        )










