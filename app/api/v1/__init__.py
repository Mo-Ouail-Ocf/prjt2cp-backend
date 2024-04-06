from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.user import router as user_router
from app.api.v1.project import router as project_router
from app.api.v1.ressource import router as ressource_router
from app.api.v1.websocket import router as ws_router
from app.api.v1.session import router as session_router


router = APIRouter()


router.include_router(
    auth_router,
    prefix="/auth",
    tags=["AUTH"],
    responses={
        401: {"description": "Coudn't validate credentials"},
        417: {"description": "Coudn't validate google user"},
        504: {"description": "Couldn't retrieve data"},
    },
)

router.include_router(
    user_router,
    prefix="/user",
    tags=["USER"],
    responses={
        401: {"description": "Coudn't validate credentials"},
        403: {"description": "Credentials expired"},
    },
)

router.include_router(ws_router, prefix="/ws")

router.include_router(
    project_router,
    prefix="/project",
    tags=["PROJECT"],
    responses={
        401: {"description": "Coudn't validate credentials"},
        403: {"description": "Credentials expired"},
    },
)

router.include_router(
    ressource_router,
    prefix="/ressource",
    tags=["RESSOURCE"],
    responses={
        401: {"description": "Coudn't validate credentials"},
        403: {"description": "Credentials expired"},
    },
)

router.include_router(
    session_router,
    prefix="/session",
    tags=["SESSION"],
    responses={
        401: {"description": "Coudn't validate credentials"},
        403: {"description": "Credentials expired"},
    },
)
