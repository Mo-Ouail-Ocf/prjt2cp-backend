from sqlalchemy.orm import Session, joinedload, contains_eager
from typing import List
from app.models.project import Project
from app.models.resource import Resource
from app.models.session import Session
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


def get_project_details(db: Session, project_id: int) -> ProjectDisplay:
    # Query the project with project_id
    project = db.query(Project).filter(Project.project_id == project_id).first()

    if project:
        # Query the related resource (if any)
        resource_data = None
        if project.resource_id:
            resource = db.query(Resource).filter(Resource.resource_id == project.resource_id).first()
            if resource:
                resource_data = {
                    "resource_id": resource.resource_id,
                    "name": resource.name,
                    "type": resource.type,
                    "level": resource.level,
                    "description": resource.description,
                    "photo": resource.photo,
                }

        # Query the participants (project users) and their related user details
        participants_data = []
        project_users = db.query(ProjectUser).filter(ProjectUser.project_id == project_id).all()
        for project_user in project_users:
            user = db.query(User).filter(User.user_id == project_user.user_id).first()
            if user:
                participant_data = {
                    "user": {  # Structure the user data within a 'user' key
                        "user_id": user.user_id,
                        "name": user.name,
                        "email":user.esi_email,
                        "image":user.profile_picture
                    },
                    "role": project_user.role,
                    "invitation_status": project_user.invitation_status,
                }
                participants_data.append(participant_data)

        # Create ProjectDisplay object with extracted data
        return ProjectDisplay(
            project_id=project.project_id,
            title=project.title,
            description=project.description,
            status=project.status,
            creation_date=project.creation_date,
            owner_id=project.owner_id,
            resource=resource_data,
            participants=participants_data,
        )

    return None  # or raise an exception if project not found

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
        .join(Project.resource)
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
                invitation_time=pu.invitation_time,
            )
            for pu in project.project_users
            if pu.user_id != user_id  # Exclude the owner from the participants list
        ]

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
            ProjectUser.user_id == user_id,
            Project.owner_id != user_id,
            ProjectUser.invitation_status == "accepted",
        )
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
            Project.project_id,
            Project.title,
            Project.description,
            User.name.label("creator_name"),
            User.esi_email.label("creator_email"),
            User.profile_picture.label("creator_image"),
            ProjectUser.invitation_time.label("invitation_time"),
        )
        .select_from(ProjectUser)
        .join(Project, ProjectUser.project_id == Project.project_id)
        .join(User, Project.owner_id == User.user_id)
        .filter(
            ProjectUser.user_id == user_id, ProjectUser.invitation_status == "pending"
        )
        .all()
    )
    return [
        {
            "project_id": project_id,
            "project_title": project_title,
            "project_description": project_description,
            "creator_name": creator_name,
            "creator_email": creator_email,
            "creator_image": creator_image,
            "invitation_time": invitation_time.isoformat(),
        }
        for project_id, project_title, project_description, creator_name, creator_email, creator_image, invitation_time in result
    ]


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

def get_sessions_by_project_id(db: Session, project_id: int):
    return db.query(Session).filter(Session.project_id == project_id).all()