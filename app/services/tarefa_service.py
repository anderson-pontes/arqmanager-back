"""
Service de Tarefas - Lógica de negócio
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.tarefa_repository import TarefaRepository
from app.repositories.etapa_repository import EtapaRepository
from app.schemas.servico import TarefaCreate, TarefaUpdate, TarefaResponse
from app.models.tarefa import Tarefa


class TarefaService:
    def __init__(self, db: Session):
        self.db = db
        self.tarefa_repo = TarefaRepository(db)
        self.etapa_repo = EtapaRepository(db)
    
    def listar_tarefas(
        self, 
        escritorio_id: int, 
        etapa_id: Optional[int] = None,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Tarefa]:
        """Lista tarefas, opcionalmente filtradas por etapa"""
        return self.tarefa_repo.get_all(escritorio_id, etapa_id, skip, limit)
    
    def obter_tarefa(self, tarefa_id: int, escritorio_id: int) -> Tarefa:
        """Obtém uma tarefa por ID"""
        tarefa = self.tarefa_repo.get_by_id(tarefa_id, escritorio_id)
        if not tarefa:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tarefa não encontrada"
            )
        return tarefa
    
    def criar_tarefa(
        self, 
        etapa_id: int, 
        tarefa_data: TarefaCreate, 
        escritorio_id: int
    ) -> Tarefa:
        """Cria uma nova tarefa com validações"""
        # Validar se etapa existe e pertence ao escritório
        etapa = self.etapa_repo.get_by_id(etapa_id, escritorio_id)
        if not etapa:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Etapa não encontrada"
            )
        
        # Validar se etapa pertence ao serviço correto
        if etapa.servico_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Etapa inválida"
            )
        
        # Validar cor se fornecida (formato hex)
        if tarefa_data.cor:
            cor = tarefa_data.cor.strip()
            if not cor.startswith('#'):
                cor = '#' + cor
            # Validar formato hex (3 ou 6 dígitos)
            cor_clean = cor[1:]
            if not (len(cor_clean) == 3 or len(cor_clean) == 6):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cor deve estar no formato hexadecimal (#RGB ou #RRGGBB)"
                )
            try:
                int(cor_clean, 16)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cor inválida. Use formato hexadecimal válido"
                )
            tarefa_data.cor = cor
        
        return self.tarefa_repo.create(etapa_id, tarefa_data, escritorio_id)
    
    def atualizar_tarefa(
        self, 
        tarefa_id: int, 
        tarefa_data: TarefaUpdate, 
        escritorio_id: int
    ) -> Tarefa:
        """Atualiza uma tarefa com validações"""
        tarefa = self.tarefa_repo.get_by_id(tarefa_id, escritorio_id)
        if not tarefa:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tarefa não encontrada"
            )
        
        # Validar cor se fornecida
        if tarefa_data.cor is not None:
            cor = tarefa_data.cor.strip()
            if not cor.startswith('#'):
                cor = '#' + cor
            cor_clean = cor[1:]
            if not (len(cor_clean) == 3 or len(cor_clean) == 6):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cor deve estar no formato hexadecimal (#RGB ou #RRGGBB)"
                )
            try:
                int(cor_clean, 16)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cor inválida. Use formato hexadecimal válido"
                )
            tarefa_data.cor = cor
        
        tarefa_atualizada = self.tarefa_repo.update(tarefa_id, tarefa_data, escritorio_id)
        if not tarefa_atualizada:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tarefa não encontrada"
            )
        return tarefa_atualizada
    
    def deletar_tarefa(self, tarefa_id: int, escritorio_id: int) -> bool:
        """Deleta uma tarefa"""
        tarefa = self.tarefa_repo.get_by_id(tarefa_id, escritorio_id)
        if not tarefa:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tarefa não encontrada"
            )
        
        return self.tarefa_repo.delete(tarefa_id, escritorio_id)
    
    def listar_tarefas_por_etapa(
        self, 
        etapa_id: int, 
        escritorio_id: int
    ) -> List[Tarefa]:
        """Lista todas as tarefas de uma etapa"""
        # Validar se etapa existe e pertence ao escritório
        etapa = self.etapa_repo.get_by_id(etapa_id, escritorio_id)
        if not etapa:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Etapa não encontrada"
            )
        
        return self.tarefa_repo.get_by_etapa(etapa_id, escritorio_id)
    
    def contar_tarefas(
        self, 
        escritorio_id: int, 
        etapa_id: Optional[int] = None
    ) -> int:
        """Conta tarefas, opcionalmente filtradas por etapa"""
        return self.tarefa_repo.count(escritorio_id, etapa_id)
    
    def buscar_tarefas(
        self, 
        escritorio_id: int, 
        search_term: str,
        etapa_id: Optional[int] = None,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Tarefa]:
        """Busca tarefas por termo"""
        if not search_term or len(search_term.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Termo de busca não pode ser vazio"
            )
        
        return self.tarefa_repo.search(escritorio_id, search_term, etapa_id, skip, limit)


