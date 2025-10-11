from sqlalchemy import Column, Integer, ForeignKey, Table
from .base import Base

aula_aluno_association = Table(
    'aula_aluno',
    Base.metadata,
    Column('aula_id', Integer, ForeignKey('aulas.id'), primary_key=True),
    Column('aluno_id', Integer, ForeignKey('alunos.id'), primary_key=True)
)