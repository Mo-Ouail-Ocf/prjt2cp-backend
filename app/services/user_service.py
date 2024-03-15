from sqlalchemy.orm import Session
from app.crud.user_crud import get_user_by_id, update_name
from app.core.exceptions import UnknownError
from app.scheme.user_scheme import UserResponse


def rename_user(user_id: int, db: Session, name: str) -> UserResponse:
    user = get_user_by_id(db, user_id)
    if user is None:
        raise UnknownError

    user = update_name(db, user, name)
    return UserResponse(id=user.user_id, email=user.esi_email, name=user.name)


def get_user(user_id: int, db: Session) -> UserResponse:
    user = get_user_by_id(db, user_id)
    if user is None:
        raise UnknownError

    return UserResponse(id=user.user_id, email=user.esi_email, name=user.name)
