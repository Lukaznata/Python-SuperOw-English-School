from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from ...core.database import get_db
from ...core.security import create_access_token
from ...schemas.administrador import AdministradorLogin
from ...schemas.token import Token
from ...services.administrador_service import AdministradorService

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/login", response_model=Token)
def login(credenciais: AdministradorLogin, db: Session = Depends(get_db)):
    """Login com nome e senha"""
    service = AdministradorService(db)
    administrador = service.autenticar(credenciais.nome, credenciais.senha)
    
    if not administrador:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nome ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": administrador.nome}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}