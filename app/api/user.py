from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Form
from app.dependencies.user import get_current_user
from app.dependencies.database import get_db
from app.scheme.user import UserResponse
from app.services.user import get_user_by_id, update_name
from sqlalchemy.orm import Session


router = APIRouter()


@router.get("/current", response_model=UserResponse)
async def current(
    user_id: Annotated[int, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(500, "Something went wrong!")

    return UserResponse(id=user.user_id, email=user.esi_email, name=user.name)


@router.put("/name", response_model=UserResponse)
async def change_name(
    user_id: Annotated[int, Depends(get_current_user)],
    db: Session = Depends(get_db),
    name: str = Form(),
):
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(500, "Something went wrong!")

    user = update_name(db, user, name)
    return UserResponse(id=user.user_id, email=user.esi_email, name=user.name)
