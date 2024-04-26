from sqlalchemy.orm import Session
from app.models import ProjectUser, Session as IdeationSession
from app.scheme.session_scheme import SessionCreate, SessionUpdate
from datetime import datetime


def create_session(
    db: Session, project_id: int, session_data: SessionCreate
) -> IdeationSession:
    session = IdeationSession(
        project_id=project_id, session_status="open", **session_data.model_dump()
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_session(db: Session, session_id: int) -> IdeationSession:
    return (
        db.query(IdeationSession)
        .filter(IdeationSession.session_id == session_id)
        .first()
    )


def update_session(
    db: Session, session_id: int, update_data: SessionUpdate
) -> IdeationSession:
    session = get_session(db, session_id)

    if session:
        for key, value in update_data.model_dump().items():
            if value != None:
                setattr(session, key, value)

    db.commit()
    db.refresh(session)
    return session


def is_moderator(db: Session, session_id: int, user_id: int) -> bool:
    session = (
        db.query(IdeationSession)
        .filter(IdeationSession.session_id == session_id)
        .first()
    )
    if session is None:
        return False

    user = (
        db.query(ProjectUser)
        .filter(ProjectUser.project_id == session.project_id)
        .filter(ProjectUser.user_id == user_id)
        .first()
    )
    if user is None:
        return False

    return user.role in ["moderator", "Admin"]


def is_session_user(db: Session, session_id: int, user_id: int) -> bool:
    session = (
        db.query(IdeationSession)
        .filter(IdeationSession.session_id == session_id)
        .first()
    )
    if session is None:
        return False

    user = (
        db.query(ProjectUser)
        .filter(ProjectUser.project_id == session.project_id)
        .filter(ProjectUser.user_id == user_id)
        .first()
    )
    if user is None:
        return False

    return user.invitation_status in ["accepted", "done"]


def get_open_sessions(db: Session, project_id: int) -> list[IdeationSession]:
    return (
        db.query(IdeationSession)
        .filter(IdeationSession.project_id == project_id)
        .filter(IdeationSession.session_status == "open")
        .all()
    )


def get_closed_sessions(db: Session, project_id: int) -> list[IdeationSession]:
    return (
        db.query(IdeationSession)
        .filter(IdeationSession.project_id == project_id)
        .filter(IdeationSession.session_status == "closed")
        .all()
    )


def close_started_session(db: Session, session_id: int):
    session = get_session(db, session_id)

    if session and session.session_status == "started":
        session.session_status = "closed"

    db.commit()
    db.refresh(session)
    return session


def start_session(db: Session, session_id: int):
    session = get_session(db, session_id)

    if session:
        session.session_status = "started"
        session.start_time = datetime.utcnow()

    db.commit()
    db.refresh(session)
    return session


def is_session_open(db: Session, session_id: int) -> bool:
    session = (
        db.query(IdeationSession)
        .filter(IdeationSession.session_id == session_id)
        .first()
    )
    if session is None:
        return False

    return session.session_status == "open"
