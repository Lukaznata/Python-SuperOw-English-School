from fastapi import FastAPI
from .api import api_router
from .models import Base
from .core.database import engine
from .core.logging import logger

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Superow API",
    description="API para gerenciamento de aulas e afazeres diários",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

logger.info("Iniciando aplicação Superow API")
app.include_router(api_router, prefix="/api/v1")