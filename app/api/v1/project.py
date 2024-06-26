from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated, List
from app.dependencies.database import get_db
from app.dependencies.project_user import valid_project_user
from app.models.user import User
from app.scheme.project_scheme import (
    ProjectCreate,
    ProjectUpdate,
    ProjectDisplay,
    PendingInvitationInfo,
    ProjectInvitationCreate,
    ProjectInvitationResponse,
    UpdateInvitation,
    SessionSchema,
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
    handle_invitation_response,
)
from app.dependencies.user import get_current_user
from app.services.user_service import get_user
from app.crud.user_crud import get_user_by_email
from app.crud.project_crud import (
    get_users,
    get_sessions_by_project_id,
    get_project_details,
)
from app.services.email_service import (
    send_invitation_email,
    send_invitation_response_email,
)

router = APIRouter()


@router.get("/{project_id}/", response_model=ProjectDisplay)
async def get_details(
    _: Annotated[int, Depends(valid_project_user)],
    project_id: int,
    db: Session = Depends(get_db),
):
    return get_project_details(db, project_id)


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
    invitations = project_service.read_pending_invitations(user_id, db)
    return [
        PendingInvitationInfo(
            project_id=invitation["project_id"],
            project_title=invitation["project_title"],
            project_description=invitation["project_description"],
            creator_name=invitation["creator_name"],
            creator_email=invitation["creator_email"],
            creator_image=invitation["creator_image"],
            invitation_time=invitation["invitation_time"],
        )
        for invitation in invitations
    ]


@router.put("/{project_id}/invite", response_model=ProjectInvitationResponse)
async def invite(
    project_id: int,
    email: ProjectInvitationCreate,
    bg_tasks: BackgroundTasks,
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
        return ProjectInvitationResponse(message="The user is already invited")
    message = invite_user(db, project_id, receiver.user_id, role="contributor")
    send_invitation_email(str(email.email), project.title, user.name, bg_tasks)
    return ProjectInvitationResponse(message=message["message"])


"""
this function must be testes as soon as possible
"""


@router.post("/{project_id}/invite", response_model=ProjectInvitationResponse)
async def handle_invitation(
    project_id: int,
    update_invitation: UpdateInvitation,
    bg_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    project = get_project(db, project_id)
    if project is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="project not found")
    user = db.query(User).filter(User.user_id == user_id).first()
    users = get_users(db, project_id)
    if not any(user.user_id == project_user.user_id for project_user in users):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail="user was not invited to the project"
        )
    if user.user_id == project.owner_id:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail="the user is the creator of the project"
        )
    creator = db.query(User).filter(User.user_id == project.owner_id).first()
    send_invitation_response_email(
        creator.esi_email, project.title, user.name, update_invitation.status, bg_tasks
    )
    handle_invitation_response(db, project_id, user_id, update_invitation.status)
    return ProjectInvitationResponse(message="Handling invitation success")


@router.get("/{project_id}/sessions", response_model=list[SessionSchema])
def get_sessions_for_project(
    project_id: int,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    users = get_users(db, project_id)
    user_found = any(user.user_id == user_id for user in users)
    if not user_found:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="not authorized"
        )
    sessions = get_sessions_by_project_id(db, project_id)
    return sessions
