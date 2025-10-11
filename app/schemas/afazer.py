from pydantic import BaseModel
from datetime import datetime

class AfazerDiarioBase(BaseModel):
    texto: str
    status: bool = False


class AfazerDiarioCreate(AfazerDiarioBase):
    administrador_id: int


class AfazerDiario(AfazerDiarioBase):
    id: int
    data_criacao: datetime
    administrador_id: int

    model_config = {
        "from_attributes": True
    }
