from typing import Optional

from pydantic import BaseModel as SCBaseModel


class UsuarioSchema(SCBaseModel):
    id: Optional[int]
    nome: Optional[str]
    sobrenome: Optional[str]
    email: str
    senha: str
    admin: Optional[bool]

    class Config:
        orm_mode = True
