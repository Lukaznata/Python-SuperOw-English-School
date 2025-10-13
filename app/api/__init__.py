from fastapi import APIRouter
from .routes import administrador, afazer, professor, idioma, aluno, aula, login, carteira, conta_receber, conta_pagar, health

api_router = APIRouter()
api_router.include_router(health.router)  # Healthcheck sem autenticação
api_router.include_router(login.router)
api_router.include_router(administrador.router)
api_router.include_router(afazer.router)
api_router.include_router(professor.router)
api_router.include_router(idioma.router)
api_router.include_router(aluno.router)
api_router.include_router(aula.router)
api_router.include_router(carteira.router)
api_router.include_router(conta_receber.router)
api_router.include_router(conta_pagar.router)