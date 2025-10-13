from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict
from ...core.database import get_db
from ...schemas import AfazerDiario, AfazerDiarioCreate
from ...schemas.pagination import PaginatedResponse
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

@router.get("/", response_model=PaginatedResponse[AfazerDiario])
def listar_afazeres(
    skip: int = 0, 
    limit: int = 100, 
    administrador_id: int = None,
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    """
    Lista afazeres com paginação.
    
    - **skip**: Número de registros para pular (default: 0)
    - **limit**: Máximo de registros a retornar (default: 100, max: 1000)
    - **administrador_id**: Filtrar por ID do administrador (opcional)
    """
    service = AfazerService(db)
    afazeres = service.listar_afazeres(skip, limit, administrador_id)
    total = service.contar_afazeres(administrador_id)
    
    return PaginatedResponse(
        items=afazeres,
        total=total,
        skip=skip,
        limit=limit
    )

@router.put("/{afazer_id}", response_model=AfazerDiario)
def atualizar_afazer(
    afazer_id: int, 
    afazer: AfazerDiarioCreate, 
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    service = AfazerService(db)
    return service.atualizar_afazer(afazer_id, afazer, current_user.id)

@router.delete("/{afazer_id}", response_model=Dict[str, str])
def deletar_afazer(
    afazer_id: int, 
    db: Session = Depends(get_db),
    current_user: Administrador = Depends(get_current_user)
):
    service = AfazerService(db)
    return service.deletar_afazer(afazer_id, current_user.id)