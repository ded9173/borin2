from app.repository.base_repository import BaseRepository
from app.models import Price

class PriceRepository(BaseRepository):
    def __init__(self):
        super().__init__(Price)
