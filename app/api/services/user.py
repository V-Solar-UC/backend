from datetime import datetime
from datetime import timedelta
from secrets import token_hex
from typing import Optional

from fastapi import HTTPException
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_400_BAD_REQUEST
from starlette.status import HTTP_401_UNAUTHORIZED

from app.api.services.base import BaseService
from app.core import config
from app.db.models import User
from app.schemas.user import UserInDB
from app.schemas.user import UserLogIn
from app.schemas.user import UserNew


class UserService(BaseService):
    model = User
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    @staticmethod
    def create_access_token(
        data: dict,
        expires_delta: Optional[timedelta] = timedelta(hours=15)
    ) -> str:
        """
        Método para crear un JWT.

        :param data: datos que se guardarán en el payload del JWT.
        :param expires_delta: el tiempo en el que expirará el JWT.
        :returns: JWT.
        """

        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({'exp': expire})

        return jwt.encode(claims=to_encode,
                          key=str(config.SECRET_KEY),
                          algorithm=config.ALGORITHM)

    async def authenticate_user(self,
                                session: AsyncSession,
                                credentials: UserLogIn
                                ) -> list([str, str, dict]):
        """
        Método para autenticar a un usuario.

        :param credentials: email y credenciales de un usuario.
        :returns: jwt, csrf_token y datos del usuario.
        :raises HTTPException: el password no coincide con su hash.
        :raises HTTPException: el usuario con el email solicitado no existe.
        """

        user = await self.find_by_email(session, credentials.email)

        if not self.verify_password(credentials.password, user.hashed_password):
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail='Incorrect credentials'
            )

        csrf_token = token_hex(16)
        jwt_expires = timedelta(hours=config.ACCESS_TOKEN_EXPIRE_HOURS)
        jwt_data = {'sub': user.username, 'csrf': csrf_token}
        jwt = self.create_access_token(jwt_data, jwt_expires)

        return jwt, csrf_token, user

    async def create_user(self, session: AsyncSession, user_data: UserNew):
        """
        Método para crear un usuario.

        :param user_data: datos del usuario a crear.
        :returns: la instancia del usuario creado.
        """
        hashed_password = self.get_password_hash(user_data.password)
        user = await self.create(
            session,
            UserInDB(**user_data.dict(), hashed_password=hashed_password)
        )
        return user

    async def find_by_email(self, session: AsyncSession, email: str):
        """
        Método para poder encontrar a un usuario a partir de su email

        :param email: email del usuario.
        :returns: instancia del usuario que coincide con el email.
        :raises HTTPException: el email no coincide con ningún usuario.
        """
        query = select(self.model).where(self.model.email == email)
        result = await session.execute(query)
        instance = result.scalars().first()
        if not instance:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail='User not found'
            )
        return instance

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)
