from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict
from ...core.database import get_db
from ...schemas import ContaReceber, ContaReceberCreate, ContaReceberUpdate
from ...schemas.pagination import PaginatedResponse
from ...services import ContaReceberService
from ...api.deps import get_current_user
from ...models.administrador import Administrador

router = APIRouter(prefix="/contas-receber", tags=["Contas a Receber"])

@router.post("/", response_model=ContaReceber)
def criar_conta_receber(
    conta: ContaReceberCreate,
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    """Cria conta a receber para o administrador logado"""
    service = ContaReceberService(db)
    return service.criar_conta(current_user.id, conta)

@router.get("/", response_model=PaginatedResponse[ContaReceber])
def listar_contas_receber(
    skip: int = 0,
    limit: int = 100,
    status: bool = None,
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    """
    Lista contas a receber do administrador logado com paginação.
    
    - **skip**: Número de registros para pular (default: 0)
    - **limit**: Máximo de registros a retornar (default: 100, max: 1000)
    - **status**: Filtrar por status - True (recebido) ou False (pendente)
    """
    service = ContaReceberService(db)
    contas = service.listar_contas(current_user.id, skip, limit, status)
    total = service.contar_contas(current_user.id, status)
    
    return PaginatedResponse(
        items=contas,
        total=total,
        skip=skip,
        limit=limit
    )

@router.get("/total", response_model=Dict[str, float])
def total_a_receber(
    status: bool = None,
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    """Retorna total a receber"""
    service = ContaReceberService(db)
    total = service.total_a_receber(current_user.id, status)
    return {"total": float(total)}

@router.get("/{conta_id}", response_model=ContaReceber)
def obter_conta_receber(
    conta_id: int,
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    service = ContaReceberService(db)
    return service.obter_conta(conta_id, current_user.id)

@router.put("/{conta_id}", response_model=ContaReceber)
def atualizar_conta_receber(
    conta_id: int,
    conta: ContaReceberUpdate,
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    service = ContaReceberService(db)
    return service.atualizar_conta(conta_id, conta, current_user.id)

@router.patch("/{conta_id}/receber", response_model=ContaReceber)
def marcar_como_recebida(
    conta_id: int,
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    """Marca conta como recebida (status = True)"""
    service = ContaReceberService(db)
    return service.marcar_como_recebida(conta_id, current_user.id)
    
@router.patch("/{conta_id}/deixar-pendente", response_model=ContaReceber)
def marcar_como_pendente(
    conta_id: int,
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    """Marca conta como pendente (status = False)"""
    service = ContaReceberService(db)
    return service.marcar_como_pendente(conta_id, current_user.id)

@router.delete("/{conta_id}", response_model=Dict[str, str])
def deletar_conta_receber(
    conta_id: int,
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    service = ContaReceberService(db)
    return service.deletar_conta(conta_id, current_user.id)