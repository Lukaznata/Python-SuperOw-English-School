from sqlalchemy.orm import Session
from ..models.idioma import Idioma
from ..schemas.idioma import IdiomaCreate
from fastapi import HTTPException, status
import logging

# Configuração do logger
logger = logging.getLogger(__name__)

class IdiomaService:
    def __init__(self, db: Session):
        self.db = db

    def criar_idioma(self, idioma: IdiomaCreate):
        db_idioma = Idioma(
            nome_idioma=idioma.nome_idioma 
        )
        self.db.add(db_idioma)
        self.db.commit()
        self.db.refresh(db_idioma)
        return db_idioma

    def listar_idiomas(self, skip: int = 0, limit: int = 100):
        return self.db.query(Idioma).offset(skip).limit(limit).all()

    def obter_idioma(self, idioma_id: int):
        idioma = self.db.query(Idioma).filter(Idioma.id == idioma_id).first()
        if idioma is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Idioma não encontrado")
        return idioma

    def atualizar_idioma(self, idioma_id: int, idioma: IdiomaCreate):
        db_idioma = self.obter_idioma(idioma_id)
        db_idioma.nome_idioma = idioma.nome_idioma
        self.db.commit()
        self.db.refresh(db_idioma)
        return db_idioma

    def deletar_idioma(self, idioma_id: int):
        idioma = self.obter_idioma(idioma_id)
        self.db.delete(idioma)
        self.db.commit()
        return {"message": "Idioma deletado com sucesso"}