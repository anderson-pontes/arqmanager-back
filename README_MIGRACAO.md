# 🔄 Migração MySQL → PostgreSQL - ARQManager

## 📖 Visão Geral

Este guia ajuda você a migrar todos os dados do sistema legado MySQL para o novo backend FastAPI com PostgreSQL.

## 🎯 O que será migrado?

| Tabela MySQL    | Tabela PostgreSQL | Registros      |
| --------------- | ----------------- | -------------- |
| `status`        | `status`          | Todos ativos   |
| `cliente`       | `cliente`         | Todos ativos   |
| `servico`       | `servicos`        | Todos ativos   |
| `servico_etapa` | `etapas`          | Todos          |
| `proposta`      | `propostas`       | Todos          |
| `projeto`       | `projetos`        | Todos ativos   |
| `movimento`     | `movimentos`      | Primeiros 1000 |

## 🚀 Início Rápido

### Opção 1: Assistente Interativo (Recomendado)

```bash
python migrar.py
```

### Opção 2: Manual

```bash
# 1. Instalar dependência
pip install pymysql

# 2. Configurar credenciais nos arquivos
#    - check_mysql.py (linha 8)
#    - migrate_data.py (linha 11)

# 3. Testar MySQL
python check_mysql.py

# 4. Executar migração
python migrate_data.py

# 5. Verificar dados
python check_migrated_data.py
```

## 📁 Arquivos de Migração

### Scripts Principais

-   **`migrar.py`** - Assistente interativo (RECOMENDADO)
-   **`migrate_data.py`** - Script de migração principal
-   **`check_mysql.py`** - Testa conexão MySQL
-   **`check_migrated_data.py`** - Verifica dados no PostgreSQL

### Documentação

-   **`GUIA_MIGRACAO_DADOS.md`** - Guia completo e detalhado
-   **`CHECKLIST_MIGRACAO.md`** - Checklist passo a passo
-   **`COMANDOS_MIGRACAO.md`** - Referência rápida de comandos

## ⚙️ Configuração

### 1. Credenciais MySQL

Edite os arquivos e configure:

```python
MYSQL_URL = "mysql+pymysql://usuario:senha@host:3306/dbarqmanager"
```

**Exemplo:**

```python
MYSQL_URL = "mysql+pymysql://root:minhasenha@localhost:3306/dbarqmanager"
```

### 2. PostgreSQL

Já configurado no arquivo `.env`:

```env
DATABASE_URL=postgresql://arqmanager_user:senha@localhost:5432/arqmanager
```

## 🔍 Verificações

### Antes da Migração

```bash
# Testar MySQL
python check_mysql.py

# Ver tabelas PostgreSQL
alembic upgrade head
```

### Após a Migração

```bash
# Verificar dados
python check_migrated_data.py

# Testar API
uvicorn app.main:app --reload
```

## 📊 Mapeamento de Campos

### Cliente

| MySQL           | PostgreSQL      | Observações          |
| --------------- | --------------- | -------------------- |
| `cod_cliente`   | `id`            | Mantém o ID original |
| `nome`          | `nome`          | -                    |
| `razao_social`  | `razao_social`  | -                    |
| `identificacao` | `identificacao` | CPF/CNPJ             |
| `tipo_pessoa`   | `tipo_pessoa`   | PF/PJ                |

### Serviço

| MySQL                 | PostgreSQL            | Observações          |
| --------------------- | --------------------- | -------------------- |
| `cod_servico`         | `id`                  | Mantém o ID original |
| `desc_servico`        | `nome`                | Renomeado            |
| `desc_documento`      | `descricao`           | Renomeado            |
| `codigo_plano_contas` | `codigo_plano_contas` | -                    |

### Etapa

| MySQL                | PostgreSQL    | Observações          |
| -------------------- | ------------- | -------------------- |
| `cod_servico_etapa`  | `id`          | Mantém o ID original |
| `descricao`          | `nome`        | Renomeado            |
| `descricao_contrato` | `descricao`   | Renomeado            |
| `exibir`             | `obrigatoria` | Lógica invertida     |

## ⚠️ Observações Importantes

### Dados Ativos

Por padrão, migra apenas registros com `ativo = 1`.

### IDs Preservados

Os IDs originais do MySQL são mantidos no PostgreSQL para facilitar referências.

### Conflitos

Usa `ON CONFLICT DO NOTHING` - registros duplicados são ignorados.

### Limite de Movimentos

Por segurança, migra apenas 1000 movimentos financeiros.
Para migrar todos, edite `migrate_data.py` linha 234.

## 🔄 Re-executar Migração

Pode executar o script múltiplas vezes:

```bash
python migrate_data.py
```

Registros já existentes são ignorados automaticamente.

## 🐛 Problemas Comuns

### "No module named 'pymysql'"

```bash
pip install pymysql
```

### "Can't connect to MySQL server"

1. Verificar se MySQL está rodando
2. Verificar credenciais
3. Testar: `python check_mysql.py`

### "relation does not exist"

```bash
alembic upgrade head
```

### Dados não aparecem

1. Verificar se migração foi concluída
2. Executar: `python check_migrated_data.py`
3. Verificar logs de erro

## 📈 Próximos Passos

Após migração bem-sucedida:

1. **Criar usuário admin**

    ```bash
    python create_admin.py
    ```

2. **Testar login**

    ```bash
    python test_login.py
    ```

3. **Iniciar API**

    ```bash
    uvicorn app.main:app --reload
    ```

4. **Acessar documentação**
    - http://localhost:8000/docs

## 💾 Backup

### Antes de Migrar

```bash
# PostgreSQL
pg_dump -U arqmanager_user arqmanager > backup_antes.sql

# MySQL (opcional)
mysqldump -u usuario -p dbarqmanager > backup_mysql.sql
```

### Restaurar Backup

```bash
# PostgreSQL
psql -U arqmanager_user arqmanager < backup_antes.sql
```

## 📞 Suporte

### Documentação

-   `GUIA_MIGRACAO_DADOS.md` - Guia detalhado
-   `CHECKLIST_MIGRACAO.md` - Checklist
-   `COMANDOS_MIGRACAO.md` - Comandos rápidos

### Logs

Salvar logs da migração:

```bash
python migrate_data.py 2>&1 | tee migracao.log
```

## ✅ Checklist Rápido

-   [ ] pymysql instalado
-   [ ] Credenciais MySQL configuradas
-   [ ] PostgreSQL rodando
-   [ ] Migrations aplicadas
-   [ ] Conexão MySQL testada
-   [ ] Migração executada
-   [ ] Dados verificados
-   [ ] API testada

---

**Tempo estimado:** 15-30 minutos  
**Dificuldade:** Fácil  
**Reversível:** Sim (dados MySQL intactos)

**Última atualização:** Janeiro 2025
