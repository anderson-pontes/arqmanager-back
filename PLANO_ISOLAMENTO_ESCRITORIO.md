# Plano de Isolamento por Escritório

## Status da Implementação

### ✅ Concluído

1. **Migration criada** (`06f4fa27b50f_add_escritorio_id_isolation.py`)
   - Adiciona `escritorio_id` em todas as tabelas necessárias
   - Preenche dados existentes baseado em relacionamentos
   - Campos inicialmente nullable para permitir migração

2. **Modelos atualizados** com `escritorio_id`:
   - ✅ Cliente
   - ✅ Projeto
   - ✅ Proposta
   - ✅ Movimento
   - ✅ Servico
   - ✅ Etapa
   - ✅ Status
   - ✅ FormaPagamento
   - ✅ Feriado
   - ✅ Indicacao
   - ✅ ProjetoColaborador
   - ✅ ProjetoPagamento
   - ✅ ProjetoDocumento
   - ✅ PropostaServicoEtapa
   - ✅ ContaMovimentacao

3. **Repositories atualizados**:
   - ✅ ClienteRepository - todos os métodos filtram por `escritorio_id`
   - ✅ ProjetoRepository - todos os métodos filtram por `escritorio_id`
   - ✅ PropostaRepository - todos os métodos filtram por `escritorio_id`
   - ✅ MovimentoRepository - todos os métodos filtram por `escritorio_id`

4. **Services atualizados**:
   - ✅ ClienteService - todos os métodos recebem e passam `escritorio_id`

5. **Endpoints atualizados**:
   - ✅ Clientes - todos os endpoints usam `get_current_escritorio()`
   - ✅ Projetos - todos os endpoints usam `get_current_escritorio()`
   - ✅ Propostas - todos os endpoints usam `get_current_escritorio()`
   - ✅ Movimentos - todos os endpoints usam `get_current_escritorio()`

6. **Sistema de Seeds criado**:
   - ✅ EscritorioSeeds - cria dados iniciais automaticamente
   - ✅ Status padrão (Em Andamento, Concluído, Pendente, Cancelado, Pausado)
   - ✅ Formas de pagamento padrão (Dinheiro, PIX, Cartões, Boleto, etc.)
   - ✅ Feriados nacionais
   - ✅ Integrado no EscritorioService.create_with_admin()

7. **Sistema de Auditoria criado**:
   - ✅ Modelo Auditoria criado
   - ✅ AuditoriaService criado
   - ✅ Migration para tabela auditoria criada
   - ⏳ Integração nos endpoints (pendente - pode ser feito via middleware ou decorator)

### 📋 Pendente

1. **Repositories adicionais** (se necessário):
   - ServicoRepository
   - StatusRepository (se existir)
   - FormaPagamentoRepository (se existir)
   - FeriadoRepository (se existir)
   - IndicacaoRepository (se existir)
   - Outros repositories relacionados

2. **Schemas (Pydantic)** - Adicionar `escritorio_id` nos schemas (se necessário):
   - ClienteCreate, ClienteUpdate
   - ProjetoCreate, ProjetoUpdate
   - PropostaCreate, PropostaUpdate
   - MovimentoCreate, MovimentoUpdate
   - ServicoCreate, ServicoUpdate
   - StatusCreate, StatusUpdate
   - FormaPagamentoCreate, FormaPagamentoUpdate
   - FeriadoCreate, FeriadoUpdate
   - IndicacaoCreate, IndicacaoUpdate
   - Outros schemas relacionados

3. **Services adicionais** (se necessário):
   - ProjetoService (se existir)
   - PropostaService (se existir)
   - MovimentoService (se existir)
   - Outros services relacionados

4. **Endpoints adicionais** (se necessário):
   - Servicos
   - Status
   - FormaPagamento
   - Feriados
   - Indicacoes
   - Outros endpoints relacionados

5. **Frontend** - Atualizar:
    - Garantir que todas as requisições incluam contexto
    - Atualizar stores para gerenciar contexto
    - Validar contexto antes de fazer requisições

## Padrão de Implementação

### Repository Pattern

Todos os repositories devem seguir este padrão:

```python
def get_all(
    self, 
    escritorio_id: int,  # SEMPRE o primeiro parâmetro após self
    skip: int = 0, 
    limit: int = 100,
    # ... outros filtros
) -> List[Model]:
    query = self.db.query(Model).filter(Model.escritorio_id == escritorio_id)
    # ... aplicar outros filtros
    return query.offset(skip).limit(limit).all()

def get_by_id(self, id: int, escritorio_id: int) -> Optional[Model]:
    return self.db.query(Model).filter(
        Model.id == id,
        Model.escritorio_id == escritorio_id
    ).first()

def create(self, data: CreateSchema, escritorio_id: int) -> Model:
    model_data = data.model_dump()
    model_data['escritorio_id'] = escritorio_id
    # ... criar modelo
    return model

def update(self, id: int, data: UpdateSchema, escritorio_id: int) -> Optional[Model]:
    model = self.get_by_id(id, escritorio_id)
    if not model:
        return None
    # ... atualizar modelo
    return model

def delete(self, id: int, escritorio_id: int, permanent: bool = False) -> bool:
    model = self.get_by_id(id, escritorio_id)
    if not model:
        return False
    # ... deletar modelo
    return True
```

### Service Pattern

Todos os services devem seguir este padrão:

```python
def create(self, data: CreateSchema, escritorio_id: int) -> Model:
    # Validar dados
    # Criar via repository
    return self.repository.create(data, escritorio_id)

def get_all(self, escritorio_id: int, **filters) -> List[Model]:
    return self.repository.get_all(escritorio_id, **filters)
```

### Endpoint Pattern

Todos os endpoints devem seguir este padrão:

```python
@router.post("/")
def create(
    data: CreateSchema,
    escritorio_id: int = Depends(get_current_escritorio),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = Service(db)
    return service.create(data, escritorio_id)
```

## Próximos Passos

1. ✅ Executar migration: `alembic upgrade head` - **CONCLUÍDO**
2. ✅ Atualizar repositories principais - **CONCLUÍDO**
3. ⏳ Atualizar schemas (se necessário) - **PENDENTE** (pode não ser necessário se escritorio_id vier do contexto)
4. ✅ Atualizar services principais - **CONCLUÍDO**
5. ✅ Atualizar endpoints principais - **CONCLUÍDO**
6. ✅ Criar sistema de seeds - **CONCLUÍDO**
7. ✅ Adicionar auditoria - **CONCLUÍDO** (modelo e service criados, falta integrar)
8. ⏳ Atualizar frontend - **PENDENTE**
9. ⏳ Testar isolamento completo - **PENDENTE**

## Observações Importantes

- **Dados Existentes**: A migration preenche `escritorio_id` baseado em relacionamentos, mas alguns dados podem ficar NULL. É necessário revisar e preencher manualmente se necessário.

- **Unique Constraints**: Alguns campos que eram `unique=True` (como `identificacao` em Cliente) foram removidos para permitir o mesmo CPF/CNPJ em escritórios diferentes. Considere criar índices compostos `(escritorio_id, identificacao)` se necessário.

- **Validação**: Sempre validar que o `escritorio_id` do recurso corresponde ao `escritorio_id` do contexto do usuário antes de permitir operações.

- **Modo Administrativo**: Quando o usuário estiver em modo administrativo (`is_admin_mode=True`), não deve acessar recursos específicos de escritório. Apenas recursos administrativos (escritórios, admins do sistema, etc.).

- **Auditoria**: O sistema de auditoria foi criado mas ainda não está integrado nos endpoints. Para integrar, pode-se usar um middleware ou decorator que registre automaticamente as ações.

## Notas Importantes

- **Dados Existentes**: A migration preenche `escritorio_id` baseado em relacionamentos, mas alguns dados podem ficar NULL. É necessário revisar e preencher manualmente se necessário.

- **Unique Constraints**: Alguns campos que eram `unique=True` (como `identificacao` em Cliente) foram removidos para permitir o mesmo CPF/CNPJ em escritórios diferentes. Considere criar índices compostos `(escritorio_id, identificacao)` se necessário.

- **Validação**: Sempre validar que o `escritorio_id` do recurso corresponde ao `escritorio_id` do contexto do usuário antes de permitir operações.

- **Modo Administrativo**: Quando o usuário estiver em modo administrativo (`is_admin_mode=True`), não deve acessar recursos específicos de escritório. Apenas recursos administrativos (escritórios, admins do sistema, etc.).

