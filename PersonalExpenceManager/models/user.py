from pydantic import BaseModel, Field
from typing import Annotated

class UserModel(BaseModel):
    name: Annotated[str, Field(max_length=50, min_length=3, title="Name of the user")]
    username: Annotated[str, Field(max_length=50, min_length=3, title="Username")]
    email: Annotated[str, Field(max_length=50, title="Email of the user")]
    password: Annotated[str, Field(min_length=8, title="Password of the user")]

class UserResponseModel(BaseModel):
    name: str
    username: str
    email: str

class LoginModel(BaseModel):
    username: Annotated[str, Field(max_length=50, min_length=3, title="Username")]
    password: Annotated[str, Field(min_length=8, title="Password of the user")]

class Token(BaseModel):
    access_token: str
    token_type: str