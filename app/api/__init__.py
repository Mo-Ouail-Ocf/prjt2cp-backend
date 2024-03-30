from fastapi import APIRouter
from app.api.v1 import rest_router


router = APIRouter()

router.include_router(rest_router, prefix="/v1")
