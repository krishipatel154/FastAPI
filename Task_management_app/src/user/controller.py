from src.user.dtos import UserSchema, LoginSchema
from sqlalchemy.orm import Session
from src.user.models import UserModel
from fastapi import HTTPException, Request
from pwdlib import PasswordHash
from src.utils.settings import settings
from datetime import datetime, timedelta, timezone
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
import jwt


password_hash = PasswordHash.recommended()

def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(plain_password, hash_password):
    return password_hash.verify(plain_password, hash_password)

def register(body: UserSchema, db: Session):
    print(body)
    # username validation
    is_user = db.query(UserModel).filter(UserModel.username == body.username).first()
    if is_user:
        raise HTTPException(400, detail="Username already exist!")
    
    # email validation
    is_user = db.query(UserModel).filter(UserModel.email == body.email).first()
    if is_user:
        raise HTTPException(400, detail="Email already exist!")
    
    # password hash
    hash_password = get_password_hash(body.password)

    user = UserModel(name=body.name, username=body.username, hash_password=hash_password, email=body.email)
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def login(body: LoginSchema, db: Session):
    user = db.query(UserModel).filter(UserModel.username == body.username).first()
    if not user:
        raise HTTPException(400, detail="Username not exist!")

    if not verify_password(body.password, user.hash_password):
        raise HTTPException(400, detail="Username not exist!")
    
    exp_time = datetime.now(timezone.utc) + timedelta(minutes=settings.EXP_TIME)
    
    token = jwt.encode({"_id": user.id, "exp": exp_time}, settings.SECRET_KRY, settings.ALGORITHM)

    return {
        "message":"Registration done successfully!",
        "payload": body,
        "token": token
    }

def is_authenticated(request: Request, db: Session):
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
        raise HTTPException(401, detail="Token expired!")

    except InvalidTokenError:
        raise HTTPException(401, detail="Invalid token!")