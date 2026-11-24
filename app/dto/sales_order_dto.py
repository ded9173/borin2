from dataclasses import dataclass, asdict
from typing import Optional, List

@dataclass
class SalesOrderItemDTO:
    sales_order_item_id: str
    product_id: str
    quantity: float
    unit_price: float

    @classmethod
    def from_model(cls, item)->"SalesOrderItemDTO":
        return cls(
            sales_order_item_id=str(item.sales_order_item_id),
            product_id=str(item.product_id),
            quantity=float(item.quantity),
            unit_price=float(item.unit_price),
        )
    def to_dict(self) -> dict:
        return asdict(self)

@dataclass
class SalesOrderDTO:
    sales_order_id: str
    order_number: str
    order_date: Optional[str] = None
    countreparties_id: str = ""
    executer_id: str = ""
    total_amount: float = 0.0
    created_at: Optional[str] = None
    Items: Optional[List[SalesOrderItemDTO]] = None

    @classmethod
    def from_model(cls, order)->"SalesOrderDTO":
        items = [SalesOrderItemDTO.from_model(item) for item in order.items] if order.items else None
        return cls(
             sales_order_id=str(order.sales_order_id), order_number=order.order_number,
            order_date=order.order_date.isoformat() if order.order_date else None,
            countreparties_id=str(order.countreparties_id), executer_id=str(order.executer_id),
            total_amount=float(order.total_amount) if order.total_amount else 0,
            created_at=str(order.created_at) if order.created_at else None,
            items=items,
            )
    def to_dict(self) -> dict:
        return asdict(self)