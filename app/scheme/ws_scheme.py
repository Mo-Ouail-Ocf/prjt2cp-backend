from typing import Union
from pydantic import BaseModel, Field, validator
from app.scheme.comment_scheme import CommentResponse, CommentRequest
from app.scheme.idea_scheme import IdeaRequest, IdeaResponse
from app.scheme.combined_idea_scheme import CombinedIdeaCreate, CombinedIdeaResponse


class ChatMessage(BaseModel):
    msg: str


class Message(BaseModel):
    # TODO: validator
    type: str = Field(pattern="chat|idea|combined_idea|comment")
    content: Union[ChatMessage, IdeaRequest, CombinedIdeaCreate, CommentRequest]


class ChatBroadCast(ChatMessage):
    user_id: int


class BroadCast(BaseModel):
    type: str = Field(pattern="chat|idea|combined_idea|comment")
    content: Union[ChatBroadCast, IdeaResponse, CombinedIdeaResponse, CommentResponse]
