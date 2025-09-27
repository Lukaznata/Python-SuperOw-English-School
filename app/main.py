from fastapi import FastAPI
from .api import endpoints
from .models import models
from .core.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Superow API")

app.include_router(endpoints.router, prefix="/api/v1")