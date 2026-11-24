from typing import Optional
from app.dto.customer_dto import CounterpartsDTO



class countrepartiesServise:
    def __init__(self):
        super().__init__()

    def get_all_dto(self, skip: int = 0, limit: int = 100) -> list[CounterpartsDTO]:
        clients = self.get_all(skip, limit)
        return [CounterpartsDTO.from_model(c) for c in clients]

    def create_countreparties(self, id) -> Optional[CounterpartsDTO]:
        countreparties = self.get_by_id(id)
        return self.repository.create(name=name, inn=inn, address=address, phone=phone, type=type)

    def update_countreparties(self, id, name=None, inn=None, address=None, phone=None, type=None):
        return self.repository.update(id, name=name, inn=inn, address=address, phone=phone, type=type)
