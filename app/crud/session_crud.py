from sqlalchemy.orm import Session
from app.models import ProjectUser, Session as IdeationSession
from app.scheme.session_scheme import SessionCreate, SessionUpdate


def create_session(db: Session, session_data: SessionCreate) -> IdeationSession:
    session = IdeationSession(
        project_id=session_data.project_id,
        title=session_data.title,
        description=session_data.description,
        ideation_technique=session_data.ideation_technique,
        session_status=session_data.session_status,
        objectives=session_data.objectives,
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

    return user.role == "moderator"


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

    return user.invitation_status == "accepted"
