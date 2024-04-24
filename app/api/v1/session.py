from typing import Annotated
from fastapi import APIRouter, Depends
from app.dependencies import (
    get_db,
    valid_project_moderator,
    valid_session_moderator,
    valid_project_user,
)
from app.scheme.session_scheme import SessionCreate, SessionResponse, SessionUpdate
from sqlalchemy.orm import Session
from app.crud.session_crud import update_session, get_open_sessions
from app.services.session_service import (
    new_session,
    export_session_drive,
    export_session_file,
    export_session,
)


router = APIRouter()


@router.post("/project/{project_id}", response_model=SessionResponse)
async def create_a_session(
    _: Annotated[int, Depends(valid_project_moderator)],
    project_id: int,
    create_data: Annotated[SessionCreate, Depends()],
    db: Session = Depends(get_db),
):
    return await new_session(project_id, create_data, db)


@router.put("/{session_id}", response_model=SessionResponse)
async def update_a_session(
    _: Annotated[int, Depends(valid_session_moderator)],
    session_id: int,
    update_data: Annotated[SessionUpdate, Depends()],
    db: Session = Depends(get_db),
):
    return update_session(db, session_id, update_data)


@router.get("/project/{project_id}", response_model=list[SessionResponse])
async def get_open_sessions_for_a_project(
    _: Annotated[int, Depends(valid_project_user)],
    project_id: int,
    db: Session = Depends(get_db),
):
    return get_open_sessions(db, project_id)


@router.get("/{session_id}/")
async def session_as_json(
    _: Annotated[int, Depends(valid_session_moderator)],
    session_id: int,
    db: Session = Depends(get_db),
):
    return export_session(session_id, db)


@router.get("/{session_id}/download")
async def download_session_as_json(
    _: Annotated[int, Depends(valid_session_moderator)],
    session_id: int,
    db: Session = Depends(get_db),
):
    return export_session_file(session_id, db)


@router.post("/{session_id}/drive")
async def upload_session_to_drive(
    user_id: Annotated[int, Depends(valid_session_moderator)],
    session_id: int,
    db: Session = Depends(get_db),
):
    await export_session_drive(user_id, session_id, db)
