from app.repository.base_repository import BaseRepository
from app.models import Items

class ItemsRepository(BaseRepository):
    def __init__(self):
        super().__init__(Items)
