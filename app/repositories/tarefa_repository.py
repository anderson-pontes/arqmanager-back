"""
Repositório de Tarefas
"""
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models.tarefa import Tarefa
from app.schemas.servico import TarefaCreate, TarefaUpdate


class TarefaRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_etapa(self, etapa_id: int, escritorio_id: int) -> List[Tarefa]:
        """Lista tarefas de uma etapa, garantindo que pertencem ao escritório"""
        return self.db.query(Tarefa).filter(
            Tarefa.etapa_id == etapa_id,
            Tarefa.escritorio_id == escritorio_id
        ).order_by(Tarefa.ordem, Tarefa.id).all()
    
    def get_by_id(self, tarefa_id: int, escritorio_id: int) -> Optional[Tarefa]:
        """Busca tarefa por ID, garantindo que pertence ao escritório"""
        return self.db.query(Tarefa).filter(
            Tarefa.id == tarefa_id,
            Tarefa.escritorio_id == escritorio_id
        ).first()
    
    def get_all(self, escritorio_id: int, etapa_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[Tarefa]:
        """Lista todas as tarefas, opcionalmente filtradas por etapa, isoladas por escritório"""
        query = self.db.query(Tarefa).filter(Tarefa.escritorio_id == escritorio_id)
        
        if etapa_id:
            query = query.filter(Tarefa.etapa_id == etapa_id)
        
        return query.order_by(Tarefa.ordem, Tarefa.id).offset(skip).limit(limit).all()
    
    def create(self, etapa_id: int, tarefa_data: TarefaCreate, escritorio_id: int) -> Tarefa:
        """Cria nova tarefa, vinculada à etapa e ao escritório"""
        tarefa_dict = tarefa_data.model_dump()
        tarefa_dict['escritorio_id'] = escritorio_id
        tarefa = Tarefa(**tarefa_dict, etapa_id=etapa_id)
        self.db.add(tarefa)
        self.db.commit()
        self.db.refresh(tarefa)
        return tarefa
    
    def update(self, tarefa_id: int, tarefa_data: TarefaUpdate, escritorio_id: int) -> Optional[Tarefa]:
        """Atualiza tarefa, garantindo que pertence ao escritório"""
        tarefa = self.get_by_id(tarefa_id, escritorio_id)
        if not tarefa:
            return None
        
        update_data = tarefa_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(tarefa, field, value)
        
        self.db.commit()
        self.db.refresh(tarefa)
        return tarefa
    
    def delete(self, tarefa_id: int, escritorio_id: int) -> bool:
        """Deleta tarefa, garantindo que pertence ao escritório"""
        tarefa = self.get_by_id(tarefa_id, escritorio_id)
        if not tarefa:
            return False
        
        self.db.delete(tarefa)
        self.db.commit()
        return True
    
    def count(self, escritorio_id: int, etapa_id: Optional[int] = None) -> int:
        """Conta tarefas, opcionalmente filtradas por etapa, isoladas por escritório"""
        query = self.db.query(Tarefa).filter(Tarefa.escritorio_id == escritorio_id)
        if etapa_id:
            query = query.filter(Tarefa.etapa_id == etapa_id)
        return query.count()
    
    def search(self, escritorio_id: int, search_term: str, etapa_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[Tarefa]:
        """Busca tarefas por termo, opcionalmente filtradas por etapa, isoladas por escritório"""
        query = self.db.query(Tarefa).filter(
            Tarefa.escritorio_id == escritorio_id,
            Tarefa.nome.ilike(f"%{search_term}%")
        )
        
        if etapa_id:
            query = query.filter(Tarefa.etapa_id == etapa_id)
        
        return query.order_by(Tarefa.ordem, Tarefa.id).offset(skip).limit(limit).all()


