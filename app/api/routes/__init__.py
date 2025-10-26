from .administrador import router as administrador_router
from .afazer import router as afazer_router
from .aluno import router as aluno_router
from .aula import router as aula_router
from .carteira import router as carteira_router
from .conta_pagar import router as conta_pagar_router
from .conta_receber import router as conta_receber_router
from .health import router as health_router
from .idioma import router as idioma_router
from .login import router as login_router
from .professor import router as professor_router
from .status_mensalidade import router as status_mensalidade_router

__all__ = [
    "administrador_router",
    "afazer_router",
    "aluno_router",
    "aula_router",
    "carteira_router",
    "conta_pagar_router",
    "conta_receber_router",
    "health_router",
    "idioma_router",
    "login_router",
    "professor_router",
    "status_mensalidade_router",
]