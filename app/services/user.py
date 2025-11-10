from sqlalchemy.orm import Session
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.core.exceptions import NotFoundException, ConflictException
from typing import List, Optional


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository(db)
    
    def get_all(
        self, 
        escritorio_id: Optional[int] = None,
        skip: int = 0, 
        limit: int = 100,
        ativo: Optional[bool] = None,
        search: Optional[str] = None
    ) -> List[UserResponse]:
        """Lista todos os usuários, opcionalmente filtrado por escritório"""
        users = self.repository.get_all(escritorio_id, skip, limit, ativo, search)
        return [UserResponse.from_orm(user) for user in users]
    
    def get_by_id(self, user_id: int) -> UserResponse:
        """Busca usuário por ID"""
        user = self.repository.get_by_id(user_id)
        if not user:
            raise NotFoundException(f"Usuário {user_id} não encontrado")
        return UserResponse.from_orm(user)
    
    def create(self, user: UserCreate) -> UserResponse:
        """Cria novo usuário"""
        # Verificar se email já existe
        existing_email = self.repository.get_by_email(user.email)
        if existing_email:
            raise ConflictException("Email já cadastrado")
        
        # Verificar se CPF já existe (apenas se fornecido)
        if user.cpf and user.cpf.strip():
            existing_cpf = self.repository.get_by_cpf(user.cpf)
            if existing_cpf:
                raise ConflictException("CPF já cadastrado")
        
        db_user = self.repository.create(user)
        return UserResponse.from_orm(db_user)
    
    def update(self, user_id: int, user: UserUpdate) -> UserResponse:
        """Atualiza usuário"""
        db_user = self.repository.update(user_id, user)
        if not db_user:
            raise NotFoundException(f"Usuário {user_id} não encontrado")
        return UserResponse.from_orm(db_user)
    
    def delete(self, user_id: int, permanent: bool = False) -> bool:
        """
        Remove usuário
        
        Args:
            user_id: ID do usuário
            permanent: Se True, remove permanentemente. Se False, soft delete (marca como inativo)
        """
        success = self.repository.delete(user_id, permanent=permanent)
        if not success:
            raise NotFoundException(f"Usuário {user_id} não encontrado")
        return True
    
    def count(self, escritorio_id: Optional[int] = None) -> int:
        """Conta total de usuários, opcionalmente filtrado por escritório"""
        return self.repository.count(escritorio_id)
