from sqlalchemy.orm import Session
from fastapi import Depends, Request, HTTPException
from utils.db import get_db
from jwt import ExpiredSignatureError, InvalidTokenError
from utils.settings import settings
from schemas.user import UserSchema
import jwt

def is_authenticated(request: Request ,db: Session = Depends(get_db)):
    try:
        token = request.headers.get("authorization")

        if not token:
            raise HTTPException(401, detail="you are unauthorised!")
        
        token = token.split(" ")[-1]

        data = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        user_id = data.get("_id")

        user = db.query(UserSchema).filter(UserSchema.id == user_id).first()
        if not user:
            raise HTTPException(401, detail="you are unauthorised!")

        return user

    except ExpiredSignatureError:
        raise HTTPException(401, detail="you are unauthorised!")

    except InvalidTokenError:
        raise HTTPException(401, detail="Invalid token!")

def current_user(request: Request):
    token = request.headers.get("authorization")
    if not token:
        raise HTTPException(401, detail="you are unauthorised!")
        
    token = token.split(" ")[-1]

    data = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM]
    )

    user_id = data.get("_id")
    
    return user_id