from pydantic import BaseModel

class IdiomaBase(BaseModel):
    nome_idioma: str

class IdiomaCreate(IdiomaBase):
    pass

class Idioma(IdiomaBase):
    id: int

    class Config:
        from_attributes = True