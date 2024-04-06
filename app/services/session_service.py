from sqlalchemy.orm import Session
from app.scheme.session_scheme import SessionCreate, SessionResponse, SessionUpdate


def create_session(create_data: SessionCreate, db: Session) -> SessionResponse:
    pass


def update_session(
    session_id: int, update_data: SessionUpdate, db: Session
) -> SessionResponse:
    pass
