# 🔧 Como Configurar a Conexão MySQL

## 📋 Opções de Configuração

Existem 3 formas de configurar a conexão MySQL:

### Opção 1: Arquivo `.mysql_config` (Recomendado)

Crie ou edite o arquivo `.mysql_config` na raiz do `arqmanager-backend`:

```bash
# .mysql_config
MYSQL_URL=mysql+pymysql://usuario:senha@host:porta/banco
```

**Exemplo:**
```bash
# MySQL Local
MYSQL_URL=mysql+pymysql://root:minhasenha@localhost:3306/dbarqmanager

# MySQL AWS RDS
MYSQL_URL=mysql+pymysql://admin:senha@dbarqmanager.cdcwiwycwh5a.sa-east-1.rds.amazonaws.com:3306/dbarqmanager
```

### Opção 2: Variável de Ambiente

```bash
# Windows PowerShell
$env:MYSQL_URL="mysql+pymysql://usuario:senha@host:porta/banco"

# Linux/Mac
export MYSQL_URL="mysql+pymysql://usuario:senha@host:porta/banco"
```

### Opção 3: Editar Diretamente o Código

Edite o arquivo `migrate_data.py` na linha 38:

```python
return "mysql+pymysql://usuario:senha@host:porta/banco"
```

## 🔍 Verificar Configuração

Execute o script para verificar a configuração atual:

```bash
python load_mysql_config.py
```

## ✅ Testar Conexão

Antes de migrar, teste a conexão:

```bash
python check_mysql.py
```

Este script irá:
- Testar a conexão
- Listar tabelas disponíveis
- Contar registros em cada tabela

## 🚀 Executar Migração

Após configurar e testar:

```bash
python migrate_data.py
```

## ⚠️ Problemas Comuns

### Erro: "Can't connect to MySQL server"

**Soluções:**
1. Verifique se o MySQL está rodando
2. Verifique se o host/porta estão corretos
3. Verifique firewall/rede (se for servidor remoto)
4. Verifique se o usuário tem permissões

### Erro: "Access denied"

**Soluções:**
1. Verifique usuário e senha
2. Verifique se o usuário tem acesso ao banco
3. Tente conectar manualmente com MySQL Workbench ou cliente similar

### Erro: "Unknown database"

**Soluções:**
1. Verifique se o nome do banco está correto
2. Crie o banco se não existir: `CREATE DATABASE dbarqmanager;`

## 📝 Exemplo Completo

```bash
# 1. Criar arquivo .mysql_config
echo "MYSQL_URL=mysql+pymysql://root:senha123@localhost:3306/dbarqmanager" > .mysql_config

# 2. Verificar configuração
python load_mysql_config.py

# 3. Testar conexão
python check_mysql.py

# 4. Executar migração
python migrate_data.py

# 5. Corrigir sequences
python fix_all_sequences.py
```




