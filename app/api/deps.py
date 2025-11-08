from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import decode_token
from app.core.exceptions import UnauthorizedException

# Security scheme
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Dependency para obter usuário atual autenticado
    """
    from app.models.user import User
    
    token = credentials.credentials
    payload = decode_token(token)
    
    if payload is None:
        raise UnauthorizedException("Token inválido ou expirado")
    
    if payload.get("type") != "access":
        raise UnauthorizedException("Tipo de token inválido")
    
    user_id_str = payload.get("sub")
    if user_id_str is None:
        raise UnauthorizedException("Token inválido")
    
    try:
        user_id = int(user_id_str)
    except (ValueError, TypeError):
        raise UnauthorizedException("Token inválido")
    
    # Buscar usuário no banco
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise UnauthorizedException("Usuário não encontrado")
    
    if not user.ativo:
        raise UnauthorizedException("Usuário inativo")
    
    return {"id": user.id, "email": user.email, "nome": user.nome, "perfil": user.perfil}


def get_current_active_user(
    current_user: dict = Depends(get_current_user)
):
    """
    Dependency para verificar se usuário está ativo
    """
    # TODO: Verificar se usuário está ativo quando implementar o modelo
    # if not current_user.ativo:
    #     raise ForbiddenException("Usuário inativo")
    
    return current_user
