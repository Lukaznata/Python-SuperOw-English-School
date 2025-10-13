from pydantic import BaseModel
from typing import Generic, TypeVar, List

# TypeVar para tipos genéricos
T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    """
    Schema genérico para respostas paginadas.
    
    Uso:
    ```python
    @router.get("/", response_model=PaginatedResponse[Aluno])
    def listar_alunos(skip: int = 0, limit: int = 100):
        ...
        return PaginatedResponse(
            items=alunos,
            total=total,
            skip=skip,
            limit=limit
        )
    ```
    """
    items: List[T]
    total: int
    skip: int
    limit: int
    
    @property
    def has_more(self) -> bool:
        """Indica se há mais itens para carregar"""
        return (self.skip + self.limit) < self.total
    
    @property
    def page(self) -> int:
        """Número da página atual (começa em 1)"""
        if self.limit == 0:
            return 1
        return (self.skip // self.limit) + 1
    
    @property
    def total_pages(self) -> int:
        """Total de páginas"""
        if self.limit == 0:
            return 1
        return (self.total + self.limit - 1) // self.limit
    
    class Config:
        from_attributes = True


class PaginationParams(BaseModel):
    """
    Parâmetros de paginação reutilizáveis.
    
    Uso:
    ```python
    @router.get("/")
    def listar_alunos(pagination: PaginationParams = Depends()):
        skip = pagination.skip
        limit = pagination.limit
    ```
    """
    skip: int = 0
    limit: int = 100
    
    def __init__(self, skip: int = 0, limit: int = 100):
        super().__init__(skip=max(0, skip), limit=min(max(1, limit), 1000))
