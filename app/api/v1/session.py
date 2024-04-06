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
from app.crud.session_crud import create_session, update_session, get_open_sessions


router = APIRouter()


@router.post("/{project_id}", response_model=SessionResponse)
async def create(
    _: Annotated[int, Depends(valid_project_moderator)],
    project_id: int,
    create_data: Annotated[SessionCreate, Depends()],
    db: Session = Depends(get_db),
):
    return create_session(db, project_id, create_data)


@router.put("/{session_id}", response_model=SessionResponse)
async def update(
    _: Annotated[int, Depends(valid_session_moderator)],
    session_id: int,
    update_data: Annotated[SessionUpdate, Depends()],
    db: Session = Depends(get_db),
):
    return update_session(db, session_id, update_data)


@router.get("/{project_id}", response_model=list[SessionResponse])
async def get_open(
    _: Annotated[int, Depends(valid_project_user)],
    project_id: int,
    db: Session = Depends(get_db),
):
    return get_open_sessions(db, project_id)
