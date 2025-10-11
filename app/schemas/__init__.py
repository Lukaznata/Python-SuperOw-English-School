from .afazer import AfazerDiario, AfazerDiarioBase, AfazerDiarioCreate
from .administrador import Administrador, AdministradorBase, AdministradorCreate
from .token import Token, TokenData
from .professor import Professor, ProfessorBase, ProfessorCreate
from .aluno import Aluno, AlunoBase, AlunoCreate
from .aula import Aula, AulaCreate

__all__ = [
    "Professor",
    "ProfessorBase",
    "ProfessorCreate",
    "AfazerDiario",
    "AfazerDiarioBase",
    "AfazerDiarioCreate",
    "Administrador",
    "AdministradorBase",
    "AdministradorCreate",
    "Token",
    "TokenData",
    "Aluno",
    "AlunoBase",
    "AlunoCreate",
    "Aula",
    "AulaCreate"
]