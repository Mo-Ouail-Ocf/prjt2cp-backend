from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import List, Optional


class UserBase(BaseModel):
    user_id: int
    name: str
    email: str
    image: Optional[str] = None

    class Config:
        from_attributes = True


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
    photo: Optional[str] = None

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
    resource: Optional[ResourceDisplay] = None
    participants: List[ProjectUserDisplay] = []

    class Config:
        from_attributes = True


class ProjectInvitationCreate(BaseModel):
    email: EmailStr


class ProjectInvitationResponse(BaseModel):
    message: str


class PendingInvitationInfo(BaseModel):
    project_id: int
    project_title: str
    project_description: str
    creator_name: str
    creator_email: EmailStr
    invitation_time: datetime
    creator_image: str

    class Config:
        from_attributes = True


class UpdateInvitation(BaseModel):
    status: bool

    class Config:
        from_attributes = True


class SessionSchema(BaseModel):
    session_id: int
    project_id: int
    title: str
    description: Optional[str]
    ideation_technique: str
    start_time: datetime
    session_status: str
    objectives: Optional[str]
    round_time: int
    nb_rounds: int

    class Config:
        from_attributes = True
