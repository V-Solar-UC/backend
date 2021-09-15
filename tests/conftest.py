import os

import pytest
from alembic import command
from alembic.config import Config
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from httpx import AsyncClient

from app.api.services.user import UserService
from app.main import get_app
from app.schemas.user import UserInDB


@pytest.fixture(scope='session', autouse=True)
def apply_migrations():
    os.environ['TESTING'] = '1'
    config = Config('alembic.ini')

    command.upgrade(config, 'head')
    yield
    command.downgrade(config, 'base')
    os.environ['TESTING'] = ''


@pytest.fixture()
async def app() -> FastAPI:
    app = get_app()
    async with LifespanManager(app):
        yield app


@pytest.fixture()
async def user(app: FastAPI):
    async with app.state.async_session() as session:
        user_data = {
            'username': 'test',
            'name': 'test name',
            'career': 'test career',
            'team': 'team test',
            'profile_photo_path': '',
            'email': 'test@mail.com',
            'password': 'testpws',
        }
        try:
            user = await UserService.find_by(session, 'email', user_data['email'])
        except HTTPException:
            hashed_password = UserService.password_hash(password=user_data['password'])
            user_data.update({'hashed_password': hashed_password})
            user = await UserService.create(session, UserInDB(**user_data))
        finally:
            return user


@pytest.fixture()
async def client(app: FastAPI) -> AsyncClient:
    async with AsyncClient(
        app=app,
        base_url='http://testserver',
        headers={'Content-Type': 'application/json'}
    ) as client:
        yield client
