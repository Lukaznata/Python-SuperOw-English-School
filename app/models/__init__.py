from .administrador import Administrador
from .afazer import AfazerDiario
from .professor import Professor
from .idioma import Idioma
from .base import Base
from .aluno import Aluno
from .aula import Aula
from .professor_aluno_association import professor_aluno_association
from .aula_aluno_association import aula_aluno_association

__all__ = ["Administrador", "AfazerDiario", "Professor", "Idioma", "Base", "Aluno", "professor_aluno_association", "aula_aluno_association", "Aula"]