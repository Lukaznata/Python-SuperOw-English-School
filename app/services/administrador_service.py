from sqlalchemy.orm import Session
from ..models import Administrador
from ..schemas import AdministradorCreate
from ..core.security import get_password_hash, verify_password
from fastapi import HTTPException, status

class AdministradorService:
    def __init__(self, db: Session):
        self.db = db

    def criar_administrador(self, administrador: AdministradorCreate):
        # Verificar se já existe
        db_admin = self.db.query(Administrador).filter(
            Administrador.nome == administrador.nome
        ).first()
        if db_admin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Administrador já existe"
            )
        
        # Criar com senha hasheada
        senha_hash = get_password_hash(administrador.senha)
        db_administrador = Administrador(
            nome=administrador.nome,
            senha_hash=senha_hash,
        )
        self.db.add(db_administrador)
        self.db.commit()
        self.db.refresh(db_administrador)
        return db_administrador

    def autenticar(self, nome: str, senha: str):
        """Autentica usuário e retorna se válido"""
        administrador = self.db.query(Administrador).filter(
            Administrador.nome == nome
        ).first()
        
        if not administrador:
            return None
        if not verify_password(senha, administrador.senha_hash):
            return None
        
        return administrador

    def obter_por_nome(self, nome: str):
        return self.db.query(Administrador).filter(
            Administrador.nome == nome
        ).first()

    def listar_administradores(self, skip: int = 0, limit: int = 100):
        return self.db.query(Administrador).offset(skip).limit(limit).all()

    def obter_administrador(self, administrador_id: int):
        administrador = self.db.query(Administrador).filter(
            Administrador.id == administrador_id
        ).first()
        if administrador is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Administrador não encontrado"
            )
        return administrador

    def deletar_administrador(self, administrador_id: int):
        administrador = self.obter_administrador(administrador_id)
        self.db.delete(administrador)
        self.db.commit()
        return {"message": "Administrador deletado com sucesso"}