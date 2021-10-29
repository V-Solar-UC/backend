from fastapi import APIRouter

from . import donor_route
from . import session_route
from . import user_route

router = APIRouter()

router.include_router(donor_route.router, prefix='/donor', tags=['Donors'])
router.include_router(user_route.router, prefix='/user', tags=['Users'])
router.include_router(session_route.router, prefix='/session', tags=['Session'])
