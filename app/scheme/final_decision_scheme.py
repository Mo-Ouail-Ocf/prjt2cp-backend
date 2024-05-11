from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class FinalDecisionRequest(BaseModel):
    rationale: str
    idea_id: int


class FinalDecisionCreate(FinalDecisionRequest):
    session_id: int


class FinalDecisionResponse(FinalDecisionCreate):
    decision_id: int
    decision_date: datetime
    new_session_id: Optional[int]=None

    class Config:
        from_attributes = True
