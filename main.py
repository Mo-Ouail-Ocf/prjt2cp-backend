from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.api.auth import router as auth_router
from app.api.user import router as user_router
from app.core.config import GOOGLE_CLIENT_ID
from app.models import models
from app.database import engine

app = FastAPI(
    title="Backend", debug=True,
    swagger_ui_init_oauth={
        "clientId": GOOGLE_CLIENT_ID,
        "appName": "Oauth Demo",
        "scopes": "openid profile email",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(auth_router, prefix="/auth")
app.include_router(user_router, prefix="/user")


models.Base.metadata.create_all(bind=engine)