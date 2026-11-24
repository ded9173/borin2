from app.repository.base_repository import BaseRepository
from app.models import Production_Order

class ProductionOrderRepository(BaseRepository):
    def __init__(self):
        super().__init__(Production_Order)
