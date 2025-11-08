"""
Repositório de Etapas
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.etapa import Etapa
from app.schemas.servico import EtapaCreate, EtapaUpdate


class EtapaRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_servico(self, servico_id: int) -> List[Etapa]:
        return self.db.query(Etapa).filter(Etapa.servico_id == servico_id).order_by(Etapa.ordem).all()
    
    def get_by_id(self, etapa_id: int) -> Optional[Etapa]:
        return self.db.query(Etapa).filter(Etapa.id == etapa_id).first()
    
    def create(self, servico_id: int, etapa_data: EtapaCreate) -> Etapa:
        etapa = Etapa(**etapa_data.model_dump(), servico_id=servico_id)
        self.db.add(etapa)
        self.db.commit()
        self.db.refresh(etapa)
        return etapa
    
    def update(self, etapa_id: int, etapa_data: EtapaUpdate) -> Optional[Etapa]:
        etapa = self.get_by_id(etapa_id)
        if not etapa:
            return None
        
        update_data = etapa_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(etapa, field, value)
        
        self.db.commit()
        self.db.refresh(etapa)
        return etapa
    
    def delete(self, etapa_id: int) -> bool:
        etapa = self.get_by_id(etapa_id)
        if not etapa:
            return False
        
        self.db.delete(etapa)
        self.db.commit()
        return True
