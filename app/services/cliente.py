from sqlalchemy.orm import Session
from app.repositories.cliente import ClienteRepository
from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse
from app.core.exceptions import NotFoundException, ConflictException
from typing import List, Optional


class ClienteService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = ClienteRepository(db)
    
    def get_all(
        self,
        escritorio_id: int,
        skip: int = 0, 
        limit: int = 100,
        ativo: Optional[bool] = None,
        tipo_pessoa: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[ClienteResponse]:
        """Lista todos os clientes, isolados por escritório"""
        clientes = self.repository.get_all(escritorio_id, skip, limit, ativo, tipo_pessoa, search)
        return [ClienteResponse.from_orm(c, self.db) for c in clientes]
    
    def get_by_id(self, cliente_id: int, escritorio_id: int) -> ClienteResponse:
        """Busca cliente por ID, garantindo que pertence ao escritório"""
        cliente = self.repository.get_by_id(cliente_id, escritorio_id)
        if not cliente:
            raise NotFoundException(f"Cliente {cliente_id} não encontrado")
        return ClienteResponse.from_orm(cliente, self.db)
    
    def create(self, cliente: ClienteCreate, escritorio_id: int) -> ClienteResponse:
        """Cria novo cliente, vinculado ao escritório"""
        # Verificar se email já existe no escritório
        if cliente.email:
            existing_email = self.repository.get_by_email(cliente.email, escritorio_id)
            if existing_email:
                raise ConflictException("Email já cadastrado neste escritório")
        
        # Verificar se CPF/CNPJ já existe no escritório
        if cliente.cpf_cnpj:
            existing_doc = self.repository.get_by_identificacao(cliente.cpf_cnpj, escritorio_id)
            if existing_doc:
                doc_type = "CPF" if cliente.tipo_pessoa == "Física" else "CNPJ"
                raise ConflictException(f"{doc_type} já cadastrado neste escritório")
        
        db_cliente = self.repository.create(cliente, escritorio_id)
        return ClienteResponse.from_orm(db_cliente, self.db)
    
    def update(self, cliente_id: int, cliente: ClienteUpdate, escritorio_id: int) -> ClienteResponse:
        """Atualiza cliente, garantindo que pertence ao escritório"""
        # Verificar se email já existe no escritório (se estiver sendo alterado)
        if cliente.email:
            existing = self.repository.get_by_email(cliente.email, escritorio_id)
            if existing and existing.id != cliente_id:
                raise ConflictException("Email já cadastrado neste escritório")
        
        db_cliente = self.repository.update(cliente_id, cliente, escritorio_id)
        if not db_cliente:
            raise NotFoundException(f"Cliente {cliente_id} não encontrado")
        return ClienteResponse.from_orm(db_cliente, self.db)
    
    def delete(self, cliente_id: int, escritorio_id: int, permanent: bool = False) -> bool:
        """
        Remove cliente, garantindo que pertence ao escritório
        
        Args:
            cliente_id: ID do cliente
            escritorio_id: ID do escritório
            permanent: Se True, remove permanentemente. Se False, soft delete (marca como inativo)
        """
        success = self.repository.delete(cliente_id, escritorio_id, permanent=permanent)
        if not success:
            raise NotFoundException(f"Cliente {cliente_id} não encontrado")
        return True
    
    def count(
        self,
        escritorio_id: int,
        ativo: Optional[bool] = None,
        tipo_pessoa: Optional[str] = None,
        search: Optional[str] = None
    ) -> int:
        """Conta total de clientes com filtros, isolados por escritório"""
        return self.repository.count(escritorio_id, ativo, tipo_pessoa, search)
