# 📄 Guia de Paginação - Superow API

## Visão Geral

O sistema de paginação permite listar grandes quantidades de dados de forma eficiente, retornando apenas um subconjunto de resultados por vez.

## 🎯 Schema de Paginação

### PaginatedResponse[T]

Schema genérico para respostas paginadas:

```python
{
    "items": [...],           # Lista de itens
    "total": 150,            # Total de itens no banco
    "skip": 0,               # Índice do primeiro item
    "limit": 20,             # Quantidade de itens retornados
    "has_more": true,        # Há mais itens para carregar?
    "page": 1,               # Página atual
    "total_pages": 8         # Total de páginas
}
```

## 📝 Como Usar

### 1. Importar o Schema

```python
from app.schemas.pagination import PaginatedResponse, PaginationParams
```

### 2. Atualizar Rota para Retornar Paginado

**Antes:**

```python
@router.get("/", response_model=List[Aluno])
def listar_alunos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = AlunoService(db)
    return service.listar_alunos(skip, limit)
```

**Depois:**

```python
@router.get("/", response_model=PaginatedResponse[Aluno])
def listar_alunos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = AlunoService(db)
    alunos = service.listar_alunos(skip, limit)
    total = service.contar_alunos()  # Novo método no service

    return PaginatedResponse(
        items=alunos,
        total=total,
        skip=skip,
        limit=limit
    )
```

### 3. Adicionar Método de Contagem no Service

```python
class AlunoService:
    def contar_alunos(self) -> int:
        """Conta o total de alunos"""
        return self.db.query(Aluno).count()
```

## 🚀 Exemplo Completo

### Rota Atualizada

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas import Aluno
from app.schemas.pagination import PaginatedResponse
from app.services import AlunoService

router = APIRouter(prefix="/alunos", tags=["Alunos"])

@router.get("/", response_model=PaginatedResponse[Aluno])
def listar_alunos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Lista alunos com paginação.

    - **skip**: Número de registros para pular (default: 0)
    - **limit**: Máximo de registros a retornar (default: 100, max: 1000)
    """
    service = AlunoService(db)
    alunos = service.listar_alunos(skip, limit)
    total = service.contar_alunos()

    return PaginatedResponse(
        items=alunos,
        total=total,
        skip=skip,
        limit=limit
    )
```

### Consumindo a API (Frontend)

#### JavaScript/TypeScript

```javascript
// Primeira página (20 itens)
const response = await fetch(
  "http://localhost:8000/api/v1/alunos?skip=0&limit=20"
);
const data = await response.json();

console.log(data.items); // Array com 20 alunos
console.log(data.total); // Total de alunos (ex: 150)
console.log(data.page); // 1
console.log(data.total_pages); // 8
console.log(data.has_more); // true

// Segunda página
const response2 = await fetch(
  "http://localhost:8000/api/v1/alunos?skip=20&limit=20"
);
```

#### Python (requests)

```python
import requests

# Primeira página
response = requests.get('http://localhost:8000/api/v1/alunos', params={
    'skip': 0,
    'limit': 20
})

data = response.json()
alunos = data['items']
total = data['total']
has_more = data['has_more']

# Próxima página
if has_more:
    response = requests.get('http://localhost:8000/api/v1/alunos', params={
        'skip': 20,
        'limit': 20
    })
```

## 🎨 Exemplo com React

```typescript
interface PaginatedResponse<T> {
  items: T[];
  total: number;
  skip: number;
  limit: number;
  has_more: boolean;
  page: number;
  total_pages: number;
}

function AlunosList() {
  const [alunos, setAlunos] = useState<Aluno[]>([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const limit = 20;

  const fetchAlunos = async (pageNum: number) => {
    const skip = (pageNum - 1) * limit;
    const response = await fetch(
      `http://localhost:8000/api/v1/alunos?skip=${skip}&limit=${limit}`
    );
    const data: PaginatedResponse<Aluno> = await response.json();

    setAlunos(data.items);
    setTotalPages(data.total_pages);
  };

  useEffect(() => {
    fetchAlunos(page);
  }, [page]);

  return (
    <div>
      <ul>
        {alunos.map((aluno) => (
          <li key={aluno.id}>{aluno.nome_completo}</li>
        ))}
      </ul>

      <div>
        <button
          onClick={() => setPage((p) => Math.max(1, p - 1))}
          disabled={page === 1}
        >
          Anterior
        </button>

        <span>
          Página {page} de {totalPages}
        </span>

        <button
          onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
          disabled={page === totalPages}
        >
          Próxima
        </button>
      </div>
    </div>
  );
}
```

## 🔍 Casos de Uso Comuns

### Infinite Scroll

```javascript
let skip = 0;
const limit = 20;
let loading = false;

async function loadMore() {
  if (loading) return;
  loading = true;

  const response = await fetch(`/api/v1/alunos?skip=${skip}&limit=${limit}`);
  const data = await response.json();

  // Adiciona novos itens
  items.push(...data.items);
  skip += limit;
  loading = false;

  // Continua carregando se houver mais
  if (data.has_more) {
    // Pode carregar mais quando usuário rolar
  }
}
```

### Busca com Paginação

```python
@router.get("/", response_model=PaginatedResponse[Aluno])
def listar_alunos(
    skip: int = 0,
    limit: int = 100,
    search: str = None,
    db: Session = Depends(get_db)
):
    service = AlunoService(db)

    if search:
        alunos = service.buscar_alunos(search, skip, limit)
        total = service.contar_busca(search)
    else:
        alunos = service.listar_alunos(skip, limit)
        total = service.contar_alunos()

    return PaginatedResponse(
        items=alunos,
        total=total,
        skip=skip,
        limit=limit
    )
```

## ⚙️ Parâmetros

| Parâmetro | Tipo | Padrão | Máximo | Descrição                          |
| --------- | ---- | ------ | ------ | ---------------------------------- |
| **skip**  | int  | 0      | -      | Número de registros a pular        |
| **limit** | int  | 100    | 1000   | Quantidade de registros a retornar |

### Validações Automáticas

- `skip` não pode ser negativo (mínimo: 0)
- `limit` tem máximo de 1000 (para performance)
- `limit` mínimo é 1

## 📊 Propriedades Calculadas

### has_more

```python
has_more = (skip + limit) < total
```

Indica se há mais registros após a página atual.

### page

```python
page = (skip // limit) + 1
```

Número da página atual (começa em 1).

### total_pages

```python
total_pages = (total + limit - 1) // limit
```

Total de páginas disponíveis.

## 🎯 Boas Práticas

### ✅ Faça

- Use paginação em todas as listagens
- Defina um `limit` razoável (10-100)
- Mostre total de páginas ao usuário
- Implemente cache quando possível
- Adicione índices no banco para campos filtrados

### ❌ Evite

- Retornar todos os registros sem paginação
- `limit` muito alto (> 1000)
- Fazer queries sem índices
- Ignorar o campo `total` (útil para UI)

## 🚀 Performance

### Otimizações

1. **Índices no Banco**

```sql
CREATE INDEX idx_aluno_nome ON alunos(nome_completo);
CREATE INDEX idx_aluno_situacao ON alunos(situacao);
```

2. **Query Eficiente**

```python
def listar_alunos(self, skip: int, limit: int):
    return (
        self.db.query(Aluno)
        .filter(Aluno.situacao == True)  # Filtro com índice
        .order_by(Aluno.id)              # Ordenação consistente
        .offset(skip)
        .limit(limit)
        .all()
    )
```

3. **Cache de Contagem**

```python
from functools import lru_cache
from datetime import datetime, timedelta

@lru_cache(maxsize=1)
def contar_alunos_cache(timestamp: int):
    # Cache válido por 5 minutos
    return db.query(Aluno).count()

def contar_alunos(self):
    # Timestamp arredondado para 5 minutos
    ts = int(time.time() / 300)
    return contar_alunos_cache(ts)
```

## 📞 Suporte

Para dúvidas sobre paginação, consulte:

- Documentação FastAPI: https://fastapi.tiangolo.com/
- SQLAlchemy Pagination: https://docs.sqlalchemy.org/
