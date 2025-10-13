from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from ...core.database import get_db
from datetime import datetime
import sys

router = APIRouter(tags=["Health"])

@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    """
    Endpoint de healthcheck para monitoramento da API.
    
    Retorna:
    - Status da API
    - Status do banco de dados
    - Versão do Python
    - Timestamp atual
    """
    
    # Verifica conexão com o banco
    db_status = "healthy"
    db_message = "Conexão com banco de dados OK"
    
    try:
        # Tenta executar query simples
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = "unhealthy"
        db_message = f"Erro ao conectar com banco: {str(e)}"
    
    response = {
        "status": "healthy" if db_status == "healthy" else "unhealthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Superow API",
        "version": "1.0.0",
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "database": {
            "status": db_status,
            "message": db_message
        }
    }
    
    return response


@router.get("/health/simple")
def simple_health_check():
    """
    Healthcheck simples sem dependências.
    Útil para verificar se a API está respondendo.
    """
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat()
    }
