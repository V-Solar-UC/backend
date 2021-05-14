import pytest
from httpx import AsyncClient

from app.core.logging import logger


@pytest.mark.asyncio
async def test_ping_response(client: AsyncClient) -> None:
    res = await client.get('v1/ping/hola')
    logger.info(client.base_url)
    logger.info(dir(res))
    assert res.status_code == 200
    assert res.json()['ping'] == 'pong'
