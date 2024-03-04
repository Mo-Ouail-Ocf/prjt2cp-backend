from fastapi import APIRouter, Depends
from app.dependencies.user import get_current_user


router = APIRouter()


@router.get("/current")
async def current(user = Depends(get_current_user)):
    return user
