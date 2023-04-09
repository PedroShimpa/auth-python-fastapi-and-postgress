from typing import Optional

from pydantic import BaseModel as SCBaseModel, EmailStr


class ContatoSchema(SCBaseModel):
    id: Optional[int] = None
    usuario_id:  Optional[int] = None
    nome: str
    email: Optional[EmailStr]
    telefone: Optional[str]

    class Config:
        orm_mode = True
