from typing import Dict
from app.websocket.ideation_room import IdeationRoom


class RoomManager:
    def __init__(self):
        self.rooms: Dict[int, IdeationRoom] = {}

    def get_room(self, session_id: int) -> IdeationRoom:
        room = self.rooms.get(session_id)

        if room is None:
            room = IdeationRoom(session_id)
            self.rooms.update({session_id: room})

        return room

    def delete_room(self, session_id: int):
        if session_id in self.rooms.keys():
            self.rooms.pop(session_id)


# Global RoomManager instance
room_manager = RoomManager()
