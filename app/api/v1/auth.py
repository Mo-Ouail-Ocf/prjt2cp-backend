from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.services.auth_service import (
    generate_tokens,
    refresh_tokens,
    login_with_credentials,
)
from app.scheme.auth_scheme import AuthRequestFrom, Token
from app.core.security import oauth2_scheme
from sqlalchemy.orm import Session
from app.dependencies.database import get_db


router = APIRouter()


@router.post("/token")
async def token(
    auth_data: Annotated[AuthRequestFrom, Depends()], db: Session = Depends(get_db)
) -> Token:
    return await generate_tokens(auth_data.code, auth_data.redirect_uri, db)


@router.post("/refresh")
async def refresh(
    refresh_token: Annotated[str, Depends(oauth2_scheme)],
) -> Token:
    return await refresh_tokens(refresh_token)


@router.post("/login")
async def login(
    login_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> Token:
    username = login_data.username
    password = login_data.password
    return await login_with_credentials(db, username, password)
