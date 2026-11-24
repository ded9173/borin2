from app.repository.base_repository import BaseRepository
from app.models import CostPrice

class CostPriceRepository(BaseRepository):
    def __init__(self):
        super().__init__(CostPrice)
