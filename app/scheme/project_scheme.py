from pydantic import BaseModel
from datetime import datetime
from app.scheme.user_scheme import User


class ProjectBase(BaseModel):
    id: int


class ProjectCreate(ProjectBase):
    title: str
    description: str
    owner_id: int


class ProjectResponse(ProjectCreate):
    status: str
    creation_date: datetime

    resource_id: int


class Project(ProjectResponse):
    owner: User
    project_users: list[User]
    # sessions
    # resource

    class Config:
        from_attributes = True
