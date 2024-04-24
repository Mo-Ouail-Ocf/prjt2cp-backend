from sqlalchemy.orm import Session
from app.core.exceptions import UnknownError
from app.crud.combined_idea_crud import get_combined_idea
from app.crud.comment_crud import get_commnets_by_ideas
from app.crud.idea_crud import get_ideas
from app.crud.project_crud import get_project, get_users
from app.crud.session_crud import get_session, create_session
from app.crud.user_crud import get_user_by_id
from app.scheme.session_scheme import SessionCreate, SessionExport, SessionResponse
import tempfile
from fastapi import Response
from app.services.drive_service import (
    retreive_drive_creds,
    upload_drive_file,
)
from app.services.email_service import send_session_email


async def new_session(
    project_id: int, create_data: SessionCreate, db: Session
) -> SessionResponse:
    session = create_session(db, project_id, create_data)
    project = get_project(db, project_id)

    if session:
        raise UnknownError

    for user in get_users(db, project_id):
        await send_session_email(user.esi_email, project.title)

    return session


def export_session(session_id: int, db: Session):
    metadata = get_session(db, session_id)
    ideas = get_ideas(db, session_id)
    comments = []
    combined_ideas = []
    for idea in ideas:
        comments += get_commnets_by_ideas(db, idea.idea_id)
        combined_ideas += get_combined_idea(db, idea.idea_id)

    return SessionExport(
        metadata=metadata, ideas=ideas, comments=comments, combined_ideas=combined_ideas
    )


async def export_session_drive(user_id: int, session_id: int, db: Session):
    user = get_user_by_id(db, user_id)
    user_creds = await retreive_drive_creds(user.google_refresh_token)

    session = export_session(session_id, db)
    file_name = f"session_{session_id}.json"
    with tempfile.NamedTemporaryFile() as fp:
        fp.write(str.encode(session.model_dump_json()))
        fp.flush()

        await upload_drive_file(fp.name, file_name, user_creds)


def export_session_file(session_id: int, db: Session) -> Response:
    session = export_session(session_id, db)
    return Response(
        str.encode(session.model_dump_json()),
        media_type="application/txt",
        headers={
            "Content-Disposition": f'attachment; filename="session_{session_id}.json"'
        },
    )
