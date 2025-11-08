# ✅ Views Criadas no PostgreSQL

## 🎉 Resumo

**6 views principais** foram recriadas no PostgreSQL com sucesso!

---

## 📊 Views Disponíveis

### 1. v_cliente (135 registros)

**Descrição:** Clientes com formatações e informações completas

**Campos principais:**

-   `cod_cliente` - ID do cliente
-   `nome` - Nome completo
-   `cod_tipo_pessoa` - Tipo (PF/PJ)
-   `cod_tipo_pessoa_formatado` - "Pessoa Física" ou "Pessoa Jurídica"
-   `identificacao` - CPF/CNPJ
-   `identificacao_sem_mascara` - CPF/CNPJ sem pontuação
-   `email`, `telefone`, `whatsapp`
-   `data_nascimento_formatada` - Data formatada DD/MM/YYYY
-   Endereço completo (logradouro, numero, bairro, cidade, uf, cep)

**Exemplo de uso:**

```sql
SELECT cod_cliente, nome, cod_tipo_pessoa_formatado, email
FROM v_cliente
WHERE ativo = true
ORDER BY nome;
```

---

### 2. v_projeto (173 registros)

**Descrição:** Projetos com informações de cliente, serviço e status

**Campos principais:**

-   `cod_projeto` - ID do projeto
-   `numero_projeto_formatado` - Ex: "2024/001"
-   `descricao` - Descrição do projeto
-   `data_inicio_formatada`, `data_previsao_fim_formatada`, `data_fim_formatada`
-   `metragem_formatada` - Metragem com formatação
-   `valor_contrato_formatado`, `saldo_contrato_formatado`
-   `cliente_nome`, `cliente_email`, `cliente_whatsapp`
-   `servico_nome`
-   `status_descricao`, `status_cor`

**Exemplo de uso:**

```sql
SELECT
    numero_projeto_formatado,
    cliente_nome,
    servico_nome,
    status_descricao,
    valor_contrato_formatado
FROM v_projeto
WHERE ativo = true
ORDER BY ano_projeto DESC, numero_projeto DESC;
```

---

### 3. v_proposta (136 registros)

**Descrição:** Propostas/Orçamentos com informações completas

**Campos principais:**

-   `cod_proposta` - ID da proposta
-   `numero_proposta_formatada` - Ex: "2024/001"
-   `nome`, `descricao`
-   `data_proposta_formatada`
-   `valor_proposta_formatado`, `valor_avista_formatado`
-   `valor_parcela_aprazo` - Descrição do parcelamento
-   `forma_pagamento`, `prazo`
-   `cliente_nome`, `cliente_email`, `cliente_telefone`
-   `servico_nome`, `servico_descricao`
-   `status_descricao`, `status_cor`

**Exemplo de uso:**

```sql
SELECT
    numero_proposta_formatada,
    cliente_nome,
    servico_nome,
    valor_proposta_formatado,
    status_descricao
FROM v_proposta
ORDER BY ano_proposta DESC, numero_proposta DESC;
```

---

### 4. v_movimento (966 registros)

**Descrição:** Movimentos financeiros (receitas e despesas)

**Campos principais:**

-   `cod_movimento` - ID do movimento
-   `cod_despesa_receita_tipo` - Tipo (1=Receita, 2=Despesa)
-   `tipo_formatado` - "Receita" ou "Despesa"
-   `descricao`, `observacao`
-   `data_entrada_formatada`, `data_efetivacao_formatada`
-   `competencia_formatada` - MM/YYYY
-   `valor_formatado`, `valor_acrescido_formatado`, `valor_desconto_formatado`
-   `valor_resultante_formatado`
-   `comprovante`, `extensao`
-   `codigo_plano_contas`
-   `numero_projeto`, `projeto_descricao`

**Exemplo de uso:**

```sql
SELECT
    tipo_formatado,
    descricao,
    data_efetivacao_formatada,
    valor_resultante_formatado,
    projeto_descricao
FROM v_movimento
WHERE ativo = true
ORDER BY data_efetivacao DESC;
```

---

### 5. v_servico_etapa (54 registros)

**Descrição:** Etapas de cada serviço

**Campos principais:**

-   `cod_servico_etapa` - ID da etapa
-   `cod_servico` - ID do serviço
-   `servico_nome`, `servico_descricao`
-   `eta_descricao` - Nome da etapa
-   `descricao_contrato` - Descrição para contrato
-   `ordem` - Ordem de execução
-   `exibir` - Se é obrigatória

**Exemplo de uso:**

```sql
SELECT
    servico_nome,
    eta_descricao,
    ordem
FROM v_servico_etapa
ORDER BY cod_servico, ordem;
```

---

### 6. v_colaborador (1 registro)

**Descrição:** Colaboradores ativos

**Campos principais:**

-   `cod_colaborador` - ID do colaborador
-   `nome`, `email`
-   `cpf`, `telefone`
-   `data_nascimento_formatada`
-   `foto`
-   `ativo`

**Exemplo de uso:**

```sql
SELECT
    nome,
    email,
    telefone,
    data_nascimento_formatada
FROM v_colaborador
WHERE ativo = true
ORDER BY nome;
```

---

## 🔧 Gerenciamento das Views

### Criar/Recriar Views

```bash
python create_views.py
```

### Listar Views Existentes

```bash
python create_views.py list
```

### Remover Todas as Views

```bash
python create_views.py drop
```

### Testar Views

```bash
python test_views.py
```

---

## 📝 Diferenças do MySQL Original

### Formatações Adaptadas

| MySQL                           | PostgreSQL                           |
| ------------------------------- | ------------------------------------ |
| `FORMAT(valor, 2, 'de_DE')`     | `TO_CHAR(valor, 'FM999G999G999D00')` |
| `DATE_FORMAT(data, '%d/%m/%Y')` | `TO_CHAR(data, 'DD/MM/YYYY')`        |
| `CONCAT(a, '/', b)`             | `a \|\| '/' \|\| b`                  |
| `LPAD(numero, 3, '0')`          | `LPAD(numero::text, 3, '0')`         |

### Campos Adaptados

-   **tipo_pessoa**: No MySQL era `cod_tipo_pessoa` (1, 2), no PostgreSQL é `tipo_pessoa` ('PF', 'PJ')
-   **telefone**: No MySQL era `telefones`, no PostgreSQL é `telefone`
-   **valor_parcela_aprazo**: Mantido como texto descritivo (não é numérico)

---

## 💡 Como Usar nas Aplicações

### Opção 1: Query Direta (SQL)

```sql
SELECT * FROM v_cliente WHERE email LIKE '%@gmail.com%';
```

### Opção 2: SQLAlchemy (Python)

```python
from sqlalchemy import text

# No repository
def get_clientes_formatados(db: Session):
    result = db.execute(text("SELECT * FROM v_cliente ORDER BY nome"))
    return result.fetchall()
```

### Opção 3: FastAPI Endpoint

```python
@router.get("/clientes/formatados")
def get_clientes_formatados(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM v_cliente"))
    return [dict(row._mapping) for row in result]
```

---

## 🚫 Views NÃO Migradas (21 views)

As seguintes views do MySQL **não foram migradas** por serem muito específicas ou não essenciais:

-   v_aniversariantes
-   v_ata
-   v_contas_escritorio
-   v_data
-   v_email_enviado
-   v_extrato_conta
-   v_extrato_conta_consolidado
-   v_extrato_conta_consolidado_ano
-   v_feriados
-   v_financeiro_projeto
-   v_indicacao
-   v_mes
-   v_permissao
-   v_plano_contas
-   v_previsto_realizado
-   v_projeto_arquivamento
-   v_projeto_rrt
-   v_proposta_microservico
-   v_proposta_servico_etapa
-   v_rrt_projeto
-   v_template_email_whatsapp

**Recomendação:** Crie essas views conforme necessidade, adaptando a sintaxe para PostgreSQL.

---

## 📊 Estatísticas

| View            | Registros | Status      |
| --------------- | --------- | ----------- |
| v_cliente       | 135       | ✅ OK       |
| v_projeto       | 173       | ✅ OK       |
| v_proposta      | 136       | ✅ OK       |
| v_movimento     | 966       | ✅ OK       |
| v_servico_etapa | 54        | ✅ OK       |
| v_colaborador   | 1         | ✅ OK       |
| **TOTAL**       | **1.465** | **✅ 100%** |

---

## 🎯 Próximos Passos

1. ✅ Views principais criadas
2. ✅ Views testadas e funcionando
3. 🔄 Criar views adicionais conforme necessidade
4. 🔄 Integrar views nos endpoints da API
5. 🔄 Documentar uso das views no Swagger

---

## 📞 Comandos Úteis

```bash
# Criar views
python create_views.py

# Testar views
python test_views.py

# Listar views
python create_views.py list

# Remover views
python create_views.py drop

# Consultar view específica
psql -U arqmanager_user -d arqmanager -c "SELECT * FROM v_cliente LIMIT 5"
```

---

**Criado em:** Janeiro 2025  
**Status:** ✅ Produção  
**Versão:** 1.0.0
