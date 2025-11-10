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


@router.put("/system-admin/{user_id}", response_model=UserResponse)
def update_system_admin(
    user_id: int,
    user_data: UserUpdate,
    current_user: dict = Depends(require_system_admin),
    db: Session = Depends(get_db)
):
    """
    Atualiza um administrador do sistema
    Apenas administradores do sistema podem atualizar outros admins
    """
    user_repo = UserRepository(db)
    
    # Verificar se usuário existe e é admin do sistema
    existing_user = user_repo.get_by_id(user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="Administrador não encontrado")
    
    if not (existing_user.perfil == "Admin" and existing_user.is_system_admin):
        raise HTTPException(
            status_code=400,
            detail="Usuário não é um administrador do sistema"
        )
    
    # Verificar se email já existe (se foi alterado)
    if user_data.email and user_data.email != existing_user.email:
        email_user = user_repo.get_by_email(user_data.email)
        if email_user:
            raise HTTPException(
                status_code=400,
                detail="Email já está cadastrado"
            )
    
    # Verificar se CPF já existe (se foi alterado e fornecido)
    if user_data.cpf and user_data.cpf.strip() and user_data.cpf != existing_user.cpf:
        cpf_user = user_repo.get_by_cpf(user_data.cpf)
        if cpf_user:
            raise HTTPException(
                status_code=400,
                detail="CPF já está cadastrado"
            )
    
    # Garantir que continua sendo admin do sistema
    update_data = user_data.dict(exclude_unset=True)
    update_data['perfil'] = "Admin"
    update_data['is_system_admin'] = True
    
    updated_user = user_repo.update(user_id, UserUpdate(**update_data))
    
    if not updated_user:
        raise HTTPException(status_code=404, detail="Administrador não encontrado")
    
    return UserResponse.from_orm(updated_user)


@router.patch("/system-admin/{user_id}/toggle-active", response_model=UserResponse)
def toggle_system_admin_active(
    user_id: int,
    current_user: dict = Depends(require_system_admin),
    db: Session = Depends(get_db)
):
    """
    Ativa ou desativa um administrador do sistema (toggle)
    Apenas administradores do sistema podem ativar/desativar outros admins
    """
    user_repo = UserRepository(db)
    
    # Verificar se usuário existe e é admin do sistema
    existing_user = user_repo.get_by_id(user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="Administrador não encontrado")
    
    if not (existing_user.perfil == "Admin" and existing_user.is_system_admin):
        raise HTTPException(
            status_code=400,
            detail="Usuário não é um administrador do sistema"
        )
    
    # Não permitir desativar a si mesmo
    if user_id == current_user.get("id"):
        raise HTTPException(
            status_code=400,
            detail="Você não pode desativar a si mesmo"
        )
    
    existing_user.ativo = not existing_user.ativo
    db.commit()
    db.refresh(existing_user)
    
    return UserResponse.from_orm(existing_user)


@router.delete("/system-admin/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_system_admin(
    user_id: int,
    current_user: dict = Depends(require_system_admin),
    db: Session = Depends(get_db)
):
    """
    Remove um administrador do sistema permanentemente (hard delete)
    Apenas administradores do sistema podem remover outros admins permanentemente
    """
    user_repo = UserRepository(db)
    
    # Verificar se usuário existe e é admin do sistema
    existing_user = user_repo.get_by_id(user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="Administrador não encontrado")
    
    if not (existing_user.perfil == "Admin" and existing_user.is_system_admin):
        raise HTTPException(
            status_code=400,
            detail="Usuário não é um administrador do sistema"
        )
    
    # Não permitir deletar a si mesmo
    if user_id == current_user.get("id"):
        raise HTTPException(
            status_code=400,
            detail="Você não pode remover a si mesmo"
        )
    
    if not user_repo.delete(user_id, permanent=True):
        raise HTTPException(status_code=404, detail="Administrador não encontrado")
    
    return None


@router.put("/escritorio-admin/{escritorio_id}/{user_id}", response_model=UserResponse)
def update_escritorio_admin(
    escritorio_id: int,
    user_id: int,
    user_data: UserUpdate,
    current_user: dict = Depends(require_system_admin),
    db: Session = Depends(get_db)
):
    """
    Atualiza um administrador de escritório
    Apenas administradores do sistema podem atualizar admins de escritório
    """
    user_repo = UserRepository(db)
    escritorio_repo = EscritorioRepository(db)
    
    # Verificar se escritório existe
    escritorio = escritorio_repo.get_by_id(escritorio_id)
    if not escritorio:
        raise HTTPException(status_code=404, detail="Escritório não encontrado")
    
    # Verificar se usuário existe e é admin do escritório
    existing_user = user_repo.get_by_id(user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="Administrador não encontrado")
    
    # Verificar se é admin do escritório (não do sistema)
    if existing_user.is_system_admin:
        raise HTTPException(
            status_code=400,
            detail="Este usuário é um administrador do sistema, não de escritório"
        )
    
    # Verificar se está vinculado ao escritório
    user_escritorios = [e.id for e in existing_user.escritorios if e.ativo]
    if escritorio_id not in user_escritorios:
        raise HTTPException(
            status_code=400,
            detail="Usuário não está vinculado a este escritório"
        )
    
    # Verificar se email já existe (se foi alterado)
    if user_data.email and user_data.email != existing_user.email:
        email_user = user_repo.get_by_email(user_data.email)
        if email_user:
            raise HTTPException(
                status_code=400,
                detail="Email já está cadastrado"
            )
    
    # Verificar se CPF já existe (se foi alterado e fornecido)
    if user_data.cpf and user_data.cpf.strip() and user_data.cpf != existing_user.cpf:
        cpf_user = user_repo.get_by_cpf(user_data.cpf)
        if cpf_user:
            raise HTTPException(
                status_code=400,
                detail="CPF já está cadastrado"
            )
    
    # Garantir que continua sendo admin (não do sistema)
    update_data = user_data.dict(exclude_unset=True)
    update_data['perfil'] = "Admin"
    update_data['is_system_admin'] = False
    
    updated_user = user_repo.update(user_id, UserUpdate(**update_data))
    
    if not updated_user:
        raise HTTPException(status_code=404, detail="Administrador não encontrado")
    
    return UserResponse.from_orm(updated_user)


@router.patch("/escritorio-admin/{escritorio_id}/{user_id}/toggle-active", response_model=UserResponse)
def toggle_escritorio_admin_active(
    escritorio_id: int,
    user_id: int,
    current_user: dict = Depends(require_system_admin),
    db: Session = Depends(get_db)
):
    """
    Ativa ou desativa um administrador de escritório (toggle)
    Apenas administradores do sistema podem ativar/desativar admins de escritório
    """
    user_repo = UserRepository(db)
    escritorio_repo = EscritorioRepository(db)
    
    # Verificar se escritório existe
    escritorio = escritorio_repo.get_by_id(escritorio_id)
    if not escritorio:
        raise HTTPException(status_code=404, detail="Escritório não encontrado")
    
    # Verificar se usuário existe e é admin do escritório
    existing_user = user_repo.get_by_id(user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="Administrador não encontrado")
    
    # Verificar se é admin do escritório (não do sistema)
    if existing_user.is_system_admin:
        raise HTTPException(
            status_code=400,
            detail="Este usuário é um administrador do sistema, não de escritório"
        )
    
    # Verificar se está vinculado ao escritório
    user_escritorios = [e.id for e in existing_user.escritorios if e.ativo]
    if escritorio_id not in user_escritorios:
        raise HTTPException(
            status_code=400,
            detail="Usuário não está vinculado a este escritório"
        )
    
    existing_user.ativo = not existing_user.ativo
    db.commit()
    db.refresh(existing_user)
    
    return UserResponse.from_orm(existing_user)


@router.delete("/escritorio-admin/{escritorio_id}/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_escritorio_admin(
    escritorio_id: int,
    user_id: int,
    current_user: dict = Depends(require_system_admin),
    db: Session = Depends(get_db)
):
    """
    Remove um administrador de escritório permanentemente (hard delete)
    Apenas administradores do sistema podem remover admins de escritório permanentemente
    """
    user_repo = UserRepository(db)
    escritorio_repo = EscritorioRepository(db)
    
    # Verificar se escritório existe
    escritorio = escritorio_repo.get_by_id(escritorio_id)
    if not escritorio:
        raise HTTPException(status_code=404, detail="Escritório não encontrado")
    
    # Verificar se usuário existe e é admin do escritório
    existing_user = user_repo.get_by_id(user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="Administrador não encontrado")
    
    # Verificar se é admin do escritório (não do sistema)
    if existing_user.is_system_admin:
        raise HTTPException(
            status_code=400,
            detail="Este usuário é um administrador do sistema, não de escritório"
        )
    
    # Verificar se está vinculado ao escritório
    user_escritorios = [e.id for e in existing_user.escritorios if e.ativo]
    if escritorio_id not in user_escritorios:
        raise HTTPException(
            status_code=400,
            detail="Usuário não está vinculado a este escritório"
        )
    
    if not user_repo.delete(user_id, permanent=True):
        raise HTTPException(status_code=404, detail="Administrador não encontrado")
    
    return None

