"""
Endpoints de Colaboradores
Alias para /users para manter compatibilidade com frontend
"""
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
from app.database import get_db
from app.services.user import UserService
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.api.deps import get_current_user, get_current_escritorio
from app.core.exceptions import ConflictException

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
def list_colaboradores(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    ativo: Optional[bool] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """
    Lista todos os colaboradores do escritório atual
    
    Filtros:
    - ativo: Filtrar por status (True/False)
    - search: Buscar por nome, email ou CPF
    """
    service = UserService(db)
    return service.get_all(escritorio_id=escritorio_id, skip=skip, limit=limit, ativo=ativo, search=search)


@router.post("/", response_model=UserResponse, status_code=201)
def create_colaborador(
    colaborador: UserCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """
    Cria um novo colaborador e vincula ao escritório atual
    """
    service = UserService(db)
    
    # Criar usuário (o service já valida email e CPF)
    try:
        new_user_response = service.create(colaborador)
    except ConflictException as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
    # Buscar o usuário criado do banco para obter o ID
    user_repo = UserRepository(db)
    new_user = user_repo.get_by_id(new_user_response.id)
    
    if not new_user:
        raise HTTPException(
            status_code=500,
            detail="Erro ao criar colaborador"
        )
    
    # Verificar se o usuário já está vinculado ao escritório
    existing_link = db.execute(
        text("""
            SELECT COUNT(*) 
            FROM colaborador_escritorio 
            WHERE colaborador_id = :user_id 
            AND escritorio_id = :escritorio_id
        """),
        {"user_id": new_user.id, "escritorio_id": escritorio_id}
    ).scalar()
    
    # Se não estiver vinculado, criar o vínculo
    if existing_link == 0:
        # Usar o perfil do colaborador ou padrão "Produção"
        # Converter enum para string se necessário
        perfil_value = colaborador.perfil
        if hasattr(perfil_value, 'value'):
            perfil = perfil_value.value
        else:
            perfil = str(perfil_value) if perfil_value else "Produção"
        
        db.execute(
            text("""
                INSERT INTO colaborador_escritorio (colaborador_id, escritorio_id, perfil, ativo)
                VALUES (:user_id, :escritorio_id, :perfil, true)
            """),
            {"user_id": new_user.id, "escritorio_id": escritorio_id, "perfil": perfil}
        )
        db.commit()
        db.refresh(new_user)
    
    return new_user_response


@router.get("/{colaborador_id}", response_model=UserResponse)
def get_colaborador(
    colaborador_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """
    Busca um colaborador por ID, garantindo que pertence ao escritório atual
    """
    user_repo = UserRepository(db)
    
    # Verificar se o colaborador está vinculado ao escritório
    vinculado = db.execute(
        text("""
            SELECT COUNT(*) 
            FROM colaborador_escritorio 
            WHERE colaborador_id = :user_id 
            AND escritorio_id = :escritorio_id
        """),
        {"user_id": colaborador_id, "escritorio_id": escritorio_id}
    ).scalar()
    
    if vinculado == 0:
        raise HTTPException(
            status_code=404,
            detail="Colaborador não encontrado neste escritório"
        )
    
    service = UserService(db)
    return service.get_by_id(colaborador_id)


@router.put("/{colaborador_id}", response_model=UserResponse)
def update_colaborador(
    colaborador_id: int,
    colaborador: UserUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """
    Atualiza um colaborador, garantindo que pertence ao escritório atual
    """
    # Verificar se o colaborador está vinculado ao escritório
    vinculado = db.execute(
        text("""
            SELECT COUNT(*) 
            FROM colaborador_escritorio 
            WHERE colaborador_id = :user_id 
            AND escritorio_id = :escritorio_id
        """),
        {"user_id": colaborador_id, "escritorio_id": escritorio_id}
    ).scalar()
    
    if vinculado == 0:
        raise HTTPException(
            status_code=404,
            detail="Colaborador não encontrado neste escritório"
        )
    
    service = UserService(db)
    return service.update(colaborador_id, colaborador)


@router.delete("/{colaborador_id}", status_code=204)
def delete_colaborador(
    colaborador_id: int,
    permanent: bool = Query(False, description="Se True, remove permanentemente. Se False, soft delete (marca como inativo)"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """
    Remove um colaborador do escritório atual
    
    Parâmetros:
    - permanent: False = Remove apenas o vínculo com o escritório (ou soft delete se não tiver outros escritórios)
    - permanent: True = Hard delete (remove do banco permanentemente)
    """
    # Verificar se o colaborador está vinculado ao escritório
    vinculado = db.execute(
        text("""
            SELECT COUNT(*) 
            FROM colaborador_escritorio 
            WHERE colaborador_id = :user_id 
            AND escritorio_id = :escritorio_id
        """),
        {"user_id": colaborador_id, "escritorio_id": escritorio_id}
    ).scalar()
    
    if vinculado == 0:
        raise HTTPException(
            status_code=404,
            detail="Colaborador não encontrado neste escritório"
        )
    
    if permanent:
        # Hard delete - remover completamente
        service = UserService(db)
        service.delete(colaborador_id, permanent=permanent)
    else:
        # Soft delete - remover apenas o vínculo com o escritório
        db.execute(
            text("""
                DELETE FROM colaborador_escritorio 
                WHERE colaborador_id = :user_id 
                AND escritorio_id = :escritorio_id
            """),
            {"user_id": colaborador_id, "escritorio_id": escritorio_id}
        )
        
        # Verificar se o usuário tem outros escritórios
        outros_escritorios = db.execute(
            text("""
                SELECT COUNT(*) 
                FROM colaborador_escritorio 
                WHERE colaborador_id = :user_id
            """),
            {"user_id": colaborador_id}
        ).scalar()
        
        # Se não tiver outros escritórios e não for admin do sistema, desativar o usuário
        if outros_escritorios == 0:
            user_repo = UserRepository(db)
            user = user_repo.get_by_id(colaborador_id)
            if user and not user.is_system_admin:
                user.ativo = False
                db.commit()
        
        db.commit()


@router.get("/stats/count")
def count_colaboradores(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """
    Retorna total de colaboradores cadastrados no escritório atual
    """
    service = UserService(db)
    return {"total": service.count(escritorio_id=escritorio_id)}

