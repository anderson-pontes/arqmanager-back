# 📊 Views do MySQL - Migração para PostgreSQL

## 🔍 O que são Views?

Views são **consultas SQL salvas** que funcionam como tabelas virtuais. Elas não armazenam dados, apenas definem como os dados devem ser consultados das tabelas reais.

## 📋 Views Encontradas no MySQL (27)

### Views de Dados Principais

-   `v_cliente` - Clientes com formatações
-   `v_projeto` - Projetos com informações relacionadas
-   `v_proposta` - Propostas com formatações
-   `v_movimento` - Movimentos financeiros formatados
-   `v_colaborador` - Colaboradores com informações completas

### Views de Relatórios

-   `v_financeiro_projeto` - Financeiro por projeto
-   `v_extrato_conta` - Extrato de contas
-   `v_extrato_conta_consolidado` - Extrato consolidado
-   `v_previsto_realizado` - Previsto vs Realizado

### Views Auxiliares

-   `v_aniversariantes` - Aniversariantes do mês
-   `v_feriados` - Feriados
-   `v_data` - Datas auxiliares
-   `v_mes` - Meses do ano
-   `v_permissao` - Permissões de usuários

### Views de Relacionamentos

-   `v_servico_etapa` - Serviços e etapas
-   `v_proposta_servico_etapa` - Propostas com etapas
-   `v_projeto_arquivamento` - Projetos arquivados
-   `v_projeto_rrt` - Projetos com RRT

### Outras Views

-   `v_ata` - Atas de reunião
-   `v_email_enviado` - Emails enviados
-   `v_indicacao` - Indicações
-   `v_plano_contas` - Plano de contas
-   `v_contas_escritorio` - Contas por escritório
-   `v_proposta_microservico` - Propostas com microserviços
-   `v_rrt_projeto` - RRT por projeto
-   `v_template_email_whatsapp` - Templates de comunicação

## ⚠️ Por que as Views NÃO foram migradas?

1. **Sintaxe Diferente**: MySQL e PostgreSQL têm sintaxes diferentes
2. **Funções Específicas**: Funções como `FORMAT()`, `CONCAT()` são diferentes
3. **Datas**: Formatação de datas é diferente entre os bancos
4. **Arquitetura Moderna**: No FastAPI, é melhor usar queries nos repositories

## 🎯 Abordagem Recomendada

### ❌ NÃO Recomendado

Migrar todas as 27 views automaticamente

### ✅ Recomendado

Recriar views **conforme necessidade** no PostgreSQL

## 💡 Como Trabalhar sem Views?

### Opção 1: Queries nos Repositories (Recomendado)

```python
# app/repositories/cliente.py
class ClienteRepository:
    def get_cliente_formatado(self, db: Session, cliente_id: int):
        return db.query(
            Cliente.id,
            Cliente.nome,
            Cliente.tipo_pessoa,
            case(
                (Cliente.tipo_pessoa == 'PF', 'Pessoa Física'),
                (Cliente.tipo_pessoa == 'PJ', 'Pessoa Jurídica'),
                else_='Não definida'
            ).label('tipo_pessoa_formatado')
        ).filter(Cliente.id == cliente_id).first()
```

### Opção 2: Criar Views PostgreSQL quando necessário

```sql
-- Criar view no PostgreSQL
CREATE OR REPLACE VIEW v_cliente AS
SELECT
    id as cod_cliente,
    nome,
    tipo_pessoa,
    CASE tipo_pessoa
        WHEN 'PF' THEN 'Pessoa Física'
        WHEN 'PJ' THEN 'Pessoa Jurídica'
        ELSE 'Não definida'
    END as tipo_pessoa_formatado,
    identificacao,
    REGEXP_REPLACE(identificacao, '[./-]', '', 'g') as identificacao_sem_mascara,
    email,
    telefone,
    whatsapp
FROM cliente
WHERE ativo = true;
```

### Opção 3: Usar Pydantic para Formatação

```python
# app/schemas/cliente.py
class ClienteResponse(BaseModel):
    id: int
    nome: str
    tipo_pessoa: str
    identificacao: str

    @property
    def tipo_pessoa_formatado(self) -> str:
        return {
            'PF': 'Pessoa Física',
            'PJ': 'Pessoa Jurídica'
        }.get(self.tipo_pessoa, 'Não definida')

    @property
    def identificacao_sem_mascara(self) -> str:
        return self.identificacao.replace('.', '').replace('-', '').replace('/', '')
```

## 🔧 Criando Views PostgreSQL

Se você realmente precisar de uma view, crie assim:

### 1. Criar arquivo de migration

```bash
alembic revision -m "create_view_cliente"
```

### 2. Adicionar SQL no arquivo de migration

```python
def upgrade():
    op.execute("""
        CREATE OR REPLACE VIEW v_cliente AS
        SELECT
            id,
            nome,
            tipo_pessoa,
            CASE tipo_pessoa
                WHEN 'PF' THEN 'Pessoa Física'
                WHEN 'PJ' THEN 'Pessoa Jurídica'
            END as tipo_pessoa_formatado
        FROM cliente
        WHERE ativo = true
    """)

def downgrade():
    op.execute("DROP VIEW IF EXISTS v_cliente")
```

### 3. Aplicar migration

```bash
alembic upgrade head
```

## 📊 Diferenças MySQL vs PostgreSQL

| Recurso          | MySQL                           | PostgreSQL                       |
| ---------------- | ------------------------------- | -------------------------------- |
| Concatenar       | `CONCAT(a, b)`                  | `a \|\| b` ou `CONCAT(a, b)`     |
| Formatar número  | `FORMAT(valor, 2, 'de_DE')`     | `TO_CHAR(valor, 'FM999G999D00')` |
| Formatar data    | `DATE_FORMAT(data, '%d/%m/%Y')` | `TO_CHAR(data, 'DD/MM/YYYY')`    |
| Case insensitive | `LIKE`                          | `ILIKE`                          |
| Regex replace    | `REPLACE()` múltiplos           | `REGEXP_REPLACE()`               |
| Aspas            | \`campo\`                       | "campo"                          |

## 🎯 Exemplo Prático: Migrar v_cliente

### MySQL Original

```sql
CREATE VIEW v_cliente AS
SELECT
    cod_cliente,
    nome,
    CONCAT(ano, '/', LPAD(numero, 3, '0')) AS numero_formatado,
    FORMAT(valor, 2, 'de_DE') AS valor_formatado
FROM cliente;
```

### PostgreSQL Adaptado

```sql
CREATE OR REPLACE VIEW v_cliente AS
SELECT
    id as cod_cliente,
    nome,
    ano || '/' || LPAD(numero::text, 3, '0') AS numero_formatado,
    TO_CHAR(valor, 'FM999G999D00') AS valor_formatado
FROM cliente;
```

## 📝 Recomendação Final

**Para o novo sistema FastAPI:**

1. ✅ **Use repositories** para queries complexas
2. ✅ **Use Pydantic** para formatações
3. ✅ **Crie views PostgreSQL** apenas se realmente necessário
4. ❌ **Não migre** todas as 27 views automaticamente

**Vantagens dessa abordagem:**

-   Código mais testável
-   Melhor performance
-   Mais flexível
-   Mais fácil de manter
-   Type-safe com Pydantic

## 🔍 Verificar se Precisa de uma View

Pergunte-se:

1. **É usada em múltiplos lugares?** → Considere criar
2. **É uma query complexa?** → Considere usar repository
3. **É apenas formatação?** → Use Pydantic
4. **É para relatórios?** → Considere criar quando necessário

## 📞 Próximos Passos

1. ✅ Dados principais já foram migrados
2. ✅ API FastAPI está funcionando
3. 🔄 Crie views conforme necessidade
4. 🔄 Implemente queries nos repositories

---

**Resumo:** As views não foram migradas propositalmente. É melhor recriar conforme necessidade usando a abordagem moderna do FastAPI com repositories e Pydantic.
