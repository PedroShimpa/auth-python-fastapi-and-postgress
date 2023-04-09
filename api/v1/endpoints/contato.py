from typing import List


from fastapi import APIRouter, status, Depends, HTTPException, Response


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.usuario_model import UsuarioModel
from models.contato_model import ContatoModel
from schemas.contato_schema import ContatoSchema
from core.deps import get_session, get_current_user

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ContatoSchema)
async def post_contato(contato: ContatoSchema, usuario_logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    novo_contato = ContatoModel(nome=contato.nome, email=contato.email, usuario_id=usuario_logado.id,
                                telefone=contato.telefone)
    db.add(novo_contato)
    await db.commit()
    return novo_contato


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[ContatoSchema])
async def get_contatos(usuario_logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ContatoModel).filter(ContatoModel.usuario_id == usuario_logado.id)
        result = await session.execute(query)
        contatos: List[ContatoModel] = result.scalars().all()
        return contatos


@router.get('/{contato_id}', status_code=status.HTTP_200_OK, response_model=ContatoSchema)
async def get_contato(contato_id: int,usuario_logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ContatoModel).filter(ContatoModel.id == contato_id).filter(ContatoModel.usuario_id == usuario_logado.id)
        result = await session.execute(query)
        contato = result.unique().scalar_one_or_none()
        if contato:
            return contato
        else:
            raise HTTPException(detail='contato não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)


@router.put('/{contato_id}', status_code=status.HTTP_202_ACCEPTED, response_model=ContatoSchema)
async def update_contato(contato_id: int, contato: ContatoSchema, usuario_logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ContatoModel).filter(ContatoModel.id == contato_id).filter(ContatoModel.usuario_id == usuario_logado.id)
        result = await session.execute(query)
        contato_up = result.unique().scalar_one_or_none()
        if contato_up:
            contato_up.nome = contato.nome
            contato_up.email = contato.email
            contato_up.telefone = contato.telefone
            await session.commit()
            return contato_up
        else:
            raise HTTPException(detail='contato não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)


@router.delete('/{contato_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_contato(contato_id: int, usuario_logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ContatoModel).filter(ContatoModel.id == contato_id).filter(ContatoModel.usuario_id == usuario_logado.id)
        result = await session.execute(query)
        contato_del = result.unique().scalar_one_or_none()
        if contato_del:

            await session.delete(contato_del)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='contato não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)
