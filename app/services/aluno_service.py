from sqlalchemy.orm import Session, joinedload
from ..models import Aluno, Professor
from ..schemas import AlunoCreate
from fastapi import HTTPException, status
from ..core.logging import logger

class AlunoService:
    def __init__ (self, db: Session):
        self.db = db
        logger.debug("AlunoService inicializado")
        
    def criar_aluno(self, aluno: AlunoCreate):
        logger.debug(f"Criando aluno no banco de dados: {aluno.nome_completo}")
        try:
            db_aluno = Aluno(**aluno.model_dump())
            self.db.add(db_aluno)
            self.db.commit()
            self.db.refresh(db_aluno)
            logger.info(f"Aluno criado no banco - ID: {db_aluno.id}, Nome: {db_aluno.nome_completo}")
            return db_aluno
        except Exception as e:
            logger.error(f"Erro ao criar aluno no banco: {str(e)}")
            self.db.rollback()
            raise
    
    def listar_alunos(self, skip: int = 0, limit: int = 100):
        alunos = self.db.query(Aluno).offset(skip).limit(limit).all()
        return alunos
    
    def contar_alunos(self) -> int:
        """Conta o total de alunos"""
        return self.db.query(Aluno).count()
    
    def obter_aluno(self, aluno_id: int):
        logger.debug(f"Buscando aluno ID: {aluno_id}")
        aluno = self.db.query(Aluno).filter(Aluno.id == aluno_id).first()
        if aluno is None:
            logger.warning(f"Aluno ID: {aluno_id} não encontrado")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado")
        logger.debug(f"Aluno encontrado: {aluno.nome_completo}")
        return aluno
    
    def atualizar_aluno(self, aluno_id: int, aluno: AlunoCreate):
        db_aluno = self.obter_aluno(aluno_id)
        for key, value in aluno.model_dump(exclude_unset=True).items():
            setattr(db_aluno, key, value)
        self.db.commit()
        self.db.refresh(db_aluno)
        return db_aluno
    
    def deletar_aluno(self, aluno_id: int):
        aluno = self.obter_aluno(aluno_id)
        self.db.delete(aluno)
        self.db.commit()
        return {"message": "Aluno deletado com sucesso"}

    def listar_professores_do_aluno(self, aluno_id: int):
        aluno = (
            self.db.query(Aluno)
            .options(joinedload(Aluno.professores))
            .filter(Aluno.id == aluno_id)
            .first()
        )
        if not aluno:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado")
        return aluno.professores
    
    def associar_professor(self, aluno_id: int, professor_id: int):
        aluno = self.obter_aluno(aluno_id)
        professor = self.db.query(Professor).filter(Professor.id == professor_id).first()
        
        if not professor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Professor não encontrado")
        
        if professor in aluno.professores:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Professor já está associado a este aluno")
        
        aluno.professores.append(professor)
        self.db.commit()
        return {"message": f"Professor {professor.nome_completo} associado ao aluno {aluno.nome_completo} com sucesso"}

    def desassociar_professor(self, aluno_id: int, professor_id: int):
        aluno = self.obter_aluno(aluno_id)
        professor = self.db.query(Professor).filter(Professor.id == professor_id).first()

        if not professor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Professor não encontrado")

        if professor not in aluno.professores:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Professor não está associado a este aluno")

        aluno.professores.remove(professor)
        self.db.commit()
        return {"message": f"Professor {professor.nome_completo} desassociado do aluno {aluno.nome_completo} com sucesso"}