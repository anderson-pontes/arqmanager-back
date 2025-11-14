"""
Modelos do banco de dados
"""
from app.models.base import Base
from app.models.user import User
from app.models.cliente import Cliente
from app.models.servico import Servico
from app.models.etapa import Etapa
from app.models.tarefa import Tarefa
from app.models.status import Status
from app.models.projeto import Projeto
from app.models.projeto_colaborador import ProjetoColaborador
from app.models.proposta import Proposta
from app.models.movimento import Movimento

# Novos models - Comentados temporariamente para evitar conflitos
# from app.models.escritorio import Escritorio
# from app.models.colaborador_escritorio import ColaboradorEscritorio
# from app.models.projeto_pagamento import ProjetoPagamento
# from app.models.proposta_servico_etapa import PropostaServicoEtapa
# from app.models.conta_bancaria import ContaBancaria
# from app.models.conta_movimentacao import ContaMovimentacao
# from app.models.plano_contas import PlanoContas
# from app.models.forma_pagamento import FormaPagamento
# from app.models.feriado import Feriado
# from app.models.indicacao import Indicacao
# from app.models.projeto_documento import ProjetoDocumento
# from app.models.acesso_grupo import AcessoGrupo
# from app.models.projeto_arquivamento import ProjetoArquivamento

__all__ = [
    "Base", "User", "Cliente", "Servico", "Etapa", "Tarefa", "Status", "Projeto", 
    "ProjetoColaborador", "Proposta", "Movimento",
    # "Escritorio", "ColaboradorEscritorio", "ProjetoPagamento", "PropostaServicoEtapa",
    # "ContaBancaria", "ContaMovimentacao", "PlanoContas", "FormaPagamento",
    # "Feriado", "Indicacao", "ProjetoDocumento", "AcessoGrupo", "ProjetoArquivamento"
]
