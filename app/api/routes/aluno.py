from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict
from ...core.database import get_db
from ...schemas import Aluno, AlunoCreate
from ...services import AlunoService
from ...api.deps import get_current_user
from ...models.administrador import Administrador

router = APIRouter(prefix="/alunos", tags=["Alunos"])

@router.post("/", response_model=Aluno)
def criar_aluno(
    aluno: AlunoCreate, 
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    service = AlunoService(db)
    return service.criar_aluno(aluno)

@router.get("/", response_model=List[Aluno])
def listar_alunos(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    service = AlunoService(db)
    return service.listar_alunos(skip, limit)

@router.get("/{aluno_id}", response_model=Aluno)
def obter_aluno(
    aluno_id: int, 
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    service = AlunoService(db)
    return service.obter_aluno(aluno_id)

@router.put("/{aluno_id}", response_model=Aluno)
def atualizar_aluno(
    aluno_id: int, 
    aluno: AlunoCreate, 
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    service = AlunoService(db)
    return service.atualizar_aluno(aluno_id, aluno)

@router.delete("/{aluno_id}", response_model=Dict[str, str])
def deletar_aluno(
    aluno_id: int, 
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    service = AlunoService(db)
    return service.deletar_aluno(aluno_id)

@router.get("/{aluno_id}/professores", response_model=List[Dict])
def listar_professores_do_aluno(
    aluno_id: int, 
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    service = AlunoService(db)
    return service.listar_professores_do_aluno(aluno_id)
    
@router.post("/{aluno_id}/professores/{professor_id}", response_model=Dict[str, str])
def associar_professor_ao_aluno(
    aluno_id: int, 
    professor_id: int, 
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    service = AlunoService(db)
    return service.associar_professor(aluno_id, professor_id)

@router.delete("/{aluno_id}/professores/{professor_id}", response_model=Dict[str, str])
def desassociar_professor_do_aluno(
    aluno_id: int, 
    professor_id: int, 
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    service = AlunoService(db)
    return service.desassociar_professor(aluno_id, professor_id)