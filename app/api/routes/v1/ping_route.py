from fastapi import APIRouter

from app.core.logging import logger

router = APIRouter()


@router.get('/{message}')
async def get_ping(message: str) -> dict:
    # useful for logging body of request to stdout in debug mode:
    logger.bind(payload={'hola': '5'}).debug('params with formatting')
    return {'ping': 'pong', 'message': message}
