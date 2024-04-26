from fastapi import WebSocket, WebSocketDisconnect
from pydantic import ValidationError
from sqlalchemy.orm import Session
from app.scheme.combined_idea_scheme import CombinedIdeaCreate
from app.scheme.final_decision_scheme import FinalDecisionRequest
from app.scheme.idea_scheme import IdeaRequest, IdeaUpdateWS
from app.scheme.comment_scheme import CommentRequest
from app.scheme.ws_scheme import ChatMessage, SysEvent, SysEventBroadcast, Vote
from app.websocket.room_manager import room_manager
from app.scheme.ws_scheme import Message
from app.crud.session_crud import is_moderator


async def session_ws(ws: WebSocket, session_id: int, user_id: int, db: Session):
    ideation_room = room_manager.get_room(session_id)

    await ideation_room.connect_user(ws)

    await ideation_room.broadcast_sys_event(
        SysEventBroadcast(event="join", user_id=user_id)
    )

    is_mod = is_moderator(db, session_id, user_id)
    votes: list[int] = []  # keep track of user votes

    try:
        while True:
            data = await ws.receive_json()
            data = Message(**data)

            if data.type == "sys_event":
                if is_mod:
                    event = SysEvent.model_validate(data.content)

                    if not await ideation_room.broadcast_sys_event(
                        SysEventBroadcast(event=event.event), db
                    ):
                        await ideation_room.send_msg(ws, "Counldn't create sys event.")
                else:
                    await ideation_room.send_msg(
                        ws, "Only moderators can create sys events!"
                    )

            elif data.type == "idea":
                idea = IdeaRequest.model_validate(data.content)

                if not await ideation_room.broadcast_idea(
                    idea, user_id, session_id, db
                ):
                    await ideation_room.send_msg(ws, "Counldn't create idea.")

            elif data.type == "idea_update":
                if is_mod:
                    idea = IdeaUpdateWS.model_validate(data.content)

                    if not await ideation_room.broadcast_idea_update(idea, db):
                        await ideation_room.send_msg(ws, "Counldn't update idea.")
                else:
                    await ideation_room.send_msg(
                        ws, "Only moderators can refine ideas!"
                    )

            elif data.type == "comment":
                comment = CommentRequest.model_validate(data.content)

                if not await ideation_room.broadcast_comment(comment, user_id, db):
                    await ideation_room.send_msg(ws, "Counldn't create comment.")

            elif data.type == "combined_idea":
                if is_mod:
                    combined_idea = CombinedIdeaCreate.model_validate(data.content)

                    if not await ideation_room.broadcast_combined_idea(
                        combined_idea, db
                    ):
                        await ideation_room.send_msg(
                            ws, "Counldn't create combined idea."
                        )
                else:
                    await ideation_room.send_msg(
                        ws, "Only moderators can combine ideas!"
                    )

            elif data.type == "vote":
                idea_id = Vote.model_validate(data.content).idea_id

                if idea_id in votes:
                    await ideation_room.send_msg(ws, "Already voted for this idea!")
                    continue

                if await ideation_room.broadcast_vote(idea_id, db):
                    votes.append(idea_id)
                else:
                    await ideation_room.send_msg(ws, "Couldn't vote!")

            elif data.type == "final_decision":
                if is_mod:
                    final_decision = FinalDecisionRequest.model_validate(data.content)

                    if not await ideation_room.broadcast_final_decision(
                        final_decision, db
                    ):
                        await ideation_room.send_msg(
                            ws, "Counldn't create final decision."
                        )

                else:
                    await ideation_room.send_msg(
                        ws, "Only moderators can create final decisions!"
                    )

            else:
                msg = ChatMessage.model_validate(data.content).msg

                await ideation_room.broadcast_msg(user_id, msg)

    # except ValidationError:
    #     await ideation_room.send_msg(ws, "Illigal action")

    except WebSocketDisconnect:
        pass

    finally:
        ideation_room.disconnect(ws)

        if len(ideation_room.active_users) == 0:
            room_manager.delete_room(db, ideation_room.session_id)
        else:
            await ideation_room.broadcast_sys_event(
                SysEventBroadcast(event="quit", user_id=user_id)
            )
