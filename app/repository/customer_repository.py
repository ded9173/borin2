from app.repository.base_repository import BaseRepository
from app.models import  Customer

class CountrerpartiesRepository(BaseRepository):

    def __init__(self):
        super().__init__(Customer)
