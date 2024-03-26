from app.core.exceptions import InvalidCredentialsError
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
    verify_password,
)
from sqlalchemy.orm import Session
from app.scheme.auth_scheme import GoogleUserInfo
from app.crud import user_crud
from app.scheme.user_scheme import UserCreate


async def generate_tokens(code: str, redirect_uri: str, db: Session) -> Token:
    google_token: str = await get_google_token(code, redirect_uri)
    user_info: GoogleUserInfo = await get_google_user_info(google_token)

    db_user = user_crud.get_user_by_email(db, user_info.email)

    if db_user is None:
        pfp = await get_google_pfp(user_info.picture)
        user = UserCreate(name=user_info.name, email=user_info.email, pfp=pfp)
        db_user = user_crud.create_user(db, user)

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

    if user.hash_passoword is None:
        raise InvalidCredentialsError

    if not verify_password(password, user.hash_passoword):
        raise InvalidCredentialsError

    access_token = create_access_token(user.user_id)
    refresh_token = create_refresh_token(user.user_id)

    return Token(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )
