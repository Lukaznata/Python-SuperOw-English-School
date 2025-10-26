from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from ...core.database import get_db
from ...services import StatusMensalidadeService
from ...schemas.status_mensalidade import (
    StatusMensalidadeCreate,
    StatusMensalidadeUpdate,
    StatusMensalidadeResponse,
    StatusMensalidadeWithAluno
)

router = APIRouter(prefix="/mensalidades", tags=["Mensalidades"])

@router.post("/", response_model=StatusMensalidadeResponse, status_code=201)
def criar_mensalidade(
    mensalidade: StatusMensalidadeCreate,
    db: Session = Depends(get_db)
):
    """Criar uma nova mensalidade"""
    try:
        return StatusMensalidadeService.create(db, mensalidade)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar mensalidade: {str(e)}")

@router.get("/", response_model=List[StatusMensalidadeResponse])
def listar_mensalidades(
    aluno_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    mes: Optional[int] = Query(None, ge=1, le=12),
    ano: Optional[int] = Query(None, ge=2000),
    db: Session = Depends(get_db)
):
    """Listar mensalidades com filtros opcionais"""
    mensalidades, _ = StatusMensalidadeService.get_all(
        db, skip=0, limit=10000, aluno_id=aluno_id, status=status, mes=mes, ano=ano
    )
    return mensalidades

@router.get("/pendentes", response_model=List[StatusMensalidadeResponse])
def listar_pendentes(db: Session = Depends(get_db)):
    """Listar mensalidades pendentes ou atrasadas"""
    return StatusMensalidadeService.get_pendentes(db)

@router.get("/aluno/{aluno_id}", response_model=List[StatusMensalidadeResponse])
def listar_por_aluno(
    aluno_id: int = Path(..., ge=1),
    db: Session = Depends(get_db)
):
    """Listar mensalidades de um aluno específico"""
    return StatusMensalidadeService.get_by_aluno(db, aluno_id)

@router.get("/mes/{mes}/ano/{ano}", response_model=List[StatusMensalidadeResponse])
def listar_por_mes_ano(
    mes: int = Path(..., ge=1, le=12),
    ano: int = Path(..., ge=2000),
    db: Session = Depends(get_db)
):
    """Listar mensalidades por mês e ano"""
    return StatusMensalidadeService.get_by_mes_ano(db, mes, ano)

@router.get("/totais")
def obter_totais(
    mes: Optional[int] = Query(None, ge=1, le=12),
    ano: Optional[int] = Query(None, ge=2000),
    db: Session = Depends(get_db)
):
    """Obter totais agrupados por status"""
    return StatusMensalidadeService.get_total_por_status(db, mes, ano)

@router.get("/{mensalidade_id}", response_model=StatusMensalidadeResponse)
def obter_mensalidade(
    mensalidade_id: int = Path(..., ge=1),
    db: Session = Depends(get_db)
):
    """Obter uma mensalidade por ID"""
    mensalidade = StatusMensalidadeService.get_by_id(db, mensalidade_id)
    if not mensalidade:
        raise HTTPException(status_code=404, detail="Mensalidade não encontrada")
    return mensalidade

@router.put("/{mensalidade_id}", response_model=StatusMensalidadeResponse)
def atualizar_mensalidade(
    mensalidade_id: int = Path(..., ge=1),
    mensalidade_data: StatusMensalidadeUpdate = ...,
    db: Session = Depends(get_db)
):
    """Atualizar uma mensalidade"""
    try:
        mensalidade = StatusMensalidadeService.update(db, mensalidade_id, mensalidade_data)
        if not mensalidade:
            raise HTTPException(status_code=404, detail="Mensalidade não encontrada")
        return mensalidade
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar mensalidade: {str(e)}")

@router.delete("/{mensalidade_id}", status_code=204)
def deletar_mensalidade(
    mensalidade_id: int = Path(..., ge=1),
    db: Session = Depends(get_db)
):
    """Deletar uma mensalidade"""
    success = StatusMensalidadeService.delete(db, mensalidade_id)
    if not success:
        raise HTTPException(status_code=404, detail="Mensalidade não encontrada")