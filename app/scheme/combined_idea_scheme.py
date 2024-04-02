from pydantic import BaseModel


class CombinedIdeaBase(BaseModel):
    pass


class CombinedIdeaCreate(CombinedIdeaBase):
    combined_idea_id: int
    source_idea_id: int


class CombinedIdeaResponse(CombinedIdeaCreate):
    class Config:
        from_attributes = True
