# ✅ Correção Schema de Cliente

## 🐛 Problema:

Erro 500 ao listar clientes - Schema esperava campos obrigatórios que estão NULL no banco.

## 🔍 Causa:

Os clientes migrados do sistema antigo têm campos de endereço opcionais (NULL), mas o schema `ClienteBase` os definia como obrigatórios.

## ✅ Solução:

### Campos Tornados Opcionais:

```python
class ClienteBase(BaseModel):
    # ... outros campos ...
    logradouro: Optional[str] = None  # ✅ Era obrigatório
    numero: Optional[str] = None      # ✅ Era obrigatório
    bairro: Optional[str] = None      # ✅ Era obrigatório
    cidade: Optional[str] = None      # ✅ Era obrigatório
    uf: Optional[str] = None          # ✅ Era obrigatório
    cep: Optional[str] = None         # ✅ Era obrigatório
```

### Validators Ajustados:

```python
@validator('uf')
def validate_uf(cls, v):
    if v and len(v) != 2:  # ✅ Só valida se não for None
        raise ValueError('UF deve ter 2 caracteres')
    return v.upper() if v else None

@validator('cep')
def validate_cep(cls, v):
    if not v:  # ✅ Se for None, retorna None
        return None
    cep = ''.join(filter(str.isdigit, v))
    if len(cep) != 8:
        raise ValueError('CEP deve ter 8 dígitos')
    return cep
```

## 🚀 Como Testar:

### 1. Reiniciar Backend

```bash
# Parar backend (Ctrl+C)
cd arqmanager-backend
python -m uvicorn app.main:app --reload
```

### 2. Testar

```
http://localhost:5173/test-integration
```

1. Login: admin@arqmanager.com / admin123
2. Clicar em "Buscar Clientes"
3. **Deve listar 135 clientes!** ✅

## 📝 Notas:

-   Clientes migrados podem não ter endereço completo
-   Novos clientes podem exigir endereço (validação no frontend)
-   Schema agora aceita ambos os casos

---

**Status:** ✅ Corrigido  
**Arquivo:** `app/schemas/cliente.py`  
**Ação:** Reiniciar backend
