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
