from typing import Any
from typing import List

from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK
from starlette.status import HTTP_201_CREATED

from app.api.dependencies.session import get_session
from app.api.services.sponsor import SponsorService
from app.schemas.sponsor import Sponsor as SponsorSchema
from app.schemas.sponsor import SponsorCreate


router = APIRouter()


@router.get('/{id}', response_model=SponsorSchema, status_code=HTTP_200_OK)
async def find_sponsor(
        id: int,
        session: AsyncSession = Depends(get_session)
) -> Any:
    sponsor = await SponsorService.find(session, id)
    return sponsor


@router.get('/', response_model=List[SponsorSchema], status_code=HTTP_200_OK)
async def get_all_sponsors(
        session: AsyncSession = Depends(get_session)
) -> Any:
    sponsors = await SponsorService.find_all(session)
    return sponsors


@router.post('/', response_model=SponsorSchema, status_code=HTTP_201_CREATED)
async def create_sponsor(
        new_sponsor: SponsorCreate = Body(..., embed=True),
        session: AsyncSession = Depends(get_session)
) -> Any:
    sponsor = await SponsorService.create(session, new_sponsor)
    return sponsor
