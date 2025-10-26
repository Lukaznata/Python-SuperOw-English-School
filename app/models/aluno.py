from sqlalchemy import Column, Integer, String, Date, Boolean, LargeBinary, Text
from sqlalchemy.orm import relationship
from .aula_aluno_association import aula_aluno_association
from .professor_aluno_association import professor_aluno_association
from .base import Base

class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, index=True)
    nome_completo = Column(String(100), nullable=False)
    data_nasc = Column(Date, nullable=False)  
    cpf = Column(String(14), unique=True, nullable=True)
    telefone = Column(String(20), nullable=False)
    pais = Column(String(50), nullable=False)
    preferencia_pagamento = Column(String(50), nullable=False)
    dia_cobranca = Column(Integer, nullable=False)
    foto_perfil = Column(LargeBinary(length=(2**32)-1), nullable=True)  # ~4GB, igual ao professor
    situacao = Column(Boolean, default=True)
    email = Column(String(100), nullable=True)
    observacao = Column(Text, nullable=True)

    # Relationships
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
    mensalidades = relationship('StatusMensalidade', back_populates="aluno", cascade="all, delete-orphan")