from fastapi import HTTPException, Response
from schemas.auth import UserSchema, LoginSchema, UpdateUserSchema, ChangePassword, ForgotPasswordSchema
from models.auth import UserModel
from models.vendor import VendorModel
from utils.settings import settings
from sqlalchemy.orm import Session
from pwdlib import PasswordHash
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta
import jwt

password_hash = PasswordHash.recommended()

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password):
    return password_hash.hash(password)

def register(body:UserSchema, db:Session):
    try:
        is_user = db.query(UserModel).filter(UserModel.email == body.email).first()
        if is_user:
            return Response(status_code=400, content="User already exist!")
        
        # password hash
        hash_password = get_password_hash(body.password)

        user = UserModel(
            firstname = body.firstname,
            lastname = body.lastname,
            email = body.email,
            password = hash_password,
            role = body.role
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    except Exception as e:
        raise HTTPException(detail=str(e), status_code=500)
    
def login(body:LoginSchema, db:Session):
    try:
        user = db.query(UserModel).filter(UserModel.email == body.email).first()
        if not user:
            return Response(status_code=404, content="User not found!")
        
        if not verify_password(body.password, user.password):
            return Response(status_code=404, content="User not found!")

        exp = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        token = jwt.encode({"email":user.email, "role":user.role, "exp":exp}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

        return {"access_token":token}

    except Exception as e:
        raise HTTPException(detail=str(e), status_code=500)
    
def delete_user(id:int, db:Session):
    try:
        user = db.query(UserModel).filter(UserModel.id == id).first()
        if not user:
            return Response(status_code=404, content="User not found!")
        
        db.delete(user)
        db.commit()

        return {"message":"User Deleted Successfully!"}

    except Exception as e:
        raise HTTPException(status_code=401,
        detail="Invalid or expired token")
      
def get_profile(db:Session, current_user):
    try:
        print(current_user.role)
        user = db.query(UserModel).filter(UserModel.id == current_user.id).first()
        return user

    except Exception as e:
        raise HTTPException(status_code=401,
        detail="Invalid or expired token")
    
def update_profile(body:UpdateUserSchema, db:Session, current_user):
    try:
        user = db.query(UserModel).filter(UserModel.id == current_user.id).first()
        if not user:
            raise HTTPException(status_code=404,detail="User Not Found")
        
        # only update fields that were sent
        update_data = body.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(user, key, value)

        db.commit()
        db.refresh(user)

        return {
            "message": "Profile updated successfully",
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500,detail=str(e))

def chnage_password(body:ChangePassword, db:Session, current_user):
    try:
        user = db.query(UserModel).filter(UserModel.id == current_user.id).first()
        if not user:
            raise HTTPException(status_code=404,detail="User Not Found")
        
        # check old password
        if not verify_password(body.old_password, user.password):
            raise HTTPException(status_code=404, detail="Old password is wrong")
        
        # Prevent same old/new password
        if body.old_password == body.new_password:
            raise HTTPException(
                status_code=400,
                detail="New password must be different from old password"
            )
        
        user.password = get_password_hash(body.new_password)

        db.commit()
        db.refresh(user)

        return {
            "message": "Password updated successfully",
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
def forgot_password(body:ForgotPasswordSchema, db:Session):
    try:
        user = db.query(UserModel).filter(UserModel.email == body.email).first()
        if not user:
            return Response(content="User not found", status_code=404)
        
        # check password and verify password
        if not body.new_password == body.verify_password:
            return Response(content="New password and Verify password must be same!", status_code=404)
        
        # Prevent same old/new password
        if verify_password(body.new_password, user.password):
            return Response(
                status_code=400,
                content="New password must be different from old password"
            )

        # password hash
        user.password = get_password_hash(body.new_password)

        db.commit()
        db.refresh(user)

        return Response(status_code=200, content="Forgot Password Successfully Done!")

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

