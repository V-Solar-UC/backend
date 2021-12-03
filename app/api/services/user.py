from datetime import datetime
from datetime import timedelta
from typing import Optional

from fastapi import HTTPException
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_401_UNAUTHORIZED

from app.api.services.base import BaseService
from app.core import config
from app.db.models import User
from app.schemas.user import UserCreate
from app.schemas.user import UserDB
from app.schemas.user import UserInDB
from app.schemas.user import UserLogIn


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

    @classmethod
    async def authenticate_user(
        cls,
        session: AsyncSession,
        credentials: UserLogIn
    ) -> list([str, str, dict]):
        """
        Método para autenticar a un usuario.

        :param credentials: email y password de un usuario.
        :returns: jwt, datos del usuario.
        :raises HTTPException: el password no coincide con su hash.
        :raises HTTPException: el usuario con el email solicitado no existe.
        """

        user = await cls.find_by(session, 'email', credentials.email)

        if not cls.verify_password(credentials.password, user.hashed_password):
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail='Incorrect credentials'
            )
        jwt_expires = timedelta(hours=config.ACCESS_TOKEN_EXPIRE_HOURS)
        jwt_data = {'sub': user.username}
        jwt = cls.create_access_token(jwt_data, jwt_expires)

        return jwt, user

    @classmethod
    async def create_user(
        cls,
        session: AsyncSession,
        user_data: UserCreate
    ) -> UserDB:
        """
        Método para crear un usuario.

        :param user_data: datos del usuario a crear.
        :returns: la instancia del usuario creado.
        """
        username = await cls.default_username(user_data.name, session)
        hashed_password = cls.password_hash(user_data.password)
        user = await cls.create(
            session,
            UserInDB(**user_data.dict(), hashed_password=hashed_password, username=username)
        )
        return user

    @classmethod
    def verify_password(cls, plain_password, hashed_password) -> bool:
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def password_hash(cls, password) -> str:
        return cls.pwd_context.hash(password)

    @classmethod
    async def default_username(cls, name, session) -> str:
        names = name.split(" ")
        username = ""
        for i in range(len(names) - 1):
            username += names[i][0]
        username += names[-1]
        username = username.lower()
        full_username = username
        counter = 0
        while True:
            try:
                users = await cls.find_by(session, 'username', full_username)
                print(users)
            except HTTPException:
                return full_username
            full_username = username + str(counter)
            counter += 1
