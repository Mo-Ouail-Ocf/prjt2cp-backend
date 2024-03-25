from datetime import datetime, timedelta
from jose import ExpiredSignatureError, jwt
from jose.exceptions import JWTClaimsError, JWTError
from app.core.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ACCESS_TOKEN_SECRET_KEY,
    REFRESH_TOKEN_SECRET_KEY,
    REFRESH_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
)
from fastapi.security import OAuth2AuthorizationCodeBearer
from app.core.exceptions import InvalidCredentialsError, ExpiredCredentialsError


oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://accounts.google.com/o/oauth2/auth",
    tokenUrl="/auth/token",
    refreshUrl="/auth/refresh",
    scopes={
        "openid": "OpenID Connect",
        "profile": "User profile",
        "email": "Email address",
    },
)


def create_access_token(client_id: int):
    exp = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": exp, "sub": str(client_id)}
    encoded_jwt = jwt.encode(to_encode, ACCESS_TOKEN_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(client_id: int):
    exp = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": exp, "sub": str(client_id)}
    encoded_jwt = jwt.encode(to_encode, REFRESH_TOKEN_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_refresh_token(refresh_token: str) -> int:
    try:
        payload = jwt.decode(
            refresh_token, REFRESH_TOKEN_SECRET_KEY, algorithms=[ALGORITHM]
        )
        client_id: str | None = payload.get("sub")
        if client_id is None:
            raise InvalidCredentialsError
        return int(client_id)
    except ExpiredSignatureError:
        raise ExpiredCredentialsError

    except (JWTClaimsError, JWTError):
        raise InvalidCredentialsError


def decode_access_token(access_token: str) -> int:
    try:
        payload = jwt.decode(
            access_token, ACCESS_TOKEN_SECRET_KEY, algorithms=[ALGORITHM]
        )
        client_id: str | None = payload.get("sub")
        if client_id is None:
            raise InvalidCredentialsError
        return int(client_id)

    except ExpiredSignatureError:
        raise ExpiredCredentialsError

    except (JWTClaimsError, JWTError):
        raise InvalidCredentialsError
