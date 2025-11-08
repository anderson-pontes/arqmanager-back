"""
Repositório de Serviços
"""
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models.servico import Servico
from app.models.etapa import Etapa
from app.schemas.servico import ServicoCreate, ServicoUpdate


class ServicoRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self, skip: int = 0, limit: int = 100, ativo: Optional[bool] = None) -> List[Servico]:
        query = self.db.query(Servico).options(joinedload(Servico.etapas))
        
        if ativo is not None:
            query = query.filter(Servico.ativo == ativo)
        
        return query.offset(skip).limit(limit).all()
    
    def get_by_id(self, servico_id: int) -> Optional[Servico]:
        return self.db.query(Servico).options(joinedload(Servico.etapas)).filter(Servico.id == servico_id).first()
    
    def create(self, servico_data: ServicoCreate) -> Servico:
        # Criar serviço
        servico_dict = servico_data.model_dump(exclude={"etapas"})
        servico = Servico(**servico_dict)
        
        # Adicionar etapas
        if servico_data.etapas:
            for etapa_data in servico_data.etapas:
                etapa = Etapa(**etapa_data.model_dump(), servico=servico)
                servico.etapas.append(etapa)
        
        self.db.add(servico)
        self.db.commit()
        self.db.refresh(servico)
        return servico
    
    def update(self, servico_id: int, servico_data: ServicoUpdate) -> Optional[Servico]:
        servico = self.get_by_id(servico_id)
        if not servico:
            return None
        
        update_data = servico_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(servico, field, value)
        
        self.db.commit()
        self.db.refresh(servico)
        return servico
    
    def delete(self, servico_id: int) -> bool:
        servico = self.get_by_id(servico_id)
        if not servico:
            return False
        
        self.db.delete(servico)
        self.db.commit()
        return True
    
    def count(self, ativo: Optional[bool] = None) -> int:
        query = self.db.query(Servico)
        if ativo is not None:
            query = query.filter(Servico.ativo == ativo)
        return query.count()
    
    def search(self, search_term: str, skip: int = 0, limit: int = 100) -> List[Servico]:
        return self.db.query(Servico).options(joinedload(Servico.etapas)).filter(
            Servico.nome.ilike(f"%{search_term}%")
        ).offset(skip).limit(limit).all()
