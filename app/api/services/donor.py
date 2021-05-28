from app.api.services.base import BaseService
from app.db.models import Donor


class DonorService(BaseService):

    @staticmethod
    async def find(*args, **kwargs):
        return await BaseService.find(Donor, *args, **kwargs)

    @staticmethod
    async def find_all(*args, **kwargs):
        return await BaseService.find_all(Donor, *args, **kwargs)

    @staticmethod
    async def create(*args, **kwargs):
        return await BaseService.create(Donor, *args, **kwargs)
