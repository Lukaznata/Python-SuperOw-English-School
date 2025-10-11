from pydantic import BaseModel
from datetime import date
from typing import Optional

class ProfessorBase(BaseModel):
    id_idioma: int
    nome_completo: str
    data_nasc: date
    cpf: Optional[str] = None
    telefone: Optional[str] = None
    pdf_contrato: Optional[bytes] = None
    mei: Optional[str] = None
    nacionalidade: str
    foto_perfil: Optional[bytes] = None
    situacao: bool = True

class ProfessorCreate(ProfessorBase):
    pass
    

class Professor(ProfessorBase):
    id: int

    class Config:
        from_attributes = True