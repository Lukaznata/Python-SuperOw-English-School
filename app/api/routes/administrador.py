from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ...core.database import get_db
from ...schemas import Administrador, AdministradorCreate
from ...services.administrador_service import AdministradorService
from ...api.deps import get_current_user
from ...models.administrador import Administrador as AdminModel

router = APIRouter(prefix="/administradores", tags=["Administradores"])

@router.post("/", response_model=Administrador)
def criar_administrador(admin: AdministradorCreate, db: Session = Depends(get_db)):
    """Criação de admin não requer autenticação (primeiro admin)"""
    service = AdministradorService(db)
    return service.criar_administrador(admin)

@router.get("/", response_model=List[Administrador])
def listar_administradores(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: AdminModel = Depends(get_current_user)
):
    service = AdministradorService(db)
    return service.listar_administradores(skip, limit)

@router.get("/atual", response_model=Administrador)
def obter_administrador_atual(
    current_user: AdminModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retorna o administrador logado"""
    return current_user