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
        # Mapear campos do frontend para o banco
        cliente_data = {
            'nome': cliente.nome,
            'email': cliente.email,
            'telefone': cliente.telefone,
            'identificacao': cliente.cpf_cnpj,
            'tipo_pessoa': cliente.tipo_pessoa,
            'data_nascimento': cliente.data_nascimento,
            'logradouro': cliente.endereco,
            'cidade': cliente.cidade,
            'uf': cliente.estado,
            'cep': cliente.cep,
            'indicado_por': cliente.observacoes,
            'ativo': cliente.ativo if cliente.ativo is not None else True
        }
        
        db_cliente = Cliente(**cliente_data)
        self.db.add(db_cliente)
        self.db.commit()
        self.db.refresh(db_cliente)
        return db_cliente
    
    def update(self, cliente_id: int, cliente: ClienteUpdate) -> Optional[Cliente]:
        """Atualiza cliente"""
        db_cliente = self.get_by_id(cliente_id)
        if not db_cliente:
            return None
        
        # Mapear campos do frontend para o banco
        field_mapping = {
            'cpf_cnpj': 'identificacao',
            'endereco': 'logradouro',
            'estado': 'uf',
            'observacoes': 'indicado_por'
        }
        
        update_data = cliente.dict(exclude_unset=True)
        for frontend_field, backend_field in field_mapping.items():
            if frontend_field in update_data:
                value = update_data.pop(frontend_field)
                update_data[backend_field] = value
        
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
    
    def count(
        self, 
        ativo: Optional[bool] = None,
        tipo_pessoa: Optional[str] = None,
        search: Optional[str] = None
    ) -> int:
        """Conta total de clientes com filtros"""
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
        
        return query.count()
