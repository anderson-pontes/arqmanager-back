# 📋 Migração de Escritórios

## 🎯 Objetivo

Migrar a tabela `escritorio` do MySQL para o PostgreSQL. Esta migração deve ser executada **PRIMEIRO**, antes de todas as outras, pois todas as outras entidades dependem de `escritorio_id`.

## 📊 Mapeamento de Campos

| MySQL | PostgreSQL | Observações |
|-------|------------|-------------|
| `id_escritorio` | `id` | Preservado |
| `nome_fantasia` | `nome_fantasia` | Direto |
| `razao_social` | `razao_social` | Direto (fallback para nome_fantasia se vazio) |
| `documento` | `documento` | Direto (pode ser NULL) |
| `email` | `email` | Direto |
| `fone` | `telefone` | Renomeado |
| `cidade` | `cidade` | Direto |
| `uf` | `uf` | Direto |
| `endereco_completo` | `endereco` | Usado como endereço principal |
| `endereco_reduzido` | - | Ignorado (usado como fallback se endereco_completo vazio) |
| `dias_uteis` | `dias_uteis` | Direto (default: TRUE) |
| `prazo_arquiva_proposta` | `prazo_arquiva_proposta` | Direto (default: 30) |
| `email_administrador` | - | Não migrado (campo não existe no novo schema) |
| `envio_email` | - | Não migrado (campo não existe no novo schema) |
| `instagram` | - | Não migrado (campo não existe no novo schema) |
| - | `ativo` | Sempre TRUE na migração |
| - | `created_at` | NOW() |
| - | `updated_at` | NOW() |

## 🔄 Ordem de Migração

A migração de escritórios deve ser executada **ANTES** de todas as outras:

1. ✅ **Escritórios** (PRIMEIRO - base de tudo)
2. Status
3. Clientes
4. Serviços
5. Etapas
6. Tarefas
7. Propostas
8. Projetos
9. Movimentos

## ⚠️ Dependências

- **Nenhuma** - Escritórios são a entidade base
- Todas as outras entidades dependem de `escritorio_id`

## 🔧 Função de Migração

A função `migrate_escritorios()` foi adicionada ao `migrate_data.py` e é executada automaticamente como primeira migração.

## 📝 Tratamento de Dados

- **IDs preservados**: Os IDs do MySQL são mantidos no PostgreSQL
- **ON CONFLICT**: Usa `ON CONFLICT (id) DO UPDATE` para atualizar registros existentes
- **Campos opcionais**: `documento` pode ser NULL se vazio no MySQL
- **Valores padrão**: `dias_uteis = TRUE`, `prazo_arquiva_proposta = 30` se não especificado

## ✅ Validações

- `nome_fantasia` é obrigatório (não pode ser NULL)
- `razao_social` usa `nome_fantasia` como fallback se vazio
- `documento` pode ser NULL (campo opcional no novo schema)
- `email` é obrigatório (não pode ser NULL)

## 🚀 Execução

A migração de escritórios é executada automaticamente quando você roda:

```bash
python migrate_data.py
```

Certifique-se de que:
1. O MySQL está acessível
2. A conexão está configurada (`.mysql_config` ou variável de ambiente)
3. O PostgreSQL está rodando
4. As tabelas já foram criadas (migrations Alembic executadas)

## 🔍 Verificação

Após a migração, verifique:

```sql
-- Contar escritórios migrados
SELECT COUNT(*) FROM escritorio;

-- Verificar se há escritórios sem nome
SELECT * FROM escritorio WHERE nome_fantasia IS NULL OR nome_fantasia = '';

-- Verificar IDs
SELECT MIN(id), MAX(id), COUNT(*) FROM escritorio;
```

## 📌 Notas Importantes

1. **Ordem crítica**: Escritórios DEVEM ser migrados primeiro
2. **IDs preservados**: Os IDs são mantidos para manter referências
3. **Campos não migrados**: Alguns campos do MySQL não existem no novo schema e são ignorados
4. **Sequence**: Após a migração, execute `fix_all_sequences.py` para corrigir a sequence




