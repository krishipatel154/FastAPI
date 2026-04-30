from fastapi import APIRouter, Depends, Request
from controllers import auth
from schemas.auth import UserSchema, UserResponseSchema, UserProfileSchema, LoginSchema, UpdateUserSchema, ChangePassword, ForgotPasswordSchema
from sqlalchemy.orm import Session
from utils.helper import is_authenticated, require_role
from utils.db import get_db

auth_router = APIRouter()

@auth_router.post("/register", response_model=UserResponseSchema)
async def register(body: UserSchema, db:Session = Depends(get_db)):
    return auth.register(body, db)

@auth_router.post("/login")
async def login(body: LoginSchema, db:Session = Depends(get_db)):
    return auth.login(body, db)

# get user profile
@auth_router.get("/profile", response_model=UserProfileSchema)
async def get_profile(db:Session = Depends(get_db), current_user = Depends(require_role(["admin", "user", "vendor"]))):
    return auth.get_profile(db, current_user)

# update profile
@auth_router.patch("/profile")
async def update_profile(body:UpdateUserSchema, db:Session = Depends(get_db), current_user = Depends(require_role(["admin", "user", "vendor"]))):
    return auth.update_profile(body, db, current_user)

# change password
@auth_router.patch("/change-password")
async def chnage_password(body:ChangePassword, db:Session = Depends(get_db), current_user = Depends(require_role(["admin", "user", "vendor"]))):
    return auth.chnage_password(body, db, current_user)

# forgot password
@auth_router.patch("/forgot-password")
async def forgot_password(body:ForgotPasswordSchema, db:Session = Depends(get_db)):
    return auth.forgot_password(body, db)

@auth_router.delete("/")
async def delete_user(id:int, db:Session = Depends(get_db), user = Depends(require_role(["admin"]))):
    return auth.delete_user(id, db)
