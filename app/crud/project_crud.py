from sqlalchemy.orm import Session
from app.models import Project


def get_project(db: Session, id: int) -> Project:
    return db.query(Project).filter(Project.project_id == id).first()
