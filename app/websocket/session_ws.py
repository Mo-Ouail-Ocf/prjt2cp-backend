from fastapi import WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from app.crud.user_crud import get_user_by_id
from app.scheme.combined_idea_scheme import CombinedIdeaCreate
from app.scheme.idea_scheme import IdeaCreate
from app.scheme.comment_scheme import CommentCreate
from app.scheme.ws_scheme import ChatMessage
from app.websocket.room_manager import room_manager
from app.scheme.ws_scheme import Message
from app.crud.session_crud import is_moderator
from app.crud.idea_crud import create_idea
from app.crud.combined_idea_crud import create_combined_idea
from app.crud.comment_crud import create_comment


async def session_ws(ws: WebSocket, session_id: int, user_id: int, db: Session):
    ideation_room = room_manager.get_room(session_id)

    await ideation_room.connect_user(ws)

    user = get_user_by_id(db, user_id)
    await ideation_room.broadcast_msg(0, f"{user.name} joined the session")

    is_mod = is_moderator(db, session_id, user_id)

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
                idea = create_idea(db, idea)
                await ideation_room.broadcast_idea(idea)
            elif data.type == "comment":
                comment = CommentCreate(**data.content.model_dump(), author_id=user_id)
                comment = create_comment(db, comment)
                await ideation_room.broadcast_comment(comment)
            elif data.type == "combined_idea":
                if is_mod:
                    combined_idea = CombinedIdeaCreate.model_validate(data.content)
                    combined_idea = create_combined_idea(db, combined_idea)
                    await ideation_room.broadcast_combined_idea(combined_idea)
                else:
                    await ideation_room.broadcast_msg(
                        0, f"{user.name}, only moderators can create combined ideas!"
                    )
            else:
                msg = ChatMessage.model_validate(data.content).msg
                await ideation_room.broadcast_msg(user_id, msg)

    except WebSocketDisconnect:
        msg = f"{user.name} has left the session"

    finally:
        ideation_room.disconnect(ws)

        if len(ideation_room.active_users) == 0:
            room_manager.delete_room(ideation_room.session_id)
        else:
            await ideation_room.broadcast_msg(0, msg)
