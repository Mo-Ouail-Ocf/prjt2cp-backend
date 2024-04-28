import httpx
from app.core.config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
from app.core.exceptions import InvalidGoogleCridentialsError
from app.scheme.google_scheme import GoogleToken, GoogleUserInfo


async def get_google_user_info(access_token: str) -> GoogleUserInfo:
    headers = {"Authorization": f"Bearer {access_token}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://www.googleapis.com/oauth2/v3/userinfo", headers=headers
        )

        if response.status_code == 200:
            return GoogleUserInfo(**response.json())

        raise InvalidGoogleCridentialsError


async def get_google_token(code, redirect_uri) -> GoogleToken:
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://oauth2.googleapis.com/token", data=data, headers=headers
        )

        if response.status_code == 200:
            token_data = response.json()
            print(token_data)

            return GoogleToken.model_validate(token_data)

        raise InvalidGoogleCridentialsError


async def refresh_google_access_token(google_refresh_token: str) -> str:
    # TODO: test this
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "refresh_token": google_refresh_token,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "grant_type": "refresh_token",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://oauth2.googleapis.com/token", data=data, headers=headers
        )

        if response.status_code == 200:
            token_data = response.json()

            return token_data.get("access_token")

        raise InvalidGoogleCridentialsError
