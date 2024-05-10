from fastapi import WebSocket, WebSocketDisconnect
from pydantic import ValidationError
from sqlalchemy.orm import Session
from app.scheme.combined_idea_scheme import CombinedIdeaWSCreate
from app.scheme.final_decision_scheme import FinalDecisionRequest
from app.scheme.idea_scheme import IdeaRequest, IdeaUpdateWS
from app.scheme.comment_scheme import CommentRequest
from app.scheme.ws_scheme import ChatMessage, SysEvent, Vote
from app.websocket.room_manager import room_manager
from app.scheme.ws_scheme import Message


async def session_ws(ws: WebSocket, session_id: int, user_id: int, db: Session):
    ideation_room = room_manager.get_room(session_id, db)
    user = await ideation_room.connect_user(ws, user_id)

    try:
        while True:
            data = await ws.receive_json()
            data = Message(**data)

            if data.type == "sys_event":
                event = SysEvent.model_validate(data.content)
                await ideation_room.broadcast_sys_event(user, event, db)

            elif data.type == "idea":
                idea = IdeaRequest.model_validate(data.content)

                if not await ideation_room.broadcast_idea(idea, user, db):
                    await ideation_room.send_msg(ws, "Counldn't create idea.")

            elif data.type == "idea_update":
                idea = IdeaUpdateWS.model_validate(data.content)

                if not await ideation_room.broadcast_idea_update(user, idea, db):
                    await ideation_room.send_msg(ws, "Counldn't update idea.")

            elif data.type == "comment":
                comment = CommentRequest.model_validate(data.content)

                if not await ideation_room.broadcast_comment(user, comment, db):
                    await ideation_room.send_msg(ws, "Counldn't create comment.")

            elif data.type == "combined_idea":
                combined_idea = CombinedIdeaWSCreate.model_validate(data.content)

                if not await ideation_room.broadcast_combined_idea(
                    user, combined_idea, db
                ):
                    await ideation_room.send_msg(ws, "Counldn't create combined idea.")

            elif data.type == "vote":
                idea_id = Vote.model_validate(data.content).idea_id

                if not await ideation_room.broadcast_vote(user, idea_id, db):
                    await ideation_room.send_msg(ws, "Couldn't vote!")

            elif data.type == "final_decision":
                final_decision = FinalDecisionRequest.model_validate(data.content)

                if not await ideation_room.broadcast_final_decision(
                    user, final_decision, db
                ):
                    await ideation_room.send_msg(ws, "Counldn't create final decision.")

            else:
                msg = ChatMessage.model_validate(data.content).msg

                await ideation_room.broadcast_msg(user_id, msg)

    except ValidationError:
        await ideation_room.send_msg(ws, "Illigal action")

    except WebSocketDisconnect:
        pass

    finally:
        await ideation_room.remove_user(user)

        if len(ideation_room.active_users) == 0:
            room_manager.delete_room(db, ideation_room.session_id)
        else:
            await ideation_room.broadcast_sys_event(user, SysEvent(event="quit"))
