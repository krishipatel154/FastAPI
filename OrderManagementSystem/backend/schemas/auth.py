from pydantic import BaseModel, Field, EmailStr
from typing import Annotated, Literal, Optional
from datetime import datetime

class UserSchema(BaseModel):
    firstname: Annotated[str, Field(max_length=100, min_length=3)]
    lastname: Annotated[str, Field(max_length=100, min_length=3)]
    email: EmailStr
    password: Annotated[str, Field(min_length=8, title="Password of the user")]
    role: Annotated[Literal["user", "admin", "vendor"], Field(title = "Role of the user")] = "user"

class UserResponseSchema(BaseModel):
    id: int
    firstname: str
    lastname: str | None
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UpdateUserSchema(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None

class ChangePassword(BaseModel):
    old_password: str
    new_password: Annotated[str, Field(min_length=8, title="Password of the user")]

class ForgotPasswordSchema(BaseModel):
    email: EmailStr
    new_password: Annotated[str, Field(min_length=8, title="Password of the user")]
    verify_password: Annotated[str, Field(min_length=8, title="Password of the user")]

class UserProfileSchema(BaseModel):
    firstname: str
    lastname: str | None
    email: EmailStr

class LoginSchema(BaseModel):
    email: EmailStr
    password: Annotated[str, Field(min_length=8, title="Password of the user")]

class LoginResponseSchema(BaseModel):
    email: EmailStr