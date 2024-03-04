from typing import Annotated
from fastapi import Depends
from app.core.security import decode_access_token, oauth2_scheme


def get_current_user(access_token: Annotated[str, Depends(oauth2_scheme)]):
    return decode_access_token(access_token)

