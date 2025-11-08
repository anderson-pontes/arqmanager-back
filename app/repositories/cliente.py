from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteUpdate
from typing import List, Optional


class ClienteRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(
        self, 
        skip: int = 0, 
        limit: int = 100,
        ativo: Optional[bool] = None,
        tipo_pessoa: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[Cliente]:
        """Lista todos os clientes com filtros"""
        query = self.db.query(Cliente)
        
        if ativo is not None:
            query = query.filter(Cliente.ativo == ativo)
        
        if tipo_pessoa:
            query = query.filter(Cliente.tipo_pessoa == tipo_pessoa)
        
        if search:
            query = query.filter(
                or_(
                    Cliente.nome.ilike(f"%{search}%"),
                    Cliente.email.ilike(f"%{search}%"),
                    Cliente.identificacao.ilike(f"%{search}%"),
                    Cliente.cidade.ilike(f"%{search}%")
                )
            )
        
        return query.offset(skip).limit(limit).all()
    
    def get_by_id(self, cliente_id: int) -> Optional[Cliente]:
        """Busca cliente por ID"""
        return self.db.query(Cliente).filter(Cliente.id == cliente_id).first()
    
    def get_by_email(self, email: str) -> Optional[Cliente]:
        """Busca cliente por email"""
        return self.db.query(Cliente).filter(Cliente.email == email).first()
    
    def get_by_identificacao(self, identificacao: str) -> Optional[Cliente]:
        """Busca cliente por CPF/CNPJ"""
        return self.db.query(Cliente).filter(Cliente.identificacao == identificacao).first()
    
    def create(self, cliente: ClienteCreate) -> Cliente:
        """Cria novo cliente"""
        db_cliente = Cliente(**cliente.dict())
        self.db.add(db_cliente)
        self.db.commit()
        self.db.refresh(db_cliente)
        return db_cliente
    
    def update(self, cliente_id: int, cliente: ClienteUpdate) -> Optional[Cliente]:
        """Atualiza cliente"""
        db_cliente = self.get_by_id(cliente_id)
        if not db_cliente:
            return None
        
        update_data = cliente.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_cliente, field, value)
        
        self.db.commit()
        self.db.refresh(db_cliente)
        return db_cliente
    
    def delete(self, cliente_id: int) -> bool:
        """Remove cliente (soft delete)"""
        db_cliente = self.get_by_id(cliente_id)
        if not db_cliente:
            return False
        
        db_cliente.ativo = False
        self.db.commit()
        return True
    
    def count(self, ativo: Optional[bool] = None) -> int:
        """Conta total de clientes"""
        query = self.db.query(Cliente)
        if ativo is not None:
            query = query.filter(Cliente.ativo == ativo)
        return query.count()
