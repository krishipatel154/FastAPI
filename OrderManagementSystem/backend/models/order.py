from utils.db import Base
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime
from typing import Literal
from sqlalchemy.orm import relationship
from utils.helper import indian_time

class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_amount = Column(Numeric(10,2), nullable=False)
    status = Column(String, default="pending")
    shipping_address = Column(String, nullable=False)

    created_at = Column(DateTime, default=indian_time)

    items = relationship("OrderItemsModel", back_populates="order")

class OrderItemsModel(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))

    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)

    order = relationship("OrderModel", back_populates="items")
    product = relationship("ProductModel")