from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    name: str
    pfp: bytes


class UserResponse(UserBase):
    id: int
    name: str


class User(UserBase):
    id: int
    name: str
    pfp: bytes
    last_activity: datetime

    class Config:
        orm_mode = True
