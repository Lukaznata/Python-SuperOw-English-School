from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .base import Base

class AfazerDiario(Base):
    __tablename__ = "afazeres_diarios"

    id = Column(Integer, primary_key=True, index=True)
    texto = Column(Text, nullable=False)
    status = Column(Boolean, default=False)
    data_criacao = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    administrador_id = Column(Integer, ForeignKey("administradores.id"))
    
    administrador = relationship("Administrador", back_populates="afazeres")