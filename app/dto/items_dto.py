from dataclasses import dataclass, asdict
from types import Optional

from app.blueprints import items


@dataclass
class ItemsDTO:
    items_id:str
    code:str
    name:str
    item_type:Optional[str] = None

    @classmethod
    def from_model(cls, order):
        return cls(
            items_id=str(order.items_id), name=items.name,
            code = items.code,  item_type = items.item_type,
        )

    def to_dict(self):
        return asdict(self)
