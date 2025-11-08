"""
Repositório de Movimentos Financeiros
"""
from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, extract
from app.models.movimento import Movimento
from app.schemas.movimento import MovimentoCreate, MovimentoUpdate


class MovimentoRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(
        self, 
        skip: int = 0, 
        limit: int = 100,
        tipo: Optional[int] = None,
        projeto_id: Optional[int] = None,
        data_inicio: Optional[date] = None,
        data_fim: Optional[date] = None,
        ativo: Optional[bool] = None
    ) -> List[Movimento]:
        query = self.db.query(Movimento).options(joinedload(Movimento.projeto))
        
        if tipo:
            query = query.filter(Movimento.tipo == tipo)
        
        if projeto_id:
            query = query.filter(Movimento.projeto_id == projeto_id)
        
        if data_inicio:
            query = query.filter(Movimento.data_entrada >= data_inicio)
        
        if data_fim:
            query = query.filter(Movimento.data_entrada <= data_fim)
        
        if ativo is not None:
            query = query.filter(Movimento.ativo == ativo)
        
        return query.order_by(Movimento.data_entrada.desc()).offset(skip).limit(limit).all()
    
    def get_by_id(self, movimento_id: int) -> Optional[Movimento]:
        return self.db.query(Movimento).options(
            joinedload(Movimento.projeto)
        ).filter(Movimento.id == movimento_id).first()
    
    def create(self, movimento_data: MovimentoCreate) -> Movimento:
        movimento = Movimento(**movimento_data.model_dump())
        self.db.add(movimento)
        self.db.commit()
        self.db.refresh(movimento)
        return movimento
    
    def update(self, movimento_id: int, movimento_data: MovimentoUpdate) -> Optional[Movimento]:
        movimento = self.get_by_id(movimento_id)
        if not movimento:
            return None
        
        update_data = movimento_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(movimento, field, value)
        
        self.db.commit()
        self.db.refresh(movimento)
        return movimento
    
    def delete(self, movimento_id: int) -> bool:
        movimento = self.get_by_id(movimento_id)
        if not movimento:
            return False
        
        self.db.delete(movimento)
        self.db.commit()
        return True
    
    def get_resumo(
        self,
        data_inicio: Optional[date] = None,
        data_fim: Optional[date] = None,
        tipo: Optional[int] = None
    ) -> dict:
        """Retorna resumo financeiro"""
        query = self.db.query(
            func.sum(Movimento.valor).label('total')
        ).filter(Movimento.ativo == True)
        
        if data_inicio:
            query = query.filter(Movimento.data_entrada >= data_inicio)
        
        if data_fim:
            query = query.filter(Movimento.data_entrada <= data_fim)
        
        if tipo:
            query = query.filter(Movimento.tipo == tipo)
        
        result = query.first()
        return {"total": float(result.total) if result.total else 0.0}
    
    def get_por_mes(self, ano: int, mes: int) -> List[Movimento]:
        """Retorna movimentos de um mês específico"""
        return self.db.query(Movimento).filter(
            extract('year', Movimento.data_entrada) == ano,
            extract('month', Movimento.data_entrada) == mes,
            Movimento.ativo == True
        ).order_by(Movimento.data_entrada).all()
