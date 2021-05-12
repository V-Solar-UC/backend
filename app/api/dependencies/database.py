from typing import Callable
from typing import Type

from databases import Database
from fastapi import Depends
from starlette.requests import Request

from app.db.repositories.base import BaseRepository


def get_database(request: Request) -> Database:
    return request.app.state.db


def get_repository(Repository: Type[BaseRepository]) -> Callable:
    def get_repo(db: Database = Depends(get_database)) -> Type[BaseRepository]:
        """ adds db atribute to a repository """
        return Repository(db)
    return get_repo
