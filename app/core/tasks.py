from typing import Callable

from fastapi import FastAPI

from app.db.tasks import create_engine
from app.db.tasks import release_connections


def create_start_app_handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        await create_engine(app)
    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:
    async def stop_app() -> None:
        await release_connections(app)
    return stop_app
