from fastapi import APIRouter, Depends, status
from models.user import UserModel, UserResponseModel, LoginModel
from sqlalchemy.orm import Session
from utils.db import get_db
from controllers import user

user_router = APIRouter()

@user_router.post("/register", response_model=UserResponseModel, status_code=status.HTTP_201_CREATED)
def register(body: UserModel, db: Session = Depends(get_db)):
    return user.register(body, db)

@user_router.post("/login", status_code=status.HTTP_200_OK)
def login(body: LoginModel, db: Session = Depends(get_db)):
    return user.login(body, db)