from typing import Optional
from pydantic import BaseModel


class GoogleUserInfo(BaseModel):
    sub: int
    name: str
    given_name: str
    family_name: str
    picture: str
    email: str
    email_verified: bool
    # locale: str
    hd: str


class GoogleToken(BaseModel):
    access_token: str
    expires_in: int
    refresh_token: Optional[str] = None
    scope: str
    token_type: str
    id_token: str
