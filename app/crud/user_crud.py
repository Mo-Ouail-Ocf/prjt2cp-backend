from pydantic import AnyHttpUrl
from sqlalchemy.orm import Session
from app.core.security import hash_passowrd
from app.models import User
from app.scheme.user_scheme import UserCreate


def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.esi_email == email).first()


def get_user_by_id(db: Session, id: int) -> User:
    return db.query(User).filter(User.user_id == id).first()


def create_user(db: Session, user: UserCreate) -> User:
    # debug
    profile_picture_url = str(user.pfp) if user.pfp else None
    user = User(
        name=user.name, esi_email=user.email, profile_picture=profile_picture_url
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_pfp(db: Session, user: User, pfp: AnyHttpUrl) -> User:
    user.profile_picture = pfp
    db.commit()
    return user


def update_name(db: Session, user: User, name: str) -> User:
    user.name = name
    db.commit()
    return user


def update_password(db: Session, user: User, password: str) -> User:
    user.hash_passoword = hash_passowrd(password)
    db.commit()
    return user
