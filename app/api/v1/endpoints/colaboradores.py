"""
Endpoints de Colaboradores
Alias para /users para manter compatibilidade com frontend
"""
from fastapi import APIRouter, Depends, Query, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
from app.database import get_db
from app.services.user import UserService
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate, UserResponse, ColaboradorEscritorioPerfilCreate, ColaboradorEscritorioPerfilResponse
from app.models.user import ColaboradorEscritorioPerfil
from app.api.deps import get_current_user, get_current_escritorio
from app.core.exceptions import ConflictException
from app.utils.upload import save_upload_file, delete_upload_file, get_file_url

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
    colaboradores = service.get_all(escritorio_id=escritorio_id, skip=skip, limit=limit, ativo=ativo, search=search)
    
    # Buscar perfis de cada colaborador
    result = []
    for colaborador in colaboradores:
        try:
            # Buscar perfis do colaborador no escritório atual
            perfis = db.query(ColaboradorEscritorioPerfil).filter(
                ColaboradorEscritorioPerfil.colaborador_id == colaborador.id,
                ColaboradorEscritorioPerfil.escritorio_id == escritorio_id
            ).order_by(ColaboradorEscritorioPerfil.perfil).all()
            
            # Buscar campos do relacionamento colaborador-escritório
            dados_escritorio = db.execute(
                text("""
                    SELECT socio, banco, agencia, tipo_conta, conta, pix_tipo, pix_chave
                    FROM colaborador_escritorio 
                    WHERE colaborador_id = :user_id 
                    AND escritorio_id = :escritorio_id
                """),
                {"user_id": colaborador.id, "escritorio_id": escritorio_id}
            ).first()
            
            socio_value = bool(dados_escritorio[0]) if dados_escritorio and dados_escritorio[0] is not None else False
            banco_value = dados_escritorio[1] if dados_escritorio and len(dados_escritorio) > 1 and dados_escritorio[1] else None
            agencia_value = dados_escritorio[2] if dados_escritorio and len(dados_escritorio) > 2 and dados_escritorio[2] else None
            tipo_conta_value = dados_escritorio[3] if dados_escritorio and len(dados_escritorio) > 3 and dados_escritorio[3] else None
            conta_value = dados_escritorio[4] if dados_escritorio and len(dados_escritorio) > 4 and dados_escritorio[4] else None
            
            # Converter UserResponse para dict
            if hasattr(colaborador, 'model_dump'):
                colaborador_dict = colaborador.model_dump()
            elif hasattr(colaborador, 'dict'):
                colaborador_dict = colaborador.dict()
            else:
                colaborador_dict = {
                    'id': colaborador.id,
                    'nome': colaborador.nome,
                    'email': colaborador.email,
                    'cpf': colaborador.cpf,
                    'telefone': colaborador.telefone,
                    'data_nascimento': colaborador.data_nascimento,
                    'perfil': colaborador.perfil.value if hasattr(colaborador.perfil, 'value') else str(colaborador.perfil),
                    'tipo': colaborador.tipo.value if hasattr(colaborador.tipo, 'value') else str(colaborador.tipo),
                    'ativo': colaborador.ativo,
                    'foto': colaborador.foto,
                    'ultimo_acesso': colaborador.ultimo_acesso,
                    'tipo_pix': colaborador.tipo_pix,
                    'chave_pix': colaborador.chave_pix,
                    'is_system_admin': colaborador.is_system_admin,
                    'created_at': colaborador.created_at,
                    'updated_at': colaborador.updated_at,
                    'escritorios': colaborador.escritorios or []
                }
            
            # Serializar perfis
            perfis_list = []
            for perfil in perfis:
                try:
                    perfis_list.append(ColaboradorEscritorioPerfilResponse.model_validate(perfil, from_attributes=True))
                except Exception as e:
                    # Se falhar, tentar criar manualmente
                    try:
                        from datetime import datetime
                        perfis_list.append(ColaboradorEscritorioPerfilResponse(
                            id=perfil.id,
                            colaborador_id=perfil.colaborador_id,
                            escritorio_id=perfil.escritorio_id,
                            perfil=perfil.perfil,
                            ativo=perfil.ativo,
                            created_at=perfil.created_at if perfil.created_at else datetime.now(),
                            updated_at=perfil.updated_at if perfil.updated_at else datetime.now()
                        ))
                    except:
                        pass
            
            colaborador_dict['perfis'] = perfis_list
            colaborador_dict['socio'] = socio_value
            colaborador_dict['banco'] = banco_value
            colaborador_dict['agencia'] = agencia_value
            colaborador_dict['tipo_conta'] = tipo_conta_value
            colaborador_dict['conta'] = conta_value
            result.append(UserResponse(**colaborador_dict))
        except Exception as e:
            # Se der erro ao buscar perfis, adicionar colaborador sem perfis
            if hasattr(colaborador, 'model_dump'):
                colaborador_dict = colaborador.model_dump()
            elif hasattr(colaborador, 'dict'):
                colaborador_dict = colaborador.dict()
            else:
                colaborador_dict = {
                    'id': colaborador.id,
                    'nome': colaborador.nome,
                    'email': colaborador.email,
                    'cpf': colaborador.cpf,
                    'telefone': colaborador.telefone,
                    'data_nascimento': colaborador.data_nascimento,
                    'perfil': colaborador.perfil.value if hasattr(colaborador.perfil, 'value') else str(colaborador.perfil),
                    'tipo': colaborador.tipo.value if hasattr(colaborador.tipo, 'value') else str(colaborador.tipo),
                    'ativo': colaborador.ativo,
                    'foto': colaborador.foto,
                    'ultimo_acesso': colaborador.ultimo_acesso,
                    'tipo_pix': colaborador.tipo_pix,
                    'chave_pix': colaborador.chave_pix,
                    'is_system_admin': colaborador.is_system_admin,
                    'created_at': colaborador.created_at,
                    'updated_at': colaborador.updated_at,
                    'escritorios': colaborador.escritorios or []
                }
            colaborador_dict['perfis'] = []
            # Buscar dados do relacionamento também no caso de erro
            try:
                dados_escritorio = db.execute(
                    text("""
                        SELECT socio, banco, agencia, tipo_conta, conta, pix_tipo, pix_chave
                        FROM colaborador_escritorio 
                        WHERE colaborador_id = :user_id 
                        AND escritorio_id = :escritorio_id
                    """),
                    {"user_id": colaborador.id, "escritorio_id": escritorio_id}
                ).first()
                
                socio_value = bool(dados_escritorio[0]) if dados_escritorio and dados_escritorio[0] is not None else False
                banco_value = dados_escritorio[1] if dados_escritorio and len(dados_escritorio) > 1 and dados_escritorio[1] else None
                agencia_value = dados_escritorio[2] if dados_escritorio and len(dados_escritorio) > 2 and dados_escritorio[2] else None
                tipo_conta_value = dados_escritorio[3] if dados_escritorio and len(dados_escritorio) > 3 and dados_escritorio[3] else None
                conta_value = dados_escritorio[4] if dados_escritorio and len(dados_escritorio) > 4 and dados_escritorio[4] else None
            except:
                socio_value = False
                banco_value = None
                agencia_value = None
                tipo_conta_value = None
                conta_value = None
            
            colaborador_dict['socio'] = socio_value
            colaborador_dict['banco'] = banco_value
            colaborador_dict['agencia'] = agencia_value
            colaborador_dict['tipo_conta'] = tipo_conta_value
            colaborador_dict['conta'] = conta_value
            result.append(UserResponse(**colaborador_dict))
    
    return result


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
    
    # Criar usuário (o service já valida email e CPF como únicos no sistema)
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
        # Criar vínculo na tabela colaborador_escritorio (compatibilidade)
        perfil_value = colaborador.perfil
        if hasattr(perfil_value, 'value'):
            perfil = perfil_value.value
        else:
            perfil = str(perfil_value) if perfil_value else "Produção"
        
        # Obter valor de socio (padrão False se não fornecido)
        socio_value = getattr(colaborador, 'socio', False) if hasattr(colaborador, 'socio') else False
        
        # Obter dados bancários
        banco_value = getattr(colaborador, 'banco', None) if hasattr(colaborador, 'banco') else None
        agencia_value = getattr(colaborador, 'agencia', None) if hasattr(colaborador, 'agencia') else None
        tipo_conta_value = getattr(colaborador, 'tipo_conta', None) if hasattr(colaborador, 'tipo_conta') else None
        conta_value = getattr(colaborador, 'conta', None) if hasattr(colaborador, 'conta') else None
        
        db.execute(
            text("""
                INSERT INTO colaborador_escritorio 
                (colaborador_id, escritorio_id, perfil, ativo, socio, banco, agencia, tipo_conta, conta, pix_tipo, pix_chave)
                VALUES (:user_id, :escritorio_id, :perfil, true, :socio, :banco, :agencia, :tipo_conta, :conta, :pix_tipo, :pix_chave)
            """),
            {
                "user_id": new_user.id,
                "escritorio_id": escritorio_id,
                "perfil": perfil,
                "socio": socio_value,
                "banco": banco_value,
                "agencia": agencia_value,
                "tipo_conta": tipo_conta_value,
                "conta": conta_value,
                "pix_tipo": colaborador.tipo_pix,
                "pix_chave": colaborador.chave_pix
            }
        )
        db.commit()
    
    # Criar múltiplos perfis se fornecidos
    if colaborador.perfis and len(colaborador.perfis) > 0:
        # Remover perfis existentes para este colaborador-escritório
        db.execute(
            text("""
                DELETE FROM colaborador_escritorio_perfil
                WHERE colaborador_id = :user_id AND escritorio_id = :escritorio_id
            """),
            {"user_id": new_user.id, "escritorio_id": escritorio_id}
        )
        db.commit()  # Commit antes de inserir novos
        
        # Inserir novos perfis
        for perfil in colaborador.perfis:
            try:
                db_perfil = ColaboradorEscritorioPerfil(
                    colaborador_id=new_user.id,
                    escritorio_id=escritorio_id,
                    perfil=perfil,
                    ativo=True
                )
                db.add(db_perfil)
            except Exception as e:
                print(f"Erro ao adicionar perfil {perfil}: {e}")
                # Continuar com os outros perfis
        db.commit()
    else:
        # Se não forneceu perfis, criar pelo menos um perfil padrão na nova tabela
        try:
            db_perfil = ColaboradorEscritorioPerfil(
                colaborador_id=new_user.id,
                escritorio_id=escritorio_id,
                perfil=perfil if 'perfil' in locals() else "Produção",
                ativo=True
            )
            db.add(db_perfil)
            db.commit()
        except Exception as e:
            print(f"Erro ao criar perfil padrão: {e}")
            # Não falhar a criação se der erro no perfil
    
    return new_user_response


@router.get("/{colaborador_id}", response_model=UserResponse)
def get_colaborador(
    colaborador_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """
    Busca um colaborador por ID (do escritório atual)
    """
    import traceback
    try:
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
        
        # Buscar o colaborador
        service = UserService(db)
        colaborador_response = service.get_by_id(colaborador_id)
        
        # Buscar campos do relacionamento colaborador-escritório
        try:
            dados_escritorio = db.execute(
                text("""
                    SELECT socio, banco, agencia, tipo_conta, conta, pix_tipo, pix_chave
                    FROM colaborador_escritorio 
                    WHERE colaborador_id = :user_id 
                    AND escritorio_id = :escritorio_id
                """),
                {"user_id": colaborador_id, "escritorio_id": escritorio_id}
            ).first()
            
            if dados_escritorio:
                # Converter para dict se necessário e adicionar campos
                if hasattr(colaborador_response, 'model_dump'):
                    colaborador_dict = colaborador_response.model_dump()
                elif hasattr(colaborador_response, 'dict'):
                    colaborador_dict = colaborador_response.dict()
                else:
                    colaborador_dict = colaborador_response
                
                colaborador_dict['socio'] = bool(dados_escritorio[0]) if dados_escritorio[0] is not None else False
                colaborador_dict['banco'] = dados_escritorio[1] if len(dados_escritorio) > 1 and dados_escritorio[1] else None
                colaborador_dict['agencia'] = dados_escritorio[2] if len(dados_escritorio) > 2 and dados_escritorio[2] else None
                colaborador_dict['tipo_conta'] = dados_escritorio[3] if len(dados_escritorio) > 3 and dados_escritorio[3] else None
                colaborador_dict['conta'] = dados_escritorio[4] if len(dados_escritorio) > 4 and dados_escritorio[4] else None
                
                # Recriar UserResponse com os campos
                from app.schemas.user import UserResponse
                return UserResponse(**colaborador_dict)
        except Exception as e:
            print(f"Erro ao buscar campos do relacionamento: {e}")
            # Continuar sem os campos se houver erro
        
        return colaborador_response
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erro ao buscar colaborador {colaborador_id}: {e}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar colaborador: {str(e)}"
        )


@router.put("/{colaborador_id}", response_model=UserResponse)
def update_colaborador(
    colaborador_id: int,
    colaborador: UserUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """
    Atualiza um colaborador
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
    
    # Atualizar dados do colaborador
    service = UserService(db)
    updated_user = service.update(colaborador_id, colaborador)
    
    # Atualizar campos específicos do relacionamento colaborador-escritório
    campos_para_atualizar = [
        colaborador.socio is not None,
        colaborador.tipo_pix is not None,
        colaborador.chave_pix is not None,
        colaborador.banco is not None,
        colaborador.agencia is not None,
        colaborador.tipo_conta is not None,
        colaborador.conta is not None,
    ]
    
    if any(campos_para_atualizar):
        update_fields = []
        params = {"user_id": colaborador_id, "escritorio_id": escritorio_id}
        
        if colaborador.socio is not None:
            update_fields.append("socio = :socio")
            params["socio"] = colaborador.socio
        
        if colaborador.tipo_pix is not None:
            update_fields.append("pix_tipo = :pix_tipo")
            params["pix_tipo"] = colaborador.tipo_pix
        
        if colaborador.chave_pix is not None:
            update_fields.append("pix_chave = :pix_chave")
            params["pix_chave"] = colaborador.chave_pix
        
        if colaborador.banco is not None:
            update_fields.append("banco = :banco")
            params["banco"] = colaborador.banco
        
        if colaborador.agencia is not None:
            update_fields.append("agencia = :agencia")
            params["agencia"] = colaborador.agencia
        
        if colaborador.tipo_conta is not None:
            update_fields.append("tipo_conta = :tipo_conta")
            params["tipo_conta"] = colaborador.tipo_conta
        
        if colaborador.conta is not None:
            update_fields.append("conta = :conta")
            params["conta"] = colaborador.conta
        
        if update_fields:
            db.execute(
                text(f"""
                    UPDATE colaborador_escritorio 
                     SET {', '.join(update_fields)}
                     WHERE colaborador_id = :user_id 
                     AND escritorio_id = :escritorio_id
                """),
                params
            )
            db.commit()
    
    return updated_user


@router.delete("/{colaborador_id}", status_code=204)
def delete_colaborador(
    colaborador_id: int,
    permanent: bool = Query(False, description="Se True, remove permanentemente do banco"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """
    Remove um colaborador (soft delete por padrão, hard delete se permanent=True)
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
    
    # Se for exclusão permanente, remover também os perfis e vínculos
    if permanent:
        # Remover perfis do colaborador neste escritório
        db.execute(
            text("""
                DELETE FROM colaborador_escritorio_perfil 
                WHERE colaborador_id = :user_id 
                AND escritorio_id = :escritorio_id
            """),
            {"user_id": colaborador_id, "escritorio_id": escritorio_id}
        )
        
        # Remover vínculo com o escritório
        db.execute(
            text("""
                DELETE FROM colaborador_escritorio 
                WHERE colaborador_id = :user_id 
                AND escritorio_id = :escritorio_id
            """),
            {"user_id": colaborador_id, "escritorio_id": escritorio_id}
        )
        db.commit()
        
        # Verificar se o colaborador tem outros vínculos com outros escritórios
        outros_vinculos = db.execute(
            text("""
                SELECT COUNT(*) 
                FROM colaborador_escritorio 
                WHERE colaborador_id = :user_id
            """),
            {"user_id": colaborador_id}
        ).scalar()
        
        # Se não tiver outros vínculos, fazer hard delete do usuário
        if outros_vinculos == 0:
            service = UserService(db)
            service.delete(colaborador_id, permanent=True)
        else:
            # Se tiver outros vínculos, apenas remover o vínculo com este escritório
            # (já foi removido acima)
            pass
    else:
        # Soft delete: remover o vínculo com este escritório e desativar o usuário
        # Remover perfis do colaborador neste escritório
        db.execute(
            text("""
                DELETE FROM colaborador_escritorio_perfil 
                WHERE colaborador_id = :user_id 
                AND escritorio_id = :escritorio_id
            """),
            {"user_id": colaborador_id, "escritorio_id": escritorio_id}
        )
        
        # Remover vínculo com o escritório
        db.execute(
            text("""
                DELETE FROM colaborador_escritorio 
                WHERE colaborador_id = :user_id 
                AND escritorio_id = :escritorio_id
            """),
            {"user_id": colaborador_id, "escritorio_id": escritorio_id}
        )
        db.commit()
        
        # Verificar se o colaborador tem outros vínculos com outros escritórios
        outros_vinculos = db.execute(
            text("""
                SELECT COUNT(*) 
                FROM colaborador_escritorio 
                WHERE colaborador_id = :user_id
            """),
            {"user_id": colaborador_id}
        ).scalar()
        
        # Se não tiver outros vínculos, desativar o usuário (soft delete)
        if outros_vinculos == 0:
            service = UserService(db)
            service.delete(colaborador_id, permanent=False)


@router.get("/stats/count")
def count_colaboradores(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """
    Retorna total de colaboradores do escritório atual
    """
    service = UserService(db)
    return {"total": service.count(escritorio_id=escritorio_id)}


@router.put("/{colaborador_id}/perfis", response_model=List[ColaboradorEscritorioPerfilResponse])
def update_colaborador_perfis(
    colaborador_id: int,
    perfis_data: ColaboradorEscritorioPerfilCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """
    Atualiza os perfis de um colaborador em um escritório específico
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
    
    # Verificar se o escritorio_id do request corresponde ao escritório atual
    if perfis_data.escritorio_id != escritorio_id:
        raise HTTPException(
            status_code=403,
            detail="Não é possível atualizar perfis de outro escritório"
        )
    
    # Remover perfis existentes
    db.execute(
        text("""
            DELETE FROM colaborador_escritorio_perfil
            WHERE colaborador_id = :user_id AND escritorio_id = :escritorio_id
        """),
        {"user_id": colaborador_id, "escritorio_id": escritorio_id}
    )
    
    # Inserir novos perfis
    perfis_criados = []
    for perfil in perfis_data.perfis:
        db_perfil = ColaboradorEscritorioPerfil(
            colaborador_id=colaborador_id,
            escritorio_id=escritorio_id,
            perfil=perfil,
            ativo=True
        )
        db.add(db_perfil)
        perfis_criados.append(db_perfil)
    
    db.commit()
    
    # Recarregar perfis criados
    for perfil in perfis_criados:
        db.refresh(perfil)
    
    return [ColaboradorEscritorioPerfilResponse.model_validate(p) for p in perfis_criados]


@router.get("/{colaborador_id}/perfis", response_model=List[ColaboradorEscritorioPerfilResponse])
def get_colaborador_perfis(
    colaborador_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """
    Lista os perfis de um colaborador em um escritório específico
    """
    import traceback
    try:
        # Verificar se o colaborador está vinculado ao escritório
        try:
            vinculado = db.execute(
                text("""
                    SELECT COUNT(*) 
                    FROM colaborador_escritorio 
                    WHERE colaborador_id = :user_id 
                    AND escritorio_id = :escritorio_id
                """),
                {"user_id": colaborador_id, "escritorio_id": escritorio_id}
            ).scalar()
        except Exception as e:
            print(f"Erro ao verificar vínculo do colaborador {colaborador_id} com escritório {escritorio_id}: {e}")
            print(traceback.format_exc())
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao verificar vínculo do colaborador: {str(e)}"
            )
        
        if vinculado == 0:
            raise HTTPException(
                status_code=404,
                detail="Colaborador não encontrado neste escritório"
            )
        
        # Buscar perfis (sem filtrar por ativo para mostrar todos)
        try:
            # Primeiro, verificar diretamente no banco com SQL para debug
            result_sql = db.execute(
                text("""
                    SELECT id, colaborador_id, escritorio_id, perfil, ativo, created_at, updated_at
                    FROM colaborador_escritorio_perfil
                    WHERE colaborador_id = :user_id AND escritorio_id = :escritorio_id
                    ORDER BY perfil
                """),
                {"user_id": colaborador_id, "escritorio_id": escritorio_id}
            ).fetchall()
            
            print(f"Query SQL direta - Perfis encontrados para colaborador {colaborador_id} no escritório {escritorio_id}: {len(result_sql)}")
            for row in result_sql:
                print(f"  - SQL Row: ID={row[0]}, Perfil={row[3]}, Ativo={row[4]}")
            
            # Agora buscar usando ORM
            perfis = db.query(ColaboradorEscritorioPerfil).filter(
                ColaboradorEscritorioPerfil.colaborador_id == colaborador_id,
                ColaboradorEscritorioPerfil.escritorio_id == escritorio_id
            ).order_by(ColaboradorEscritorioPerfil.perfil).all()
            
            # Log para debug
            print(f"ORM Query - Perfis encontrados: {len(perfis)}")
            for p in perfis:
                print(f"  - ORM Perfil: {p.perfil}, ID: {p.id}, Ativo: {p.ativo}")
        except Exception as e:
            print(f"Erro ao buscar perfis do colaborador {colaborador_id}: {e}")
            print(traceback.format_exc())
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao buscar perfis: {str(e)}"
            )
        
        # Se não houver perfis, retornar lista vazia (isso é válido)
        if not perfis:
            return []
        
        # Validar e serializar perfis
        result = []
        for perfil in perfis:
            try:
                # Usar model_validate com from_attributes=True
                result.append(ColaboradorEscritorioPerfilResponse.model_validate(perfil, from_attributes=True))
            except Exception as e:
                # Log do erro mas continua com os outros perfis
                print(f"Erro ao validar perfil {perfil.id}: {e}")
                print(traceback.format_exc())
                # Se houver erro na validação, tentar criar manualmente com valores padrão para datas None
                try:
                    from datetime import datetime
                    result.append(ColaboradorEscritorioPerfilResponse(
                        id=perfil.id,
                        colaborador_id=perfil.colaborador_id,
                        escritorio_id=perfil.escritorio_id,
                        perfil=perfil.perfil,
                        ativo=perfil.ativo,
                        created_at=perfil.created_at if perfil.created_at else datetime.now(),
                        updated_at=perfil.updated_at if perfil.updated_at else datetime.now()
                    ))
                except Exception as e2:
                    print(f"Erro ao criar resposta manual para perfil {perfil.id}: {e2}")
                    continue
        
        print(f"Perfis serializados para retorno: {len(result)}")
        return result
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erro geral ao buscar perfis do colaborador {colaborador_id}: {e}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar perfis do colaborador: {str(e)}"
        )


@router.post("/{colaborador_id}/foto", response_model=UserResponse)
async def upload_colaborador_foto(
    colaborador_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    escritorio_id: int = Depends(get_current_escritorio)
):
    """
    Faz upload de foto do colaborador
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
    
    # Buscar colaborador atual para obter foto antiga
    service = UserService(db)
    colaborador = service.get_by_id(colaborador_id)
    
    if not colaborador:
        raise HTTPException(
            status_code=404,
            detail="Colaborador não encontrado"
        )
    
    # Salvar novo arquivo
    try:
        file_path = save_upload_file(file, subdirectory="colaboradores")
        
        # Deletar foto antiga se existir
        if colaborador.foto:
            delete_upload_file(colaborador.foto)
        
        # Atualizar campo foto no banco
        update_data = UserUpdate(foto=file_path)
        updated_colaborador = service.update(colaborador_id, update_data)
        
        # Buscar campo socio para incluir na resposta
        try:
            socio_result = db.execute(
                text("""
                    SELECT socio 
                    FROM colaborador_escritorio 
                    WHERE colaborador_id = :user_id 
                    AND escritorio_id = :escritorio_id
                """),
                {"user_id": colaborador_id, "escritorio_id": escritorio_id}
            ).first()
            
            if socio_result:
                if hasattr(updated_colaborador, 'model_dump'):
                    colaborador_dict = updated_colaborador.model_dump()
                elif hasattr(updated_colaborador, 'dict'):
                    colaborador_dict = updated_colaborador.dict()
                else:
                    colaborador_dict = updated_colaborador
                
                colaborador_dict['socio'] = bool(socio_result[0]) if socio_result[0] is not None else False
                return UserResponse(**colaborador_dict)
        except Exception:
            pass
        
        return updated_colaborador
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao fazer upload da foto: {str(e)}"
        )
