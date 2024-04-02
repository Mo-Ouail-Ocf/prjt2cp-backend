from datetime import datetime
from pydantic import BaseModel, EmailStr
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
        from_attributes = True


class ResourceDisplay(BaseModel):
    resource_id: int
    name: str
    type: str
    level: Optional[str] = None
    description: Optional[str] = None
    photo: Optional[str] = None  # Assuming this is how you store binary data

    class Config:
        from_attributes = True


class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: str
    resource_id: int


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
    resource: Optional[ResourceDisplay] = None  # Include the resource
    participants: List[ProjectUserDisplay] = []

    class Config:
        from_attributes = True


class ProjectInvitationCreate(BaseModel):
    email: EmailStr


class ProjectInvitationResponse(BaseModel):
    message: str


class PendingInvitationInfo(BaseModel):
    project_title: str
    project_description: str
    creator_name: str
    creator_email: EmailStr

    class Config:
        from_attributes = True
