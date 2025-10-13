from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict

from ...core.database import get_db
from ...schemas import Professor, ProfessorCreate, Aluno
from ...schemas.pagination import PaginatedResponse
from ...services import ProfessorService
from ...api.deps import get_current_user
from ...models.administrador import Administrador

router = APIRouter(prefix="/professores", tags=["Professores"])

@router.post("/", response_model=Professor)
def criar_professor(
    professor: ProfessorCreate, 
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    service = ProfessorService(db)
    return service.criar_professor(professor)

@router.get("/", response_model=PaginatedResponse[Professor])
def listar_professores(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    """
    Lista professores com paginação.
    
    - **skip**: Número de registros para pular (default: 0)
    - **limit**: Máximo de registros a retornar (default: 100, max: 1000)
    """
    service = ProfessorService(db)
    professores = service.listar_professores(skip, limit)
    total = service.contar_professores()
    
    return PaginatedResponse(
        items=professores,
        total=total,
        skip=skip,
        limit=limit
    )

@router.get("/{professor_id}", response_model=Professor)
def obter_professor(
    professor_id: int, 
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    service = ProfessorService(db)
    return service.obter_professor(professor_id)

@router.put("/{professor_id}", response_model=Professor)
def atualizar_professor(
    professor_id: int, 
    professor: ProfessorCreate, 
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    service = ProfessorService(db)
    return service.atualizar_professor(professor_id, professor)

@router.delete("/{professor_id}", response_model=Dict[str, str])
def deletar_professor(
    professor_id: int, 
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    service = ProfessorService(db)
    return service.deletar_professor(professor_id)

@router.get("/{professor_id}/alunos", response_model=List[Aluno])
def listar_alunos_do_professor(
    professor_id: int, 
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    service = ProfessorService(db)
    return service.listar_alunos_do_professor(professor_id)

@router.post("/{professor_id}/alunos/{aluno_id}", response_model=Dict[str, str])
def associar_aluno_ao_professor(
    professor_id: int, 
    aluno_id: int, 
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    service = ProfessorService(db)
    return service.associar_aluno(professor_id, aluno_id)

@router.delete("/{professor_id}/alunos/{aluno_id}", response_model=Dict[str, str])
def desassociar_aluno_do_professor(
    professor_id: int, 
    aluno_id: int, 
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    service = ProfessorService(db)
    return service.desassociar_aluno(professor_id, aluno_id)