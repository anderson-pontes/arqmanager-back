# 🚀 Guia de Início Rápido - ARQManager Backend

## 📚 Documentação Disponível

👉 **Ver índice completo:** [INDICE_DOCUMENTACAO.md](INDICE_DOCUMENTACAO.md)

**Documentação Principal:**

-   **🚀 QUICK_START.md** (este arquivo) - Início rápido
-   **📖 README.md** - Documentação completa do projeto

**Migração de Dados:**

-   **🔄 README_MIGRACAO.md** - Visão geral da migração ⭐
-   **📖 GUIA_MIGRACAO_DADOS.md** - Guia detalhado
-   **✅ CHECKLIST_MIGRACAO.md** - Checklist passo a passo
-   **⚡ COMANDOS_MIGRACAO.md** - Referência rápida
-   **💡 EXEMPLOS_MIGRACAO.md** - Exemplos práticos

## ✅ Backend 100% Completo!

**7 Fases Implementadas** | **~55 Endpoints RESTful** | **10 Modelos** | **PostgreSQL**

### Módulos Disponíveis:

-   🔐 Autenticação JWT
-   👥 Usuários/Colaboradores
-   👤 Clientes (PF/PJ)
-   🛠️ Serviços e Etapas
-   📋 Projetos com Equipe
-   💰 Propostas/Orçamentos
-   💵 Movimentos Financeiros
-   📊 Status e Controles

## � Migxração de Dados MySQL → PostgreSQL

**Já tem dados no MySQL?** Siga o guia de migração:

1. 📖 Leia: `GUIA_MIGRACAO_DADOS.md`
2. ✅ Siga: `CHECKLIST_MIGRACAO.md`
3. 🚀 Execute: `python migrate_data.py`

**Arquivos de migração:**

-   `check_mysql.py` - Testa conexão MySQL
-   `migrate_data.py` - Executa migração
-   `check_migrated_data.py` - Verifica dados migrados

## 📋 Próximos Passos

### 1. Criar Ambiente Virtual

```bash
python -m venv venv
```

### 2. Ativar Ambiente Virtual

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/Mac:**

```bash
source venv/bin/activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar Banco de Dados

Crie um banco PostgreSQL:

```sql
CREATE DATABASE arqmanager;
CREATE USER arqmanager_user WITH PASSWORD 'sua_senha';
GRANT ALL PRIVILEGES ON DATABASE arqmanager TO arqmanager_user;
```

### 5. Configurar Variáveis de Ambiente

Copie o arquivo de exemplo:

```bash
copy .env.example .env
```

Edite o `.env` e configure:

```env
DATABASE_URL=postgresql://arqmanager_user:sua_senha@localhost:5432/arqmanager
SECRET_KEY=gere-uma-chave-secreta-aqui
```

**Gerar SECRET_KEY:**

```python
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 6. Testar a API

Inicie o servidor:

```bash
uvicorn app.main:app --reload
```

Acesse:

-   **API**: http://localhost:8000
-   **Documentação**: http://localhost:8000/docs
-   **Health Check**: http://localhost:8000/api/v1/health

### 7. Testar Health Check

```bash
curl http://localhost:8000/api/v1/health
```

Resposta esperada:

```json
{
    "status": "ok",
    "message": "ARQManager API is running"
}
```

## 🎯 O que foi implementado?

✅ **Estrutura de Pastas**

-   Organização Clean Architecture
-   Separação em camadas

✅ **Configurações**

-   Settings com Pydantic
-   Variáveis de ambiente
-   CORS configurado

✅ **Segurança**

-   JWT (tokens de acesso e refresh)
-   Hash de senhas (bcrypt)
-   Autenticação preparada

✅ **Banco de Dados**

-   SQLAlchemy configurado
-   Alembic para migrations
-   Models base com timestamps

✅ **API**

-   FastAPI configurado
-   Documentação automática (Swagger)
-   Health check endpoint
-   Exception handlers

✅ **Documentação**

-   README completo
-   Guia de instalação
-   Estrutura documentada

## 📁 Estrutura Criada

```
arqmanager-backend/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   ├── __init__.py
│   │   │   └── api.py
│   │   ├── __init__.py
│   │   └── deps.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── security.py
│   │   └── exceptions.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── base.py
│   ├── schemas/
│   │   └── __init__.py
│   ├── repositories/
│   │   └── __init__.py
│   ├── services/
│   │   └── __init__.py
│   ├── utils/
│   │   └── __init__.py
│   ├── __init__.py
│   ├── database.py
│   └── main.py
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── tests/
│   └── __init__.py
├── .env.example
├── .gitignore
├── alembic.ini
├── requirements.txt
├── README.md
├── QUICK_START.md
└── PLANO_MIGRACAO_FASTAPI.md
```

## 🔜 Próxima Fase

**Fase 2: Autenticação e Usuários**

Implementar:

-   [ ] Model User/Colaborador
-   [ ] Endpoints de autenticação (login, refresh)
-   [ ] Gestão de usuários
-   [ ] Permissões e grupos

Veja detalhes em `PLANO_MIGRACAO_FASTAPI.md`

## 🐛 Troubleshooting

### Erro ao instalar psycopg2

**Windows:**

```bash
pip install psycopg2-binary
```

### Erro de conexão com banco

Verifique:

1. PostgreSQL está rodando
2. Credenciais no `.env` estão corretas
3. Banco de dados foi criado

### Porta 8000 em uso

Altere a porta:

```bash
uvicorn app.main:app --reload --port 8001
```

## 📚 Recursos

-   **FastAPI Docs**: https://fastapi.tiangolo.com
-   **SQLAlchemy**: https://docs.sqlalchemy.org
-   **Alembic**: https://alembic.sqlalchemy.org
-   **Pydantic**: https://docs.pydantic.dev

---

**Status**: ✅ FASE 1 COMPLETA  
**Próximo**: Fase 2 - Autenticação e Usuários  
**Data**: Janeiro 2025
