from pydantic import BaseModel, Field, field_validator
from datetime import date
from typing import Optional
from app.core.validators import validar_cpf, validar_telefone, validar_dia_cobranca

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
    
    @field_validator('dia_cobranca')
    @classmethod
    def validar_dia_cobranca_aluno(cls, v):
        """Valida o dia de cobrança (1-31)"""
        return validar_dia_cobranca(v)

class AlunoCreate(AlunoBase):
    pass

class Aluno(AlunoBase):
    id: int

    class Config:
        from_attributes = True