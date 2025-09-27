from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class AfazerDiarioBase(BaseModel):
    texto: str
    status: bool = False


class AfazerDiarioCreate(AfazerDiarioBase):
    pass


class AfazerDiario(AfazerDiarioBase):
    id: int
    data_criacao: datetime
    administrador_id: int

    class Config:
        orm_mode = True


class AdministradorBase(BaseModel):
    nome: str


class AdministradorCreate(AdministradorBase):
    senha: str


class Administrador(AdministradorBase):
    id: int
    afazeres: List[AfazerDiario] = []

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None