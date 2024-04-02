from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.dependencies.database import get_db
from app.scheme.project_scheme import (
    ProjectCreate,
    ProjectUpdate,
    ProjectDisplay,
    PendingInvitationInfo,
    ProjectInvitationCreate,
    ProjectInvitationResponse,
    UpdateInvitation,
)
from app.services import project_service
from app.services.project_service import (
    create_and_return_project,
    update_existing_project,
    remove_project,
    fetch_owned_projects,
    fetch_participated_projects,
    get_project,
    invite_user,
)
from app.dependencies.user import get_current_user
from app.services.user_service import get_user
from app.crud.user_crud import get_user_by_email
from app.crud.project_crud import get_users
from app.services.email_service import (
    send_invitation_email,
    send_invitation_response_email,
)

router = APIRouter()


@router.post("/", response_model=ProjectDisplay)
def create_project(
    project_create: ProjectCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    project_data_with_owner = project_create.model_dump()
    project_data_with_owner["owner_id"] = user_id
    project = create_and_return_project(db, project_data_with_owner)
    return project


@router.get("/user/owned", response_model=List[ProjectDisplay])
def read_owned_projects(
    db: Session = Depends(get_db), user_id: int = Depends(get_current_user)
):
    return fetch_owned_projects(db, user_id)


@router.get("/user/participated", response_model=List[ProjectDisplay])
def read_participated_projects(
    db: Session = Depends(get_db), user_id: int = Depends(get_current_user)
):
    return fetch_participated_projects(db, user_id)


@router.put("/{project_id}", response_model=ProjectDisplay)
def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    # Fetch the existing project to check ownership
    existing_project = get_project(db, project_id)
    if not existing_project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Authorization check: Ensure the user is the project owner
    if existing_project.owner_id != user_id:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this project"
        )

    # Proceed with update if authorized
    updated_project = update_existing_project(
        db, project_id, project_update.model_dump()
    )
    return updated_project


@router.delete("/{project_id}", status_code=204)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    # Fetch the project to check ownership
    project_to_delete = get_project(db, project_id)
    if not project_to_delete:
        raise HTTPException(status_code=404, detail="Project not found")

    # Authorization check: Ensure the user is the project owner
    if project_to_delete.owner_id != user_id:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this project"
        )

    remove_project(db, project_id)
    return {"message": "Project deleted successfully"}


@router.get("/user/pending-invitations", response_model=List[PendingInvitationInfo])
def read_pending_invitations(
    user_id: int = Depends(get_current_user), db: Session = Depends(get_db)
):
    invitations = project_service.get_pending_invitations(db, user_id)
    return [
        PendingInvitationInfo(
            project_title=invitation.Project.title,
            project_description=invitation.Project.description,
            creator_name=invitation.User.creator_name,
            creator_email=invitation.User.creator_email,
        )
        for invitation in invitations
    ]


@router.put("/{project_id}/invite", response_model=ProjectInvitationResponse)
async def invite(
    project_id: int,
    email: ProjectInvitationCreate,
    db: Session = Depends(get_db),
    sender_id: int = Depends(get_current_user),
):
    project = get_project(db, project_id)
    if project is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="project not found")
    user = get_user(sender_id, db)
    if project.owner_id != sender_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    receiver = get_user_by_email(db, str(email.email))
    if receiver is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
        )
    users = get_users(db, project_id)
    if receiver in users:
        return ProjectInvitationResponse("The user is already invited")
    message = invite_user(db, project_id, receiver.user_id, role="contributor")
    await send_invitation_email(str(email.email), project.title, user.name)
    return ProjectInvitationResponse(message=message["message"])


"""
this function must be testes as soon as possible
"""


@router.post("/{project_id}/invite", response_model=ProjectInvitationResponse)
async def handle_invitation(
    project_id: int,
    update_invitation: UpdateInvitation,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    project = get_project(db, project_id)
    if project is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="project not found")
    user = get_user(user_id, db)
    users = get_users(db, project_id)
    if user not in users:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail="user was not invited to the project"
        )
    if user.user_id == project.owner_id:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail="the user is the creator of the project"
        )
    creator = get_user(project.owner_id)
    await send_invitation_response_email(
        creator.email, project.title, user.name, update_invitation.status
    )
    return ProjectInvitationResponse("Handling invitation success")
