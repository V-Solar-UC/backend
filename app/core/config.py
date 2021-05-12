import logging
import sys

from databases import DatabaseURL
from loguru import logger
from starlette.config import Config
from starlette.datastructures import Secret

from .logging import format_record
from .logging import InterceptHandler

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
LOGGERS = ('uvicorn.asgi', 'uvicorn.access', 'uvicorn')

logging.getLogger().handlers = [InterceptHandler()]
for logger_name in LOGGERS:
    logging_logger = logging.getLogger(logger_name)
    logging_logger.handlers = [InterceptHandler(level=LOGGING_LEVEL)]

# set format
logger.configure(
    handlers=[{'sink': sys.stdout,
               'level': LOGGING_LEVEL, 'format': format_record}]
)

diagnose = True if DEBUG else False  # avoid leaking sensitive data in production
# save logs to disk
logger.add('log/access.log', format=format_record, enqueue=True, backtrace=True,
           diagnose=diagnose, compression='zip', rotation='10 MB', retention='1 month')
