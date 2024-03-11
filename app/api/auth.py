from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from app.services.auth import generate_tokens, refresh_tokens
from app.scheme.auth import AuthRequestFrom, Token
from app.core.security import oauth2_scheme
from sqlalchemy.orm import Session
from app.dependencies.database import get_db

router = APIRouter()


@router.post("/token")
async def token(auth_data: Annotated[AuthRequestFrom, Depends()], db: Session = Depends(get_db)) -> Token:
    if auth_data is None:
        raise HTTPException(status_code=400, detail="Authorization data not provided")

    return await generate_tokens(auth_data.code, auth_data.redirect_uri, db)


@router.post("/refresh")
async def refresh_access_token(refresh_token: Annotated[str, Depends(oauth2_scheme)]) -> Token:
    return await refresh_tokens(refresh_token)
