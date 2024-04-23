from aiogoogle import Aiogoogle
import mimetypes
from aiogoogle.auth.creds import UserCreds
from app.core.config import drive_client_creds
from app.core.exceptions import DriveUploadError
from app.services.google_auth_service import refresh_google_access_token


async def retreive_drive_creds(google_refresh_token: str) -> UserCreds:
    google_creds = await refresh_google_access_token(google_refresh_token)

    return UserCreds(
        access_token=google_creds.access_token,
        refresh_token=google_refresh_token,
        expires_in=google_creds.expires_in or None,
    )


async def upload_drive_file(file_path: str, file_name: str, user_creds: UserCreds):
    try:
        async with Aiogoogle(
            user_creds=user_creds, client_creds=drive_client_creds
        ) as aiogoogle:
            drive_v3 = await aiogoogle.discover("drive", "v3")

            parent_id = await get_drive_directory_id(user_creds)

            req = drive_v3.files.create(
                upload_file=file_path,
                fields="id",
                json={"name": file_name, "parents": [parent_id]},
            )

            req.upload_file_content_type = mimetypes.guess_type(file_path)[0]
            await aiogoogle.as_user(req)

    except Exception:
        raise DriveUploadError


async def get_drive_directory_id(user_creds: UserCreds) -> str:
    try:
        async with Aiogoogle(
            user_creds=user_creds, client_creds=drive_client_creds
        ) as aiogoogle:
            drive_v3 = await aiogoogle.discover("drive", "v3")

            res = await aiogoogle.as_user(
                drive_v3.files.list(
                    q="name='tikta' and mimeType='application/vnd.google-apps.folder'"
                )
            )

            if len(res.get("files")) != 0:
                return res.get("files")[0].get("id")

            req = drive_v3.files.create(
                fields="id",
                json={
                    "name": "tikta",
                    "mimeType": "application/vnd.google-apps.folder",
                },
            )
            res = await aiogoogle.as_user(req)

            return res.get("id")

    except Exception:
        raise DriveUploadError
