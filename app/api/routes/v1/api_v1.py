from fastapi import APIRouter

from . import ping_route

router = APIRouter()

router.include_router(ping_route.router, prefix='/ping', tags=['ping'])
