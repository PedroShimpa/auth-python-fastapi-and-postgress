from typing import List, Optional, Any


from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from models.usuario_model import UsuarioModel
from schemas.usuario_schema import UsuarioSchemaBase, UsuarioSchemaContatos, UsuarioSchemaCreate, UsuarioSchemaUp
from core.deps import get_session, get_current_user
from core.security import gerar_hash_senha
from core.auth import autenticar, criar_token_acesso

router = APIRouter()


@router.post('/login', response_model=UsuarioSchemaBase)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),  db: AsyncSession = Depends(get_session)):
    usuario = await autenticar(email=form_data.username, senha=form_data.password, db=db)

    if not usuario:
        raise HTTPException(detail='Dados de acesso inválidos',
                            status_code=status.HTTP_400_BAD_REQUEST)

    return JSONResponse(content={"access_token": criar_token_acesso(sub=usuario.id), "token_type": "bearer"}, status_code=status.HTTP_200_OK)


@router.get('/logado', response_model=UsuarioSchemaBase)
def get_logado(usuario_logado: UsuarioModel = Depends(get_current_user)):
    return usuario_logado


@router.post('/registrar', response_model=UsuarioSchemaBase, status_code=status.HTTP_201_CREATED)
async def post_usuario(usuario: UsuarioSchemaCreate, db: AsyncSession = Depends(get_session)):
    novo_usuario: UsuarioModel = UsuarioModel(nome=usuario.nome, sobrenome=usuario.sobrenome,
                                              email=usuario.email, senha=gerar_hash_senha(usuario.senha), admin=usuario.admin)
    async with db as session:
        try:
            session.add(novo_usuario)
            await session.commit()
            return novo_usuario
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail='Já existe um usuário com este email cadastrado.')


@router.get('/', response_model=List[UsuarioSchemaBase], status_code=status.HTTP_200_OK)
async def get_usuarios(usuario_logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel)
        result = await session.execute(query)
        usuarios: List[UsuarioModel] = result.scalars().all()
        return usuarios


@router.get('/{usuario_id}', status_code=status.HTTP_200_OK, response_model=UsuarioSchemaContatos)
async def get_usuario(usuario_id: int, usuario_logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario: UsuarioSchemaContatos = result.unique().scalar_one_or_none()
        if usuario:
            return usuario
        else:
            raise HTTPException(detail='usuario não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)


@router.put('/{usuario_id}', status_code=status.HTTP_202_ACCEPTED, response_model=UsuarioSchemaBase)
async def update_contato(usuario_id: int, usuario: UsuarioSchemaUp, usuario_logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_up: UsuarioSchemaBase = result.unique().scalar_one_or_none()
        if usuario_up:
            usuario_up.nome = usuario.nome
            usuario_up.sobrenome = usuario.sobrenome
            usuario_up.email = usuario.email
            usuario_up.senha = gerar_hash_senha(usuario.senha)
            usuario_up.admin = usuario.admin

            await session.commit()
            return usuario_up
        else:
            raise HTTPException(detail='usuario não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)


@router.delete('/{usuario_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(usuario_id: int, usuario_logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_del = result.unique().scalar_one_or_none()
        if usuario_del:
            await session.delete(usuario_del)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='contato não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)
