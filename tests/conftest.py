import os
import warnings

import pytest
from alembic import command
from alembic.config import Config
from asgi_lifespan import LifespanManager
from databases import Database
from fastapi import FastAPI
from httpx import AsyncClient

from app.main import get_app


@pytest.fixture(scope='session')
def apply_migrations():
    # warnings.filterwarnings("ignore", category=DeprecationWarning)
    os.environ['TESTING'] = '1'
    config = Config('alembic.ini')

    command.upgrade(config, 'head')
    yield
    # TODO: do i need to downgrade if using force_rollback in db object?
    command.downgrade(config, 'base')
    os.environ['TESTING'] = ''


@pytest.fixture
def app(apply_migrations: None) -> FastAPI:
    app = get_app()
    return app


@pytest.fixture
def db(app: FastAPI) -> Database:
    return app.state.db


@pytest.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url='http://testserver',
            headers={'Content-Type': 'application/json'}
        ) as client:
            yield client
