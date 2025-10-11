from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict
from ...core.database import get_db
from ...schemas.idioma import Idioma, IdiomaCreate
from ...services.idioma_service import IdiomaService
from ...api.deps import get_current_user
from ...models.administrador import Administrador


router = APIRouter(prefix="/idiomas", tags=["Idiomas"])


@router.post("/", response_model=Idioma)
def criar_idioma(
    idioma: IdiomaCreate, 
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    service = IdiomaService(db)
    return service.criar_idioma(idioma)

@router.get("/", response_model=List[Idioma])
def listar_idiomas(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    service = IdiomaService(db)
    return service.listar_idiomas(skip, limit)

@router.get("/{idioma_id}", response_model=Idioma)
def obter_idioma(
    idioma_id: int, 
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    service = IdiomaService(db)
    return service.obter_idioma(idioma_id)

@router.put("/{idioma_id}", response_model=Idioma)
def atualizar_idioma(
    idioma_id: int, 
    idioma: IdiomaCreate, 
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    service = IdiomaService(db)
    return service.atualizar_idioma(idioma_id, idioma)

@router.delete("/{idioma_id}", response_model=Dict[str, str])
def deletar_idioma(
    idioma_id: int, 
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    service = IdiomaService(db)
    return service.deletar_idioma(idioma_id)