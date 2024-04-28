from app.core.exceptions import InvalidCredentialsError
from app.scheme.auth_scheme import Token
from app.services.google_auth_service import (
    get_google_user_info,
    get_google_token,
)
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    verify_password,
)
from sqlalchemy.orm import Session
from app.scheme.google_scheme import GoogleToken, GoogleUserInfo
from app.crud import user_crud
from app.scheme.user_scheme import UserCreate


async def generate_tokens(code: str, redirect_uri: str, db: Session) -> Token:
    google_token: GoogleToken = await get_google_token(code, redirect_uri)
    user_info: GoogleUserInfo = await get_google_user_info(google_token.access_token)

    db_user = user_crud.get_user_by_email(db, user_info.email)

    if db_user is None:
        user = UserCreate(
            name=user_info.name,
            email=user_info.email,
            pfp=user_info.picture,
            google_refresh_token=google_token.refresh_token,
        )
        db_user = user_crud.create_user(db, user)
    elif google_token.refresh_token:
        user_crud.update_google_refresh_token(db, db_user, google_token.refresh_token)

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


async def login_with_credentials(db: Session, username: str, password: str) -> Token:
    email = f"{username}@esi.dz"
    user = user_crud.get_user_by_email(db, email)

    if user is None:
        raise InvalidCredentialsError

    if user.hash_password is None:
        raise InvalidCredentialsError

    if not verify_password(password, user.hash_password):
        raise InvalidCredentialsError

    access_token = create_access_token(user.user_id)
    refresh_token = create_refresh_token(user.user_id)

    return Token(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )
