from pydantic import BaseModel, field_validator
from datetime import date
from decimal import Decimal
from app.core.validators import validar_valor_positivo

class ContaPagarBase(BaseModel):
    nome: str
    valor: Decimal
    data_pagamento: date
    status: bool = False

    @field_validator('valor')
    @classmethod
    def validar_valor_conta(cls, v):
        """Valida se o valor é positivo"""
        return validar_valor_positivo(v, 'Valor da conta a pagar')

class ContaPagarCreate(ContaPagarBase):
    pass

class ContaPagarUpdate(BaseModel):
    nome: str | None = None
    valor: Decimal | None = None
    data_pagamento: date | None = None
    status: bool | None = None

class ContaPagar(ContaPagarBase):
    id: int
    id_adm: int

    class Config:
        from_attributes = True