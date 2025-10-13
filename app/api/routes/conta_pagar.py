from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict
from ...core.database import get_db
from ...schemas import ContaPagar, ContaPagarCreate, ContaPagarUpdate
from ...schemas.pagination import PaginatedResponse
from ...services import ContaPagarService
from ...api.deps import get_current_user
from ...models.administrador import Administrador

router = APIRouter(prefix="/contas-pagar", tags=["Contas a Pagar"])

@router.post("/", response_model=ContaPagar)
def criar_conta_pagar(
    conta: ContaPagarCreate,
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    """Cria conta a pagar para o administrador logado"""
    service = ContaPagarService(db)
    return service.criar_conta(current_user.id, conta)

@router.get("/", response_model=PaginatedResponse[ContaPagar])
def listar_contas_pagar(
    skip: int = 0,
    limit: int = 100,
    status: bool = None,
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    """
    Lista contas a pagar do administrador logado com paginação.
    
    - **skip**: Número de registros para pular (default: 0)
    - **limit**: Máximo de registros a retornar (default: 100, max: 1000)
    - **status**: Filtrar por status - True (pago) ou False (pendente)
    """
    service = ContaPagarService(db)
    contas = service.listar_contas(current_user.id, skip, limit, status)
    total = service.contar_contas(current_user.id, status)
    
    return PaginatedResponse(
        items=contas,
        total=total,
        skip=skip,
        limit=limit
    )

@router.get("/total", response_model=Dict[str, float])
def total_a_pagar(
    status: bool = None,
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    """Retorna total a pagar"""
    service = ContaPagarService(db)
    total = service.total_a_pagar(current_user.id, status)
    return {"total": float(total)}

@router.get("/{conta_id}", response_model=ContaPagar)
def obter_conta_pagar(
    conta_id: int,
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    service = ContaPagarService(db)
    return service.obter_conta(conta_id, current_user.id)

@router.put("/{conta_id}", response_model=ContaPagar)
def atualizar_conta_pagar(
    conta_id: int,
    conta: ContaPagarUpdate,
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    service = ContaPagarService(db)
    return service.atualizar_conta(conta_id, conta, current_user.id)

@router.patch("/{conta_id}/pagar", response_model=ContaPagar)
def marcar_como_paga(
    conta_id: int,
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    """Marca conta como paga (status = True)"""
    service = ContaPagarService(db)
    return service.marcar_como_paga(conta_id, current_user.id)

@router.patch("/{conta_id}/deixar-pendente", response_model=ContaPagar)
def marcar_como_pendente(
    conta_id: int,
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    """Marca conta como pendente (status = False)"""
    service = ContaPagarService(db)
    return service.marcar_como_pendente(conta_id, current_user.id)

@router.delete("/{conta_id}", response_model=Dict[str, str])
def deletar_conta_pagar(
    conta_id: int,
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    service = ContaPagarService(db)
    return service.deletar_conta(conta_id, current_user.id)