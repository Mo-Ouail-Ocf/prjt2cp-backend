from datetime import datetime, timedelta
from jose import jwt
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, ACCESS_TOKEN_SECRET_KEY, REFRESH_TOKEN_SECRET_KEY, REFRESH_TOKEN_EXPIRE_MINUTES, ALGORITHM
from app.scheme.auth import AccessTokenData, RefreshTokenData
from fastapi.security import OAuth2AuthorizationCodeBearer
from app.core.exceptions import credentials_exception


oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://accounts.google.com/o/oauth2/auth",
    tokenUrl="/auth/token",
    refreshUrl="/auth/refresh",
    scopes={"openid": "OpenID Connect", "profile": "User profile", "email": "Email address"}
)


def create_access_token(data: AccessTokenData):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(data.sub), "data": data.dict()}
    encoded_jwt = jwt.encode(to_encode, ACCESS_TOKEN_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: RefreshTokenData):
    expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(data.sub), "data": data.dict()}
    encoded_jwt = jwt.encode(to_encode, REFRESH_TOKEN_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_refresh_token(refresh_token: str) -> RefreshTokenData:
    try:
        payload = jwt.decode(refresh_token, REFRESH_TOKEN_SECRET_KEY, algorithms=[ALGORITHM])
        refresh_token_data: dict | None = payload.get("data")
        if refresh_token_data is None:
            raise credentials_exception
        return RefreshTokenData(**refresh_token_data)
    except: 
        raise credentials_exception

def decode_access_token(access_token: str) -> AccessTokenData:
    try:
        payload = jwt.decode(access_token, ACCESS_TOKEN_SECRET_KEY, algorithms=[ALGORITHM])
        access_token_data: dict | None = payload.get("data")
        if access_token_data is None:
            raise credentials_exception
        return AccessTokenData(**access_token_data)
    except:
        raise credentials_exception
