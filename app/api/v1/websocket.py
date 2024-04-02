from fastapi import APIRouter, WebSocket, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_ws_user
from app.dependencies import get_db
from app.websocket.session_ws import session_ws


router = APIRouter()


@router.websocket("/{session_id}")
async def session_websocket(
    websocket: WebSocket,
    session_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_ws_user),
):
    return await session_ws(websocket, session_id, user_id, db)
