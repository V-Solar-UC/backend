import logging
import sys
from pprint import pformat

from loguru import logger
from loguru._defaults import LOGURU_FORMAT

from .config import DEBUG
from .config import LOGGING_LEVEL


class InterceptHandler(logging.Handler):
    """
    Default handler from examples in loguru documentaion.
    See https://loguru.readthedocs.io/en/stable/overview.html
    """

    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def format_record(record: dict) -> str:
    """
    Custom format for loguru loggers.
    Uses pformat for log any data like request/response body during debug.
    Works with logging if loguru handler it.

    IMPORTANT: it works as long as 'DEBUG' variable exists. Make sure it
                does not exist in production mode.

    Example:
    >>> payload = [{"users":[{"name": "Nick", "age": 87, "is_active": True}, {"name": "Alex", "age": 27, "is_active": True}], "count": 2}]
    >>> logger.bind(payload=).debug("users payload")
    >>> [   {   'count': 2,
    >>>         'users': [   {'age': 87, 'is_active': True, 'name': 'Nick'},
    >>>                      {'age': 27, 'is_active': True, 'name': 'Alex'}]}]
    """
    format_string = LOGURU_FORMAT

    if record['extra'].get('payload') is not None:
        record['extra']['payload'] = pformat(
            record['extra']['payload'], indent=4, compact=True, width=88
        )
        format_string += '\n<level>{extra[payload]}</level>'

    format_string += '{exception}\n'
    return format_string


logging.getLogger().handlers = [InterceptHandler()]
for logger_name in ('uvicorn.asgi', 'uvicorn.access', 'uvicorn'):
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
