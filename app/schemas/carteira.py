from pydantic import BaseModel, computed_field, field_validator
from decimal import Decimal

class CarteiraBase(BaseModel):
    id_adm: int

class CarteiraCreate(BaseModel):
    pass

class CarteiraUpdate(BaseModel):
    saldo_atual: Decimal

    @field_validator('saldo_atual')
    @classmethod
    def validar_saldo(cls, v):
        """Valida se o saldo é um valor numérico válido"""
        # Permite valores negativos para saldo (pode estar no vermelho)
        if v is None:
            raise ValueError('Saldo atual é obrigatório')
        return v

class Carteira(CarteiraBase):
    id: int
    id_adm: int
    saldo_atual: Decimal # Será calculado automaticamente

    class Config:
        from_attributes = True