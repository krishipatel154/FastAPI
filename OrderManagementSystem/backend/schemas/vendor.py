from pydantic import BaseModel, Field, EmailStr
from typing import Annotated, Optional
from fastapi import Form, File, UploadFile

class VendorSchema(BaseModel):
    firstname: Annotated[str, Field(min_length=2, max_length=100)]
    lastname: Annotated[Optional[str], Field(min_length=2, max_length=100)] = None
    email: EmailStr
    password: Annotated[str, Field(min_length=8, max_length=100)]
    business_name: Annotated[str, Field(min_length=2, max_length=100)]
    business_type: Annotated[str, Field(min_length=2, max_length=100)]
    business_address: Annotated[Optional[str], Field(min_length=2, max_length=255)] = None
    gst_number: Annotated[Optional[str], Field(min_length=2, max_length=100)] = None
    pan_card: Annotated[str, Field(min_length=2, max_length=100)]
    phone_number: Annotated[str, Field(min_length=10, max_length=10)]
    id_proof_path: str
    business_license_path: str

class VenderListResponseSchema(BaseModel):
    firstname: str
    lastname: str
    email: str
    business_name: str
    business_type: str
    phone_number: str
    vendor_status: str
