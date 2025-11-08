# 🚀 Plano de Migração ARQManager - PHP para FastAPI

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Análise do Sistema Atual](#análise-do-sistema-atual)
3. [Arquitetura do Novo Backend](#arquitetura-do-novo-backend)
4. [Estrutura do Projeto](#estrutura-do-projeto)
5. [Roadmap de Implementação](#roadmap-de-implementação)
6. [Stack Tecnológica](#stack-tecnológica)
7. [Guia de Implementação por Módulo](#guia-de-implementação-por-módulo)

---

## 1. Visão Geral

### 1.1 Objetivo

Migrar o sistema ARQManager de PHP (monolítico) para uma arquitetura moderna com:

-   **Backend**: FastAPI (Python)
-   **Frontend**: React + TypeScript (já em desenvolvimento)
-   **Banco de Dados**: PostgreSQL (mantém estrutura atual)

### 1.2 Estratégia de Migração

**Abordagem**: Desenvolvimento incremental por módulos

**Fases**:

1. ✅ **Fase 1**: Frontend React com dados mock (CONCLUÍDA)
2. 🔄 **Fase 2**: Backend FastAPI por módulos (EM PLANEJAMENTO)
3. 🔜 **Fase 3**: Integração progressiva
4. 🔜 **Fase 4**: Migração de dados e homologação
5. 🔜 **Fase 5**: Deploy e transição

### 1.3 Princípios

-   ✅ Manter todas as funcionalidades existentes
-   ✅ Melhorar performance e escalabilidade
-   ✅ Código limpo e testável
-   ✅ Documentação automática (OpenAPI/Swagger)
-   ✅ Segurança aprimorada
-   ✅ API RESTful padronizada

---

## 2. Análise do Sistema Atual (PHP)

### 2.1 Estrutura de Módulos Identificada

**Módulos Principais**:

-   `principal/` - Gestão de Projetos, Propostas, Clientes
-   `acesso/` - Autenticação e Permissões
-   `apoio/` - Serviços, Etapas, Status, Feriados
-   `config/` - Configurações do Escritório
-   `log/` - Auditoria e Logs

**Funcionalidades Core**:

-   Gestão de Clientes
-   Gestão de Colaboradores
-   Gestão de Projetos e Propostas
-   Gestão Financeira (Contas, Movimentações, Pagamentos)
-   Gestão de Serviços e Etapas
-   Gestão de Documentos
-   Reuniões e Atas
-   Relatórios e Dashboard
-   Área do Cliente
-   Notificações (Email/WhatsApp)

### 2.2 Banco de Dados

**Tabelas Principais** (40+ tabelas):

**Core**:

-   `escritorio`, `colaborador`, `cliente`
-   `projeto`, `proposta`, `servico`
-   `status`, `etapa`, `servico_etapa`

**Financeiro**:

-   `conta_bancaria`, `conta_movimentacao`
-   `projeto_pagamento`, `forma_pagamento`
-   `plano_contas`

**Documentos e Comunicação**:

-   `documento`, `projeto_documento`
-   `reuniao`, `reuniao_manifestacao`
-   `email`, `email_tipo`

**Controle**:

-   `acesso_grupo`, `acesso_permissao_grupo`
-   `feriados`, `alerta`

---

## 3. Arquitetura do Novo Backend

### 3.1 Padrão Arquitetural

**Clean Architecture + Repository Pattern**

```

```

├── API Layer (FastAPI Routes)
│ └── Endpoints REST
├── Service Layer (Business Logic)
│ └── Regras de Negócio
├── Repository Layer (Data Access)
│ └── SQLAlchemy ORM
└── Database Layer (PostgreSQL)
└── Tabelas e Views

```

### 3.2 Camadas

**1. API Layer** (`app/api/v1/endpoints/`)
- Routers FastAPI
- Validação de entrada (Pydantic)
- Documentação automática
- Tratamento de erros HTTP

**2. Service Layer** (`app/services/`)
- Lógica de negócio
- Orquestração de operações
- Validações complexas
- Transações

**3. Repository Layer** (`app/repositories/`)
- Acesso ao banco de dados
- Queries SQLAlchemy
- CRUD operations
- Filtros e paginação

**4. Models Layer** (`app/models/`)
- SQLAlchemy Models
- Relacionamentos
- Constraints

**5. Schemas Layer** (`app/schemas/`)
- Pydantic Models
- Validação de dados
- Serialização/Deserialização

---

## 4. Estrutura do Projeto

```

arqmanager-backend/
├── app/
│ ├── **init**.py
│ ├── main.py # Aplicação FastAPI
│ ├── config.py # Configurações
│ ├── database.py # Conexão DB
│ │
│ ├── api/
│ │ ├── **init**.py
│ │ ├── deps.py # Dependências
│ │ └── v1/
│ │ ├── **init**.py
│ │ ├── api.py # Router principal
│ │ └── endpoints/
│ │ ├── auth.py
│ │ ├── users.py
│ │ ├── clientes.py
│ │ ├── projetos.py
│ │ ├── propostas.py
│ │ ├── financeiro.py
│ │ └── ...
│ │
│ ├── core/
│ │ ├── **init**.py
│ │ ├── security.py # JWT, Hash
│ │ ├── config.py # Settings
│ │ └── exceptions.py # Custom Exceptions
│ │
│ ├── models/
│ │ ├── **init**.py
│ │ ├── base.py
│ │ ├── user.py
│ │ ├── cliente.py
│ │ ├── projeto.py
│ │ └── ...
│ │
│ ├── schemas/
│ │ ├── **init**.py
│ │ ├── user.py
│ │ ├── cliente.py
│ │ ├── projeto.py
│ │ └── ...
│ │
│ ├── repositories/
│ │ ├── **init**.py
│ │ ├── base.py
│ │ ├── user.py
│ │ ├── cliente.py
│ │ └── ...
│ │
│ ├── services/
│ │ ├── **init**.py
│ │ ├── auth.py
│ │ ├── cliente.py
│ │ ├── projeto.py
│ │ └── ...
│ │
│ └── utils/
│ ├── **init**.py
│ ├── validators.py
│ ├── formatters.py
│ └── email.py
│
├── alembic/ # Migrations
│ ├── versions/
│ └── env.py
│
├── tests/
│ ├── **init**.py
│ ├── conftest.py
│ ├── test_auth.py
│ └── ...
│
├── .env.example
├── .gitignore
├── alembic.ini
├── pyproject.toml
├── requirements.txt
└── README.md

```

---

## 5. Roadmap de Implementação

### FASE 1: Setup Inicial (Semana 1)

**Objetivo**: Estrutura base do projeto

**Tarefas**:
- [ ] Criar estrutura de pastas
- [ ] Configurar ambiente virtual Python
- [ ] Instalar dependências (FastAPI, SQLAlchemy, etc.)
- [ ] Configurar variáveis de ambiente
- [ ] Setup do banco de dados
- [ ] Configurar Alembic (migrations)
- [ ] Criar modelos base (Base, TimestampMixin)
- [ ] Implementar sistema de autenticação JWT
- [ ] Configurar CORS
- [ ] Documentação Swagger/OpenAPI

**Entregáveis**:
- ✅ Projeto FastAPI rodando
- ✅ Conexão com banco de dados
- ✅ Documentação automática em `/docs`
- ✅ Endpoint de health check

---

### FASE 2: Autenticação e Usuários (Semana 2)

**Objetivo**: Sistema de autenticação completo

**Módulos**:
- Autenticação (Login, Logout, Refresh Token)
- Gestão de Usuários/Colaboradores
- Permissões e Grupos de Acesso
- Escritórios (Multi-tenant)

**Endpoints**:
```

POST /api/v1/auth/login
POST /api/v1/auth/refresh
POST /api/v1/auth/logout
GET /api/v1/auth/me

GET /api/v1/users
POST /api/v1/users
GET /api/v1/users/{id}
PUT /api/v1/users/{id}
DELETE /api/v1/users/{id}

GET /api/v1/escritorios
GET /api/v1/escritorios/{id}
PUT /api/v1/escritorios/{id}

```

**Models**:
- `User` (Colaborador)
- `Escritorio`
- `UserEscritorio` (relação many-to-many)
- `AcessoGrupo`
- `AcessoPermissao`

---

### FASE 3: Clientes (Semana 3)

**Objetivo**: CRUD completo de clientes

**Endpoints**:
```

GET /api/v1/clientes
POST /api/v1/clientes
GET /api/v1/clientes/{id}
PUT /api/v1/clientes/{id}
DELETE /api/v1/clientes/{id}
GET /api/v1/clientes/search?q=nome

```

**Features**:
- Listagem com paginação
- Filtros (ativo, tipo pessoa, cidade)
- Busca por nome/documento
- Validação de CPF/CNPJ
- Soft delete
- Auditoria (created_at, updated_at)

**Models**:
- `Cliente`
- `Endereco` (embedded ou tabela separada)

---

### FASE 4: Serviços e Etapas (Semana 4)

**Objetivo**: Gestão de serviços oferecidos

**Endpoints**:
```

GET /api/v1/servicos
POST /api/v1/servicos
GET /api/v1/servicos/{id}
PUT /api/v1/servicos/{id}
DELETE /api/v1/servicos/{id}

GET /api/v1/servicos/{id}/etapas
POST /api/v1/servicos/{id}/etapas
PUT /api/v1/etapas/{id}
DELETE /api/v1/etapas/{id}

GET /api/v1/servicos/{id}/microservicos
POST /api/v1/servicos/{id}/microservicos

```

**Models**:
- `Servico`
- `ServicoEtapa`
- `ServicoMicroservico`

---

### FASE 5: Propostas (Semana 5)

**Objetivo**: Sistema de propostas/orçamentos

**Endpoints**:
```

GET /api/v1/propostas
POST /api/v1/propostas
GET /api/v1/propostas/{id}
PUT /api/v1/propostas/{id}
DELETE /api/v1/propostas/{id}
POST /api/v1/propostas/{id}/converter-projeto
POST /api/v1/propostas/{id}/duplicar
GET /api/v1/propostas/{id}/pdf

```

**Features**:
- Geração de número automático
- Cálculo de valores
- Etapas da proposta
- Conversão para projeto
- Geração de PDF
- Histórico de status

**Models**:
- `Proposta`
- `PropostaEtapa`
- `PropostaMicroservico`

---

### FASE 6: Projetos (Semanas 6-7)

**Objetivo**: Gestão completa de projetos

**Endpoints**:
```

GET /api/v1/projetos
POST /api/v1/projetos
GET /api/v1/projetos/{id}
PUT /api/v1/projetos/{id}
DELETE /api/v1/projetos/{id}

GET /api/v1/projetos/{id}/etapas
POST /api/v1/projetos/{id}/etapas
PUT /api/v1/projetos/{id}/etapas/{etapa_id}

GET /api/v1/projetos/{id}/documentos
POST /api/v1/projetos/{id}/documentos
DELETE /api/v1/projetos/{id}/documentos/{doc_id}

GET /api/v1/projetos/{id}/equipe
POST /api/v1/projetos/{id}/equipe
DELETE /api/v1/projetos/{id}/equipe/{user_id}

GET /api/v1/projetos/{id}/timeline

```

**Features**:
- Gestão de etapas
- Upload de documentos
- Equipe do projeto
- Timeline/histórico
- Cálculo de prazos
- Alertas de atraso

**Models**:
- `Projeto`
- `ProjetoEtapa`
- `ProjetoDocumento`
- `ProjetoColaborador`
- `ProjetoTimeline`

---

### FASE 7: Financeiro (Semanas 8-9)

**Objetivo**: Gestão financeira completa

**Endpoints**:
```

# Contas Bancárias

GET /api/v1/contas
POST /api/v1/contas
GET /api/v1/contas/{id}
PUT /api/v1/contas/{id}
GET /api/v1/contas/{id}/saldo

# Movimentações

GET /api/v1/movimentacoes
POST /api/v1/movimentacoes
GET /api/v1/movimentacoes/{id}
PUT /api/v1/movimentacoes/{id}
DELETE /api/v1/movimentacoes/{id}

# Pagamentos de Projeto

GET /api/v1/projetos/{id}/pagamentos
POST /api/v1/projetos/{id}/pagamentos
PUT /api/v1/pagamentos/{id}
POST /api/v1/pagamentos/{id}/efetivar

# Relatórios

GET /api/v1/financeiro/dashboard
GET /api/v1/financeiro/fluxo-caixa
GET /api/v1/financeiro/relatorio-mensal

```

**Features**:
- Contas bancárias
- Movimentações (receitas/despesas)
- Pagamentos de projetos
- Conciliação bancária
- Relatórios financeiros
- Dashboard financeiro

**Models**:
- `ContaBancaria`
- `ContaMovimentacao`
- `ProjetoPagamento`
- `PlanoContas`
- `CategoriaFinanceira`

---

### FASE 8: Reuniões e Documentos (Semana 10)

**Objetivo**: Gestão de reuniões e documentação

**Endpoints**:
```

GET /api/v1/reunioes
POST /api/v1/reunioes
GET /api/v1/reunioes/{id}
PUT /api/v1/reunioes/{id}

POST /api/v1/reunioes/{id}/manifestacoes
GET /api/v1/reunioes/{id}/ata

GET /api/v1/documentos
POST /api/v1/documentos/upload
GET /api/v1/documentos/{id}/download

```

**Models**:
- `Reuniao`
- `ReuniaoManifestacao`
- `Documento`
- `DocumentoTipo`

---

### FASE 9: Dashboard e Relatórios (Semana 11)

**Objetivo**: Dashboards e relatórios gerenciais

**Endpoints**:
```

GET /api/v1/dashboard/estatisticas
GET /api/v1/dashboard/projetos-ativos
GET /api/v1/dashboard/projetos-atrasados
GET /api/v1/dashboard/aniversariantes
GET /api/v1/dashboard/pagamentos-pendentes

GET /api/v1/relatorios/projetos
GET /api/v1/relatorios/financeiro
GET /api/v1/relatorios/produtividade

```

---

### FASE 10: Área do Cliente (Semana 12)

**Objetivo**: Portal para clientes

**Endpoints**:
```

POST /api/v1/cliente/auth/login
GET /api/v1/cliente/projetos
GET /api/v1/cliente/projetos/{id}
GET /api/v1/cliente/projetos/{id}/documentos
GET /api/v1/cliente/projetos/{id}/pagamentos
GET /api/v1/cliente/reunioes
POST /api/v1/cliente/reunioes/{id}/confirmar

````

---

### FASE 11: Notificações (Semana 13)

**Objetivo**: Sistema de notificações

**Features**:
- Email (SMTP)
- WhatsApp (API)
- Notificações in-app
- Templates personalizáveis
- Agendamento de envios

---

### FASE 12: Testes e Documentação (Semana 14)

**Objetivo**: Qualidade e documentação

**Tarefas**:
- [ ] Testes unitários (pytest)
- [ ] Testes de integração
- [ ] Documentação da API
- [ ] Guia de deploy
- [ ] Scripts de migração de dados

---

## 6. Stack Tecnológica

### 6.1 Core

```python
# requirements.txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0
````

### 6.2 Banco de Dados

```python
sqlalchemy==2.0.23
alembic==1.12.1
psycopg2-binary==2.9.9
```

### 6.3 Validação e Serialização

```python
pydantic==2.5.0
pydantic-settings==2.1.0
email-validator==2.1.0
```

### 6.4 Utilitários

```python
python-dateutil==2.8.2
pytz==2023.3
```

### 6.5 Testes

```python
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
```

### 6.6 Documentação

```python
mkdocs==1.5.3
mkdocs-material==9.5.0
```

---

## 7. Guia de Implementação por Módulo

### 7.1 Exemplo: Módulo de Clientes

#### 1. Model (SQLAlchemy)

```python
# app/models/cliente.py
from sqlalchemy import Column, Integer, String, Boolean, Date, Enum
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin

class Cliente(Base, TimestampMixin):
    __tablename__ = "cliente"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False, index=True)
    razao_social = Column(String(255))
    email = Column(String(255), nullable=False, index=True)
    identificacao = Column(String(20), unique=True, index=True)
    tipo_pessoa = Column(Enum('Física', 'Jurídica'), nullable=False)
    telefone = Column(String(20))
    whatsapp = Column(String(20))
    data_nascimento = Column(Date)
    ativo = Column(Boolean, default=True)

    # Endereço (pode ser JSON ou tabela separada)
    logradouro = Column(String(255))
    numero = Column(String(20))
    complemento = Column(String(100))
    bairro = Column(String(100))
    cidade = Column(String(100))
    uf = Column(String(2))
    cep = Column(String(10))

    # Relacionamentos
    projetos = relationship("Projeto", back_populates="cliente")
    propostas = relationship("Proposta", back_populates="cliente")
```

#### 2. Schema (Pydantic)

```python
# app/schemas/cliente.py
from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import date
from enum import Enum

class TipoPessoa(str, Enum):
    FISICA = "Física"
    JURIDICA = "Jurídica"

class EnderecoBase(BaseModel):
    logradouro: str
    numero: str
    complemento: Optional[str] = None
    bairro: str
    cidade: str
    uf: str
    cep: str

class ClienteBase(BaseModel):
    nome: str
    razao_social: Optional[str] = None
    email: EmailStr
    identificacao: str
    tipo_pessoa: TipoPessoa
    telefone: str
    whatsapp: Optional[str] = None
    data_nascimento: Optional[date] = None
    endereco: EnderecoBase
    ativo: bool = True

    @validator('identificacao')
    def validate_documento(cls, v, values):
        tipo = values.get('tipo_pessoa')
        if tipo == TipoPessoa.FISICA:
            # Validar CPF
            pass
        else:
            # Validar CNPJ
            pass
        return v

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(ClienteBase):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    # ... outros campos opcionais

class ClienteInDB(ClienteBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ClienteResponse(ClienteInDB):
    pass
```

#### 3. Repository

```python
# app/repositories/cliente.py
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteUpdate
from typing import List, Optional

class ClienteRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        ativo: Optional[bool] = None,
        search: Optional[str] = None
    ) -> List[Cliente]:
        query = self.db.query(Cliente)

        if ativo is not None:
            query = query.filter(Cliente.ativo == ativo)

        if search:
            query = query.filter(
                or_(
                    Cliente.nome.ilike(f"%{search}%"),
                    Cliente.identificacao.ilike(f"%{search}%")
                )
            )

        return query.offset(skip).limit(limit).all()

    def get_by_id(self, cliente_id: int) -> Optional[Cliente]:
        return self.db.query(Cliente).filter(Cliente.id == cliente_id).first()

    def get_by_email(self, email: str) -> Optional[Cliente]:
        return self.db.query(Cliente).filter(Cliente.email == email).first()

    def create(self, cliente: ClienteCreate) -> Cliente:
        db_cliente = Cliente(**cliente.dict())
        self.db.add(db_cliente)
        self.db.commit()
        self.db.refresh(db_cliente)
        return db_cliente

    def update(self, cliente_id: int, cliente: ClienteUpdate) -> Optional[Cliente]:
        db_cliente = self.get_by_id(cliente_id)
        if not db_cliente:
            return None

        update_data = cliente.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_cliente, field, value)

        self.db.commit()
        self.db.refresh(db_cliente)
        return db_cliente

    def delete(self, cliente_id: int) -> bool:
        db_cliente = self.get_by_id(cliente_id)
        if not db_cliente:
            return False

        # Soft delete
        db_cliente.ativo = False
        self.db.commit()
        return True
```

#### 4. Service

```python
# app/services/cliente.py
from app.repositories.cliente import ClienteRepository
from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse
from app.core.exceptions import NotFoundException, ConflictException
from typing import List

class ClienteService:
    def __init__(self, repository: ClienteRepository):
        self.repository = repository

    def get_all(self, skip: int = 0, limit: int = 100, **filters) -> List[ClienteResponse]:
        clientes = self.repository.get_all(skip, limit, **filters)
        return [ClienteResponse.from_orm(c) for c in clientes]

    def get_by_id(self, cliente_id: int) -> ClienteResponse:
        cliente = self.repository.get_by_id(cliente_id)
        if not cliente:
            raise NotFoundException(f"Cliente {cliente_id} não encontrado")
        return ClienteResponse.from_orm(cliente)

    def create(self, cliente: ClienteCreate) -> ClienteResponse:
        # Verificar se email já existe
        existing = self.repository.get_by_email(cliente.email)
        if existing:
            raise ConflictException("Email já cadastrado")

        db_cliente = self.repository.create(cliente)
        return ClienteResponse.from_orm(db_cliente)

    def update(self, cliente_id: int, cliente: ClienteUpdate) -> ClienteResponse:
        db_cliente = self.repository.update(cliente_id, cliente)
        if not db_cliente:
            raise NotFoundException(f"Cliente {cliente_id} não encontrado")
        return ClienteResponse.from_orm(db_cliente)

    def delete(self, cliente_id: int) -> bool:
        success = self.repository.delete(cliente_id)
        if not success:
            raise NotFoundException(f"Cliente {cliente_id} não encontrado")
        return True
```

#### 5. Endpoint (FastAPI)

```python
# app/api/v1/endpoints/clientes.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.api.deps import get_db, get_current_user
from app.services.cliente import ClienteService
from app.repositories.cliente import ClienteRepository
from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse

router = APIRouter()

def get_cliente_service(db: Session = Depends(get_db)) -> ClienteService:
    repository = ClienteRepository(db)
    return ClienteService(repository)

@router.get("/", response_model=List[ClienteResponse])
def list_clientes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    ativo: Optional[bool] = None,
    search: Optional[str] = None,
    service: ClienteService = Depends(get_cliente_service),
    current_user = Depends(get_current_user)
):
    """Lista todos os clientes com filtros opcionais"""
    return service.get_all(skip=skip, limit=limit, ativo=ativo, search=search)

@router.post("/", response_model=ClienteResponse, status_code=201)
def create_cliente(
    cliente: ClienteCreate,
    service: ClienteService = Depends(get_cliente_service),
    current_user = Depends(get_current_user)
):
    """Cria um novo cliente"""
    return service.create(cliente)

@router.get("/{cliente_id}", response_model=ClienteResponse)
def get_cliente(
    cliente_id: int,
    service: ClienteService = Depends(get_cliente_service),
    current_user = Depends(get_current_user)
):
    """Busca um cliente por ID"""
    return service.get_by_id(cliente_id)

@router.put("/{cliente_id}", response_model=ClienteResponse)
def update_cliente(
    cliente_id: int,
    cliente: ClienteUpdate,
    service: ClienteService = Depends(get_cliente_service),
    current_user = Depends(get_current_user)
):
    """Atualiza um cliente"""
    return service.update(cliente_id, cliente)

@router.delete("/{cliente_id}", status_code=204)
def delete_cliente(
    cliente_id: int,
    service: ClienteService = Depends(get_cliente_service),
    current_user = Depends(get_current_user)
):
    """Remove um cliente (soft delete)"""
    service.delete(cliente_id)
```

---

## 8. Próximos Passos

### Imediato (Esta Semana)

1. [ ] Criar repositório `arqmanager-backend`
2. [ ] Setup inicial do projeto FastAPI
3. [ ] Configurar banco de dados
4. [ ] Implementar autenticação JWT
5. [ ] Criar primeiro endpoint (health check)

### Curto Prazo (Próximas 2 Semanas)

1. [ ] Implementar módulo de Clientes completo
2. [ ] Implementar módulo de Serviços
3. [ ] Testes unitários dos módulos
4. [ ] Documentação da API

### Médio Prazo (Próximo Mês)

1. [ ] Implementar todos os módulos core
2. [ ] Integração com frontend React
3. [ ] Testes de integração
4. [ ] Deploy em ambiente de homologação

---

**Data**: Janeiro 2025  
**Versão**: 1.0  
**Status**: 📋 EM PLANEJAMENTO
