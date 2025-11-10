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
        escritorio_id: int,
        skip: int = 0, 
        limit: int = 100,
        cliente_id: Optional[int] = None,
        status_id: Optional[int] = None,
        ano: Optional[int] = None
    ) -> List[Proposta]:
        """Lista todas as propostas com filtros, isoladas por escritório"""
        query = self.db.query(Proposta).filter(Proposta.escritorio_id == escritorio_id).options(
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
    
    def get_by_id(self, proposta_id: int, escritorio_id: int) -> Optional[Proposta]:
        """Busca proposta por ID, garantindo que pertence ao escritório"""
        return self.db.query(Proposta).options(
            joinedload(Proposta.cliente),
            joinedload(Proposta.servico),
            joinedload(Proposta.status)
        ).filter(
            Proposta.id == proposta_id,
            Proposta.escritorio_id == escritorio_id
        ).first()
    
    def create(self, proposta_data: PropostaCreate, escritorio_id: int) -> Proposta:
        """Cria nova proposta, vinculada ao escritório"""
        proposta_dict = proposta_data.model_dump()
        proposta_dict['escritorio_id'] = escritorio_id
        proposta = Proposta(**proposta_dict)
        self.db.add(proposta)
        self.db.commit()
        self.db.refresh(proposta)
        return proposta
    
    def update(self, proposta_id: int, proposta_data: PropostaUpdate, escritorio_id: int) -> Optional[Proposta]:
        """Atualiza proposta, garantindo que pertence ao escritório"""
        proposta = self.get_by_id(proposta_id, escritorio_id)
        if not proposta:
            return None
        
        update_data = proposta_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(proposta, field, value)
        
        self.db.commit()
        self.db.refresh(proposta)
        return proposta
    
    def delete(self, proposta_id: int, escritorio_id: int) -> bool:
        """Remove proposta, garantindo que pertence ao escritório"""
        proposta = self.get_by_id(proposta_id, escritorio_id)
        if not proposta:
            return False
        
        self.db.delete(proposta)
        self.db.commit()
        return True
    
    def count(
        self,
        escritorio_id: int,
        cliente_id: Optional[int] = None,
        status_id: Optional[int] = None,
        ano: Optional[int] = None
    ) -> int:
        """Conta total de propostas com filtros, isoladas por escritório"""
        query = self.db.query(Proposta).filter(Proposta.escritorio_id == escritorio_id)
        
        if cliente_id:
            query = query.filter(Proposta.cliente_id == cliente_id)
        
        if status_id:
            query = query.filter(Proposta.status_id == status_id)
        
        if ano:
            query = query.filter(Proposta.ano_proposta == ano)
        
        return query.count()
    
    def search(self, escritorio_id: int, search_term: str, skip: int = 0, limit: int = 100) -> List[Proposta]:
        """Busca propostas por termo, isoladas por escritório"""
        return self.db.query(Proposta).options(
            joinedload(Proposta.cliente),
            joinedload(Proposta.servico),
            joinedload(Proposta.status)
        ).filter(
            Proposta.escritorio_id == escritorio_id,
            (Proposta.nome.ilike(f"%{search_term}%")) |
            (Proposta.identificacao.ilike(f"%{search_term}%")) |
            (Proposta.descricao.ilike(f"%{search_term}%"))
        ).offset(skip).limit(limit).all()
    
    def get_proximo_numero(self, escritorio_id: int, ano: int) -> int:
        """Retorna o próximo número de proposta para o ano, isolado por escritório"""
        ultimo = self.db.query(Proposta).filter(
            Proposta.escritorio_id == escritorio_id,
            Proposta.ano_proposta == ano
        ).order_by(Proposta.numero_proposta.desc()).first()
        
        return (ultimo.numero_proposta + 1) if ultimo else 1
