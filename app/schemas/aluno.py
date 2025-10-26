from pydantic import BaseModel, Field, field_validator
from datetime import date
from typing import Optional
from app.core.validators import validar_cpf, validar_telefone
import base64

class AlunoBase(BaseModel):
    nome_completo: str = Field(..., min_length=1, max_length=100)
    data_nasc: date
    cpf: Optional[str] = None
    telefone: str
    pais: str
    preferencia_pagamento: str
    dia_cobranca: int = Field(..., ge=1, le=31)
    foto_perfil: Optional[bytes] = None
    situacao: bool = True
    email: Optional[str] = None
    observacao: Optional[str] = None

    @field_validator('cpf')
    @classmethod
    def validar_cpf_aluno(cls, v):
        """Valida o CPF do aluno"""
        return validar_cpf(v)
    
    @field_validator('telefone')
    @classmethod
    def validar_telefone_aluno(cls, v):
        """Valida o telefone do aluno"""
        return validar_telefone(v)

class AlunoCreate(AlunoBase):
    pass

class Aluno(AlunoBase):
    id: int
    cpf: Optional[str] = None  # ⬅️ Permite retornar None
    email: Optional[str] = None  # ⬅️ Permite retornar None
    observacao: Optional[str] = None  # ⬅️ Permite retornar None
    foto_perfil: str

    @field_validator('foto_perfil', mode='before')
    @classmethod
    def encode_foto_perfil(cls, v):
        """Converte bytes para base64"""
        if isinstance(v, bytes):
            return base64.b64encode(v).decode('utf-8')
        return v or ""  # ⬅️ Retorna string vazia se for None

    class Config:
        from_attributes = True

class AlunoWithProfessores(Aluno):
    professores: list[dict] = []

    class Config:
        from_attributes = True