"""
Endpoints administrativos - apenas para admin do sistema
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app.repositories.user import UserRepository, EscritorioRepository
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.api.deps import require_system_admin
from app.core.security import get_password_hash
from app.models.user import User, user_escritorio
from typing import List, Optional

router = APIRouter()


@router.post("/system-admin", response_model=UserResponse)
def create_system_admin(
    user_data: UserCreate,
    current_user: dict = Depends(require_system_admin),
    db: Session = Depends(get_db)
):
    """
    Cria um novo administrador do sistema
    Apenas administradores do sistema podem criar outros admins
    """
    user_repo = UserRepository(db)
    
    # Verificar se email já existe
    existing_user = user_repo.get_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email já está cadastrado"
        )
    
    # Verificar se CPF já existe (apenas se fornecido)
    if user_data.cpf and user_data.cpf.strip():
        existing_cpf = user_repo.get_by_cpf(user_data.cpf)
        if existing_cpf:
            raise HTTPException(
                status_code=400,
                detail="CPF já está cadastrado"
            )
    
    # Garantir que é admin do sistema
    user_data.perfil = "Admin"
    user_data.is_system_admin = True
    
    # Criar usuário
    new_user = user_repo.create(user_data)
    
    return UserResponse.from_orm(new_user)


@router.post("/escritorio-admin/{escritorio_id}", response_model=UserResponse)
def create_escritorio_admin(
    escritorio_id: int,
    user_data: UserCreate,
    current_user: dict = Depends(require_system_admin),
    db: Session = Depends(get_db)
):
    """
    Cria um novo administrador para um escritório específico
    Apenas administradores do sistema podem criar admins de escritório
    """
    user_repo = UserRepository(db)
    escritorio_repo = EscritorioRepository(db)
    
    # Verificar se escritório existe
    escritorio = escritorio_repo.get_by_id(escritorio_id)
    if not escritorio:
        raise HTTPException(
            status_code=404,
            detail="Escritório não encontrado"
        )
    
    if not escritorio.ativo:
        raise HTTPException(
            status_code=400,
            detail="Escritório está inativo"
        )
    
    # Verificar se email já existe
    existing_user = user_repo.get_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email já está cadastrado"
        )
    
    # Verificar se CPF já existe (apenas se fornecido)
    if user_data.cpf and user_data.cpf.strip():
        existing_cpf = user_repo.get_by_cpf(user_data.cpf)
        if existing_cpf:
            raise HTTPException(
                status_code=400,
                detail="CPF já está cadastrado"
            )
    
    # Garantir que é admin do escritório (não do sistema)
    user_data.perfil = "Admin"
    user_data.is_system_admin = False
    
    # Criar usuário
    new_user = user_repo.create(user_data)
    
    # Vincular ao escritório
    db.execute(
        text("""
            INSERT INTO colaborador_escritorio (colaborador_id, escritorio_id, perfil, ativo)
            VALUES (:user_id, :escritorio_id, 'Admin', true)
        """),
        {"user_id": new_user.id, "escritorio_id": escritorio_id}
    )
    
    db.commit()
    db.refresh(new_user)
    
    return UserResponse.from_orm(new_user)


@router.get("/system-admins", response_model=List[UserResponse])
def list_system_admins(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: dict = Depends(require_system_admin),
    db: Session = Depends(get_db)
):
    """Lista todos os administradores do sistema"""
    user_repo = UserRepository(db)
    users = user_repo.get_all(skip=skip, limit=limit)
    
    # Filtrar apenas admins do sistema
    system_admins = [
        u for u in users 
        if u.perfil == "Admin" and (u.is_system_admin or False)
    ]
    
    return [UserResponse.from_orm(u) for u in system_admins]


@router.get("/escritorio-admins/{escritorio_id}", response_model=List[UserResponse])
def list_escritorio_admins(
    escritorio_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: dict = Depends(require_system_admin),
    db: Session = Depends(get_db)
):
    """Lista todos os administradores de um escritório"""
    user_repo = UserRepository(db)
    escritorio_repo = EscritorioRepository(db)
    
    # Verificar se escritório existe
    escritorio = escritorio_repo.get_by_id(escritorio_id)
    if not escritorio:
        raise HTTPException(
            status_code=404,
            detail="Escritório não encontrado"
        )
    
    # Buscar admins do escritório usando relacionamento
    admins = (
        db.query(User)
        .join(user_escritorio, User.id == user_escritorio.c.colaborador_id)
        .filter(
            user_escritorio.c.escritorio_id == escritorio_id,
            user_escritorio.c.perfil == 'Admin',
            User.perfil == 'Admin',
            User.is_system_admin == False,
            User.ativo == True,
            user_escritorio.c.ativo == True
        )
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    return [UserResponse.from_orm(u) for u in admins]

