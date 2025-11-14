"""
Service de Etapas - Lógica de negócio
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.etapa_repository import EtapaRepository
from app.repositories.tarefa_repository import TarefaRepository
from app.repositories.servico_repository import ServicoRepository
from app.schemas.servico import EtapaCreate, EtapaUpdate
from app.models.etapa import Etapa


class EtapaService:
    def __init__(self, db: Session):
        self.db = db
        self.etapa_repo = EtapaRepository(db)
        self.tarefa_repo = TarefaRepository(db)
        self.servico_repo = ServicoRepository(db)
    
    def listar_etapas_por_servico(
        self, 
        servico_id: int, 
        escritorio_id: int
    ) -> List[Etapa]:
        """Lista todas as etapas de um serviço"""
        # Validar se serviço existe e pertence ao escritório
        servico = self.servico_repo.get_by_id(servico_id, escritorio_id)
        if not servico:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Serviço não encontrado"
            )
        
        return self.etapa_repo.get_by_servico(servico_id, escritorio_id)
    
    def obter_etapa(self, etapa_id: int, escritorio_id: int) -> Etapa:
        """Obtém uma etapa por ID"""
        etapa = self.etapa_repo.get_by_id(etapa_id, escritorio_id)
        if not etapa:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Etapa não encontrada"
            )
        return etapa
    
    def criar_etapa(
        self, 
        servico_id: int, 
        etapa_data: EtapaCreate, 
        escritorio_id: int
    ) -> Etapa:
        """Cria uma nova etapa com validações"""
        # Validar se serviço existe e pertence ao escritório
        servico = self.servico_repo.get_by_id(servico_id, escritorio_id)
        if not servico:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Serviço não encontrado"
            )
        
        return self.etapa_repo.create(servico_id, etapa_data, escritorio_id)
    
    def atualizar_etapa(
        self, 
        etapa_id: int, 
        etapa_data: EtapaUpdate, 
        escritorio_id: int
    ) -> Etapa:
        """Atualiza uma etapa com validações"""
        etapa = self.etapa_repo.get_by_id(etapa_id, escritorio_id)
        if not etapa:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Etapa não encontrada"
            )
        
        etapa_atualizada = self.etapa_repo.update(etapa_id, etapa_data, escritorio_id)
        if not etapa_atualizada:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Etapa não encontrada"
            )
        return etapa_atualizada
    
    def deletar_etapa(self, etapa_id: int, escritorio_id: int) -> bool:
        """Deleta uma etapa - não permite se tiver tarefas"""
        etapa = self.etapa_repo.get_by_id(etapa_id, escritorio_id)
        if not etapa:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Etapa não encontrada"
            )
        
        # Validar se etapa tem tarefas
        tarefas = self.tarefa_repo.get_by_etapa(etapa_id, escritorio_id)
        if tarefas:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não é possível excluir etapa que possui tarefas. Exclua as tarefas primeiro."
            )
        
        return self.etapa_repo.delete(etapa_id, escritorio_id)


