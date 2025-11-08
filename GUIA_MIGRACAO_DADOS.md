# 🔄 Guia de Migração de Dados MySQL → PostgreSQL

## 📋 Pré-requisitos

### 1. Instalar Dependência MySQL

O script precisa do driver MySQL para Python:

```bash
pip install pymysql
```

### 2. Verificar Conexões

**MySQL:**

-   Host, porta, usuário e senha
-   Nome do banco: `dbarqmanager`

**PostgreSQL:**

-   Já configurado no `.env`
-   Banco criado e migrations aplicadas

## 🚀 Passo a Passo

### Etapa 1: Configurar Credenciais MySQL

Edite o arquivo `migrate_data.py` na linha 11:

```python
MYSQL_URL = "mysql+pymysql://usuario:senha@host:3306/dbarqmanager"
```

**Exemplo:**

```python
MYSQL_URL = "mysql+pymysql://root:minhasenha@localhost:3306/dbarqmanager"
```

### Etapa 2: Garantir que o PostgreSQL está Pronto

```bash
# Ativar ambiente virtual
venv\Scripts\activate

# Aplicar todas as migrations
alembic upgrade head
```

### Etapa 3: Testar Conexão MySQL

Antes de migrar, teste se consegue conectar:

```bash
python check_mysql.py
```

### Etapa 4: Executar Migração

```bash
python migrate_data.py
```

## 📊 O que será Migrado

O script migra na ordem correta (respeitando foreign keys):

1. ✅ **Status** - Tabela de status dos projetos
2. ✅ **Clientes** - Pessoas físicas e jurídicas
3. ✅ **Serviços** - Tipos de serviços oferecidos
4. ✅ **Etapas** - Etapas de cada serviço
5. ✅ **Propostas** - Orçamentos e propostas
6. ✅ **Projetos** - Projetos em andamento
7. ✅ **Movimentos** - Movimentos financeiros (limitado a 1000)

## ⚠️ Observações Importantes

### Dados Ativos

O script migra apenas registros com `ativo = 1` (exceto etapas).

### Conflitos

Usa `ON CONFLICT DO NOTHING` - se o registro já existe, pula.

### Movimentos Financeiros

Por segurança, migra apenas os primeiros 1000 registros.
Para migrar todos, edite a linha 234 do `migrate_data.py`:

```python
# Remover ou aumentar o LIMIT
LIMIT 1000
```

### Erros

Se houver erros em registros específicos, eles são exibidos mas não param a migração.

## 🔍 Verificar Migração

Após a migração, verifique os dados:

```bash
python check_db.py
```

Ou conecte no PostgreSQL:

```bash
psql -U arqmanager_user -d arqmanager
```

```sql
-- Contar registros
SELECT 'status' as tabela, COUNT(*) FROM status
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
```

## 🐛 Troubleshooting

### Erro: "No module named 'pymysql'"

```bash
pip install pymysql
```

### Erro: "Can't connect to MySQL server"

Verifique:

1. MySQL está rodando
2. Credenciais corretas no `migrate_data.py`
3. Firewall não está bloqueando

### Erro: "relation does not exist"

Execute as migrations primeiro:

```bash
alembic upgrade head
```

### Erro: "foreign key constraint"

A ordem de migração está correta no script.
Se persistir, verifique se as tabelas referenciadas existem.

## 📝 Logs

O script exibe:

-   ✅ Sucessos em verde
-   ⚠️ Avisos em amarelo
-   ❌ Erros em vermelho

Exemplo de saída:

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
✅ 156 movimentos migrados (limitado a 1000)

============================================================
🎉 MIGRAÇÃO CONCLUÍDA COM SUCESSO!
============================================================
```

## 🔄 Re-executar Migração

Pode executar o script múltiplas vezes com segurança.
Registros duplicados são ignorados (ON CONFLICT DO NOTHING).

## 📞 Próximos Passos

Após a migração:

1. ✅ Verificar dados no PostgreSQL
2. ✅ Testar API com dados reais
3. ✅ Criar usuário admin
4. ✅ Testar login e funcionalidades

```bash
# Criar usuário admin
python create_admin.py
```

---

**Dúvidas?** Verifique os logs do script ou consulte a documentação.
