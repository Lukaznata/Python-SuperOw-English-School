from sqlalchemy.orm import Session, joinedload
from ..models import Aula, Aluno, Professor
from ..schemas import AulaCreate
from fastapi import HTTPException, status

class AulaService:
    def __init__(self, db: Session):
        self.db = db

    def criar_aula(self, aula: AulaCreate):
        # Verificar se professor existe
        professor = self.db.query(Professor).filter(Professor.id == aula.professor_id).first()
        if not professor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Professor com id {aula.professor_id} não encontrado"
            )
        
        db_aula = Aula(**aula.model_dump())
        self.db.add(db_aula)
        self.db.commit()
        self.db.refresh(db_aula)
        return db_aula

    def listar_aulas(self, skip: int = 0, limit: int = 100):
        aulas = self.db.query(Aula).offset(skip).limit(limit).all()
        return aulas

    def obter_aula(self, aula_id: int):
        aula = self.db.query(Aula).filter(Aula.id == aula_id).first()
        if aula is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aula não encontrada")
        return aula

    def listar_alunos_da_aula(self, aula_id: int):
        aula = (
            self.db.query(Aula)
            .options(joinedload(Aula.alunos))
            .filter(Aula.id == aula_id)
            .first()
        )
        if not aula:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aula não encontrada")
        return aula.alunos

    def associar_aluno(self, aula_id: int, aluno_id: int):
        aula = self.obter_aula(aula_id)
        aluno = self.db.query(Aluno).filter(Aluno.id == aluno_id).first()
        
        if not aluno:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado")
        
        if aluno in aula.alunos:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Aluno já está associado a esta aula")
        
        aula.alunos.append(aluno)
        self.db.commit()
        return {"message": f"Aluno {aluno.nome_completo} associado à aula com sucesso"}

    def desassociar_aluno(self, aula_id: int, aluno_id: int):
        aula = self.obter_aula(aula_id)
        aluno = self.db.query(Aluno).filter(Aluno.id == aluno_id).first()
        
        if not aluno:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado")
        
        if aluno not in aula.alunos:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Aluno não está associado a esta aula")
        
        aula.alunos.remove(aluno)
        self.db.commit()
        return {"message": f"Aluno {aluno.nome_completo} desassociado da aula com sucesso"}

    def atualizar_aula(self, aula_id: int, aula: AulaCreate):
        # Verificar se professor existe ao atualizar
        professor = self.db.query(Professor).filter(Professor.id == aula.professor_id).first()
        if not professor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Professor com id {aula.professor_id} não encontrado"
            )
        
        db_aula = self.obter_aula(aula_id)
        for key, value in aula.model_dump(exclude_unset=True).items():
            setattr(db_aula, key, value)
        self.db.commit()
        self.db.refresh(db_aula)
        return db_aula

    def deletar_aula(self, aula_id: int):
        aula = self.obter_aula(aula_id)
        self.db.delete(aula)
        self.db.commit()
        return {"message": "Aula deletada com sucesso"}