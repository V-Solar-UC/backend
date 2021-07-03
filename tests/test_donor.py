import pytest
from httpx import AsyncClient
from starlette.status import HTTP_200_OK
from starlette.status import HTTP_201_CREATED
from starlette.status import HTTP_404_NOT_FOUND
from starlette.status import HTTP_409_CONFLICT

donor = {
    'name': 'donor1'
}

body = {
    'new_donor': donor
}


@pytest.mark.parametrize(
    'payload, status_code',
    (
        (body, HTTP_201_CREATED),
        (body, HTTP_409_CONFLICT)
    )
)
@pytest.mark.asyncio
async def test_create_donor(
        client: AsyncClient,
        payload: dict,
        status_code: int
) -> None:
    res = await client.post('/v1/donor', json=payload)
    assert res.status_code == status_code
    if status_code == HTTP_201_CREATED:
        donor['id'] = res.json()['id']
        assert res.json() == donor


@pytest.mark.parametrize(
    'id, status_code',
    (
        (1, HTTP_200_OK),
        (122312, HTTP_404_NOT_FOUND)
    )
)
@pytest.mark.asyncio
async def test_get_donor(
        client: AsyncClient,
        id: int,
        status_code: int
) -> None:
    res = await client.get(f'/v1/donor/{id}')
    assert res.status_code == status_code
    if status_code == HTTP_200_OK:
        assert res.json()['id'] == id


@pytest.mark.asyncio
async def test_get_all_donors(client: AsyncClient) -> None:
    res = await client.get('/v1/donor')
    assert res.status_code == HTTP_200_OK
    assert isinstance(res.json(), list)
    assert donor in res.json()

# async def test_update_donor():
#     pass


@pytest.mark.parametrize(
    'id, status_code',
    (
        (1, HTTP_200_OK),
        (123231, HTTP_404_NOT_FOUND)
    )
)
@pytest.mark.asyncio
async def test_delete_donor(
        client: AsyncClient,
        id: int,
        status_code: int
) -> None:
    res = await client.delete(f'/v1/donor/{id}')
    assert res.status_code == status_code
    if status_code == HTTP_200_OK:
        assert res.json() == donor
        res_get = await client.get(f'/v1/donor/{id}')
        assert res_get.status_code == HTTP_404_NOT_FOUND
