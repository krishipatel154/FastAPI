from utils.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from zoneinfo import ZoneInfo

def indian_time():
    return datetime.now(ZoneInfo("Asia/Kolkata"))

class VendorModel(Base):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    # firstname = Column(String(100), nullable=False)
    # lastname = Column(String(100), nullable=True)
    # email = Column(String(255), unique=True, nullable=False, index=True)
    # password = Column(String, nullable=False)
    business_name = Column(String(100), nullable=False)
    business_type = Column(String(100), nullable=False)
    gst_number = Column(String, nullable=True)
    pan_card = Column(String, nullable=False)
    business_address = Column(String(255), nullable=True)
    phone_number = Column(String(10), unique=True, nullable=False)
    id_proof_path = Column(String, nullable=False)
    business_license_path = Column(String, nullable=False)

    vendor_status = Column(
        String(50),
        default="pending",
        nullable=False
    )  # pending / approved / rejected

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
