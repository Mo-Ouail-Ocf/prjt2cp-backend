import httpx
from app.core.config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
from app.core.exceptions import google_exception
from fastapi import HTTPException


async def get_google_user_info(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}

    async with httpx.AsyncClient() as client:
        response = await client.get("https://www.googleapis.com/oauth2/v3/userinfo", headers=headers)
        if response.status_code == 200:
            return response.json()

        raise google_exception


async def get_google_token(code, redirect_uri):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post("https://oauth2.googleapis.com/token", data=data, headers=headers)
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get("access_token")
            return access_token

        raise google_exception


async def get_google_pfp(url) -> bytes:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            return response.content

        return bytes()
