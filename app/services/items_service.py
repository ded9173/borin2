from typing import Optional, List
from app.repository.items_repository import ItemsRepository
from app.services.base_service import BaseService
from app.dto import ItemsDTO
class ItemService(BaseService):
    def __init__(self):
        super().__init__(ItemsRepository())

    def get_all_dto(self, skip: int = 0, limit: int = 100) -> List[ItemsDTO]:
        items = self.get_all(skip,limit)
        return [List[ItemsDTO].from_model(m) for m in items]

    def get_by_id_dto(self, item_id) -> Optional[ItemsDTO]:
        item = self.get_by_id(item_id)
        return ItemsDTO.from_model(item) if item else None

    def create_items(self, name, code, type):
        return self.repository.create_items(name=name, code=code, type=type)

    def update_item(self, item_id, name, code, type):
        return self.repository.update_item(item_id, name, code, type)

