from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from ...core.database import get_db
from ...core.security import create_access_token
from ...schemas.administrador import AdministradorLogin
from ...schemas.token import Token
from ...services.administrador_service import AdministradorService
from ...core.logging import logger

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/login", response_model=Token)
def login(credenciais: AdministradorLogin, db: Session = Depends(get_db)):
    """Login com nome e senha"""
    logger.info(f"Tentativa de login - Usuário: {credenciais.nome}")
    
    try:
        service = AdministradorService(db)
        administrador = service.autenticar(credenciais.nome, credenciais.senha)
        
        if not administrador:
            logger.warning(f"Login falhou - Usuário: {credenciais.nome} - Credenciais inválidas")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Nome ou senha incorretos",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token = create_access_token(
            data={"sub": administrador.nome}
        )
        
        logger.info(f"Login bem-sucedido - Usuário: {credenciais.nome} - ID: {administrador.id}")
        return {"access_token": access_token, "token_type": "bearer"}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro no processo de login - Usuário: {credenciais.nome} - Erro: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao processar login"
        )