from typing import Annotated
from fastapi import Query, Depends, WebSocketException, status
from app.core.security import decode_access_token
from app.crud.session_crud import is_session_user, is_session_open
from app.dependencies import get_db
from sqlalchemy.orm import Session


def get_ws_user(access_token: Annotated[str, Query()]) -> int:
    return decode_access_token(access_token)


def valid_session_user_ws(
    user_id: Annotated[int, Depends(get_ws_user)],
    session_id: int,
    db: Session = Depends(get_db),
) -> int:
    if is_session_user(db, session_id, user_id):
        return user_id

    raise WebSocketException(
        code=status.WS_1008_POLICY_VIOLATION,
        reason="You're not a member of this session",
    )


def session_open_ws(session_id: int, db: Session = Depends(get_db)) -> int:
    if is_session_open(db, session_id):
        return session_id

    raise WebSocketException(
        code=status.WS_1008_POLICY_VIOLATION,
        reason="Session closed",
    )
