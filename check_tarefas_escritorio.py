"""Script para verificar tarefas de um escritório"""
from sqlalchemy import text
from app.database import engine

def check_tarefas_escritorio(escritorio_id: int):
    """Verifica tarefas de um escritório específico"""
    
    with engine.connect() as conn:
        # Verificar informações do escritório
        result = conn.execute(text("""
            SELECT id, nome_fantasia, razao_social
            FROM escritorio
            WHERE id = :escritorio_id
        """), {'escritorio_id': escritorio_id})
        
        escritorio = result.first()
        if not escritorio:
            print(f"ERRO: Escritorio {escritorio_id} nao encontrado!")
            return
        
        print(f"Escritorio: {escritorio[1]} (ID: {escritorio[0]})")
        print("=" * 60)
        
        # Contar serviços
        result = conn.execute(text("""
            SELECT COUNT(*) FROM servicos WHERE escritorio_id = :escritorio_id
        """), {'escritorio_id': escritorio_id})
        total_servicos = result.scalar()
        print(f"\nServicos: {total_servicos}")
        
        # Contar etapas
        result = conn.execute(text("""
            SELECT COUNT(*) FROM etapas WHERE escritorio_id = :escritorio_id
        """), {'escritorio_id': escritorio_id})
        total_etapas = result.scalar()
        print(f"Etapas: {total_etapas}")
        
        # Contar tarefas
        result = conn.execute(text("""
            SELECT COUNT(*) FROM tarefas WHERE escritorio_id = :escritorio_id
        """), {'escritorio_id': escritorio_id})
        total_tarefas = result.scalar()
        print(f"Tarefas: {total_tarefas}")
        
        # Listar serviços com suas etapas e tarefas
        print("\n" + "=" * 60)
        print("Detalhamento por Servico:")
        print("=" * 60)
        
        result = conn.execute(text("""
            SELECT id, nome, descricao
            FROM servicos
            WHERE escritorio_id = :escritorio_id
            ORDER BY id
        """), {'escritorio_id': escritorio_id})
        
        servicos = list(result)
        
        for servico in servicos:
            servico_id = servico[0]
            servico_nome = servico[1]
            
            print(f"\nServico: {servico_nome} (ID: {servico_id})")
            
            # Buscar etapas deste serviço
            result = conn.execute(text("""
                SELECT id, nome, ordem
                FROM etapas
                WHERE servico_id = :servico_id AND escritorio_id = :escritorio_id
                ORDER BY ordem
            """), {'servico_id': servico_id, 'escritorio_id': escritorio_id})
            
            etapas = list(result)
            
            if not etapas:
                print("  AVISO: Nenhuma etapa encontrada")
                continue
            
            for etapa in etapas:
                etapa_id = etapa[0]
                etapa_nome = etapa[1]
                etapa_ordem = etapa[2]
                
                print(f"  - Etapa {etapa_ordem}: {etapa_nome} (ID: {etapa_id})")
                
                # Buscar tarefas desta etapa
                result = conn.execute(text("""
                    SELECT id, nome, ordem, cor, tem_prazo, precisa_detalhamento
                    FROM tarefas
                    WHERE etapa_id = :etapa_id AND escritorio_id = :escritorio_id
                    ORDER BY ordem
                """), {'etapa_id': etapa_id, 'escritorio_id': escritorio_id})
                
                tarefas = list(result)
                
                if not tarefas:
                    print(f"      AVISO: Nenhuma tarefa encontrada")
                else:
                    for tarefa in tarefas:
                        tarefa_id = tarefa[0]
                        tarefa_nome = tarefa[1]
                        tarefa_ordem = tarefa[2]
                        tarefa_cor = tarefa[3] or 'sem cor'
                        tarefa_prazo = 'Sim' if tarefa[4] else 'Nao'
                        tarefa_detalhe = 'Sim' if tarefa[5] else 'Nao'
                        
                        print(f"      - Tarefa {tarefa_ordem}: {tarefa_nome} (ID: {tarefa_id})")
                        print(f"        Cor: {tarefa_cor} | Prazo: {tarefa_prazo} | Detalhamento: {tarefa_detalhe}")
        
        print("\n" + "=" * 60)
        print(f"Resumo: {total_servicos} servicos, {total_etapas} etapas, {total_tarefas} tarefas")
        print("=" * 60)

if __name__ == "__main__":
    check_tarefas_escritorio(1)

