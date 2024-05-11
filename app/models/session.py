import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship
from app.core.database import Base


class Session(Base):
    __tablename__ = "sessions"
    session_id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.project_id"))
    title = Column(String)
    description = Column(Text, nullable=True)
    ideation_technique = Column(String)
    start_time = Column(TIMESTAMP(timezone=True), default=datetime.datetime.utcnow)
    session_status = Column(String)
    objectives = Column(Text, nullable=True)
    round_time = Column(Integer)
    nb_rounds = Column(Integer, default=1)
    is_from_final_decision = Column(Boolean, default=False)

    project = relationship("Project", back_populates="sessions")
    ideas = relationship("Idea", back_populates="session")
