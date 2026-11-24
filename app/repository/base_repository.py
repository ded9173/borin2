from typing import Optional

from app.extensions import db

class BaseRepository:

    def __init__(self, model):
        self.model = model

    def get_all(self, skip: int = 0, limit: int = 100) -> list:
        return db.session.execute(db.select([self.model])).offset(skip).limit(limit).all()

    def get_by_id(self, item_id) -> Optional:
        return db.session.get(self.model, item_id)

    def create(self, **kwargs):
        item = self.model(**kwargs)
        db.session.add(item)
        db.session.commit()
        return item

    def update(self, item_id, **kwargs):
        item = self.get_by_id(item_id)
        if item:
            for key, value in kwargs.items():
                if value is not None:
                    setattr(item, key, value)
                db.session.commit()
            return item

    def delete(self, item_id):
        item = self.get_by_id(item_id)
        if item:
            db.session.delete(item)
            db.session.commit()
            return True
        return False