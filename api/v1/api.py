from fastapi import APIRouter

from api.v1.endpoints import contato, usuario

api_router = APIRouter()
api_router.include_router(
    contato.router, prefix='/contatos', tags=["contatos"])

api_router.include_router(
    usuario.router, prefix='/usuarios', tags=["usuarios"])