from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import TIMESTAMP
from app.core.database import Base
import datetime


class ProjectUser(Base):
    __tablename__ = "project_user"
    project_user_id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.project_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    role = Column(String)
    invitation_status = Column(String)
    invitation_time = Column(TIMESTAMP(timezone=True), default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="project_users")
    project = relationship("Project", back_populates="project_users")
