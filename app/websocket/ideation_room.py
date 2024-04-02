from typing import List
from fastapi import WebSocket
from app.scheme.ws_scheme import BroadCast, ChatBroadCast
from app.models import Idea, CombinedIdea, Comment
from app.scheme.combined_idea_scheme import CombinedIdeaResponse
from app.scheme.idea_scheme import IdeaResponse
from app.scheme.comment_scheme import CommentResponse


class IdeationRoom:
    def __init__(self, session_id: int):
        self.session_id = session_id
        self.active_users: List[WebSocket] = []

    async def connect_user(self, ws: WebSocket):
        await ws.accept()
        self.active_users.append(ws)

    async def broadcast(self, data: BroadCast):
        for user_ws in self.active_users:
            await user_ws.send_json(data.model_dump_json())

    def disconnect(self, ws: WebSocket):
        self.active_users.remove(ws)

    async def broadcast_idea(self, idea: Idea):
        content = IdeaResponse(
            content=idea.content,
            details=idea.details,
            session_id=idea.session_id,
            parent_idea_id=idea.parent_idea_id,
            submitter_id=idea.submitter_id,
            idea_id=idea.idea_id,
            creation_data=idea.creation_date,
        )
        data = BroadCast(type="idea", content=content)

        await self.broadcast(data)

    async def broadcast_combined_idea(self, combined_idea: CombinedIdea):
        content = CombinedIdeaResponse(
            combined_idea_id=combined_idea.combined_idea_id,
            source_idea_id=combined_idea.source_idea_id,
        )
        data = BroadCast(type="combined_idea", content=content)

        await self.broadcast(data)

    async def broadcast_comment(self, comment: Comment):
        content = CommentResponse(
            author_id=comment.author_id,
            idea_id=comment.idea_id,
            content=comment.content,
            comment_id=comment.comment_id,
            creation_date=comment.creation_date,
        )
        data = BroadCast(type="comment", content=content)

        await self.broadcast(data)

    async def broadcast_msg(self, user_id: int, message: str):
        content = ChatBroadCast(user_id=user_id, msg=message)
        data = BroadCast(type="chat", content=content)

        await self.broadcast(data)
