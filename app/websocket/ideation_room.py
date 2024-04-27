from fastapi import WebSocket, status, WebSocketException
from sqlalchemy.orm import Session
from app.scheme.final_decision_scheme import FinalDecisionCreate, FinalDecisionRequest
from app.scheme.ws_scheme import (
    WSUser,
    BroadCast,
    ChatBroadCast,
    SysEvent,
    SysEventBroadcast,
    Vote,
    Message,
)
from app.scheme.combined_idea_scheme import CombinedIdeaCreate
from app.scheme.idea_scheme import IdeaCreate, IdeaRequest, IdeaUpdateWS
from app.scheme.comment_scheme import CommentCreate, CommentRequest
from app.crud.idea_crud import create_idea, add_idea_vote, update_idea
from app.crud.combined_idea_crud import create_combined_idea
from app.crud.comment_crud import create_comment
from app.crud.final_decision_crud import create_final_decision
from app.crud.session_crud import start_session
from typing import Optional


class IdeationRoom:
    def __init__(self, session_id: int, moderators: list[int]):
        self.session_id: int = session_id
        self.moderators: list[int] = moderators
        self.active_users: list[WSUser] = []
        self.ideas: list[int] = []
        self.started: bool = False

    async def connect_user(self, ws: WebSocket, user_id: int):
        user = WSUser(ws=ws, user_id=user_id)
        content = SysEventBroadcast(
            event="joined", users=[user.user_id for user in self.active_users]
        )

        await ws.accept()
        await ws.send_json(
            BroadCast(type="sys_event", content=content).model_dump_json()
        )
        await self.broadcast_sys_event(user, SysEvent(event="join"))

        self.active_users.append(user)
        return user

    async def broadcast(self, data: BroadCast):
        for user in self.active_users:
            await user.ws.send_json(data.model_dump_json())

    def disconnect(self, user: WSUser):
        if user in self.active_users:
            self.active_users.remove(user)

    async def broadcast_sys_event(
        self, user: WSUser, event: SysEvent, db: Optional[Session] = None
    ):
        if event.event in ["start", "close"] and not user.user_id in self.moderators:
            return await self.send_msg(
                user.ws, "Only moderators can create sys events!"
            )

        if event.event == "start":
            if db:
                start_session(db, self.session_id)
                self.started = True
            else:
                raise WebSocketException(code=status.WS_1011_INTERNAL_ERROR)

        content = SysEventBroadcast(event=event.event, users=[user.user_id])
        data = BroadCast(type="sys_event", content=content)
        await self.broadcast(data)

        if event.event == "close":
            for user in self.active_users:
                await self.disconnect(user)

    async def broadcast_vote(self, user: WSUser, idea_id: int, db: Session) -> bool:
        if idea_id in user.votes:
            await self.send_msg(user.ws, "Already voted for this idea!")
            return True

        if idea_id not in self.ideas:
            return False

        add_idea_vote(db, idea_id)
        user.votes.append(idea_id)

        data = BroadCast(type="vote", content=Vote(idea_id=idea_id))
        await self.broadcast(data)

        return True

    async def broadcast_idea(
        self, idea: IdeaRequest, user: WSUser, db: Session
    ) -> bool:
        if not self.started:  # we only need this here because others depend on this
            return False

        idea = IdeaCreate(
            **idea.model_dump(),
            submitter_id=user.user_id,
            session_id=self.session_id,
        )

        try:
            idea = create_idea(db, idea)
        except:
            return False

        data = BroadCast(type="idea", content=idea)

        self.ideas.append(idea.idea_id)
        await self.broadcast(data)

        return True

    async def broadcast_idea_update(
        self, user: WSUser, idea: IdeaUpdateWS, db: Session
    ) -> bool:
        if not user.user_id in self.moderators:
            await self.send_msg(user.ws, "Only moderators can refine ideas!")
            return True

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
        self, user: WSUser, combined_idea: CombinedIdeaCreate, db: Session
    ) -> bool:
        if not user.user_id in self.moderators:
            await self.send_msg(user.ws, "Only moderators can combine ideas!")
            return True

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

    async def broadcast_comment(
        self, user: WSUser, comment: CommentRequest, db: Session
    ) -> bool:
        if comment.idea_id not in self.ideas:
            return False

        comment = CommentCreate(**comment.model_dump(), author_id=user.user_id)

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

    async def broadcast_final_decision(
        self, user: WSUser, final_decision: FinalDecisionRequest, db: Session
    ) -> bool:
        if user.user_id not in self.moderators:
            await self.send_msg(user.ws, "Only moderators can create final decisions!")
            return True

        if final_decision.idea_id not in self.ideas:
            return False

        final_decision = FinalDecisionCreate(
            **final_decision.model_dump(), session_id=self.session_id
        )

        try:
            final_decision = create_final_decision(db, final_decision)
        except:
            return False

        data = BroadCast(type="final_decision", content=final_decision)
        await self.broadcast(data)

        return True

    @staticmethod
    async def send_msg(ws: WebSocket, msg: str):
        data = Message(type="chat", content=ChatBroadCast(msg=msg, user_id=0))
        await ws.send_json(data.model_dump_json())
