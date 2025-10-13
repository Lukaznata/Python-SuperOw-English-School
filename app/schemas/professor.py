from pydantic import BaseModel, field_validator
from datetime import date
from typing import Optional
from app.core.validators import validar_cpf, validar_telefone_opcional, validar_mei

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

    @field_validator('cpf')
    @classmethod
    def validar_cpf_professor(cls, v):
        """Valida o CPF do professor"""
        return validar_cpf(v)
    
    @field_validator('telefone')
    @classmethod
    def validar_telefone_professor(cls, v):
        """Valida o telefone do professor (opcional)"""
        return validar_telefone_opcional(v)
    
    @field_validator('mei')
    @classmethod
    def validar_mei_professor(cls, v):
        """Valida o número do MEI (14 dígitos)"""
        return validar_mei(v)

class ProfessorCreate(ProfessorBase):
    pass
    

class Professor(ProfessorBase):
    id: int

    class Config:
        from_attributes = True