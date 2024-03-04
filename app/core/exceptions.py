from fastapi import HTTPException, status

# TODO make good exception and status code

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"}
)

google_exception = HTTPException(
    status.HTTP_417_EXPECTATION_FAILED,
    detail="Couldn't validate google user"
)

deserialize_exception = HTTPException(
    status.HTTP_422_UNPROCESSABLE_ENTITY,
    "Couldn't deserialize data"
)

