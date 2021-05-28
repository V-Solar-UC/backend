from typing import Any
from typing import List

from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK
from starlette.status import HTTP_201_CREATED

from app.api.dependencies.session import get_session
from app.api.services.donor import DonorService
from app.schemas.donor import Donor as DonorSchema
from app.schemas.donor import DonorCreate


router = APIRouter()


@router.post('/', response_model=DonorSchema, status_code=HTTP_201_CREATED)
async def create_donor(
        new_donor: DonorCreate = Body(..., embed=True),
        session: AsyncSession = Depends(get_session)
) -> Any:
    donor = await DonorService.create(session, new_donor)
    return donor


@router.get('/{id}', response_model=DonorSchema, status_code=HTTP_200_OK)
async def find_donor(
        id: int,
        session: AsyncSession = Depends(get_session)
) -> Any:
    donor = await DonorService.find(session, id)
    return donor


@router.get('/', response_model=List[DonorSchema], status_code=HTTP_200_OK)
async def get_all_donors(
        session: AsyncSession = Depends(get_session)
) -> Any:
    donors = await DonorService.find_all(session)
    return donors


@router.delete('/{id}', response_model=DonorSchema, status_code=HTTP_200_OK)
async def delete_donor(
        id: int,
        session: AsyncSession = Depends(get_session)
) -> Any:
    donor = await DonorService.find(session, id)
    await DonorService.delete(session, donor)
    return donor
