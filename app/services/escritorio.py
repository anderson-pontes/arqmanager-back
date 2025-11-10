from sqlalchemy.orm import Session
from sqlalchemy import text
from app.repositories.user import EscritorioRepository, UserRepository
from app.schemas.user import EscritorioCreate, UserCreate
from app.models.user import Escritorio, User
from app.core.security import get_password_hash
from app.core.exceptions import NotFoundException
from typing import Dict


class EscritorioService:
    def __init__(self, db: Session):
        self.db = db
        self.escritorio_repo = EscritorioRepository(db)
        self.user_repo = UserRepository(db)
    
    def create_with_admin(
        self, 
        escritorio_data: EscritorioCreate,
        admin_data: UserCreate
    ) -> Dict:
        """
        Cria um novo escritório e automaticamente cria um admin do escritório
        
        Args:
            escritorio_data: Dados do escritório
            admin_data: Dados do administrador do escritório
            
        Returns:
            Dict com escritorio e admin criados
        """
        # Criar escritório
        db_escritorio = Escritorio(
            nome_fantasia=escritorio_data.nome_fantasia,
            razao_social=escritorio_data.razao_social,
            documento=escritorio_data.documento if escritorio_data.documento and escritorio_data.documento.strip() else None,
            cpf=escritorio_data.cpf if escritorio_data.cpf and escritorio_data.cpf.strip() else None,
            email=escritorio_data.email,
            telefone=escritorio_data.telefone,
            endereco=escritorio_data.endereco,
            logradouro=escritorio_data.logradouro,
            numero=escritorio_data.numero,
            complemento=escritorio_data.complemento,
            bairro=escritorio_data.bairro,
            cidade=escritorio_data.cidade,
            uf=escritorio_data.uf,
            cep=escritorio_data.cep,
            cor=escritorio_data.cor
        )
        self.db.add(db_escritorio)
        self.db.flush()  # Para obter o ID
        
        # Criar admin do escritório
        admin_data.perfil = "Admin"
        admin_data.is_system_admin = False  # Admin do escritório, não do sistema
        admin_user = self.user_repo.create(admin_data)
        
        # Vincular admin ao escritório
        self.db.execute(
            text("""
                INSERT INTO colaborador_escritorio (colaborador_id, escritorio_id, perfil, ativo)
                VALUES (:user_id, :escritorio_id, 'Admin', true)
            """),
            {"user_id": admin_user.id, "escritorio_id": db_escritorio.id}
        )
        
        self.db.commit()
        self.db.refresh(db_escritorio)
        self.db.refresh(admin_user)
        
        return {
            "escritorio": db_escritorio,
            "admin": admin_user
        }
    
    def get_by_id(self, escritorio_id: int) -> Escritorio:
        """Busca escritório por ID"""
        escritorio = self.escritorio_repo.get_by_id(escritorio_id)
        if not escritorio:
            raise NotFoundException("Escritório não encontrado")
        return escritorio

