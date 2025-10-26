from pydantic import BaseModel, Field, field_validator
from datetime import date
from typing import Optional
from app.core.validators import validar_cpf, validar_telefone
import base64

class ProfessorBase(BaseModel):
    id_idioma: int
    nome_completo: str
    data_nasc: date
    cpf: Optional[str] = None
    telefone: str
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
        """Valida o telefone do professor"""
        return validar_telefone(v)

class ProfessorCreate(ProfessorBase):
    pass

class Professor(ProfessorBase):
    id: int
    cpf: Optional[str] = None  # ⬅️ Permite retornar None
    mei: Optional[str] = None  # ⬅️ Permite retornar None
    foto_perfil: str
    pdf_contrato: str

    @field_validator('foto_perfil', mode='before')
    @classmethod
    def encode_foto_perfil(cls, v):
        """Converte bytes para base64"""
        if isinstance(v, bytes):
            return base64.b64encode(v).decode('utf-8')
        return v or ""  # ⬅️ Retorna string vazia se for None

    @field_validator('pdf_contrato', mode='before')
    @classmethod
    def encode_pdf_contrato(cls, v):
        """Converte bytes para base64"""
        if isinstance(v, bytes):
            return base64.b64encode(v).decode('utf-8')
        return v or ""  # ⬅️ Retorna string vazia se for None

    class Config:
        from_attributes = True