from typing import Annotated
from fastapi import Query
from app.core.security import decode_access_token


def get_ws_user(access_token: Annotated[str, Query()]) -> int:
    return decode_access_token(access_token)
