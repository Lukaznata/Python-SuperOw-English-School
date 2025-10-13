from pydantic import BaseModel, Field, field_serializer, field_validator
from datetime import datetime
from typing import Optional
from decimal import Decimal
from app.core.validators import validar_valor_positivo

class AulaBase(BaseModel):
    professor_id: int
    data_aula: datetime
    idioma: str
    valor_professor: Decimal
    valor_escola: Decimal
    status: bool = True
    repetir_dia: bool = False

    @field_validator('valor_professor')
    @classmethod
    def validar_valor_professor(cls, v):
        """Valida se o valor do professor é positivo"""
        return validar_valor_positivo(v, 'Valor do professor')
    
    @field_validator('valor_escola')
    @classmethod
    def validar_valor_escola(cls, v):
        """Valida se o valor da escola é positivo"""
        return validar_valor_positivo(v, 'Valor da escola')

class AulaCreate(AulaBase):
    pass

class Aula(AulaBase):
    id: int

    @field_serializer('data_aula')
    def serialize_data_aula(self, dt: datetime, _info):
        # Formato: "05/10/2025 14:30"
        return dt.strftime("%d/%m/%Y %H:%M")
    
    class Config:
        from_attributes = True