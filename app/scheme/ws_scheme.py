from typing import Union, Optional
from pydantic import BaseModel, Field, ConfigDict
from app.scheme.comment_scheme import CommentResponse, CommentRequest
from app.scheme.final_decision_scheme import (
    FinalDecisionRequest,
    FinalDecisionResponse,
)
from app.scheme.idea_scheme import IdeaRequest, IdeaResponse, IdeaUpdateWS
from app.scheme.combined_idea_scheme import CombinedIdeaCreate, CombinedIdeaResponse
from fastapi import WebSocket


class SysEvent(BaseModel):
    event: str = Field(pattern="join|joined|start|close|quit")


class ChatMessage(BaseModel):
    msg: str


class Vote(BaseModel):
    # votes is anonymous, so no user id
    idea_id: int


class Message(BaseModel):
    type: str = Field(
        pattern="chat|idea|idea_update|combined_idea|comment|vote|sys_event|final_decision"
    )
    content: Optional[
        Union[
            ChatMessage,
            IdeaRequest,
            IdeaUpdateWS,
            CombinedIdeaCreate,
            CommentRequest,
            SysEvent,
            # order is importent
            FinalDecisionRequest,
            Vote,
        ]
    ]


class ChatBroadCast(ChatMessage):
    user_id: int


class SysEventBroadcast(SysEvent):
    users: list[int]


class BroadCast(BaseModel):
    type: str = Field(
        pattern="chat|idea|combined_idea|comment|vote|sys_event|final_decision"
    )
    content: Union[
        ChatBroadCast,
        IdeaResponse,
        CombinedIdeaResponse,
        CommentResponse,
        Vote,
        SysEventBroadcast,
        FinalDecisionResponse,
    ]


class WSUser(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    ws: WebSocket
    user_id: int
    votes: list[int] = []  # keep track of user votes
