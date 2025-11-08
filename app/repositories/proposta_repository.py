"""
Repositório de Propostas
"""
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models.proposta import Proposta
from app.schemas.proposta import PropostaCreate, PropostaUpdate


class PropostaRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(
        self, 
        skip: int = 0, 
        limit: int = 100,
        cliente_id: Optional[int] = None,
        status_id: Optional[int] = None,
        ano: Optional[int] = None
    ) -> List[Proposta]:
        query = self.db.query(Proposta).options(
            joinedload(Proposta.cliente),
            joinedload(Proposta.servico),
            joinedload(Proposta.status)
        )
        
        if cliente_id:
            query = query.filter(Proposta.cliente_id == cliente_id)
        
        if status_id:
            query = query.filter(Proposta.status_id == status_id)
        
        if ano:
            query = query.filter(Proposta.ano_proposta == ano)
        
        return query.order_by(Proposta.ano_proposta.desc(), Proposta.numero_proposta.desc()).offset(skip).limit(limit).all()
    
    def get_by_id(self, proposta_id: int) -> Optional[Proposta]:
        return self.db.query(Proposta).options(
            joinedload(Proposta.cliente),
            joinedload(Proposta.servico),
            joinedload(Proposta.status)
        ).filter(Proposta.id == proposta_id).first()
    
    def create(self, proposta_data: PropostaCreate) -> Proposta:
        proposta = Proposta(**proposta_data.model_dump())
        self.db.add(proposta)
        self.db.commit()
        self.db.refresh(proposta)
        return proposta
    
    def update(self, proposta_id: int, proposta_data: PropostaUpdate) -> Optional[Proposta]:
        proposta = self.get_by_id(proposta_id)
        if not proposta:
            return None
        
        update_data = proposta_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(proposta, field, value)
        
        self.db.commit()
        self.db.refresh(proposta)
        return proposta
    
    def delete(self, proposta_id: int) -> bool:
        proposta = self.get_by_id(proposta_id)
        if not proposta:
            return False
        
        self.db.delete(proposta)
        self.db.commit()
        return True
    
    def count(
        self,
        cliente_id: Optional[int] = None,
        status_id: Optional[int] = None,
        ano: Optional[int] = None
    ) -> int:
        query = self.db.query(Proposta)
        
        if cliente_id:
            query = query.filter(Proposta.cliente_id == cliente_id)
        
        if status_id:
            query = query.filter(Proposta.status_id == status_id)
        
        if ano:
            query = query.filter(Proposta.ano_proposta == ano)
        
        return query.count()
    
    def search(self, search_term: str, skip: int = 0, limit: int = 100) -> List[Proposta]:
        return self.db.query(Proposta).options(
            joinedload(Proposta.cliente),
            joinedload(Proposta.servico),
            joinedload(Proposta.status)
        ).filter(
            (Proposta.nome.ilike(f"%{search_term}%")) |
            (Proposta.identificacao.ilike(f"%{search_term}%")) |
            (Proposta.descricao.ilike(f"%{search_term}%"))
        ).offset(skip).limit(limit).all()
    
    def get_proximo_numero(self, ano: int) -> int:
        """Retorna o próximo número de proposta para o ano"""
        ultimo = self.db.query(Proposta).filter(
            Proposta.ano_proposta == ano
        ).order_by(Proposta.numero_proposta.desc()).first()
        
        return (ultimo.numero_proposta + 1) if ultimo else 1
