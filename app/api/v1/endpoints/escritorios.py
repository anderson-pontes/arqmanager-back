from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.escritorio import EscritorioService
from app.repositories.user import EscritorioRepository, UserRepository
from app.schemas.user import (
    EscritorioCreate, 
    EscritorioResponse, 
    EscritorioUpdate,
    UserCreate, 
    UserResponse
)
from app.api.deps import require_system_admin, get_current_user, require_escritorio_access, require_escritorio_edit_access
from typing import Dict, List, Optional

router = APIRouter()


@router.get("/", response_model=List[EscritorioResponse])
def list_escritorios(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    ativo: Optional[bool] = None,
    current_user: dict = Depends(require_system_admin),
    db: Session = Depends(get_db)
):
    """Lista todos os escritórios (apenas admin do sistema)"""
    repo = EscritorioRepository(db)
    escritorios = repo.get_all(skip=skip, limit=limit, ativo=ativo)
    return [EscritorioResponse.from_orm(e) for e in escritorios]


@router.get("/{escritorio_id}", response_model=EscritorioResponse)
def get_escritorio(
    escritorio_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Busca escritório por ID
    Permite acesso se:
    - É admin do sistema (pode ver qualquer escritório)
    - É admin do escritório (pode ver apenas o próprio escritório)
    """
    # Verificar permissões
    require_escritorio_access(escritorio_id, current_user, db)
    
    service = EscritorioService(db)
    escritorio = service.get_by_id(escritorio_id)
    return EscritorioResponse.from_orm(escritorio)


@router.post("/", response_model=Dict)
def create_escritorio_with_admin(
    escritorio_data: EscritorioCreate,
    admin_data: UserCreate,
    current_user: dict = Depends(require_system_admin),
    db: Session = Depends(get_db)
):
    """
    Cria um novo escritório e automaticamente cria um administrador do escritório
    Apenas administradores do sistema podem criar escritórios
    """
    service = EscritorioService(db)
    result = service.create_with_admin(escritorio_data, admin_data)
    
    return {
        "escritorio": EscritorioResponse.from_orm(result["escritorio"]),
        "admin": {
            "id": result["admin"].id,
            "nome": result["admin"].nome,
            "email": result["admin"].email
        }
    }


@router.put("/{escritorio_id}", response_model=EscritorioResponse)
def update_escritorio(
    escritorio_id: int,
    escritorio_data: EscritorioUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Atualiza um escritório
    Permite acesso se:
    - É admin do sistema (pode editar qualquer escritório)
    - É admin do escritório (pode editar apenas o próprio escritório)
    """
    # Verificar permissões de edição
    require_escritorio_edit_access(escritorio_id, current_user, db)
    
    repo = EscritorioRepository(db)
    escritorio = repo.get_by_id(escritorio_id)
    
    if not escritorio:
        raise HTTPException(status_code=404, detail="Escritório não encontrado")
    
    # Se não é admin do sistema, restringir alguns campos
    is_system_admin = current_user.get("is_system_admin", False)
    if not is_system_admin:
        # Admin do escritório não pode alterar alguns campos
        restricted_fields = ['documento', 'cpf', 'ativo']
        update_data = escritorio_data.dict(exclude_unset=True)
        for field in restricted_fields:
            if field in update_data:
                del update_data[field]
    else:
        update_data = escritorio_data.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(escritorio, field, value)
    
    db.commit()
    db.refresh(escritorio)
    
    return EscritorioResponse.from_orm(escritorio)


@router.patch("/{escritorio_id}/toggle-active", response_model=EscritorioResponse)
def toggle_escritorio_active(
    escritorio_id: int,
    current_user: dict = Depends(require_system_admin),
    db: Session = Depends(get_db)
):
    """
    Ativa ou desativa um escritório (toggle)
    Quando desativa, também desativa todos os usuários vinculados ao escritório
    Quando ativa, reativa os usuários vinculados (mas não os que foram desativados manualmente)
    Apenas admin do sistema pode ativar/desativar escritórios
    """
    from sqlalchemy import text
    from app.models.user import User, user_escritorio
    
    repo = EscritorioRepository(db)
    escritorio = repo.get_by_id(escritorio_id)
    
    if not escritorio:
        raise HTTPException(status_code=404, detail="Escritório não encontrado")
    
    novo_status = not escritorio.ativo
    escritorio.ativo = novo_status
    
    # Se estiver desativando, desativar todos os usuários vinculados
    if not novo_status:
        # Buscar todos os usuários vinculados ao escritório
        usuarios_vinculados = (
            db.query(User)
            .join(user_escritorio, User.id == user_escritorio.c.colaborador_id)
            .filter(
                user_escritorio.c.escritorio_id == escritorio_id,
                user_escritorio.c.ativo == True
            )
            .all()
        )
        
        # Desativar usuários que só têm acesso a este escritório
        for usuario in usuarios_vinculados:
            # Verificar se o usuário tem acesso a outros escritórios ativos
            outros_escritorios_count = db.execute(
                text("""
                    SELECT COUNT(*) 
                    FROM colaborador_escritorio 
                    WHERE colaborador_id = :user_id 
                    AND escritorio_id != :escritorio_id 
                    AND ativo = true
                """),
                {"user_id": usuario.id, "escritorio_id": escritorio_id}
            ).scalar()
            
            # Se não tiver outros escritórios ativos, desativar o usuário
            if outros_escritorios_count == 0 and not usuario.is_system_admin:
                usuario.ativo = False
        
        # Desativar o vínculo na tabela de associação
        db.execute(
            text("""
                UPDATE colaborador_escritorio 
                SET ativo = false 
                WHERE escritorio_id = :escritorio_id AND ativo = true
            """),
            {"escritorio_id": escritorio_id}
        )
    
    db.commit()
    db.refresh(escritorio)
    
    return EscritorioResponse.from_orm(escritorio)


@router.delete("/{escritorio_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_escritorio(
    escritorio_id: int,
    current_user: dict = Depends(require_system_admin),
    db: Session = Depends(get_db)
):
    """
    Remove um escritório permanentemente (hard delete)
    Apenas admin do sistema pode remover escritórios permanentemente
    """
    repo = EscritorioRepository(db)
    
    if not repo.delete(escritorio_id, permanent=True):
        raise HTTPException(status_code=404, detail="Escritório não encontrado")
    
    return None


@router.post("/{escritorio_id}/logo", response_model=EscritorioResponse)
async def upload_escritorio_logo(
    escritorio_id: int,
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Faz upload de logo do escritório
    Permite acesso se:
    - É admin do sistema (pode fazer upload em qualquer escritório)
    - É admin do escritório (pode fazer upload apenas no próprio escritório)
    """
    # Verificar permissões de edição
    require_escritorio_edit_access(escritorio_id, current_user, db)
    from app.utils.upload import save_upload_file, delete_upload_file
    
    try:
        # Verificar se escritório existe
        repo = EscritorioRepository(db)
        escritorio = repo.get_by_id(escritorio_id)
        
        if not escritorio:
            raise HTTPException(status_code=404, detail="Escritório não encontrado")
        
        # Salvar arquivo
        file_path = save_upload_file(file, subdirectory="escritorios")
        
        # Deletar logo antiga se existir
        if hasattr(escritorio, 'logo') and escritorio.logo:
            try:
                delete_upload_file(escritorio.logo)
            except Exception:
                pass  # Ignorar erros ao deletar logo antiga
        
        # Atualizar logo no banco
        escritorio.logo = file_path
        
        db.commit()
        db.refresh(escritorio)
        
        return EscritorioResponse.from_orm(escritorio)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao fazer upload da logo: {str(e)}"
        )


@router.delete("/{escritorio_id}/logo", response_model=EscritorioResponse)
def delete_escritorio_logo(
    escritorio_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Remove a logo do escritório
    Permite acesso se:
    - É admin do sistema (pode remover logo de qualquer escritório)
    - É admin do escritório (pode remover logo apenas do próprio escritório)
    """
    # Verificar permissões de edição
    require_escritorio_edit_access(escritorio_id, current_user, db)
    from app.utils.upload import delete_upload_file
    
    try:
        # Verificar se escritório existe
        repo = EscritorioRepository(db)
        escritorio = repo.get_by_id(escritorio_id)
        
        if not escritorio:
            raise HTTPException(status_code=404, detail="Escritório não encontrado")
        
        # Deletar logo se existir
        if escritorio.logo:
            try:
                delete_upload_file(escritorio.logo)
            except Exception:
                pass  # Ignorar erros ao deletar
        
        # Remover logo do banco
        escritorio.logo = None
        
        db.commit()
        db.refresh(escritorio)
        
        return EscritorioResponse.from_orm(escritorio)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao remover logo: {str(e)}"
        )

