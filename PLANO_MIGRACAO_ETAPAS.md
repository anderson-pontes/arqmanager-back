# 🚀 Plano de Migração ARQManager - PHP para FastAPI + React

## 📋 Índice

1. [Visão Geral](#1-visão-geral)
2. [Status Atual da Migração](#2-status-atual-da-migração)
3. [Análise do Sistema PHP](#3-análise-do-sistema-php)
4. [Estratégia de Migração por Etapas](#4-estratégia-de-migração-por-etapas)
5. [Detalhamento das Etapas](#5-detalhamento-das-etapas)
6. [Checklist de Migração](#6-checklist-de-migração)
7. [Riscos e Mitigações](#7-riscos-e-mitigações)

---

## 1. Visão Geral

### 1.1 Objetivo

Migrar o sistema **ARQManager** de uma arquitetura monolítica PHP para uma arquitetura moderna:

- **Backend**: FastAPI (Python) + PostgreSQL
- **Frontend**: React + TypeScript + Vite
- **Arquitetura**: API RESTful + SPA (Single Page Application)

### 1.2 Benefícios da Migração

- ✅ **Performance**: FastAPI é uma das frameworks mais rápidas do Python
- ✅ **Type Safety**: TypeScript no frontend + Pydantic no backend
- ✅ **Documentação Automática**: OpenAPI/Swagger integrado
- ✅ **Escalabilidade**: Arquitetura desacoplada permite escalar independentemente
- ✅ **Manutenibilidade**: Código mais limpo e testável
- ✅ **Modernidade**: Stack atualizada e com suporte ativo

### 1.3 Princípios da Migração

1. **Migração Incremental**: Módulo por módulo, sem interromper o sistema atual
2. **Compatibilidade**: Manter todas as funcionalidades existentes
3. **Melhoria Contínua**: Aproveitar para refatorar e melhorar
4. **Testes**: Cada módulo migrado deve ser testado antes de avançar
5. **Documentação**: Documentar cada etapa e decisão

---

## 2. Status Atual da Migração

### 2.1 ✅ O Que Já Foi Implementado

#### Backend (FastAPI)

- ✅ **Autenticação e Autorização**
  - JWT tokens com refresh token
  - Endpoints: `/api/v1/auth/login`, `/api/v1/auth/refresh`
  - Middleware de autenticação
  - Arquivos: `app/api/v1/endpoints/auth.py`, `app/services/auth.py`

- ✅ **Gestão de Clientes (CRUD Completo)**
  - Listagem com paginação, busca e filtros
  - Criação de Pessoa Física e Jurídica
  - Edição e exclusão (soft delete)
  - Validação de CPF/CNPJ
  - Arquivos: `app/models/cliente.py`, `app/schemas/cliente.py`, `app/repositories/cliente.py`, `app/services/cliente.py`, `app/api/v1/endpoints/clientes.py`

- ✅ **Banco de Dados**
  - PostgreSQL 17.5 configurado
  - Migração de dados do MySQL para PostgreSQL
  - Sequences corrigidas
  - Tabelas principais: `cliente`, `usuario`, `escritorio`

#### Frontend (React + TypeScript)

- ✅ **Autenticação**
  - Página de login funcional
  - Proteção de rotas
  - Gerenciamento de estado (Zustand)
  - Arquivos: `src/pages/auth/Login.tsx`, `src/hooks/useAuth.ts`, `src/api/services/auth.service.ts`

- ✅ **Gestão de Clientes**
  - Listagem com paginação e busca
  - Formulário de criação/edição
  - Página de detalhes
  - Arquivos: `src/pages/clientes/*`, `src/api/services/clientes.service.ts`

- ✅ **Layout e UI**
  - Layout responsivo com Sidebar e Header
  - Componentes shadcn/ui integrados
  - Paleta de cores profissional (Concrete + Bronze)
  - Arquivos: `src/components/layout/*`

### 2.2 🔄 Em Desenvolvimento

- 🔄 **Gestão Financeira** (parcial)
  - Contas bancárias (listagem)
  - Receitas e Despesas (formulários criados, integração pendente)

### 2.3 ❌ Ainda Não Migrado

**Módulos Principais**:
- ❌ Gestão de Projetos
- ❌ Gestão de Propostas/Orçamentos
- ❌ Gestão de Colaboradores (parcial)
- ❌ Gestão de Serviços e Etapas
- ❌ Gestão de Documentos
- ❌ Reuniões e Atas
- ❌ Relatórios e Dashboard
- ❌ Área do Cliente
- ❌ Notificações (Email/WhatsApp)
- ❌ Sistema de Permissões Completo
- ❌ Gestão de Escritórios (múltiplos escritórios)

**Módulos de Apoio**:
- ❌ Status, Feriados, FormaPagamento
- ❌ PlanoContas
- ❌ Configurações
- ❌ Configurações
- ❌ Colaboradores
---

## 3. Análise do Sistema PHP

### 3.1 Estrutura de Módulos Identificada

```
arqmanager/
├── modulos/
│   ├── principal/          # Módulos principais do negócio
│   │   ├── ClienteCTR.php
│   │   ├── ProjetoCTR.php
│   │   ├── PropostaCTR.php
│   │   ├── ColaboradorCTR.php
│   │   ├── ContaBancariaCTR.php
│   │   ├── ContaMovimentacaoCTR.php
│   │   ├── ServicoCTR.php
│   │   ├── EtapaCTR.php
│   │   ├── DocumentoCTR.php
│   │   ├── ReuniaoCTR.php
│   │   └── ...
│   ├── acesso/             # Autenticação e permissões
│   │   ├── AcessoGrupoCTR.php
│   │   ├── AcessoPermissaoGrupoCTR.php
│   │   └── ...
│   ├── apoio/              # Módulos de apoio
│   │   ├── StatusCTR.php
│   │   ├── FeriadosCTR.php
│   │   ├── FormaPagamentoCTR.php
│   │   └── ...
│   ├── config/             # Configurações
│   └── log/                # Auditoria
├── classes/                # Classes core
│   ├── bancoDeDados/      # Camada de acesso a dados
│   ├── persistencia/       # ORM customizado
│   └── utilitarios/        # Utilitários (PDF, Email, etc)
└── cliente/                # Área do cliente
```

### 3.2 Principais Entidades do Banco de Dados

**Core**:
- `escritorio`, `colaborador`, `cliente`
- `projeto`, `proposta`, `servico`, `etapa`
- `servico_etapa`, `servico_microservico`

**Financeiro**:
- `conta_bancaria`, `conta_movimentacao`
- `projeto_pagamento`, `forma_pagamento`
- `plano_contas`, `conta_bancaria_balanco`

**Documentos e Comunicação**:
- `documento`, `projeto_documento`, `documento_escritorio`
- `reuniao`, `reuniao_manifestacao`
- `email`, `email_tipo`, `email_tipo_escritorio`

**Controle e Apoio**:
- `acesso_grupo`, `acesso_permissao_grupo`, `acesso_modulo_transacao`
- `status`, `feriados`, `feriados_escritorio`
- `alerta`, `indicacao`, `justificativa`

**Relacionamentos Complexos**:
- `proposta_servico_etapa` (vincula proposta com etapas)
- `proposta_microservico` (vincula proposta com microserviços)
- `projeto_colaborador` (equipe do projeto)
- `colaborador_escritorio_grupo` (permissões por escritório)

### 3.3 Funcionalidades Complexas Identificadas

1. **Sistema de Propostas/Orçamentos**
   - Cálculo automático de prazos baseado em etapas
   - Microserviços com quantidades e dias
   - Conversão de proposta para projeto
   - Geração de PDF

2. **Gestão de Projetos**
   - Cronograma (Gantt) baseado em etapas
   - Controle de status (9 estados diferentes)
   - Arquivamento com justificativa
   - Timeline de atividades

3. **Sistema Financeiro**
   - Parcelas de pagamento vinculadas a projetos
   - Previsão vs Realizado
   - Acréscimos e descontos
   - Saldo do contrato

4. **Sistema de Permissões**
   - Grupos de acesso
   - Permissões por módulo/transação
   - Múltiplos escritórios com permissões isoladas

5. **Notificações**
   - Emails automáticos (PHPMailer)
   - WhatsApp (API externa)
   - Alertas do sistema

---

## 4. Estratégia de Migração por Etapas

### 4.1 Fases da Migração

```
┌─────────────────────────────────────────────────────────────┐
│ FASE 1: Fundação (✅ CONCLUÍDA)                              │
├─────────────────────────────────────────────────────────────┤
│ ✅ Autenticação e Autorização                                │
│ ✅ Estrutura base do projeto                                 │
│ ✅ Clientes (CRUD completo)                                  │
│ ✅ Banco de dados migrado                                    │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ FASE 2: Módulos de Apoio (🔄 EM ANDAMENTO)                  │
├─────────────────────────────────────────────────────────────┤
│ 🔄 Colaboradores (parcial)                                  │
│ 🔄 Contas Bancárias (listagem)                              │
│ ⏳ Status, Feriados, FormaPagamento                         │
│ ⏳ PlanoContas                                               │
│ ⏳ Configurações básicas                                     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ FASE 3: Gestão Financeira                                    │
├─────────────────────────────────────────────────────────────┤
│ ⏳ Contas Bancárias (CRUD completo)                         │
│ ⏳ Movimentações (Receitas/Despesas)                         │
│ ⏳ ProjetoPagamento (Parcelas)                               │
│ ⏳ Relatórios Financeiros                                    │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ FASE 4: Serviços e Etapas                                    │
├─────────────────────────────────────────────────────────────┤
│ ⏳ Serviços (CRUD)                                           │
│ ⏳ Etapas (CRUD)                                             │
│ ⏳ ServicoEtapa (vinculação)                                 │
│ ⏳ Microserviços                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ FASE 5: Propostas/Orçamentos                                │
├─────────────────────────────────────────────────────────────┤
│ ⏳ Propostas (CRUD)                                          │
│ ⏳ PropostaServicoEtapa                                      │
│ ⏳ PropostaMicroservico                                      │
│ ⏳ Cálculo de prazos                                         │
│ ⏳ Geração de PDF                                            │
│ ⏳ Conversão para Projeto                                    │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ FASE 6: Gestão de Projetos                                   │
├─────────────────────────────────────────────────────────────┤
│ ⏳ Projetos (CRUD)                                           │
│ ⏳ ProjetoColaborador (equipe)                               │
│ ⏳ Cronograma (Gantt)                                        │
│ ⏳ Timeline                                                  │
│ ⏳ Controle de Status                                        │
│ ⏳ Arquivamento                                              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ FASE 7: Documentos e Comunicação                             │
├─────────────────────────────────────────────────────────────┤
│ ⏳ Upload de Documentos                                      │
│ ⏳ ProjetoDocumento                                          │
│ ⏳ Reuniões e Atas                                           │
│ ⏳ Sistema de Emails                                         │
│ ⏳ Notificações                                              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ FASE 8: Sistema de Permissões                                │
├─────────────────────────────────────────────────────────────┤
│ ⏳ Grupos de Acesso                                          │
│ ⏳ Permissões por Módulo                                     │
│ ⏳ Múltiplos Escritórios                                     │
│ ⏳ Isolamento de Dados                                       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ FASE 9: Dashboard e Relatórios                              │
├─────────────────────────────────────────────────────────────┤
│ ⏳ Dashboard Principal                                       │
│ ⏳ Relatórios de Projetos                                    │
│ ⏳ Relatórios Financeiros                                    │
│ ⏳ Gráficos e Estatísticas                                   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ FASE 10: Área do Cliente e Finalização                       │
├─────────────────────────────────────────────────────────────┤
│ ⏳ Portal do Cliente                                         │
│ ⏳ Visualização de Projetos                                  │
│ ⏳ Aprovação de Propostas                                    │
│ ⏳ Testes de Integração                                      │
│ ⏳ Migração de Dados Final                                   │
│ ⏳ Deploy e Transição                                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Detalhamento das Etapas

### ETAPA 1: Módulos de Apoio (Prioridade Alta)

**Objetivo**: Criar a base de dados de apoio necessária para os módulos principais.

#### 1.1 Status
- **Backend**:
  - Model: `app/models/status.py`
  - Schema: `app/schemas/status.py`
  - Repository: `app/repositories/status.py`
  - Service: `app/services/status.py`
  - Endpoint: `app/api/v1/endpoints/status.py`
- **Frontend**:
  - Service: `src/api/services/status.service.ts`
  - Hook: `src/hooks/useStatus.ts` (opcional)
  - Componente: Select de Status reutilizável

#### 1.2 Feriados
- **Backend**: CRUD completo
- **Frontend**: Calendário com feriados marcados

#### 1.3 FormaPagamento
- **Backend**: CRUD completo
- **Frontend**: Select reutilizável

#### 1.4 PlanoContas
- **Backend**: CRUD completo (hierárquico)
- **Frontend**: Tree view para seleção

**Estimativa**: 1-2 semanas

---

### ETAPA 2: Gestão Financeira Completa

#### 2.1 Contas Bancárias (Completar)
- ✅ Listagem já existe
- ⏳ CRUD completo
- ⏳ Saldo atualizado em tempo real
- ⏳ Histórico de movimentações

#### 2.2 Movimentações (Receitas/Despesas)
- ✅ Formulários criados no frontend
- ⏳ Backend completo
- ⏳ Categorização
- ⏳ Filtros e relatórios

#### 2.3 ProjetoPagamento
- ⏳ Parcelas vinculadas a projetos
- ⏳ Controle de previsão vs realizado
- ⏳ Acréscimos e descontos
- ⏳ Cálculo de saldo do contrato

#### 2.4 Relatórios Financeiros
- ⏳ Fluxo de caixa
- ⏳ Receitas vs Despesas
- ⏳ Projeções
- ⏳ Exportação (PDF/Excel)

**Estimativa**: 2-3 semanas

---

### ETAPA 3: Serviços e Etapas

#### 3.1 Serviços
- ⏳ CRUD completo
- ⏳ Hierarquia de serviços
- ⏳ Valores padrão

#### 3.2 Etapas
- ⏳ CRUD completo
- ⏳ Prazos padrão
- ⏳ Ordem de execução

#### 3.3 ServicoEtapa
- ⏳ Vinculação serviço-etapa
- ⏳ Prazos customizados por serviço

#### 3.4 Microserviços
- ⏳ CRUD completo
- ⏳ Vinculação com serviços
- ⏳ Quantidades e dias

**Estimativa**: 2 semanas

---

### ETAPA 4: Propostas/Orçamentos

#### 4.1 Propostas (CRUD Base)
- ⏳ Criação, edição, listagem
- ⏳ Status de proposta
- ⏳ Vinculação com cliente

#### 4.2 PropostaServicoEtapa
- ⏳ Seleção de serviços e etapas
- ⏳ Cálculo automático de prazos
- ⏳ Valores por etapa

#### 4.3 PropostaMicroservico
- ⏳ Adição de microserviços
- ⏳ Quantidades e dias
- ⏳ Previsão de datas

#### 4.4 Funcionalidades Avançadas
- ⏳ Cálculo de prazos totais
- ⏳ Geração de PDF do orçamento
- ⏳ Conversão para projeto
- ⏳ Envio por email

**Estimativa**: 3-4 semanas

---

### ETAPA 5: Gestão de Projetos

#### 5.1 Projetos (CRUD Base)
- ⏳ Criação a partir de proposta ou do zero
- ⏳ Edição e listagem
- ⏳ Filtros avançados

#### 5.2 ProjetoColaborador
- ⏳ Alocação de equipe
- ⏳ Funções e responsabilidades
- ⏳ Carga horária

#### 5.3 Cronograma (Gantt)
- ⏳ Visualização de etapas
- ⏳ Dependências entre etapas
- ⏳ Ajuste de prazos
- ⏳ Biblioteca: react-gantt ou similar

#### 5.4 Timeline
- ⏳ Histórico de atividades
- ⏳ Mudanças de status
- ⏳ Uploads de documentos
- ⏳ Reuniões

#### 5.5 Controle de Status
- ⏳ 9 estados diferentes
- ⏳ Transições de status
- ⏳ Notificações automáticas

#### 5.6 Arquivamento
- ⏳ Justificativa obrigatória
- ⏳ Histórico preservado
- ⏳ Possibilidade de reabertura

**Estimativa**: 4-5 semanas

---

### ETAPA 6: Documentos e Comunicação

#### 6.1 Upload de Documentos
- ⏳ Backend: FastAPI com upload de arquivos
- ⏳ Frontend: Drag & drop
- ⏳ Validação de tipos e tamanhos
- ⏳ Armazenamento (local ou S3)

#### 6.2 ProjetoDocumento
- ⏳ Vinculação com projetos
- ⏳ Categorização
- ⏳ Versões

#### 6.3 Reuniões e Atas
- ⏳ CRUD de reuniões
- ⏳ Confirmação do cliente
- ⏳ Manifestações
- ⏳ Impacto no cronograma

#### 6.4 Sistema de Emails
- ⏳ Templates de email
- ⏳ Envio automático
- ⏳ Histórico de envios
- ⏳ Biblioteca: FastAPI-Mail ou similar

#### 6.5 Notificações
- ⏳ Notificações in-app
- ⏳ Emails automáticos
- ⏳ WhatsApp (opcional, API externa)

**Estimativa**: 3 semanas

---

### ETAPA 7: Sistema de Permissões

#### 7.1 Grupos de Acesso
- ⏳ CRUD de grupos
- ⏳ Hierarquia de grupos

#### 7.2 Permissões por Módulo
- ⏳ Definição de módulos/transações
- ⏳ Atribuição de permissões
- ⏳ Middleware de verificação

#### 7.3 Múltiplos Escritórios
- ⏳ Isolamento de dados por escritório
- ⏳ Troca de escritório (contexto)
- ⏳ Permissões por escritório

**Estimativa**: 2-3 semanas

---

### ETAPA 8: Dashboard e Relatórios

#### 8.1 Dashboard Principal
- ⏳ Cards de resumo
- ⏳ Gráficos (Chart.js ou Recharts)
- ⏳ Projetos em andamento
- ⏳ Pagamentos pendentes
- ⏳ Aniversariantes

#### 8.2 Relatórios de Projetos
- ⏳ Listagem filtrada
- ⏳ Exportação PDF/Excel
- ⏳ Gráficos de progresso

#### 8.3 Relatórios Financeiros
- ⏳ Fluxo de caixa
- ⏳ Receitas vs Despesas
- ⏳ Projeções

**Estimativa**: 2 semanas

---

### ETAPA 9: Área do Cliente

#### 9.1 Portal do Cliente
- ⏳ Autenticação separada
- ⏳ Visualização de projetos
- ⏳ Status em tempo real

#### 9.2 Aprovação de Propostas
- ⏳ Visualização de orçamentos
- ⏳ Aprovação/rejeição
- ⏳ Assinatura digital (opcional)

**Estimativa**: 2 semanas

---

### ETAPA 10: Finalização

#### 10.1 Testes de Integração
- ⏳ Testes end-to-end
- ⏳ Testes de carga
- ⏳ Testes de segurança

#### 10.2 Migração de Dados Final
- ⏳ Scripts de migração
- ⏳ Validação de integridade
- ⏳ Backup completo

#### 10.3 Deploy e Transição
- ⏳ Deploy em produção
- ⏳ Monitoramento
- ⏳ Suporte durante transição

**Estimativa**: 2-3 semanas

---

## 6. Checklist de Migração

### Para Cada Módulo Migrado

#### Backend
- [ ] Model criado (`app/models/`)
- [ ] Schema criado (`app/schemas/`)
- [ ] Repository criado (`app/repositories/`)
- [ ] Service criado (`app/services/`)
- [ ] Endpoints criados (`app/api/v1/endpoints/`)
- [ ] Testes unitários
- [ ] Documentação no Swagger
- [ ] Validações implementadas
- [ ] Tratamento de erros

#### Frontend
- [ ] Service criado (`src/api/services/`)
- [ ] Hook criado (se necessário) (`src/hooks/`)
- [ ] Páginas criadas (`src/pages/`)
- [ ] Componentes reutilizáveis
- [ ] Validação de formulários
- [ ] Tratamento de erros
- [ ] Loading states
- [ ] Responsividade

#### Integração
- [ ] Testes de integração
- [ ] Validação de dados
- [ ] Performance verificada
- [ ] Documentação atualizada

---

## 7. Riscos e Mitigações

### 7.1 Riscos Identificados

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| Perda de dados na migração | Alto | Baixo | Backups completos, scripts de validação |
| Incompatibilidade de funcionalidades | Médio | Médio | Testes detalhados, validação com usuários |
| Performance inferior | Médio | Baixo | Testes de carga, otimizações |
| Atraso no cronograma | Baixo | Alto | Planejamento realista, priorização |
| Resistência dos usuários | Médio | Médio | Treinamento, documentação clara |

### 7.2 Estratégias de Mitigação

1. **Backups Regulares**: Antes de cada etapa crítica
2. **Ambiente de Testes**: Separado do ambiente de produção
3. **Migração Gradual**: Módulo por módulo, sem interromper o sistema atual
4. **Validação Contínua**: Testes automatizados e manuais
5. **Documentação**: Manter documentação atualizada
6. **Comunicação**: Manter stakeholders informados

---

## 8. Próximos Passos Imediatos

### Prioridade 1 (Esta Semana)
1. ✅ Completar botões de voltar/cancelar em ReceitaForm e DespesaForm
2. ⏳ Completar CRUD de Contas Bancárias
3. ⏳ Implementar Status (módulo de apoio)

### Prioridade 2 (Próximas 2 Semanas)
1. ⏳ Implementar Feriados e FormaPagamento
2. ⏳ Completar Movimentações (Receitas/Despesas)
3. ⏳ Implementar PlanoContas

### Prioridade 3 (Próximo Mês)
1. ⏳ Iniciar módulo de Serviços e Etapas
2. ⏳ Planejar estrutura de Propostas

---

## 9. Recursos e Ferramentas

### Backend
- **FastAPI**: Framework web
- **SQLAlchemy**: ORM
- **Pydantic**: Validação
- **Alembic**: Migrações
- **PostgreSQL**: Banco de dados
- **Pytest**: Testes

### Frontend
- **React 18+**: Framework UI
- **TypeScript**: Tipagem
- **Vite**: Build tool
- **React Router**: Roteamento
- **Axios**: HTTP client
- **React Hook Form**: Formulários
- **Zod**: Validação
- **Shadcn/ui**: Componentes
- **Tailwind CSS**: Estilização

### Ferramentas de Desenvolvimento
- **Git**: Controle de versão
- **Docker** (opcional): Containerização
- **Postman/Insomnia**: Testes de API
- **Swagger/OpenAPI**: Documentação

---

## 10. Conclusão

Este plano de migração fornece um roadmap claro e detalhado para migrar o sistema ARQManager de PHP para FastAPI + React. A abordagem incremental permite migrar sem interromper o sistema atual, garantindo continuidade dos negócios.

**Estimativa Total**: 20-25 semanas (5-6 meses)

**Próxima Revisão**: Após conclusão da Fase 2 (Módulos de Apoio)

---

**Última atualização**: 2025-01-XX  
**Versão**: 1.0.0  
**Status**: Em planejamento ativo











