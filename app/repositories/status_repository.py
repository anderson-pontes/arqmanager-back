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
    
    def get_all(self, skip: int = 0, limit: int = 100, ativo: Optional[bool] = None) -> List[Status]:
        query = self.db.query(Status)
        
        if ativo is not None:
            query = query.filter(Status.ativo == ativo)
        
        return query.offset(skip).limit(limit).all()
    
    def get_by_id(self, status_id: int) -> Optional[Status]:
        return self.db.query(Status).filter(Status.id == status_id).first()
    
    def create(self, status_data: StatusCreate) -> Status:
        status = Status(**status_data.model_dump())
        self.db.add(status)
        self.db.commit()
        self.db.refresh(status)
        return status
    
    def update(self, status_id: int, status_data: StatusUpdate) -> Optional[Status]:
        status = self.get_by_id(status_id)
        if not status:
            return None
        
        update_data = status_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(status, field, value)
        
        self.db.commit()
        self.db.refresh(status)
        return status
    
    def delete(self, status_id: int) -> bool:
        status = self.get_by_id(status_id)
        if not status:
            return False
        
        self.db.delete(status)
        self.db.commit()
        return True
