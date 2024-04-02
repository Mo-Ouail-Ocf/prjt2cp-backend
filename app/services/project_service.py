# project_service.py
from sqlalchemy.orm import Session
from typing import List
from app.crud import project_crud
from app.crud.project_crud import (
    create_project,
    update_project,
    delete_project,
    get_owned_projects,
    get_participated_projects,
    invite_user_to_project,
)
from app.models.project import Project
from app.models.project_user import (
    ProjectUser,
)  


def create_and_return_project(db: Session, project_data: dict) -> Project:
    return create_project(db, project_data)


def update_existing_project(db: Session, project_id: int, update_data: dict) -> Project:
    return update_project(db, project_id, update_data)


def remove_project(db: Session, project_id: int):
    delete_project(db, project_id)


def fetch_owned_projects(db: Session, user_id: int) -> List[Project]:
    return get_owned_projects(db, user_id)


def fetch_participated_projects(db: Session, user_id: int) -> List[Project]:
    return get_participated_projects(db, user_id)


def get_project(db: Session, project_id: int) -> Project:
    return project_crud.get_project(db, project_id)


def read_pending_invitations(user_id: int, db: Session):
    return project_crud.get_pending_invitations(db, user_id)


def invite_user(db: Session, project_id: int, user_id: int, role: str) -> dict:
    project_user = invite_user_to_project(
        db, project_id, user_id, role, invitation_status="pending"
    )
    return {"message": f"User {user_id} invited to project {project_id} as {role}"}


def handle_invitation_response(
    db: Session, project_id: int, user_id: int, accept: bool
) -> ProjectUser:
    status = "accepted" if accept else "refused"
    project_user = project_crud.update_invitation_status(
        db, project_id, user_id, status
    )
    return project_user
