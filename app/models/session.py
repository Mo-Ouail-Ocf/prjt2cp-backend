import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Text
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

    project = relationship("Project", back_populates="sessions")
    ideas = relationship("Idea", back_populates="session")
