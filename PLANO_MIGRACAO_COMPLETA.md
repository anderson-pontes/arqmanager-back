# 📋 Plano de Migração Completa - MySQL → PostgreSQL

## 🔍 Análise Atual

### ✅ O que JÁ foi migrado:

**Dados (1.485 registros):**

-   7 Status
-   135 Clientes
-   13 Serviços
-   54 Etapas
-   136 Propostas
-   173 Projetos
-   966 Movimentos
-   1 Colaborador

**Views (6):**

-   v_cliente
-   v_projeto
-   v_proposta
-   v_movimento
-   v_servico_etapa
-   v_colaborador

### ⚠️ O que NÃO foi migrado:

**Views (21):** Secundárias, criar conforme necessidade
**Procedures (22):** Reescrever em Python
**Functions (10):** Reescrever em Python
**Triggers (3):** Avaliar necessidade
**Tabelas (43):** Muitas auxiliares

---

## 🎯 Priorização da Migração

### 🔴 PRIORIDADE ALTA (Essencial para funcionamento)

#### 1. Tabelas Críticas

**escritorio** (4 registros)

-   Tabela de escritórios/empresas
-   **Ação:** Migrar AGORA
-   **Impacto:** Alto - sistema multi-tenant

**colaborador_escritorio** (19 registros)

-   Relacionamento colaborador-escritório
-   **Ação:** Migrar AGORA
-   **Impacto:** Alto - controle de acesso

**projeto_colaborador** (100 registros)

-   Equipe dos projetos
-   **Ação:** Migrar AGORA
-   **Impacto:** Alto - gestão de projetos

**projeto_pagamento** (436 registros)

-   Pagamentos dos projetos
-   **Ação:** Migrar AGORA
-   **Impacto:** Alto - financeiro

**proposta_servico_etapa** (1.114 registros)

-   Etapas das propostas
-   **Ação:** Migrar AGORA
-   **Impacto:** Alto - gestão de propostas

**conta_bancaria** (10 registros)

-   Contas bancárias
-   **Ação:** Migrar AGORA
-   **Impacto:** Alto - financeiro

**conta_movimentacao** (1.343 registros)

-   Movimentações bancárias
-   **Ação:** Migrar AGORA
-   **Impacto:** Alto - financeiro

**plano_contas** (621 registros)

-   Plano de contas contábil
-   **Ação:** Migrar AGORA
-   **Impacto:** Alto - financeiro

### 🟡 PRIORIDADE MÉDIA (Importante mas não crítico)

**acesso_grupo** (6 registros)

-   Grupos de acesso
-   **Ação:** Migrar depois
-   **Impacto:** Médio - permissões

**acesso_permissao_grupo** (187 registros)

-   Permissões por grupo
-   **Ação:** Migrar depois
-   **Impacto:** Médio - permissões

**forma_pagamento** (11 registros)

-   Formas de pagamento
-   **Ação:** Migrar depois
-   **Impacto:** Médio - financeiro

**feriados** (767 registros)

-   Feriados para cálculo de prazos
-   **Ação:** Migrar depois
-   **Impacto:** Médio - prazos

**indicacao** (39 registros)

-   Indicações de clientes
-   **Ação:** Migrar depois
-   **Impacto:** Médio - marketing

**projeto_documento** (19 registros)

-   Documentos dos projetos
-   **Ação:** Migrar depois
-   **Impacto:** Médio - gestão documental

**email** (394 registros)

-   Histórico de emails
-   **Ação:** Migrar depois
-   **Impacto:** Médio - comunicação

### 🟢 PRIORIDADE BAIXA (Opcional)

**log\_\*** (várias tabelas)

-   Logs do sistema
-   **Ação:** Não migrar
-   **Impacto:** Baixo - histórico

**reuniao** (0 registros)

-   Reuniões (vazio)
-   **Ação:** Não migrar
-   **Impacto:** Nenhum

**sticker** (10 registros)

-   Adesivos/etiquetas
-   **Ação:** Avaliar necessidade
-   **Impacto:** Baixo

---

## 🔧 Stored Procedures - Conversão para Python

### Procedures Críticas (Converter AGORA)

#### 1. **atualiza_saldo_projeto**

```sql
-- MySQL Procedure
CREATE PROCEDURE atualiza_saldo_projeto(IN param_cod_projeto int)
BEGIN
    -- Atualiza saldo do projeto
END
```

**Conversão Python:**

```python
# app/services/projeto_service.py
class ProjetoService:
    def atualizar_saldo_projeto(self, db: Session, projeto_id: int):
        """Atualiza saldo do projeto baseado nos pagamentos"""
        projeto = db.query(Projeto).filter(Projeto.id == projeto_id).first()
        if not projeto:
            return

        # Calcular total pago
        total_pago = db.query(func.sum(ProjetoPagamento.valor_recebido))\
            .filter(ProjetoPagamento.projeto_id == projeto_id)\
            .scalar() or 0

        # Atualizar saldo
        projeto.saldo_contrato = projeto.valor_contrato - total_pago
        db.commit()
```

#### 2. **Prazo** / **prazo_dias**

```python
# app/utils/prazo.py
from datetime import datetime, timedelta
from app.models import Feriado

def calcular_prazo(data_inicio: date, dias: int, escritorio_id: int, db: Session) -> date:
    """Calcula prazo considerando dias úteis e feriados"""
    data_atual = data_inicio
    dias_contados = 0

    # Buscar feriados do escritório
    feriados = db.query(Feriado.data)\
        .filter(Feriado.escritorio_id == escritorio_id)\
        .all()
    feriados_set = {f[0] for f in feriados}

    while dias_contados < dias:
        data_atual += timedelta(days=1)

        # Pular fins de semana
        if data_atual.weekday() >= 5:  # 5=sábado, 6=domingo
            continue

        # Pular feriados
        if data_atual in feriados_set:
            continue

        dias_contados += 1

    return data_atual
```

#### 3. **sp_extrato_conta_principal**

```python
# app/services/financeiro_service.py
class FinanceiroService:
    def extrato_conta_principal(
        self,
        db: Session,
        periodo: date,
        escritorio_id: int
    ):
        """Gera extrato da conta principal"""
        movimentos = db.query(ContaMovimentacao)\
            .filter(
                ContaMovimentacao.escritorio_id == escritorio_id,
                ContaMovimentacao.data >= periodo
            )\
            .order_by(ContaMovimentacao.data)\
            .all()

        saldo = 0
        extrato = []

        for mov in movimentos:
            if mov.tipo == 'receita':
                saldo += mov.valor
            else:
                saldo -= mov.valor

            extrato.append({
                'data': mov.data,
                'descricao': mov.descricao,
                'valor': mov.valor,
                'tipo': mov.tipo,
                'saldo': saldo
            })

        return extrato
```

### Procedures Secundárias (Converter DEPOIS)

-   sp_projeto_estatistica
-   sp_relatorio_a_pagar_pago
-   sp_relatorio_a_receber_recebido
-   sp_media_financeiro_anual

---

## 📊 Functions - Conversão para Python

### Functions Importantes

#### 1. **f_extenso** (Número por extenso)

```python
# app/utils/formatters.py
from num2words import num2words

def numero_por_extenso(valor: float) -> str:
    """Converte número para extenso"""
    return num2words(valor, lang='pt_BR', to='currency')
```

#### 2. **f_saldo_conta_bancaria_periodo**

```python
# app/utils/financeiro.py
def saldo_conta_periodo(
    db: Session,
    conta_id: int,
    data_inicio: date,
    data_fim: date
) -> float:
    """Calcula saldo da conta no período"""
    movimentos = db.query(ContaMovimentacao)\
        .filter(
            ContaMovimentacao.conta_id == conta_id,
            ContaMovimentacao.data.between(data_inicio, data_fim)
        )\
        .all()

    saldo = 0
    for mov in movimentos:
        if mov.tipo == 'receita':
            saldo += mov.valor
        else:
            saldo -= mov.valor

    return saldo
```

---

## ⚡ Triggers - Avaliação

### Triggers Existentes

#### 1. **insere_conta_movimentacao**

**O que faz:** Insere movimentação bancária automaticamente

**Recomendação:** ❌ NÃO migrar
**Alternativa:** Fazer explicitamente no service

```python
# app/services/movimento_service.py
def criar_movimento(self, db: Session, movimento_data: dict):
    # Criar movimento
    movimento = Movimento(**movimento_data)
    db.add(movimento)

    # Criar movimentação bancária explicitamente
    if movimento.conta_bancaria_id:
        movimentacao = ContaMovimentacao(
            conta_id=movimento.conta_bancaria_id,
            valor=movimento.valor,
            tipo=movimento.tipo,
            data=movimento.data_efetivacao
        )
        db.add(movimentacao)

    db.commit()
```

#### 2. **atualiza_movimentacao_inicial**

**Recomendação:** ❌ NÃO migrar - fazer no service

#### 3. **insere_usuario_master**

**Recomendação:** ❌ NÃO migrar - criar via migration ou script

---

## 📝 Plano de Ação Recomendado

### Fase 1: Tabelas Críticas (1-2 dias)

```bash
# Criar script de migração
python migrate_tabelas_criticas.py
```

**Tabelas a migrar:**

1. escritorio
2. colaborador_escritorio
3. projeto_colaborador
4. projeto_pagamento
5. proposta_servico_etapa
6. conta_bancaria
7. conta_movimentacao
8. plano_contas

### Fase 2: Procedures Críticas (2-3 dias)

**Criar services:**

1. ProjetoService.atualizar_saldo_projeto()
2. PrazoUtils.calcular_prazo()
3. FinanceiroService.extrato_conta()

### Fase 3: Ajustar API (1-2 dias)

**Endpoints a criar/ajustar:**

1. GET /api/v1/escritorios
2. GET /api/v1/projetos/{id}/equipe
3. GET /api/v1/projetos/{id}/pagamentos
4. GET /api/v1/financeiro/extrato
5. GET /api/v1/plano-contas

### Fase 4: Tabelas Secundárias (2-3 dias)

**Migrar conforme necessidade:**

-   acesso_grupo
-   acesso_permissao_grupo
-   forma_pagamento
-   feriados
-   indicacao

### Fase 5: Testes e Validação (2-3 dias)

1. Testar todos os endpoints
2. Validar cálculos financeiros
3. Testar permissões
4. Validar relatórios

---

## 🚀 Começar Agora

### Passo 1: Migrar Tabelas Críticas

Vou criar o script para você:

```bash
python migrate_tabelas_criticas.py
```

### Passo 2: Criar Models

Adicionar models no SQLAlchemy para as novas tabelas

### Passo 3: Criar Services

Converter procedures em services Python

### Passo 4: Criar Endpoints

Adicionar endpoints na API

---

## ❓ Perguntas para Você

1. **Qual a prioridade?**

    - Migrar todas as tabelas críticas agora?
    - Ou migrar gradualmente conforme necessidade?

2. **Procedures:**

    - Converter todas agora?
    - Ou apenas as essenciais?

3. **Permissões:**

    - Sistema de permissões é crítico?
    - Ou pode ser simplificado?

4. **Multi-tenant:**
    - Sistema precisa suportar múltiplos escritórios?
    - Ou é single-tenant?

---

## 💡 Recomendação Final

**Abordagem Incremental:**

1. ✅ **JÁ FEITO:** Dados principais migrados
2. 🔄 **PRÓXIMO:** Migrar 8 tabelas críticas
3. 🔄 **DEPOIS:** Converter 3-4 procedures principais
4. 🔄 **DEPOIS:** Ajustar API conforme necessidade
5. 🔄 **DEPOIS:** Migrar tabelas secundárias

**Tempo estimado total:** 10-15 dias de desenvolvimento

---

**Quer que eu comece criando o script para migrar as tabelas críticas?**
