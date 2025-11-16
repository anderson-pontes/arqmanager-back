"""Script para associar serviços a TODOS os escritórios"""
from sqlalchemy import text
from app.database import engine

def associate_servicos_to_all_escritorios():
    """Associa cada serviço a todos os escritórios (duplicando se necessário)"""
    
    with engine.connect() as conn:
        # Buscar todos os escritórios
        result = conn.execute(text("SELECT id, nome_fantasia FROM escritorio ORDER BY id"))
        escritorios = [(row[0], row[1]) for row in result]
        
        if not escritorios:
            print("ERRO: Nenhum escritorio encontrado!")
            return
        
        print(f"Encontrados {len(escritorios)} escritorios:")
        for esc_id, esc_nome in escritorios:
            print(f"  - ID {esc_id}: {esc_nome}")
        
        # Buscar todos os serviços do primeiro escritório (que já foram migrados)
        result = conn.execute(text("""
            SELECT id, nome, descricao, codigo_plano_contas, ativo
            FROM servicos
            WHERE escritorio_id = 1
        """))
        servicos = list(result)
        
        if not servicos:
            print("\nNenhum servico encontrado no escritorio 1.")
            return
        
        print(f"\nEncontrados {len(servicos)} servicos no escritorio 1.")
        print("Associando servicos a TODOS os escritorios...")
        
        total_criados = 0
        
        # Para cada escritório (exceto o primeiro, que já tem)
        for esc_id, esc_nome in escritorios[1:]:
            print(f"\nProcessando escritorio {esc_id} ({esc_nome})...")
            
            for servico in servicos:
                servico_id_original = servico[0]
                nome = servico[1]
                descricao = servico[2]
                codigo_plano_contas = servico[3]
                ativo = servico[4]
                
                # Verificar se já existe este serviço para este escritório
                result = conn.execute(text("""
                    SELECT id FROM servicos 
                    WHERE nome = :nome AND escritorio_id = :escritorio_id
                """), {'nome': nome, 'escritorio_id': esc_id})
                
                if result.first():
                    # Já existe, pular
                    continue
                
                # Criar novo serviço para este escritório
                # Usar um ID maior para não conflitar (ou deixar o banco gerar)
                result = conn.execute(text("""
                    INSERT INTO servicos (
                        nome, descricao, codigo_plano_contas, ativo, escritorio_id,
                        created_at, updated_at
                    )
                    VALUES (
                        :nome, :descricao, :codigo_plano_contas, :ativo, :escritorio_id,
                        NOW(), NOW()
                    )
                    RETURNING id
                """), {
                    'nome': nome,
                    'descricao': descricao,
                    'codigo_plano_contas': codigo_plano_contas,
                    'ativo': ativo,
                    'escritorio_id': esc_id
                })
                
                novo_servico_id = result.scalar()
                total_criados += 1
                
                # Copiar etapas do serviço original
                result = conn.execute(text("""
                    SELECT id, nome, descricao, ordem, obrigatoria
                    FROM etapas
                    WHERE servico_id = :servico_id_original
                """), {'servico_id_original': servico_id_original})
                
                etapas = list(result)
                
                for etapa in etapas:
                    etapa_nome = etapa[1]
                    etapa_descricao = etapa[2]
                    etapa_ordem = etapa[3]
                    etapa_obrigatoria = etapa[4]
                    
                    # Criar etapa para o novo serviço
                    result = conn.execute(text("""
                        INSERT INTO etapas (
                            nome, descricao, ordem, servico_id, obrigatoria, escritorio_id,
                            created_at, updated_at
                        )
                        VALUES (
                            :nome, :descricao, :ordem, :servico_id, :obrigatoria, :escritorio_id,
                            NOW(), NOW()
                        )
                        RETURNING id
                    """), {
                        'nome': etapa_nome,
                        'descricao': etapa_descricao,
                        'ordem': etapa_ordem,
                        'servico_id': novo_servico_id,
                        'obrigatoria': etapa_obrigatoria,
                        'escritorio_id': esc_id
                    })
                    
                    nova_etapa_id = result.scalar()
                    
                    # Copiar tarefas da etapa original
                    result = conn.execute(text("""
                        SELECT nome, ordem, cor, tem_prazo, precisa_detalhamento
                        FROM tarefas
                        WHERE etapa_id = :etapa_id_original
                    """), {'etapa_id_original': etapa[0]})
                    
                    tarefas = list(result)
                    
                    for tarefa in tarefas:
                        conn.execute(text("""
                            INSERT INTO tarefas (
                                etapa_id, nome, ordem, cor, tem_prazo, precisa_detalhamento,
                                escritorio_id, created_at, updated_at
                            )
                            VALUES (
                                :etapa_id, :nome, :ordem, :cor, :tem_prazo, :precisa_detalhamento,
                                :escritorio_id, NOW(), NOW()
                            )
                        """), {
                            'etapa_id': nova_etapa_id,
                            'nome': tarefa[0],
                            'ordem': tarefa[1],
                            'cor': tarefa[2],
                            'tem_prazo': tarefa[3],
                            'precisa_detalhamento': tarefa[4],
                            'escritorio_id': esc_id
                        })
            
            conn.commit()
            print(f"  OK: Servicos copiados para escritorio {esc_id}")
        
        print(f"\nOK: {total_criados} servicos criados para outros escritorios")
        print("Todos os escritorios agora tem acesso aos servicos!")

if __name__ == "__main__":
    associate_servicos_to_all_escritorios()




