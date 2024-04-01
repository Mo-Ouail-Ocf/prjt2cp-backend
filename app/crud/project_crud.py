from sqlalchemy.orm import Session, joinedload
from typing import List
from app.models.project import Project
from app.models.project_user import ProjectUser


def create_project(db: Session, project_data: dict) -> Project:
    project = Project(**project_data)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def get_project(db: Session, project_id: int) -> Project:
    return db.query(Project).filter(Project.project_id == project_id).first()


def update_project(db: Session, project_id: int, update_data: dict) -> Project:
    project = get_project(db, project_id)
    if project:
        for key, value in update_data.items():
            setattr(project, key, value)
        db.commit()
    return project


def delete_project(db: Session, project_id: int):
    project = get_project(db, project_id)
    if project:
        db.delete(project)
        db.commit()


def get_owned_projects(db: Session, user_id: int) -> List[Project]:
    return (
        db.query(Project)
        .options(joinedload(Project.project_users).joinedload(ProjectUser.user))
        .filter(Project.owner_id == user_id)
        .all()
    )


def get_participated_projects(db: Session, user_id: int) -> List[Project]:
    return (
        db.query(Project)
        .join(ProjectUser, Project.project_id == ProjectUser.project_id)
        .options(joinedload(Project.project_users).joinedload(ProjectUser.user))
        .filter(ProjectUser.user_id == user_id, ProjectUser.role != "owner")
        .distinct()
        .all()
    )


def get_project_users(db: Session, project_id: int) -> List[ProjectUser]:
    return db.query(ProjectUser).filter(ProjectUser.project_id == project_id).all()
