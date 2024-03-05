from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, LargeBinary
from sqlalchemy.orm import relationship
from database import Base
import datetime

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    esi_email = Column(String, unique=True, index=True)
    profile_picture = Column(LargeBinary)
    last_activity = Column(DateTime, default=datetime.datetime.utcnow)

    projects = relationship('Project', back_populates='owner')
    comments = relationship('Comment', back_populates='author')
    ideas = relationship('Idea', back_populates='submitter')

class Project(Base):
    __tablename__ = 'projects'

    project_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    status = Column(String)
    creation_date = Column(DateTime, default=datetime.datetime.utcnow)
    owner_id = Column(Integer, ForeignKey('users.user_id'))

    owner = relationship('User', back_populates='projects')
    sessions = relationship('Session', back_populates='project')
    resource_id = Column(Integer, ForeignKey('resources.resource_id'))
    resource = relationship('Resource', back_populates='projects')

class Resource(Base):
    __tablename__ = 'resources'

    resource_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String)
    level = Column(String)
    description = Column(Text)
    photo = Column(LargeBinary)

    projects = relationship('Project', back_populates='resource')

class Session(Base):
    __tablename__ = 'sessions'

    session_id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.project_id'))
    title = Column(String, index=True)
    description = Column(Text)
    ideation_technique = Column(String)
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    session_status = Column(String)
    objectives = Column(Text)

    project = relationship('Project', back_populates='sessions')
    ideas = relationship('Idea', back_populates='session')

class Idea(Base):
    __tablename__ = 'ideas'

    idea_id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    details = Column(Text)
    creation_date = Column(DateTime, default=datetime.datetime.utcnow)
    session_id = Column(Integer, ForeignKey('sessions.session_id'))
    submitter_id = Column(Integer, ForeignKey('users.user_id'))

    session = relationship('Session', back_populates='ideas')
    submitter = relationship('User', back_populates='ideas')
    comments = relationship('Comment', back_populates='idea')

class Comment(Base):
    __tablename__ = 'comments'

    comment_id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    creation_date = Column(DateTime, default=datetime.datetime.utcnow)
    idea_id = Column(Integer, ForeignKey('ideas.idea_id'))
    author_id = Column(Integer, ForeignKey('users.user_id'))

    idea = relationship('Idea', back_populates='comments')
    author = relationship('User', back_populates='comments')
