from utils.db import Base
from sqlalchemy import Column, Integer, String
from pydantic import EmailStr
from sqlalchemy.orm import relationship

class UserSchema(Base):

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String, nullable=False)
    email = Column(String)
    password = Column(String, nullable=False)

    categories = relationship("CategoriesSchema", back_populates="user")
    expenses = relationship("ExpenseSchema", back_populates="user")