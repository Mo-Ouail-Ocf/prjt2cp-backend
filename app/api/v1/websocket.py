from fastapi import APIRouter, WebSocket, Depends, WebSocketDisconnect
from sqlalchemy.orm import Session
from app.websocket.room_manager import room_manager
from app.core.security import get_current_user
from app.core.database import get_db
from app.crud import save_idea  # Assume this is a function you've defined to save ideas

router = APIRouter()

@router.websocket("/ws/session/{session_id}")
async def session_websocket(websocket: WebSocket, session_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    ideation_room = room_manager.get_room(session_id)
    await ideation_room.connect_user(websocket)

    try:
        while True:
            data = await websocket.receive_json()
            if data['type'] == 'chat':
                await ideation_room.broadcast(data['content'], "chat")
            elif data['type'] == 'idea':
                # Here, you could save the idea to the database and then broadcast it
                save_idea(db, data['content'], current_user, session_id)
                await ideation_room.broadcast(data['content'], "idea")
    except WebSocketDisconnect:
        ideation_room.disconnect(websocket)
        await ideation_room.broadcast("someone disconnected")