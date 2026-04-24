from fastapi import Request, HTTPException, Depends
from sqlalchemy.orm import Session
from jwt import InvalidTokenError, ExpiredSignatureError
from src.utils.settings import settings
from src.user.models import UserModel
from src.utils.db import get_db
import jwt

def is_authenticated(request: Request, db: Session = Depends(get_db)):
    try:
        token = request.headers.get("authorization")
        if not token:
            raise HTTPException(401, detail="you are unauthorised!")
        
        token = token.split(" ")[-1]

        data = jwt.decode(
            token,
            settings.SECRET_KRY,
            algorithms=[settings.ALGORITHM]
        )

        user_id = data.get("_id")

        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise HTTPException(401, detail="you are unauthorised!")

        return user

    except ExpiredSignatureError:
        raise HTTPException(401, detail="you are unauthorised!")

    except InvalidTokenError:
        raise HTTPException(401, detail="Invalid token!")