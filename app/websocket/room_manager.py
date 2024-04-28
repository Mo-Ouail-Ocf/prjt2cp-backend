from typing import Dict
from sqlalchemy.orm import Session
from app.websocket.ideation_room import IdeationRoom
from app.crud.session_crud import close_started_session, get_moderators


class RoomManager:
    def __init__(self):
        self.rooms: Dict[int, IdeationRoom] = {}

    def get_room(self, session_id: int, db: Session) -> IdeationRoom:
        room = self.rooms.get(session_id)

        if room is None:
            mods = get_moderators(db, session_id)
            room = IdeationRoom(session_id, mods)
            self.rooms.update({session_id: room})

        return room

    def delete_room(self, db: Session, session_id: int):
        if session_id in self.rooms.keys():
            self.rooms.pop(session_id)
            close_started_session(db, session_id)


# Global RoomManager instance
room_manager = RoomManager()
