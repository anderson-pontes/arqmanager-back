# ARQManager Backend API

Sistema de gestão para escritórios de arquitetura - Backend FastAPI

## 🚀 Tecnologias

-   **FastAPI** - Framework web moderno e rápido
-   **SQLAlchemy** - ORM para Python
-   **PostgreSQL** - Banco de dados
-   **Alembic** - Migrations
-   **Pydantic** - Validação de dados
-   **JWT** - Autenticação

## 📋 Pré-requisitos

-   Python 3.11+
-   PostgreSQL 14+
-   pip

## 🔧 Instalação e Configuração

### 1. Clone o repositório

```bash
cd arqmanager-backend
```

### 2. Crie um ambiente virtual

```bash
python -m venv venv
```

### 3. Ative o ambiente virtual

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/Mac:**

```bash
source venv/bin/activate
```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

### 5. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# Database
DATABASE_URL=postgresql://usuario:senha@localhost:5432/arqmanager

# Security
SECRET_KEY=sua-chave-secreta-aqui-gerar-uma-chave-aleatoria-forte
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=True
ENVIRONMENT=development

# CORS (opcional - ajuste conforme necessário)
CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]

# Upload
UPLOAD_DIR=./uploads
MAX_UPLOAD_SIZE=10485760
```

**Importante:**
- Substitua `usuario`, `senha` e `arqmanager` pelos dados do seu banco PostgreSQL
- Gere uma `SECRET_KEY` forte e aleatória (pode usar: `python -c "import secrets; print(secrets.token_urlsafe(32))"`)

### 6. Crie o banco de dados

Certifique-se de que o PostgreSQL está rodando e crie o banco de dados:

```sql
CREATE DATABASE arqmanager;
```

### 7. Execute as migrations

```bash
alembic upgrade head
```

Isso criará todas as tabelas necessárias no banco de dados.

### 8. Crie um administrador do sistema

Após configurar o banco de dados, você precisa criar pelo menos um usuário administrador do sistema:

```bash
python scripts/create_system_admin.py
```

O script irá solicitar:
- **Nome completo**: Nome do administrador
- **Email**: Email único para login
- **CPF**: CPF (apenas números, sem pontos ou traços)
- **Senha**: Senha com mínimo de 6 caracteres

**Exemplo:**
```
Nome completo: Administrador Sistema
Email: admin@arqmanager.com
CPF (apenas números): 12345678900
Senha (mínimo 6 caracteres): admin123
```

**Nota:** O administrador do sistema tem acesso total à aplicação, incluindo:
- Gerenciamento de escritórios
- Criação de outros administradores
- Acesso a todas as funcionalidades administrativas

### 9. Inicie o servidor

```bash
uvicorn app.main:app --reload
```

A API estará disponível em: `http://localhost:8000`

**Para produção**, use:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 📚 Documentação

-   **Swagger UI**: http://localhost:8000/docs
-   **ReDoc**: http://localhost:8000/redoc

## 🔐 Autenticação

A API usa JWT (JSON Web Tokens) para autenticação.

### Login

```bash
POST /api/v1/auth/login
{
  "email": "user@example.com",
  "senha": "password"
}
```

### Usar o token

```bash
Authorization: Bearer <token>
```

## 👤 Criar Administrador do Sistema

### Método 1: Script Interativo (Recomendado)

```bash
python scripts/create_system_admin.py
```

Este script solicita os dados interativamente e valida:
- Email único no sistema
- CPF único (se fornecido)
- Senha com mínimo de 6 caracteres

### Método 2: Via API (requer admin existente)

Se você já tem um administrador do sistema, pode criar outros via API:

```bash
POST /api/v1/admin/system-admin
Authorization: Bearer <token-do-admin>
{
  "nome": "Novo Admin",
  "email": "novo@admin.com",
  "cpf": "12345678900",
  "senha": "senha123"
}
```

### Método 3: Script Automático (para testes)

```bash
python scripts/create_system_admin_auto.py --nome "Admin" --email "admin@test.com" --cpf "12345678900" --senha "admin123"
```

## 🧪 Testes

```bash
pytest
```

## 📁 Estrutura do Projeto

```
arqmanager-backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       └── api.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── exceptions.py
│   ├── models/
│   ├── schemas/
│   ├── repositories/
│   ├── services/
│   ├── utils/
│   ├── database.py
│   └── main.py
├── alembic/
│   └── versions/
├── scripts/
│   ├── create_system_admin.py
│   ├── create_system_admin_auto.py
│   └── check_and_create_admin.py
├── tests/
├── uploads/
├── .env
├── requirements.txt
└── README.md
```

## 🛠️ Comandos Úteis

### Criar nova migration

```bash
alembic revision --autogenerate -m "descricao da migration"
```

### Aplicar migrations

```bash
alembic upgrade head
```

### Reverter última migration

```bash
alembic downgrade -1
```

### Ver status das migrations

```bash
alembic current
alembic history
```

## ⚠️ Troubleshooting

### Erro de conexão com banco de dados

- Verifique se o PostgreSQL está rodando
- Confirme as credenciais no arquivo `.env`
- Verifique se o banco de dados foi criado

### Erro ao executar migrations

- Certifique-se de que o banco de dados existe
- Verifique se o usuário PostgreSQL tem permissões adequadas
- Tente executar `alembic upgrade head` novamente

### Erro ao criar administrador

- Verifique se as migrations foram executadas
- Confirme que o email/CPF não está duplicado
- Verifique os logs de erro para mais detalhes

### Porta 8000 já em uso

- Altere a porta no arquivo `.env` (PORT=8001)
- Ou pare o processo que está usando a porta 8000

## 📝 Licença

Propriedade de ARQManager © 2025
