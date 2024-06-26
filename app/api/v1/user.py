from typing import Annotated
from fastapi import APIRouter, Depends, Form
from app.dependencies import get_current_user, get_db
from app.scheme.user_scheme import UserResponse
from sqlalchemy.orm import Session
from app.services.user_service import rename_user, get_user, set_password


router = APIRouter()


@router.get("/current", response_model=UserResponse)
async def current(
    user_id: Annotated[int, Depends(get_current_user)], db: Session = Depends(get_db)
):
    return get_user(user_id, db)


@router.put("/name", response_model=UserResponse)
async def name(
    user_id: Annotated[int, Depends(get_current_user)],
    db: Session = Depends(get_db),
    name: str = Form(),
):
    return rename_user(user_id, name, db)


@router.put("/password", response_model=UserResponse)
async def change_password(
    user_id: Annotated[int, Depends(get_current_user)],
    db: Session = Depends(get_db),
    old_password: str = Form(default=""),
    new_password: str = Form(),
):
    return set_password(user_id, old_password, new_password, db)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    return get_user(user_id, db)
