from fastapi import WebSocket
from sqlalchemy.orm import Session
from app.scheme.ws_scheme import BroadCast, ChatBroadCast, SysEvent, Vote
from app.scheme.combined_idea_scheme import CombinedIdeaCreate
from app.scheme.idea_scheme import IdeaCreate, IdeaUpdateWS
from app.scheme.comment_scheme import CommentCreate
from app.crud.idea_crud import create_idea, add_idea_vote, update_idea
from app.crud.combined_idea_crud import create_combined_idea
from app.crud.comment_crud import create_comment
from app.scheme.ws_scheme import Message


class IdeationRoom:
    def __init__(self, session_id: int):
        self.session_id = session_id
        self.active_users: list[WebSocket] = []
        self.ideas: list[int] = []

    async def connect_user(self, ws: WebSocket):
        await ws.accept()
        self.active_users.append(ws)

    async def broadcast(self, data: BroadCast):
        for user_ws in self.active_users:
            await user_ws.send_json(data.model_dump_json())

    def disconnect(self, ws: WebSocket):
        self.active_users.remove(ws)

    async def broadcast_sys_event(self, event: SysEvent):
        data = BroadCast(type="sys_event", content=event)
        await self.broadcast(data)

    async def broadcast_vote(self, idea_id: int, db: Session) -> bool:
        if idea_id not in self.ideas:
            return False

        add_idea_vote(db, idea_id)

        data = BroadCast(type="vote", content=Vote(idea_id=idea_id))
        await self.broadcast(data)

        return True

    async def broadcast_idea(self, idea: IdeaCreate, db: Session) -> bool:
        try:
            idea = create_idea(db, idea)
        except:
            return False

        data = BroadCast(type="idea", content=idea)

        self.ideas.append(idea.idea_id)
        await self.broadcast(data)

        return True

    async def broadcast_idea_update(self, idea: IdeaUpdateWS, db: Session) -> bool:
        if not idea.idea_id in self.ideas:
            return False

        try:
            idea = update_idea(db, idea.idea_id, idea)
        except:
            return False

        data = BroadCast(type="idea", content=idea)

        await self.broadcast(data)
        return True

    async def broadcast_combined_idea(
        self, combined_idea: CombinedIdeaCreate, db: Session
    ) -> bool:
        if combined_idea.source_idea_id not in self.ideas:
            return False

        if combined_idea.combined_idea_id not in self.ideas:
            return False

        try:
            combined_idea = create_combined_idea(db, combined_idea)
        except:
            return False

        data = BroadCast(type="combined_idea", content=combined_idea)
        await self.broadcast(data)

        return True

    async def broadcast_comment(self, comment: CommentCreate, db: Session) -> bool:
        if comment.idea_id not in self.ideas:
            return False

        try:
            comment = create_comment(db, comment)
        except:
            return False

        data = BroadCast(type="comment", content=comment)
        await self.broadcast(data)

        return True

    async def broadcast_msg(self, user_id: int, message: str):
        content = ChatBroadCast(user_id=user_id, msg=message)
        data = BroadCast(type="chat", content=content)

        await self.broadcast(data)

    @staticmethod
    async def send_msg(ws: WebSocket, msg: str):
        data = Message(type="chat", content=ChatBroadCast(msg=msg, user_id=0))
        await ws.send_json(data.model_dump_json())
