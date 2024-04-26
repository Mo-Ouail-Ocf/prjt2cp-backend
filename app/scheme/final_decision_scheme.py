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

    class Config:
        from_attributes = True
