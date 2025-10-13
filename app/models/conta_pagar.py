from sqlalchemy import Column, Integer, String, Numeric, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class ContaPagar(Base):
    __tablename__ = "contas_pagar"

    id = Column(Integer, primary_key=True, index=True)
    id_adm = Column(Integer, ForeignKey("administradores.id"), nullable=False)
    nome = Column(String(250), nullable=False)
    valor = Column(Numeric(10, 2), nullable=False)
    data_pagamento = Column(Date, nullable=False)
    status = Column(Boolean, default=False)  # False = pendente, True = pago

    # Relationship
    administrador = relationship("Administrador", back_populates="contas_pagar")