from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class SessionCreate(BaseModel):
    title: str
    description: Optional[str] = None
    ideation_technique: str = Field(pattern="brain_writing|brain_storming")
    objectives: Optional[str] = None


class SessionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    session_status: str = Field(pattern="open|colsed")
    objectives: Optional[str] = None


class SessionResponse(SessionCreate):
    session_id: int
    session_status: str
    start_time: datetime
    project_id: int

    class Config:
        from_attributes = True
