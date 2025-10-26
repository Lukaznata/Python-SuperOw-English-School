from sqlalchemy import Column, Integer, String, Date, Boolean, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship
from .professor_aluno_association import professor_aluno_association
from .base import Base

class Professor(Base):
    __tablename__ = "professores"

    id = Column(Integer, primary_key=True, index=True)
    id_idioma = Column(Integer, ForeignKey("idiomas.id"), nullable=False)
    nome_completo = Column(String(250), nullable=False)
    data_nasc = Column(Date, nullable=False)
    cpf = Column(String(11), unique=True)
    telefone = Column(String(11), unique=True, nullable=False)
    pdf_contrato = Column(LargeBinary(length=(2**32)-1))  # ~4GB
    mei = Column(String(250))
    foto_perfil = Column(LargeBinary(length=(2**32)-1))  # ~4GB
    nacionalidade = Column(String(100), nullable=False)
    situacao = Column(Boolean, default=True)
    pix = Column(String(250))

    alunos = relationship(
        "Aluno",
        secondary=professor_aluno_association,
        back_populates="professores"
    )
    aulas = relationship("Aula", back_populates="professor")
