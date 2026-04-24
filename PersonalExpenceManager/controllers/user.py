from fastapi import HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from schemas.user import UserSchema
from models.user import UserModel, LoginModel
from pwdlib import PasswordHash
from utils.settings import settings
from datetime import timedelta, datetime
import jwt

password_hash = PasswordHash.recommended()

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)


def register(body: UserModel, db: Session):
    # validate username
    is_user = db.query(UserSchema).filter(UserSchema.username == body.username).first()
    if is_user:
        raise HTTPException(400, detail="username already exist!")
    
    # validate email
    is_user = db.query(UserSchema).filter(UserSchema.email == body.email).first()
    if is_user:
        raise HTTPException(400, detail="email already exist!")
    
    hash_password = get_password_hash(body.password)

    user = UserSchema(
        name = body.name, username = body.username, email = body.email, password = hash_password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def login(body: LoginModel, db: Session):
    # validate username
    user = db.query(UserSchema).filter(UserSchema.username == body.username).first()
    if not user:
        raise HTTPException(404, detail="Invalid credantials!")
    
    if not verify_password(body.password, user.password):
        raise HTTPException(404, detail="Invalid credantials!")
    
    expire  = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    token = jwt.encode({"_id": user.id, "exp": expire}, settings.SECRET_KEY, settings.ALGORITHM)

    return { 
        "access_token": token,
        "token_type": "bearer"
    }