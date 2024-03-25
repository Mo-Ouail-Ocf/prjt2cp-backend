import datetime
from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship
from app.core.database import Base


class Comment(Base):
    __tablename__ = "comments"
    comment_id = Column(Integer, primary_key=True)
    content = Column(Text)
    creation_date = Column(TIMESTAMP(timezone=True), default=datetime.datetime.utcnow)
    idea_id = Column(Integer, ForeignKey("ideas.idea_id"))
    author_id = Column(Integer, ForeignKey("users.user_id"))

    idea = relationship("Idea", back_populates="comments")
    author = relationship("User", back_populates="comments")
