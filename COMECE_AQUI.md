# 🎯 COMECE AQUI - Migração de Dados

## 🚀 3 Passos para Migrar

### 1️⃣ Instalar Dependência

```bash
pip install pymysql
```

### 2️⃣ Configurar MySQL

Edite `migrate_data.py` linha 11:

```python
MYSQL_URL = "mysql+pymysql://seu_usuario:sua_senha@localhost:3306/dbarqmanager"
```

### 3️⃣ Executar Migração

```bash
python migrar.py
```

## ✅ Pronto!

O assistente vai guiar você pelo resto do processo.

---

## 📚 Precisa de Mais Informações?

-   **Visão Geral:** [README_MIGRACAO.md](README_MIGRACAO.md)
-   **Guia Completo:** [GUIA_MIGRACAO_DADOS.md](GUIA_MIGRACAO_DADOS.md)
-   **Checklist:** [CHECKLIST_MIGRACAO.md](CHECKLIST_MIGRACAO.md)
-   **Comandos:** [COMANDOS_MIGRACAO.md](COMANDOS_MIGRACAO.md)
-   **Exemplos:** [EXEMPLOS_MIGRACAO.md](EXEMPLOS_MIGRACAO.md)
-   **Índice Completo:** [INDICE_DOCUMENTACAO.md](INDICE_DOCUMENTACAO.md)

---

## 🐛 Problemas?

### Erro: "No module named 'pymysql'"

```bash
pip install pymysql
```

### Erro: "Can't connect to MySQL"

Verifique as credenciais em `migrate_data.py`

### Erro: "relation does not exist"

```bash
alembic upgrade head
```

### Outros Problemas

Veja: [GUIA_MIGRACAO_DADOS.md](GUIA_MIGRACAO_DADOS.md) - Seção Troubleshooting

---

**Tempo estimado:** 15-30 minutos  
**Dificuldade:** Fácil

Boa migração! 🎉
