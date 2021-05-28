import os

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import DATABASE_URL
from app.core.logging import logger


async def create_engine(app: FastAPI) -> None:
    # these can be configured in config as well
    DB_URL = f'{DATABASE_URL}_test' if os.environ.get(
        'TESTING') else DATABASE_URL

    engine = create_async_engine(DB_URL, echo=True)
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    logger.info('CREATED SQLALCHEMY ENGINE')

    app.state.async_session = async_session
    app.state._engine = engine


async def release_connections(app: FastAPI) -> None:
    # TODO: there might be better ways to close all connections
    await app.state._engine.dispose()
