from typing import Union, Optional
from pydantic import BaseModel, Field
from app.scheme.comment_scheme import CommentResponse, CommentRequest
from app.scheme.idea_scheme import IdeaRequest, IdeaResponse, IdeaUpdateWS
from app.scheme.combined_idea_scheme import CombinedIdeaCreate, CombinedIdeaResponse


class ChatMessage(BaseModel):
    msg: str


class Vote(BaseModel):
    # votes is anonymous, so no user id
    idea_id: int


class Message(BaseModel):
    type: str = Field(pattern="chat|idea|idea_update|combined_idea|comment|vote|start")
    content: Optional[
        Union[
            ChatMessage,
            IdeaRequest,
            IdeaUpdateWS,
            CombinedIdeaCreate,
            CommentRequest,
            Vote,
        ]
    ]


class ChatBroadCast(ChatMessage):
    user_id: int


class SysEvent(BaseModel):
    user_id: Optional[int] = None
    event: str = Field(pattern="start|join|quit")


class BroadCast(BaseModel):
    type: str = Field(pattern="chat|idea|combined_idea|comment|vote|sys_event")
    content: Union[
        ChatBroadCast,
        IdeaResponse,
        CombinedIdeaResponse,
        CommentResponse,
        Vote,
        SysEvent,
    ]
