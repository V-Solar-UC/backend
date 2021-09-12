from typing import List
from typing import Type
from typing import TypeVar

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND
from starlette.status import HTTP_409_CONFLICT
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from app.db.models import Base

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)


class BaseService:

    model: Type[ModelType] = None

    """
    TODO: Definir un método find_by() en donde le pases el atributo
          y el valor deseado, y luego te retorne la instancia.
    """

    @classmethod
    async def find(
            cls,
            session: AsyncSession,
            id: int
    ) -> Type[ModelType]:
        q = select(cls.model).where(cls.model.id == id)
        result = await session.execute(q)
        instance = result.scalars().first()
        if not instance:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail='object not found'
            )
        return instance

    @classmethod
    async def find_all(
            cls,
            session: AsyncSession
    ) -> List[Type[ModelType]]:
        q = select(cls.model)
        result = await session.execute(q)
        return result.scalars().all()

    @classmethod
    async def create(
            cls,
            session: AsyncSession,
            obj_in: Type[CreateSchemaType]
    ) -> Type[ModelType]:
        try:
            new_obj = cls.model(**obj_in.dict())
            session.add(new_obj)
            await session.commit()
            return new_obj
        except IntegrityError:
            raise HTTPException(status_code=HTTP_409_CONFLICT,
                                detail='object exists')

    @classmethod
    async def delete(
            cls,
            session: AsyncSession,
            obj: Type[ModelType]
    ) -> None:
        try:
            await session.delete(obj)
            await session.commit()
        except SQLAlchemyError:
            raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY)
