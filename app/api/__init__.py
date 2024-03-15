from fastapi import APIRouter
from app.api.rest import rest_router
from app.api.ws import ws_router


router = APIRouter()

router.include_router(rest_router, prefix="")
router.include_router(ws_router, prefix="/ws")
