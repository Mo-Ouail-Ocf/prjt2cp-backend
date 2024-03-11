import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Text, create_engine
from sqlalchemy.dialects.postgresql import BYTEA, TIMESTAMP
from sqlalchemy.orm import relationship , backref
# Assuming Base is imported from your 'database' module as you've mentioned
from app.database import Base


class ProjectUser(Base):
    __tablename__ = 'project_user'
    project_user_id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.project_id'))
    user_id = Column(Integer, ForeignKey('users.user_id'))
    role = Column(String)
    invitation_status = Column(String)

    user = relationship("User", back_populates="project_users")
    project = relationship("Project", back_populates="project_users")

class Resource(Base):
    __tablename__ = 'resources'
    resource_id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    level = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    photo = Column(BYTEA, nullable=True)
    owner_id = Column(Integer, ForeignKey('users.user_id'), nullable=True)
    owner = relationship('User', back_populates='owned_resources')

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    name = Column(String)
    esi_email = Column(String, unique=True)
    profile_picture = Column(BYTEA)
    last_activity = Column(TIMESTAMP(timezone=True), default=datetime.datetime.utcnow)

    project_users = relationship("ProjectUser", back_populates="user")
    owned_projects = relationship('Project', back_populates='owner')
    comments = relationship('Comment', back_populates='author')
    ideas = relationship('Idea', back_populates='submitter')
    owned_resources = relationship('Resource', back_populates='owner')

class Project(Base):
    __tablename__ = 'projects'
    project_id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text)
    status = Column(String)
    creation_date = Column(TIMESTAMP(timezone=True), default=datetime.datetime.utcnow)
    owner_id = Column(Integer, ForeignKey('users.user_id'))
    resource_id = Column(Integer, ForeignKey('resources.resource_id'))

    owner = relationship('User', back_populates='owned_projects')
    project_users = relationship("ProjectUser", back_populates="project")
    sessions = relationship('Session', back_populates='project')
    resource = relationship('Resource', backref='projects')

class Session(Base):
    __tablename__ = 'sessions'
    session_id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.project_id'))
    title = Column(String)
    description = Column(Text, nullable=True)
    ideation_technique = Column(String)
    start_time = Column(TIMESTAMP(timezone=True), default=datetime.datetime.utcnow)
    session_status = Column(String)
    objectives = Column(Text, nullable=True)

    project = relationship('Project', back_populates='sessions')
    ideas = relationship('Idea', back_populates='session')

class Idea(Base):
    __tablename__ = 'ideas'
    idea_id = Column(Integer, primary_key=True)
    content = Column(Text)
    details = Column(Text, nullable=True)
    creation_date = Column(TIMESTAMP(timezone=True), default=datetime.datetime.utcnow)
    session_id = Column(Integer, ForeignKey('sessions.session_id'))
    submitter_id = Column(Integer, ForeignKey('users.user_id'))
    votes = Column(Integer, nullable=True)  # For dot voting
    parent_idea_id = Column(Integer, ForeignKey('ideas.idea_id'), nullable=True)  # For tracking idea expansions

    session = relationship('Session', back_populates='ideas')
    submitter = relationship('User', back_populates='ideas')
    comments = relationship('Comment', back_populates='idea')
    # For expansions
    expansions = relationship('Idea', backref=backref('parent_idea', remote_side=[idea_id]))

class CombinedIdea(Base):
    __tablename__ = 'combined_ideas'
    combined_idea_id = Column(Integer, ForeignKey('ideas.idea_id'), primary_key=True)
    source_idea_id = Column(Integer, ForeignKey('ideas.idea_id'), primary_key=True)

    source_idea = relationship('Idea', foreign_keys=[source_idea_id], backref='contributed_to_combinations')
    combined_idea = relationship('Idea', foreign_keys=[combined_idea_id], backref='resulted_from_combinations')

class Comment(Base):
    __tablename__ = 'comments'
    comment_id = Column(Integer, primary_key=True)
    content = Column(Text)
    creation_date = Column(TIMESTAMP(timezone=True), default=datetime.datetime.utcnow)
    idea_id = Column(Integer, ForeignKey('ideas.idea_id'))
    author_id = Column(Integer, ForeignKey('users.user_id'))

    idea = relationship('Idea', back_populates='comments')
    author = relationship('User', back_populates='comments')


