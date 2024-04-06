from sqlalchemy.orm import Session
from app.models import ProjectUser


def is_project_moderator(db: Session, project_id: int, user_id: int) -> bool:
    user = (
        db.query(ProjectUser)
        .filter(ProjectUser.project_id == project_id)
        .filter(ProjectUser.user_id == user_id)
        .first()
    )

    if user is None:
        return False

    return user.invitation_status in ["accepted", "done"] and user.role in [
        "moderator",
        "Admin",
    ]


def is_project_user(db: Session, project_id: int, user_id: int) -> bool:
    user = (
        db.query(ProjectUser)
        .filter(ProjectUser.project_id == project_id)
        .filter(ProjectUser.user_id == user_id)
        .first()
    )

    if user is None:
        return False

    return user.invitation_status in ["accepted", "done"]
