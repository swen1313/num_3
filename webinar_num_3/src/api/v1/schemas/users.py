from datetime import datetime
from pydantic import BaseModel, UUID4, EmailStr

__all__ = (
    "UserLogin",
    "UserEmail",
    "UserCreate",
    "User",
)


class UserBase(BaseModel):
    username: str


class UserLogin(UserBase):
    password: str


class UserEmail(UserBase):
    email: EmailStr


class UserCreate(UserLogin, UserEmail):
    pass


class User(UserLogin, UserEmail):
    uuid: UUID4
    created_at: datetime
    is_superuser: bool