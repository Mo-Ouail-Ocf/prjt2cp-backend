from typing import List, Dict
from fastapi import WebSocket

class IdeationRoom:
    def __init__(self, session_id: int):
        self.session_id = session_id
        self.active_users: List[WebSocket] = []

    async def connect_user(self, websocket: WebSocket):
        await websocket.accept()
        self.active_users.append(websocket)

    async def broadcast(self, message: dict, message_type: str):
        for user_ws in self.active_users:
            await user_ws.send_json({
                "type": message_type, 
                **message
            })

    def disconnect(self, ws: WebSocket):
        self.active_users.remove(ws)

class RoomManager:
    def __init__(self):
        self.rooms: Dict[int, IdeationRoom] = {}

    def get_room(self, session_id: int) -> IdeationRoom:
        if session_id not in self.rooms:
            self.rooms[session_id] = IdeationRoom(session_id)
        return self.rooms[session_id]

    def delete_room(self, session_id: int):
        if session_id in self.rooms:
            del self.rooms[session_id]
    
    def create_room(self, session_id: int):
        if session_id not in self.rooms:
            self.rooms[session_id] = IdeationRoom(session_id)

   