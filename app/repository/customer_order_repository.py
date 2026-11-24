from app.repository.base_repository import BaseRepository
from app.models import CustomerOrder

class customer_orderRepository(BaseRepository):
    def __init__(self):
        super().__init__(CustomerOrder)

