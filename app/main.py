from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.v1 import api_v1
from app.core import config
from app.core import logging
from app.core import tasks


def get_app() -> FastAPI:
    app = FastAPI(title=config.PROJECT_NAME, version=config.VERSION)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )

    app.add_event_handler('startup', tasks.create_start_app_handler(app))
    app.add_event_handler('shutdown', tasks.create_stop_app_handler(app))

    app.include_router(api_v1.router, prefix='/v1')

    return app
