from pydantic import BaseModel
from app.scheme.idea_scheme import IdeaRequest


class CombinedIdeaBase(BaseModel):
    pass


class CombinedIdeaCreate(CombinedIdeaBase):
    combined_idea_id: int
    source_idea_id: int


class CombinedIdeaResponse(CombinedIdeaCreate):
    class Config:
        from_attributes = True


class CombinedIdeaWSCreate(BaseModel):
    idea: IdeaRequest
    source_idea_ids: list[int]
