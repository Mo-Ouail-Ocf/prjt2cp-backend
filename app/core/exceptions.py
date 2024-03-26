from fastapi import HTTPException, WebSocket, status, Request 
from fastapi.responses import JSONResponse
from jose import JWTError, ExpiredSignatureError
from httpx import RequestError


InvalidGoogleCridentialsError = HTTPException(
    status.HTTP_417_EXPECTATION_FAILED,
    detail="Couldn't validate google user"
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


async def jwt_error_handler(request: Request, exc: JWTError) -> JSONResponse:
    if isinstance(exc, ExpiredSignatureError):
        code = status.HTTP_403_FORBIDDEN
    else:
        code = status.HTTP_401_UNAUTHORIZED

    return JSONResponse(
        status_code=code,
        content={"detail": f"JWT: {exc}"},
    ) 


async def httpx_error_hander(request: Request, exc: RequestError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_504_GATEWAY_TIMEOUT,
        content={"detail": f"Couldn't retrieve data"},
    ) 


async def jwt_ws_error_handler(websocket: WebSocket, exc: JWTError) -> None:
    await websocket.close(
        code=status.WS_1008_POLICY_VIOLATION,
        reason=f"JWT: {exc}"
    )
