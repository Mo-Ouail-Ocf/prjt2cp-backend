from fastapi import FastAPI
from httpx import TimeoutException
from jose.exceptions import JWTError
from app.core.exceptions import httpx_error_hander, jwt_error_handler
from starlette.middleware.cors import CORSMiddleware
from app.api import router
from app.core.config import GOOGLE_CLIENT_ID
from app.core.database import Base, engine


app = FastAPI(
    title="Backend",
    debug=True,
    swagger_ui_init_oauth={
        "clientId": GOOGLE_CLIENT_ID,
        "appName": "Backned",
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

app.include_router(router, prefix="")

app.add_exception_handler(JWTError, jwt_error_handler)
app.add_exception_handler(TimeoutException, httpx_error_hander)


Base.metadata.create_all(bind=engine)
