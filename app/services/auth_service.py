from app.scheme.auth_scheme import Token
from app.services.google_auth_service import (
    get_google_user_info,
    get_google_token,
    get_google_pfp,
)
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
)
from sqlalchemy.orm import Session
from app.scheme.auth_scheme import GoogleUserInfo
from app.crud.user_crud import get_user_by_email, create_user
from app.scheme.user_scheme import UserCreate


async def generate_tokens(code: str, redirect_uri: str, db: Session) -> Token:
    google_token: str = await get_google_token(code, redirect_uri)
    user_info: GoogleUserInfo = await get_google_user_info(google_token)

    db_user = get_user_by_email(db, user_info.email)

    if db_user is None:
        pfp = await get_google_pfp(user_info.picture)
        user = UserCreate(name=user_info.name, email=user_info.email, pfp=pfp)
        db_user = create_user(db, user)

    access_token = create_access_token(db_user.user_id)
    refresh_token = create_refresh_token(db_user.user_id)

    return Token(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )


async def refresh_tokens(refresh_token: str) -> Token:
    user_id = decode_refresh_token(refresh_token)

    access_token = create_access_token(user_id)
    refresh_token = create_refresh_token(user_id)

    return Token(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )
