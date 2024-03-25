from fastapi import HTTPException, status


InvalidGoogleCridentialsError = HTTPException(
    status.HTTP_417_EXPECTATION_FAILED, detail="Couldn't validate google user"
)

InvalidCredentialsError = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
)

ExpiredCredentialsError = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Credentials expired",
)

UnknownError = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Unexpected error",
)

SlowConnectionError = HTTPException(
    status_code=status.HTTP_504_GATEWAY_TIMEOUT,
    detail="Couldn't retrieve data",
)
