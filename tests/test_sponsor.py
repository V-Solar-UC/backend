import pytest
from httpx import AsyncClient
from starlette.status import HTTP_200_OK
from starlette.status import HTTP_201_CREATED
from starlette.status import HTTP_404_NOT_FOUND
from starlette.status import HTTP_409_CONFLICT

sponsor = {
    'name': 'sponsor',
    'logo_path': 'path'
}

body = {
    'new_sponsor': sponsor
}


@pytest.mark.parametrize(
    'payload, status_code',
    (
        (body, HTTP_201_CREATED),
        (body, HTTP_409_CONFLICT)
    )
)
@pytest.mark.asyncio
async def test_create_sponsor(
        client: AsyncClient,
        payload: dict,
        status_code: int
) -> None:
    res = await client.post('/v1/sponsor', json=payload)
    assert res.status_code == status_code
    if status_code == HTTP_201_CREATED:
        sponsor['id'] = res.json()['id']
        assert res.json() == sponsor


@pytest.mark.parametrize(
    'id, status_code',
    (
        (1, HTTP_200_OK),
        (122312, HTTP_404_NOT_FOUND)
    )
)
@pytest.mark.asyncio
async def test_get_sponsor(
        client: AsyncClient,
        id: int,
        status_code: int
) -> None:
    res = await client.get(f'/v1/sponsor/{id}')
    assert res.status_code == status_code
    if status_code == HTTP_200_OK:
        assert res.json()['id'] == id


@pytest.mark.asyncio
async def test_get_all_sponsors(client: AsyncClient) -> None:
    res = await client.get('/v1/sponsor')
    assert res.status_code == HTTP_200_OK
    assert isinstance(res.json(), list)
    assert sponsor in res.json()
