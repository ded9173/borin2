from app.repository.base_repository import BaseRepository
from app.models import Users

class UsersRepository(BaseRepository):
    def __init__(self):
        super().__init__(Users)