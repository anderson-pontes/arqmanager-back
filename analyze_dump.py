#!/usr/bin/env python3
"""
Analisa o dump do MySQL e extrai informações sobre as tabelas
"""
import re

# Ler o arquivo
with open('../dbarqmanager.sql', 'r', encoding='utf-8') as f:
    content = f.read()

# Encontrar todas as tabelas
tables = re.findall(r'CREATE TABLE `(\w+)`', content)

print(f"📊 Total de tabelas: {len(tables)}\n")
print("📋 Lista de tabelas:")
print("=" * 50)

# Agrupar por categoria
categorias = {
    'Acesso/Permissões': [],
    'Clientes': [],
    'Projetos': [],
    'Financeiro': [],
    'Documentos': [],
    'Apoio/Configuração': [],
    'Logs': [],
    'Outros': []
}

for table in sorted(set(tables)):
    if 'acesso' in table or 'permissao' in table or 'grupo' in table:
        categorias['Acesso/Permissões'].append(table)
    elif 'cliente' in table:
        categorias['Clientes'].append(table)
    elif 'projeto' in table or 'proposta' in table:
        categorias['Projetos'].append(table)
    elif 'movimento' in table or 'conta' in table or 'plano_contas' in table or 'forma_pagamento' in table:
        categorias['Financeiro'].append(table)
    elif 'documento' in table or 'arquivo' in table or 'email' in table:
        categorias['Documentos'].append(table)
    elif 'log' in table:
        categorias['Logs'].append(table)
    elif 'etapa' in table or 'status' in table or 'feriados' in table or 'indicacao' in table or 'escritorio' in table or 'colaborador' in table:
        categorias['Apoio/Configuração'].append(table)
    else:
        categorias['Outros'].append(table)

for categoria, tabelas in categorias.items():
    if tabelas:
        print(f"\n{categoria} ({len(tabelas)} tabelas):")
        for t in tabelas:
            print(f"  - {t}")

# Tabelas principais para migração
print("\n" + "=" * 50)
print("🎯 PRIORIDADE DE MIGRAÇÃO:")
print("=" * 50)
print("\n✅ JÁ MIGRADAS:")
print("  - users (colaborador)")
print("  - clientes (cliente)")
print("  - servicos (não existe no MySQL - novo)")
print("  - etapas (relacionado a servicos - novo)")

print("\n📋 PRÓXIMAS FASES:")
print("\nFase 5 - Projetos:")
print("  - projeto")
print("  - projeto_colaborador")
print("  - projeto_documento")
print("  - projeto_etapa")
print("  - projeto_servico")

print("\nFase 6 - Propostas/Orçamentos:")
print("  - proposta")
print("  - proposta_servico")
print("  - proposta_etapa")

print("\nFase 7 - Financeiro:")
print("  - movimento")
print("  - conta_bancaria")
print("  - conta_movimentacao")
print("  - plano_contas")

print("\nFase 8 - Documentos:")
print("  - documento")
print("  - email")
print("  - arquivo_tipo")

print("\nFase 9 - Apoio:")
print("  - escritorio")
print("  - feriados")
print("  - forma_pagamento")
print("  - indicacao")
print("  - status")
