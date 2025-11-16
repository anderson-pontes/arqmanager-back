# 📝 Migração de Tarefas (servico_microservico → tarefas)

## ✅ Implementação Concluída

A migração de tarefas foi implementada no script `migrate_data.py`. A função `migrate_tarefas()` migra todos os registros da tabela `servico_microservico` (MySQL) para `tarefas` (PostgreSQL).

## 🔄 Mapeamento de Campos

| MySQL (servico_microservico) | PostgreSQL (tarefas) | Observações |
|------------------------------|---------------------|-------------|
| `cod_microservico` | `id` | ID preservado |
| `cod_etapa` | `etapa_id` | FK para etapas |
| `descricao` | `nome` | Nome da tarefa |
| `ordem` | `ordem` | Ordem de exibição |
| `cor` | `cor` | Cor hexadecimal |
| `prazo` | `tem_prazo` | Boolean (1=Sim, 0=Não) |
| `detalhe` | `precisa_detalhamento` | Boolean (1=Sim, 0=Não) |
| - | `escritorio_id` | Obtido da etapa |

## 🚀 Como Executar

### 1. Garantir que Serviços e Etapas já foram migrados

A migração de tarefas depende de:
- ✅ Serviços migrados
- ✅ Etapas migradas

### 2. Executar a migração completa

```bash
cd arqmanager-backend
python migrate_data.py
```

A função `migrate_tarefas()` será executada automaticamente após `migrate_etapas()`.

### 3. Corrigir sequences após migração

Após a migração, execute o script para corrigir as sequences:

```bash
python fix_all_sequences.py
```

Ou execute individualmente:

```bash
python fix_etapas_sequence.py
python fix_tarefas_sequence.py
```

## 📊 Funcionalidades da Migração

### ✅ Validações Implementadas

1. **Verificação de Etapa**: Verifica se a etapa existe no PostgreSQL antes de migrar a tarefa
2. **Preservação de IDs**: Mantém os IDs originais do MySQL
3. **Escritório ID**: Obtém automaticamente o `escritorio_id` da etapa relacionada
4. **Atualização de Registros**: Se a tarefa já existe, atualiza em vez de criar duplicata
5. **Tratamento de Erros**: Captura e reporta erros sem interromper a migração

### 📈 Relatório de Migração

A função exibe:
- ✅ Número de tarefas migradas
- 🔄 Número de tarefas atualizadas (se já existiam)
- ⚠️ Número de tarefas puladas (etapas não encontradas ou erros)

## ⚠️ Observações Importantes

1. **Ordem de Execução**: A migração de tarefas deve ser executada APÓS a migração de etapas
2. **IDs Preservados**: Os IDs do MySQL são preservados no PostgreSQL
3. **Escritório ID**: Obtido automaticamente da etapa relacionada
4. **Campos Booleanos**: `prazo` e `detalhe` são convertidos de TINYINT(1) para Boolean
5. **Valores Nulos**: Campos opcionais são tratados adequadamente

## 🔍 Verificação Pós-Migração

Após a migração, verifique:

```sql
-- Contar tarefas migradas
SELECT COUNT(*) FROM tarefas;

-- Verificar tarefas por etapa
SELECT etapa_id, COUNT(*) as total
FROM tarefas
GROUP BY etapa_id
ORDER BY etapa_id;

-- Verificar tarefas sem etapa (não deveria haver)
SELECT COUNT(*) FROM tarefas t
LEFT JOIN etapas e ON t.etapa_id = e.id
WHERE e.id IS NULL;
```

## 🐛 Troubleshooting

### Erro: "Etapa não encontrada"

- Verifique se as etapas foram migradas corretamente
- Verifique se os IDs das etapas foram preservados

### Erro: "Violação de chave primária"

- Execute `fix_tarefas_sequence.py` para corrigir a sequence
- Verifique se há IDs duplicados

### Tarefas sem escritorio_id

- Execute o script de correção de sequences
- Verifique se as etapas têm `escritorio_id` preenchido




