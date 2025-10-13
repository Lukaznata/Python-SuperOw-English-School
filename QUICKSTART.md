# 🚀 Guia de Início Rápido - Superow API

## Setup em 5 Minutos

### 1️⃣ Instalar Dependências

```bash
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 2️⃣ Configurar Banco de Dados

```bash
# Criar banco no MySQL
mysql -u root -p
CREATE DATABASE superow_db;
exit;
```

### 3️⃣ Configurar Variáveis de Ambiente

```bash
# Copiar template
copy .env.example .env

# Editar .env com suas credenciais
# DB_USER=seu_usuario
# DB_PASSWORD=sua_senha
# SECRET_KEY=gere-uma-chave-aleatoria
```

### 4️⃣ Executar Migrações

```bash
alembic upgrade head
```

### 5️⃣ Iniciar Servidor

```bash
uvicorn app.main:app --reload
```

✅ API rodando em: http://localhost:8000  
📚 Documentação em: http://localhost:8000/docs

## 🔑 Primeiro Login

### Criar Administrador

Execute no MySQL:

```sql
USE superow_db;

-- Senha: admin123
INSERT INTO administrador (usuario, nome, senha_hash, situacao)
VALUES (
    'admin',
    'Administrador',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5nRzI9WUmRvUy',
    1
);
```

### Fazer Login

```bash
POST http://localhost:8000/api/v1/auth/login
Content-Type: application/json

{
  "nome": "admin",
  "senha": "admin123"
}
```

**Resposta:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Usar Token

Adicione o header em todas as requisições:

```
Authorization: Bearer <seu_token_aqui>
```

## 📝 Testar Endpoints

### Criar Aluno

```bash
POST http://localhost:8000/api/v1/alunos
Authorization: Bearer <token>
Content-Type: application/json

{
  "nome_completo": "João Silva",
  "data_nasc": "1995-05-15",
  "cpf": "12345678900",
  "telefone": "11987654321",
  "pais": "Brasil",
  "situacao": true
}
```

### Listar Alunos

```bash
GET http://localhost:8000/api/v1/alunos
Authorization: Bearer <token>
```

### Healthcheck (sem autenticação)

```bash
GET http://localhost:8000/api/v1/health
```

## 🎯 Próximos Passos

1. ✅ Explorar documentação Swagger em `/docs`
2. ✅ Criar professores e idiomas
3. ✅ Agendar aulas
4. ✅ Gerenciar contas a pagar/receber
5. ✅ Ver logs em `logs/app_YYYYMMDD.log`

## 🐛 Problemas Comuns

### Erro de Conexão com Banco

```
sqlalchemy.exc.OperationalError
```

**Solução**: Verifique credenciais no `.env`

### Secret Key Warning

```
⚠️ AVISO DE SEGURANÇA: SECRET_KEY não foi configurada!
```

**Solução**: Adicione `SECRET_KEY` no `.env`

### Import Error

```
ModuleNotFoundError: No module named 'fastapi'
```

**Solução**: Ative o venv e instale dependências

## 📞 Suporte

- 📖 README completo: `README.md`
- 📋 Logging: `LOGGING.md`
- 📄 Paginação: `PAGINATION.md`
- ✅ TODOs: `TODO.md`
- 📚 Documentação: http://localhost:8000/docs

---

**Pronto! Sua API está funcionando! 🎉**
