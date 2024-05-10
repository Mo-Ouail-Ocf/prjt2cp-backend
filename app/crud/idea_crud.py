from sqlalchemy.orm import Session
from app.models import Idea
from app.scheme.idea_scheme import IdeaCreate, IdeaUpdate


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


def add_idea_vote(db: Session, idea_id: int):
    idea = db.query(Idea).filter(Idea.idea_id == idea_id).first()
    if not idea:
        return

    idea.votes += 1
    db.commit()


def get_ideas(db: Session, session_id: int) -> list[Idea]:
    return db.query(Idea).filter(Idea.session_id == session_id).all()


def update_idea(db: Session, idea_id: int, update_data: IdeaUpdate):
    idea = db.query(Idea).filter(Idea.idea_id == idea_id).first()
    if not idea:
        return

    for key, value in update_data.model_dump().items():
        if value != None:
            setattr(idea, key, value)

    db.commit()
    return idea
