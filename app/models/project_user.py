from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class ProjectUser(Base):
    __tablename__ = "project_user"
    project_user_id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.project_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    role = Column(String)
    invitation_status = Column(String)

    user = relationship("User", back_populates="project_users")
    project = relationship("Project", back_populates="project_users")
