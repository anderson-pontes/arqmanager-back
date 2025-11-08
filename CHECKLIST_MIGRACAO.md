# ✅ Checklist de Migração MySQL → PostgreSQL

## 📝 Preparação

-   [ ] **1. Instalar dependência MySQL**

    ```bash
    pip install pymysql
    ```

-   [ ] **2. Configurar credenciais MySQL**

    -   Editar `check_mysql.py` linha 8
    -   Editar `migrate_data.py` linha 11
    -   Formato: `mysql+pymysql://usuario:senha@host:3306/dbarqmanager`

-   [ ] **3. Verificar PostgreSQL está pronto**

    ```bash
    # Ativar ambiente virtual
    venv\Scripts\activate

    # Aplicar migrations
    alembic upgrade head
    ```

## 🧪 Testes

-   [ ] **4. Testar conexão MySQL**

    ```bash
    python check_mysql.py
    ```

    -   Deve mostrar tabelas e contagem de registros
    -   Anote quantos registros existem em cada tabela

-   [ ] **5. Verificar PostgreSQL vazio**
    ```bash
    python check_migrated_data.py
    ```
    -   Deve mostrar 0 registros (ou registros anteriores)

## 🚀 Migração

-   [ ] **6. Executar migração**

    ```bash
    python migrate_data.py
    ```

    -   Aguarde o processo concluir
    -   Observe os logs para erros

-   [ ] **7. Verificar dados migrados**
    ```bash
    python check_migrated_data.py
    ```
    -   Compare com os números do MySQL
    -   Verifique exemplos de dados

## ✅ Validação

-   [ ] **8. Testar API com dados reais**

    ```bash
    uvicorn app.main:app --reload
    ```

    -   Acesse: http://localhost:8000/docs
    -   Teste endpoints de clientes, serviços, etc.

-   [ ] **9. Criar usuário admin**

    ```bash
    python create_admin.py
    ```

-   [ ] **10. Testar login**
    ```bash
    python test_login.py
    ```

## 📊 Resultados Esperados

Após a migração, você deve ter:

| Tabela     | Descrição                                           |
| ---------- | --------------------------------------------------- |
| Status     | Status dos projetos (Em andamento, Concluído, etc.) |
| Clientes   | Pessoas físicas e jurídicas                         |
| Serviços   | Tipos de serviços oferecidos                        |
| Etapas     | Etapas de cada serviço                              |
| Propostas  | Orçamentos e propostas                              |
| Projetos   | Projetos em andamento                               |
| Movimentos | Movimentos financeiros                              |

## 🐛 Problemas Comuns

### Erro: "No module named 'pymysql'"

```bash
pip install pymysql
```

### Erro: "Can't connect to MySQL server"

-   Verificar se MySQL está rodando
-   Verificar credenciais no arquivo
-   Testar conexão manual

### Erro: "relation does not exist"

```bash
alembic upgrade head
```

### Dados não aparecem na API

-   Verificar se migrations foram aplicadas
-   Verificar se dados foram realmente migrados
-   Verificar logs do servidor

## 📞 Próximos Passos

Após migração bem-sucedida:

1. ✅ Backup do banco PostgreSQL
2. ✅ Testar todas as funcionalidades
3. ✅ Configurar ambiente de produção
4. ✅ Documentar customizações

---

**Tempo estimado:** 15-30 minutos  
**Dificuldade:** Média  
**Reversível:** Sim (dados originais no MySQL permanecem intactos)
