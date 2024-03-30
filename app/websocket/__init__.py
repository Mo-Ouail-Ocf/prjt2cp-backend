from app.websocket.chat import router as chat_router
from fastapi import APIRouter

router = APIRouter()


router.include_router(chat_router, prefix="/chat")
