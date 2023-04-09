from typing import Optional

from pydantic import BaseModel as SCBaseModel


class ContatoSchema(SCBaseModel):
    id: Optional[int]
    usuario_id: int
    nome: str
    email: Optional[str]
    telefone: Optional[str]
    telefone: Optional[bool]

    class Config:
        orm_mode = True
