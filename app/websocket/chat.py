from typing import Dict, Annotated, Any
from fastapi import (
    APIRouter,
    WebSocket,
    Depends,
    WebSocketDisconnect,
    WebSocketException,
    status,
)
from sqlalchemy.orm import Session
from app.dependencies import get_ws_user
from app.crud.project_crud import get_project
from app.dependencies.database import get_db


router = APIRouter()


class ChatRoom:
    def __init__(self, id: int, users: list[int]):
        self.id = id
        self.white_list: list[int] = users
        self.active: list[WebSocket] = []

    async def connect(self, websocket: WebSocket, user_id):
        if user_id in self.white_list:
            await websocket.accept()
            self.active.append(websocket)
        else:
            await websocket.close(
                code=status.WS_1008_POLICY_VIOLATION,
                reason="User is not member of this project",
            )

    def disconnect(self, ws: WebSocket):
        self.active.remove(ws)

    async def send_msg(self, msg: str, ws: WebSocket):
        await ws.send_text(msg)

    async def broadcast(self, msg: str):
        for ws in self.active:
            await ws.send_text(msg)


class RoomManager:
    def __init__(self):
        self.rooms: Dict[int, ChatRoom] = {}

    def get_room(self, id: int, db: Session) -> ChatRoom:
        room = self.rooms.get(id)
        if room is not None:
            return room

        project = get_project(db, id)
        if project is None:
            raise WebSocketException(
                code=status.WS_1007_INVALID_FRAME_PAYLOAD_DATA,
                reason="Project doesn't exist",
            )

        room = ChatRoom(
            project.project_id, [user.user_id for user in project.project_users]
        )
        self.rooms.update({id: room})
        return room

    def remove_room(self, id: int):
        self.rooms.pop(id)


room_manager = RoomManager()


@router.websocket("/{project_id}")
async def ws_endpoint(
    *,
    project_id: int,
    ws: WebSocket,
    db: Session = Depends(get_db),
    user_id: Annotated[Any, Depends(get_ws_user)],
):
    room = room_manager.get_room(project_id, db)
    await room.connect(ws, user_id)
    try:
        while True:
            data = await ws.receive_text()
            await room.broadcast(f"message: {data}")

    except WebSocketDisconnect:
        room.disconnect(ws)
        await room.broadcast("someone disconnected")

    finally:
        if len(room.active) == 0:
            room_manager.remove_room(room.id)
