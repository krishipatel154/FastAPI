from fastapi import APIRouter, Depends, Form, File, UploadFile
from typing import List
from utils.helper import require_role
from controllers import vendor
from schemas.vendor import VenderListResponseSchema
from sqlalchemy.orm import Session
from utils.db import get_db

vendor_router = APIRouter()

@vendor_router.post("/register")
def register_vendor(firstname: str = Form(...),
    lastname: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    business_name: str = Form(...),
    business_type: str = Form(...),
    gst_number: str = Form(None),
    pan_card: str = Form(...),
    business_address: str = Form(None),
    phone_number: str = Form(...),

    id_proof: UploadFile = File(...),
    business_license: UploadFile = File(...),
    db:Session = Depends(get_db)
):
    return vendor.register_vendor(firstname=firstname,
        lastname=lastname,
        email=email,
        password=password,
        business_name=business_name,
        business_type=business_type,
        gst_number=gst_number,
        pan_card=pan_card,
        business_address=business_address,
        phone_number=phone_number,
        id_proof=id_proof,
        business_license=business_license,
        db=db
    )

@vendor_router.get("/all", response_model=List[VenderListResponseSchema])
def list_vendors(db:Session = Depends(get_db), user = Depends(require_role(["admin"]))):
    return vendor.list_vendors(db)

# @vendor_router.get("/single/{id}")
# def get_single_vendor(id:int, db:Session, user = Depends(require_role(["admin"]))):
#     return vendor.get_single_vendor(id, db)

@vendor_router.get("/pending")
def list_vendors_by_status(status: Literal["pending", "approved", "rejected"], db:Session = Depends(get_db), user = Depends(require_role(["admin"]))):
    return vendor.list_vendors_by_status(status, db)

