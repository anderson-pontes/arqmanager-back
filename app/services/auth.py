from datetime import timedelta
from sqlalchemy.orm import Session
from app.repositories.user import UserRepository
from app.schemas.user import UserLogin, UserWithToken, UserResponse
from app.core.security import verify_password, create_access_token, create_refresh_token, decode_token
from app.core.exceptions import UnauthorizedException, NotFoundException
from typing import Optional


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
    
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
        
        # Criar tokens
        access_token = create_access_token(data={"sub": user.id, "email": user.email})
        refresh_token = create_refresh_token(data={"sub": user.id, "email": user.email})
        
        # Verificar se precisa selecionar escritório
        requires_selection = len(user.escritorios) > 1
        
        return UserWithToken(
            user=UserResponse.from_orm(user),
            access_token=access_token,
            refresh_token=refresh_token,
            requires_escritorio_selection=requires_selection
        )
    
    def refresh_token(self, refresh_token: str) -> dict:
        """
        Gera novo access token a partir do refresh token
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
        
        # Criar novo access token
        new_access_token = create_access_token(data={"sub": user_id, "email": email})
        
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
