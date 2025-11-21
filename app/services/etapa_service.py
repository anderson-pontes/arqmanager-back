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
        
        # Validar nome obrigatório
        if not etapa_data.nome or not etapa_data.nome.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nome da etapa é obrigatório"
            )
        
        # Validar tamanho do nome
        if len(etapa_data.nome) > 500:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nome da etapa não pode ter mais de 500 caracteres"
            )
        
        # Validar ordem numérica
        if etapa_data.ordem is not None and etapa_data.ordem < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ordem deve ser um número positivo ou zero"
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
    
    def reordenar_etapas(
        self,
        servico_id: int,
        etapa_ids: List[int],
        escritorio_id: int
    ) -> List[Etapa]:
        """
        Reordena etapas de um serviço em lote
        Recebe uma lista de IDs na nova ordem e atualiza o campo ordem de cada etapa
        """
        # Validar se serviço existe e pertence ao escritório
        servico = self.servico_repo.get_by_id(servico_id, escritorio_id)
        if not servico:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Serviço não encontrado"
            )
        
        # Validar se todas as etapas pertencem ao serviço e escritório
        etapas = self.etapa_repo.get_by_servico(servico_id, escritorio_id)
        etapa_ids_existentes = {etapa.id for etapa in etapas}
        
        if len(etapa_ids) != len(etapa_ids_existentes):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Número de etapas não corresponde ao esperado"
            )
        
        for etapa_id in etapa_ids:
            if etapa_id not in etapa_ids_existentes:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Etapa {etapa_id} não pertence ao serviço {servico_id}"
                )
        
        # Atualizar ordem de cada etapa
        etapas_atualizadas = []
        for ordem, etapa_id in enumerate(etapa_ids):
            etapa = self.etapa_repo.get_by_id(etapa_id, escritorio_id)
            if etapa:
                etapa_atualizada = self.etapa_repo.update(
                    etapa_id,
                    EtapaUpdate(ordem=ordem),
                    escritorio_id
                )
                if etapa_atualizada:
                    etapas_atualizadas.append(etapa_atualizada)
        
        return etapas_atualizadas


