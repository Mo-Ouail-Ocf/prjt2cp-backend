from app.models.auth import AccessTokenData, RefreshTokenData, Token
from app.services.google_auth import get_google_user_info, get_google_token
from app.core.security import create_access_token, create_refresh_token, decode_refresh_token
from app.core.exceptions import deserialize_exception


async def generate_tokens(code: str, redirect_uri: str) -> Token:
    google_token = await get_google_token(code, redirect_uri)
    user_info = await get_google_user_info(google_token)

    # user = get_user(user_info)

    # if not user:
    #     user = create_user(user_info)
    user = user_info

    try:
        access_token = create_access_token(AccessTokenData(**user))
        refresh_token = create_refresh_token(RefreshTokenData(**user))

        return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")
    except:
        raise deserialize_exception


async def refresh_tokens(refresh_token: str) -> Token:
    refresh_token_data = decode_refresh_token(refresh_token)
    # access_token_data = get_user_info(refresh_token_data.email)
    access_token_data = AccessTokenData(**refresh_token_data.dict())

    access_token = create_access_token(access_token_data)
    refresh_token = create_refresh_token(refresh_token_data)

    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")

