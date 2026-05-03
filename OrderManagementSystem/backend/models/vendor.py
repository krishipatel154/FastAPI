from utils.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from zoneinfo import ZoneInfo
from sqlalchemy import Enum

def indian_time():
    return datetime.now(ZoneInfo("Asia/Kolkata"))

class VendorModel(Base):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    business_name = Column(String(100), nullable=False)
    business_type = Column(String(100), nullable=False)
    gst_number = Column(String, nullable=True)
    pan_card = Column(String, nullable=False)
    business_address = Column(String(255), nullable=True)
    phone_number = Column(String(10), unique=True, nullable=False)
    id_proof_path = Column(String, nullable=False)
    business_license_path = Column(String, nullable=False)

    vendor_status = Column(
        Enum("pending", "approved", "rejected", name="vendor_status"),
        default="pending",
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        default=indian_time,
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        default=indian_time,
        onupdate=indian_time,
        nullable=False
    )

    user = relationship("UserModel")
    products = relationship("ProductModel", back_populates="vendor", cascade="all, delete")