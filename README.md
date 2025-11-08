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

## 🔧 Instalação

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

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas configurações.

### 6. Execute as migrations

```bash
alembic upgrade head
```

### 7. Inicie o servidor

```bash
uvicorn app.main:app --reload
```

A API estará disponível em: `http://localhost:8000`

## 📚 Documentação

-   **Swagger UI**: http://localhost:8000/docs
-   **ReDoc**: http://localhost:8000/redoc

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
├── tests/
├── .env
├── .env.example
├── requirements.txt
└── README.md
```

## 🔐 Autenticação

A API usa JWT (JSON Web Tokens) para autenticação.

### Login

```bash
POST /api/v1/auth/login
{
  "email": "user@example.com",
  "password": "password"
}
```

### Usar o token

```bash
Authorization: Bearer <token>
```

## 📝 Licença

Propriedade de ARQManager © 2025
