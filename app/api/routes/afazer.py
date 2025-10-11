from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict
from ...core.database import get_db
from ...schemas import AfazerDiario, AfazerDiarioCreate
from ...services.afazer_service import AfazerService
from ...api.deps import get_current_user
from ...models.administrador import Administrador

router = APIRouter(prefix="/afazeres", tags=["Afazeres"])

@router.post("/", response_model=AfazerDiario)
def criar_afazer(
    afazer: AfazerDiarioCreate, 
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    service = AfazerService(db)
    return service.criar_afazer(afazer)

@router.get("/", response_model=List[AfazerDiario])
def listar_afazeres(
    skip: int = 0, 
    limit: int = 100, 
    administrador_id: int = None,
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    service = AfazerService(db)
    return service.listar_afazeres(skip, limit, administrador_id)

@router.put("/{afazer_id}", response_model=AfazerDiario)
def atualizar_afazer(
    afazer_id: int, 
    afazer: AfazerDiarioCreate, 
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    service = AfazerService(db)
    return service.atualizar_afazer(afazer_id, afazer)

@router.delete("/{afazer_id}", response_model=Dict[str, str])
def deletar_afazer(
    afazer_id: int, 
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    service = AfazerService(db)
    return service.deletar_afazer(afazer_id)