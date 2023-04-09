from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.configs import settings

class ContatoModel(settings.DBBaseModel):
    __tablename__ = 'contatos'
    
    id= Column(Integer,primary_key=True, autoincrement=True)
    nome = Column(String(256))
    email = Column(String(256), nullable=True)
    telefone = Column(String(256), nullable=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    criador = relationship("UsuarioModel", back_populates='contatos', lazy='joined')