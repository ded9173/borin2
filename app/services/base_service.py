from typing import List, Optional

class BaseService:
    def __init__(self, repository):
        self.repository = repository

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.repository.get_all(skip=skip, limit=limit)

    def get_by_id(self, item_id):
        return self.repository.get_by_id(item_id)

    def get_by_id(self, item_id):
        return self.repository.get_by_id(item_id)

    def create(self, **kwargs):
        return self.repository.create(**kwargs)

    def update(self, **kwargs):
        return self.repository.update(**kwargs)

    def delete(self, item_id):
        return self.repository.delete(item_id)
