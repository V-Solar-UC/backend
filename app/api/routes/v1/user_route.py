from typing import Any
from typing import List

from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK
from starlette.status import HTTP_201_CREATED

from app.api.dependencies.session import get_session
from app.api.services.user import UserService
from app.schemas.user import UserCreate
from app.schemas.user import UserOut


router = APIRouter()


@router.post('/', response_model=UserOut, status_code=HTTP_201_CREATED)
async def create_user(
    new_user: UserCreate = Body(..., embed=True),
    session: AsyncSession = Depends(get_session)
) -> Any:

    user = await UserService.create_user(session, new_user)
    return user


@router.get('/{id}', response_model=UserOut, status_code=HTTP_200_OK)
async def find_user(
        id: int,
        session: AsyncSession = Depends(get_session)
) -> Any:
    user = await UserService.find(session, id)
    return user


@router.get('/', response_model=List[UserOut], status_code=HTTP_200_OK)
async def get_all_users(
        session: AsyncSession = Depends(get_session)
) -> Any:
    users = await UserService.find_all(session)
    return users


@router.delete('/{id}', response_model=UserOut, status_code=HTTP_200_OK)
async def delete_user(
        id: int,
        session: AsyncSession = Depends(get_session)
) -> Any:
    user = await UserService.find(session, id)
    await UserService.delete(session, user)
    return user
