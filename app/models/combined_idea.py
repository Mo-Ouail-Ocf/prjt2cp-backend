from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class CombinedIdea(Base):
    __tablename__ = "combined_ideas"
    combined_idea_id = Column(Integer, ForeignKey("ideas.idea_id"), primary_key=True)
    source_idea_id = Column(Integer, ForeignKey("ideas.idea_id"), primary_key=True)

    source_idea = relationship(
        "Idea", foreign_keys=[source_idea_id], backref="contributed_to_combinations"
    )
    combined_idea = relationship(
        "Idea", foreign_keys=[combined_idea_id], backref="resulted_from_combinations"
    )
