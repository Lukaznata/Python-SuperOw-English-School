from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from .base import Base

class Carteira(Base):
    __tablename__ = "carteiras"

    id = Column(Integer, primary_key=True, index=True)
    id_adm = Column(Integer, ForeignKey("administradores.id"), nullable=False, unique=True)

    # Relationship
    administrador = relationship("Administrador", back_populates="carteira")