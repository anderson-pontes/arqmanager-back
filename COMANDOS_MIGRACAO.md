# ⚡ Comandos Rápidos - Migração de Dados

## 🚀 Migração Assistida (Recomendado)

```bash
# Ativar ambiente virtual
venv\Scripts\activate

# Executar assistente interativo
python migrar.py
```

O assistente vai:

-   ✅ Verificar dependências
-   ✅ Testar conexões
-   ✅ Executar migração
-   ✅ Verificar resultados

## 🔧 Migração Manual

### 1. Preparação

```bash
# Instalar dependência
pip install pymysql

# Aplicar migrations
alembic upgrade head
```

### 2. Configurar Credenciais

Edite os arquivos e configure a URL do MySQL:

```python
# check_mysql.py (linha 8)
# migrate_data.py (linha 11)
MYSQL_URL = "mysql+pymysql://usuario:senha@localhost:3306/dbarqmanager"
```

### 3. Testar Conexão

```bash
python check_mysql.py
```

### 4. Executar Migração

```bash
python migrate_data.py
```

### 5. Verificar Dados

```bash
python check_migrated_data.py
```

## 📊 Verificações Rápidas

### Ver tabelas PostgreSQL

```bash
python -c "from sqlalchemy import create_engine, inspect; from app.core.config import settings; print('\n'.join(inspect(create_engine(settings.DATABASE_URL)).get_table_names()))"
```

### Contar registros

```bash
python check_migrated_data.py
```

### Testar API

```bash
uvicorn app.main:app --reload
```

Acesse: http://localhost:8000/docs

## 🔄 Re-executar Migração

Pode executar quantas vezes quiser:

```bash
python migrate_data.py
```

Registros duplicados são ignorados automaticamente.

## 🐛 Solução de Problemas

### Erro: pymysql não encontrado

```bash
pip install pymysql
```

### Erro: Tabelas não existem

```bash
alembic upgrade head
```

### Erro: Conexão MySQL

Verifique:

1. MySQL está rodando
2. Credenciais corretas
3. Banco existe

```bash
# Testar conexão
python check_mysql.py
```

### Ver logs detalhados

```bash
# Executar com output completo
python migrate_data.py 2>&1 | tee migracao.log
```

## 📝 Ordem de Migração

O script migra nesta ordem (respeitando foreign keys):

1. Status
2. Clientes
3. Serviços
4. Etapas
5. Propostas
6. Projetos
7. Movimentos

## 💡 Dicas

### Migrar apenas uma tabela

Edite `migrate_data.py` e comente as funções que não quer executar:

```python
# migrate_status(mysql_session, pg_session)
migrate_clientes(mysql_session, pg_session)
# migrate_servicos(mysql_session, pg_session)
# ...
```

### Aumentar limite de movimentos

Edite linha 234 de `migrate_data.py`:

```python
# De:
LIMIT 1000

# Para:
LIMIT 10000  # ou remova o LIMIT
```

### Backup antes de migrar

```bash
# PostgreSQL
pg_dump -U arqmanager_user arqmanager > backup_antes.sql

# MySQL
mysqldump -u usuario -p dbarqmanager > backup_mysql.sql
```

## 📚 Documentação Completa

-   `GUIA_MIGRACAO_DADOS.md` - Guia detalhado
-   `CHECKLIST_MIGRACAO.md` - Checklist passo a passo
-   `QUICK_START.md` - Início rápido do projeto

---

**Tempo estimado:** 10-20 minutos  
**Dificuldade:** Fácil com assistente, Média manual
