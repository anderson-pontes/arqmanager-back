"""
Service de Serviços - Lógica de negócio
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.servico_repository import ServicoRepository
from app.repositories.etapa_repository import EtapaRepository
from app.schemas.servico import ServicoCreate, ServicoUpdate
from app.models.servico import Servico


class ServicoService:
    def __init__(self, db: Session):
        self.db = db
        self.servico_repo = ServicoRepository(db)
        self.etapa_repo = EtapaRepository(db)
    
    def listar_servicos(
        self, 
        escritorio_id: int,
        skip: int = 0, 
        limit: int = 100,
        ativo: Optional[bool] = None,
        search: Optional[str] = None
    ) -> List[Servico]:
        """Lista serviços com filtros opcionais"""
        if search:
            return self.servico_repo.search(escritorio_id, search, skip, limit)
        return self.servico_repo.get_all(escritorio_id, skip, limit, ativo)
    
    def obter_servico(self, servico_id: int, escritorio_id: int) -> Servico:
        """Obtém um serviço por ID"""
        servico = self.servico_repo.get_by_id(servico_id, escritorio_id)
        if not servico:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Serviço não encontrado"
            )
        return servico
    
    def criar_servico(
        self, 
        servico_data: ServicoCreate, 
        escritorio_id: int
    ) -> Servico:
        """Cria um novo serviço com validações"""
        # Validar código do plano de contas único por escritório
        if servico_data.codigo_plano_contas:
            servicos_existentes = self.servico_repo.get_all(escritorio_id, 0, 1000)
            for servico in servicos_existentes:
                if servico.codigo_plano_contas == servico_data.codigo_plano_contas:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Código do plano de contas '{servico_data.codigo_plano_contas}' já existe para este escritório"
                    )
        
        return self.servico_repo.create(servico_data, escritorio_id)
    
    def atualizar_servico(
        self, 
        servico_id: int, 
        servico_data: ServicoUpdate, 
        escritorio_id: int
    ) -> Servico:
        """Atualiza um serviço com validações"""
        servico = self.servico_repo.get_by_id(servico_id, escritorio_id)
        if not servico:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Serviço não encontrado"
            )
        
        # Validar código do plano de contas único por escritório (se alterado)
        if servico_data.codigo_plano_contas and servico_data.codigo_plano_contas != servico.codigo_plano_contas:
            servicos_existentes = self.servico_repo.get_all(escritorio_id, 0, 1000)
            for s in servicos_existentes:
                if s.id != servico_id and s.codigo_plano_contas == servico_data.codigo_plano_contas:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Código do plano de contas '{servico_data.codigo_plano_contas}' já existe para este escritório"
                    )
        
        servico_atualizado = self.servico_repo.update(servico_id, servico_data, escritorio_id)
        if not servico_atualizado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Serviço não encontrado"
            )
        return servico_atualizado
    
    def deletar_servico(self, servico_id: int, escritorio_id: int) -> bool:
        """Deleta um serviço - não permite se tiver etapas"""
        servico = self.servico_repo.get_by_id(servico_id, escritorio_id)
        if not servico:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Serviço não encontrado"
            )
        
        # Validar se serviço tem etapas
        etapas = self.etapa_repo.get_by_servico(servico_id, escritorio_id)
        if etapas:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não é possível excluir serviço que possui etapas. Exclua as etapas primeiro."
            )
        
        return self.servico_repo.delete(servico_id, escritorio_id)
    
    def contar_servicos(
        self, 
        escritorio_id: int, 
        ativo: Optional[bool] = None
    ) -> int:
        """Conta serviços"""
        return self.servico_repo.count(escritorio_id, ativo)
    
    def listar_servicos_hierarquia(
        self,
        escritorio_id: int,
        ativo: Optional[bool] = None
    ) -> List[Servico]:
        """Lista serviços com etapas e tarefas aninhadas (hierarquia completa)"""
        from sqlalchemy.orm import joinedload
        from app.models.etapa import Etapa
        from app.models.tarefa import Tarefa
        
        query = self.db.query(Servico).filter(
            Servico.escritorio_id == escritorio_id
        ).options(
            joinedload(Servico.etapas).joinedload(Etapa.tarefas)
        )
        
        if ativo is not None:
            query = query.filter(Servico.ativo == ativo)
        
        # Ordenar por ordem em cada nível
        servicos = query.all()
        
        # Ordenar etapas e tarefas manualmente (garantir ordem correta)
        for servico in servicos:
            if servico.etapas:
                servico.etapas = sorted(servico.etapas, key=lambda e: (e.ordem, e.id))
                for etapa in servico.etapas:
                    if etapa.tarefas:
                        etapa.tarefas = sorted(etapa.tarefas, key=lambda t: (t.ordem, t.id))
        
        return servicos


