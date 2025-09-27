from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..models import models
from ..schemas import schemas
from passlib.context import CryptContext
from datetime import datetime

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/administradores/", response_model=schemas.Administrador)
def criar_administrador(admin: schemas.AdministradorCreate, db: Session = Depends(get_db)):
    senha_hash = pwd_context.hash(admin.senha)
    db_admin = models.Administrador(nome=admin.nome, senha_hash=senha_hash)
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin


@router.get("/administradores/", response_model=List[schemas.Administrador])
def listar_administradores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    administradores = db.query(models.Administrador).offset(skip).limit(limit).all()
    return administradores


@router.post("/afazeres/", response_model=schemas.AfazerDiario)
def criar_afazer(
    afazer: schemas.AfazerDiarioCreate, 
    administrador_id: int,
    db: Session = Depends(get_db)
):
    db_afazer = models.AfazerDiario(**afazer.dict(), administrador_id=administrador_id)
    db.add(db_afazer)
    db.commit()
    db.refresh(db_afazer)
    return db_afazer


@router.get("/afazeres/", response_model=List[schemas.AfazerDiario])
def listar_afazeres(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    afazeres = db.query(models.AfazerDiario).offset(skip).limit(limit).all()
    return afazeres


@router.put("/afazeres/{afazer_id}", response_model=schemas.AfazerDiario)
def atualizar_afazer(
    afazer_id: int,
    afazer: schemas.AfazerDiarioCreate,
    db: Session = Depends(get_db)
):
    db_afazer = db.query(models.AfazerDiario).filter(models.AfazerDiario.id == afazer_id).first()
    if db_afazer is None:
        raise HTTPException(status_code=404, detail="Afazer não encontrado")
    
    for key, value in afazer.dict().items():
        setattr(db_afazer, key, value)
    
    db.commit()
    db.refresh(db_afazer)
    return db_afazer


@router.delete("/afazeres/{afazer_id}")
def deletar_afazer(afazer_id: int, db: Session = Depends(get_db)):
    db_afazer = db.query(models.AfazerDiario).filter(models.AfazerDiario.id == afazer_id).first()
    if db_afazer is None:
        raise HTTPException(status_code=404, detail="Afazer não encontrado")
    
    db.delete(db_afazer)
    db.commit()
    return {"message": "Afazer deletado com sucesso"}