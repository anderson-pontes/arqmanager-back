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
    Dependency para obter usuário atual autenticado com contexto
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
    
    # Extrair contexto do token
    escritorio_id = payload.get("escritorio_id")
    perfil_contexto = payload.get("perfil")
    is_system_admin = payload.get("is_system_admin", False)
    is_admin_mode = payload.get("is_admin_mode", False)  # Modo administrativo
    
    return {
        "id": user.id,
        "email": user.email,
        "nome": user.nome,
        "perfil": user.perfil,
        "escritorio_id": escritorio_id,
        "perfil_contexto": perfil_contexto,  # Perfil no escritório selecionado
        "is_system_admin": is_system_admin,
        "is_admin_mode": is_admin_mode  # Modo administrativo (sem escritório)
    }


def get_current_active_user(
    current_user: dict = Depends(get_current_user)
):
    """
    Dependency para verificar se usuário está ativo
    """
    return current_user


def get_current_escritorio(
    current_user: dict = Depends(get_current_user)
) -> int:
    """
    Dependency para obter escritório atual do contexto
    Retorna o ID do escritório selecionado
    Não permite acesso em modo administrativo
    """
    # Se estiver em modo administrativo, não tem escritório
    if current_user.get("is_admin_mode"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Esta operação requer um escritório selecionado. Saia do modo administrativo primeiro."
        )
    
    escritorio_id = current_user.get("escritorio_id")
    if not escritorio_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Escritório não selecionado. Selecione um escritório primeiro."
        )
    return escritorio_id


def require_system_admin(
    current_user: dict = Depends(get_current_user)
):
    """
    Dependency para verificar se usuário é admin do sistema
    Permite acesso mesmo se não estiver em modo administrativo (is_admin_mode)
    pois a área administrativa pode ser acessada de qualquer contexto
    """
    if not current_user.get("is_system_admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Apenas administradores do sistema podem acessar este recurso."
        )
    return current_user


def require_escritorio_access(
    escritorio_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Dependency para verificar se usuário tem acesso a um escritório (visualização)
    Permite acesso se:
    - É admin do sistema (pode acessar qualquer escritório)
    - Está tentando acessar o próprio escritório do contexto (qualquer usuário vinculado)
    """
    from app.models.user import User, ColaboradorEscritorioPerfil
    from sqlalchemy import text
    
    # Admin do sistema pode acessar qualquer escritório
    if current_user.get("is_system_admin"):
        return current_user
    
    # Verificar se é admin do escritório
    user_id = current_user.get("id")
    escritorio_context_id = current_user.get("escritorio_id")
    
    # Se está tentando acessar o escritório do contexto atual, permitir acesso
    # (se o usuário tem esse escritório no contexto, significa que ele tem acesso)
    if escritorio_context_id == escritorio_id:
        return current_user
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Acesso negado. Você não tem permissão para acessar este escritório."
    )


def require_escritorio_edit_access(
    escritorio_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Dependency para verificar se usuário pode editar um escritório
    Permite acesso se:
    - É admin do sistema (pode editar qualquer escritório)
    - É admin do escritório e está tentando editar o próprio escritório
    """
    from app.models.user import User, ColaboradorEscritorioPerfil
    from sqlalchemy import text
    
    # Admin do sistema pode editar qualquer escritório
    if current_user.get("is_system_admin"):
        return current_user
    
    # Verificar se é admin do escritório
    user_id = current_user.get("id")
    escritorio_context_id = current_user.get("escritorio_id")
    
    # Se está tentando editar o escritório do contexto atual
    if escritorio_context_id == escritorio_id:
        # Verificar se é admin do escritório
        perfil_contexto = current_user.get("perfil_contexto")
        if perfil_contexto in ["Admin", "Administrador"]:
            return current_user
        
        # Verificar na tabela de perfis
        perfil_result = db.execute(
            text("""
                SELECT perfil, ativo
                FROM colaborador_escritorio_perfil
                WHERE colaborador_id = :user_id
                AND escritorio_id = :escritorio_id
                AND ativo = true
            """),
            {"user_id": user_id, "escritorio_id": escritorio_id}
        ).first()
        
        if perfil_result and perfil_result[0] in ["Admin", "Administrador"]:
            return current_user
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Acesso negado. Apenas administradores podem editar este escritório."
    )
