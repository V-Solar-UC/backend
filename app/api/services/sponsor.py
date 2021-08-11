from app.api.services.base import BaseService
from app.db.models import Sponsor


class SponsorService(BaseService):

    @staticmethod
    async def find(*args, **kwargs):
        return await BaseService.find(Sponsor, *args, **kwargs)

    @staticmethod
    async def find_all(*args, **kwargs):
        return await BaseService.find_all(Sponsor, *args, **kwargs)

    @staticmethod
    async def create(*args, **kwargs):
        return await BaseService.create(Sponsor, *args, **kwargs)
