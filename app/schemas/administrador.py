from pydantic import BaseModel, field_validator
from typing import List
from .afazer import AfazerDiario


class AdministradorBase(BaseModel):
    nome: str


class AdministradorCreate(AdministradorBase):
    senha: str

    @field_validator("senha")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError('senha deve ter pelo menos 6 caracteres')
        if len(v.encode('utf-8')) > 72:
            raise ValueError('senha não pode ter mais que 72 bytes')
        return v


class Administrador(AdministradorBase):
    id: int
    afazeres: List[AfazerDiario] = []

    model_config = {
        "from_attributes": True
    }

class AdministradorLogin(BaseModel):
    nome: str
    senha: str