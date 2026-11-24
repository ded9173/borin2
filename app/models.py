"""SQLAlchemy models aligned with database/db.sql."""
from datetime import date
from flask_login import UserMixin
from sqlalchemy import CheckConstraint, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, Boolean, func
from app.extensions import db


class Customer(db.Model):
    __tablename__ = "counterparties"
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(255), nullable=False)
    inn = db.Column(String(20))
    address = db.Column(String(255))
    phone = db.Column(String(30))
    type = db.Column(String(30))


class Items(db.Model):
    __tablename__ = "items"
    id = db.Column(Integer, primary_key=True)
    code = db.Column(String(100), nullable=False)
    name = db.Column(String(255), nullable=False)
    item_type = db.Column(String(50), nullable=False)


class Price(db.Model):
    __tablename__ = "price"
    id = db.Column(Integer, primary_key=True)
    item_id = db.Column(Integer, ForeignKey("items.id"))
    price = db.Column(Numeric(12, 2), nullable=False)
    effective_from = db.Column(Date)
    effective_to = db.Column(Date)


class CostPrice(db.Model):
    __tablename__ = "cost_price"
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(255))
    item_id = db.Column(Integer, ForeignKey("items.id"))
    price_id = db.Column(Integer, ForeignKey("price.id"))
    cost_price = db.Column(Numeric(12, 2), nullable=False)


class CustomerOrder(db.Model):
    __tablename__ = "customer_order"
    id = db.Column(Integer, primary_key=True)
    items_id = db.Column(Integer, ForeignKey("items.id"))
    counterparties_id = db.Column(Integer, ForeignKey("counterparties.id"))
    quantity = db.Column(Numeric(12, 2), nullable=False)
    unit_price = db.Column(Numeric(12, 2), nullable=False)


class ManufacturingOrder(db.Model):
    __tablename__ = "manufactur_order"
    id = db.Column(Integer, primary_key=True)
    items_id = db.Column(Integer, ForeignKey("items.id"))
    cost_price = db.Column(Integer, ForeignKey("cost_price.id"))


class ProductionOrder(db.Model):
    __tablename__ = "production_orders"
    id = db.Column(Integer, primary_key=True)
    items_id = db.Column(Integer, ForeignKey("items.id"))
    cost_price = db.Column(Integer, ForeignKey("cost_price.id"))
    quantity = db.Column(Numeric(12, 2))
    unit_price = db.Column(Numeric(12, 2))


# Backward-compatible class name used by legacy service modules.
Production_Order = ProductionOrder


class Users(UserMixin, db.Model):
    __tablename__ = "users"
    user_id = db.Column("users_id", Integer, primary_key=True, autoincrement=True)
    login = db.Column(String(50), unique=True, nullable=False, index=True)
    password_hash = db.Column(String(255), nullable=False)
    role = db.Column(String(30), nullable=False, default="Пользователь")
    is_blocked = db.Column(Boolean, nullable=False, default=False)
    failed_attempts = db.Column(Integer, nullable=False, default=0)
    blocked_until = db.Column(DateTime)
    created_at = db.Column(DateTime, server_default=func.current_timestamp())

    def get_id(self):
        return str(self.user_id)


class Notes(db.Model):
    __tablename__ = "notes"
    note_id = db.Column("id", Integer, primary_key=True, autoincrement=True)
    title = db.Column(String(255), nullable=False)
    content = db.Column(Text, nullable=False)
    id_user = db.Column(Integer, ForeignKey("users.users_id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = db.Column(DateTime, server_default=func.current_timestamp())
