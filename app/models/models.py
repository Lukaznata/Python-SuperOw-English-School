from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class Administrador(Base):
    __tablename__ = "administradores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    senha_hash = Column(String(255), nullable=False)
    afazeres = relationship("AfazerDiario", back_populates="administrador")


class AfazerDiario(Base):
    __tablename__ = "afazeres_diarios"

    id = Column(Integer, primary_key=True, index=True)
    texto = Column(String(500), nullable=False)
    status = Column(Boolean, default=False)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    administrador_id = Column(Integer, ForeignKey("administradores.id"))
    
    administrador = relationship("Administrador", back_populates="afazeres")