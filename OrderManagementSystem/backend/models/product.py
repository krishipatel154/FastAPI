from utils.db import Base
from sqlalchemy import Column, Integer, String, Text, Numeric, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from typing import Literal

class CategoryModel(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)

    products = relationship("ProductModel", back_populates="category")

class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), index=True)
    description = Column(String(500))
    price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False, index=True)

    vendor = relationship("VendorModel", back_populates="products")
    category = relationship("CategoryModel", back_populates="products")

    __table_args__ = (
        CheckConstraint('quantity >= 0', name='check_quantity_non_negative'),
    )

    @property
    def stock_status(self):
        if self.quantity == 0:
            return "out_of_stock"
        elif self.quantity < 5:
            return "low_stock"
        return "in_stock"