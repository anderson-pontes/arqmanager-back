# 🔧 Plano de Conversão de Procedures MySQL → Python

## 📊 Procedures Encontradas (22)

### 🔴 PRIORIDADE ALTA - Críticas (5)

#### 1. **atualiza_saldo_projeto**

**O que faz:** Atualiza o saldo do projeto baseado nos pagamentos

**Conversão Python:**

```python
# app/services/projeto_service.py
from sqlalchemy import func
from app.models import Projeto, ProjetoPagamento

class ProjetoService:
    def atualizar_saldo_projeto(self, db: Session, projeto_id: int):
        """Atualiza saldo do projeto"""
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
        return projeto
```

**Onde usar:** Após criar/atualizar pagamentos

---

#### 2. **Prazo / prazo_dias**

**O que faz:** Calcula prazos considerando dias úteis e feriados

**Conversão Python:**

```python
# app/utils/prazo.py
from datetime import datetime, timedelta, date
from sqlalchemy.orm import Session
from app.models import Feriado

def calcular_prazo(
    data_inicio: date,
    dias: int,
    escritorio_id: int,
    db: Session
) -> date:
    """
    Calcula prazo considerando dias úteis e feriados

    Args:
        data_inicio: Data inicial
        dias: Quantidade de dias úteis
        escritorio_id: ID do escritório (para buscar feriados)
        db: Sessão do banco

    Returns:
        Data final calculada
    """
    # Buscar feriados
    feriados = db.query(Feriado.data)\
        .filter(Feriado.ativo == True)\
        .all()
    feriados_set = {f[0] for f in feriados}

    data_atual = data_inicio
    dias_contados = 0

    while dias_contados < dias:
        data_atual += timedelta(days=1)

        # Pular fins de semana (5=sábado, 6=domingo)
        if data_atual.weekday() >= 5:
            continue

        # Pular feriados
        if data_atual in feriados_set:
            continue

        dias_contados += 1

    return data_atual


def calcular_dias_uteis(
    data_inicio: date,
    data_fim: date,
    escritorio_id: int,
    db: Session
) -> int:
    """Calcula quantidade de dias úteis entre duas datas"""
    feriados = db.query(Feriado.data)\
        .filter(Feriado.ativo == True)\
        .all()
    feriados_set = {f[0] for f in feriados}

    dias_uteis = 0
    data_atual = data_inicio

    while data_atual <= data_fim:
        # Contar apenas dias úteis (seg-sex) que não são feriados
        if data_atual.weekday() < 5 and data_atual not in feriados_set:
            dias_uteis += 1
        data_atual += timedelta(days=1)

    return dias_uteis
```

**Onde usar:** Ao calcular datas de etapas, prazos de projetos

---

#### 3. **sp_extrato_conta_principal**

**O que faz:** Gera extrato da conta bancária principal

**Conversão Python:**

```python
# app/services/financeiro_service.py
from datetime import date
from sqlalchemy.orm import Session
from app.models import ContaMovimentacao, ContaBancaria

class FinanceiroService:
    def extrato_conta(
        self,
        db: Session,
        conta_id: int,
        data_inicio: date,
        data_fim: date
    ):
        """Gera extrato de uma conta bancária"""
        movimentos = db.query(ContaMovimentacao)\
            .filter(
                ContaMovimentacao.conta_bancaria_id == conta_id,
                ContaMovimentacao.data >= data_inicio,
                ContaMovimentacao.data <= data_fim
            )\
            .order_by(ContaMovimentacao.data, ContaMovimentacao.id)\
            .all()

        saldo = 0
        extrato = []

        for mov in movimentos:
            if mov.tipo == 'receita':
                saldo += mov.valor
            else:
                saldo -= mov.valor

            extrato.append({
                'id': mov.id,
                'data': mov.data,
                'descricao': mov.descricao,
                'tipo': mov.tipo,
                'valor': mov.valor,
                'saldo': saldo
            })

        return extrato
```

**Endpoint:**

```python
# app/api/v1/endpoints/financeiro.py
@router.get("/extrato/{conta_id}")
def get_extrato(
    conta_id: int,
    data_inicio: date,
    data_fim: date,
    db: Session = Depends(get_db)
):
    service = FinanceiroService()
    return service.extrato_conta(db, conta_id, data_inicio, data_fim)
```

---

#### 4. **AtualizarProjetoCompleto**

**O que faz:** Atualiza todas as informações do projeto

**Conversão Python:**

```python
# app/services/projeto_service.py
class ProjetoService:
    def atualizar_projeto_completo(
        self,
        db: Session,
        projeto_id: int,
        dados: dict
    ):
        """Atualiza projeto e recalcula tudo"""
        projeto = db.query(Projeto).filter(Projeto.id == projeto_id).first()
        if not projeto:
            raise HTTPException(404, "Projeto não encontrado")

        # Atualizar dados básicos
        for key, value in dados.items():
            if hasattr(projeto, key):
                setattr(projeto, key, value)

        # Recalcular saldo
        self.atualizar_saldo_projeto(db, projeto_id)

        # Recalcular prazos das etapas
        self.recalcular_prazos_etapas(db, projeto_id)

        db.commit()
        return projeto
```

---

#### 5. **ConcluirEtapaEProjetoSeRRTFinal**

**O que faz:** Conclui etapa e projeto se for a última etapa

**Conversão Python:**

```python
# app/services/etapa_service.py
class EtapaService:
    def concluir_etapa(
        self,
        db: Session,
        projeto_id: int,
        etapa_id: int
    ):
        """Conclui etapa e verifica se deve concluir projeto"""
        # Marcar etapa como concluída
        etapa = db.query(PropostaServicoEtapa)\
            .filter(
                PropostaServicoEtapa.projeto_id == projeto_id,
                PropostaServicoEtapa.etapa_id == etapa_id
            ).first()

        if etapa:
            etapa.data_conclusao = date.today()

            # Verificar se todas as etapas foram concluídas
            total_etapas = db.query(PropostaServicoEtapa)\
                .filter(PropostaServicoEtapa.projeto_id == projeto_id)\
                .count()

            etapas_concluidas = db.query(PropostaServicoEtapa)\
                .filter(
                    PropostaServicoEtapa.projeto_id == projeto_id,
                    PropostaServicoEtapa.data_conclusao.isnot(None)
                )\
                .count()

            # Se todas concluídas, concluir projeto
            if total_etapas == etapas_concluidas:
                projeto = db.query(Projeto).filter(Projeto.id == projeto_id).first()
                if projeto:
                    projeto.status_id = 5  # Status "Concluído"
                    projeto.data_fim = date.today()

            db.commit()
```

---

### 🟡 PRIORIDADE MÉDIA - Importantes (8)

#### 6. **sp_projeto_estatistica**

**Conversão:** Criar endpoint de estatísticas do projeto

#### 7. **sp_relatorio_a_pagar_pago**

**Conversão:** Endpoint de relatório de despesas

#### 8. **sp_relatorio_a_receber_recebido**

**Conversão:** Endpoint de relatório de receitas

#### 9. **sp_media_financeiro_anual**

**Conversão:** Endpoint de média financeira anual

#### 10. **sp_atualizar_parcelas_restantes**

**Conversão:** Service para atualizar parcelas

#### 11. **f_projeto_prazo_etapa**

**Conversão:** Usar função calcular_prazo já criada

#### 12. **f_projeto_prazo_microservico**

**Conversão:** Similar ao prazo_etapa

#### 13. **cadastrar_estrutura_padrao_plano_contas**

**Conversão:** Script de seed para plano de contas padrão

---

### 🟢 PRIORIDADE BAIXA - Opcionais (9)

14. excluir_conta_bancaria
15. limpa_propostas_escritorio
16. sp_apagarEscritorio
17. sp_movimento
18. sp_principal
19. TEMP
20. ZZZ_sp_atualiza_extrato_conta
21. ZZZ_sp_temp
22. Outras procedures de limpeza/manutenção

---

## 📝 Plano de Implementação

### Fase 1: Procedures Críticas (1-2 dias)

```bash
# Criar estrutura de services
mkdir -p app/services
mkdir -p app/utils

# Criar arquivos
touch app/services/projeto_service.py
touch app/services/financeiro_service.py
touch app/services/etapa_service.py
touch app/utils/prazo.py
```

### Fase 2: Implementar Services (2-3 dias)

1. ✅ Criar ProjetoService com atualiza_saldo_projeto
2. ✅ Criar utils/prazo.py com cálculo de prazos
3. ✅ Criar FinanceiroService com extrato_conta
4. ✅ Criar EtapaService com concluir_etapa

### Fase 3: Criar Endpoints (1 dia)

1. ✅ POST /api/v1/projetos/{id}/atualizar-saldo
2. ✅ GET /api/v1/financeiro/extrato/{conta_id}
3. ✅ POST /api/v1/projetos/{id}/etapas/{etapa_id}/concluir
4. ✅ GET /api/v1/projetos/{id}/estatisticas

### Fase 4: Procedures Médias (2-3 dias)

Implementar relatórios e estatísticas

### Fase 5: Testes (1-2 dias)

Testar todas as conversões

---

## 🎯 Recomendação

**NÃO migre todas as procedures agora!**

### Abordagem Incremental:

1. ✅ **Implemente apenas as 5 críticas** (2-3 dias)
2. 🔄 **Use o sistema** e veja quais procedures são realmente necessárias
3. 🔄 **Implemente sob demanda** conforme necessidade

### Vantagens:

-   ✅ Menos trabalho inicial
-   ✅ Foco no que é realmente usado
-   ✅ Código mais limpo e moderno
-   ✅ Melhor testabilidade

---

## 💡 Próximos Passos

### Opção 1: Implementar Agora (Recomendado)

```bash
# Criar as 5 procedures críticas
python create_critical_services.py
```

### Opção 2: Implementar Depois

-   Use o sistema como está
-   Implemente procedures conforme necessidade
-   Priorize baseado no uso real

---

## 📊 Comparação

| Aspecto           | Procedures MySQL | Services Python |
| ----------------- | ---------------- | --------------- |
| **Manutenção**    | Difícil          | Fácil           |
| **Testes**        | Complexo         | Simples         |
| **Debug**         | Limitado         | Completo        |
| **Versionamento** | Difícil          | Git             |
| **Reutilização**  | Baixa            | Alta            |
| **Performance**   | Alta             | Boa             |

---

## 🎓 Conclusão

**Recomendação:** Implemente apenas as **5 procedures críticas** agora e deixe as outras para implementar conforme necessidade.

**Tempo estimado:** 2-3 dias para as críticas

**Quer que eu crie os services críticos agora?**
