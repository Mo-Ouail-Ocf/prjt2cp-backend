from sqlalchemy.orm import Session
from app.models.models import User
from app.scheme.user import UserCreate


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.esi_email == email).first()


def create_user(db: Session, user: UserCreate):
    user = User(name=user.name, esi_email=user.email, profile_picture=user.pfp)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
