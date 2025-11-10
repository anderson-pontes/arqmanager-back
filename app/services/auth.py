from datetime import timedelta
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.repositories.user import UserRepository, EscritorioRepository
from app.schemas.user import (
    UserLogin, UserWithToken, UserResponse, 
    EscritorioContextInfo, SetContextRequest
)
from app.core.security import verify_password, create_access_token, create_refresh_token, decode_token
from app.core.exceptions import UnauthorizedException, NotFoundException
from typing import Optional, List


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        self.escritorio_repo = EscritorioRepository(db)
    
    def login(self, credentials: UserLogin) -> UserWithToken:
        """
        Autentica usuário e retorna tokens
        """
        # Buscar usuário por email
        user = self.user_repo.get_by_email(credentials.email)
        
        if not user:
            raise UnauthorizedException("Email ou senha incorretos")
        
        # Verificar se usuário está ativo
        if not user.ativo:
            raise UnauthorizedException("Usuário inativo")
        
        # Verificar senha
        if not verify_password(credentials.senha, user.senha):
            raise UnauthorizedException("Email ou senha incorretos")
        
        # Verificar se é admin do sistema
        is_system_admin = user.perfil == "Admin" and (user.is_system_admin or False)
        
        # Preparar lista de escritórios disponíveis
        available_escritorios: List[EscritorioContextInfo] = []
        requires_selection = False
        
        if is_system_admin:
            # Admin do sistema: buscar TODOS os escritórios ativos
            all_escritorios = self.escritorio_repo.get_all(limit=1000)
            available_escritorios = [
                EscritorioContextInfo(
                    id=e.id,
                    nome_fantasia=e.nome_fantasia,
                    razao_social=e.razao_social,
                    cor=e.cor or "#6366f1",
                    perfil=None  # Admin escolhe o perfil
                )
                for e in all_escritorios if e.ativo
            ]
            requires_selection = True  # Admin sempre precisa selecionar
        else:
            # Usuário comum: apenas seus escritórios
            for escritorio in user.escritorios:
                if not escritorio.ativo:
                    continue
                    
                perfil = self._get_user_perfil_in_escritorio(user.id, escritorio.id)
                available_escritorios.append(
                    EscritorioContextInfo(
                        id=escritorio.id,
                        nome_fantasia=escritorio.nome_fantasia,
                        razao_social=escritorio.razao_social,
                        cor=escritorio.cor or "#6366f1",
                        perfil=perfil
                    )
                )
            
            requires_selection = len(available_escritorios) > 1
        
        # Criar tokens (sem contexto ainda, será definido depois)
        access_token = create_access_token(data={
            "sub": str(user.id), 
            "email": user.email,
            "is_system_admin": is_system_admin
        })
        refresh_token = create_refresh_token(data={
            "sub": str(user.id), 
            "email": user.email
        })
        
        return UserWithToken(
            user=UserResponse.from_orm(user),
            access_token=access_token,
            refresh_token=refresh_token,
            requires_escritorio_selection=requires_selection,
            is_system_admin=is_system_admin,
            available_escritorios=available_escritorios
        )
    
    def set_context(self, user_id: int, escritorio_id: Optional[int] = None, perfil: Optional[str] = None) -> dict:
        """
        Define o contexto de escritório e perfil para o usuário
        Gera novo token com contexto incluído
        
        Se escritorio_id for None, define contexto de área administrativa (apenas para admin do sistema)
        """
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("Usuário não encontrado")
        
        if not user.ativo:
            raise UnauthorizedException("Usuário inativo")
        
        # Verificar se é admin do sistema
        is_system_admin = user.perfil == "Admin" and (user.is_system_admin or False)
        
        # Se não tem escritório_id, é modo administrativo
        is_admin_mode = escritorio_id is None
        
        if is_admin_mode:
            # Apenas admin do sistema pode acessar área administrativa
            if not is_system_admin:
                raise UnauthorizedException("Apenas administradores do sistema podem acessar a área administrativa")
        elif is_system_admin:
            # Admin pode acessar qualquer escritório
            escritorio = self.escritorio_repo.get_by_id(escritorio_id)
            if not escritorio:
                raise NotFoundException("Escritório não encontrado")
            if not escritorio.ativo:
                raise UnauthorizedException("Escritório inativo")
        else:
            # Usuário comum: verificar se tem acesso ao escritório
            user_escritorios = [e.id for e in user.escritorios if e.ativo]
            if escritorio_id not in user_escritorios:
                raise UnauthorizedException("Usuário não tem acesso a este escritório")
            
            # Buscar perfil real do usuário neste escritório
            perfil_real = self._get_user_perfil_in_escritorio(user_id, escritorio_id)
            if perfil_real:
                perfil = perfil_real  # Usar perfil real, não o escolhido
        
        # Criar novo token com contexto
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "is_system_admin": is_system_admin,
            "is_admin_mode": is_admin_mode  # Flag para indicar modo administrativo
        }
        
        # Adicionar contexto de escritório apenas se não for modo admin
        if not is_admin_mode:
            token_data["escritorio_id"] = escritorio_id
            token_data["perfil"] = perfil
        
        access_token = create_access_token(data=token_data)
        
        return {
            "access_token": access_token,
            "escritorio_id": escritorio_id,
            "perfil": perfil,
            "is_admin_mode": is_admin_mode
        }
    
    def get_available_escritorios(self, user_id: int) -> List[EscritorioContextInfo]:
        """
        Retorna lista de escritórios disponíveis para o usuário
        """
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("Usuário não encontrado")
        
        is_system_admin = user.perfil == "Admin" and (user.is_system_admin or False)
        
        if is_system_admin:
            # Admin: todos os escritórios
            escritorios = self.escritorio_repo.get_all(limit=1000)
            return [
                EscritorioContextInfo(
                    id=e.id,
                    nome_fantasia=e.nome_fantasia,
                    razao_social=e.razao_social,
                    cor=e.cor or "#6366f1",
                    perfil=None
                )
                for e in escritorios if e.ativo
            ]
        else:
            # Usuário comum: apenas seus escritórios
            result = []
            for escritorio in user.escritorios:
                if not escritorio.ativo:
                    continue
                perfil = self._get_user_perfil_in_escritorio(user.id, escritorio.id)
                result.append(
                    EscritorioContextInfo(
                        id=escritorio.id,
                        nome_fantasia=escritorio.nome_fantasia,
                        razao_social=escritorio.razao_social,
                        cor=escritorio.cor or "#6366f1",
                        perfil=perfil
                    )
                )
            return result
    
    def _get_user_perfil_in_escritorio(self, user_id: int, escritorio_id: int) -> Optional[str]:
        """Busca o perfil do usuário em um escritório específico"""
        result = self.db.execute(
            text("""
                SELECT perfil FROM colaborador_escritorio 
                WHERE colaborador_id = :user_id AND escritorio_id = :escritorio_id AND ativo = true
            """),
            {"user_id": user_id, "escritorio_id": escritorio_id}
        ).first()
        return result[0] if result else None
    
    def refresh_token(self, refresh_token: str) -> dict:
        """
        Gera novo access token a partir do refresh token
        Mantém o contexto se existir
        """
        payload = decode_token(refresh_token)
        
        if not payload:
            raise UnauthorizedException("Token inválido ou expirado")
        
        if payload.get("type") != "refresh":
            raise UnauthorizedException("Tipo de token inválido")
        
        user_id = payload.get("sub")
        email = payload.get("email")
        
        # Verificar se usuário ainda existe e está ativo
        user = self.user_repo.get_by_id(user_id)
        if not user or not user.ativo:
            raise UnauthorizedException("Usuário não encontrado ou inativo")
        
        # Criar novo access token (sem contexto, será definido novamente)
        new_access_token = create_access_token(data={
            "sub": str(user_id), 
            "email": email,
            "is_system_admin": user.perfil == "Admin" and (user.is_system_admin or False)
        })
        
        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }
    
    def get_current_user(self, user_id: int) -> UserResponse:
        """
        Retorna dados do usuário atual
        """
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("Usuário não encontrado")
        
        return UserResponse.from_orm(user)
