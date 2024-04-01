from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import relationship
from app.core.database import Base


class Resource(Base):
    __tablename__ = "resources"
    resource_id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    level = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    photo = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    owner = relationship("User", back_populates="owned_resources")
