from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict
from ...core.database import get_db
from ...schemas import Aluno, AlunoCreate, Professor
from ...schemas.pagination import PaginatedResponse
from ...services import AlunoService
from ...api.deps import get_current_user
from ...models.administrador import Administrador
from ...core.logging import logger

router = APIRouter(prefix="/alunos", tags=["Alunos"])

@router.post("/", response_model=Aluno)
def criar_aluno(
    aluno: AlunoCreate, 
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    logger.info(f"Criando novo aluno: {aluno.nome_completo} - Usuário: {current_user.nome}")
    try:
        service = AlunoService(db)
        novo_aluno = service.criar_aluno(aluno)
        logger.info(f"Aluno criado com sucesso - ID: {novo_aluno.id}")
        return novo_aluno
    except Exception as e:
        logger.error(f"Erro ao criar aluno: {str(e)}")
        raise

@router.get("/", response_model=PaginatedResponse[Aluno])
def listar_alunos(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    """
    Lista alunos com paginação.
    
    - **skip**: Número de registros para pular (default: 0)
    - **limit**: Máximo de registros a retornar (default: 100, max: 1000)
    """
    logger.info(f"Listando alunos - skip: {skip}, limit: {limit} - Usuário: {current_user.nome}")
    service = AlunoService(db)
    alunos = service.listar_alunos(skip, limit)
    total = service.contar_alunos()
    logger.info(f"Retornando {len(alunos)} de {total} alunos")
    
    return PaginatedResponse(
        items=alunos,
        total=total,
        skip=skip,
        limit=limit
    )

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
    logger.warning(f"Deletando aluno ID: {aluno_id} - Usuário: {current_user.nome}")
    try:
        service = AlunoService(db)
        resultado = service.deletar_aluno(aluno_id)
        logger.info(f"Aluno ID: {aluno_id} deletado com sucesso")
        return resultado
    except Exception as e:
        logger.error(f"Erro ao deletar aluno ID: {aluno_id} - {str(e)}")
        raise

@router.get("/{aluno_id}/professores", response_model=List[Professor])
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