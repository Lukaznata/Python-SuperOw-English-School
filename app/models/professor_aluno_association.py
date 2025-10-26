from sqlalchemy import Table, Column, Integer, ForeignKey
from .base import Base

professor_aluno_association = Table(
    'professor_aluno', Base.metadata,
    Column('professor_id', Integer, ForeignKey('professores.id'), primary_key=True),
    Column('aluno_id', Integer, ForeignKey('alunos.id'), primary_key=True)
)