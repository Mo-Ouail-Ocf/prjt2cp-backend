from pydantic import BaseModel
from datetime import datetime


class CommentBase(BaseModel):
    pass


class CommentRequest(CommentBase):
    idea_id: int
    content: str


class CommentCreate(CommentRequest):
    author_id: int


class CommentResponse(CommentCreate):
    comment_id: int
    creation_date: datetime

    class Config:
        from_attributes = True
