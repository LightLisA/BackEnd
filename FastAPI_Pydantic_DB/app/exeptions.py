from fastapi import HTTPException, status

HTTPException_UserAlreadyExists = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User has already existed",
    headers={"WWW-Authenticate": "Bearer"},
)

HTTPException_IncorrectEmailOrPassword = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect password or email",
    headers={"WWW-Authenticate": "Bearer"},
)

HTTPException_TokenExpired = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token has expired..",
    headers={"WWW-Authenticate": "Bearer"},
)

HTTPException_InvalidToken = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid Token",
    headers={"WWW-Authenticate": "Bearer"},
)

HTTPException_IncorrectTokenFormat = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect token format",
    headers={"WWW-Authenticate": "Bearer"},
)

HTTPException_UserIdNotFound = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Used ID hasn't found",
    headers={"WWW-Authenticate": "Bearer"},
)

HTTPException_UserNotFound = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="User hasn't found",
    headers={"WWW-Authenticate": "Bearer"},
)

