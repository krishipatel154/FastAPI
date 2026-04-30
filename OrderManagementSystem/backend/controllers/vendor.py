from fastapi import HTTPException
from sqlalchemy.orm import Session
from schemas.vendor import VendorSchema
from models.vendor import VendorModel
from models.auth import UserModel
from utils.settings import settings
from fastapi import UploadFile
from pwdlib import PasswordHash
from jwt.exceptions import InvalidTokenError
import os
import shutil
import jwt

password_hash = PasswordHash.recommended()

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password):
    return password_hash.hash(password)

def save_file(file: UploadFile, vendor_name: str, folder_name: str):
    # Example:
    # uploads/krishi_traders/id_proof/pan.pdf

    safe_vendor_name = vendor_name.strip().replace(" ", "_").lower()

    folder_path = os.path.join(
        settings.UPLOAD_DIR,
        safe_vendor_name,
        folder_name
    )

    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(
        folder_path,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_path

# vendor registration
def register_vendor(firstname: str,
    lastname: str,
    email: str,
    password: str,
    business_name: str,
    business_type: str,
    gst_number: str,
    pan_card: str,
    business_address: str,
    phone_number: str,
    id_proof: UploadFile,
    business_license: UploadFile, 
    db:Session
):
    try:
        is_user = db.query(UserModel).filter(UserModel.email == email).first()
        if is_user:
            raise HTTPException(status_code=400, detail="Email already exist")
        
        # Save files
        id_proof_path = save_file(
            id_proof,
            business_name,
            "id_proof"
        )

        business_license_path = save_file(
            business_license,
            business_name,
            "business_license"
        )

        role = "vendor"
        new_user = UserModel(
            firstname=firstname,
            lastname=lastname,
            email=email,
            password=get_password_hash(password),
            role=role
        )

        db.add(new_user)
        db.flush()

        new_vendor = VendorModel(
            user_id=new_user.id,
            business_name=business_name,
            business_type=business_type,
            gst_number=gst_number,
            pan_card=pan_card,
            business_address=business_address,
            phone_number=phone_number,
            id_proof_path=id_proof_path,
            business_license_path=business_license_path
        )

        db.add(new_vendor)
        db.commit()
        db.refresh(new_vendor)
        db.refresh(new_user)

        return new_vendor

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
def list_vendors(db:Session):
    try:
        vendors = db.query(
            VendorModel,
            UserModel
        ).join(
            UserModel,
            VendorModel.user_id == UserModel.id
        ).all()

        result = []

        for vendor, user in vendors:
            result.append({
                "firstname": user.firstname,
                "lastname": user.lastname,
                "email": user.email,
                "business_name": vendor.business_name,
                "business_type": vendor.business_type,
                "phone_number": vendor.phone_number,
                "vendor_status": vendor.vendor_status
            })

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
def list_vendors_by_status(status:str, db:Session):
    try:
        vendors = db.query(
            VendorModel,
            UserModel
        ).join(
            UserModel,
            VendorModel.user_id == UserModel.id
        ).filter(VendorModel.vendor_status == status).all()

        result = []

        for vendor, user in vendors:
            result.append({
                "firstname": user.firstname,
                "lastname": user.lastname,
                "email": user.email,
                "business_name": vendor.business_name,
                "business_type": vendor.business_type,
                "phone_number": vendor.phone_number,
                "vendor_status": vendor.vendor_status
            })

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# def get_single_vendor(id:int, db:Session):
#     pass
    # try:
    #     vendor = db.query(VendorModel, UserModel).join(UserModel, VendorModel.user_id == UserModel.id).filter(V)