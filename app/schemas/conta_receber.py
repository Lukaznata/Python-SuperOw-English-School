from pydantic import BaseModel, field_validator
from datetime import date
from decimal import Decimal
from app.core.validators import validar_valor_positivo

class ContaReceberBase(BaseModel):
    nome: str
    valor: Decimal
    data_recebimento: date
    status: bool = False

    @field_validator('valor')
    @classmethod
    def validar_valor(cls, v):
        """Valida se o valor é positivo"""
        return validar_valor_positivo(v, 'Valor da conta a receber')

class ContaReceberCreate(ContaReceberBase):
    pass

class ContaReceberUpdate(BaseModel):
    nome: str | None = None
    valor: Decimal | None = None
    data_recebimento: date | None = None
    status: bool | None = None

class ContaReceber(ContaReceberBase):
    id: int
    id_adm: int

    class Config:
        from_attributes = True