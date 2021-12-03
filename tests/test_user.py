import copy

import pytest
from httpx import AsyncClient
from starlette.status import HTTP_201_CREATED
from starlette.status import HTTP_409_CONFLICT


user = {
    'name': 'test name 2',
    'career': 'test career',
    'team': 'team test',
    'profile_photo_path': '',
    'email': 'test_2@mail.com',
    'password': 'testpws',
}

user_2 = {
    'name': 'test name 3',
    'career': 'test career',
    'team': 'team test',
    'profile_photo_path': '',
    'email': 'test_2@mail.com',
    'password': 'testpws',
}


body = {'new_user': user}

body_2 = {'new_user': user_2}


@pytest.mark.parametrize(
    'payload, status_code',
    (
        (body, HTTP_201_CREATED),
        (body, HTTP_409_CONFLICT),
        (body_2, HTTP_409_CONFLICT)
    )
)
@pytest.mark.asyncio
async def test_create_user(
        client: AsyncClient,
        payload: dict,
        status_code: int
) -> None:
    res = await client.post('/v1/user', json=payload)
    assert res.status_code == status_code
    if status_code == HTTP_201_CREATED:
        copy_user = copy.copy(user)
        copy_user['id'] = res.json()['id']
        copy_user['username'] = res.json()['username']
        del copy_user['password']
        assert res.json() == copy_user
