from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.scheme.combined_idea_scheme import CombinedIdeaResponse
from app.scheme.comment_scheme import CommentResponse
from app.scheme.idea_scheme import IdeaResponse


class SessionCreate(BaseModel):
    title: str
    description: Optional[str] = None
    ideation_technique: str = Field(pattern="brain_writing|brain_storming")
    objectives: Optional[str] = None
    round_time: int
    nb_rounds: int = 1


class SessionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    objectives: Optional[str] = None


class SessionResponse(SessionCreate):
    session_id: int
    session_status: str = Field(pattern="open|started|colsed")
    start_time: datetime
    project_id: int

    class Config:
        from_attributes = True


class SessionExport(BaseModel):
    metadata: SessionResponse
    ideas: list[IdeaResponse]
    comments: list[CommentResponse]
    combined_ideas: list[CombinedIdeaResponse]
