from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class IdeaBase(BaseModel):
    pass


class IdeaRequest(IdeaBase):
    content: str
    details: Optional[str]
    parent_idea_id: Optional[int]
    idea_type: str = Field(pattern="^(?:|expended|combined)$", default="") 



class IdeaCreate(IdeaRequest):
    submitter_id: int
    session_id: int


class IdeaUpdate(IdeaBase):
    content: Optional[str]
    details: Optional[str]
    deleted: bool = False


class IdeaUpdateWS(IdeaUpdate):
    idea_id: int
    idea_type: str = "refined"


class IdeaResponse(IdeaCreate):
    idea_id: int
    creation_date: datetime
    votes: int
    deleted: bool
    idea_type: str = Field(pattern="^(?:|expended|combined|refined)$") 

    class Config:
        from_attributes = True
