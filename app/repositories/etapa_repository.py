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
    
    def get_by_servico(self, servico_id: int, escritorio_id: int) -> List[Etapa]:
        """Lista etapas de um serviço, garantindo que pertencem ao escritório"""
        return self.db.query(Etapa).filter(
            Etapa.servico_id == servico_id,
            Etapa.escritorio_id == escritorio_id
        ).order_by(Etapa.ordem).all()
    
    def get_by_id(self, etapa_id: int, escritorio_id: int) -> Optional[Etapa]:
        """Busca etapa por ID, garantindo que pertence ao escritório"""
        return self.db.query(Etapa).filter(
            Etapa.id == etapa_id,
            Etapa.escritorio_id == escritorio_id
        ).first()
    
    def create(self, servico_id: int, etapa_data: EtapaCreate, escritorio_id: int) -> Etapa:
        """Cria nova etapa, vinculada ao escritório"""
        etapa_dict = etapa_data.model_dump()
        etapa_dict['escritorio_id'] = escritorio_id
        etapa = Etapa(**etapa_dict, servico_id=servico_id)
        self.db.add(etapa)
        self.db.commit()
        self.db.refresh(etapa)
        return etapa
    
    def update(self, etapa_id: int, etapa_data: EtapaUpdate, escritorio_id: int) -> Optional[Etapa]:
        """Atualiza etapa, garantindo que pertence ao escritório"""
        etapa = self.get_by_id(etapa_id, escritorio_id)
        if not etapa:
            return None
        
        update_data = etapa_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(etapa, field, value)
        
        self.db.commit()
        self.db.refresh(etapa)
        return etapa
    
    def delete(self, etapa_id: int, escritorio_id: int) -> bool:
        """Deleta etapa, garantindo que pertence ao escritório"""
        etapa = self.get_by_id(etapa_id, escritorio_id)
        if not etapa:
            return False
        
        self.db.delete(etapa)
        self.db.commit()
        return True
