import datetime
from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship, backref
from app.core.database import Base


class Idea(Base):
    __tablename__ = "ideas"
    idea_id = Column(Integer, primary_key=True)
    content = Column(Text)
    details = Column(Text, nullable=True)
    creation_date = Column(TIMESTAMP(timezone=True), default=datetime.datetime.utcnow)
    session_id = Column(Integer, ForeignKey("sessions.session_id"))
    submitter_id = Column(Integer, ForeignKey("users.user_id"))
    votes = Column(Integer, nullable=True)  # For dot voting
    parent_idea_id = Column(
        Integer, ForeignKey("ideas.idea_id"), nullable=True
    )  # For tracking idea expansions

    session = relationship("Session", back_populates="ideas")
    submitter = relationship("User", back_populates="ideas")
    comments = relationship("Comment", back_populates="idea")
    # For expansions
    expansions = relationship(
        "Idea", backref=backref("parent_idea", remote_side=[idea_id])
    )
