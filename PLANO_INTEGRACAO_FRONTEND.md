# 🔗 Plano de Integração Front-end → Back-end

## 🎯 Objetivo

Conectar o front-end existente ao novo back-end FastAPI de forma incremental, testando cada etapa.

---

## 📋 Etapas de Integração

### 🔴 ETAPA 1: Configuração Inicial (30 min)

#### 1.1. Configurar CORS no Backend

```python
# app/main.py - Já configurado, mas verificar
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8080",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### 1.2. Criar arquivo de configuração no Front-end

```javascript
// src/config/api.js
const API_CONFIG = {
    baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
    apiVersion: '/api/v1',
    timeout: 30000,
};

export const API_ENDPOINTS = {
    // Auth
    login: '/auth/login',
    refresh: '/auth/refresh',
    me: '/auth/me',

    // Clientes
    clientes: '/clientes',
    clienteById: (id) => `/clientes/${id}`,

    // Projetos
    projetos: '/projetos',
    projetoById: (id) => `/projetos/${id}`,

    // Serviços
    servicos: '/servicos',
    servicoById: (id) => `/servicos/${id}`,

    // Propostas
    propostas: '/propostas',
    propostaById: (id) => `/propostas/${id}`,
};

export default API_CONFIG;
```

#### 1.3. Criar serviço HTTP (Axios)

```javascript
// src/services/api.js
import axios from 'axios';
import API_CONFIG from '../config/api';

const api = axios.create({
    baseURL: API_CONFIG.baseURL + API_CONFIG.apiVersion,
    timeout: API_CONFIG.timeout,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Interceptor para adicionar token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Interceptor para refresh token
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            try {
                const refreshToken = localStorage.getItem('refresh_token');
                const response = await axios.post(
                    `${API_CONFIG.baseURL}${API_CONFIG.apiVersion}/auth/refresh`,
                    { refresh_token: refreshToken }
                );

                const { access_token } = response.data;
                localStorage.setItem('access_token', access_token);

                originalRequest.headers.Authorization = `Bearer ${access_token}`;
                return api(originalRequest);
            } catch (refreshError) {
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                window.location.href = '/login';
                return Promise.reject(refreshError);
            }
        }

        return Promise.reject(error);
    }
);

export default api;
```

**✅ Teste da Etapa 1:**

```javascript
// src/tests/api.test.js
import api from '../services/api';

// Testar conexão
api.get('/health')
    .then((response) => console.log('✅ API conectada:', response.data))
    .catch((error) => console.error('❌ Erro:', error));
```

---

### 🟡 ETAPA 2: Autenticação (1-2 horas)

#### 2.1. Criar serviço de autenticação

```javascript
// src/services/auth.service.js
import api from './api';
import { API_ENDPOINTS } from '../config/api';

class AuthService {
    async login(email, password) {
        const formData = new FormData();
        formData.append('username', email);
        formData.append('password', password);

        const response = await api.post(API_ENDPOINTS.login, formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
        });

        const { access_token, refresh_token, token_type } = response.data;

        localStorage.setItem('access_token', access_token);
        localStorage.setItem('refresh_token', refresh_token);
        localStorage.setItem('token_type', token_type);

        return response.data;
    }

    async logout() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('token_type');
    }

    async getCurrentUser() {
        const response = await api.get(API_ENDPOINTS.me);
        return response.data;
    }

    isAuthenticated() {
        return !!localStorage.getItem('access_token');
    }

    getToken() {
        return localStorage.getItem('access_token');
    }
}

export default new AuthService();
```

#### 2.2. Criar componente de Login

```javascript
// src/pages/Login.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import AuthService from '../services/auth.service';

function Login() {
    const [email, setEmail] = useState('admin@arqmanager.com');
    const [password, setPassword] = useState('admin123');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            await AuthService.login(email, password);
            navigate('/dashboard');
        } catch (err) {
            setError(err.response?.data?.detail || 'Erro ao fazer login');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-container">
            <form onSubmit={handleSubmit}>
                <h2>Login - ARQManager</h2>

                {error && <div className="error">{error}</div>}

                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />

                <input
                    type="password"
                    placeholder="Senha"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />

                <button type="submit" disabled={loading}>
                    {loading ? 'Entrando...' : 'Entrar'}
                </button>
            </form>
        </div>
    );
}

export default Login;
```

**✅ Teste da Etapa 2:**

1. Acessar página de login
2. Usar credenciais: admin@arqmanager.com / admin123
3. Verificar se token é salvo no localStorage
4. Verificar redirecionamento para dashboard

---

### 🟢 ETAPA 3: Listagem de Clientes (1-2 horas)

#### 3.1. Criar serviço de clientes

```javascript
// src/services/cliente.service.js
import api from './api';
import { API_ENDPOINTS } from '../config/api';

class ClienteService {
    async getAll(params = {}) {
        const response = await api.get(API_ENDPOINTS.clientes, { params });
        return response.data;
    }

    async getById(id) {
        const response = await api.get(API_ENDPOINTS.clienteById(id));
        return response.data;
    }

    async create(data) {
        const response = await api.post(API_ENDPOINTS.clientes, data);
        return response.data;
    }

    async update(id, data) {
        const response = await api.put(API_ENDPOINTS.clienteById(id), data);
        return response.data;
    }

    async delete(id) {
        const response = await api.delete(API_ENDPOINTS.clienteById(id));
        return response.data;
    }

    async search(query) {
        const response = await api.get(API_ENDPOINTS.clientes, {
            params: { search: query },
        });
        return response.data;
    }
}

export default new ClienteService();
```

#### 3.2. Criar componente de listagem

```javascript
// src/pages/Clientes/ClientesList.jsx
import React, { useState, useEffect } from 'react';
import ClienteService from '../../services/cliente.service';

function ClientesList() {
    const [clientes, setClientes] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [search, setSearch] = useState('');

    useEffect(() => {
        loadClientes();
    }, []);

    const loadClientes = async () => {
        try {
            setLoading(true);
            const data = await ClienteService.getAll();
            setClientes(data);
        } catch (err) {
            setError('Erro ao carregar clientes');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleSearch = async (e) => {
        const query = e.target.value;
        setSearch(query);

        if (query.length >= 3) {
            try {
                const data = await ClienteService.search(query);
                setClientes(data);
            } catch (err) {
                console.error(err);
            }
        } else if (query.length === 0) {
            loadClientes();
        }
    };

    if (loading) return <div>Carregando...</div>;
    if (error) return <div className="error">{error}</div>;

    return (
        <div className="clientes-list">
            <h2>Clientes</h2>

            <input
                type="text"
                placeholder="Buscar cliente..."
                value={search}
                onChange={handleSearch}
            />

            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Nome</th>
                        <th>Email</th>
                        <th>Telefone</th>
                        <th>Tipo</th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
                    {clientes.map((cliente) => (
                        <tr key={cliente.id}>
                            <td>{cliente.id}</td>
                            <td>{cliente.nome}</td>
                            <td>{cliente.email}</td>
                            <td>{cliente.telefone}</td>
                            <td>{cliente.tipo_pessoa}</td>
                            <td>
                                <button onClick={() => handleEdit(cliente.id)}>
                                    Editar
                                </button>
                                <button
                                    onClick={() => handleDelete(cliente.id)}
                                >
                                    Excluir
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default ClientesList;
```

**✅ Teste da Etapa 3:**

1. Acessar página de clientes
2. Verificar se lista carrega (135 clientes)
3. Testar busca
4. Verificar se dados estão corretos

---

### 🔵 ETAPA 4: CRUD Completo de Clientes (2-3 horas)

#### 4.1. Formulário de criação/edição

```javascript
// src/pages/Clientes/ClienteForm.jsx
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import ClienteService from '../../services/cliente.service';

function ClienteForm() {
    const { id } = useParams();
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({
        nome: '',
        email: '',
        telefone: '',
        tipo_pessoa: 'PF',
        identificacao: '',
        logradouro: '',
        numero: '',
        bairro: '',
        cidade: '',
        uf: '',
        cep: '',
    });

    useEffect(() => {
        if (id) {
            loadCliente();
        }
    }, [id]);

    const loadCliente = async () => {
        try {
            const data = await ClienteService.getById(id);
            setFormData(data);
        } catch (err) {
            console.error(err);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        try {
            if (id) {
                await ClienteService.update(id, formData);
            } else {
                await ClienteService.create(formData);
            }
            navigate('/clientes');
        } catch (err) {
            alert('Erro ao salvar cliente');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    return (
        <div className="cliente-form">
            <h2>{id ? 'Editar' : 'Novo'} Cliente</h2>

            <form onSubmit={handleSubmit}>
                <input
                    name="nome"
                    placeholder="Nome"
                    value={formData.nome}
                    onChange={handleChange}
                    required
                />

                <input
                    name="email"
                    type="email"
                    placeholder="Email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                />

                <select
                    name="tipo_pessoa"
                    value={formData.tipo_pessoa}
                    onChange={handleChange}
                >
                    <option value="PF">Pessoa Física</option>
                    <option value="PJ">Pessoa Jurídica</option>
                </select>

                <input
                    name="identificacao"
                    placeholder={formData.tipo_pessoa === 'PF' ? 'CPF' : 'CNPJ'}
                    value={formData.identificacao}
                    onChange={handleChange}
                    required
                />

                {/* Mais campos... */}

                <button type="submit" disabled={loading}>
                    {loading ? 'Salvando...' : 'Salvar'}
                </button>
            </form>
        </div>
    );
}

export default ClienteForm;
```

**✅ Teste da Etapa 4:**

1. Criar novo cliente
2. Editar cliente existente
3. Excluir cliente
4. Validar dados salvos

---

### 🟣 ETAPA 5: Projetos (2-3 horas)

Similar à etapa de clientes, criar:

-   ProjetoService
-   ProjetosList
-   ProjetoForm

**✅ Teste da Etapa 5:**

1. Listar projetos (173 registros)
2. Criar novo projeto
3. Editar projeto
4. Vincular cliente ao projeto

---

### 🟠 ETAPA 6: Propostas (2-3 horas)

Similar às etapas anteriores.

---

### 🔴 ETAPA 7: Dashboard e Relatórios (3-4 horas)

#### 7.1. Criar serviço de dashboard

```javascript
// src/services/dashboard.service.js
import api from './api';

class DashboardService {
    async getStats() {
        const response = await api.get('/dashboard/stats');
        return response.data;
    }

    async getRecentProjects() {
        const response = await api.get('/projetos', {
            params: { limit: 5, sort: '-created_at' },
        });
        return response.data;
    }

    async getFinanceiro(mes, ano) {
        const response = await api.get('/financeiro/resumo', {
            params: { mes, ano },
        });
        return response.data;
    }
}

export default new DashboardService();
```

---

## 📊 Cronograma Estimado

| Etapa     | Descrição            | Tempo         | Acumulado    |
| --------- | -------------------- | ------------- | ------------ |
| 1         | Configuração Inicial | 30 min        | 30 min       |
| 2         | Autenticação         | 1-2h          | 2.5h         |
| 3         | Listagem Clientes    | 1-2h          | 4.5h         |
| 4         | CRUD Clientes        | 2-3h          | 7.5h         |
| 5         | Projetos             | 2-3h          | 10.5h        |
| 6         | Propostas            | 2-3h          | 13.5h        |
| 7         | Dashboard            | 3-4h          | 17.5h        |
| **TOTAL** |                      | **~18 horas** | **2-3 dias** |

---

## 🧪 Checklist de Testes

### Por Etapa:

-   [ ] Etapa 1: API responde no /health
-   [ ] Etapa 2: Login funciona e salva token
-   [ ] Etapa 3: Lista de clientes carrega
-   [ ] Etapa 4: CRUD de clientes completo
-   [ ] Etapa 5: CRUD de projetos completo
-   [ ] Etapa 6: CRUD de propostas completo
-   [ ] Etapa 7: Dashboard exibe dados

### Geral:

-   [ ] CORS configurado corretamente
-   [ ] Tokens JWT funcionando
-   [ ] Refresh token automático
-   [ ] Tratamento de erros
-   [ ] Loading states
-   [ ] Validações de formulário

---

## 🛠️ Ferramentas Úteis

### Para Testes:

```bash
# Testar endpoints manualmente
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@arqmanager.com&password=admin123"

# Testar com token
curl -X GET http://localhost:8000/api/v1/clientes \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

### Postman Collection:

Criar collection com todos os endpoints para testes

---

## 📝 Próximos Passos

**Quer que eu crie:**

1. ✅ Arquivos de configuração (api.js, api.service.js)
2. ✅ Serviço de autenticação completo
3. ✅ Componente de login
4. ✅ Serviço de clientes
5. ✅ Componente de listagem de clientes

**Ou prefere começar por outra etapa?**
