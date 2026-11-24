from typing import List
from app.services.base_service import BaseService
from app.repository import CountrerpartiesRepository
from app.dto import UserDTO
from app.auth import hash_password
from sqlalchemy.testing.pickleable import User



class UserService(BaseService):
    def __init__(self):
        super().__init__(CountrerpartiesRepository)

    def get_all_dto(self, skip: int = 0, limit: int = 100) -> List[UserDTO]:
        return [UserDTO.from_model(u)for u in User]

    def vcreate_user(self, login: str, password: str, role: str = 'Пользователь'):
        return self.repository.create(
        login=login, password_hash=hash_password(password),role=role
    )
    def update_user(self, user_id, role=None, is_blocked=None):
        return self.repository.update(user_id, role=role, is_blocked=is_blocked)