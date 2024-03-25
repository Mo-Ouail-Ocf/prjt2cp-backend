from fastapi import APIRouter
from app.api.rest.auth import router as auth_router
from app.api.rest.user import router as user_router


rest_router = APIRouter()

rest_router.include_router(
    auth_router,
    prefix="/auth",
    tags=["AUTH"],
    responses={
        417: {"description": "Coudn't validate google user"},
        504: {"description": "Couldn't retrieve data"},
    },
)
rest_router.include_router(
    user_router,
    prefix="/user",
    tags=["USER"],
    responses={
        401: {"description": "Coudn't validate credentials"},
        403: {"description": "Credentials expired"},
    },
)
