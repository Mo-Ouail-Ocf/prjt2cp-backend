from sqlalchemy.orm import Session
from app.models import Idea
from app.scheme.idea_scheme import IdeaCreate


def create_idea(db: Session, idea_data: IdeaCreate) -> Idea:
    idea = Idea(
        content=idea_data.content,
        details=idea_data.details,
        session_id=idea_data.session_id,
        submitter_id=idea_data.submitter_id,
        parent_idea_id=idea_data.parent_idea_id,
    )
    db.add(idea)
    db.commit()
    db.refresh(idea)
    return idea
