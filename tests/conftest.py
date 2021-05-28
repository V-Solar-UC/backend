import os

import pytest
from alembic import command
from alembic.config import Config
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient

from app.main import get_app


@pytest.fixture(scope='session', autouse=True)
def apply_migrations():
    os.environ['TESTING'] = '1'
    config = Config('alembic.ini')

    command.upgrade(config, 'head')
    yield
    command.downgrade(config, 'base')
    os.environ['TESTING'] = ''


@pytest.fixture(scope='session')
def app() -> FastAPI:
    app = get_app()
    return app


@pytest.fixture()
async def client(app: FastAPI) -> AsyncClient:
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url='http://testserver',
            headers={'Content-Type': 'application/json'}
        ) as client:
            yield client
