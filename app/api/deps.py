from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.security import SECRET_KEY, ALGORITHM
from ..models.administrador import Administrador

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Obtém usuário atual do token JWT"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        nome: str = payload.get("sub")
        if nome is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(Administrador).filter(Administrador.nome == nome).first()
    if user is None:
        raise credentials_exception
    
    return user