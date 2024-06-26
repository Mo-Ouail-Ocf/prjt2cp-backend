from typing import Optional
from pydantic import BaseModel
from fastapi import Form


class AuthRequestFrom:
    def __init__(
        self,
        grant_type: str = Form(regex="authorization_code"),
        client_id: Optional[str] = Form(default=None),
        client_secret: Optional[str] = Form(default=None),
        code: str = Form(),
        redirect_uri: str = Form(),
    ):
        self.grant_type = grant_type
        self.client_id = client_id
        self.client_secret = client_secret
        self.code = code
        self.redirect_uri = redirect_uri


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
