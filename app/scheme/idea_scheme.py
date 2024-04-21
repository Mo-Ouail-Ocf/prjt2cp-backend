from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class IdeaBase(BaseModel):
    pass


class IdeaRequest(IdeaBase):
    content: str
    details: Optional[str]
    parent_idea_id: Optional[int]


class IdeaCreate(IdeaRequest):
    submitter_id: int
    session_id: int


class IdeaResponse(IdeaCreate):
    idea_id: int
    creation_date: datetime
    votes: Optional[int]

    class Config:
        from_attributes = True
