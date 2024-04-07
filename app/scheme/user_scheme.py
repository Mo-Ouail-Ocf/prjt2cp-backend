from pydantic import BaseModel, AnyHttpUrl
from datetime import datetime


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    name: str
    pfp: AnyHttpUrl
    google_refresh_token: str


class UserResponse(UserBase):
    id: int
    name: str
    pfp: AnyHttpUrl


class User(UserCreate):
    id: int
    last_activity: datetime
    hash_password: str

    class Config:
        from_attributes = True
