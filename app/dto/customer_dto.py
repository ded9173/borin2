from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class CounterpartsDTO:
    countreparties_id:str
    name:str
    inn:Optional[str] = None
    address:Optional[str] = None
    phone:Optional[str] = None
    countreparties_type: str = ""
    created_at: Optional[str] = None

@classmethod
def from_model(cls, countreparties) -> "CounterpartsDTO":
    return cls(
        countreparties_id=str(countreparties.countreparties.id), name=countreparties.name, inn=countreparties.inn,
        address=countreparties.address, phone=countreparties.phone, countreparties_type=countreparties.countreparties_type,
        created_at=countreparties.created_at.isoformat() if countreparties.created_at else None,
    )

def to_dict(self) -> dict:
    return asdict(self)
