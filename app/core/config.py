from dotenv import load_dotenv
from os import getenv
from fastapi_mail import ConnectionConfig

load_dotenv()


GOOGLE_CLIENT_ID = getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = getenv("GOOGLE_CLIENT_SECRET", "")

ACCESS_TOKEN_SECRET_KEY = getenv("ACCESS_TOKEN_SECRET_KEY", "")
REFRESH_TOKEN_SECRET_KEY = getenv("REFRESH_TOKEN_SECRET_KEY", "")

ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_MINUTES = 7 * 24 * 60
ALGORITHM = "HS256"

DATABASE_URL = getenv("DATABASE_URL", "")

# Email configurations
MAIL_USERNAME = getenv("MAIL_USERNAME", "")
MAIL_PASSWORD = getenv("MAIL_PASSWORD", "")
MAIL_FROM = getenv("MAIL_FROM", "")
MAIL_PORT = int(getenv("MAIL_PORT", 587))
MAIL_SERVER = getenv("MAIL_SERVER", "")
MAIL_TLS = getenv("MAIL_TLS", "True") == "True"
MAIL_SSL = getenv("MAIL_SSL", "False") == "True"

# Set up ConnectionConfig for FastAPI-Mail
mail_config = ConnectionConfig(
    MAIL_USERNAME=getenv("MAIL_USERNAME", ""),
    MAIL_PASSWORD=getenv("MAIL_PASSWORD", ""),
    MAIL_FROM=getenv("MAIL_FROM", ""),
    MAIL_PORT=int(getenv("MAIL_PORT", 587)),
    MAIL_SERVER=getenv("MAIL_SERVER", ""),
    MAIL_FROM_NAME=getenv("MAIL_FROM_NAME", "FastAPI Application"),  # Optional
    MAIL_STARTTLS=getenv("MAIL_STARTTLS", "True") == "True",
    MAIL_SSL_TLS=getenv("MAIL_SSL_TLS", "False") == "True",
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)
OPENAI_TOKEN = getenv("OPENAI_TOKEN","")