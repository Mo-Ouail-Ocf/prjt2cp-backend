from typing import Annotated
from fastapi import APIRouter, Depends
from app.dependencies.user import get_current_user

router = APIRouter()


@router.get("/current")
async def current(user_id: Annotated[int, Depends(get_current_user)]):
    return {"id": str(user_id)}
