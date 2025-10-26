from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class StatusMensalidadeBase(BaseModel):
    aluno_id: int = Field(..., description="ID do aluno")
    data: date = Field(..., description="Data da mensalidade")
    status: str = Field(..., description="Status da mensalidade (Pago, Pendente, Atrasado)")
    valor: float = Field(..., gt=0, description="Valor da mensalidade")

class StatusMensalidadeCreate(StatusMensalidadeBase):
    pass

class StatusMensalidadeUpdate(BaseModel):
    aluno_id: Optional[int] = None
    data: Optional[date] = None
    status: Optional[str] = None
    valor: Optional[float] = Field(None, gt=0)

class StatusMensalidadeResponse(StatusMensalidadeBase):
    id: int

    class Config:
        from_attributes = True

class StatusMensalidadeWithAluno(StatusMensalidadeResponse):
    aluno_nome: Optional[str] = None
    
    class Config:
        from_attributes = True