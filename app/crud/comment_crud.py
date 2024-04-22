from sqlalchemy.orm import Session
from app.models import Comment
from app.scheme.comment_scheme import CommentCreate


def create_comment(db: Session, comment_data: CommentCreate) -> Comment:
    comment = Comment(
        author_id=comment_data.author_id,
        idea_id=comment_data.idea_id,
        content=comment_data.content,
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def get_commnets_by_ideas(db: Session, idea_id: int) -> list[Comment]:
    return db.query(Comment).filter(Comment.idea_id == idea_id).all()
