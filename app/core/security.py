from datetime import datetime, timedelta
from jose import jwt
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, ACCESS_TOKEN_SECRET_KEY, REFRESH_TOKEN_SECRET_KEY, \
    REFRESH_TOKEN_EXPIRE_MINUTES, ALGORITHM
from fastapi.security import OAuth2AuthorizationCodeBearer
from app.core.exceptions import credentials_exception

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://accounts.google.com/o/oauth2/auth",
    tokenUrl="/auth/token",
    refreshUrl="/auth/refresh",
    scopes={"openid": "OpenID Connect",
            "profile": "User profile", "email": "Email address"}
)


def create_access_token(client_id: int):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(client_id)}
    encoded_jwt = jwt.encode(
        to_encode, ACCESS_TOKEN_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(client_id: int):
    expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(client_id)}
    encoded_jwt = jwt.encode(
        to_encode, REFRESH_TOKEN_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_refresh_token(refresh_token: str) -> int:
    try:
        payload = jwt.decode(
            refresh_token, REFRESH_TOKEN_SECRET_KEY, algorithms=[ALGORITHM])
        client_id: str | None = payload.get("sub")
        if client_id is None:
            raise credentials_exception
        return int(client_id)
    except:
        raise credentials_exception


def decode_access_token(access_token: str) -> int:
    try:
        payload = jwt.decode(
            access_token, ACCESS_TOKEN_SECRET_KEY, algorithms=[ALGORITHM])
        client_id: str | None = payload.get("sub")
        if client_id is None:
            raise credentials_exception
        id = int(client_id)
        return id
    except:
        raise credentials_exception
