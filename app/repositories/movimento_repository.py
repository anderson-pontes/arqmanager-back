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
        escritorio_id: int,
        skip: int = 0, 
        limit: int = 100,
        tipo: Optional[int] = None,
        projeto_id: Optional[int] = None,
        data_inicio: Optional[date] = None,
        data_fim: Optional[date] = None,
        ativo: Optional[bool] = None
    ) -> List[Movimento]:
        """Lista todos os movimentos com filtros, isolados por escritório"""
        query = self.db.query(Movimento).filter(Movimento.escritorio_id == escritorio_id).options(joinedload(Movimento.projeto))
        
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
    
    def get_by_id(self, movimento_id: int, escritorio_id: int) -> Optional[Movimento]:
        """Busca movimento por ID, garantindo que pertence ao escritório"""
        return self.db.query(Movimento).options(
            joinedload(Movimento.projeto)
        ).filter(
            Movimento.id == movimento_id,
            Movimento.escritorio_id == escritorio_id
        ).first()
    
    def create(self, movimento_data: MovimentoCreate, escritorio_id: int) -> Movimento:
        """Cria novo movimento, vinculado ao escritório"""
        movimento_dict = movimento_data.model_dump()
        movimento_dict['escritorio_id'] = escritorio_id
        movimento = Movimento(**movimento_dict)
        self.db.add(movimento)
        self.db.commit()
        self.db.refresh(movimento)
        return movimento
    
    def update(self, movimento_id: int, movimento_data: MovimentoUpdate, escritorio_id: int) -> Optional[Movimento]:
        """Atualiza movimento, garantindo que pertence ao escritório"""
        movimento = self.get_by_id(movimento_id, escritorio_id)
        if not movimento:
            return None
        
        update_data = movimento_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(movimento, field, value)
        
        self.db.commit()
        self.db.refresh(movimento)
        return movimento
    
    def delete(self, movimento_id: int, escritorio_id: int) -> bool:
        """Remove movimento, garantindo que pertence ao escritório"""
        movimento = self.get_by_id(movimento_id, escritorio_id)
        if not movimento:
            return False
        
        self.db.delete(movimento)
        self.db.commit()
        return True
    
    def get_resumo(
        self,
        escritorio_id: int,
        data_inicio: Optional[date] = None,
        data_fim: Optional[date] = None,
        tipo: Optional[int] = None
    ) -> dict:
        """Retorna resumo financeiro, isolado por escritório"""
        query = self.db.query(
            func.sum(Movimento.valor).label('total')
        ).filter(
            Movimento.ativo == True,
            Movimento.escritorio_id == escritorio_id
        )
        
        if data_inicio:
            query = query.filter(Movimento.data_entrada >= data_inicio)
        
        if data_fim:
            query = query.filter(Movimento.data_entrada <= data_fim)
        
        if tipo:
            query = query.filter(Movimento.tipo == tipo)
        
        result = query.first()
        return {"total": float(result.total) if result.total else 0.0}
    
    def get_por_mes(self, escritorio_id: int, ano: int, mes: int) -> List[Movimento]:
        """Retorna movimentos de um mês específico, isolados por escritório"""
        return self.db.query(Movimento).filter(
            Movimento.escritorio_id == escritorio_id,
            extract('year', Movimento.data_entrada) == ano,
            extract('month', Movimento.data_entrada) == mes,
            Movimento.ativo == True
        ).order_by(Movimento.data_entrada).all()
