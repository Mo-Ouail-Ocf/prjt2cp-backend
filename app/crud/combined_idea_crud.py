from sqlalchemy.orm import Session
from app.models import CombinedIdea
from app.scheme.combined_idea_scheme import CombinedIdeaCreate


def create_combined_idea(db: Session, comment_data: CombinedIdeaCreate) -> CombinedIdea:
    combined_idea = CombinedIdea(
        source_idea_id=comment_data.source_idea_id,
        combined_idea_id=comment_data.combined_idea_id,
    )
    db.add(combined_idea)
    db.commit()
    db.refresh(combined_idea)
    return combined_idea
