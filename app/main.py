from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .api import api_router
from .models import Base
from .core.database import engine
from .core.logging import logger
import time
from typing import Callable

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Superow API",
    description="API para gerenciamento de aulas e afazeres diários",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuração do CORS
origins = [
    "http://localhost:3000",      # React, Next.js (desenvolvimento)
    "http://localhost:5173",      # Vite (desenvolvimento)
    "http://localhost:8080",      # Vue.js (desenvolvimento)
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8080",
    # Adicione aqui a URL do seu frontend em produção
    # "https://seu-frontend.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,           # Lista de origens permitidas
    allow_credentials=True,          # Permite envio de cookies/credenciais
    allow_methods=["*"],             # Permite todos os métodos HTTP (GET, POST, PUT, DELETE, etc)
    allow_headers=["*"],             # Permite todos os headers
)


# Middleware para logging de requisições
@app.middleware("http")
async def log_requests(request: Request, call_next: Callable):
    """Middleware para logar todas as requisições HTTP"""
    start_time = time.time()
    
    # Log da requisição
    logger.info(f"Requisição iniciada: {request.method} {request.url.path}")
    logger.debug(f"Headers: {dict(request.headers)}")
    logger.debug(f"Cliente: {request.client.host if request.client else 'Desconhecido'}")
    
    try:
        response = await call_next(request)
        
        # Calcula tempo de processamento
        process_time = time.time() - start_time
        
        # Log da resposta
        logger.info(
            f"Requisição concluída: {request.method} {request.url.path} - "
            f"Status: {response.status_code} - Tempo: {process_time:.3f}s"
        )
        
        # Adiciona header com tempo de processamento
        response.headers["X-Process-Time"] = str(process_time)
        
        return response
    
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(
            f"Erro na requisição: {request.method} {request.url.path} - "
            f"Erro: {str(e)} - Tempo: {process_time:.3f}s"
        )
        logger.error(f"Traceback completo:", exc_info=True)
        
        # Retorna erro 500
        return JSONResponse(
            status_code=500,
            content={"detail": "Erro interno do servidor", "error": str(e)}
        )


# Exception handler global
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handler global para exceções não tratadas"""
    logger.error(f"Exceção não tratada na rota {request.url.path}: {str(exc)}")
    logger.error("Traceback:", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Erro interno do servidor",
            "path": str(request.url.path),
            "method": request.method
        }
    )


logger.info("=" * 80)
logger.info("Iniciando aplicação Superow API")
logger.info(f"Documentação disponível em: /docs")
logger.info(f"CORS configurado para: {origins}")
logger.info("=" * 80)

app.include_router(api_router, prefix="/api/v1")