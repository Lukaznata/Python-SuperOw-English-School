from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class StatusMensalidade(Base):
    __tablename__ = "status_mensalidade"

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id", ondelete="CASCADE"), nullable=False)
    data = Column(Date, nullable=False)
    status = Column(String(50), nullable=False)  # Ex: "Pago", "Pendente", "Atrasado"
    valor = Column(Float, nullable=False)

    # Relacionamento com Aluno
    aluno = relationship("Aluno", back_populates="mensalidades")