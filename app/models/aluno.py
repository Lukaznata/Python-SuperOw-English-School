from sqlalchemy import Column, Integer, String, Date, Boolean, LargeBinary
from sqlalchemy.orm import relationship
from .aula_aluno_association import aula_aluno_association
from .professor_aluno_association import professor_aluno_association
from .base import Base

class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, index=True)
    nome_completo = Column(String(250), nullable=False)
    data_nasc = Column(Date, nullable=False)
    cpf = Column(String(11), unique=True)
    telefone = Column(String(11), unique=True, nullable=False)
    preferencia_pagamento = Column(String(50))
    dia_cobranca = Column(Integer)
    foto_perfil = Column(LargeBinary)
    pais = Column(String(100))
    situacao = Column(Boolean, default=True)

    professores = relationship(
        "Professor",
        secondary=professor_aluno_association,
        back_populates="alunos"
    )
    aulas = relationship(
        "Aula",
        secondary=aula_aluno_association,
        back_populates="alunos"
    )