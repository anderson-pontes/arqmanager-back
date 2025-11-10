"""
Repositório de Projetos
"""
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models.projeto import Projeto
from app.models.projeto_colaborador import ProjetoColaborador
from app.schemas.projeto import ProjetoCreate, ProjetoUpdate


class ProjetoRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(
        self,
        escritorio_id: int,
        skip: int = 0, 
        limit: int = 100, 
        ativo: Optional[bool] = None,
        cliente_id: Optional[int] = None,
        status_id: Optional[int] = None
    ) -> List[Projeto]:
        """Lista todos os projetos com filtros, isolados por escritório"""
        query = self.db.query(Projeto).filter(Projeto.escritorio_id == escritorio_id).options(
            joinedload(Projeto.cliente),
            joinedload(Projeto.servico),
            joinedload(Projeto.status),
            joinedload(Projeto.colaboradores)
        )
        
        if ativo is not None:
            query = query.filter(Projeto.ativo == ativo)
        
        if cliente_id:
            query = query.filter(Projeto.cliente_id == cliente_id)
        
        if status_id:
            query = query.filter(Projeto.status_id == status_id)
        
        return query.offset(skip).limit(limit).all()
    
    def get_by_id(self, projeto_id: int, escritorio_id: int) -> Optional[Projeto]:
        """Busca projeto por ID, garantindo que pertence ao escritório"""
        return self.db.query(Projeto).options(
            joinedload(Projeto.cliente),
            joinedload(Projeto.servico),
            joinedload(Projeto.status),
            joinedload(Projeto.colaboradores)
        ).filter(
            Projeto.id == projeto_id,
            Projeto.escritorio_id == escritorio_id
        ).first()
    
    def create(self, projeto_data: ProjetoCreate, escritorio_id: int) -> Projeto:
        """Cria novo projeto, vinculado ao escritório"""
        # Criar projeto
        projeto_dict = projeto_data.model_dump(exclude={"colaboradores"})
        projeto_dict['escritorio_id'] = escritorio_id
        projeto = Projeto(**projeto_dict)
        
        # Adicionar colaboradores
        if projeto_data.colaboradores:
            for colab_data in projeto_data.colaboradores:
                colab_dict = colab_data.model_dump()
                colab_dict['escritorio_id'] = escritorio_id
                colab = ProjetoColaborador(**colab_dict, projeto=projeto)
                projeto.colaboradores.append(colab)
        
        self.db.add(projeto)
        self.db.commit()
        self.db.refresh(projeto)
        return projeto
    
    def update(self, projeto_id: int, projeto_data: ProjetoUpdate, escritorio_id: int) -> Optional[Projeto]:
        """Atualiza projeto, garantindo que pertence ao escritório"""
        projeto = self.get_by_id(projeto_id, escritorio_id)
        if not projeto:
            return None
        
        update_data = projeto_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(projeto, field, value)
        
        self.db.commit()
        self.db.refresh(projeto)
        return projeto
    
    def delete(self, projeto_id: int, escritorio_id: int) -> bool:
        """Remove projeto, garantindo que pertence ao escritório"""
        projeto = self.get_by_id(projeto_id, escritorio_id)
        if not projeto:
            return False
        
        self.db.delete(projeto)
        self.db.commit()
        return True
    
    def count(
        self,
        escritorio_id: int,
        ativo: Optional[bool] = None,
        cliente_id: Optional[int] = None,
        status_id: Optional[int] = None
    ) -> int:
        """Conta total de projetos com filtros, isolados por escritório"""
        query = self.db.query(Projeto).filter(Projeto.escritorio_id == escritorio_id)
        
        if ativo is not None:
            query = query.filter(Projeto.ativo == ativo)
        
        if cliente_id:
            query = query.filter(Projeto.cliente_id == cliente_id)
        
        if status_id:
            query = query.filter(Projeto.status_id == status_id)
        
        return query.count()
    
    def search(self, escritorio_id: int, search_term: str, skip: int = 0, limit: int = 100) -> List[Projeto]:
        """Busca projetos por termo, isolados por escritório"""
        return self.db.query(Projeto).options(
            joinedload(Projeto.cliente),
            joinedload(Projeto.servico),
            joinedload(Projeto.status)
        ).filter(
            Projeto.escritorio_id == escritorio_id,
            Projeto.descricao.ilike(f"%{search_term}%")
        ).offset(skip).limit(limit).all()
    
    # Métodos para colaboradores
    def add_colaborador(self, projeto_id: int, colaborador_id: int, escritorio_id: int, funcao: Optional[str] = None) -> Optional[ProjetoColaborador]:
        """Adiciona colaborador ao projeto, garantindo que pertence ao escritório"""
        projeto = self.get_by_id(projeto_id, escritorio_id)
        if not projeto:
            return None
        
        colab = ProjetoColaborador(
            projeto_id=projeto_id,
            colaborador_id=colaborador_id,
            funcao=funcao,
            escritorio_id=escritorio_id
        )
        self.db.add(colab)
        self.db.commit()
        self.db.refresh(colab)
        return colab
    
    def remove_colaborador(self, projeto_id: int, colaborador_id: int, escritorio_id: int) -> bool:
        """Remove colaborador do projeto, garantindo que pertence ao escritório"""
        colab = self.db.query(ProjetoColaborador).filter(
            ProjetoColaborador.projeto_id == projeto_id,
            ProjetoColaborador.colaborador_id == colaborador_id,
            ProjetoColaborador.escritorio_id == escritorio_id
        ).first()
        
        if not colab:
            return False
        
        self.db.delete(colab)
        self.db.commit()
        return True
