# 📋 Sistema de Logging - Superow API

## Visão Geral

O sistema de logging foi implementado para rastrear todas as operações da API, facilitando debugging, monitoramento e auditoria.

## 📁 Estrutura de Logs

### Localização

- **Diretório**: `logs/`
- **Formato do arquivo**: `app_YYYYMMDD.log`
- **Exemplo**: `app_20251012.log`

### Rotação Automática

- Novo arquivo criado automaticamente a cada dia
- Logs antigos são mantidos para histórico

## 🎯 Níveis de Log

### DEBUG

- **Uso**: Informações detalhadas para desenvolvimento
- **Exemplo**: Parâmetros de funções, queries SQL

```python
logger.debug(f"Buscando aluno ID: {aluno_id}")
```

### INFO

- **Uso**: Confirmação de operações normais
- **Exemplo**: Requisições HTTP, operações bem-sucedidas

```python
logger.info(f"Aluno criado com sucesso - ID: {novo_aluno.id}")
```

### WARNING

- **Uso**: Situações potencialmente problemáticas
- **Exemplo**: Recursos não encontrados, operações de deleção

```python
logger.warning(f"Aluno ID: {aluno_id} não encontrado")
```

### ERROR

- **Uso**: Erros que precisam atenção
- **Exemplo**: Exceções, falhas de operação

```python
logger.error(f"Erro ao criar aluno: {str(e)}")
```

## 🔍 O que é Logado Automaticamente

### 1. Requisições HTTP (Middleware)

```
INFO - Requisição iniciada: GET /api/v1/alunos
INFO - Requisição concluída: GET /api/v1/alunos - Status: 200 - Tempo: 0.123s
```

### 2. Autenticação

```
INFO - Tentativa de login - Usuário: admin
INFO - Login bem-sucedido - Usuário: admin - ID: 1
WARNING - Login falhou - Usuário: admin - Credenciais inválidas
```

### 3. Operações CRUD

```
INFO - Criando novo aluno: João Silva - Usuário: admin
INFO - Aluno criado com sucesso - ID: 15
WARNING - Deletando aluno ID: 15 - Usuário: admin
```

### 4. Erros e Exceções

```
ERROR - Erro ao criar aluno: Duplicate entry '12345678900' for key 'cpf'
ERROR - Traceback: [stack trace completo]
```

## 📝 Como Adicionar Logs no Seu Código

### 1. Importar o Logger

```python
from app.core.logging import logger
```

### 2. Em Rotas (API)

```python
@router.post("/", response_model=Aluno)
def criar_aluno(aluno: AlunoCreate, db: Session = Depends(get_db)):
    logger.info(f"Criando novo aluno: {aluno.nome_completo}")
    try:
        service = AlunoService(db)
        novo_aluno = service.criar_aluno(aluno)
        logger.info(f"Aluno criado - ID: {novo_aluno.id}")
        return novo_aluno
    except Exception as e:
        logger.error(f"Erro ao criar aluno: {str(e)}")
        raise
```

### 3. Em Services

```python
def criar_aluno(self, aluno: AlunoCreate):
    logger.debug(f"Salvando aluno no banco: {aluno.nome_completo}")
    try:
        db_aluno = Aluno(**aluno.model_dump())
        self.db.add(db_aluno)
        self.db.commit()
        logger.info(f"Aluno salvo - ID: {db_aluno.id}")
        return db_aluno
    except Exception as e:
        logger.error(f"Erro no banco: {str(e)}")
        self.db.rollback()
        raise
```

## 🛠️ Configuração Avançada

### Formato do Log

```
2025-10-12 14:30:45 - app.api.routes.aluno - INFO - [aluno.py:15] - Criando novo aluno
```

Formato: `timestamp - módulo - nível - [arquivo:linha] - mensagem`

### Alterar Nível de Log

Em `app/core/logging.py`:

```python
# Para desenvolvimento (mais detalhes)
logging.basicConfig(level=logging.DEBUG, ...)

# Para produção (menos verboso)
logging.basicConfig(level=logging.INFO, ...)
```

## 📊 Monitoramento

### Visualizar Logs em Tempo Real

```bash
# PowerShell
Get-Content logs/app_20251012.log -Wait -Tail 50

# Ou usando tail (Git Bash / WSL)
tail -f logs/app_20251012.log
```

### Filtrar Logs por Nível

```bash
# Apenas erros
Select-String -Path logs/app_20251012.log -Pattern "ERROR"

# Apenas warnings e errors
Select-String -Path logs/app_20251012.log -Pattern "WARNING|ERROR"
```

### Buscar por Usuário/Operação

```bash
Select-String -Path logs/app_20251012.log -Pattern "João Silva"
Select-String -Path logs/app_20251012.log -Pattern "Login"
```

## 🔒 Boas Práticas

### ✅ Faça

- Log de operações importantes (CRUD, autenticação)
- Log de erros com traceback completo
- Log de operações de deleção/modificação
- Inclua IDs e identificadores únicos

### ❌ Evite

- Logar senhas ou tokens
- Logar dados sensíveis (CPF completo, etc)
- Logs excessivos em loops
- Informações de cartão de crédito

### Exemplo de Log Seguro

```python
# ❌ Não faça
logger.info(f"Login: usuário={user}, senha={password}")

# ✅ Faça
logger.info(f"Login: usuário={user}")

# ❌ Não faça
logger.info(f"CPF: {cpf}")

# ✅ Faça
logger.info(f"CPF: {cpf[:3]}***{cpf[-2:]}")  # 123***90
```

## 🎓 Decorator de Log (Avançado)

Use o decorator para logar funções automaticamente:

```python
from app.core.logging import log_function_call

@log_function_call
def funcao_importante(param1, param2):
    # Logs automáticos de entrada e saída
    return resultado
```

## 📈 Análise de Performance

O middleware adiciona o header `X-Process-Time` em todas as respostas:

```
X-Process-Time: 0.123
```

Tempo em segundos para processar a requisição.

## 🚨 Alertas e Monitoramento

### Monitorar Erros Críticos

Configure alertas para:

- Múltiplas tentativas de login falhadas
- Erros 500 frequentes
- Tempo de resposta alto
- Exceções não tratadas

### Ferramentas Recomendadas

- **Desenvolvimento**: Logs no console + arquivo
- **Produção**: ELK Stack, Grafana, Sentry
- **Simples**: Python logging handlers personalizados

## 📞 Suporte

Para mais informações sobre logging:

- Documentação Python: https://docs.python.org/3/library/logging.html
- FastAPI Logging: https://fastapi.tiangolo.com/tutorial/middleware/
