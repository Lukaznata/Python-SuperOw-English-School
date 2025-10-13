from sqlalchemy import Column, String, Integer, Numeric, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship
from .base import Base

class ContaReceber(Base):
    __tablename__ = "contas_receber"

    id = Column(Integer, primary_key=True, index=True)
    id_adm = Column(Integer, ForeignKey("administradores.id"), nullable=False)
    nome = Column(String(250), nullable=False)
    valor = Column(Numeric(10, 2), nullable=False)
    data_recebimento = Column(Date, nullable=False, index=True)
    status = Column(Boolean, default=False, index=True)

    # Relationship
    administrador = relationship("Administrador", back_populates="contas_receber")