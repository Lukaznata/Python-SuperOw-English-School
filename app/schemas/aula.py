from pydantic import BaseModel, Field, field_serializer
from datetime import datetime
from typing import Optional
from decimal import Decimal

class AulaBase(BaseModel):
    professor_id: int
    data_aula: datetime
    idioma: str
    valor_professor: Decimal
    valor_escola: Decimal
    status: bool = True
    repetir_dia: bool = False

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