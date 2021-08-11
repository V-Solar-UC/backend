from fastapi import APIRouter

from . import donor_route
from . import sponsor_route

router = APIRouter()

router.include_router(donor_route.router, prefix='/donor', tags=['donors'])
router.include_router(
    sponsor_route.router,
    prefix='/sponsor',
    tags=['sponsors'])
