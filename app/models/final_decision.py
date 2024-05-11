import datetime
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship
from app.core.database import Base


class FinalDecision(Base):
    __tablename__ = "final_decisions"
    decision_id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("sessions.session_id"))
    idea_id = Column(Integer, ForeignKey("ideas.idea_id"))
    rationale = Column(String)
    decision_date = Column(TIMESTAMP(timezone=True), default=datetime.datetime.utcnow)
    new_session_id = Column(Integer, ForeignKey("sessions.session_id"), nullable=True)

    session = relationship("Session", foreign_keys=[session_id])
    idea = relationship("Idea")
