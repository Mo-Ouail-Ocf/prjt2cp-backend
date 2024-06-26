from fastapi import APIRouter, WebSocket, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db, valid_session_user_ws, session_open_ws
from app.websocket.session_ws import session_ws


router = APIRouter()


@router.websocket("/{session_id}")
async def session_websocket(
    websocket: WebSocket,
    session_id: int = Depends(session_open_ws),
    db: Session = Depends(get_db),
    user_id: int = Depends(valid_session_user_ws),
):
    return await session_ws(websocket, session_id, user_id, db)
