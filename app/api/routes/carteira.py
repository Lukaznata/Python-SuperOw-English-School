from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from typing import List, Dict
from ...core.database import get_db
from ...schemas import Carteira, CarteiraCreate
from ...services import CarteiraService
from ...api.deps import get_current_user
from ...models.administrador import Administrador

router = APIRouter(prefix="/carteiras", tags=["Carteiras"])

@router.post("/", response_model=Carteira)
def criar_carteira(
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    """Cria carteira para o administrador logado"""
    service = CarteiraService(db)
    return service.criar_carteira(current_user.id)

@router.get("/", response_model=List[Carteira])
def listar_carteiras(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    service = CarteiraService(db)
    return service.listar_carteiras(skip, limit)

@router.get("/minha", response_model=Carteira)
def obter_minha_carteira(
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    """Obtém carteira do administrador logado com saldo calculado automaticamente"""
    service = CarteiraService(db)
    return service.obter_carteira_por_admin(current_user.id)

@router.get("/{carteira_id}", response_model=Carteira)
def obter_carteira(
    carteira_id: int,
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    service = CarteiraService(db)
    return service.obter_carteira(carteira_id)

@router.delete("/{carteira_id}", response_model=Dict[str, str])
def deletar_carteira(
    carteira_id: int,
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    service = CarteiraService(db)
    return service.deletar_carteira(carteira_id)