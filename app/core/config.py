import logging

from databases import DatabaseURL
from starlette.config import Config
from starlette.datastructures import Secret

config = Config('.env')

PROJECT_NAME = 'V-Solar backend'
VERSION = '0.1.0'

POSTGRES_USER: str = config('POSTGRES_USER', cast=str)
POSTGRES_PASSWORD: Secret = config('POSTGRES_PASSWORD', cast=Secret)
POSTGRES_SERVER: str = config('POSTGRES_SERVER', cast=str, default='db')
POSTGRES_PORT: str = config('POSTGRES_PORT', cast=str, default='5432')
POSTGRES_DB: str = config('POSTGRES_DB', cast=str)

DATABASE_URL = config(
    'DATABASE_URL',
    cast=DatabaseURL,
    default=f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}'
)

DEBUG: bool = config('DEBUG', cast=bool, default=False)

LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
