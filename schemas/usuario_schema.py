from typing import Optional, List

from pydantic import BaseModel as SCBaseModel, EmailStr


from schemas.contato_schema import ContatoSchema


class UsuarioSchemaBase(SCBaseModel):
    id: Optional[int] = None
    nome: str
    sobrenome: str
    email: EmailStr
    admin: bool = False

    class Config:
        orm_mode = True


class UsuarioSchemaCreate(UsuarioSchemaBase):
    senha: str


class UsuarioSchemaContatos(UsuarioSchemaBase):
    contatos: Optional[List[ContatoSchema]]


class UsuarioSchemaUp(UsuarioSchemaBase):
    nome: Optional[str]
    sobrenome: Optional[str]
    email: Optional[EmailStr]
    senha: Optional[str]
    admin: Optional[bool]
