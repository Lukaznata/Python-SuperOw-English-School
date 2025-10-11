from fastapi import APIRouter
from .routes import administrador, afazer, professor, idioma, aluno, aula, login

api_router = APIRouter()
api_router.include_router(login.router)  # Rota de login (sem autenticação)
api_router.include_router(administrador.router)
api_router.include_router(afazer.router)
api_router.include_router(professor.router)
api_router.include_router(idioma.router)
api_router.include_router(aluno.router)
api_router.include_router(aula.router)