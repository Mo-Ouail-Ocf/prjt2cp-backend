from sqlalchemy.orm import Session
from app.crud.combined_idea_crud import get_combined_idea
from app.crud.comment_crud import get_commnets_by_ideas
from app.crud.idea_crud import get_ideas
from app.crud.session_crud import get_session
from app.scheme.session_scheme import SessionExport


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
