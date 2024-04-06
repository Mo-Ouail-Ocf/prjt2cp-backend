from pydantic import BaseModel, AnyHttpUrl
from datetime import datetime


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    name: str
    pfp: AnyHttpUrl


class UserResponse(UserBase):
    id: int
    name: str
    pfp: AnyHttpUrl


class User(UserBase):
    id: int
    name: str
    pfp: AnyHttpUrl
    last_activity: datetime

    class Config:
        from_attributes = True
