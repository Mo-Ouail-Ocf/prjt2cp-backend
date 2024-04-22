from fastapi import WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from app.crud.user_crud import get_user_by_id
from app.scheme.combined_idea_scheme import CombinedIdeaCreate
from app.scheme.idea_scheme import IdeaCreate
from app.scheme.comment_scheme import CommentCreate
from app.scheme.ws_scheme import ChatMessage, Vote
from app.websocket.room_manager import room_manager
from app.scheme.ws_scheme import Message
from app.crud.session_crud import is_moderator
from app.websocket.ideation_room import send_msg


async def session_ws(ws: WebSocket, session_id: int, user_id: int, db: Session):
    ideation_room = room_manager.get_room(session_id)

    await ideation_room.connect_user(ws)

    user = get_user_by_id(db, user_id)
    await ideation_room.broadcast_msg(0, f"{user.name} joined the session")

    is_mod = is_moderator(db, session_id, user_id)
    votes: list[int] = []  # keep track of user votes

    msg = f"{user.name} kicked for rule violation"

    try:
        while True:
            data = await ws.receive_json()
            data = Message(**data)

            if data.type == "idea":
                idea = IdeaCreate(
                    **data.content.model_dump(),
                    submitter_id=user_id,
                    session_id=session_id,
                )

                if not await ideation_room.broadcast_idea(idea, db):
                    await send_msg(ws, "Counldn't create idea.")

            elif data.type == "comment":
                comment = CommentCreate(**data.content.model_dump(), author_id=user_id)

                if not await ideation_room.broadcast_comment(comment, db):
                    await send_msg(ws, "Counldn't create comment.")

            elif data.type == "combined_idea":
                if is_mod:
                    combined_idea = CombinedIdeaCreate.model_validate(data.content)

                    if not await ideation_room.broadcast_combined_idea(
                        combined_idea, db
                    ):
                        await send_msg(ws, "Counldn't create combined idea.")
                else:
                    await send_msg(ws, "Only moderators can combine ideas!")

            elif data.type == "vote":
                idea_id = Vote.model_validate(data.content).idea_id

                if idea_id in votes:
                    await send_msg(ws, "Already voted for this idea!")
                    continue

                if await ideation_room.broadcast_vote(idea_id, db):
                    votes.append(idea_id)
                else:
                    await send_msg(ws, "Couldn't vote!")

            else:
                msg = ChatMessage.model_validate(data.content).msg

                await ideation_room.broadcast_msg(user_id, msg)

    except WebSocketDisconnect:
        msg = f"{user.name} has left the session"

    finally:
        ideation_room.disconnect(ws)

        if len(ideation_room.active_users) == 0:
            room_manager.delete_room(db, ideation_room.session_id)
        else:
            await ideation_room.broadcast_msg(0, msg)
