from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict
from ...core.database import get_db
from ...schemas import Aula, AulaCreate, Aluno
from ...schemas.pagination import PaginatedResponse
from ...services import AulaService
from ...api.deps import get_current_user
from ...models.administrador import Administrador

router = APIRouter(prefix="/aulas", tags=["Aulas"])

@router.post("/", response_model=Aula)
def criar_aula(
    aula: AulaCreate, 
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    service = AulaService(db)
    return service.criar_aula(aula)

@router.get("/", response_model=PaginatedResponse[Aula])
def listar_aulas(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    """
    Lista aulas com paginação.
    
    - **skip**: Número de registros para pular (default: 0)
    - **limit**: Máximo de registros a retornar (default: 100, max: 1000)
    """
    service = AulaService(db)
    aulas = service.listar_aulas(skip, limit)
    total = service.contar_aulas()
    
    return PaginatedResponse(
        items=aulas,
        total=total,
        skip=skip,
        limit=limit
    )

@router.get("/{aula_id}", response_model=Aula)
def obter_aula(
    aula_id: int, 
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    service = AulaService(db)
    return service.obter_aula(aula_id)

@router.get("/{aula_id}/alunos", response_model=List[Aluno])
def listar_alunos_da_aula(
    aula_id: int, 
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    service = AulaService(db)
    return service.listar_alunos_da_aula(aula_id)

@router.post("/{aula_id}/alunos/{aluno_id}", response_model=Dict[str, str])
def associar_aluno_na_aula(
    aula_id: int, 
    aluno_id: int, 
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    service = AulaService(db)
    return service.associar_aluno(aula_id, aluno_id)

@router.delete("/{aula_id}/alunos/{aluno_id}", response_model=Dict[str, str])
def desassociar_aluno_da_aula(
    aula_id: int, 
    aluno_id: int, 
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    service = AulaService(db)
    return service.desassociar_aluno(aula_id, aluno_id)

@router.put("/{aula_id}", response_model=Aula)
def atualizar_aula(
    aula_id: int, 
    aula: AulaCreate, 
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    service = AulaService(db)
    return service.atualizar_aula(aula_id, aula)

@router.delete("/{aula_id}", response_model=Dict[str, str])
def deletar_aula(
    aula_id: int, 
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    service = AulaService(db)
    return service.deletar_aula(aula_id)