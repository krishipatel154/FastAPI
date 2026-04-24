from utils.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Text, DateTime
from schemas.user import UserSchema
from sqlalchemy.orm import relationship
from datetime import datetime

class CategoriesSchema(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    user = relationship("UserSchema", back_populates="categories")
    expenses = relationship("ExpenseSchema", back_populates="category")

class ExpenseSchema(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    date = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    user = relationship("UserSchema", back_populates="expenses")
    category = relationship("CategoriesSchema", back_populates="expenses")