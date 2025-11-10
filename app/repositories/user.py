from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, text
from app.models.user import User, Escritorio
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash
from typing import List, Optional


class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(
        self, 
        skip: int = 0, 
        limit: int = 100,
        ativo: Optional[bool] = None,
        search: Optional[str] = None
    ) -> List[User]:
        """Lista todos os usuários com filtros"""
        query = self.db.query(User).options(joinedload(User.escritorios))
        
        if ativo is not None:
            query = query.filter(User.ativo == ativo)
        
        if search:
            query = query.filter(
                or_(
                    User.nome.ilike(f"%{search}%"),
                    User.email.ilike(f"%{search}%"),
                    User.cpf.ilike(f"%{search}%")
                )
            )
        
        return query.offset(skip).limit(limit).all()
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Busca usuário por ID"""
        return self.db.query(User).options(joinedload(User.escritorios)).filter(User.id == user_id).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Busca usuário por email"""
        return self.db.query(User).options(joinedload(User.escritorios)).filter(User.email == email).first()
    
    def get_by_cpf(self, cpf: str) -> Optional[User]:
        """Busca usuário por CPF"""
        return self.db.query(User).filter(User.cpf == cpf).first()
    
    def create(self, user: UserCreate) -> User:
        """Cria novo usuário"""
        # Hash da senha
        hashed_password = get_password_hash(user.senha)
        
        # Criar usuário
        db_user = User(
            nome=user.nome,
            email=user.email,
            senha=hashed_password,
            cpf=user.cpf if user.cpf and user.cpf.strip() else None,  # CPF opcional
            telefone=user.telefone,
            data_nascimento=user.data_nascimento,
            perfil=user.perfil,
            tipo=user.tipo,
            tipo_pix=user.tipo_pix,
            chave_pix=user.chave_pix,
            is_system_admin=user.is_system_admin if hasattr(user, 'is_system_admin') and user.is_system_admin else False
        )
        
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def update(self, user_id: int, user: UserUpdate) -> Optional[User]:
        """Atualiza usuário"""
        db_user = self.get_by_id(user_id)
        if not db_user:
            return None
        
        update_data = user.dict(exclude_unset=True)
        
        # Se senha foi fornecida, fazer hash antes de salvar
        if 'senha' in update_data and update_data['senha']:
            update_data['senha'] = get_password_hash(update_data['senha'])
        
        # Se CPF foi fornecido, tratar como opcional
        if 'cpf' in update_data:
            if update_data['cpf'] is None or (isinstance(update_data['cpf'], str) and not update_data['cpf'].strip()):
                update_data['cpf'] = None
        
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def delete(self, user_id: int, permanent: bool = False) -> bool:
        """
        Remove usuário
        
        Args:
            user_id: ID do usuário
            permanent: Se True, remove permanentemente. Se False, soft delete (marca como inativo)
        """
        db_user = self.get_by_id(user_id)
        if not db_user:
            return False
        
        if permanent:
            # Hard delete - remove do banco permanentemente
            # Primeiro, remover relacionamentos com escritórios
            self.db.execute(
                text("DELETE FROM colaborador_escritorio WHERE colaborador_id = :user_id"),
                {"user_id": user_id}
            )
            self.db.delete(db_user)
        else:
            # Soft delete - marca como inativo
            db_user.ativo = False
        
        self.db.commit()
        return True
    
    def count(self) -> int:
        """Conta total de usuários"""
        return self.db.query(User).count()


class EscritorioRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self, skip: int = 0, limit: int = 100, ativo: Optional[bool] = None) -> List[Escritorio]:
        """Lista todos os escritórios"""
        query = self.db.query(Escritorio)
        if ativo is not None:
            query = query.filter(Escritorio.ativo == ativo)
        return query.offset(skip).limit(limit).all()
    
    def get_by_id(self, escritorio_id: int) -> Optional[Escritorio]:
        """Busca escritório por ID"""
        return self.db.query(Escritorio).filter(Escritorio.id == escritorio_id).first()
    
    def get_by_documento(self, documento: str) -> Optional[Escritorio]:
        """Busca escritório por documento (CNPJ)"""
        return self.db.query(Escritorio).filter(Escritorio.documento == documento).first()
    
    def update(self, escritorio_id: int, escritorio_data: dict) -> Optional[Escritorio]:
        """Atualiza escritório"""
        escritorio = self.get_by_id(escritorio_id)
        if not escritorio:
            return None
        
        for field, value in escritorio_data.items():
            setattr(escritorio, field, value)
        
        self.db.commit()
        self.db.refresh(escritorio)
        return escritorio
    
    def delete(self, escritorio_id: int, permanent: bool = False) -> bool:
        """
        Remove escritório
        
        Args:
            escritorio_id: ID do escritório
            permanent: Se True, remove permanentemente. Se False, soft delete (marca como inativo)
        """
        from app.models.user import User, user_escritorio
        
        escritorio = self.get_by_id(escritorio_id)
        if not escritorio:
            return False
        
        if permanent:
            # Hard delete - remove do banco permanentemente
            # IMPORTANTE: Excluir todos os dados relacionados ao escritório
            
            # 1. Desativar/Excluir usuários que só têm acesso a este escritório
            usuarios_vinculados = (
                self.db.query(User)
                .join(user_escritorio, User.id == user_escritorio.c.colaborador_id)
                .filter(user_escritorio.c.escritorio_id == escritorio_id)
                .all()
            )
            
            for usuario in usuarios_vinculados:
                # Verificar se o usuário tem acesso a outros escritórios
                outros_escritorios_count = self.db.execute(
                    text("""
                        SELECT COUNT(*) 
                        FROM colaborador_escritorio 
                        WHERE colaborador_id = :user_id 
                        AND escritorio_id != :escritorio_id
                    """),
                    {"user_id": usuario.id, "escritorio_id": escritorio_id}
                ).scalar()
                
                # Se não tiver outros escritórios e não for admin do sistema, excluir o usuário
                if outros_escritorios_count == 0 and not usuario.is_system_admin:
                    # Remover relacionamentos restantes do usuário
                    self.db.execute(
                        text("DELETE FROM colaborador_escritorio WHERE colaborador_id = :user_id"),
                        {"user_id": usuario.id}
                    )
                    # Excluir o usuário
                    self.db.delete(usuario)
            
            # 2. Remover relacionamentos com colaboradores
            self.db.execute(
                text("DELETE FROM colaborador_escritorio WHERE escritorio_id = :escritorio_id"),
                {"escritorio_id": escritorio_id}
            )
            
            # 3. Excluir movimentações de contas bancárias do escritório
            # Usar subquery para excluir todas as movimentações das contas do escritório
            self.db.execute(
                text("""
                    DELETE FROM conta_movimentacao 
                    WHERE conta_bancaria_id IN (
                        SELECT id FROM conta_bancaria WHERE escritorio_id = :escritorio_id
                    )
                """),
                {"escritorio_id": escritorio_id}
            )
            
            # 4. Excluir contas bancárias do escritório
            self.db.execute(
                text("DELETE FROM conta_bancaria WHERE escritorio_id = :escritorio_id"),
                {"escritorio_id": escritorio_id}
            )
            
            # 5. Excluir plano de contas do escritório
            self.db.execute(
                text("DELETE FROM plano_contas WHERE escritorio_id = :escritorio_id"),
                {"escritorio_id": escritorio_id}
            )
            
            # 6. Excluir o escritório
            self.db.delete(escritorio)
        else:
            # Soft delete - marca como inativo
            escritorio.ativo = False
            
            # Desativar todos os usuários vinculados que não têm outros escritórios
            usuarios_vinculados = (
                self.db.query(User)
                .join(user_escritorio, User.id == user_escritorio.c.colaborador_id)
                .filter(
                    user_escritorio.c.escritorio_id == escritorio_id,
                    user_escritorio.c.ativo == True
                )
                .all()
            )
            
            for usuario in usuarios_vinculados:
                # Verificar se o usuário tem acesso a outros escritórios ativos
                outros_escritorios_count = self.db.execute(
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
            self.db.execute(
                text("""
                    UPDATE colaborador_escritorio 
                    SET ativo = false 
                    WHERE escritorio_id = :escritorio_id AND ativo = true
                """),
                {"escritorio_id": escritorio_id}
            )
        
        self.db.commit()
        return True
