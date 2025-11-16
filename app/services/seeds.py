"""
Sistema de Seeds para dados iniciais por escritório
Cria dados básicos quando um novo escritório é criado
"""
from sqlalchemy.orm import Session
from app.models.status import Status
from app.models.servico import Servico
from app.models.etapa import Etapa
from app.models.forma_pagamento import FormaPagamento
from app.models.feriado import Feriado
from datetime import date
from typing import List


class EscritorioSeeds:
    """Classe para criar seeds de dados iniciais para um escritório"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def criar_status_padrao(self, escritorio_id: int) -> List[Status]:
        """Cria status padrão para o escritório"""
        status_padrao = [
            {"descricao": "Em Andamento", "cor": "#3b82f6", "ativo": True},
            {"descricao": "Concluído", "cor": "#10b981", "ativo": True},
            {"descricao": "Pendente", "cor": "#f59e0b", "ativo": True},
            {"descricao": "Cancelado", "cor": "#ef4444", "ativo": True},
            {"descricao": "Pausado", "cor": "#6b7280", "ativo": True},
        ]
        
        status_criados = []
        for status_data in status_padrao:
            status = Status(
                descricao=status_data["descricao"],
                cor=status_data["cor"],
                ativo=status_data["ativo"],
                escritorio_id=escritorio_id
            )
            self.db.add(status)
            status_criados.append(status)
        
        self.db.flush()
        return status_criados
    
    def criar_formas_pagamento_padrao(self, escritorio_id: int) -> List[FormaPagamento]:
        """Cria formas de pagamento padrão para o escritório"""
        formas_padrao = [
            {"descricao": "Dinheiro", "ativo": True},
            {"descricao": "PIX", "ativo": True},
            {"descricao": "Cartão de Crédito", "ativo": True},
            {"descricao": "Cartão de Débito", "ativo": True},
            {"descricao": "Boleto Bancário", "ativo": True},
            {"descricao": "Transferência Bancária", "ativo": True},
            {"descricao": "Cheque", "ativo": True},
        ]
        
        formas_criadas = []
        for forma_data in formas_padrao:
            forma = FormaPagamento(
                descricao=forma_data["descricao"],
                ativo=forma_data["ativo"],
                escritorio_id=escritorio_id
            )
            self.db.add(forma)
            formas_criadas.append(forma)
        
        self.db.flush()
        return formas_criadas
    
    def criar_feriados_nacionais(self, escritorio_id: int, ano: int = None) -> List[Feriado]:
        """Cria feriados nacionais para o escritório"""
        if ano is None:
            ano = date.today().year
        
        feriados_nacionais = [
            {"data": date(ano, 1, 1), "descricao": "Confraternização Universal", "tipo": "nacional"},
            {"data": date(ano, 4, 21), "descricao": "Tiradentes", "tipo": "nacional"},
            {"data": date(ano, 5, 1), "descricao": "Dia do Trabalhador", "tipo": "nacional"},
            {"data": date(ano, 9, 7), "descricao": "Independência do Brasil", "tipo": "nacional"},
            {"data": date(ano, 10, 12), "descricao": "Nossa Senhora Aparecida", "tipo": "nacional"},
            {"data": date(ano, 11, 2), "descricao": "Finados", "tipo": "nacional"},
            {"data": date(ano, 11, 15), "descricao": "Proclamação da República", "tipo": "nacional"},
            {"data": date(ano, 12, 25), "descricao": "Natal", "tipo": "nacional"},
        ]
        
        feriados_criados = []
        for feriado_data in feriados_nacionais:
            feriado = Feriado(
                data=feriado_data["data"],
                descricao=feriado_data["descricao"],
                tipo=feriado_data["tipo"],
                ativo=True,
                escritorio_id=escritorio_id
            )
            self.db.add(feriado)
            feriados_criados.append(feriado)
        
        self.db.flush()
        return feriados_criados
    
    def criar_servicos_basicos(self, escritorio_id: int) -> List[Servico]:
        """Cria serviços básicos para o escritório (opcional)"""
        # Por enquanto, não criamos serviços automáticos
        # Cada escritório pode criar seus próprios serviços
        return []
    
    def criar_todos_seeds(self, escritorio_id: int, ano: int = None) -> dict:
        """
        Cria todos os seeds para um escritório
        
        Args:
            escritorio_id: ID do escritório
            ano: Ano para os feriados (padrão: ano atual)
        
        Returns:
            Dict com todos os dados criados
        """
        if ano is None:
            ano = date.today().year
        
        status = self.criar_status_padrao(escritorio_id)
        formas_pagamento = self.criar_formas_pagamento_padrao(escritorio_id)
        feriados = self.criar_feriados_nacionais(escritorio_id, ano)
        servicos = self.criar_servicos_basicos(escritorio_id)
        
        self.db.commit()
        
        return {
            "status": len(status),
            "formas_pagamento": len(formas_pagamento),
            "feriados": len(feriados),
            "servicos": len(servicos)
        }










