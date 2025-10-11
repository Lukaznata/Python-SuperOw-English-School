from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class AlunoBase(BaseModel):
    nome_completo: str
    data_nasc: date
    cpf: Optional[str] = None
    telefone: str
    preferencia_pagamento: Optional[str] = None
    dia_cobranca: Optional[int] = None
    foto_perfil: Optional[bytes] = None
    pais: Optional[str] = None
    situacao: bool = True

class AlunoCreate(AlunoBase):
    pass

class Aluno(AlunoBase):
    id: int

    class Config:
        from_attributes = True