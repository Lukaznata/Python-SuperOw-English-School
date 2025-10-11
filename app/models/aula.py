from sqlalchemy import Column, Integer, String, DateTime, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .aula_aluno_association import aula_aluno_association
from .base import Base

class Aula(Base):
    __tablename__ = "aulas"

    id = Column(Integer, primary_key=True, index=True)
    professor_id = Column(Integer, ForeignKey("professores.id"), nullable=False)
    data_aula = Column(DateTime, nullable=False)
    idioma = Column(String(40), nullable=False)
    valor_professor = Column(Numeric(4, 2), nullable=False)
    valor_escola = Column(Numeric(4, 2), nullable=False)
    status = Column(Boolean, default=True)
    repetir_dia = Column(Boolean, default=False)

    professor = relationship("Professor", back_populates="aulas")
    alunos = relationship(
        "Aluno",
        secondary=aula_aluno_association,
        back_populates="aulas"
    )