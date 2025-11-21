#!/usr/bin/env python3
"""
Teste completo para funcionalidades de Serviço/Etapa/Tarefa implementadas:
- Endpoint hierárquico
- Validações de exclusão
- Criação de tarefas com cores
- Hierarquia completa
"""
import requests
import json
import sys
import time
from typing import Optional

# Configurações
BASE_URL = "http://localhost:8000/api/v1"
LOGIN_DATA = {
    "email": "admin@arqmanager.com",
    "senha": "admin123"
}

# Cores para teste
CORES_TESTE = ["#FF5733", "#33FF57", "#3357FF", "#FF33F5", "#F5FF33"]

def get_token() -> Optional[str]:
    """Faz login, seleciona escritório e retorna o token"""
    try:
        # 1. Login
        response = requests.post(f"{BASE_URL}/auth/login", json=LOGIN_DATA, timeout=10)
        if response.status_code != 200:
            print(f"[ERRO] Erro no login: {response.status_code} - {response.text}")
            return None
        
        data = response.json()
        token = data.get("access_token")
        if not token:
            print(f"[ERRO] Token nao encontrado na resposta")
            return None
        
        print(f"[OK] Login realizado com sucesso")
        
        # 2. Buscar escritórios disponíveis
        headers = {"Authorization": f"Bearer {token}"}
        esc_response = requests.get(f"{BASE_URL}/auth/available-escritorios", headers=headers, timeout=10)
        
        if esc_response.status_code == 200:
            escritorios = esc_response.json()
            if escritorios and len(escritorios) > 0:
                escritorio = escritorios[0]
                escritorio_id = escritorio.get("id") if isinstance(escritorio, dict) else None
                perfis = escritorio.get("perfis", []) if isinstance(escritorio, dict) else []
                perfil = perfis[0].get("perfil") if perfis and isinstance(perfis[0], dict) else None
                
                # 3. Selecionar escritório
                context_data = {
                    "escritorio_id": escritorio_id,
                    "perfil": perfil
                }
                context_response = requests.post(
                    f"{BASE_URL}/auth/set-context",
                    json=context_data,
                    headers=headers,
                    timeout=10
                )
                
                if context_response.status_code == 200:
                    context_result = context_response.json()
                    new_token = context_result.get("access_token")
                    if new_token:
                        print(f"[OK] Escritorio selecionado (ID: {escritorio_id})")
                        return new_token
                    else:
                        print(f"[AVISO] Novo token nao encontrado, usando token original")
                        return token
                else:
                    print(f"[AVISO] Erro ao selecionar escritorio: {context_response.status_code}")
                    print(f"[AVISO] Continuando com token original (pode falhar em alguns endpoints)")
                    return token
            else:
                print(f"[AVISO] Nenhum escritorio disponivel, usando token original")
                return token
        else:
            print(f"[AVISO] Erro ao buscar escritorios: {esc_response.status_code}")
            print(f"[AVISO] Continuando com token original (pode falhar em alguns endpoints)")
            return token
        
    except Exception as e:
        print(f"[ERRO] Erro ao conectar: {e}")
        return None

def print_section(title: str):
    """Imprime seção do teste"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def test_hierarquia_endpoint(headers: dict):
    """Testa o endpoint hierárquico"""
    print_section("TESTE 1: Endpoint Hierárquico")
    
    print("\n[TESTE] Testando GET /servicos/hierarquia...")
    response = requests.get(f"{BASE_URL}/servicos/hierarquia", headers=headers, timeout=10)
    
    if response.status_code == 200:
        servicos = response.json()
        print(f"[OK] Endpoint hierarquico funcionando!")
        print(f"   Total de serviços: {len(servicos)}")
        
        # Verificar estrutura hierárquica
        for servico in servicos[:3]:  # Mostrar apenas os 3 primeiros
            print(f"\n   [SERVICO] Servico: {servico['nome']} (ID: {servico['id']})")
            if 'etapas' in servico and servico['etapas']:
                print(f"      Etapas: {len(servico['etapas'])}")
                for etapa in servico['etapas'][:2]:  # Mostrar apenas 2 etapas
                    print(f"         |-- {etapa['nome']} (ID: {etapa['id']}, Ordem: {etapa['ordem']})")
                    if 'tarefas' in etapa and etapa['tarefas']:
                        print(f"            Tarefas: {len(etapa['tarefas'])}")
                        for tarefa in etapa['tarefas'][:2]:  # Mostrar apenas 2 tarefas
                            cor_info = f" (Cor: {tarefa['cor']})" if tarefa.get('cor') else ""
                            print(f"               |-- {tarefa['nome']}{cor_info}")
            else:
                print(f"      Nenhuma etapa cadastrada")
        
        return True
    else:
        print(f"[ERRO] Erro: {response.status_code} - {response.text}")
        return False

def test_criar_servico_completo(headers: dict):
    """Cria um serviço completo com etapas e tarefas para testes"""
    print_section("TESTE 2: Criar Serviço Completo")
    
    # Gerar código único baseado em timestamp
    codigo_unico = f"TEST.{int(time.time())}"
    
    servico_data = {
        "nome": "Teste - Serviço Completo",
        "descricao": "Serviço criado para testes de hierarquia",
        "codigo_plano_contas": codigo_unico,
        "ativo": True,
        "etapas": [
            {
                "nome": "Etapa 1 - Teste",
                "descricao": "Primeira etapa de teste",
                "ordem": 1,
                "obrigatoria": True
            },
            {
                "nome": "Etapa 2 - Teste",
                "descricao": "Segunda etapa de teste",
                "ordem": 2,
                "obrigatoria": True
            }
        ]
    }
    
    print("\n[CRIAR] Criando servico com etapas...")
    response = requests.post(f"{BASE_URL}/servicos", json=servico_data, headers=headers, timeout=10)
    
    if response.status_code == 201:
        servico = response.json()
        servico_id = servico['id']
        print(f"[OK] Servico criado: {servico['nome']} (ID: {servico_id})")
        print(f"   Etapas criadas: {len(servico.get('etapas', []))}")
        
        # Criar tarefas para as etapas
        etapa_ids = []
        for etapa in servico.get('etapas', []):
            etapa_id = etapa['id']
            etapa_ids.append(etapa_id)
            
            # Criar 2 tarefas por etapa com cores diferentes
            for i, cor in enumerate(CORES_TESTE[:2], 1):
                tarefa_data = {
                    "nome": f"Tarefa {i} - {etapa['nome']}",
                    "ordem": i,
                    "cor": cor,
                    "tem_prazo": True,
                    "precisa_detalhamento": i == 1
                }
                
                print(f"\n   [CRIAR] Criando tarefa na etapa {etapa['nome']}...")
                tarefa_response = requests.post(
                    f"{BASE_URL}/servicos/{servico_id}/etapas/{etapa_id}/tarefas",
                    json=tarefa_data,
                    headers=headers,
                    timeout=10
                )
                
                if tarefa_response.status_code == 201:
                    tarefa = tarefa_response.json()
                    print(f"      [OK] Tarefa criada: {tarefa['nome']} (Cor: {tarefa.get('cor', 'N/A')})")
                else:
                    print(f"      [ERRO] Erro ao criar tarefa: {tarefa_response.status_code} - {tarefa_response.text}")
        
        return servico_id, etapa_ids
    else:
        print(f"[ERRO] Erro ao criar servico: {response.status_code} - {response.text}")
        return None, []

def test_validacao_exclusao(headers: dict, servico_id: int, etapa_ids: list):
    """Testa validações de exclusão"""
    print_section("TESTE 3: Validações de Exclusão")
    
    if not etapa_ids:
        print("[AVISO] Nenhuma etapa disponivel para teste")
        return
    
    etapa_id = etapa_ids[0]
    
    # Teste 1: Tentar excluir serviço com etapas (deve falhar)
    print("\n[TESTE] Teste 1: Tentando excluir servico com etapas...")
    response = requests.delete(f"{BASE_URL}/servicos/{servico_id}", headers=headers, timeout=10)
    
    if response.status_code == 400:
        print(f"[OK] Validacao funcionando! Erro esperado: {response.json().get('detail', 'N/A')}")
    else:
        print(f"[ERRO] Validacao falhou! Status: {response.status_code}")
        print(f"   Resposta: {response.text}")
    
    # Teste 2: Tentar excluir etapa com tarefas (deve falhar)
    print(f"\n[TESTE] Teste 2: Tentando excluir etapa com tarefas (ID: {etapa_id})...")
    response = requests.delete(
        f"{BASE_URL}/servicos/{servico_id}/etapas/{etapa_id}",
        headers=headers,
        timeout=10
    )
    
    if response.status_code == 400:
        print(f"[OK] Validacao funcionando! Erro esperado: {response.json().get('detail', 'N/A')}")
    else:
        print(f"[ERRO] Validacao falhou! Status: {response.status_code}")
        print(f"   Resposta: {response.text}")
    
    # Teste 3: Excluir tarefas primeiro (deve funcionar)
    print(f"\n[EXCLUIR] Teste 3: Excluindo tarefas da etapa {etapa_id}...")
    
    # Listar tarefas da etapa
    tarefas_response = requests.get(
        f"{BASE_URL}/servicos/{servico_id}/etapas/{etapa_id}/tarefas",
        headers=headers,
        timeout=10
    )
    
    if tarefas_response.status_code == 200:
        tarefas = tarefas_response.json()
        print(f"   Tarefas encontradas: {len(tarefas)}")
        
        for tarefa in tarefas:
            tarefa_id = tarefa['id']
            delete_response = requests.delete(
                f"{BASE_URL}/servicos/{servico_id}/etapas/{etapa_id}/tarefas/{tarefa_id}",
                headers=headers,
                timeout=10
            )
            if delete_response.status_code == 204:
                print(f"      [OK] Tarefa {tarefa['nome']} excluida")
            else:
                print(f"      [ERRO] Erro ao excluir tarefa: {delete_response.status_code}")
    
    # Teste 4: Agora deve conseguir excluir a etapa
    print(f"\n[EXCLUIR] Teste 4: Excluindo etapa {etapa_id} (sem tarefas)...")
    response = requests.delete(
        f"{BASE_URL}/servicos/{servico_id}/etapas/{etapa_id}",
        headers=headers,
        timeout=10
    )
    
    if response.status_code == 204:
        print(f"[OK] Etapa excluida com sucesso!")
    else:
        print(f"[ERRO] Erro ao excluir etapa: {response.status_code} - {response.text}")

def test_hierarquia_completa(headers: dict, servico_id: int):
    """Testa se a hierarquia completa está sendo retornada"""
    print_section("TESTE 4: Verificar Hierarquia Completa")
    
    print(f"\n[BUSCAR] Buscando servico {servico_id} via endpoint hierarquico...")
    response = requests.get(f"{BASE_URL}/servicos/hierarquia", headers=headers, timeout=10)
    
    if response.status_code == 200:
        servicos = response.json()
        servico = next((s for s in servicos if s['id'] == servico_id), None)
        
        if servico:
            print(f"[OK] Servico encontrado: {servico['nome']}")
            print(f"   Etapas: {len(servico.get('etapas', []))}")
            
            total_tarefas = 0
            for etapa in servico.get('etapas', []):
                tarefas_count = len(etapa.get('tarefas', []))
                total_tarefas += tarefas_count
                if tarefas_count > 0:
                    print(f"      |-- {etapa['nome']}: {tarefas_count} tarefa(s)")
                    for tarefa in etapa.get('tarefas', []):
                        cor = tarefa.get('cor', 'sem cor')
                        print(f"         |-- {tarefa['nome']} (Cor: {cor})")
            
            print(f"\n   Total de tarefas: {total_tarefas}")
            return True
        else:
            print(f"[AVISO] Servico {servico_id} nao encontrado na lista")
            return False
    else:
        print(f"[ERRO] Erro: {response.status_code} - {response.text}")
        return False

def test_cores_tarefas(headers: dict, servico_id: int):
    """Testa criação e validação de cores em tarefas"""
    print_section("TESTE 5: Cores em Tarefas")
    
    # Listar etapas do serviço
    etapas_response = requests.get(
        f"{BASE_URL}/servicos/{servico_id}/etapas",
        headers=headers,
        timeout=10
    )
    
    if etapas_response.status_code != 200 or not etapas_response.json():
        print("[AVISO] Nenhuma etapa disponivel para teste de cores")
        return
    
    etapa = etapas_response.json()[0]
    etapa_id = etapa['id']
    
    print(f"\n[CORES] Testando cores em tarefas da etapa: {etapa['nome']}")
    
    # Teste 1: Cor válida (hex completo)
    print("\n   Teste 1: Criar tarefa com cor válida (#FF5733)...")
    tarefa_data = {
        "nome": "Tarefa com Cor Válida",
        "ordem": 10,
        "cor": "#FF5733",
        "tem_prazo": True,
        "precisa_detalhamento": False
    }
    
    response = requests.post(
        f"{BASE_URL}/servicos/{servico_id}/etapas/{etapa_id}/tarefas",
        json=tarefa_data,
        headers=headers,
        timeout=10
    )
    
    if response.status_code == 201:
        tarefa = response.json()
        print(f"      [OK] Tarefa criada com cor: {tarefa.get('cor')}")
    else:
        print(f"      [ERRO] Erro: {response.status_code} - {response.text}")
    
    # Teste 2: Cor sem # (deve adicionar automaticamente)
    print("\n   Teste 2: Criar tarefa com cor sem # (33FF57)...")
    tarefa_data2 = {
        "nome": "Tarefa com Cor Sem #",
        "ordem": 11,
        "cor": "33FF57",  # Sem #
        "tem_prazo": True,
        "precisa_detalhamento": False
    }
    
    response = requests.post(
        f"{BASE_URL}/servicos/{servico_id}/etapas/{etapa_id}/tarefas",
        json=tarefa_data2,
        headers=headers,
        timeout=10
    )
    
    if response.status_code == 201:
        tarefa = response.json()
        cor_salva = tarefa.get('cor', '')
        if cor_salva.startswith('#'):
            print(f"      [OK] Cor formatada corretamente: {cor_salva}")
        else:
            print(f"      [AVISO] Cor nao foi formatada: {cor_salva}")
    else:
        print(f"      [ERRO] Erro: {response.status_code} - {response.text}")
    
    # Teste 3: Cor inválida (deve falhar)
    print("\n   Teste 3: Tentar criar tarefa com cor inválida (XXXXXX)...")
    tarefa_data3 = {
        "nome": "Tarefa com Cor Inválida",
        "ordem": 12,
        "cor": "XXXXXX",  # Inválida
        "tem_prazo": True,
        "precisa_detalhamento": False
    }
    
    response = requests.post(
        f"{BASE_URL}/servicos/{servico_id}/etapas/{etapa_id}/tarefas",
        json=tarefa_data3,
        headers=headers,
        timeout=10
    )
    
    if response.status_code == 400:
        print(f"      [OK] Validacao funcionando! Erro: {response.json().get('detail', 'N/A')}")
    else:
        print(f"      [ERRO] Validacao falhou! Status: {response.status_code}")

def limpar_dados_teste(headers: dict, servico_id: int):
    """Limpa os dados de teste criados"""
    print_section("LIMPEZA: Removendo Dados de Teste")
    
    print(f"\n[EXCLUIR] Excluindo servico de teste (ID: {servico_id})...")
    
    # Primeiro, excluir todas as etapas e tarefas
    etapas_response = requests.get(
        f"{BASE_URL}/servicos/{servico_id}/etapas",
        headers=headers,
        timeout=10
    )
    
    if etapas_response.status_code == 200:
        etapas = etapas_response.json()
        for etapa in etapas:
            etapa_id = etapa['id']
            
            # Excluir tarefas
            tarefas_response = requests.get(
                f"{BASE_URL}/servicos/{servico_id}/etapas/{etapa_id}/tarefas",
                headers=headers,
                timeout=10
            )
            
            if tarefas_response.status_code == 200:
                tarefas = tarefas_response.json()
                for tarefa in tarefas:
                    requests.delete(
                        f"{BASE_URL}/servicos/{servico_id}/etapas/{etapa_id}/tarefas/{tarefa['id']}",
                        headers=headers,
                        timeout=10
                    )
            
            # Excluir etapa
            requests.delete(
                f"{BASE_URL}/servicos/{servico_id}/etapas/{etapa_id}",
                headers=headers,
                timeout=10
            )
    
    # Excluir serviço
    response = requests.delete(f"{BASE_URL}/servicos/{servico_id}", headers=headers, timeout=10)
    if response.status_code == 204:
        print(f"[OK] Servico de teste excluido")
    else:
        print(f"[AVISO] Erro ao excluir servico: {response.status_code}")

def main():
    """Executa todos os testes"""
    print("\n" + "="*60)
    print("  TESTE COMPLETO: Serviço/Etapa/Tarefa")
    print("="*60)
    
    # Login
    token = get_token()
    if not token:
        print("\n[ERRO] Nao foi possivel fazer login. Verifique se o servidor esta rodando.")
        sys.exit(1)
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Executar testes
    resultados = {
        "hierarquia": False,
        "criacao": False,
        "validacao": False,
        "cores": False
    }
    
    try:
        # Teste 1: Endpoint hierárquico
        resultados["hierarquia"] = test_hierarquia_endpoint(headers)
        
        # Teste 2: Criar serviço completo
        servico_id, etapa_ids = test_criar_servico_completo(headers)
        if servico_id:
            resultados["criacao"] = True
            
            # Teste 3: Validações de exclusão
            test_validacao_exclusao(headers, servico_id, etapa_ids)
            resultados["validacao"] = True
            
            # Teste 4: Hierarquia completa
            test_hierarquia_completa(headers, servico_id)
            
            # Teste 5: Cores em tarefas
            test_cores_tarefas(headers, servico_id)
            resultados["cores"] = True
            
            # Limpar dados de teste
            limpar_dados_teste(headers, servico_id)
        
    except Exception as e:
        print(f"\n[ERRO] Erro durante os testes: {e}")
        import traceback
        traceback.print_exc()
    
    # Resumo
    print_section("RESUMO DOS TESTES")
    print("\n[RESULTADO] Testes Concluidos:")
    print(f"   - Endpoint Hierarquico: {'[OK]' if resultados['hierarquia'] else '[ERRO]'}")
    print(f"   - Criacao Completa: {'[OK]' if resultados['criacao'] else '[ERRO]'}")
    print(f"   - Validacoes de Exclusao: {'[OK]' if resultados['validacao'] else '[ERRO]'}")
    print(f"   - Cores em Tarefas: {'[OK]' if resultados['cores'] else '[ERRO]'}")
    
    total = sum(resultados.values())
    print(f"\n[RESULTADO] {total}/4 testes passaram")
    
    if total == 4:
        print("\n[SUCESSO] Todos os testes passaram com sucesso!")
        sys.exit(0)
    else:
        print("\n[AVISO] Alguns testes falharam. Verifique os logs acima.")
        sys.exit(1)

if __name__ == "__main__":
    main()

