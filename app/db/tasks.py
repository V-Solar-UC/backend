import os

from databases import Database
from fastapi import FastAPI

from app.core.config import DATABASE_URL
from app.core.config import logger


async def connect_to_db(app: FastAPI) -> None:
    # these can be configured in config as well
    DB_URL = f'{DATABASE_URL}_test' if os.environ.get(
        'TESTING') else DATABASE_URL

    fr = True if os.environ.get('TESTING') else False

    database = Database(DB_URL, min_size=2, max_size=10, force_rollback=fr)

    try:
        logger.info('--- CONNECTING TO DB ---')
        await database.connect()
        logger.info('--- CONNECTED TO DB ---')
        app.state.db = database
    except Exception as e:
        logger.warn('--- DB CONNECTION ERROR ---')
        logger.warn(e)
        logger.warn('--- DB CONNECTION ERROR ---')


async def close_db_connection(app: FastAPI) -> None:
    try:
        logger.info('--- DISCONNECTING FROM DB ---')
        await app.state.db.disconnect()
        logger.info('--- DISCONNECTED FROM DB ---')
    except Exception as e:
        logger.warn('--- DB DISCONNECT ERROR ---')
        logger.warn(e)
        logger.warn('--- DB DISCONNECT ERROR ---')
