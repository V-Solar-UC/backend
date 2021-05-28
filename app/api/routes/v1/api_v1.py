from fastapi import APIRouter

from . import donor_route

router = APIRouter()

router.include_router(donor_route.router, prefix='/donor', tags=['donors'])
