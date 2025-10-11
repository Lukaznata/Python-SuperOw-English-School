from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import AfazerDiario, Administrador
from ..schemas import AfazerDiarioCreate
from typing import List

from ..core.logging import logger

class AfazerService:
    def __init__(self, db: Session):
        self.db = db

    def criar_afazer(self, afazer: AfazerDiarioCreate) -> AfazerDiario:
        try:
            logger.info(f"Tentando criar novo afazer para administrador {afazer.administrador_id}")
            admin = self.db.query(Administrador).filter(
                Administrador.id == afazer.administrador_id
            ).first()
            if not admin:
                logger.warning(f"Tentativa de criar afazer para administrador inexistente: {afazer.administrador_id}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Administrador com ID {afazer.administrador_id} não encontrado"
                )

            db_afazer = AfazerDiario(**afazer.dict())
            self.db.add(db_afazer)
            self.db.commit()
            self.db.refresh(db_afazer)
            logger.info(f"Afazer criado com sucesso: ID {db_afazer.id}")
            return db_afazer
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao criar afazer: {str(e)}")
            raise

    def listar_afazeres(self, skip: int = 0, limit: int = 100, administrador_id: int = None) -> List[AfazerDiario]:
        try:
            query = self.db.query(AfazerDiario)
            if administrador_id:
                query = query.filter(AfazerDiario.administrador_id == administrador_id)
            return query.offset(skip).limit(limit).all()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao listar afazeres"
            )

    def atualizar_afazer(self, afazer_id: int, afazer: AfazerDiarioCreate) -> AfazerDiario:
        try:
            logger.info(f"Tentando atualizar afazer: ID {afazer_id}")
            db_afazer = self.db.query(AfazerDiario).filter(AfazerDiario.id == afazer_id).first()
            if not db_afazer:
                logger.warning(f"Tentativa de atualizar afazer inexistente: ID {afazer_id}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Afazer não encontrado"
                )

            admin = self.db.query(Administrador).filter(
                Administrador.id == afazer.administrador_id
            ).first()
            if not admin:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Administrador com ID {afazer.administrador_id} não encontrado"
                )

            for key, value in afazer.dict().items():
                setattr(db_afazer, key, value)
            
            self.db.commit()
            self.db.refresh(db_afazer)
            logger.info(f"Afazer atualizado com sucesso: ID {afazer_id}")
            return db_afazer
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao atualizar afazer: {str(e)}")
            raise

    def deletar_afazer(self, afazer_id: int) -> dict:
        try:
            logger.info(f"Tentando deletar afazer: ID {afazer_id}")
            db_afazer = self.db.query(AfazerDiario).filter(AfazerDiario.id == afazer_id).first()
            if not db_afazer:
                logger.warning(f"Tentativa de deletar afazer inexistente: ID {afazer_id}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Afazer não encontrado"
                )

            self.db.delete(db_afazer)
            self.db.commit()
            logger.info(f"Afazer deletado com sucesso: ID {afazer_id}")
            return {"message": "Afazer deletado com sucesso"}
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao deletar afazer: {str(e)}")   
            raise