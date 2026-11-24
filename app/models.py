from datetime import date

from sqlalchemy import (
    Column,
    String,
    Text,
    ForeignKey,
    Numeric,
    CheckConstraint,
    column, Integer, DateTime, Date,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.extensions import db


class Customer (db.Model):
    __tablename__ = "countrerparties"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=func.random_uuid()
    )
    name = Column(String(255), nullable=False)
    inn = Column(String(20))
    address = Column(String(255))
    phone = Column(String(20))
    type = Column(String(20), nullable=True)

    __table_args__ = (
        CheckConstraint(
            "type IN ( 'Постовшик', 'Покупатель')",
            name = "chk_client_type",
        ),
    )

    sales_orders_as_customer = relationship(
        "SalesOrder", foreign_keys="SalesOrder.customer_id", back_populates="customer"
    )
    sales_orders_suplier = relationship(
        "salesorder",foreign_keys="salesorder.suplier_id", back_populates="suplier"
    )

class Items(db.Model):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, nullable=False)
    name = Column(String, nullable=False)
    item_type = Column(String, nullable=False)  # 'Продукция', 'Материалы', 'Операция'

    __table_args__ = (
        CheckConstraint(
            "item_type IN ('Продукция', 'Материалы', 'Операция')",
            name="chk_item_type"
        ),
    )


    specifications = relationship("Specification", back_populates="item", cascade="all, delete-orphan")
    prices = relationship("Price", back_populates="item", cascade="all, delete-orphan")
    cost_prices = relationship("CostPrice", back_populates="item", cascade="all, delete-orphan")
    production_orders = relationship("ProductionOrder", back_populates="item", cascade="all, delete-orphan")
    customer_order_items = relationship("CustomerOrderItem", back_populates="item")


class Price (db.Model):
    id = Column(
        uuid=UUID(as_uuid=True), primary_key=True, default=func.random_uuid()
    )
    item_id = Column(Integer, ForeignKey('items.id'))
    price = Column(Numeric(10, 2), nullable=False)
    effective_date = Column(Date, nullable=False, default=date.today)

    item = relationship("Items", back_populates="prices")
    cost_prices = relationship("CostPrice", back_populates="price", cascade="all, delete-orphan")


class CostPrice (db.Model):
    id = Column(
        uuid=UUID(as_uuid=True), primary_key=True, default=func.random_uuid()
    )
    name = Column(String(255), nullable=True)
    item_id = Column(Integer, ForeignKey('items.id'))
    price_id = Column(Integer, ForeignKey('price.id'))
    cost_price = Column(Numeric(10, 2), nullable=False)

    item = relationship('item', back_populates='cost_price')
    price = relationship('price', back_populates='cost_price')

class CustomerOrder (db.Model):
    id = Column()
    Customer_id = Column(Integer, ForeignKey("Customer.id"))
    quantity = Column(Integer)
    unit_price = Column(Numeric)


    items = relationship('items', back_populates='orders')
    Customer_id = relationship('v', back_populates='orders')


class Production_Order (db.Model):
    id = Column(
        uuid=UUID(as_uuid=True), primary_key=True, default=func.random_uuid()
    )
    item_id = Column(Integer, ForeignKey("items.id"))
    customer_order_id = Column(Integer, ForeignKey("customer_order.id"))
    cost_price = column(int)
    quantity = Column(int)
    unit_price = Column(int)

    CustomerOrder_id = relationship("CustomerOrder", back_populates="CustomerOrder", cascade="all, delete-orphan")
    items = relationship('items', back_populates='orders', cascade='all, delete-orphan')

class Specification(db.Model):
    id = Column(
        uuid=UUID(as_uuid=True), primary_key=True, default=func.random_uuid()
    )
    item_id = Column(Integer, ForeignKey("items.id"))
    quantity = Column(int)
    cost_price = Column(int)

    items = relationship('items', back_populates='manufactur_order')
    items_id = relationship('cost_price', back_populates='items', cascade='all, delete-orphan')



class ProductionOrderItem(db.Model):
    """Продукция в заказе на производство."""
    __tablename__ = "production_order_items"

    order_item_id = Column(
        UUID(as_uuid=True), primary_key=True, default=func.gen_random_uuid()
    )
    production_order_id = Column(
        UUID(as_uuid=True),
        ForeignKey("production_orders.order_id", ondelete="CASCADE"),
        nullable=False,
    )
    product_id = Column(
        UUID(as_uuid=True),
        ForeignKey("products.product_id", ondelete="RESTRICT"),
        nullable=False,
    )
    quantity = Column(Numeric(10, 2), nullable=False)
    completed_quantity = Column(Numeric(10, 2), nullable=False, server_default="0.00")
    unit_price = Column(Numeric(10, 2), nullable=False)
    total_price = Column(Numeric(12, 2), nullable=False)

    __table_args__ = (
        CheckConstraint("quantity > 0", name="chk_prod_order_qty_positive"),
        CheckConstraint("completed_quantity >= 0", name="chk_prod_order_completed_non_negative"),
        CheckConstraint("unit_price >= 0", name="chk_prod_order_unit_price_non_negative"),
        CheckConstraint("total_price >= 0", name="chk_prod_order_total_price_non_negative"),
    )

    # ondelete="RESTRICT" — запрещает удалять Product, если он используется в ProductionOrderItem.
    # Это защита от случайного удаления данных, на которые есть ссылки.
    production_order = relationship("ProductionOrder", back_populates="items")
    product = relationship("Product", back_populates="prod_order_items")


class Users(db.Model):

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, server_default = "Пользователь")
    filed_attempt = Column(Integer, nullable=False, server_default= False)
    failed_attempt = Column(Integer, nullable=False, server_default= "0")
    blocked_until = column(DateTime)
    created_at = Column(DateTime, server_default= "0")

    __table_args__ = (
        CheckConstraint(
            "role IN( 'Администатор', 'Пользователь')",
            name = "chk_client_role",
        ),
    )

    notes = relationship('notes', back_populates='user')

    @property
    def is_authenticated(self):
        return True
    @property
    def is_active(self):
        return True
    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.user_id)

class Notes (db.Model):
    __tablename__ = "notes"

    note_id =Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    id_user = column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship('users', backref='notes')
