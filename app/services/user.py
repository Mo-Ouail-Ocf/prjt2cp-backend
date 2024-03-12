from sqlalchemy.orm import Session
from app.models.models import User
from app.scheme.user import UserCreate


def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.esi_email == email).first()


def create_user(db: Session, user: UserCreate) -> User:
    user = User(name=user.name, esi_email=user.email, profile_picture=user.pfp)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_id(db: Session, id: int) -> User:
    return db.query(User).filter(User.user_id == id).first()


def update_pfp(db: Session, user: User, pfp: bytes) -> User:
    user.profile_picture = pfp
    db.commit()
    return user


def update_name(db: Session, user: User, name: str) -> User:
    user.name = name
    db.commit()
    return user
