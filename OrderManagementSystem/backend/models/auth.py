# database tables
from utils.db import Base
from sqlalchemy import Column, Integer, String, Enum, Boolean, DateTime
from datetime import datetime
from zoneinfo import ZoneInfo
import enum

def indian_time():
    return datetime.now(ZoneInfo("Asia/Kolkata"))

class UserRole(str, enum.Enum):
    user = "user"
    admin = "admin"
    vendor = "vendor"

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)  # hashed password only
    role = Column(
        Enum(UserRole),
        default=UserRole.user,
        nullable=False
    )
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=indian_time, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=indian_time, onupdate=indian_time, nullable=False)
