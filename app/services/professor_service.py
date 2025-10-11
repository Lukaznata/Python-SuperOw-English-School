from sqlalchemy.orm import Session, joinedload

from app.models import professor
from app.models.idioma import Idioma
from ..models import Professor, Aluno
from ..schemas import ProfessorCreate
from fastapi import HTTPException, status

class ProfessorService:
    def __init__(self, db: Session):
        self.db = db

    def criar_professor(self, professor: ProfessorCreate):
         # Verificar se o idioma existe
        idioma = self.db.query(Idioma).filter(Idioma.id == professor.id_idioma).first()
        if not idioma:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Idioma com id {professor.id_idioma} não encontrado"
            )
        # Criar o professor
        db_professor = Professor(**professor.model_dump())
        self.db.add(db_professor)
        self.db.commit()
        self.db.refresh(db_professor)
        return db_professor

    def listar_professores(self, skip: int = 0, limit: int = 100):
        professores = self.db.query(Professor).offset(skip).limit(limit).all()
        return professores

    def obter_professor(self, professor_id: int):
        professor = self.db.query(Professor).filter(Professor.id == professor_id).first()
        if professor is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Professor não encontrado")
        return professor

    def atualizar_professor(self, professor_id: int, professor: ProfessorCreate):
        db_professor = self.obter_professor(professor_id)
        for key, value in professor.model_dump(exclude_unset=True).items():
            setattr(db_professor, key, value)
        self.db.commit()
        self.db.refresh(db_professor)
        return db_professor

    def deletar_professor(self, professor_id: int):
        professor = self.obter_professor(professor_id)
        self.db.delete(professor)
        self.db.commit()
        return {"message": "Professor deletado com sucesso"}

    def listar_alunos_do_professor(self, professor_id: int):
        professor = (
            self.db.query(Professor)
            .options(joinedload(Professor.alunos))
            .filter(Professor.id == professor_id)
            .first()
        )
        if not professor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Professor não encontrado")
        return professor.alunos
    
    def associar_aluno(self, professor_id: int, aluno_id: int):
        professor = self.obter_professor(professor_id)
        aluno = self.db.query(Aluno).filter(Aluno.id == aluno_id).first()

        if not aluno:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado")
        
        if aluno in professor.alunos:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Aluno já associado ao professor")
        professor.alunos.append(aluno)
        self.db.commit()
        self.db.refresh(professor)
        return {"message": f"Aluno {aluno.nome_completo} associado ao professor {professor.nome_completo} com sucesso"}

    def desassociar_aluno(self, professor_id: int, aluno_id: int):
        professor = self.obter_professor(professor_id)
        aluno = self.db.query(Aluno).filter(Aluno.id == aluno_id).first()

        if not aluno:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado")

        if aluno not in professor.alunos:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Aluno não associado ao professor")

        professor.alunos.remove(aluno)
        self.db.commit()
        self.db.refresh(professor)
        return {"message": f"Aluno {aluno.nome_completo} desassociado do professor {professor.nome_completo} com sucesso"}