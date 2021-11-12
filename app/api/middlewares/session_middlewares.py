from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose import JWTError
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.api.dependencies.session import get_session
from app.api.services.user import UserService
from app.core.config import ALGORITHM
from app.core.config import SECRET_KEY
from app.schemas.user import UserDB

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='v1/session/login')


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
) -> UserDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(token, str(SECRET_KEY), algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await UserService.find_by(session, 'username', username)

    if user is None:
        raise credentials_exception
    return user
