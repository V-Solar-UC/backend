from typing import Any

from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response
from starlette.status import HTTP_200_OK

from app.api.dependencies.session import get_session
from app.api.services.user import UserService
from app.schemas.user import UserDB as UserOut
from app.schemas.user import UserLogIn


AUTH_HEADER = 'Authorization'

router = APIRouter()


@router.post('/login', response_model=UserOut, status_code=HTTP_200_OK)
async def log_in(
    response: Response,
    credentials: UserLogIn = Body(..., embed=True),
    session: AsyncSession = Depends(get_session)
) -> Any:

    jwt, user = await UserService.authenticate_user(session, credentials)
    response.headers.update({AUTH_HEADER: f'Bearer {jwt}'})
    return user
