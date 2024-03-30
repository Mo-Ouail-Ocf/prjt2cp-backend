from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

class UserBase(BaseModel):
    user_id: int
    name: str
    email: str
    image: Optional[str] = None

class ProjectUserDisplay(BaseModel):
    user: UserBase
    role: str
    invitation_status: str

    class Config:
        orm_mode = True

class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: str
    owner_id: int

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class ProjectDisplay(BaseModel):
    project_id: int
    title: str
    description: Optional[str] = None
    status: str
    creation_date: datetime
    owner_id: int
    participants: List[ProjectUserDisplay] = []

    class Config:
        orm_mode = True
