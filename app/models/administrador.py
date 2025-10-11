from sqlalchemy import Column, Integer,String, Text
from sqlalchemy.orm import relationship
from .base import Base

class Administrador(Base):
    __tablename__ = "administradores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    senha_hash = Column(Text, nullable=False)
    
    afazeres = relationship("AfazerDiario", back_populates="administrador")