import pytest
from httpx import AsyncClient
from jose import jwt
from starlette.status import HTTP_200_OK
from starlette.status import HTTP_401_UNAUTHORIZED

from app.api.routes.v1.session_route import AUTH_HEADER
from app.core import config
from app.schemas.user import UserDB

credentials = {
    'email': 'test@mail.com',
    'password': 'testpws',
}

user = {
    'username': 'test',
    'name': 'test name',
    'career': 'test career',
    'team': 'team test',
    'profile_photo_path': '',
}

user.update(credentials)
body = {'credentials': dict(credentials)}
credentials.update({'password': 'wrong_password'})
wrong_body = {'credentials': credentials}


@pytest.mark.parametrize(
    'payload, status_code',
    (
        (body, HTTP_200_OK),
        (wrong_body, HTTP_401_UNAUTHORIZED)
    )
)
@pytest.mark.asyncio
async def test_login_user(
        client: AsyncClient,
        payload: dict,
        status_code: int,
        user: UserDB,
) -> None:

    res = await client.post('/v1/session/login', json=payload)
    assert res.status_code == status_code
    if status_code == HTTP_200_OK:
        assert AUTH_HEADER in res.headers

        access_token = res.headers.get(AUTH_HEADER).split()[1]
        token_payload = jwt.decode(
            access_token,
            str(config.SECRET_KEY),
            algorithms=[config.ALGORITHM]
        )

        assert user.username == token_payload.get('sub')
