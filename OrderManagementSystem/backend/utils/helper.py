from fastapi import Request, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.auth import UserModel
from utils.db import get_db
from jwt.exceptions import InvalidTokenError
from utils.settings import settings
from datetime import datetime
from zoneinfo import ZoneInfo
import jwt

def indian_time():
    return datetime.now(ZoneInfo("Asia/Kolkata"))

def is_authenticated(request:Request, db:Session = Depends(get_db)):
    try:
        token = request.headers.get("authorization")
        if not token:
            raise HTTPException(detail="You are unauthorized!", status_code=401)
        
        token = token.split(" ")[-1]
        data = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        email = data.get("email")
        user = db.query(UserModel).filter(UserModel.email == email).first()
        if not user:
            raise HTTPException(detail="You are unauthorized!", status_code=401)

        return user

    except InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
    
def require_role(allowed_roles: list):
    def role_checker(user = Depends(is_authenticated)):
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action"
            )
        return user

    return role_checker