"""
Script para excluir todos os serviços, etapas e tarefas do banco de dados
"""
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import text
from app.database import SessionLocal
from app.models.servico import Servico
from app.models.etapa import Etapa
from app.models.tarefa import Tarefa
from app.models.proposta_servico_etapa import PropostaServicoEtapa

def limpar_servicos_etapas_tarefas():
    """Exclui todos os serviços, etapas e tarefas do banco de dados"""
    db = SessionLocal()
    
    try:
        print("=" * 60)
        print("LIMPEZA DE SERVIÇOS, ETAPAS E TAREFAS")
        print("=" * 60)
        
        # Contar registros antes
        count_tarefas = db.query(Tarefa).count()
        count_etapas = db.query(Etapa).count()
        count_servicos = db.query(Servico).count()
        count_proposta_etapas = db.query(PropostaServicoEtapa).count()
        
        print(f"\nRegistros encontrados:")
        print(f"  - Tarefas: {count_tarefas}")
        print(f"  - Etapas: {count_etapas}")
        print(f"  - Servicos: {count_servicos}")
        print(f"  - Referencias em proposta_servico_etapa: {count_proposta_etapas}")
        
        if count_tarefas == 0 and count_etapas == 0 and count_servicos == 0:
            print("\n[OK] Nenhum registro encontrado. Nada a excluir.")
            return
        
        # Confirmar exclusão (aceitar argumento de linha de comando)
        print("\n" + "=" * 60)
        print("ATENCAO: Esta acao ira excluir TODOS os registros!")
        
        # Verificar se foi passado argumento --confirm ou --force
        confirmar = len(sys.argv) > 1 and sys.argv[1] == '--confirm'
        force = len(sys.argv) > 1 and sys.argv[1] == '--force'
        
        if not confirmar and not force:
            print("\nPara executar, use:")
            print("  python limpar_servicos_etapas_tarefas.py --confirm  (exclui apenas sem referencias)")
            print("  python limpar_servicos_etapas_tarefas.py --force    (exclui TUDO, incluindo referencias)")
            return
        
        print("\n[INFO] Excluindo registros...")
        
        # Usar SQL direto para excluir na ordem correta
        # Excluir referências primeiro, depois as tabelas principais
        
        # 1. Excluir referências em proposta_servico_etapa primeiro
        count_proposta_etapas = db.query(PropostaServicoEtapa).count()
        if count_proposta_etapas > 0:
            db.execute(text("DELETE FROM proposta_servico_etapa"))
            print(f"  [OK] {count_proposta_etapas} referencia(s) em proposta_servico_etapa excluida(s)")
        
        # 2. Tarefas (já tem CASCADE na FK, mas vamos excluir explicitamente)
        if count_tarefas > 0:
            db.execute(text("DELETE FROM tarefas"))
            print(f"  [OK] {count_tarefas} tarefa(s) excluida(s)")
        
        # 3. Etapas
        if count_etapas > 0:
            db.execute(text("DELETE FROM etapas"))
            print(f"  [OK] {count_etapas} etapa(s) excluida(s)")
        
        # 4. Serviços (excluir apenas os que não têm referências em projetos/propostas)
        # Primeiro, vamos contar quantos podem ser excluídos
        result = db.execute(text("""
            SELECT COUNT(*) FROM servicos s
            WHERE NOT EXISTS (
                SELECT 1 FROM projetos p WHERE p.servico_id = s.id
            )
            AND NOT EXISTS (
                SELECT 1 FROM propostas pr WHERE pr.servico_id = s.id
            )
        """))
        servicos_sem_ref = result.scalar() or 0
        
        if servicos_sem_ref > 0:
            db.execute(text("""
                DELETE FROM servicos
                WHERE id NOT IN (
                    SELECT DISTINCT servico_id FROM projetos WHERE servico_id IS NOT NULL
                    UNION
                    SELECT DISTINCT servico_id FROM propostas WHERE servico_id IS NOT NULL
                )
            """))
            print(f"  [OK] {servicos_sem_ref} servico(s) excluido(s) (sem referencias em projetos/propostas)")
        
        # Verificar se ainda há serviços com referências
        result = db.execute(text("""
            SELECT COUNT(*) FROM servicos s
            WHERE EXISTS (
                SELECT 1 FROM projetos p WHERE p.servico_id = s.id
            )
            OR EXISTS (
                SELECT 1 FROM propostas pr WHERE pr.servico_id = s.id
            )
        """))
        servicos_com_ref = result.scalar() or 0
        
        if servicos_com_ref > 0:
            if force:
                # Modo force: excluir todas as dependências em cascata
                print(f"  [INFO] Modo FORCE ativado. Removendo todas as referencias...")
                
                # Identificar projetos que referenciam serviços
                result = db.execute(text("SELECT id FROM projetos WHERE servico_id IS NOT NULL"))
                projeto_ids = [row[0] for row in result]
                
                if projeto_ids:
                    print(f"  [INFO] Encontrados {len(projeto_ids)} projeto(s) com referencia a servicos")
                    
                    # Excluir todas as dependências dos projetos em ordem
                    # 1. projeto_pagamento
                    db.execute(text(f"DELETE FROM projeto_pagamento WHERE projeto_id IN ({','.join(map(str, projeto_ids))})"))
                    print(f"  [OK] Referencias em projeto_pagamento excluidas")
                    
                    # 2. projeto_colaborador
                    db.execute(text(f"DELETE FROM projeto_colaborador WHERE projeto_id IN ({','.join(map(str, projeto_ids))})"))
                    print(f"  [OK] Referencias em projeto_colaborador excluidas")
                    
                    # 3. projeto_documento
                    db.execute(text(f"DELETE FROM projeto_documento WHERE projeto_id IN ({','.join(map(str, projeto_ids))})"))
                    print(f"  [OK] Referencias em projeto_documento excluidas")
                    
                    # 4. movimentos
                    db.execute(text(f"DELETE FROM movimentos WHERE projeto_id IN ({','.join(map(str, projeto_ids))})"))
                    print(f"  [OK] Referencias em movimentos excluidas")
                    
                    # 5. projeto_arquivamento
                    db.execute(text(f"DELETE FROM projeto_arquivamento WHERE projeto_id IN ({','.join(map(str, projeto_ids))})"))
                    print(f"  [OK] Referencias em projeto_arquivamento excluidas")
                    
                    # 6. Agora excluir os projetos
                    db.execute(text(f"DELETE FROM projetos WHERE id IN ({','.join(map(str, projeto_ids))})"))
                    print(f"  [OK] {len(projeto_ids)} projeto(s) excluido(s)")
                
                # Contar e remover referências em propostas
                result = db.execute(text("SELECT COUNT(*) FROM propostas WHERE servico_id IS NOT NULL"))
                count_prop_refs = result.scalar() or 0
                if count_prop_refs > 0:
                    db.execute(text("DELETE FROM propostas WHERE servico_id IS NOT NULL"))
                    print(f"  [OK] {count_prop_refs} proposta(s) excluida(s) (tinham referencia a servicos)")
                
                # Agora excluir os serviços restantes
                result = db.execute(text("SELECT COUNT(*) FROM servicos"))
                count_restantes = result.scalar() or 0
                if count_restantes > 0:
                    db.execute(text("DELETE FROM servicos"))
                    print(f"  [OK] {count_restantes} servico(s) restante(s) excluido(s)")
            else:
                print(f"  [AVISO] {servicos_com_ref} servico(s) nao podem ser excluidos porque tem referencias em projetos ou propostas")
                print(f"  [INFO] Use --force para excluir TUDO (incluindo projetos/propostas que referenciam servicos)")
        
        # Commit das alterações
        db.commit()
        
        print("\n" + "=" * 60)
        print("[OK] Limpeza concluida com sucesso!")
        print("=" * 60)
        
        # Verificar se realmente foram excluídos
        count_tarefas_final = db.query(Tarefa).count()
        count_etapas_final = db.query(Etapa).count()
        count_servicos_final = db.query(Servico).count()
        
        print(f"\nRegistros restantes:")
        print(f"  - Tarefas: {count_tarefas_final}")
        print(f"  - Etapas: {count_etapas_final}")
        print(f"  - Serviços: {count_servicos_final}")
        
    except Exception as e:
        db.rollback()
        print(f"\n[ERRO] ERRO ao excluir registros: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    limpar_servicos_etapas_tarefas()

