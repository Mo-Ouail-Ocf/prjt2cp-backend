from datetime import datetime, timedelta
from jose import jwt
from jose.exceptions import JWTClaimsError
from app.core.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ACCESS_TOKEN_SECRET_KEY,
    REFRESH_TOKEN_SECRET_KEY,
    REFRESH_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
)
from fastapi.security import OAuth2AuthorizationCodeBearer
from passlib.context import CryptContext


oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://accounts.google.com/o/oauth2/auth?access_type=offline&prompt=consent",
    tokenUrl="/v1/auth/token",
    refreshUrl="/v1/auth/refresh",
    scopes={
        "openid": "OpenID Connect",
        "profile": "User profile",
        "email": "Email address",
        "https://www.googleapis.com/auth/drive": "Google drive access",
        "https://www.googleapis.com/auth/drive.file": "Google drive file access",
    },
)

password_contex = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return password_contex.hash(password)


def verify_password(password: str, hash: str) -> bool:
    return password_contex.verify(password, hash)


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
    payload = jwt.decode(
        refresh_token, REFRESH_TOKEN_SECRET_KEY, algorithms=[ALGORITHM]
    )
    client_id: str | None = payload.get("sub")
    if client_id is None:
        raise JWTClaimsError("Invalid signature")
    return int(client_id)


def decode_access_token(access_token: str) -> int:
    payload = jwt.decode(access_token, ACCESS_TOKEN_SECRET_KEY, algorithms=[ALGORITHM])
    client_id: str | None = payload.get("sub")
    if client_id is None:
        raise JWTClaimsError("Invalid signature")
    return int(client_id)
