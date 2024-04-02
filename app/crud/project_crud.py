from sqlalchemy.orm import Session, joinedload, contains_eager
from typing import List
from app.models.project import Project
from app.models.project_user import ProjectUser
from app.models.user import User
from app.scheme.project_scheme import (
    ProjectDisplay,
    ProjectUserDisplay,
    ResourceDisplay,
    UserBase,
)


def create_project(db: Session, project_data: dict) -> Project:
    project = Project(**project_data)
    db.add(project)
    db.commit()
    db.refresh(project)
    admin_project_user = ProjectUser(
        project_id=project.project_id,
        user_id=project.owner_id,
        role="Admin",
        invitation_status="done",
    )
    db.add(admin_project_user)
    db.commit()
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


def get_owned_projects(db: Session, user_id: int) -> List[ProjectDisplay]:
    # Fetch projects owned by the user, including their resources and participants
    projects = (
        db.query(Project)
        .join(Project.resource)  # Explicitly join the Resource table
        .options(
            contains_eager(
                Project.resource
            ),  # Contains eager will match projects with their resources
            joinedload(Project.project_users).joinedload(ProjectUser.user),
        )
        .filter(Project.owner_id == user_id)
        .all()
    )

    owned_projects = []
    for project in projects:
        # Construct participants list
        participants = [
            ProjectUserDisplay(
                user=UserBase(
                    user_id=pu.user.user_id,
                    name=pu.user.name,
                    email=pu.user.esi_email,  # Replace with actual email field name
                    image=pu.user.profile_picture,  # Replace with actual image field name
                ),
                role=pu.role,
                invitation_status=pu.invitation_status,
            )
            for pu in project.project_users
            if pu.user_id != user_id  # Exclude the owner from the participants list
        ]

        # Prepare project data including resource and participants
        project_data = ProjectDisplay(
            project_id=project.project_id,
            title=project.title,
            description=project.description,
            status=project.status,
            creation_date=project.creation_date,
            owner_id=project.owner_id,
            resource=ResourceDisplay.from_orm(project.resource)
            if project.resource
            else None,
            participants=participants,
        )
        owned_projects.append(project_data)

    return owned_projects


def get_participated_projects(db: Session, user_id: int) -> List[ProjectDisplay]:
    projects = (
        db.query(Project)
        .join(ProjectUser, ProjectUser.project_id == Project.project_id)
        .filter(
            ProjectUser.user_id == user_id, Project.owner_id != user_id
        )  # Exclude projects where the user is the owner
        .options(
            joinedload(Project.project_users).joinedload(ProjectUser.user),
            contains_eager(Project.resource),
        )
        .distinct()
        .all()
    )

    participated_projects = []
    for project in projects:
        # Construct participants list
        participants = [
            ProjectUserDisplay(
                user=UserBase.from_orm(pu.user),
                role=pu.role,
                invitation_status=pu.invitation_status,
            )
            for pu in project.project_users
            if pu.user_id
            != project.owner_id  # Optionally, exclude the owner from the participants list
        ]

        # Prepare project data including resource and participants
        project_data = ProjectDisplay(
            project_id=project.project_id,
            title=project.title,
            description=project.description,
            status=project.status,
            creation_date=project.creation_date,
            owner_id=project.owner_id,
            resource=ResourceDisplay.from_orm(project.resource)
            if project.resource
            else None,
            participants=participants,
        )
        participated_projects.append(project_data)

    return participated_projects


def invite_user_to_project(
    db: Session,
    project_id: int,
    user_id: int,
    role: str,
    invitation_status: str = "pending",
) -> ProjectUser:
    project_user = ProjectUser(
        project_id=project_id,
        user_id=user_id,
        role=role,
        invitation_status=invitation_status,
    )
    db.add(project_user)
    db.commit()
    db.refresh(project_user)
    return project_user


def get_pending_invitations(db: Session, user_id: int):
    result = (
        db.query(
            ProjectUser,
            Project.title,
            Project.details,
            User.name.label("creator_name"),
            User.email.label("creator_email"),
        )
        .join(Project, ProjectUser.project_id == Project.id)
        .join(User, Project.owner_id == User.id)
        .filter(
            ProjectUser.user_id == user_id, ProjectUser.invitation_status == "pending"
        )
        .all()
    )
    return result


def get_users(db: Session, project_id: int):
    return (
        db.query(User)
        .join(ProjectUser)
        .filter(ProjectUser.project_id == project_id)
        .all()
    )


def update_invitation_status(
    db: Session, project_id: int, user_id: int, status: str
) -> ProjectUser:
    project_user = (
        db.query(ProjectUser)
        .filter(ProjectUser.project_id == project_id, ProjectUser.user_id == user_id)
        .first()
    )
    project_user.invitation_status = status
    db.commit()
    db.refresh(project_user)
    return project_user
