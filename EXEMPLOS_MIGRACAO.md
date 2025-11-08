# 💡 Exemplos Práticos - Migração de Dados

## 🎯 Cenários Comuns

### Cenário 1: Primeira Migração

```bash
# 1. Ativar ambiente
venv\Scripts\activate

# 2. Instalar dependência
pip install pymysql

# 3. Usar assistente
python migrar.py
```

**Resultado esperado:**

```
============================================================
  🔄 ASSISTENTE DE MIGRAÇÃO MySQL → PostgreSQL
============================================================

Este assistente vai guiá-lo através do processo de migração.
Certifique-se de ter:
  ✅ Acesso ao banco MySQL
  ✅ PostgreSQL configurado
  ✅ Ambiente virtual ativado

Deseja continuar? (s/n): s
```

### Cenário 2: Migração Manual Completa

```bash
# 1. Configurar credenciais
# Editar migrate_data.py linha 11:
# MYSQL_URL = "mysql+pymysql://root:senha123@localhost:3306/dbarqmanager"

# 2. Testar MySQL
python check_mysql.py

# 3. Aplicar migrations
alembic upgrade head

# 4. Executar migração
python migrate_data.py

# 5. Verificar
python check_migrated_data.py
```

### Cenário 3: Re-migração (Atualizar Dados)

```bash
# Simplesmente execute novamente
python migrate_data.py

# Registros novos serão adicionados
# Registros existentes serão ignorados
```

## 📊 Exemplos de Saída

### check_mysql.py - Sucesso

```
============================================================
🔍 TESTE DE CONEXÃO MYSQL
============================================================

🔌 Tentando conectar em: localhost:3306/dbarqmanager
✅ Conexão estabelecida com sucesso!

📋 Tabelas disponíveis:
   - status
   - cliente
   - servico
   - servico_etapa
   - proposta
   - projeto
   - movimento

📊 Contagem de registros ativos:
   ✅ Status: 8 registros
   ✅ Clientes: 45 registros
   ✅ Serviços: 17 registros
   ✅ Etapas: 63 registros
   ✅ Propostas: 23 registros
   ✅ Projetos: 12 registros
   ✅ Movimentos: 1547 registros

============================================================
✅ Teste concluído! Você pode executar a migração.
============================================================
```

### migrate_data.py - Sucesso

```
============================================================
🔄 MIGRAÇÃO DE DADOS: MySQL → PostgreSQL
============================================================

🔌 Conectando nos bancos de dados...
✅ Conexões estabelecidas

📊 Migrando Status...
✅ 8 status migrados

👥 Migrando Clientes...
✅ 45 clientes migrados

🛠️  Migrando Serviços...
✅ 17 serviços migrados

📋 Migrando Etapas...
✅ 63 etapas migradas

💰 Migrando Propostas...
✅ 23 propostas migradas

📁 Migrando Projetos...
✅ 12 projetos migrados

💵 Migrando Movimentos Financeiros...
✅ 1000 movimentos migrados (limitado a 1000)

============================================================
🎉 MIGRAÇÃO CONCLUÍDA COM SUCESSO!
============================================================
```

### check_migrated_data.py - Sucesso

```
============================================================
🔍 VERIFICAÇÃO DE DADOS MIGRADOS - PostgreSQL
============================================================

✅ Conectado ao PostgreSQL

📊 Contagem de registros:
   ✅ Status: 8 registros
   ✅ Clientes: 45 registros
   ✅ Serviços: 17 registros
   ✅ Etapas: 63 registros
   ✅ Propostas: 23 registros
   ✅ Projetos: 12 registros
   ✅ Movimentos: 1000 registros
   ⚠️  Colaboradores: Tabela não existe ou erro

   📈 Total: 1168 registros migrados

📋 Exemplos de dados:

   Status:
      - [1] Em Andamento
      - [2] Concluído
      - [3] Cancelado

   Serviços:
      - [1] Projeto Arquitetônico
      - [2] Projeto Estrutural
      - [3] Projeto Elétrico

   Clientes:
      - [1] João Silva (PF)
      - [2] Maria Santos (PF)
      - [3] Construtora ABC Ltda (PJ)

============================================================
✅ Verificação concluída!
============================================================
```

## 🐛 Exemplos de Erros

### Erro 1: pymysql não instalado

```
❌ Erro ao conectar no MySQL:
   No module named 'pymysql'

💡 Configure a URL do MySQL no início do arquivo migrate_data.py
```

**Solução:**

```bash
pip install pymysql
```

### Erro 2: Credenciais incorretas

```
❌ Erro ao conectar no MySQL:
   (1045, "Access denied for user 'usuario'@'localhost' (using password: YES)")
```

**Solução:**

```python
# Verificar credenciais em migrate_data.py linha 11
MYSQL_URL = "mysql+pymysql://usuario_correto:senha_correta@localhost:3306/dbarqmanager"
```

### Erro 3: Banco não existe

```
❌ Erro ao conectar no MySQL:
   (1049, "Unknown database 'dbarqmanager'")
```

**Solução:**

```sql
-- Criar banco no MySQL
CREATE DATABASE dbarqmanager;
```

### Erro 4: Tabelas não existem no PostgreSQL

```
❌ Erro ao migrar Status:
   relation "status" does not exist
```

**Solução:**

```bash
alembic upgrade head
```

## 🔧 Customizações

### Exemplo 1: Migrar apenas Clientes

Edite `migrate_data.py` função `main()`:

```python
def main():
    # ... código de conexão ...

    try:
        # Comentar o que não quer migrar
        # migrate_status(mysql_session, pg_session)
        migrate_clientes(mysql_session, pg_session)  # Apenas clientes
        # migrate_servicos(mysql_session, pg_session)
        # migrate_etapas(mysql_session, pg_session)
        # migrate_propostas(mysql_session, pg_session)
        # migrate_projetos(mysql_session, pg_session)
        # migrate_movimentos(mysql_session, pg_session)

        print("\n✅ Migração de clientes concluída!")
```

### Exemplo 2: Migrar todos os Movimentos

Edite `migrate_data.py` linha 234:

```python
# De:
result = mysql_session.execute(text("""
    SELECT ... FROM movimento
    WHERE ativo = 1
    LIMIT 1000
"""))

# Para:
result = mysql_session.execute(text("""
    SELECT ... FROM movimento
    WHERE ativo = 1
    -- LIMIT removido
"""))
```

### Exemplo 3: Adicionar Log Detalhado

Edite `migrate_data.py`:

```python
def migrate_clientes(mysql_session, pg_session):
    """Migra tabela cliente"""
    print("\n👥 Migrando Clientes...")

    result = mysql_session.execute(text("""..."""))

    count = 0
    for row in result:
        try:
            # Adicionar log
            print(f"   Migrando: [{row[0]}] {row[1]}")

            pg_session.execute(text("""..."""), {...})
            count += 1
        except Exception as e:
            print(f"⚠️  Erro ao migrar cliente {row[0]}: {e}")
```

## 📝 Verificações SQL

### Verificar dados no PostgreSQL

```sql
-- Conectar
psql -U arqmanager_user -d arqmanager

-- Contar registros
SELECT
    'status' as tabela, COUNT(*) as total FROM status
UNION ALL
SELECT 'clientes', COUNT(*) FROM cliente
UNION ALL
SELECT 'servicos', COUNT(*) FROM servicos
UNION ALL
SELECT 'etapas', COUNT(*) FROM etapas
UNION ALL
SELECT 'propostas', COUNT(*) FROM propostas
UNION ALL
SELECT 'projetos', COUNT(*) FROM projetos
UNION ALL
SELECT 'movimentos', COUNT(*) FROM movimentos;

-- Ver exemplos
SELECT id, nome, tipo_pessoa FROM cliente LIMIT 5;
SELECT id, nome FROM servicos LIMIT 5;
SELECT id, descricao FROM status;
```

### Comparar MySQL vs PostgreSQL

```bash
# MySQL
mysql -u usuario -p dbarqmanager -e "SELECT COUNT(*) FROM cliente WHERE ativo = 1"

# PostgreSQL
psql -U arqmanager_user -d arqmanager -c "SELECT COUNT(*) FROM cliente"
```

## 🎯 Fluxo Completo Recomendado

```bash
# 1. Preparação
venv\Scripts\activate
pip install pymysql

# 2. Configurar
# Editar migrate_data.py e check_mysql.py com credenciais

# 3. Testar
python check_mysql.py

# 4. Backup (opcional mas recomendado)
pg_dump -U arqmanager_user arqmanager > backup_antes.sql

# 5. Migrar
python migrate_data.py

# 6. Verificar
python check_migrated_data.py

# 7. Testar API
uvicorn app.main:app --reload

# 8. Criar admin
python create_admin.py

# 9. Testar login
python test_login.py

# 10. Acessar docs
# http://localhost:8000/docs
```

---

**Dica:** Use o assistente `python migrar.py` para um processo guiado!
