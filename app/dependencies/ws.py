from typing import Annotated
from fastapi import HTTPException, Query, WebSocketException, status
from app.core.security import decode_access_token


def get_ws_user(access_token: Annotated[str, Query()]) -> int:
    try:
        return decode_access_token(access_token)
    except HTTPException as e:
        raise WebSocketException(status.WS_1008_POLICY_VIOLATION, e.detail)
