from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.exceptions import (
    InvalidProjectError,
    InvalidProjectUserError,
    InvalidSessionError,
    NotModeratorError,
)
from app.crud.project_crud import get_project
from app.crud.session_crud import is_moderator, is_session_user, get_session
from app.dependencies import get_db, get_current_user
from app.crud.project_user_crud import is_project_moderator, is_project_user


def valid_project(project_id: int, db: Session = Depends(get_db)) -> int:
    project = get_project(db, project_id)
    if not project:
        raise InvalidProjectError

    return project_id


def valid_session(session_id: int, db: Session = Depends(get_db)) -> int:
    session = get_session(db, session_id)
    if not session:
        raise InvalidSessionError

    return session_id


def valid_project_user(
    user_id: Annotated[int, Depends(get_current_user)],
    project_id: Annotated[int, Depends(valid_project)],
    db: Session = Depends(get_db),
) -> int:
    if is_project_user(db, project_id, user_id):
        return user_id

    raise InvalidProjectUserError


def valid_project_moderator(
    user_id: Annotated[int, Depends(get_current_user)],
    project_id: Annotated[int, Depends(valid_project)],
    db: Session = Depends(get_db),
) -> int:
    if is_project_moderator(db, project_id, user_id):
        return user_id

    raise NotModeratorError


def valid_session_moderator(
    user_id: Annotated[int, Depends(get_current_user)],
    session_id: Annotated[int, Depends(valid_session)],
    db: Session = Depends(get_db),
) -> int:
    if is_moderator(db, session_id, user_id):
        return user_id

    raise NotModeratorError


def valid_session_user(
    user_id: Annotated[int, Depends(get_current_user)],
    session_id: Annotated[int, Depends(valid_session)],
    db: Session = Depends(get_db),
) -> int:
    if is_session_user(db, session_id, user_id):
        return user_id

    raise InvalidProjectUserError
