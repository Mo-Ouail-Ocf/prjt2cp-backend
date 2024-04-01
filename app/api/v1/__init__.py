from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.user import router as user_router
from app.api.v1.project import router as project_router
from app.api.v1.ressource import router as ressource_router
rest_router = APIRouter()

rest_router.include_router(
    auth_router,
    prefix="/auth",
    tags=["AUTH"],
    responses={
        401: {"description": "Coudn't validate credentials"},
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
rest_router.include_router(
    project_router,
    prefix="/project",
    tags=["PROJECT"],
    responses={
        401: {"description": "Coudn't validate credentials"},
        403: {"description": "Credentials expired"},
    },
)
rest_router.include_router(
    ressource_router,
    prefix="/ressource",
    tags=["RESSOURCE"],
    responses={
        401: {"description": "Coudn't validate credentials"},
        403: {"description": "Credentials expired"},
    },
)


