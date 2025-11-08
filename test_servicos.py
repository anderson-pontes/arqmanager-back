#!/usr/bin/env python3
"""
Script para testar endpoints de serviços e etapas
"""
import requests
import json

# Configurações
BASE_URL = "http://localhost:8000/api/v1"
LOGIN_DATA = {
    "email": "admin@arqmanager.com",
    "senha": "admin123"
}

def get_token():
    """Faz login e retorna o token"""
    response = requests.post(f"{BASE_URL}/auth/login", json=LOGIN_DATA)
    print(f"Login status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        token = data.get("access_token")
        print(f"Token obtido: {token[:50]}..." if token else "Token não encontrado!")
        return token
    else:
        print(f"❌ Erro no login: {response.status_code} - {response.text}")
        return None

def test_servicos():
    """Testa os endpoints de serviços"""
    print("🔐 Fazendo login...")
    token = get_token()
    if not token:
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\n📋 1. Listando serviços...")
    response = requests.get(f"{BASE_URL}/servicos", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        servicos = response.json()
        print(f"Total de serviços: {len(servicos)}")
    else:
        print(f"Erro: {response.text}")
    
    print("\n➕ 2. Criando serviço com etapas...")
    servico_data = {
        "nome": "Projeto Arquitetônico Residencial",
        "descricao": "Projeto completo de arquitetura residencial",
        "valor_base": 15000.00,
        "unidade": "m²",
        "ativo": True,
        "etapas": [
            {
                "nome": "Levantamento",
                "descricao": "Levantamento do terreno e necessidades do cliente",
                "ordem": 1,
                "obrigatoria": True
            },
            {
                "nome": "Estudo Preliminar",
                "descricao": "Desenvolvimento do estudo preliminar",
                "ordem": 2,
                "obrigatoria": True
            },
            {
                "nome": "Anteprojeto",
                "descricao": "Desenvolvimento do anteprojeto",
                "ordem": 3,
                "obrigatoria": True
            },
            {
                "nome": "Projeto Legal",
                "descricao": "Projeto para aprovação na prefeitura",
                "ordem": 4,
                "obrigatoria": True
            },
            {
                "nome": "Projeto Executivo",
                "descricao": "Projeto detalhado para execução",
                "ordem": 5,
                "obrigatoria": False
            }
        ]
    }
    
    response = requests.post(f"{BASE_URL}/servicos", json=servico_data, headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        servico_criado = response.json()
        print(f"✅ Serviço criado: {servico_criado['nome']} (ID: {servico_criado['id']})")
        print(f"   Etapas: {len(servico_criado['etapas'])}")
        servico_id = servico_criado['id']
    else:
        print(f"❌ Erro: {response.text}")
        return
    
    print("\n➕ 3. Criando outro serviço...")
    servico_data2 = {
        "nome": "Projeto de Interiores",
        "descricao": "Projeto de design de interiores",
        "valor_base": 8000.00,
        "unidade": "m²",
        "ativo": True,
        "etapas": [
            {
                "nome": "Briefing",
                "descricao": "Reunião inicial com cliente",
                "ordem": 1,
                "obrigatoria": True
            },
            {
                "nome": "Conceito",
                "descricao": "Desenvolvimento do conceito",
                "ordem": 2,
                "obrigatoria": True
            },
            {
                "nome": "Projeto 3D",
                "descricao": "Renderizações 3D",
                "ordem": 3,
                "obrigatoria": False
            }
        ]
    }
    
    response = requests.post(f"{BASE_URL}/servicos", json=servico_data2, headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        servico_criado = response.json()
        print(f"✅ Serviço criado: {servico_criado['nome']} (ID: {servico_criado['id']})")
    else:
        print(f"❌ Erro: {response.text}")
    
    print(f"\n🔍 4. Buscando serviço por ID ({servico_id})...")
    response = requests.get(f"{BASE_URL}/servicos/{servico_id}", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        servico = response.json()
        print(f"✅ Serviço encontrado: {servico['nome']}")
        print(f"   Valor base: R$ {servico['valor_base']}")
        print(f"   Etapas:")
        for etapa in servico['etapas']:
            obrig = "✓" if etapa['obrigatoria'] else "○"
            print(f"      {etapa['ordem']}. [{obrig}] {etapa['nome']}")
    else:
        print(f"❌ Erro: {response.text}")
    
    print(f"\n✏️ 5. Atualizando serviço ({servico_id})...")
    update_data = {
        "valor_base": 18000.00,
        "descricao": "Projeto completo de arquitetura residencial - ATUALIZADO"
    }
    
    response = requests.put(f"{BASE_URL}/servicos/{servico_id}", json=update_data, headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        servico_atualizado = response.json()
        print(f"✅ Serviço atualizado: R$ {servico_atualizado['valor_base']}")
    else:
        print(f"❌ Erro: {response.text}")
    
    print("\n📊 6. Contando serviços...")
    response = requests.get(f"{BASE_URL}/servicos/stats/count", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        stats = response.json()
        print(f"✅ Total de serviços: {stats['total']}")
    else:
        print(f"❌ Erro: {response.text}")
    
    print("\n🔍 7. Buscando serviços (filtro)...")
    response = requests.get(f"{BASE_URL}/servicos?search=projeto", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        servicos = response.json()
        print(f"✅ Serviços encontrados: {len(servicos)}")
        for s in servicos:
            print(f"   - {s['nome']} (R$ {s['valor_base']})")
    else:
        print(f"❌ Erro: {response.text}")
    
    print(f"\n📋 8. Listando etapas do serviço ({servico_id})...")
    response = requests.get(f"{BASE_URL}/servicos/{servico_id}/etapas", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        etapas = response.json()
        print(f"✅ Total de etapas: {len(etapas)}")
        etapa_id = etapas[0]['id'] if etapas else None
    else:
        print(f"❌ Erro: {response.text}")
        etapa_id = None
    
    if etapa_id:
        print(f"\n➕ 9. Adicionando nova etapa ao serviço ({servico_id})...")
        nova_etapa = {
            "nome": "Acompanhamento de Obra",
            "descricao": "Acompanhamento durante a execução",
            "ordem": 6,
            "obrigatoria": False
        }
        
        response = requests.post(f"{BASE_URL}/servicos/{servico_id}/etapas", json=nova_etapa, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            etapa_criada = response.json()
            print(f"✅ Etapa criada: {etapa_criada['nome']}")
        else:
            print(f"❌ Erro: {response.text}")
        
        print(f"\n✏️ 10. Atualizando etapa ({etapa_id})...")
        update_etapa = {
            "descricao": "Levantamento completo do terreno e necessidades - ATUALIZADO"
        }
        
        response = requests.put(f"{BASE_URL}/servicos/{servico_id}/etapas/{etapa_id}", json=update_etapa, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            etapa_atualizada = response.json()
            print(f"✅ Etapa atualizada: {etapa_atualizada['nome']}")
        else:
            print(f"❌ Erro: {response.text}")
    
    print("\n🎉 Teste completo!")

if __name__ == "__main__":
    test_servicos()
