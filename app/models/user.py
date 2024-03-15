import datetime
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import BYTEA, TIMESTAMP
from sqlalchemy.orm import relationship
from app.core.database import Base


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    name = Column(String)
    esi_email = Column(String, unique=True)
    profile_picture = Column(BYTEA)
    last_activity = Column(TIMESTAMP(timezone=True), default=datetime.datetime.utcnow)

    project_users = relationship("ProjectUser", back_populates="user")
    owned_projects = relationship("Project", back_populates="owner")
    comments = relationship("Comment", back_populates="author")
    ideas = relationship("Idea", back_populates="submitter")
    owned_resources = relationship("Resource", back_populates="owner")
