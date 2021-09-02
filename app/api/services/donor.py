from app.api.services.base import BaseService
from app.db.models import Donor


class DonorService(BaseService):
    model = Donor
