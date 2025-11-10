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
    
    def get_all(self, escritorio_id: int, skip: int = 0, limit: int = 100, ativo: Optional[bool] = None) -> List[Servico]:
        """Lista todos os serviços, isolados por escritório"""
        query = self.db.query(Servico).filter(Servico.escritorio_id == escritorio_id).options(joinedload(Servico.etapas))
        
        if ativo is not None:
            query = query.filter(Servico.ativo == ativo)
        
        return query.offset(skip).limit(limit).all()
    
    def get_by_id(self, servico_id: int, escritorio_id: int) -> Optional[Servico]:
        """Busca serviço por ID, garantindo que pertence ao escritório"""
        return self.db.query(Servico).options(joinedload(Servico.etapas)).filter(
            Servico.id == servico_id,
            Servico.escritorio_id == escritorio_id
        ).first()
    
    def create(self, servico_data: ServicoCreate, escritorio_id: int) -> Servico:
        """Cria novo serviço, vinculado ao escritório"""
        # Criar serviço
        servico_dict = servico_data.model_dump(exclude={"etapas"})
        servico_dict['escritorio_id'] = escritorio_id
        servico = Servico(**servico_dict)
        
        # Adicionar etapas
        if servico_data.etapas:
            for etapa_data in servico_data.etapas:
                etapa_dict = etapa_data.model_dump()
                etapa_dict['escritorio_id'] = escritorio_id
                etapa = Etapa(**etapa_dict, servico=servico)
                servico.etapas.append(etapa)
        
        self.db.add(servico)
        self.db.commit()
        self.db.refresh(servico)
        return servico
    
    def update(self, servico_id: int, servico_data: ServicoUpdate, escritorio_id: int) -> Optional[Servico]:
        """Atualiza serviço, garantindo que pertence ao escritório"""
        servico = self.get_by_id(servico_id, escritorio_id)
        if not servico:
            return None
        
        update_data = servico_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(servico, field, value)
        
        self.db.commit()
        self.db.refresh(servico)
        return servico
    
    def delete(self, servico_id: int, escritorio_id: int) -> bool:
        """Deleta serviço, garantindo que pertence ao escritório"""
        servico = self.get_by_id(servico_id, escritorio_id)
        if not servico:
            return False
        
        self.db.delete(servico)
        self.db.commit()
        return True
    
    def count(self, escritorio_id: int, ativo: Optional[bool] = None) -> int:
        """Conta serviços, isolados por escritório"""
        query = self.db.query(Servico).filter(Servico.escritorio_id == escritorio_id)
        if ativo is not None:
            query = query.filter(Servico.ativo == ativo)
        return query.count()
    
    def search(self, escritorio_id: int, search_term: str, skip: int = 0, limit: int = 100) -> List[Servico]:
        """Busca serviços, isolados por escritório"""
        return self.db.query(Servico).filter(
            Servico.escritorio_id == escritorio_id,
            Servico.nome.ilike(f"%{search_term}%")
        ).options(joinedload(Servico.etapas)).offset(skip).limit(limit).all()
