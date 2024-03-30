from sqlalchemy.orm import Session
from app.core.security import verify_password
from app.crud import user_crud
from app.core.exceptions import InvalidCredentialsError
from app.scheme.user_scheme import UserResponse


def rename_user(user_id: int, name: str, db: Session) -> UserResponse:
    user = user_crud.get_user_by_id(db, user_id)
    if user is None:
        raise InvalidCredentialsError

    user = user_crud.update_name(db, user, name)
    return UserResponse(
        id=user.user_id, email=user.esi_email, name=user.name, pfp=user.profile_picture
    )


def get_user(user_id: int, db: Session) -> UserResponse:
    user = user_crud.get_user_by_id(db, user_id)
    if user is None:
        raise InvalidCredentialsError

    return UserResponse(
        id=user.user_id, email=user.esi_email, name=user.name, pfp=user.profile_picture
    )


def set_password(
    user_id: int, old_password: str, new_password: str, db: Session
) -> UserResponse:
    user = user_crud.get_user_by_id(db, user_id)
    if user is None:
        raise InvalidCredentialsError

    if not (
        user.hash_passoword is None
        or verify_password(old_password, user.hash_passoword)
    ):
        raise InvalidCredentialsError

    user = user_crud.update_password(db, user, new_password)

    return UserResponse(
        id=user.user_id, email=user.esi_email, name=user.name, pfp=user.profile_picture
    )
