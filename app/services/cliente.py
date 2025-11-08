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
        skip: int = 0, 
        limit: int = 100,
        ativo: Optional[bool] = None,
        tipo_pessoa: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[ClienteResponse]:
        """Lista todos os clientes"""
        clientes = self.repository.get_all(skip, limit, ativo, tipo_pessoa, search)
        return [ClienteResponse.from_orm(c) for c in clientes]
    
    def get_by_id(self, cliente_id: int) -> ClienteResponse:
        """Busca cliente por ID"""
        cliente = self.repository.get_by_id(cliente_id)
        if not cliente:
            raise NotFoundException(f"Cliente {cliente_id} não encontrado")
        return ClienteResponse.from_orm(cliente)
    
    def create(self, cliente: ClienteCreate) -> ClienteResponse:
        """Cria novo cliente"""
        # Verificar se email já existe
        existing_email = self.repository.get_by_email(cliente.email)
        if existing_email:
            raise ConflictException("Email já cadastrado")
        
        # Verificar se CPF/CNPJ já existe
        existing_doc = self.repository.get_by_identificacao(cliente.identificacao)
        if existing_doc:
            doc_type = "CPF" if cliente.tipo_pessoa.value == "Física" else "CNPJ"
            raise ConflictException(f"{doc_type} já cadastrado")
        
        db_cliente = self.repository.create(cliente)
        return ClienteResponse.from_orm(db_cliente)
    
    def update(self, cliente_id: int, cliente: ClienteUpdate) -> ClienteResponse:
        """Atualiza cliente"""
        # Verificar se email já existe (se estiver sendo alterado)
        if cliente.email:
            existing = self.repository.get_by_email(cliente.email)
            if existing and existing.id != cliente_id:
                raise ConflictException("Email já cadastrado")
        
        db_cliente = self.repository.update(cliente_id, cliente)
        if not db_cliente:
            raise NotFoundException(f"Cliente {cliente_id} não encontrado")
        return ClienteResponse.from_orm(db_cliente)
    
    def delete(self, cliente_id: int) -> bool:
        """Remove cliente (soft delete)"""
        success = self.repository.delete(cliente_id)
        if not success:
            raise NotFoundException(f"Cliente {cliente_id} não encontrado")
        return True
    
    def count(self, ativo: Optional[bool] = None) -> int:
        """Conta total de clientes"""
        return self.repository.count(ativo)
