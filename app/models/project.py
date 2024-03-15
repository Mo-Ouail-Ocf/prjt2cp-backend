import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship
from app.core.database import Base


class Project(Base):
    __tablename__ = "projects"
    project_id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text)
    status = Column(String)
    creation_date = Column(TIMESTAMP(timezone=True), default=datetime.datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("users.user_id"))
    resource_id = Column(Integer, ForeignKey("resources.resource_id"))

    owner = relationship("User", back_populates="owned_projects")
    project_users = relationship("ProjectUser", back_populates="project")
    sessions = relationship("Session", back_populates="project")
    resource = relationship("Resource", backref="projects")
