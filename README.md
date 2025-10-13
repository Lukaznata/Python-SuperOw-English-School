# 🎓 Superow - Sistema de Gerenciamento de Escola de Inglês

API REST desenvolvida com FastAPI para gerenciar alunos, professores, aulas e finanças de uma escola de inglês.

## 🚀 Funcionalidades

- ✅ **Autenticação JWT** - Login seguro com tokens
- ✅ **Gerenciamento de Alunos** - CRUD completo com associação de professores
- ✅ **Gerenciamento de Professores** - Cadastro com idiomas e MEI
- ✅ **Gestão de Aulas** - Agendamento com valores e repetições
- ✅ **Controle Financeiro** - Contas a pagar/receber e carteira
- ✅ **Tarefas (Afazeres)** - Sistema de to-do list
- ✅ **Validações** - CPF, telefone, valores monetários
- ✅ **Logging Completo** - Rastreamento de todas operações
- ✅ **CORS Configurado** - Pronto para frontend

## 📋 Pré-requisitos

- Python 3.8+
- MySQL 8.0+
- pip (gerenciador de pacotes Python)

## 🔧 Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/Lukaznata/Python-SuperOw-English-School.git
cd Python-SuperOw-English-School/backend
```

### 2. Crie e ative o ambiente virtual
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente
```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o arquivo .env com suas configurações
# Configure: banco de dados, SECRET_KEY, etc
```

### 5. Configure o banco de dados
```bash
# Crie o banco de dados MySQL
mysql -u root -p
CREATE DATABASE superow_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit;

# Execute as migrações
alembic upgrade head

# OU recrie o banco do zero
python recreate_db.py
```

### 6. Inicie o servidor
```bash
uvicorn app.main:app --reload
```

A API estará disponível em: `http://localhost:8000`

## 📚 Documentação da API

Após iniciar o servidor, acesse:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔐 Autenticação

### Primeiro Acesso

1. Crie um administrador (use o script ou insira direto no banco):
```python
from app.core.security import get_password_hash
# Hash: senha123
# Insira no banco com nome: admin, senha_hash: $2b$12$...
```

2. Faça login:
```bash
POST /api/v1/auth/login
{
  "nome": "admin",
  "senha": "senha123"
}
```

3. Use o token retornado:
```bash
Authorization: Bearer <seu_token_aqui>
```

## 📂 Estrutura do Projeto

```
backend/
├── app/
│   ├── api/
│   │   ├── routes/         # Endpoints da API
│   │   └── deps.py         # Dependências (autenticação)
│   ├── core/
│   │   ├── database.py     # Configuração do banco
│   │   ├── security.py     # JWT e criptografia
│   │   ├── logging.py      # Sistema de logs
│   │   └── validators.py   # Validações customizadas
│   ├── models/             # Modelos SQLAlchemy
│   ├── schemas/            # Schemas Pydantic
│   ├── services/           # Lógica de negócio
│   └── main.py            # Aplicação principal
├── alembic/               # Migrações do banco
├── logs/                  # Arquivos de log
├── .env                   # Variáveis de ambiente (não versionado)
├── .env.example          # Template de configuração
├── requirements.txt       # Dependências Python
└── README.md             # Este arquivo
```

## 🔧 Variáveis de Ambiente

Arquivo `.env`:

```env
# Banco de Dados
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_NAME=superow_db

# Segurança
SECRET_KEY=sua-chave-secreta-super-segura-de-no-minimo-32-caracteres
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

## 🛠️ Comandos Úteis

```bash
# Iniciar servidor em modo desenvolvimento
uvicorn app.main:app --reload

# Iniciar em porta específica
uvicorn app.main:app --reload --port 8080

# Criar nova migração
alembic revision --autogenerate -m "descrição"

# Aplicar migrações
alembic upgrade head

# Ver logs em tempo real
Get-Content logs/app_20251012.log -Wait -Tail 50
```

## 📊 Endpoints Principais

### Autenticação
- `POST /api/v1/auth/login` - Login

### Alunos
- `GET /api/v1/alunos` - Listar alunos
- `POST /api/v1/alunos` - Criar aluno
- `GET /api/v1/alunos/{id}` - Obter aluno
- `PUT /api/v1/alunos/{id}` - Atualizar aluno
- `DELETE /api/v1/alunos/{id}` - Deletar aluno

### Professores
- `GET /api/v1/professores` - Listar professores
- `POST /api/v1/professores` - Criar professor
- Similar aos endpoints de alunos...

### Aulas
- `GET /api/v1/aulas` - Listar aulas
- `POST /api/v1/aulas` - Criar aula
- Similar aos endpoints anteriores...

### Financeiro
- `GET /api/v1/contas-pagar` - Contas a pagar
- `GET /api/v1/contas-receber` - Contas a receber
- `GET /api/v1/carteira` - Saldo da carteira

## 🧪 Testes

```bash
# Execute os testes (quando implementados)
pytest

# Com cobertura
pytest --cov=app tests/
```

## 📝 Validações Implementadas

- **CPF**: Validação completa com dígitos verificadores
- **Telefone**: Formato brasileiro (11) 98765-4321
- **MEI**: 14 dígitos
- **Valores**: Monetários devem ser positivos
- **Dia de Cobrança**: Entre 1 e 31

## 📖 Logging

Todos os logs são salvos em `logs/app_YYYYMMDD.log`

Ver documentação completa em: [LOGGING.md](LOGGING.md)

## 🔒 Segurança

- ✅ Senhas com hash bcrypt
- ✅ Autenticação JWT
- ✅ Tokens com expiração configurável
- ✅ CORS restrito
- ✅ Validação de inputs
- ✅ SQL Injection protegido (SQLAlchemy ORM)

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto é privado e de propriedade da Superow English School.

## 👥 Autores

- **Lucas** - [@Lukaznata](https://github.com/Lukaznata)

## 🐛 Reportar Bugs

Encontrou um bug? Abra uma issue no GitHub com:
- Descrição do problema
- Passos para reproduzir
- Comportamento esperado vs atual
- Screenshots (se aplicável)

## 📞 Suporte

Para dúvidas ou suporte, entre em contato através do GitHub Issues.
