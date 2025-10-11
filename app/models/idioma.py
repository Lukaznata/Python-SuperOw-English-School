from sqlalchemy import Column, Integer, String
from .base import Base

class Idioma(Base):
    __tablename__ = "idiomas"

    id = Column(Integer, primary_key=True, index=True)
    nome_idioma = Column(String(40), nullable=False, unique=True)