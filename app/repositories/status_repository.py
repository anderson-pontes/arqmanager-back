"""
Repositório de Status
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.status import Status
from app.schemas.projeto import StatusCreate, StatusUpdate


class StatusRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self, escritorio_id: int, skip: int = 0, limit: int = 100, ativo: Optional[bool] = None) -> List[Status]:
        """Lista todos os status, isolados por escritório"""
        query = self.db.query(Status).filter(Status.escritorio_id == escritorio_id)
        
        if ativo is not None:
            query = query.filter(Status.ativo == ativo)
        
        return query.offset(skip).limit(limit).all()
    
    def get_by_id(self, status_id: int, escritorio_id: int) -> Optional[Status]:
        """Busca status por ID, garantindo que pertence ao escritório"""
        return self.db.query(Status).filter(
            Status.id == status_id,
            Status.escritorio_id == escritorio_id
        ).first()
    
    def create(self, status_data: StatusCreate, escritorio_id: int) -> Status:
        """Cria novo status, vinculado ao escritório"""
        status_dict = status_data.model_dump()
        status_dict['escritorio_id'] = escritorio_id
        status = Status(**status_dict)
        self.db.add(status)
        self.db.commit()
        self.db.refresh(status)
        return status
    
    def update(self, status_id: int, status_data: StatusUpdate, escritorio_id: int) -> Optional[Status]:
        """Atualiza status, garantindo que pertence ao escritório"""
        status = self.get_by_id(status_id, escritorio_id)
        if not status:
            return None
        
        update_data = status_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(status, field, value)
        
        self.db.commit()
        self.db.refresh(status)
        return status
    
    def delete(self, status_id: int, escritorio_id: int) -> bool:
        """Deleta status, garantindo que pertence ao escritório"""
        status = self.get_by_id(status_id, escritorio_id)
        if not status:
            return False
        
        self.db.delete(status)
        self.db.commit()
        return True
