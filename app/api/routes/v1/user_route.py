from typing import Any
from typing import List

from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response
from starlette.status import HTTP_200_OK
from starlette.status import HTTP_201_CREATED

from app.api.dependencies.session import get_session
from app.api.services.user import UserService
from app.schemas.user import UserLogIn
from app.schemas.user import UserNew
from app.schemas.user import UserOut


router = APIRouter()


@router.post('/', response_model=UserOut, status_code=HTTP_201_CREATED)
async def create_user(
    new_user: UserNew = Body(..., embed=True),
    session: AsyncSession = Depends(get_session)
) -> Any:

    user = await UserService().create_user(session, new_user)
    return user


@router.post('/login', response_model=UserOut, status_code=HTTP_200_OK)
async def log_in(
    response: Response,
    credentials: UserLogIn = Body(..., embed=True),
    session: AsyncSession = Depends(get_session)
) -> Any:

    jwt, csrf_token, user = await UserService().authenticate_user(session, credentials)

    response.headers.update({'Authorization': f'Bearer {csrf_token}'})
    response.set_cookie(
        key='access_token',
        value=jwt,
        domain='localhost',
        httponly=True
    )
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
    print(users)
    return users


@router.delete('/{id}', response_model=UserOut, status_code=HTTP_200_OK)
async def delete_user(
        id: int,
        session: AsyncSession = Depends(get_session)
) -> Any:
    user = await UserService.find(session, id)
    await UserService.delete(session, user)
    return user
